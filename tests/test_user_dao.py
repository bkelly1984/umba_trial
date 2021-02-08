import logging
from os.path import exists
import unittest

from db import Db
from user_dao import UserDao


class TestUserDao(unittest.TestCase):

    db_name = "user_dao_test"

    def test_user_dao(self):

        # Make sure we're not overwriting a database
        if exists(f'{TestUserDao.db_name}.db'):
            logging.fatal(f"Database test file '{TestUserDao.db_name}.db' already exists. Aborting.")
            return

        # Create the database and dao
        db = Db(TestUserDao.db_name)
        dao = UserDao()

        # Test non-existence
        self.assertFalse(db.does_table_exist(dao),
                         f"User table exists before creation")

        # Test creation
        try:
            db.create_table(dao)
        except Exception as e:
            self.fail(f"Create user table failed with exception {e}")

        self.assertTrue(db.does_table_exist(dao),
                        f"User table does not exist after creation")

        # Test empty count
        self.assertEqual(dao.get_count(db), 0,
                         f"User table contains rows when none entered")

        # Test deletion
        try:
            db.delete_table(dao)
        except Exception as e:
            self.fail(f"Delete user table failed with exception {e}")

        self.assertFalse(db.does_table_exist(dao),
                         f"User table exists after deletion")

        # Clean up
        db.destroy()


if __name__ == '__main__':
    unittest.main()
