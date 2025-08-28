from flask import session, make_response, redirect, url_for
from flask_login import login_user, logout_user

from datetime import datetime
from ..src.admin_login.admin_login import AdminLogin
from werkzeug.security import check_password_hash
from app_sps.admin.models.admin_models.models import AdminModels
from app_sps.admin.models.data_models.models import DataModels
from ..src.utils.utils import Utils, SearchData
from app_sps.logs.logclass import logger

def authorize_admin(req, db):
    """
    Authorizes an admin user using secret key and password.

    Args:
        req: HTTP request object containing 'secret_key' and 'password' in form data.
        db: Database connection object.

    Returns:
        tuple: JSON response with status message and HTTP status code.
    """
    try:
        if not req:
            return {'error': 'Invalid input'}, 400

        secret_key_form = req.form.get('secret_key', None)
        psw_form = req.form.get('password', None)
        if not all([secret_key_form, psw_form]):
            return {'error': 'No required data'}, 400

        admin = AdminModels(db)

        ad_data = admin.get_admin_data(secret_key_form)

        if not ad_data:
            return {'error': 'Secret key not found in db'}, 404

        psw_db = ad_data['password']

        if psw_db != psw_form:
            return {'error': 'Invalid password'}, 401

        ad_login = AdminLogin().create(ad_data)

        session['user_type'] = 'admin'

        login_user(ad_login)

        return {'message': 'Successful authorization'}, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'status': 'error', 'message': 'An unexpected error occurred'}, 500


def fetch_and_search_data(req, data_type, db):
    """
    Retrieves and optionally filters music, album, or author data based on search input.

    Args:
        req: HTTP request object with optional POST form fields for search.
        data_type (str): Type of data to retrieve ('music', 'albums', 'authors').
        db: Database connection object.

    Returns:
        tuple: JSON response with the requested data or error message, and HTTP status code.
    """
    try:
        if not req:
            return {'error': 'Invalid input'}, 400

        data_db = DataModels(db)
        search = SearchData(data_db)

        if data_type == 'music':
            music_list = data_db.get_all_music()
            albums_list = data_db.get_all_albums()

            if not all([music_list, albums_list]):
                return {'error': 'Data not found'}, 404

            if req.method == 'POST':
                if 'name_music' in req.form:
                    search_text = req.form.get('name_music', '').strip().lower()
                    music_list = search.search_music(search_text)

                if 'name_album' in req.form:
                    search_text = req.form.get('name_album', '').strip().lower()
                    albums_list = search.search_albums(search_text)

            return {"music_list": music_list, "albums_list": albums_list}, 200

        elif data_type == 'authors':
            authors_list = data_db.get_all_authors()
            if not authors_list:
                return {'error': 'Data not found'}, 404

            if req.method == 'POST':
                search_text = req.form.get('name', '').strip().lower()
                authors_list = search.search_authors(search_text)

            return {'authors_list': authors_list}, 200

        elif data_type == 'albums':
            albums_list = data_db.get_all_albums()
            authors_list = data_db.get_all_authors()

            if not all([albums_list, albums_list]):
                return {'error': 'Data not found'}, 404

            if req.method == 'POST':
                if 'name_album' in req.form:
                    search_text = req.form.get('name_album', '').strip().lower()
                    albums_list = search.search_albums(search_text)

                if 'name_author' in req.form:
                    search_text = req.form.get('name_author', '').strip().lower()
                    authors_list = search.search_authors(search_text)

            return {'authors_list': authors_list, 'albums_list': albums_list}, 200

        else:
            return {'error': 'Invalid data type'}, 400

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def remove_data_from_db(req, item_id, datatype, db):
    """
    Removes a specific record (music, author, or album) by its ID.

    Args:
        req: HTTP request (must be POST).
        item_id (int): ID of the item to delete.
        datatype (str): Type of item ('music', 'author', 'album').
        db: Database connection object.

    Returns:
        tuple: JSON response indicating result of the operation and HTTP status code.
    """
    try:
        if req.method != 'POST':
            return {'error': 'Method Not Allowed'}, 405

        data_db = DataModels(db)

        delete_map = {
            'music': data_db.del_music_in_db,
            'author': data_db.del_author_in_db,
            'album': data_db.del_album_in_db
        }

        if datatype not in delete_map:
            return {'error': 'Unknown entity type'}, 400

        res = delete_map[datatype](item_id)
        if not res:
            return {'error': 'Data processing error'}, 422

        return {'message': 'Data removed successfully'}, 200

    except Exception:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': f'An unexpected error occurred'}, 500


