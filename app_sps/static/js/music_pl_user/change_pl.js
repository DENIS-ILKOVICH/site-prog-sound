
    // Обработка клика по названию плейлиста
    // Клик по названию для его изменения
    document.querySelectorAll('.playlist-title-text').forEach((title) => {
        title.addEventListener('click', (event) => {
            const formId = event.target.getAttribute('data-form-id');
            const nameForm = document.getElementById(formId);

            // Скрываем текстовое название
            event.target.style.display = 'none';

            if (nameForm) {
                // Показываем форму
                nameForm.style.display = 'block';
                const input = nameForm.querySelector('.name-input');
                if (input) {
                    input.style.display = 'block'; // Показываем поле ввода
                    input.focus(); // Устанавливаем фокус на поле ввода
                }
            }
        });
    });

    // Автоматическая отправка формы при изменении названия
    document.querySelectorAll('.name-input').forEach((input) => {
        input.addEventListener('blur', () => {
            const form = input.closest('form');
            if (form) {
                form.submit(); // Отправляем форму
            }
        });
    });

    // Клик по изображению для смены обложки (из предыдущего примера)
    document.querySelectorAll('.playlist-img').forEach((img) => {
        img.addEventListener('click', (event) => {
            const inputId = event.target.getAttribute('data-input-id');
            const fileInput = document.getElementById(inputId);

            // Показываем графическое предупреждение
            const alertId = `alert-${inputId.split('-').pop()}`;
            const alertMessage = document.getElementById(alertId);
            if (alertMessage) {
                alertMessage.classList.add('alert-visible');
                setTimeout(() => {
                    alertMessage.classList.remove('alert-visible');
                }, 1500);
            }

            if (fileInput) {
                fileInput.click();
            }
        });
    });

    // Отправка формы при выборе файла
    document.querySelectorAll('.upload-input').forEach((input) => {
        input.addEventListener('change', () => {
            const form = input.closest('form');
            if (form) {
                form.submit();
            }
        });
    });

