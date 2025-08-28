from flask import *
from . import admin
from flask_login import current_user, login_required
from .services.services import authorize_admin, fetch_and_search_data, insert_data_in_db, \
    remove_data_from_db, update_data_from_db, get_image_data, logout_pr
from ..locales.load_language import load_language
from app_sps.logs.logclass import logger
import io

@admin.route('/login', methods=['POST', 'GET'])
def login():
    try:
        logger.log_request(request)

        if current_user.is_authenticated:
            return redirect(url_for('admin.main'))

        db = getattr(g, 'db', None)
        if request.method == 'POST':
            response, status_code = authorize_admin(request, db)
            print(response, status_code)
            if status_code == 200:
                return redirect(url_for('admin.main'))

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        return render_template('login_admin.html', title='Login', content_ln=content_ln)

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise

@admin.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = logout_pr()
        logout_status = response if status_code == 200 else None
        return logout_status
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise

@admin.route('/', methods=['POST', 'GET'])
def main():
    try:
        logger.log_request(request)

        if not current_user.is_authenticated:
            return redirect(url_for('admin.login'))

        print(session)
        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu_admin']
        return render_template('main.html', title='Main', menu=menu, content_ln=content_ln)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@admin.route('/music/<action>', methods=['POST', 'GET'])
def music(action):
    try:
        logger.log_request(request)

        if not current_user.is_authenticated:
            return redirect(url_for('admin.login'))

        db = getattr(g, 'db', None)
        response, status_code = fetch_and_search_data(request, 'music', db)

        music_list = response.get('music_list', []) if status_code == 200 else []
        albums_list = response.get('albums_list', []) if status_code == 200 else []

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu_admin']

        if action == 'add':
            return render_template('add_music.html', title='Music', menu=menu, music_list=music_list, album_list=albums_list,
                                   content_ln=content_ln)
        elif action == 'update':
            return render_template('change_music.html', title='Music', menu=menu, music=music_list, content_ln=content_ln)
        else:
            abort(404)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@admin.route('/authors/<action>', methods=['POST', 'GET'])
def authors(action):
    try:
        logger.log_request(request)

        if not current_user.is_authenticated:
            return redirect(url_for('admin.login'))

        db = getattr(g, 'db', None)
        response, status_code = fetch_and_search_data(request, 'authors', db)
        authors_list = response.get('authors_list', []) if status_code == 200 else []

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu_admin']

        if action == 'add':
            return render_template('add_author.html', menu=menu, title='Performers', authors_list=authors_list,
                            content_ln=content_ln)
        elif action == 'update':
            return render_template('change_authors.html', title='Performers', menu=menu, authors=authors_list, content_ln=content_ln)
        else:
            abort(404)

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@admin.route('/albums/<action>', methods=['POST', 'GET'])
def albums(action):
    try:
        logger.log_request(request)

        if not current_user.is_authenticated:
            return redirect(url_for('admin.login'))

        db = getattr(g, 'db', None)
        response, status_code = fetch_and_search_data(request, 'albums', db)

        albums_list = response.get('albums_list', []) if status_code == 200 else []
        authors_list = response.get('authors_list', []) if status_code == 200 else []

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu_admin']
        if action == 'add':
            return render_template('add_albums.html', menu=menu, title='Albums', albums_list=albums_list,
                               authors_list=authors_list, content_ln=content_ln)
        elif action == 'update':
            return render_template('change_albums.html', title='Albums',menu=menu, albums=albums_list, content_ln=content_ln)
        else:
            abort(404)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@admin.route('/add_data_to_db/<datatype>/<action>', methods=['POST'])
def add_data_to_db(datatype, action):
    try:
        logger.log_request(request)

        if not current_user.is_authenticated:
            return redirect(url_for('admin.login'))

        db = getattr(g, 'db', None)

        response, status_code = insert_data_in_db(request, datatype, db)
        print(response, status_code)

        if datatype == 'music':
            return redirect(url_for('admin.music', action=action))
        if datatype == 'author':
            return redirect(url_for('admin.authors', action=action))
        if datatype == 'album':
            return redirect(url_for('admin.albums', action=action))
        else:
            return redirect(url_for('admin.main'))

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@admin.route('/remove_data/<int:item_id>/<datatype>/<action>', methods=['POST'])
def remove_data(item_id, datatype, action):
    try:
        logger.log_request(request)

        if not current_user.is_authenticated:
            return redirect(url_for('admin.login'))

        db = getattr(g, 'db', None)

        response, status_code = remove_data_from_db(request, item_id, datatype, db)
        print(response, status_code)

        if datatype == 'music':
            return redirect(url_for('admin.music', action=action))
        if datatype == 'author':
            return redirect(url_for('admin.authors', action=action))
        if datatype == 'album':
            return redirect(url_for('admin.albums', action=action))
        else:
            return redirect(url_for('admin.main'))

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@admin.route('/update_data/<int:item_id>/<datatype>/<action>', methods=['POST', 'GET'])
def update_data(datatype, item_id, action):
    try:
        logger.log_request(request)

        if not current_user.is_authenticated:
            return redirect(url_for('admin.login'))

        db = getattr(g, 'db', None)

        response, status_code = update_data_from_db(request, item_id, datatype, db)
        print(response, status_code)

        if datatype == 'music':
            return redirect(url_for('admin.music', action=action))
        if datatype == 'author':
            return redirect(url_for('admin.authors', action=action))
        if datatype == 'album':
            return redirect(url_for('admin.albums', action=action))
        else:
            return redirect(url_for('admin.main'))

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@admin.route('/get_image/<string:datatype>_img/<int:item_id>')
def get_image(datatype, item_id):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)

        response, status_code = get_image_data(datatype, item_id, db)
        print(response, status_code)

        if status_code == 200 and isinstance(response, (bytes, bytearray)):
            return send_file(io.BytesIO(response), mimetype='image/jpeg')

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    return send_file(io.BytesIO(b''), mimetype='image/jpeg')
