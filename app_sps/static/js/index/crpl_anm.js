
const createPlaylistLink = document.querySelector('.create-playlist-href');
const createPlaylistForm = document.getElementById('create-playlist-form');

createPlaylistLink.addEventListener('click', function(event) {
    event.preventDefault();

    if (createPlaylistForm.style.display === 'none') {
        createPlaylistForm.style.display = 'block';
    } else {
        createPlaylistForm.style.display = 'none';
    }
});