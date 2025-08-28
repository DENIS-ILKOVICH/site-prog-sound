from flask import *
from flask_login import *
from app_sps.playlist.services.services import *
from ..locales.load_language import load_language
import io
from . import playlist
from app_sps.logs.logclass import logger



@playlist.route('/get_user_playlist', methods=['POST'])
@login_required
def get_user_playlist():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = playlist_show(db)
        pl = response if status_code == 200 else None
        return pl
    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@playlist.route('/create_playlist', methods=['POST', 'GET'])
@login_required
def create_playlist():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = playlist_crate(request, db)

        return jsonify(response)

    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    raise

@playlist.route('/add_music_in_playlist', methods=['POST'])
@login_required
def add_music_in_playlist():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = music_add_in_playlist(request, db)
        complete_playlists = response if status_code == 201 else {}

        if not complete_playlists:
            return redirect(url_for('content.index'))

        music_id = complete_playlists.get('music_id', 0)
        music_name = complete_playlists.get('music_name', 'Music')
        return redirect(url_for('content.show_music', m_id=int(music_id), name=music_name))


    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    raise

@playlist.route('/playlist_user', methods=['POST', 'GET'])
@login_required
def playlist_user():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response1, status_code1 = all_plist_user(current_user.get_id(), db)
        plist_user = response1 if status_code1 == 200 else False

        response2, status_code2 = playlist_show(db)
        playlist_data = response2 if status_code2 == 200 else []

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('playlist_user.html', title='Плейлисты', menu=menu, playlist_user=plist_user,
                               content_ln=content_ln, playlist=playlist_data)
    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@playlist.route('/playlist_img/<int:pl_id>')
def playlist_img(pl_id):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = playlist_image(pl_id, db)
        if status_code == 200 and isinstance(response, (bytes, bytearray)):
            return send_file(io.BytesIO(response), mimetype='image/jpeg')

    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    return send_file(io.BytesIO(b''), mimetype='image/jpeg')


@playlist.route('/music_pl_user/<int:pl_id>/<name>', methods=['POST', 'GET'])
@login_required
def music_pl_user(pl_id, name):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response1, status_code1 = playlist_music(pl_id, db)
        pl_music = response1 if status_code1 == 200 else False

        response2, status_code2 = playlist_show(db)
        playlist_ = response2 if status_code2 == 200 else []

        playlist_data = pl_music.get('playlist_data', [])
        music_playlist = pl_music.get('music_playlist', [])

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('music_pl_user.html', menu=menu, playlist_data=playlist_data, playlist=playlist_,
                               content_ln=content_ln, music_playlist=music_playlist, title=name.replace('_', ' '))
    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@playlist.route('/change_user_pl_img/<int:pl_id>/<name>', methods=['POST', "GET"])
@login_required
def change_user_pl_img(pl_id, name):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        if request.method == 'POST':
            response, staus_code = change_data_playlist(pl_id, request, db, 'image')
            # return jsonify(response)
        return redirect(url_for('playlist.music_pl_user', pl_id=pl_id, name=name))
    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@playlist.route('/change_user_pl_name/<int:pl_id>/<name_pl>', methods=['POST', "GET"])
@login_required
def change_user_pl_name(pl_id, name_pl):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        if request.method == 'POST':
            response, staus_code = change_data_playlist(pl_id, request, db, 'name')
            # return jsonify(response)
        return redirect(url_for('playlist.music_pl_user', pl_id=pl_id, name=name_pl))
    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@playlist.route('/delete_pl_user/<int:pl_id>', methods=['POST', 'GET'])
@login_required
def delete_pl_user(pl_id):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        if request.method == 'POST':
            response, status_code = remove_data_playlist(pl_id, 'playlist', db)
            print(response, status_code)

        return redirect(url_for('playlist.playlist_user'))
    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    raise

@playlist.route('/remove_music_in_pl/<int:pl_id>/<int:m_id>/<name>', methods=['POST', 'GET'])
@login_required
def remove_music_in_pl(pl_id, m_id, name):
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        if request.method == 'POST':
            response, status_code = remove_data_playlist(pl_id, 'music', db, m_id)
        # return jsonify(response)
        return redirect(url_for('playlist.music_pl_user', pl_id=pl_id, name=name))
    except Exception as e:
       logger.log_error("Internal Server Error", stack_trace=str(e))
    raise
