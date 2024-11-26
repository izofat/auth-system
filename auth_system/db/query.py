from datetime import datetime

from .connection import DbConnection


class BaseQuery:  # pylint: disable=too-few-public-methods
    def __init__(self, connection):
        self._connection = connection

    def execute_query(self, query: str, *args, is_commit: bool = False):
        with self._connection as conn:
            cursor = conn.cursor(dictionary=True)

            try:
                cursor.execute(query, (*args,))
                if is_commit:
                    conn.commit()
                    return cursor.rowcount

                result = cursor.fetchall()
                return result

            except Exception as e:
                raise e
            finally:
                cursor.close()


class TableQueries(BaseQuery):
    def create_user_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS user(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(25) NOT NULL,
                password VARCHAR(300) NOT NULL,
                name VARCHAR(100) NOT NULL,
                lastName VARCHAR(100) NOT NULL,
                email VARCHAR(254) NOT NULL,
                emailVerified BOOL NOT NULL DEFAULT FALSE,
                createdAt DATETIME DEFAULT NOW(),
                updatedAt DATETIME DEFAULT NOW()
            )
        """
        return self.execute_query(query)

    def create_token_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS token(
                id INT AUTO_INCREMENT PRIMARY KEY,
                userId INT NOT NULL,
                jwtToken VARCHAR(2000) NOT NULL,
                jwtExpireDate DATETIME NOT NULL,
                createdAt DATETIME DEFAULT NOW(),
                FOREIGN KEY (userId) REFERENCES user(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )
        """
        return self.execute_query(query)


class SelectQueries(BaseQuery):
    def get_user(self, username: str):
        query = """
            SELECT * FROM user WHERE username = %s 
        """
        return self.execute_query(query, username)

    def get_token(self, user_id: int):
        query = """
            SELECT id, userId, jwtToken, jwtExpireDate FROM token 
            WHERE userId = %s
            ORDER BY jwtExpireDate DESC
            LIMIT 1
        """
        return self.execute_query(query, user_id)


class InsertQueries(BaseQuery):
    def register_account(
        self, username: str, password: str, name: str, lastName: str, email: str
    ):
        query = """
            INSERT IGNORE INTO user (username, password, name, lastName, email)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(
            query, username, password, name, lastName, email, is_commit=True
        )

    def insert_token(self, user_id: int, jwt_token: str, jwt_expire_date: datetime):
        query = """
            INSERT INTO token (userId, jwtToken, jwtExpireDate)
            VALUES (%s, %s, %s)
        """
        return self.execute_query(
            query, user_id, jwt_token, jwt_expire_date, is_commit=True
        )


class Query:
    def __init__(self):
        self.connection = DbConnection()
        self._tables = TableQueries(self.connection)
        self._select = SelectQueries(self.connection)
        self._insert = InsertQueries(self.connection)

        self._tables.create_user_table()
        self._tables.create_token_table()

    def get_user(self, username: str):
        return self._select.get_user(username)

    def get_token(self, user_id: int):
        return self._select.get_token(user_id)

    def register_account(
        self, username: str, password: str, name: str, lastName: str, email: str
    ):
        return self._insert.register_account(username, password, name, lastName, email)

    def insert_token(self, user_id: int, jwt_token: str, jwt_expire_date: datetime):
        return self._insert.insert_token(user_id, jwt_token, jwt_expire_date)
