
    document.addEventListener("DOMContentLoaded", () => {
        const listItems = document.querySelectorAll(".random-music-item");

        // Используем IntersectionObserver для появления элементов списка
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry, index) => {
                    if (entry.isIntersecting) {
                        const delay = index * 0.1; // Задержка между появлениями элементов
                        entry.target.classList.add("visible");
                        entry.target.style.transitionDelay = `${delay}s`; // Применяем задержку
                        observer.unobserve(entry.target); // Останавливаем наблюдение после появления
                    }
                });
            },
            {
                threshold: 0.1, // Когда 10% элемента в поле зрения
            }
        );

        listItems.forEach((item) => observer.observe(item)); // Применяем наблюдатель ко всем элементам списка
    });
