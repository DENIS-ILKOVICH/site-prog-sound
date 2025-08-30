const images = [
    {% for album in albums %}
        {
            main: "{{ url_for('albums_img', al_id=album.id) }}",
            name: "{{ album.name }}",
            link: "{{ url_for('show_albums', al_id=album.id, name=album.name | replace(' ', '_')) }}"
        }{% if not loop.last %},{% endif %}
    {% endfor %}
];

let currentSlide = 0;

function switchSlide() {
    const slider = document.querySelector('.slider');
    const mainImage = document.getElementById('main-image');
    const switchImage = document.getElementById('switch-image');
    const albumTitle = document.getElementById('album-title');
    const albumLink = document.getElementById('album-link');

    if (images.length <= 1) return;

    slider.classList.add('transition');
    albumTitle.classList.add('transition');
    albumLink.style.pointerEvents = 'none';

    setTimeout(() => {
        currentSlide = (currentSlide + 1) % images.length;
        mainImage.src = images[currentSlide].main;

        const nextSlide = (currentSlide + 1) % images.length;
        switchImage.src = images[nextSlide].main;

        albumTitle.textContent = images[currentSlide].name;
        albumLink.href = images[currentSlide].link;

        setTimeout(() => albumTitle.classList.remove('transition'), 1000);
        slider.classList.remove('transition');

        setTimeout(() => albumLink.style.pointerEvents = 'auto', 1000);
    }, 1000);
}
