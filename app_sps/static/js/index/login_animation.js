
   document.querySelector('.login').addEventListener('submit', async function (event) {
        event.preventDefault(); // Остановить стандартное поведение формы

        const formData = new FormData(this);
        const response = await fetch(this.action, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (result.success) {
            // Показать оверлей и контейнер
            document.getElementById('overlay').style.display = 'block';
            const container = document.getElementById('animation-container');
            container.style.display = 'block';

            // Запуск анимации
            const animation = lottie.loadAnimation({
                container: container,
                path: '/static/animation_icon/login_success.json',
                renderer: 'svg',
                loop: false,
                autoplay: true
            });

            // Редирект после завершения анимации
            animation.addEventListener('complete', () => {
                window.location.href = result.redirect;
            });
        } else {
            // Показать сообщение об ошибке
            const flashContainer = document.querySelector('.flash-messages');
            flashContainer.innerHTML = `<div class="messagetxt ${result.category}">${result.message}</div>`;
        }
    });
