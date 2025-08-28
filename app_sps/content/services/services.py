from app_sps.content.models.models import Sound
from app_sps.content.src.utils.utils import Utils
from flask import current_app, session, make_response
from flask_login import current_user
from threading import Lock
from datetime import datetime, timedelta
from app_sps.logs.logclass import logger

db_lock = Lock()

def get_all_content(db):
    """
    Retrieve all music, authors, and albums from the database.

    Args:
        db: Database connection.

    Returns:
        tuple: Dictionary with 'music', 'authors', 'albums' lists and HTTP status code.
        Returns error dict if data not found or on unexpected server error.
    """
    try:
        sound = Sound(db)

        music_data = sound.get_all_music()
        authors_data = sound.get_all_authors()
        albums_data = sound.get_all_albums()

        if not all([music_data, authors_data, albums_data]):
            return {'error': 'Data not found'}, 404

        data = {
            'music': music_data,
            'authors': authors_data,
            'albums': albums_data
        }

        return data, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def get_music_category(db, category):
    """
    Retrieve music records filtered by a specific category.

    Args:
        db: Database connection.
        category: Category name to filter music.

    Returns:
        tuple: List of music records and HTTP status code.
        Returns error dict if no records found or on unexpected server error.
    """
    try:
        music_category_data = Sound(db).get_music_category(category)
        if not music_category_data:
            return {'error': 'Music in this category was not found'}, 404

        return music_category_data, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def get_all_data_from_music(db, m_id):
    """
    Retrieve all related data for a specific music record.

    Args:
        db: Database connection.
        m_id: Music ID.

    Returns:
        tuple: Dictionary with music details, album, category, auditions, date release, and playlist.
        Returns error dict if invalid input, record not found, or internal error.
    """
    try:
        sound = Sound(db)
        utils = Utils()

        if not m_id:
            return {'error': 'Invalid input'}, 400

        music_data = sound.get_one_music(m_id)
        if not music_data:
            return {'error': 'Music not found'}, 404

        al_id = music_data[0]['albums_id'] if music_data[0]['albums_id'] else None
        albums_data = []
        if al_id:
            albums_data = sound.get_one_album(al_id)

        try:
            lang = session.get('language', 'en')
            category_data = music_data[0]['category'].split(',') if lang == 'ru' else music_data[0][f'category_{lang}'].split(',')
            category_list = [item.strip() for item in category_data]
            category_music_data = sound.get_music_category(category_list[0])
            category_music_list = [item for item in category_music_data if item['id'] != music_data[0]['id']]
            category_music_list.append(music_data)
        except Exception as e:
            return {'error': 'Internal server error, invalid data format'}, 500

        auditions_data = utils.get_auditions(datatype='music', item_id=m_id)

        date_release = utils.get_date(month_id=music_data[0]['date'])

        playlist_add = []

        playlist_add = []
        if current_user.is_authenticated:
            user_id = current_user.get_id()
            if user_id:
                playlist_add = sound.get_playlist(user_id)

        data = {
            'music': category_music_list,
            'albums': albums_data,
            'category': category_list,
            'auditions': auditions_data,
            'date_release': date_release,
            'playlist_add': playlist_add
        }

        return data, 200

    except ValueError as e:
        return {'error': 'Invalid input', 'details': str(e)}, 422
    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def get_image_data(datatype, item_id, db):
    """
    Retrieve image data for a music, author, or album record.

    Args:
        datatype: 'music', 'author', or 'album'.
        item_id: ID of the item.
        db: Database connection.

    Returns:
        tuple: Image bytes and HTTP status code.
        Returns error dict if input is invalid, datatype is wrong, or image not found.
    """
    try:
        if not datatype or not item_id:
            return {'error': 'Invalid input'}, 400

        image = None
        sound = Sound(db)
        if datatype == 'music':
            image = sound.music_image(item_id)
        elif datatype == 'author':
            image = sound.author_image(item_id)
        elif datatype == 'album':
            image = sound.album_image(item_id)
        else:
            return {'error': 'Invalid datatype'}, 400

        if not image:
            return {'error': 'Image not found'}, 404

        return image[0]['image'], 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def get_music_audio(m_id, db):
    """
    Retrieve audio data for a specific music record.

    Args:
        m_id: Music ID.
        db: Database connection.

    Returns:
        tuple: Audio bytes and HTTP status code.
        Returns error dict if input is invalid or audio not found.
    """
    try:
        if not m_id:
            return {'error': 'Invalid input'}, 400

        sound = Sound(db)

        audio = sound.music_audio(m_id)
        if not audio:
            return {'error': 'Audio not found'}, 404

        return audio[0]['audio'], 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def get_all_data_from_author(a_id, name, db):
    """
    Retrieve all data related to an author, including albums, music, and best track/genre.

    Args:
        a_id: Author ID.
        name: Author name.
        db: Database connection.

    Returns:
        tuple: Dictionary with author info, albums, music, auditions, best track/genre, first track.
        Returns error dict if invalid input, data not found, or internal error.
    """
    try:
        if not a_id:
            return {'error': 'Invalid input'}, 400

        sound = Sound(db)
        utils = Utils()

        author = sound.get_one_author(a_id)
        if not author:
            return {'error': 'Data not found'}, 404

        albums = sound.get_author_albums(a_id) if sound.get_author_albums(a_id) else []
        music = sound.get_author_music_id(name) if sound.get_author_music_id(name) else []

        auditions_data = utils.get_auditions('author', a_id)
        best_track = utils.best_track(music)
        best_genre = utils.best_genre(music, best_track)
        first_track = utils.first_track(music)

        data_ver = [auditions_data, best_track, best_genre, first_track]
        for i in range(len(data_ver)):
            if data_ver[i] is None:
                data_ver[i] = []

        data = {
            'author': author,
            'albums': albums,
            'music': music,
            'auditions_data': auditions_data,
            'best_track': best_track,
            'best_genre': best_genre,
            'first_track': first_track
        }

        return data, 200

    except ValueError as e:
        return {'error': 'Invalid input', 'details': str(e)}, 422
    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def get_all_data_from_album(al_id, db):
    """
    Retrieve all data related to an album, including author, music, best track, auditions, and release date.

    Args:
        al_id: Album ID.
        db: Database connection.

    Returns:
        tuple: Dictionary with album info, music, author, best track, auditions, and release date.
        Returns error dict if invalid input, album or author not found, or internal error.
    """
    try:
        if not al_id:
            return {'error': 'Invalid input'}, 400

        sound = Sound(db)
        utils = Utils()

        album = sound.get_one_album(al_id)
        if not album:
            return {'error': 'Album not found'}, 404

        author_id = album[0]['author_id']
        if not author_id:
            return {'error': 'Author not found'}, 404

        music = sound.get_album_music(al_id)
        author = sound.get_one_author(author_id)
        if not all([music, author]):
            return {'error': 'data not found'}, 404

        best_track = utils.best_track(music)
        auditions_data = utils.get_auditions('album', al_id)
        date_release = utils.get_date(album[0]['date'])

        data_ver = [auditions_data, best_track, best_track, date_release]
        for i in range(len(data_ver)):
            if data_ver[i] is None:
                data_ver[i] = []

        data = {
            'albums_data': album,
            'music_data': music,
            'author_data': author,
            'best_track_data': best_track,
            'auditions_data': auditions_data,
            'date_release_data': date_release
        }
        return data, 200

    except ValueError as e:
        return {'error': 'Invalid input', 'details': str(e)}, 422

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def site_search_data(data):
    """
    Search cached site data for items matching the query string.

    Args:
        data: Search string.

    Returns:
        tuple: List of matching items and HTTP status code.
        Returns error dict if input is invalid or internal server error.
    """
    try:
        if not data:
            return {'error': 'Invalid input'}, 400

        search_list = []
        search_cache = current_app.cache.get_search_data()
        for item in search_cache:
            if data in item['name'].lower():
                search_list.append(item)

        return search_list, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def get_content_data(datatype, db):
    """
    Retrieve all records for a given content type: music, authors, or albums.

    Args:
        datatype: 'music', 'authors', or 'albums'.
        db: Database connection.

    Returns:
        tuple: List of records and HTTP status code.
        Returns error dict if input is invalid, datatype wrong, or no data found.
    """
    try:
        if not datatype:
            return {'error': 'Invalid input'}, 400

        sound = Sound(db)

        if datatype == 'music':
            data = sound.get_all_music()
        elif datatype == 'authors':
            data = sound.get_all_authors()
        elif datatype == 'albums':
            data = sound.get_all_albums()
        else:
            return {'error': 'Invalid datatype'}, 400

        if not data:
            return {'error': 'Data not found'}, 404

        return data, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def add_audit(m_id, user_id, db):
    """
    Add an audition entry for a user listening to a music track.

    Args:
        m_id: Music ID.
        user_id: User ID.
        db: Database connection.

    Returns:
        tuple: Success message or error dict with HTTP status code.
        Returns conflict if entry already exists.
    """
    try:
        if not all([m_id, user_id]):
            return {'error': 'Invalid input'}, 400

        with db_lock:
            sound = Sound(db)
            current_datetime = datetime.now()
            tm = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            res = sound.add_audition(user_id, m_id, tm)

            if not res:
                return {"message": 'This entry already exists'}, 409

            return {"success": True}, 201

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def get_language(req):
    """
    Determine and set user's language preference based on cookies or headers.

    Args:
        req: Flask request object.

    Returns:
        tuple: Dictionary with 'language' and HTTP status code.
        Defaults to 'en' if not specified or invalid.
    """
    try:

        if not req:
            return {'error': 'Invalid input'}, 400

        if 'language' in req.cookies:
            session['language'] = req.cookies.get('language') if req.cookies.get('language') in ['ru', 'en',
                                                                                                 'en'] else 'en'

            return {'language': session['language']}, 200

        lang_header = req.headers.get("Accept-Language", "")

        if not lang_header:
            session['language'] = 'en'
            return {'language': 'en'}, 200

        languages = [lang.split(";")[0] for lang in lang_header.split(",")]

        session['language'] = languages[0][:2] if languages and languages[0][:2] in ['ru', 'en'] else 'en'

        return {'language': session['language']}, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def add_language(lang):
    """
    Set a language cookie and store language in session.

    Args:
        lang: Language code ('ru' or 'en').

    Returns:
        tuple: Flask response with message and HTTP status code.
        Returns error dict if input is invalid or internal error.
    """
    try:
        if not lang:
            return {'error': 'Invalid input'}, 400

        response = make_response({"message": "Language data saved"})
        expires = datetime.now() + timedelta(days=30)
        response.set_cookie('language', lang, expires=expires)

        session["language"] = lang

        return response, 201

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500
