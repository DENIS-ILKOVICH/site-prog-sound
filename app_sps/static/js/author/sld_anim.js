
// Подготовка данных из шаблона
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

    // Проверка: если только один слайд, выход из функции
    if (images.length <= 1) return;

    // Плавный эффект анимации
    slider.classList.add('transition');
    albumTitle.classList.add('transition'); // Добавляем анимацию для названия

    // Убираем возможность перехода по ссылке во время анимации
    albumLink.style.pointerEvents = 'none';

    // Обновление изображений
    setTimeout(() => {
        currentSlide = (currentSlide + 1) % images.length;
        mainImage.src = images[currentSlide].main;

        // Обновление переключателя на следующий слайд
        const nextSlide = (currentSlide + 1) % images.length;
        switchImage.src = images[nextSlide].main;

        // Обновление названия альбома
        albumTitle.textContent = images[currentSlide].name;

        // Обновление ссылки на альбом
        albumLink.href = images[currentSlide].link;

        // Сброс анимации
        setTimeout(() => {
            albumTitle.classList.remove('transition'); // Убираем анимацию из названия
        }, 1000); // время анимации соответствует CSS
        slider.classList.remove('transition');

        // Включаем возможность клика по ссылке после завершения анимации
        setTimeout(() => {
            albumLink.style.pointerEvents = 'auto';
        }, 1000); // Время анимации
    }, 1000); // Время анимации
}

