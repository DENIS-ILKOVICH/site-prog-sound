from flask import session
from app_sps.locales.load_language import load_language
from app_sps.content.models.models import Sound
from datetime import *
from database import db_instance
import re


class Utils:
    def __init__(self, db=None):
        """
        Initialize the Utils object with a database connection and Sound service.

        Args:
            db: Optional database connection. If None, a default instance is used.

        Attributes:
            sound: Instance of Sound class for data access.
            search_data: Dictionary for storing auxiliary search-related data.
        """
        if db is None:
            db = db_instance.get_db()
        self.db = db
        self.sound = Sound(self.db)
        self.search_data = {}

    def get_auditions(self, datatype, item_id):
        """
        Calculate total auditions for a music, author, or album.

        Args:
            datatype (str): Type of item ('music', 'author', 'album').
            item_id (int): ID of the music, author, or album.

        Returns:
            str: Total number of auditions as a string.
            Returns '0' if there are no auditions or None on error.
        """
        try:
            total = 0
            audit = ''
            if datatype == 'music':
                audit = self.sound.get_count_music_auditions(item_id) or '0'


            if datatype == 'author':
                author_name = self.sound.get_one_author(item_id)[0]['name']
                author_music_id = self.sound.get_author_music_id(author_name)
                if author_music_id:
                    music_id_list = {item['id'] for item in author_music_id}
                    for item in list(music_id_list):
                        total += self.sound.get_count_music_auditions(item)
                    audit = str(total) if total > 0 else '0'

            if datatype == 'album':
                albums_music_id = self.sound.get_album_music_id(item_id)
                if albums_music_id:
                    albums_id_list = {item['id'] for item in albums_music_id}
                    for item in list(albums_id_list):
                        total += self.sound.get_count_music_auditions(item)
                    audit = str(total) if total > 0 else '0'

            return audit
        except Exception:
            return None

    def get_date(self, month_id):
        """
        Convert a date string from "DD.MM.YYYY" format to a readable string with month names.

        Args:
            month_id (str): Date string in "DD.MM.YYYY" format.

        Returns:
            str: Formatted date string like "25 January 2024".
            Returns None if input is invalid or error occurs.
        """
        lang = session.get('language', 'en')
        months_data = load_language(lang)

        months = {index: item for index, item in enumerate(months_data['auxiliary_data']['date']['months'], 1)}

        try:
            if not month_id:
                return None

            parts_data = month_id.split('.')
            parts = [item.replace("\u200b", "").strip() for item in parts_data]
            if len(parts) != 3:
                return None

            day, month, year = map(int, parts)

            if not (1 <= day <= 31) or not (1 <= month <= 12) or len(str(year)) != 4:
                return None

            date_release = f'{day} {months[month]} {year}'
            return date_release
        except Exception:
            return None

    def best_track(self, music):
        """
        Determine the most popular track based on auditions.

        Args:
            music (list): List of music items with 'id', 'artist', and 'name'.

        Returns:
            dict: Dictionary with 'id', 'name', and 'auditions' of the best track.
            Returns empty dict if no music or error occurs.
        """
        try:
            best_track = {}
            if music:
                author_id_list = {item['id']: f"{item['artist']} - {item['name']}" for item in music}
                max_auditions = 0
                for key, value in author_id_list.items():
                    auditions_value = self.sound.get_count_music_auditions(key)
                    if auditions_value:
                        if max_auditions < auditions_value:
                            best_track = {'id': key, 'name': value, 'auditions': auditions_value}
                            max_auditions = auditions_value
                    else:
                        best_track = {'id': None, 'name': None, 'auditions': None}
            return best_track
        except Exception:
            return None

    def best_genre(self, music, best_track):
        """
        Find the genre of the best track.

        Args:
            music (list): List of music items.
            best_track (dict): Best track dictionary with 'id' key.

        Returns:
            str: Primary genre of the best track.
            Returns empty string or None on error.
        """
        try:
            genre = ''
            lang = session.get('language', 'en')
            if music:
                for item in music:
                    if best_track['id']:
                        if best_track['id'] == item['id']:
                            genre = item['category'] if lang == 'ru' else item[f'category_{lang}']
                    else:
                        return None
            return genre.split(',')[0]
        except Exception:
            return None

    def first_track(self, music):
        """
        Get the earliest track by release date.

        Args:
            music (list): List of music items with 'date' field.

        Returns:
            dict: Music item that was released first.
            Returns None if input is invalid or error occurs.
        """
        try:
            first_track = None
            if music:
                sorted_list = sorted(
                    music,
                    key=lambda x: datetime.strptime(re.sub(r'[^\x00-\x7F]+', '', x["date"]), "%d.%m.%Y")
                )
                first_track = sorted_list[0]
            return first_track
        except Exception:
            return None
