class Sound:
    def __init__(self, db):
        """Initialize Sound with a database connection."""
        if db is None:
            raise ValueError("Database connection is not established.")
        self.__db = db
        self.__cur = db.cursor()

    # --------------------------------GET ALL DATA---------------------------------------------------------
    def get_all_music(self):
        """Return all music records."""
        try:
            music = self.__cur.execute('select * from music').fetchall()
            return [dict(item) for item in music]
        except Exception as e:
            print(e)
        return []

    def get_all_authors(self):
        """Return all authors."""
        try:
            authors = self.__cur.execute('select * from authors').fetchall()
            return [dict(item) for item in authors]
        except Exception as e:
            print(e)
        return []

    def get_all_albums(self):
        """Return all albums."""
        try:
            albums = self.__cur.execute('select * from albums').fetchall()
            return [dict(item) for item in albums]
        except Exception as e:
            print(e)
        return []

    def get_music_category(self, category):
        """Return music filtered by category."""
        try:
            search_term = f"%{category}%"
            music_category = self.__cur.execute(
                "SELECT * FROM music WHERE category LIKE ? OR category_en LIKE ?",
                (search_term, search_term)
            ).fetchall()
            return [dict(item) for item in music_category]
        except Exception as e:
            print(e)
        return []

    # --------------------------------GET ONE DATA---------------------------------------------------------
    def get_one_music(self, m_id):
        """Return a single music record by ID."""
        try:
            music = self.__cur.execute('select * from music where id = ?', (m_id,)).fetchall()
            return [dict(item) for item in music]
        except Exception as e:
            print(e)
        return []

    def get_one_author(self, a_id):
        """Return a single author by ID."""
        try:
            author = self.__cur.execute('select * from authors where id = ?', (a_id,))
            print('est')
            return [dict(item) for item in author]
        except Exception as e:
            print(e)
        return False

    def get_one_album(self, al_id):
        """Return a single album by ID."""
        try:
            album = self.__cur.execute('select * from albums where id = ?', (al_id,))
            return [dict(item) for item in album]
        except Exception as e:
            print(e)
        return False

    # -------------------------------GET BIN FILE------------------------------------------------
    def music_audio(self, m_id):
        """Return audio data for a music record."""
        try:
            audio = self.__cur.execute('select audio from music where id = ?', (m_id,)).fetchall()
            return [dict(item) for item in audio]
        except Exception as e:
            print(e)
        return []

    def music_image(self, m_id):
        """Return image data for a music record."""
        try:
            image = self.__cur.execute('select image from music where id = ?', (m_id,)).fetchall()
            return [dict(item) for item in image]
        except Exception as e:
            print(e)
        return []

    def author_image(self, a_id):
        """Return image data for an author."""
        try:
            image = self.__cur.execute('select image from authors where id = ?', (a_id,)).fetchall()
            return [dict(item) for item in image]
        except Exception as e:
            print(e)
        return []

    def album_image(self, al_id):
        """Return image data for an album."""
        try:
            image = self.__cur.execute('select image from albums where id = ?', (al_id,)).fetchall()
            return [dict(item) for item in image]
        except Exception as e:
            print(e)
        return []

    # -----------------------------------AUDITION / PLAYLIST--------------------------------------------
    def get_count_music_auditions(self, m_id):
        """Return count of auditions for a music record."""
        try:
            auditions = self.__cur.execute('SELECT count(*) FROM auditions where music_id = ?', (m_id,)).fetchone()
            return auditions[0]
        except Exception as e:
            print(e)
        return False

    def get_playlist(self, user_id):
        """Return playlist for a user."""
        try:
            playlist = self.__cur.execute('select * from user_playlist where user_id = ?', (user_id,)).fetchall()
            return [dict(item) for item in playlist]
        except Exception as e:
            print(e)
        return False

    def add_audition(self, user_id, m_id, tm):
        """Add an audition record for a user and music."""
        try:
            res = self.__cur.execute('SELECT COUNT(*) from auditions where music_id = ? and user_id = ?',
                                     (int(m_id), int(user_id))).fetchone()
            if res[0] > 0:
                return False

            self.__cur.execute('''INSERT INTO auditions (music_id, user_id, time) VALUES (?, ?, ?)''',
                               (m_id, user_id, tm))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    # ----------------------------------AUTHOR / ALBUM RELATIONS--------------------------------------------
    def get_author_music_id(self, author_name):
        """Return all music records for a given author name."""
        try:
            search_term = f"%{str(author_name)}%"
            id_list = self.__cur.execute('SELECT * FROM music where artist LIKE ?', (search_term,)).fetchall()
            return [dict(item) for item in id_list]
        except Exception as e:
            print(e)
        return False

    def get_album_music_id(self, al_id):
        """Return music IDs for a given album."""
        try:
            al_music = self.__cur.execute('SELECT id FROM music where albums_id = ?', (int(al_id),)).fetchall()
            return [dict(item) for item in al_music]
        except Exception as e:
            print(e)
        return False

    def get_author_albums(self, a_id):
        """Return all albums for a given author ID."""
        try:
            a_music = self.__cur.execute('select * from albums where author_id = ?', (a_id,))
            return [dict(item) for item in a_music]
        except Exception as e:
            print(e)
        return False

    def get_album_music(self, al_id):
        """Return all music records for a given album ID."""
        try:
            al_music = self.__cur.execute('select * from music where albums_id = ?', (al_id,))
            return [dict(item) for item in al_music]
        except Exception as e:
            print(e)
        return False
