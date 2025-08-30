
const playlistLink = document.querySelector('.show-playlist-href');
const playlist = document.getElementById('playlist');
const contentUnderPlaylist = document.querySelector('.content-under-playlist');


playlistLink.addEventListener('click', function() {

    playlist.classList.toggle('show');


    if (playlist.classList.contains('show')) {
        contentUnderPlaylist.style.marginTop = '300px';
    } else {
        contentUnderPlaylist.style.marginTop = '0';
    }
});
