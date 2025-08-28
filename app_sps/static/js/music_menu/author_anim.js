
    document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.author-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.intersectionRatio >= 0.5) { // Карточка видима на 50% или больше
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Перестаем наблюдать за элементом после его появления
            }
        });
    }, { threshold: 0.5 }); // Срабатывает, когда видимость достигает 50%

    cards.forEach((card) => observer.observe(card));
});

