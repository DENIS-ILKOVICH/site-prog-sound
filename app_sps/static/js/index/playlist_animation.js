    // Получаем ссылку и список
    const playlistLink = document.querySelector('.show-playlist-href');
    const playlist = document.getElementById('playlist');
    const contentUnderPlaylist = document.querySelector('.content-under-playlist');

    // Добавляем обработчик события для клика по ссылке
    playlistLink.addEventListener('click', function() {
        // Переключаем класс 'show', чтобы показать/скрыть список
        playlist.classList.toggle('show');

        // Если плейлист раскрывается, добавляем сдвиг для элементов под ним
        if (playlist.classList.contains('show')) {
            contentUnderPlaylist.style.marginTop = '300px';  // Сдвигаем элементы вниз
        } else {
            contentUnderPlaylist.style.marginTop = '0';  // Возвращаем элементы в исходное положение
        }
    });
