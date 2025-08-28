
    document.addEventListener("DOMContentLoaded", function () {
        const playlistItems = document.querySelectorAll(".playlist-item");

        playlistItems.forEach(item => {
            item.addEventListener("click", function () {
                const songList = this.querySelector(".song-list");

                if (songList.style.maxHeight === "0px" || !songList.style.maxHeight) {
                    // Когда блок скрыт, показываем его с анимацией
                    songList.style.display = "block";  // Убедимся, что блок отображается
                    songList.offsetHeight;  // Принудительно перерисовываем элемент, чтобы анимация сработала
                    songList.style.maxHeight = songList.scrollHeight + "px";  // Анимация раскрытия
                    songList.style.opacity = 1;  // Плавное появление
                } else {
                    // Когда блок открыт, скрываем его с анимацией
                    songList.style.maxHeight = "0";
                    songList.style.opacity = 0;
                    setTimeout(() => {
                        songList.style.display = "none";  // Скрываем блок после анимации
                    }, 500);  // Время, равное длительности анимации
                }
            });
        });
    });

