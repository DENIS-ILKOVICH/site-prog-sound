from flask import *
from flask_login import *
from app_sps.playlist.models.models import Playlist
import json
from app_sps.logs.logclass import logger

def playlist_crate(req, db):
    """
    Create a new playlist with a default image.

    Args:
        req: Flask request object containing form data with playlist name.
        db: Database connection.

    Returns:
        tuple: JSON response with status and message or playlist info, and HTTP status code.
    """
    try:
        if not req:
            return {'status': 'error', 'message': 'Invalid input'}, 400

        if 'name' not in request.form:
            return {'status': 'error', 'message': 'Playlist name is required'}, 400

        playlist = Playlist(db)

        response = {}

        name = request.form.get('name', '').strip()
        image_path = 'app_sps/static/images/default_pl_img.png'

        if not all([name, image_path]):
            raise ValueError('data processing error!')

        with open(image_path, 'rb') as file:
            binary_image = file.read()

        user_id = current_user.get_id()
        cr_pl_status = playlist.create_plst_db(user_id, name, binary_image)

        if not cr_pl_status:
            raise ValueError('Data processing error!')

        response['status'] = 'success'
        response['name'] = name

        return response, 201

    except ValueError as e:
        return {'status': 'error', 'message': f'Invalid input. Details:{str(e)}'}, 422
    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'status': 'error', 'message': 'An unexpected error occurred'}, 500


def playlist_show(db):
    """
    Retrieve all playlists for the current user, including associated music.

    Args:
        db: Database connection.

    Returns:
        tuple: JSON list of playlists with song details and HTTP status code.
    """
    try:

        user_id = current_user.get_id()

        playlist = Playlist(db)

        playlists = playlist.get_playlist(user_id)
        playlists_with_songs = playlist.get_playlist_music(
            user_id)

        playlists_with_songs_dict = {}

        for playlist in playlists_with_songs:

            try:
                song_list = json.loads(playlist['song_list'])
            except json.JSONDecodeError:
                song_list = []

            playlists_with_songs_dict[playlist['playlist_id']] = {
                'playlist_name': playlist['playlist_name'],
                'song_list': song_list
            }

        complete_playlists = []

        for playlist in playlists:
            if playlist['id'] in playlists_with_songs_dict:

                complete_playlists.append({
                    'playlist_id': playlist['id'],
                    'playlist_name': playlists_with_songs_dict[playlist['id']]['playlist_name'],
                    'song_list': playlists_with_songs_dict[playlist['id']]['song_list']
                })

            else:

                complete_playlists.append({
                    'playlist_id': playlist['id'],
                    'playlist_name': playlist['name'],
                    'song_list': []
                })

        return complete_playlists, 200

    except ValueError as e:
        return {'status': 'error', 'message': f'Invalid input. Details:{str(e)}'}, 422
    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'status': 'error', 'message': 'An unexpected error occurred'}, 500


def music_add_in_playlist(req, db):
    """
    Add a music track to a user's playlist.

    Args:
        req: Flask request object containing form data with music_id, music_name, and playlist_id.
        db: Database connection.

    Returns:
        tuple: JSON response with added music info and HTTP status code.
    """
    try:
        if not req:
            return {'error': 'Invalid input'}, 400

        music_id = 0
        music_name = ''

        if request.method == 'POST':
            playlist = Playlist(db)

            music_id = request.form.get('music_id', 0)
            music_name = request.form.get('music_name', 0)
            playlist_id = request.form.get('playlist_id', 0)

            if not all([music_id, music_name, playlist_id]):
                raise ValueError('Invalid input')

            cr_pl_status = playlist.add_music_in_plst(playlist_id, music_id)

            if not cr_pl_status:
                raise ValueError('Data processing error!')

        data = {
            'music_id': music_id,
            'music_name': music_name
        }

        return data, 201

    except ValueError as e:
        return {'status': 'error', 'message': f'Invalid input. Details: {str(e)}'}, 422
    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'status': 'error', 'message': 'An unexpected error occurred'}, 500


