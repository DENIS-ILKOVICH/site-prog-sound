document.addEventListener('DOMContentLoaded', function () {
    // Функция для загрузки и отображения плейлистов
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
            playlistContainer.innerHTML = ''; // Очистка контейнера перед загрузкой

            if (playlists.length > 0) {
                playlists.forEach(item => {
                    // Создание элемента для каждого плейлиста
                    const playlistItem = document.createElement('li');
                    playlistItem.className = 'playlist-item';

                    // Заголовок с названием плейлиста
                    const playlistTitle = document.createElement('h3');
                    playlistTitle.textContent = item.playlist_name;
                    playlistItem.appendChild(playlistTitle);

                    // Список песен
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
                        emptyMessage.textContent = 'Плейлист пуст';
                        songList.appendChild(emptyMessage);
                    }

                    playlistItem.appendChild(songList);
                    playlistContainer.appendChild(playlistItem);

                    // Добавление обработчика событий для открытия/закрытия плейлиста
                    playlistTitle.addEventListener('click', function () {
                        playlistItem.classList.toggle('open');
                    });
                });
            } else {
                const emptyMessage = document.createElement('li');
                emptyMessage.textContent = 'Нет доступных плейлистов';
                playlistContainer.appendChild(emptyMessage);
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки плейлистов:', error);
        });
    }

    // Загрузка плейлистов при загрузке страницы
    loadPlaylists();
});
