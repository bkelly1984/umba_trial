import logging
import os
import sqlite3


class Db:
    """
    This is a representation a sqlite3 database with modification hooks which will operate with generic_dao objects.

    Attributes:
        max_records (int): the largest number of records that can possibly be handled by the database.
        max_limit (int): the largest number of records to be returned in any query.
    """

    max_records = pow(2, 64)
    max_limit = 100

    def __init__(self, name='github'):
        """
        This Db class constructor.

        Parameters:
            name (string): name and non-suffixed filename of the database.
        """

        self.db_name = name
        self.filename = f'{self.db_name}.db'
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

    def destroy(self):
        """
        Close the database connections and delete the underlying file.

        Parameters: None
        Returns: None
        """

        self.cursor.close()
        self.connection.close()
        os.remove(self.filename)

    def commit(self):
        """
        Write any pending operations to the database.

        Parameters: None
        Returns: None
        """

        self.connection.commit()

    def does_table_exist(self, dao):
        """
        Checks to see if a the table name in a dao exists in the database.

        Parameters:
            dao (GenericDao): The table name to look for.

        Returns:
            bool: Does the table name exist in the database?
        """

        sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{dao.table_name}'"
        return bool(self.cursor.execute(sql).fetchone())

    def create_table(self, dao):
        """
        Creates a table in the database defined by the passed dao object.

        Parameters:
            dao (GenericDao): The table name to create.

        Returns: None
        """

        logging.info(f"Creating {dao.table_name} table")
        col_list = [f"{c} {t}" for c, t in zip(dao.columns, dao.column_types)]
        col_list[dao.primary_key_index] = f"{col_list[dao.primary_key_index]} primary key"
        self.cursor.execute(f"CREATE TABLE {dao.table_name} ({', '.join(col_list)})")
        self.commit()

    def delete_table(self, dao):
        """
        Deletes a table in the database with the same name as the passed dao object.

        Parameters:
            dao (GenericDao): The table name to delete.

        Returns: None
        """

        logging.info(f"Deleting {dao.table_name} table")
        self.cursor.execute(f"DROP TABLE {dao.table_name}")
        self.commit()

