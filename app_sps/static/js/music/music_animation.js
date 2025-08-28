
    document.addEventListener('DOMContentLoaded', function () {
        // Переключение видимости меню плейлиста
        const playlistTitle = document.querySelector('.playlist-title');
        const playlistMenu = document.querySelector('.playlist-menu');

        playlistTitle.addEventListener('click', function () {
            if (playlistMenu.classList.contains('show')) {
                playlistMenu.style.maxHeight = '0';  // Закрыть меню
                playlistMenu.style.padding = '0';  // Скрыть отступы
                playlistMenu.style.marginTop = '0';  // Убрать отступ сверху
            } else {
                playlistMenu.style.maxHeight = '1000px';  // Открыть меню
                playlistMenu.style.padding = '10px';  // Добавить отступы
                playlistMenu.style.marginTop = '10px';  // Добавить отступ сверху
            }
            playlistMenu.classList.toggle('show');
        });

        // Плавное открытие/закрытие формы для создания плейлиста
        const createPlaylistText = document.querySelector('.create-playlist-text');
        const createPlaylistForm = document.querySelector('.create-playlist');

        createPlaylistText.addEventListener('click', function () {
            createPlaylistForm.classList.toggle('show');
            if (createPlaylistForm.classList.contains('show')) {
                createPlaylistForm.style.opacity = '1';  // Плавное появление формы
                createPlaylistForm.style.transition = 'opacity 0.5s ease-in-out';  // Плавный переход
            } else {
                createPlaylistForm.style.opacity = '0';  // Плавное исчезновение формы
            }
        });

        // Плавная анимация радиокнопок при их выборе
        const playlistRadios = document.querySelectorAll('.playlist-radio');
        playlistRadios.forEach(function (radio) {
            radio.addEventListener('change', function () {
                playlistRadios.forEach(function (otherRadio) {
                    if (otherRadio !== radio) {
                        otherRadio.checked = false;
                    }
                });
            });
        });

        // Управление плавным изменением фона для активных радио кнопок
        const playlistLabels = document.querySelectorAll('.playlist-label');
        playlistLabels.forEach(function(label) {
            label.addEventListener('transitionend', function () {
                if (label.previousElementSibling.checked) {
                    label.style.transition = 'background-color 0.3s, color 0.3s';
                }
            });
        });
    });
