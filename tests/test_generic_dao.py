import logging
from os.path import exists
import unittest

from db import Db
from generic_dao import GenericDao


class TestGenericDao(unittest.TestCase):

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

    db_name = "generic_dao_test"

    test_data = [
        {
            "id": 1,
            "data": "Mairzy doats and dozy doats"
        },
        {
            "id": 2,
            "data": "Four score and seven years ago"
        }
    ]

    def test_generic_dao(self):

        # Calculate expected answers from the database
        expected_1 = (TestGenericDao.test_data[0]["id"], TestGenericDao.test_data[0]["data"])
        expected_2 = (TestGenericDao.test_data[1]["id"], TestGenericDao.test_data[1]["data"])

        # Make sure we're not overwriting a database
        if exists(f'{TestGenericDao.db_name}.db'):
            logging.fatal(f"Database test file '{TestGenericDao.db_name}.db' already exists. Aborting.")
            return

        # Create the database and dao
        db = Db(TestGenericDao.db_name)
        dao = TestGenericDao.TestDao()

        # Test non-existence
        self.assertFalse(db.does_table_exist(dao),
                         f"Database table '{dao.table_name}' already exists")

        # Test creation
        db.create_table(dao)
        self.assertTrue(db.does_table_exist(dao),
                        f"Database table does not exist after creation")

        # Test empty count
        self.assertEqual(dao.get_count(db), 0,
                         f"Database table contains rows when none entered")

        # Add one record
        try:
            dao.create(db, TestGenericDao.test_data[0])
        except Exception as e:
            self.fail(f"Create of first record failed with exception {e}")

        # Test single count
        self.assertEqual(dao.get_count(db), 1,
                         f"Incorrect number of records after one create")

        # Add a second record
        try:
            dao.create(db, TestGenericDao.test_data[1])
        except Exception as e:
            self.fail(f"Create of second record failed with exception {e}")

        # Test second count
        self.assertEqual(dao.get_count(db), 2,
                         f"Incorrect number of records after two creates")

        # Read all records
        try:
            result = dao.read(db, 0, 2, "id", False)
        except Exception as e:
            self.fail(f"Read all record failed with exception {e}")

        # Verify read records
        self.assertEqual(result, [expected_1, expected_2],
                         f"All results {result} do not match expected {[expected_1, expected_2]}")

        # Test sorting 1
        try:
            result = dao.read(db, 0, 2, "id", True)
        except Exception as e:
            self.fail(f"Read sorting 1 failed with exception {e}")

        # Verify read records
        self.assertEqual(result, [expected_2, expected_1],
                         f"Sorting 1 results {result} do not expected output")

        # Test sorting 2
        try:
            result = dao.read(db, 0, 2, "data", False)
        except Exception as e:
            self.fail(f"Read sorting 2 failed with exception {e}")

        # Verify read records
        self.assertEqual(result, [expected_2, expected_1],
                         f"Sorting 2 results {result} do not expected output")

        # Test sorting 3
        try:
            result = dao.read(db, 0, 2, "data", True)
        except Exception as e:
            self.fail(f"Read sorting 3 failed with exception {e}")

        # Verify read records
        self.assertEqual(result, [expected_1, expected_2],
                         f"Sorting 3 results {result} do not expected output")

        # Test read limit
        try:
            result = dao.read(db, 0, 1, "id", False)
        except Exception as e:
            self.fail(f"Read limit failed with exception {e}")

        # Verify read records
        self.assertEqual(result, [expected_1],
                         f"Read limit results {result} do not match {[expected_1]}")

        # Test read offset
        try:
            result = dao.read(db, 1, 1, "id", False)
        except Exception as e:
            self.fail(f"Read offset failed with exception {e}")

        # Verify read records
        self.assertEqual(result, [expected_2],
                         f"Read offset results {result} do not match {[expected_2]}")

        # Test clear_table
        try:
            dao.clear_table(db)
        except Exception as e:
            self.fail(f"Clear table failed with exception {e}")

        # Verify clear_table
        self.assertEqual(dao.get_count(db), 0,
                         f"Table is not empty after clear table is called")

        # Clean up
        db.delete_table(dao)
        db.destroy()


if __name__ == '__main__':
    unittest.main()
