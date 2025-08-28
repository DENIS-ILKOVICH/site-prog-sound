from flask_login import UserMixin

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        """Load user from database by ID."""
        self.__user = db.getuser(user_id)
        return self

    def create(self, user):
        """Create a user object from provided data."""
        self.__user = user
        return self

    def get_id(self):
        """Return user ID as string."""
        return str(self.__user['id'])

    def get_name(self):
        """Return user's name or 'No name' if not set."""
        return str(self.__user['name']) if self.__user else 'No name'

    def get_mail(self):
        """Return user's email or 'No email' if not set."""
        return str(self.__user['email']) if self.__user else 'No email'

    def get_avatar(self):
        """Return user's avatar or 'No avatar' if not set."""
        return self.__user['avatar'] if self.__user else 'No avatar'

    def get_user(self):
        """Return all user data as dictionary."""
        return self.__user
