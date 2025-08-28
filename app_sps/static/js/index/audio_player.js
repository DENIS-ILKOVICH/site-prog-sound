document.addEventListener("DOMContentLoaded", () => {
    const playPauseMainBtn = document.getElementById("play-pause-main");
    const prevTrackBtn = document.getElementById("prev-track");
    const nextTrackBtn = document.getElementById("next-track");
    const repeatBtn = document.getElementById("repeat-btn");
    const shuffleBtn = document.getElementById("shuffle-btn");
    const trackInfo = document.getElementById("current-track-info");
    const cards = document.querySelectorAll(".music-card");

    const progressSlider = document.getElementById("slider-progress");
    const currentTimeElement = document.getElementById("current-time");
    const durationTimeElement = document.getElementById("duration-time");

    const volumeSlider = document.getElementById("volume-slider");
    volumeSlider.value = 0.1;
    let currentVolume = 0.1;
    let audio = null;
    let currentTrackId = null;
    let isSeeking = false;
    let lastUpdateTime = null;
    let isRepeat = false;
    let isShuffle = false;

    volumeSlider.addEventListener("input", handleVolumeChange);
    repeatBtn.addEventListener("click", toggleRepeat);
    shuffleBtn.addEventListener("click", toggleShuffle);
    playPauseMainBtn.addEventListener("click", togglePlayPauseMain);
    nextTrackBtn.addEventListener("click", nextTrackHandler);
    prevTrackBtn.addEventListener("click", prevTrackHandler);
    progressSlider.addEventListener("input", handleProgressSliderInput);
    progressSlider.addEventListener("change", handleProgressSliderChange);

    // Обработчики карточек
    cards.forEach(card => {
        const playPauseBtn = card.querySelector(".play-pause-btn");
        playPauseBtn.addEventListener("click", () => handleCardClick(card));
    });

    // Обработчики прогресса
    const progressContainer = document.querySelector('.progress-container');
    progressContainer.addEventListener('mouseenter', () => setProgressSliderStyle('8px', '#ccc'));
    progressContainer.addEventListener('mouseleave', () => setProgressSliderStyle('4px', '#ccc'));

    function handleVolumeChange() {
        currentVolume = volumeSlider.value;
        if (audio) {
            audio.volume = currentVolume;
        }

        // Обновляем заливку слайдера
        const volumeFill = volumeSlider.querySelector('::before');
        const fillWidth = currentVolume * 100; // Вычисляем ширину заливки (в процентах)
        volumeSlider.style.setProperty('--volume-fill-width', `${fillWidth}%`);
    }

    // Обновление заливки громкости
    function updateVolumeSliderFill() {
        const value = volumeSlider.value;
        volumeSlider.style.background = `linear-gradient(to right, #f5d78f 0%, #f5d78f ${value * 100}%, #555 ${value * 100}%, #555 100%)`;
    }

    function toggleRepeat() {
        isRepeat = !isRepeat;
        const repeatImg = repeatBtn.querySelector("img");
        repeatImg.src = isRepeat ? "/static/images/repeat-on.png" : "/static/images/repeat-off.png";
    }

    function toggleShuffle() {
        isShuffle = !isShuffle;
        const shuffleImg = shuffleBtn.querySelector("img");
        shuffleImg.src = isShuffle ? "/static/images/shuffle-on.png" : "/static/images/shuffle-off.png";
    }

    function playTrack(trackId, artist, name) {
        if (audio) {
            audio.pause();
            audio = null;
        }

        audio = new Audio(`/music_audio/${trackId}`);
        audio.volume = currentVolume;

        audio.addEventListener("loadedmetadata", () => {
            durationTimeElement.textContent = formatTime(audio.duration);
            updateProgressBar();
        });

        audio.addEventListener("timeupdate", updateProgressBar);

        audio.addEventListener("ended", () => {
            if (isRepeat) {
                audio.currentTime = 0;
                audio.play();
            } else {
                nextTrack();
            }
        });

        audio.play();
        currentTrackId = trackId;

        trackInfo.textContent = `${artist} - ${name}`;
        updateCardState(trackId);
        updateMainButtonState(true);

        recordAudition(trackId);
    }
    function updateProgressBar() {
        if (audio && !isSeeking) {
            const progress = (audio.currentTime / audio.duration) * 100;
            progressSlider.value = progress;
            progressSlider.style.setProperty("--progress-fill-width", `${progress}%`);
            currentTimeElement.textContent = formatTime(audio.currentTime);
        }
    }


    function recordAudition(trackId) {
        fetch(`/auditions/${trackId}`, { method: "POST" })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Прослушивание записано!');
                }
            })
            .catch(error => {
                console.error("Ошибка записи прослушивания:", error);
            });
    }

    function formatTime(timeInSeconds) {
        if (isNaN(timeInSeconds)) return "00:00";
        const minutes = Math.floor(timeInSeconds / 60);
        const seconds = Math.floor(timeInSeconds % 60);
        return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    }

    function updateCardState(trackId) {
        cards.forEach(card => {
            const playPauseBtn = card.querySelector(".play-pause-btn");
            const playPauseImg = playPauseBtn.querySelector("img");
            if (parseInt(card.dataset.id) === trackId) {
                playPauseImg.src = "/static/images/pause3.png";
            } else {
                playPauseImg.src = "/static/images/play3.png";
            }
        });
    }

    function updateMainButtonState(isPlaying) {
        const playPauseImg = playPauseMainBtn.querySelector("img");
        playPauseImg.src = isPlaying ? "/static/images/pause.png" : "/static/images/play.png";
    }

    function updateProgressSmoothly(timestamp) {
        if (audio && !isSeeking && !audio.paused) {
            if (lastUpdateTime === null) {
                lastUpdateTime = timestamp;
            }
            const elapsed = (timestamp - lastUpdateTime) / 1000;
            lastUpdateTime = timestamp;

            const currentTime = audio.currentTime + elapsed;
            const progress = Math.min((currentTime / audio.duration) * 100, 100);

            progressSlider.value = progress;
            currentTimeElement.textContent = formatTime(audio.currentTime);
        }
        requestAnimationFrame(updateProgressSmoothly);
    }

    function resetProgress() {
        progressSlider.value = 0;
        progressSlider.style.setProperty("--progress-fill-width", "0%");
        currentTimeElement.textContent = "00:00";
    }

    function setProgressSliderStyle(height, backgroundColor) {
        progressSlider.style.height = height;
        progressSlider.style.backgroundColor = backgroundColor;
    }

    function nextTrack() {
        const currentCardIndex = Array.from(cards).findIndex(card => parseInt(card.dataset.id) === currentTrackId);
        let nextCard = isShuffle ? getRandomCard() : cards[(currentCardIndex + 1) % cards.length];
        const trackId = parseInt(nextCard.dataset.id);
        playTrack(trackId, nextCard.dataset.artist, nextCard.dataset.name);

        resetProgress();
    }

    function prevTrack() {
        const currentCardIndex = Array.from(cards).findIndex(card => parseInt(card.dataset.id) === currentTrackId);
        const prevCard = cards[(currentCardIndex - 1 + cards.length) % cards.length];
        const trackId = parseInt(prevCard.dataset.id);
        playTrack(trackId, prevCard.dataset.artist, prevCard.dataset.name);

        resetProgress();
    }

    function nextTrackHandler() {
        nextTrack();
        resetProgress();
    }

    function prevTrackHandler() {
        prevTrack();
        resetProgress();
    }

    function handleProgressSliderInput() {
        isSeeking = true;
        if (audio && !isNaN(audio.duration)) {
            const progress = progressSlider.value;
            audio.currentTime = (audio.duration * progress) / 100;
            currentTimeElement.textContent = formatTime(audio.currentTime);
        }
    }

    function handleProgressSliderChange() {
        isSeeking = false;
        lastUpdateTime = null;
    }

    function handleCardClick(card) {
        const trackId = parseInt(card.dataset.id);
        const artist = card.dataset.artist;
        const name = card.dataset.name;

        if (currentTrackId === trackId && !audio.paused) {
            audio.pause();
            updateMainButtonState(false);
            updateCardState(null);
        } else {
            playTrack(trackId, artist, name);
        }
    }

    function getRandomCard() {
        return cards[Math.floor(Math.random() * cards.length)];
    }

    function togglePlayPauseMain() {
        if (audio && !audio.paused) {
            audio.pause();
            updateMainButtonState(false);
            updateCardState(null);
        } else if (audio) {
            audio.play();
            updateMainButtonState(true);
            updateCardState(currentTrackId);
        }
    }
});