def insert_data_in_db(req, data_type, db):
    """
    Inserts a new music track, author, or album into the database.

    Args:
        req: HTTP POST request with form data and uploaded files.
        data_type (str): Type of data to insert ('music', 'author', 'album').
        db: Database connection object.

    Returns:
        tuple: JSON response indicating success or failure, and HTTP status code.
    """
    try:
        if not req:
            return {'error': 'Invalid input'}, 400

        if req.method != 'POST':
            return {'error': 'Method Not Allowed'}, 405

        data_db = DataModels(db)
        utils = Utils()

        if data_type == 'music':
            file = req.files.get('file')
            image_file = req.files.get('image')
            category = req.form.get('category')
            al_id = req.form.get('al_id')
            name = req.form.get('title')
            artist = req.form.get('artist')
            duration = req.form.get('duration')
            status = req.form.get('status')
            date_r = req.form.get('date_r', '').strip()

            if not all([file, image_file, category, artist, al_id, name, duration, status]):
                return {'error': 'Invalid input'}, 400

            audio_data = file.read()
            image_data = image_file.read()

            date_validation = utils.input_format_date(date_r)
            count_music = data_db.get_music_by_data(name, artist)

            if None in [date_validation, count_music]:
                return {'error': 'Data processing error'}, 422

            if count_music[0] > 0:
                return {'error': 'Conflict'}, 409

            res = data_db.music_add_in_db(category, name, artist, image_data, audio_data, duration,
                                          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          status, al_id, date_r)

        elif data_type == 'author':
            image_file = req.files.get('image')
            image_data = image_file.read()
            name = req.form.get('name')

            if not all([image_file, name]):
                return {'error': 'Invalid input'}, 400

            count_authors = data_db.get_authors_by_data(name)
            if not count_authors:
                return {'error': 'Data processing error'}, 422
            if count_authors[0] > 0:
                return {'error': 'Conflict'}, 409

            res = data_db.author_add_in_db(name, image_data)

        elif data_type == 'album':
            autor_id = req.form.get('a_id')
            image_file = req.files.get('image')
            name = req.form.get('name')
            date_r = req.form.get('album_date', '').strip()

            if not all([autor_id, image_file, name, date_r]):
                return {'error': 'Invalid input album data'}, 400

            image_data = image_file.read()

            date_validation = utils.input_format_date(date_r)
            count_albums = data_db.get_albums_by_data(name)
            if None in [date_validation, count_albums]:
                return {'error': 'Data processing error'}, 422

            if count_albums[0] > 0:
                return {'error': 'Conflict'}, 409

            res = data_db.album_add_in_db(autor_id, name, image_data, date_validation)

        else:
            return {'error': 'Unknown entity type'}, 400

        if not res:
            return {'error': 'Data processing error'}, 422

        return {'message': 'Data added successfully'}, 201

    except Exception:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': f'An unexpected error occurred'}, 500


