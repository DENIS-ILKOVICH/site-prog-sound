from app_sps.content.models.models import Sound
from database import db_instance

class Cache:
    def __init__(self, db=None):
        """
        Initialize the Cache object with a database connection and Sound service.

        Args:
            db: Optional database connection. If None, a default instance is used.

        Attributes:
            sound: Instance of Sound class for data access.
            search_data: Dictionary to store cached search data.
        """
        if db is None:
            db = db_instance.get_db()
        self.db = db
        self.sound = Sound(self.db)
        self.search_data = {}

    def load_search_data(self):
        """
        Load authors, albums, and music data into a searchable cache.

        Each item is stored as a dictionary with 'name', 'id', and 'type' keys.

        Returns:
            None if an error occurs. On success, populates the `search_data` attribute.
        """
        try:
            authors_data = self.sound.get_all_authors()
            albums_data = self.sound.get_all_albums()
            music_data = self.sound.get_all_music()

            search_cache = []
            for item in authors_data:
                search_cache.append({'name': item['name'], 'id': item['id'], 'type': 'author'})
            for item in albums_data:
                search_cache.append({'name': item['name'], 'id': item['id'], 'type': 'album'})
            for item in music_data:
                search_cache.append(
                    {'name': f"{item['artist']} - {item['name']}", 'id': item['id'], 'type': 'music'}
                )
            self.search_data = search_cache
        except Exception:
            return None

    def get_search_data(self):
        """
        Retrieve the cached search data.

        Returns:
            dict: Cached search items with 'name', 'id', and 'type' keys.
        """
        return self.search_data
