from flask import g, render_template, request, jsonify, send_file, abort, redirect, url_for
from flask_login import login_required
from app_sps.content.services.services import *
import random
from app_sps.playlist.services.services import playlist_show
import io
from ..locales.load_language import load_language
from . import content
from app_sps.logs.logclass import logger


@content.route('/', methods=['POST', 'GET'])
def index():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        print(request.cookies)

        lang = session.get('language', 'en')
        content_ln = load_language(lang)
        menu = content_ln['menu']

        response1, status_code1 = get_all_content(db)
        content_data = response1 if status_code1 == 200 else {}

        response2, status_code2 = playlist_show(db)
        playlist = response2 if status_code2 == 200 else None

        music_list = content_data.get('music', [])
        authors_list = content_data.get('authors', [])
        albums_list = content_data.get('albums', [])

        random_music = []
        if music_list:
            random_numbers = random.sample(range(len(music_list)), min(10, len(music_list)))
            random_music = [music_list[i] for i in random_numbers]


        return render_template(
            'music_menu.html',
            title=content_ln['sections']['home'],
            menu=menu,
            content_ln=content_ln,
            author=authors_list,
            albums=albums_list,
            random_music=random_music,
            playlist=playlist
        )
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/show_music_category/<category>', methods=['GET'])
def show_music_category(category):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = get_music_category(db, category)
        category_music = response if status_code == 200 else {}

        response2, status_code2 = playlist_show(db)
        playlist = response2 if status_code2 == 200 else None

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('music_category.html', title=category, menu=menu, music=category_music,
                               category=category, playlist=playlist, content_ln=content_ln)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/show_music/<int:m_id>/<name>', methods=['GET'])
def show_music(m_id, name):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)

        response, status_code = get_all_data_from_music(db, m_id)

        music_data = response if status_code == 200 else {}

        music = music_data.get('music', [])
        album = music_data.get('albums', [])
        category_list = music_data.get('category', [])
        auditions_data = music_data.get('auditions', [])
        date_release = music_data.get('date_release', [])
        playlist_add = music_data.get('playlist_add', [])

        response2, status_code2 = playlist_show(db)
        playlist = response2 if status_code2 == 200 else None

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('music.html', title=name.replace('_', ' '), menu=menu, music=music,
                               album=album, category_list=category_list, auditions_data=auditions_data,
                               date_release=date_release, playlist_add=playlist_add, playlist=playlist, content_ln=content_ln)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/show_author/<int:a_id>/<name>', methods=['POST', 'GET'])
def show_author(a_id, name):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = get_all_data_from_author(a_id, name, db)
        author_data = response if status_code == 200 else {}

        response2, status_code2 = playlist_show(db)
        playlist = response2 if status_code2 == 200 else None

        author = author_data.get('author', [])
        albums = author_data.get('albums', [])
        music = author_data.get('music', [])
        auditions_data = author_data.get('auditions_data', [])
        best_track = author_data.get('best_track', [])
        best_genre = author_data.get('best_genre', [])
        first_track = author_data.get('first_track', [])

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('author.html', author=author, menu=menu, albums=albums, music=music,
                               title=name.replace('_', ' '), auditions_data=auditions_data,
                               best_track=best_track, first_track=first_track, best_genre=best_genre, playlist=playlist, content_ln=content_ln)

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/show_albums/<int:al_id>/<name>', methods=['POST', 'GET'])
def show_albums(al_id, name):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = get_all_data_from_album(al_id, db)
        album_data = response if status_code == 200 else {}

        response2, status_code2 = playlist_show(db)
        playlist = response2 if status_code2 == 200 else None

        album = album_data.get('albums_data', [])
        music = album_data.get('music_data', [])
        author = album_data.get('author_data', [])
        best_track = album_data.get('best_track_data', [])
        auditions_data = album_data.get('auditions_data', [])
        date_release = album_data.get('date_release_data', [])


        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('album.html', author=author, menu=menu, albums=album, music=music, playlist=playlist,
                               title=name.replace('_', ' '), auditions_data=auditions_data, best_track=best_track,
                               date_release=date_release, content_ln=content_ln)

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/authors', methods=['POST', 'GET'])
def authors():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = get_content_data('authors', db)
        authors = response if status_code == 200 else []

        response2, status_code2 = playlist_show(db)
        playlist = response2 if status_code2 == 200 else None

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('authors_full.html', menu=menu, author=authors, title=content_ln['sections']['performers'], playlist=playlist, content_ln=content_ln)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/albums', methods=['POST', 'GET'])
def albums():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = get_content_data('albums', db)
        print(response, status_code)
        albums = response if status_code == 200 else []

        response2, status_code2 = playlist_show(db)
        playlist = response2 if status_code2 == 200 else None

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('albums_full.html', menu=menu, albums=albums, title=content_ln['sections']['albums'], playlist=playlist, content_ln=content_ln)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/all_music', methods=['POST', 'GET'])
def all_music():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = get_content_data('music', db)
        music = response if status_code == 200 else []

        response2, status_code2 = playlist_show(db)
        playlist = response2 if status_code2 == 200 else None

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('all_music.html', menu=menu, music=music, title=content_ln['sections']['music'], playlist=playlist, content_ln=content_ln)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/site_search', methods=['POST'])
def site_search():
    try:
        logger.log_request(request)

        search_request = request.json.get('search', '').strip().lower()

        response, status_code = site_search_data(search_request)
        search_list = response if status_code == 200 else {}

        return jsonify(search_list)


    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/<string:datatype>_img/<int:item_id>')
def get_image(datatype, item_id):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = get_image_data(datatype, item_id, db)
        if status_code == 200 and isinstance(response, (bytes, bytearray)):
            return send_file(io.BytesIO(response), mimetype='image/jpeg')

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    return send_file(io.BytesIO(b''), mimetype='image/jpeg')


@content.route('/music_audio/<int:m_id>')
def music_audio(m_id):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = get_music_audio(m_id, db)
        if status_code == 200 and isinstance(response, (bytes, bytearray)):
            return send_file(io.BytesIO(response), mimetype='audio/mpeg')


    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    return send_file(io.BytesIO(b''), mimetype='image/jpeg')


@content.route('/auditions/<int:m_id>', methods=['POST'])
@login_required
def auditions(m_id):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        if request.method == 'POST':
            response, status_code = add_audit(m_id, current_user.get_id(), db)
            audit_add_status = response if status_code == 201 else {"success": False}

            print(response, status_code)
            return jsonify(audit_add_status)

        abort(404)

    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/change_language/<lang>', methods=['POST', "GET"])
def change_language(lang):
    try:
        logger.log_request(request)

        response, status_code = add_language(lang)
        return response
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@content.route('/language', methods=['POST'])
def language():
    try:
        logger.log_request(request)

        response, status_code = get_language(request)
        print(response, status_code)

        return redirect(url_for('content.index'))
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


