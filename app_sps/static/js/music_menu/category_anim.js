
    document.addEventListener('DOMContentLoaded', function () {
    // Получаем все блоки
    const bigBlocks = document.querySelectorAll('.big-block');
    const smallBlocks = document.querySelectorAll('.small-block');

    // Объединяем все блоки в один массив
    const allBlocks = [...bigBlocks, ...smallBlocks];

    // Функция для добавления анимации с задержкой
    allBlocks.forEach((block, index) => {
        setTimeout(() => {
            block.classList.add('visible');
        }, 200 * index); // Устанавливаем задержку для каждого элемента (200ms)
    });
});

