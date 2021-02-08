import logging
from os.path import exists
import unittest

from db import Db
from generic_dao import GenericDao


class TestDb(unittest.TestCase):

    class TestDao(GenericDao):

        @property
        def table_name(self):
            return "test_table"

        @property
        def columns(self):
            return ["id", "data"]

        @property
        def column_types(self):
            return ["integer", "text"]

        @property
        def primary_key_index(self):
            return 0

    db_name = "db_test"

    # Test database creation
    def test_db(self):

        # Make sure we're not overwriting a database
        if exists(f'{TestDb.db_name}.db'):
            logging.fatal(f"Database test file '{TestDb.db_name}.db' already exists. Aborting.")
            return

        # Create the database
        db = Db(TestDb.db_name)
        self.assertTrue(exists(f"{TestDb.db_name}.db"),
                        f"Database file '{TestDb.db_name}.db' does not exist after creation")

        # Test a commit
        try:
            db.commit()
        except Exception as e:
            self.fail(f"Database commit failed with exception {e}")

        # Make sure test table does not exist
        dao = TestDb.TestDao()
        self.assertFalse(db.does_table_exist(dao),
                         f"Database table '{dao.table_name}' exists before creation")

        # Create the table
        try:
            db.create_table(dao)
        except Exception as e:
            self.fail(f"Table create failed with exception {e}")

        # Verify the table was created
        self.assertTrue(db.does_table_exist(dao),
                         f"Database table '{dao.table_name}' does not exist after creation")

        # Delete the table
        try:
            db.delete_table(dao)
        except Exception as e:
            self.fail(f"Table delete failed with exception {e}")

        # Verify the table was deleted
        self.assertFalse(db.does_table_exist(dao),
                         f"Database table '{dao.table_name}' exists after deletion")

        # Test the destruction of the database
        db.destroy()
        self.assertFalse(exists(f"{TestDb.db_name}.db"),
                         f"Database file '{TestDb.db_name}.db' exists after destruction")


if __name__ == '__main__':
    unittest.main()
