class DataModels:
    def __init__(self, db):
        """
        Initialize the DataModels class with a database connection.
        Raises an error if the connection is not provided.
        """
        if db is None:
            raise ValueError("Database connection is not established.")
        self.__db = db
        self.__cur = db.cursor()

    # ----------------------------------------###--GET DATA--###-----------------------------------------------------

    # --------------------------- GET ALL DATA ---------------------------
    def get_all_music(self):
        """
        Retrieve all music records from the database, ordered by descending ID.
        """
        try:
            music_list = self.__cur.execute('SELECT * FROM music ORDER BY id DESC').fetchall()
            return [dict(item) for item in music_list]
        except Exception as e:
            print(e)
        return False

    def get_all_albums(self):
        """
        Retrieve all album records from the database, ordered by descending ID.
        """
        try:
            albums_list = self.__cur.execute('SELECT * FROM albums ORDER BY id DESC').fetchall()
            return [dict(item) for item in albums_list]
        except Exception as e:
            print(e)
        return False

    def get_all_authors(self):
        """
        Retrieve all author records from the database, ordered by descending ID.
        """
        try:
            music_list = self.__cur.execute('SELECT * FROM authors ORDER BY id DESC').fetchall()
            return [dict(item) for item in music_list]
        except Exception as e:
            print(e)
        return False

    # ---------------------- GET ONE ITEM BY ID --------------------------
    def get_music_by_id(self, music_id):
        """
        Retrieve a single music record by its ID.
        """
        try:
            music_data = self.__cur.execute('SELECT * FROM music WHERE id = ?', (music_id,)).fetchall()
            return [dict(item) for item in music_data]
        except Exception as e:
            print(e)
        return False

    def get_albums_by_id(self, album_id):
        """
        Retrieve a single album record by its ID.
        """
        try:
            albums_data = self.__cur.execute('SELECT * FROM albums WHERE id = ?', (album_id,)).fetchall()
            return [dict(item) for item in albums_data]
        except Exception as e:
            print(e)
        return False

    def get_author_by_id(self, album_id):
        """
        Retrieve a single author record by its ID.
        """
        try:
            author_data = self.__cur.execute('SELECT * FROM authors WHERE id = ?', (album_id,)).fetchall()
            return [dict(item) for item in author_data]
        except Exception as e:
            print(e)
        return False

    # ---------------------- GET DATA BY TEXT SEARCH ---------------------
    def get_music_by_text(self, text):
        """
        Search for music entries by name using a partial match.
        """
        try:
            music_list = self.__cur.execute("SELECT * FROM music WHERE name LIKE ? ORDER BY id DESC",
                                            (f"%{text}%",)).fetchall()
            return [dict(item) for item in music_list]
        except Exception as e:
            print(e)
        return False

    def get_albums_by_text(self, text):
        """
        Search for albums by name using a partial match.
        """
        try:
            albums_list = self.__cur.execute("SELECT * FROM albums WHERE name LIKE ? ORDER BY id DESC",
                                             (f"%{text}%",)).fetchall()
            return [dict(item) for item in albums_list]
        except Exception as e:
            print(e)
        return False

    def get_authors_by_text(self, text):
        """
        Search for authors by name using a partial match.
        """
        try:
            authors_list = self.__cur.execute("SELECT * FROM authors WHERE name LIKE ? ORDER BY id DESC",
                                              (f"%{text}%",)).fetchall()
            return [dict(item) for item in authors_list]
        except Exception as e:
            print(e)
        return False

    # -------------------------- COUNT MATCHING ENTRIES ---------------------------
    def get_music_by_data(self, name, artist):
        """
        Count music entries by exact name and artist match.
        """
        try:
            music_list = self.__cur.execute("SELECT COUNT(*) FROM music WHERE name = ? AND artist = ?",
                                            (name, artist)).fetchone()
            return music_list
        except Exception as e:
            print(e)
        return None

    def get_authors_by_data(self, name):
        """
        Count author entries with the specified name.
        """
        try:
            authors_list = self.__cur.execute("SELECT COUNT(*) FROM authors WHERE name = ?",
                                              (name,)).fetchone()
            return authors_list
        except Exception as e:
            print(e)
        return None

    def get_albums_by_data(self, name):
        """
        Count album entries with the specified name.
        """
        try:
            albums_list = self.__cur.execute("SELECT COUNT(*) FROM albums WHERE name = ?",
                                             (name,)).fetchone()
            return albums_list
        except Exception as e:
            print(e)
        return None

    # -------------------------- GET IMAGES BY ID --------------------------
    def music_image(self, m_id):
        """
        Get the image associated with a specific music ID.
        """
        try:
            image = self.__cur.execute('SELECT image FROM music WHERE id = ?', (m_id,)).fetchall()
            return [dict(item) for item in image]
        except Exception as e:
            print(e)
        return []

    def author_image(self, a_id):
        """
        Get the image associated with a specific author ID.
        """
        try:
            image = self.__cur.execute('SELECT image FROM authors WHERE id = ?', (a_id,)).fetchall()
            return [dict(item) for item in image]
        except Exception as e:
            print(e)
        return []

    def album_image(self, al_id):
        """
        Get the image associated with a specific album ID.
        """
        try:
            image = self.__cur.execute('SELECT image FROM albums WHERE id = ?', (al_id,)).fetchall()
            return [dict(item) for item in image]
        except Exception as e:
            print(e)
        return []

    # ----------------------------------------###--ADD DATA--###-----------------------------------------------------
    def music_add_in_db(self, category, name, artist, image_data, audio_data, duration, tm, status, al_id, date_r):
        """
        Insert a new music entry into the database.
        """
        try:
            self.__cur.execute('''
                INSERT INTO music (category, name, artist, image, audio, duration, time, status, albums_id, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (category, name, artist, image_data, audio_data, duration, tm, status, al_id, date_r))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return None

    def author_add_in_db(self, name, image_data):
        """
        Insert a new author into the database.
        """
        try:
            self.__cur.execute('''
                INSERT INTO authors (name, image)
                VALUES (?, ?)
            ''', (name, image_data))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return None

    def album_add_in_db(self, autor_id, name, image_data, date_r):
        """
        Insert a new album into the database.
        """
        try:
            self.__cur.execute('''
                INSERT INTO albums (author_id, name, image, date)
                VALUES (?, ?, ?, ?)
            ''', (autor_id, name, image_data, date_r))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return None

    # ----------------------------------------###--DELETE DATA--###-----------------------------------------------------
    def del_music_in_db(self, m_id):
        """
        Delete a music entry by ID.
        """
        try:
            self.__cur.execute('DELETE FROM music WHERE id = ?', (m_id,))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return None

    def del_author_in_db(self, a_id):
        """
        Delete an author entry by ID.
        """
        try:
            self.__cur.execute('DELETE FROM authors WHERE id = ?', (a_id,))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return None

    def del_album_in_db(self, al_id):
        """
        Delete an album entry by ID.
        """
        try:
            self.__cur.execute('DELETE FROM albums WHERE id = ?', (al_id,))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return None

    # ----------------------------------------###--UPDATE DATA--###-----------------------------------------------------
    # ----------------------- Update Images -----------------------
    def update_music_image(self, image_data, m_id):
        """
        Update the image of a specific music entry.
        """
        try:
            self.__cur.execute('UPDATE music SET image = ? WHERE id = ?', (image_data, m_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def update_author_image(self, image_data, a_id):
        """
        Update the image of a specific author.
        """
        try:
            self.__cur.execute('UPDATE authors SET image = ? WHERE id = ?', (image_data, a_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def update_album_image(self, image_data, al_id):
        """
        Update the image of a specific album.
        """
        try:
            self.__cur.execute('UPDATE albums SET image = ? WHERE id = ?', (image_data, al_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    # ----------------------- Update Names -----------------------
    def update_music_name(self, music_name, m_id):
        """
        Update both artist and name of a music entry.
        Expects music_name as a tuple: (artist, name)
        """
        try:
            self.__cur.execute('UPDATE music SET artist = ? WHERE id = ?', (music_name[0], m_id))
            self.__cur.execute('UPDATE music SET name = ? WHERE id = ?', (music_name[1], m_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def update_author_name(self, author_name, a_id):
        """
        Update the name of a specific author.
        """
        try:
            self.__cur.execute('UPDATE authors SET name = ? WHERE id = ?', (author_name, a_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def update_album_name(self, album_name, al_id):
        """
        Update the name of a specific album.
        """
        try:
            self.__cur.execute('UPDATE albums SET name = ? WHERE id = ?', (album_name, al_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    # ----------------------- Update Dates -----------------------
    def update_music_date(self, music_date, m_id):
        """
        Update the release date of a specific music entry.
        """
        try:
            self.__cur.execute('UPDATE music SET date = ? WHERE id = ?', (music_date, m_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def update_album_date(self, album_date, al_id):
        """
        Update the release date of a specific album.
        """
        try:
            self.__cur.execute('UPDATE albums SET date = ? WHERE id = ?', (album_date, al_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    # ---------------------- Update Foreign Keys -----------------------
    def update_album_id_for_music(self, m_id, al_id):
        """
        Update the album ID foreign key for a music entry.
        """
        try:
            self.__cur.execute('UPDATE music SET albums_id = ? WHERE id = ?', (int(al_id), m_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def update_author_id_for_album(self, al_id, a_id):
        """
        Update the author ID foreign key for an album entry.
        """
        try:
            self.__cur.execute('UPDATE albums SET author_id = ? WHERE id = ?', (int(a_id), al_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    # ---------------------- Update Category -----------------------
    def update_music_category(self, category, m_id):
        """
        Update the category of a specific music entry.
        """
        try:
            self.__cur.execute('UPDATE music SET category = ? WHERE id = ?', (category, m_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False
