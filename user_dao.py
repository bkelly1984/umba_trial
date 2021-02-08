from generic_dao import GenericDao


class UserDao(GenericDao):
    """
    This defines the name and structure of the git_user table.

     Attributes:
            UserDao.table_name (str): the name of this table in the database.
            UserDao.columns (list): the names of the columns in this table.
            UserDao.column_types (list): the data types of the columns in this table.
            UserDao.primary_key_index (int): the index of the table primary key.
    """

    @property
    def table_name(self):
        return "git_user"

    @property
    def columns(self):
        return ["login", "id", "node_id", "avatar_url", "html_url", "type", "site_admin"]

    @property
    def column_types(self):
        return ["text", "integer", "text", "text", "text", "text", "text"]

    @property
    def primary_key_index(self):
        return 1
