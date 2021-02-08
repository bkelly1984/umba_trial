import logging

class GenericDao:
    """
    This abstract class contains information and parameters to manipulate a database table.

     Attributes:
            table_name (str): the name of this table in the database.
            columns (list): the names of the columns in this table.
            column_types (list): the data types of the columns in this table.
            primary_key_index (int): the index of the table primary key.
    """

    @property
    def table_name(self):
        raise NotImplementedError

    @property
    def columns(self):
        raise NotImplementedError

    @property
    def column_types(self):
        raise NotImplementedError

    @property
    def primary_key_index(self):
        raise NotImplementedError

    def clear_table(self, db):
        """
        Delete all records from the table.

        Parameters:
            db (Db): the database on which to operate.

        Returns: None
        """

        logging.info(f"Clearning {self.table_name} table")
        db.cursor.execute(f"DELETE FROM {self.table_name}")
        db.commit()

    def create_or_clear_table(self, db):
        """
        End with an empty table in the database regardless of starting state.

        Parameters:
            db (Db): the database on which to operate.

        Returns: None
        """

        if db.does_table_exist(self):
            self.clear_table(db)
        else:
            db.create_table(self)

    def get_count(self, db):
        """
        Get the number of records for this table in the passed database.

        Parameters:
            db (Db): the database on which to operate.

        Returns:
            int: the number of records in the table.
       """

        return db.cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}").fetchone()[0]

    def create(self, db, value_dict):
        """
        Create a new record in this table on the passed database.

        Parameters:
            db (Db): the database on which to operate.
            value_dict (dict): The values of the new record in order of columns

        Returns: None
        """

        # Check that we were passed a dict object
        if not isinstance(value_dict, dict):
            logging.error(f"create passed an object of type {type(value_dict)}")
            return

        # Create a list of new values in order of the table columns
        value_list = []
        for column_name in self.columns:
            if column_name in value_dict:
                value_list.append(value_dict[column_name])
            else:
                logging.warning(f"value_dict does not contain a value for field {column_name}")
                value_list.append(None)

        # Write a row to the database
        sql_string = f"INSERT INTO {self.table_name} VALUES ({', '.join('?' * len(self.columns))})"
        logging.debug(f"Executing create: {sql_string}")
        db.cursor.execute(sql_string, value_list)

    def read(self, db, offset, limit, sort_by, desc_flag=False):
        """
        Read records in this table from the passed database and return them in a list.

        Parameters:
            db (Db): the database on which to operate.
            offset (int): The number of records to skip before returning results
            limit (int): The maximum number of records to return, capped by Db.max_limit
            sort_by (string): The name of the column on which to sort
            desc_flag (bool): Sort in descending order rather than ascending?

        Returns:
            list: A list of all the records found with the passed paramerers.
        """

        # Check the passed offset and limit
        if offset < 0:
            logging.warning(f"invalid offset of {offset} for table {self.table_name}, setting to 0")
            offset = 0

        if limit < 0:
            logging.warning(f"invalid limit of {limit} for table {self.table_name}, setting to 0")
            limit = 0
        elif limit > db.max_limit:
            logging.warning(f"limit of {limit} exceeds maximum, setting to {db.max_limit} records")
            limit = db.max_limit

        # Set a default order_string
        if not sort_by:
            order_string = f"{self.columns[0]} ASC"

        # Parse, verify, and convert the passed sort parameters
        elif sort_by.lower() in self.columns:
            if self.column_types[self.columns.index(sort_by.lower())] == "text":
                order_string = f"LOWER({sort_by.lower()})"
            else:
                order_string = f"{sort_by.lower()}"

            if desc_flag:
                order_string = f"{order_string} DESC"
            else:
                order_string = f"{order_string} ASC"
        else:
            logging.warning(f"invalid sort_by column {sort_by} for table {self.table_name}")

        # Build the SQL -- two layers so it can be filtered by result numbers
        sql_string = f"""SELECT {', '.join([f"a.{x}" for x in self.columns])}, (SELECT COUNT(*) FROM 
                {self.table_name} b WHERE a.id >= b.id) as row_num FROM {self.table_name} a
                WHERE row_num > ? AND row_num <= ? ORDER BY {order_string}"""

        logging.debug(f"Executing read: {sql_string}")
        return db.cursor.execute(sql_string, (offset, offset + limit)).fetchall()
