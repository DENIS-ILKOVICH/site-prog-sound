class AdminModels:

    def __init__(self, db):
        if db is None:
            raise ValueError("Database connection is not established.")
        self.__db = db
        self.__cur = db.cursor()

    def get_admin_data(self, ad_secret_key):
        try:
            ad_data = self.__cur.execute('select * from admin where secret_key = ? LIMIT 1', (ad_secret_key, )).fetchone()
            if ad_data:
                return ad_data
        except Exception as e:
            print(e)
        return False

    def get_admin_by_id(self, ad_id):
        try:
            ad_data = self.__cur.execute('select * from admin where id = ?', (ad_id, )).fetchall()
            if ad_data:
                return [dict(item) for item in ad_data]
        except Exception as e:
            print(e)
        return False
