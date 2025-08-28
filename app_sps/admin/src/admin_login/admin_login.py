from flask_login import UserMixin


class AdminLogin(UserMixin):
    def fromDB(self, ad_id, db):
        self.__admin = db.get_admin_data(ad_id)
        return self

    def create(self, admin):
        self.__admin = admin
        return self

    def get_id(self):
        return str(self.__admin['id'])

    def get_secret_key(self):
        return str(self.__admin['secret_key']) if self.__admin else ''

    def get_last_login(self):
        return str(self.__admin['last_login']) if self.__admin else ''

    def get_create_at(self):
        return str(self.__admin['create_at']) if self.__admin else ''

    def get_rights(self):
        return str(self.__admin['rights']) if self.__admin else ''

    def get_admin(self):
        return self.__admin
