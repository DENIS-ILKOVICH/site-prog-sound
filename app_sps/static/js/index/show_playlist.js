document.addEventListener('DOMContentLoaded', function () {
    function loadPlaylists() {
        fetch('/show_playlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(playlists => {
            const playlistContainer = document.getElementById('playlist');
            playlistContainer.innerHTML = '';

            if (playlists.length > 0) {
                playlists.forEach(item => {

                    const playlistItem = document.createElement('li');
                    playlistItem.className = 'playlist-item';

                    const playlistTitle = document.createElement('h3');
                    playlistTitle.textContent = item.playlist_name;
                    playlistItem.appendChild(playlistTitle);

                    const songList = document.createElement('ul');
                    songList.className = 'song-list';

                    if (item.song_list.length > 0) {
                        item.song_list.forEach(song => {
                            const songItem = document.createElement('li');
                            const songLink = document.createElement('a');
                            songLink.href = `/show_music/${song.id}/${encodeURIComponent(song.name)}`;
                            songLink.textContent = song.name;
                            songItem.appendChild(songLink);
                            songList.appendChild(songItem);
                        });
                    } else {
                        const emptyMessage = document.createElement('li');
                        emptyMessage.textContent = 'Playlist is empty';
                        songList.appendChild(emptyMessage);
                    }

                    playlistItem.appendChild(songList);
                    playlistContainer.appendChild(playlistItem);

                    playlistTitle.addEventListener('click', function () {
                        playlistItem.classList.toggle('open');
                    });
                });
            } else {
                const emptyMessage = document.createElement('li');
                emptyMessage.textContent = 'No available playlists';
                playlistContainer.appendChild(emptyMessage);
            }
        })
        .catch(error => {
            console.error('Error loading playlists:', error);
        });
    }

    loadPlaylists();
});

