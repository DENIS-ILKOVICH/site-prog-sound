    // Получаем ссылку и форму
    const createPlaylistLink = document.querySelector('.create-playlist-href');
    const createPlaylistForm = document.getElementById('create-playlist-form');

    // Добавляем обработчик события для клика на ссылку
    createPlaylistLink.addEventListener('click', function(event) {
        event.preventDefault(); // Отменяем стандартное действие ссылки
        // Переключаем отображение формы
        if (createPlaylistForm.style.display === 'none') {
            createPlaylistForm.style.display = 'block';
        } else {
            createPlaylistForm.style.display = 'none';
        }
    });