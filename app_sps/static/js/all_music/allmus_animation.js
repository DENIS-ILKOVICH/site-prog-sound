
document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".cart-music");

    // Используем IntersectionObserver для отслеживания появления карточек
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    const delay = index * 0.1; // Задержка между появлениями
                    entry.target.classList.add("visible");
                    entry.target.style.transitionDelay = `${delay}s`; // Устанавливаем задержку
                    observer.unobserve(entry.target); // Останавливаем наблюдение после появления
                }
            });
        },
        {
            threshold: 0.2, // Когда 20% карточки в поле зрения
        }
    );

    cards.forEach((card) => observer.observe(card)); // Применяем наблюдатель ко всем карточкам
});