
// Получаем ссылку на контейнер с результатами поиска
const searchResultsContainer = document.getElementById('search-results-container');
const searchInput = document.getElementById('search-input');

searchInput.addEventListener('input', function() {
    let searchQuery = this.value.trim().toLowerCase();

    // Получаем данные из элемента data-message-list
    const messageList = JSON.parse(searchInput.getAttribute('data-message-list') || '[]'); // Преобразуем строку JSON в массив

    // Проверяем, что запрос не пустой
    if (searchQuery.length > 0) {
        fetch('/site_search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ search: searchQuery })
        })
        .then(response => response.json())
        .then(data => {
            let resultsContainer = document.getElementById('search-results');
            resultsContainer.innerHTML = '';  // Очищаем старые результаты

            if (data.length > 0) {
                data.forEach(item => {
                    let itemHTML = '';

                    // Формируем HTML для каждого элемента в зависимости от его типа
                    if (item.type === 'music') {
                        itemHTML = `
                            <a href="/show_music/${item.id}/${item.name.replace(' ', '_')}">
                                <div class="search-item">
                                    <img src="/music_img/${item.id}">
                                    <p>${item.name}</p>
                                </div>
                            </a>
                        `;
                    } else if (item.type === 'author') {
                        itemHTML = `
                            <a href="/show_author/${item.id}/${item.name}">
                                <div class="search-item">
                                    <img src="/author_img/${item.id}">
                                    <p>${item.name}</p>
                                </div>
                            </a>
                        `;
                    } else if (item.type === 'album') {
                        itemHTML = `
                            <a href="/show_albums/${item.id}/${item.name}">
                                <div class="search-item">
                                    <img src="/album_img/${item.id}">
                                    <p>${item.name}</p>
                                </div>
                            </a>
                        `;
                    }

                    resultsContainer.innerHTML += itemHTML; // Добавляем новый результат
                });

                // Показываем блок с результатами
                searchResultsContainer.classList.add('show');
            } else {
                // Если ничего не найдено, добавляем данные из messageList
                if (messageList.length > 0) {
                    resultsContainer.innerHTML = `<p class="no-results">${messageList}</p>`;
                } else {
                    resultsContainer.innerHTML = '<p class="no-results">Ничего не найдено.</p>';
                }
                searchResultsContainer.classList.add('show');
            }
        })
        .catch(error => {
            console.error('Ошибка при поиске:', error);
        });
    } else {
        // Скрываем блок с результатами, если поле ввода пустое
        searchResultsContainer.classList.remove('show');
    }
});
