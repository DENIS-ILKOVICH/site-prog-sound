
class Utils:
    def __init__(self):
        pass


    @staticmethod
    def input_format_date(date):
        """
        Validates and formats a date string into the format 'dd.mm.yyyy'.

        Args:
            date (str): Input date string with any common separator (e.g., '.', '/', ':').

        Returns:
            str | None: Formatted date string in 'dd.mm.yyyy' format if valid, otherwise None.
        """
        if not date or len(date) != 10:
            return None

        separator = '.'
        for item in ['.', '/', '|', ',', ':', ';']:
            if item in date:
                separator = item
                break

        try:
            day, month, year = map(int, date.split(separator))
        except ValueError:
            return None

        if not (1 <= day <= 31):
            return None

        if not (1 <= month <= 12):
            return None

        if not (1000 <= year <= 3000):
            return None

        return f"{day:02}.{month:02}.{year}"



class SearchData:
    def __init__(self, data_db):
        self.data_db = data_db


    def search_music(self, search_text):
        """
        Searches for music records by name or ID.

        Args:
            search_text (str): Music name (partial or full) or numeric ID.

        Returns:
            list[dict] | bool: List of matching music records or False if none found.
        """
        if search_text.isdigit():
            return self.data_db.get_music_by_id(search_text)
        return self.data_db.get_music_by_text(search_text)


    def search_albums(self, search_text):
        """
        Searches for album records by name or ID.

        Args:
            search_text (str): Album name (partial or full) or numeric ID.

        Returns:
            list[dict] | bool: List of matching albums or False if none found.
        """
        if search_text.isdigit():
            return self.data_db.get_albums_by_id(search_text)
        return self.data_db.get_albums_by_text(search_text)


    def search_authors(self, search_text):
        """
        Searches for author records by name or ID.

        Args:
            search_text (str): Author name (partial or full) or numeric ID.

        Returns:
            list[dict] | bool: List of matching authors or False if none found.
        """
        if search_text.isdigit():
            return self.data_db.get_author_by_id(search_text)
        return self.data_db.get_authors_by_text(search_text)