def playlist_image(pl_id, db):
    """
    Retrieve the image associated with a playlist.

    Args:
        pl_id (int): Playlist ID.
        db: Database connection.

    Returns:
        tuple: Binary image data and HTTP status code.
    """
    try:
        if not pl_id:
            return {'error': 'Invalid input'}, 400

        playlist = Playlist(db)

        image = playlist.playlist_img(pl_id)

        if not image:
            return {'error': 'Image not found'}, 404

        return image[0]['image'], 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'status': 'error', 'message': 'An unexpected error occurred'}, 500


def playlist_music(pl_id, db):
    """
    Retrieve a playlist and all music tracks associated with it.

    Args:
        pl_id (int): Playlist ID.
        db: Database connection.

    Returns:
        tuple: JSON object with playlist metadata and list of music tracks, and HTTP status code.
    """
    try:
        playlist = Playlist(db)

        playlist_data = playlist.get_playlist_one(pl_id)
        if not playlist_data:
            return {'error': 'Playlist not found'}, 404

        music_playlist = []
        music_pl = playlist.get_playlist_music_id(pl_id)
        for item in music_pl:
            music = playlist.music_one_second(item['music_id'])
            if music:
                music_playlist.append(music)

        data = {
            'playlist_data': playlist_data,
            'music_playlist': music_playlist
        }

        return data, 200
    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'status': 'error', 'message': 'An unexpected error occurred'}, 500


def all_plist_user(user_id, db):
    """
    Get all playlists belonging to a specific user.

    Args:
        user_id (int): User ID.
        db: Database connection.

    Returns:
        tuple: JSON list of playlists and HTTP status code.
    """
    try:
        if not user_id:
            return {'error': 'Invalid input'}, 400

        playlist = Playlist(db)
        plist_user = playlist.get_playlist(user_id)
        if not plist_user:
            return {'error': 'Playlist not found'}, 404

        return plist_user, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'status': 'error', 'message': 'An unexpected error occurred'}, 500


def change_data_playlist(pl_id, req, db, datatype):
    """
    Change playlist image or name.

    Args:
        pl_id (int): Playlist ID.
        req: Flask request object containing new data.
        db: Database connection.
        datatype (str): Type of data to change ('image' or 'name').

    Returns:
        tuple: JSON response with result message and HTTP status code.
    """
    try:
        if not all([pl_id, req, datatype]):
            return {'error': 'Invalid input'}, 400

        playlist = Playlist(db)
        response = {}

        if datatype == 'image':
            image_file = request.files.get('image', b"")
            if not image_file:
                return {'error': 'Image not found'}, 404

            image_data = image_file.read()
            res = playlist.change_img_pl(pl_id, image_data)
            if not res:
                return {'error': 'Data processing error!'}, 422

            response = {'message': 'The image has been successfully modified', 'datatype': 'image'}

        if datatype == 'name':
            name = req.form.get('name', '')
            if not name:
                return {'error': 'Name not found'}, 404

            res = playlist.change_name_pl(pl_id, name)
            if not res:
                return {'error': 'Data processing error!'}, 422

            response = {'message': 'The name was successfully modified', 'datatype': 'image'}

        return response, 201

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'status': 'error', 'message': 'An unexpected error occurred'}, 500


def remove_data_playlist(pl_id, datatype, db, m_id=None):
    """
    Delete an entire playlist or a specific music track from a playlist.

    Args:
        pl_id (int): Playlist ID.
        datatype (str): Type of deletion ('playlist' or 'music').
        db: Database connection.
        m_id (int, optional): Music ID, required if datatype is 'music'.

    Returns:
        tuple: JSON response with result message and HTTP status code.
    """
    try:
        if not all([pl_id, datatype]):
            return {'error': 'Invalid input'}, 400

        response = {}
        playlist = Playlist(db)

        if datatype == 'playlist':
            playlist.del_pl(pl_id)
            response = {'message': 'The removal was a success!', 'action': 'del_pl'}

        if datatype == 'music':
            if not m_id:
                return {'error': 'Invalid input'}, 400

            playlist.del_mus_pl(pl_id, m_id)
            response = {'message': 'The removal was a success!', 'action': 'del_mus'}

        return response, 201

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'status': 'error', 'message': 'An unexpected error occurred'}, 500
