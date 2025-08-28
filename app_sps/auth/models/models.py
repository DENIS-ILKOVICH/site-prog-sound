from itsdangerous import URLSafeTimedSerializer
from datetime import datetime

class Users:
    def __init__(self, db):
        """
        Initialize Users with a database connection.
        """
        if db is None:
            raise ValueError("Database connection is not established.")
        self.__db = db
        self.__cur = db.cursor()

    def get_user_by_email(self, mail):
        """
        Retrieve an active user by email.
        """
        try:
            self.__cur.execute('SELECT * FROM users WHERE email = ? and status = 1 LIMIT 1', (mail.lower(),))
            res = self.__cur.fetchone()
            if res:
                return res
        except Exception as e:
            print(e)
        return False

    def adduser(self, name, email, hpsw):
        """
        Add a new user to the database if not already registered.
        """
        try:
            self.__cur.execute("SELECT COUNT(*) FROM users WHERE email LIKE ?", (email,))
            res = self.__cur.fetchone()
            if res[0] > 0:
                return False

            last_id = self.__cur.execute('SELECT id FROM users ORDER BY id DESC LIMIT 1').fetchone()
            next_id = str(int(last_id[0]) + 1) if last_id else '1'

            current_datetime = datetime.now()
            tm = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            email_data = email.lower()

            self.__cur.execute('INSERT INTO users (id, name, email, password, time, status) '
                               'VALUES (?, ?, ?, ?, ?, ?)', (next_id, name, email_data, hpsw, tm, 1))
            self.__db.commit()

            id_user = self.__cur.execute('SELECT * FROM users WHERE email = ? LIMIT 1', (email_data,)).fetchone()
            return id_user
        except Exception as e:
            print(e)
        return None

    def generate_remember_token(self, secret_key, user_id):
        """
        Generate a remember token and save it for the user.
        """
        serializer = URLSafeTimedSerializer(secret_key)
        data = {"user_id": user_id}
        token = serializer.dumps(data)

        try:
            self.__cur.execute('UPDATE users SET remember_token = ? WHERE id = ?', (token, user_id))
            self.__db.commit()
        except Exception as e:
            print(e)
        return token

    def verify_remember_token(self, token, secret_key):
        """
        Verify a remember token and return the associated user.
        """
        serializer = URLSafeTimedSerializer(secret_key)
        try:
            data = serializer.loads(token)
            user_id = data['user_id']
            user = self.__cur.execute('SELECT * FROM users WHERE id = ? LIMIT 1', (user_id,)).fetchone()
            if user:
                return user
        except Exception:
            return None

    def remember_token_none(self, user_id):
        """
        Clear the remember token for a user.
        """
        token = None
        try:
            self.__cur.execute('UPDATE users SET remember_token = ? WHERE id = ?', (token, user_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return None

    def getuser(self, user_id):
        """
        Retrieve a user by ID.
        """
        try:
            self.__cur.execute('SELECT * FROM users WHERE id = ? LIMIT 1', (user_id,))
            res = self.__cur.fetchone()
            if res:
                return res
            else:
                return False
        except Exception as e:
            print(e)
        return False
