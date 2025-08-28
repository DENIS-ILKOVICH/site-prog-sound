
    window.addEventListener('DOMContentLoaded', () => {
    const playlists = document.querySelectorAll('.playlist-user-block');

    playlists.forEach((playlist, index) => {
        setTimeout(() => {
            playlist.classList.remove('hidden');
            playlist.classList.add('visible');
        }, index * 220); // Задержка между появлениями (300ms для каждой карточки)
    });
});

