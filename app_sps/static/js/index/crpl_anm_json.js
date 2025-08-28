// Инициализация анимации Lottie с локальным JSON
const toastAnimationContainer = document.getElementById('toast-animation');
const toastAnimation = lottie.loadAnimation({
    container: toastAnimationContainer, // Элемент, где будет отображаться анимация
    renderer: 'svg',
    loop: false,
    autoplay: false,
    path: '/static/animation_icon/create_success.json'
});

// Функция для показа уведомления
function showToast(message, callback, animate = true) {
    const toast = document.getElementById('toast');

    const toastMessage = document.getElementById('toast-message');

    toastMessage.textContent = message;
    toast.classList.add('show');

    if (animate) {
        toastAnimationContainer.style.display = 'block'; // Показываем анимацию
        toastAnimation.play();
    } else {
        toastAnimationContainer.style.display = 'none'; // Скрываем анимацию
    }

    setTimeout(() => {
        toast.classList.remove('show');
        toastAnimation.stop();
        if (typeof callback === 'function') {
            callback();
        }
    }, 2000);
}

// Обработчик отправки формы
document.getElementById('create-playlist-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const dataInput = document.getElementById('create-playlist-form')
    const messageList = JSON.parse(dataInput.getAttribute('data-createpl-list') || '[]'); // Преобразуем строку JSON в массив
    const form = event.target;
    const nameInput = document.getElementById('playlist-name');
    const playlistName = nameInput.value.trim();

    if (!playlistName) {
        showToast(messageList[0], null, false);
        return;
    }

    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const result = await response.json();

        if (result.status === 'success') {
            showToast(messageList[1], () => {
                location.reload();
            }, true); // Анимация только при успехе
            nameInput.value = ''; // Очистить поле ввода
        } else {
            showToast(`${messageList[3]}: ${result.message}`, null, false);
        }
    } catch (error) {
        showToast(messageList[2], null, false);
    }
});
