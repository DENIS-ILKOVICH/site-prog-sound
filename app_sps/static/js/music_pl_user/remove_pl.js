// Инициализация анимации Lottie для удаления плейлиста
const removePlaylistAnimation = lottie.loadAnimation({
    container: document.getElementById('toast-animation-remove'),
    renderer: 'svg',
    loop: false,
    autoplay: false,
    path: '/static/animation_icon/remove_playlist.json'
});

// Функция для показа уведомления с анимацией удаления
function showToastRemove(message, callback) {
    const toast = document.getElementById('toast-remove');
    const toastMessage = document.getElementById('toast-message-remove');

    toastMessage.textContent = message;
    toast.classList.add('show');

    // Запускаем анимацию удаления
    removePlaylistAnimation.play();

    // Дожидаемся окончания анимации, затем скрываем уведомление
    removePlaylistAnimation.addEventListener('complete', () => {
        toast.classList.remove('show');
        removePlaylistAnimation.stop();
        if (typeof callback === 'function') {
            callback(); // Вызов функции после завершения анимации
        }
    });
}

// Открыть модальное окно
function openModal() {
    document.getElementById("modal").style.display = "block";
}

// Закрыть модальное окно
function closeModal() {
    document.getElementById("modal").style.display = "none";
}

// Подтверждение удаления плейлиста
function confirmDelete() {
    closeModal(); // Закрыть модальное окно
    showToastRemove('Плейлист успешно удалён!', () => {
        // После завершения уведомления отправляем форму
        document.querySelector('.remove-playlist-user').submit();
    });
}