def get_image_data(datatype, item_id, db):
    """
    Retrieves image binary data for the specified entity type and ID.

    Args:
        datatype (str): Type of data ('music', 'author', 'album').
        item_id (int): ID of the item whose image is requested.
        db: Database connection object.

    Returns:
        tuple: Raw image data (bytes) and HTTP status code, or JSON error response.
    """
    try:
        if not datatype or not item_id:
            return {'error': 'Invalid input'}, 400

        image = None
        data_db = DataModels(db)
        if datatype == 'music':
            image = data_db.music_image(item_id)
        elif datatype == 'author':
            image = data_db.author_image(item_id)
        elif datatype == 'album':
            image = data_db.album_image(item_id)
        else:
            return {'error': 'Invalid datatype'}, 400

        if not image:
            return {'error': 'Image not found'}, 404

        return image[0]['image'], 200

    except Exception:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def update_data_from_db(req, item_id, datatype, db):
    """
    Updates a specific music, author, or album record in the database.

    Args:
        req: HTTP POST request with update parameters or files.
        item_id (int): ID of the item to update.
        datatype (str): Type of item ('music', 'author', 'album').
        db: Database connection object.

    Returns:
        tuple: JSON response with status message and HTTP status code.
    """
    try:
        if not req or not item_id:
            return {'error': 'Invalid input'}, 400

        if req.method != 'POST':
            return {'error': 'Method Not Allowed'}, 405

        res = None
        data_db = DataModels(db)

        if datatype == 'music':
            if 'image' in req.files:
                image_file = req.files.get('image')
                image_data = image_file.read()
                if image_data:
                    res = data_db.update_music_image(image_data, item_id)

            elif "music_name" in req.form:
                music_name = [item.strip() for item in req.form.get('music_name').split('-')]
                if music_name and len(music_name) > 1:
                    res = data_db.update_music_name(music_name, item_id)

            elif 'music_date' in req.form:
                music_date = req.form.get('music_date').strip()
                if music_date and len(music_date) > 9:
                    res = data_db.update_music_date(music_date, item_id)

            elif 'album_id' in req.form:
                album_id = req.form.get('album_id').strip()
                if album_id.isdigit():
                    res = data_db.update_album_id_for_music(album_id, item_id)

            elif 'category' in req.form:
                category = req.form.get('category').strip()
                if category and len(category) > 1:
                    res = data_db.update_music_category(category, item_id)

            else:
                return {'error': 'Invalid request data'}, 400

        elif datatype == 'author':
            if 'image' in req.files:
                image_file = req.files.get('image')
                image_data = image_file.read()
                if image_data:
                    res = data_db.update_author_image(image_data, item_id)

            elif 'author_name' in req.form:
                author_name = req.form.get('author_name').strip()
                if author_name and len(author_name) > 1:
                    res = data_db.update_author_name(author_name, item_id)
            else:
                return {'error': 'Invalid request data'}, 400

        elif datatype == 'album':
            if 'image' in req.files:
                image_file = req.files.get('image')
                image_data = image_file.read()
                if image_data:
                    res = data_db.update_album_image(image_data, item_id)

            elif 'album_name' in req.form:
                album_name = req.form.get('album_name').strip()
                if album_name and len(album_name) > 1:
                    res = data_db.update_album_name(album_name, item_id)

            elif 'album_date' in req.form:
                album_date = req.form.get('album_date').strip()
                if album_date and len(album_date) > 9:
                    res = data_db.update_album_date(album_date, item_id)

            if 'author_id' in req.form:
                author_id = req.form.get('author_id').strip()
                if author_id.isdigit():
                    res = data_db.update_author_id_for_album(item_id, author_id)

            else:
                return {'error': 'Invalid request data'}, 400

        else:
            return {'error': 'Unknown entity type'}, 400

        if not res:
            return {'error': 'Data processing error'}, 422

        return {'message': 'Data updated successfully'}, 201
    except Exception:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def logout_pr():
    """
    Logs out the current user and clears authentication cookies.

    Returns:
        tuple: Redirect response to login page and HTTP status code.
    """
    try:
        response = make_response(redirect(url_for('auth.login')))
        response.delete_cookie('remember_token')
        logout_user()
        return response, 200
    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500