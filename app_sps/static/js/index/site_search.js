const searchResultsContainer = document.getElementById('search-results-container');
const searchInput = document.getElementById('search-input');

searchInput.addEventListener('input', function() {
    let searchQuery = this.value.trim().toLowerCase();

    const messageList = JSON.parse(searchInput.getAttribute('data-message-list') || '[]');

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
            resultsContainer.innerHTML = '';

            if (data.length > 0) {
                data.forEach(item => {
                    let itemHTML = '';

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

                    resultsContainer.innerHTML += itemHTML;
                });

                searchResultsContainer.classList.add('show');
            } else {
                if (messageList.length > 0) {
                    resultsContainer.innerHTML = `<p class="no-results">${messageList}</p>`;
                } else {
                    resultsContainer.innerHTML = '<p class="no-results">No results found.</p>';
                }
                searchResultsContainer.classList.add('show');
            }
        })
        .catch(error => {
            console.error('Error during search:', error);
        });
    } else {
        searchResultsContainer.classList.remove('show');
    }
});

