function openModalSetting() {
  const modal = document.getElementById('settingsModal');
  modal.classList.remove('hide');
  modal.style.display = 'flex';
  // Даем браузеру применить display, чтобы анимация сработала
  requestAnimationFrame(() => {
    modal.classList.add('show');
  });
}

function closeModalSetting(event) {
  const modal = document.getElementById('settingsModal');
  if (event.target === modal) {
    modal.classList.remove('show');
    modal.classList.add('hide');
    setTimeout(() => modal.style.display = 'none', 500);
  }
}

        let currentLanguage = 'en'; // по умолчанию (будет перезаписано после запроса)

    function updateLanguageButton(lang) {
        currentLanguage = lang;
        const activeBtn = document.getElementById('activeLangBtn');
        activeBtn.src = `/static/images/${lang}.png`;
    }

    // Клик по активному языку — показать остальные, кроме текущего
    document.getElementById('activeLangBtn').addEventListener('click', () => {
        const otherLangs = document.getElementById('otherLangs');
        // Скрываем/показываем блок
        otherLangs.style.display = otherLangs.style.display === 'none' ? 'flex' : 'none';
        // Скрываем текущий язык внутри блока
        Array.from(otherLangs.children).forEach(img => {
            img.style.display = (img.dataset.lang === currentLanguage) ? 'none' : 'inline-block';
        });
    });

    // Клик по любому из остальных языков — просто выводим в консоль
    Array.from(document.querySelectorAll('#otherLangs .lang-btn')).forEach(img => {
        img.addEventListener('click', () => {
            console.log('Выбран язык:', img.dataset.lang);
            // Можно здесь также обновить серверный язык, если нужно
        });
    });

    // После получения языка с сервера (например после /active-language)
    function setLanguageFromServer(lang) {
        updateLanguageButton(lang);
    }

    // Пример использования с fetch
    function checkLanguageAndOpenModal() {
        fetch('/active-language')
            .then(response => {
                if (response.ok) return response.json();
                throw new Error('Ошибка запроса');
            })
            .then(data => {
                console.log('Ответ сервера:', data);
                setLanguageFromServer(data.language);
                openModalSetting();
            })
            .catch(error => console.error('Ошибка при запросе /active-language:', error));
    }
                    document.addEventListener('click', (e) => {
    if (!document.getElementById('languageSelector').contains(e.target)) {
        otherLangs.style.display = 'none';
    }
});

Array.from(document.querySelectorAll('#otherLangs .lang-btn')).forEach(item => {
    item.addEventListener('click', () => {
        const selectedLang = item.dataset.lang;

        // Отправляем запрос на сервер
        fetch(`/change_language/${selectedLang}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка при смене языка');
            return response.json(); // если сервер возвращает JSON
        })
        .then(data => {
            // Обновляем активный язык
            updateLanguageButton(selectedLang);
            // Перезагрузка страницы после успешного изменения
            window.location.reload();
        })
        .catch(error => {
            console.error('Ошибка при смене языка:', error);
        });
    });
});
// глобальная переменная состояния автологина (1 = включен, 0 = выключен)
let autoLoginStatus = 0;

// Проверяем статус автологина при открытии модалки
function checkAutoLoginStatus() {
    return fetch('/auth/check_autologin', {
        method: 'POST'
    })
    .then(response => response.json().then(data => ({status: response.status, body: data})))
    .then(result => {
        const autologinCheckbox = document.getElementById('autologin');

        if (result.status === 200 && result.body.status === 'success') {
            // Пользователь авторизован и токен есть → включаем
            autologinCheckbox.checked = true;
            autologinCheckbox.disabled = false;
            autoLoginStatus = 1;
        } else {
            // Токена нет или пользователь не авторизован
            autologinCheckbox.checked = false;
            autologinCheckbox.disabled = (result.status === 401); // если не авторизован — блокируем
            autoLoginStatus = 0;
        }
    })
    .catch(error => {
        console.error('Ошибка при запросе /check_login:', error);
        const autologinCheckbox = document.getElementById('autologin');
        autologinCheckbox.checked = false;
        autologinCheckbox.disabled = true;
        autoLoginStatus = 0;
    });
}

// Обработчик клика по чекбоксу
document.getElementById('autologin').addEventListener('change', function () {
    const newStatus = this.checked ? '1' : '0';

    fetch('/auth/autologin_checkbox', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({status: newStatus})
    })
    .then(response => response.json().then(data => ({status: response.status, body: data})))
    .then(result => {
        if (result.status === 200 && result.body.success) {
            console.log(result.body.message);
            autoLoginStatus = parseInt(newStatus);
        } else {
            console.error('Ошибка при изменении автологина:', result.body);
            // если сервер вернул ошибку — возвращаем чекбокс в исходное состояние
            this.checked = (autoLoginStatus === 1);
        }
    })
    .catch(error => {
        console.error('Ошибка при запросе /autologin_checkbox:', error);
        // возвращаем чекбокс обратно
        this.checked = (autoLoginStatus === 1);
    });
});

// Теперь открытие модалки делает два запроса: язык + автологин
function checkLanguageAndOpenModal() {
    Promise.all([
        fetch('/active-language')
            .then(response => {
                if (response.ok) return response.json();
                throw new Error('Ошибка запроса языка');
            })
            .then(data => {
                console.log('Ответ сервера (язык):', data);
                setLanguageFromServer(data.language);
            }),
        checkAutoLoginStatus()
    ])
    .then(() => {
        openModalSetting();
    })
    .catch(error => console.error('Ошибка при запросах перед открытием настроек:', error));
}

// Обработчик кнопки Login / Logout
document.querySelectorAll('.btn-logout').forEach(btn => {
    btn.addEventListener('click', () => {
        if (btn.textContent.trim() === 'Logout') {
            // Запрос на logout
            fetch('/auth/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    console.log('Успешный выход');
                    window.location.reload();
                } else {
                    console.error('Ошибка при выходе');
                }
            })
            .catch(error => console.error('Ошибка при запросе logout:', error));
        } else {
            // Редирект на страницу логина
            window.location.href = '/auth/login';
        }
    });
});
