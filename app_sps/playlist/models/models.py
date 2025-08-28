
class Playlist:
    def __init__(self, db):
        """
        Initialize the Playlist with a database connection.
        """
        self.__db = db
        self.__cur = db.cursor()

    def create_plst_db(self, user_id, name, image):
        """
        Create a new playlist in the database for a user.
        """
        try:
            self.__cur.execute('''INSERT INTO user_playlist (user_id, name, image) VALUES (?, ?, ?)''',
                               (user_id, name, image))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def get_playlist(self, user_id):
        """
        Retrieve all playlists for a given user.
        """
        try:
            playlist = self.__cur.execute('select * from user_playlist where user_id = ?', (user_id,)).fetchall()
            return [dict(item) for item in playlist]
        except Exception as e:
            print(e)
        return False

    def get_playlist_music(self, user_id):
        """
        Retrieve playlists and their songs for a given user.
        """
        try:
            res = self.__cur.execute("""
                SELECT up.id AS playlist_id, 
                       up.name AS playlist_name, 
                       json_group_array(
                           json_object('id', m.id, 'name', m.name)
                       ) AS song_list
                FROM user_playlist up
                JOIN playlist_music pm ON up.id = pm.playlist_id
                JOIN music m ON pm.music_id = m.id
                WHERE up.user_id = ?
                GROUP BY up.id, up.name;
            """, (user_id,)).fetchall()
            result = [dict(item) for item in res]
            return result
        except Exception as e:
            print(e)
        return False

    def add_music_in_plst(self, playlist_id, music_id):
        """
        Add a music track to a playlist if it's not already there.
        """
        try:
            self.__cur.execute("SELECT COUNT(*) FROM playlist_music WHERE playlist_id = ? and music_id = ?",
                               (playlist_id, music_id))
            res = self.__cur.fetchone()
            if res[0] > 0:
                return False

            self.__cur.execute('''INSERT INTO playlist_music (playlist_id, music_id) VALUES (?, ?)''',
                               (playlist_id, music_id))
            self.__db.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def playlist_img(self, pl_id):
        """
        Get the image of a specific playlist.
        """
        try:
            list_music = self.__cur.execute('select image from user_playlist where id = ?', (pl_id,)).fetchall()
            return [dict(item) for item in list_music]
        except Exception as e:
            print(e)
        return []

    def get_playlist_one(self, pl_id):
        """
        Retrieve a single playlist by its ID.
        """
        try:
            playlist = self.__cur.execute('select * from user_playlist where id = ?', (pl_id,)).fetchall()
            return [dict(item) for item in playlist]
        except Exception as e:
            print(e)
        return False

    def get_playlist_music_id(self, pl_id):
        """
        Retrieve all music IDs associated with a playlist.
        """
        try:
            playlist = self.__cur.execute('select * from playlist_music where playlist_id = ?', (pl_id,)).fetchall()
            return [dict(item) for item in playlist]
        except Exception as e:
            print(e)
        return False

    def music_one_second(self, m_id):
        """
        Retrieve full music data for a specific music ID.
        """
        try:
            list_music = self.__cur.execute('select * from music where id = ?', (m_id,)).fetchone()
            return dict(list_music)
        except Exception as e:
            print(e)
        return []

    def change_img_pl(self, pl_id, image):
        """
        Update the image of a playlist.
        """
        try:
            self.__cur.execute('UPDATE user_playlist SET image = ? WHERE id = ?', (image, pl_id))
            self.__db.commit()
        except Exception as e:
            print(e)
        return []

    def change_name_pl(self, pl_id, name):
        """
        Update the name of a playlist.
        """
        try:
            self.__cur.execute('UPDATE user_playlist SET name = ? WHERE id = ?', (name, pl_id))
            self.__db.commit()
        except Exception as e:
            print(e)
        return []

    def del_pl(self, pl_id):
        """
        Delete a playlist and its related music associations.
        """
        try:
            self.__cur.execute("DELETE FROM user_playlist WHERE id = ?;", (pl_id,))
            self.__cur.execute("DELETE FROM playlist_music WHERE playlist_id = ?;", (pl_id,))
            self.__db.commit()
        except Exception as e:
            print(e)
        return False

    def del_mus_pl(self, pl_id, m_id):
        """
        Delete a music track from a playlist.
        """
        try:
            self.__cur.execute("DELETE FROM playlist_music WHERE playlist_id = ? and music_id = ?;", (pl_id, m_id))
            self.__db.commit()
        except Exception as e:
            print(e)
        return False
