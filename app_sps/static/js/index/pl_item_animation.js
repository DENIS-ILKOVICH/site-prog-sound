
    document.addEventListener("DOMContentLoaded", function () {
        const playlistItems = document.querySelectorAll(".playlist-item");

        playlistItems.forEach(item => {
            item.addEventListener("click", function () {
                const songList = this.querySelector(".song-list");

                if (songList.style.maxHeight === "0px" || !songList.style.maxHeight) {

                    songList.style.display = "block";
                    songList.offsetHeight;
                    songList.style.maxHeight = songList.scrollHeight + "px";
                    songList.style.opacity = 1;
                } else {

                    songList.style.maxHeight = "0";
                    songList.style.opacity = 0;
                    setTimeout(() => {
                        songList.style.display = "none";
                    }, 500);
                }
            });
        });
    });

