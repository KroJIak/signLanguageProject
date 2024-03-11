document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('webcam');
    const overlayImage = document.getElementById('overlayImage');
    const errorOverlay = document.getElementById('error-overlay');
    const responseTime = 1000 / 20;
    const urlAPI = 'http://localhost:2468/service/detection/dictionary/0/gesture/А';

    function updateVideoSize() {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        video.style.width = windowWidth + 'px';
        video.style.height = windowHeight + 'px';
        overlayImage.style.width = windowWidth + 'px';
        overlayImage.style.height = windowHeight + 'px';
        errorOverlay.style.width = windowWidth + 'px';
        errorOverlay.style.height = windowHeight + 'px';
    }

    window.addEventListener('resize', updateVideoSize);

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            updateVideoSize();
            video.onloadedmetadata = async () => {
                setInterval(async () => {
                    await sendImageToServer();
                }, responseTime);
            };
        } catch (error) {
            console.error('Ошибка при получении доступа к вебкамере:', error);
            showErrorOverlay();
        }
    } else {
        console.error('Ваш браузер не поддерживает API getUserMedia');
        showErrorOverlay();
    }

    async function sendImageToServer() {
        if (!video.srcObject || !video.srcObject.active) {
            console.warn('Видеопоток с вебкамеры не активен.');
            return;
        }

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');

        // Отразим изображение по горизонтали
        context.translate(canvas.width, 0);
        context.scale(-1, 1);

        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        const base64String = canvas.toDataURL('image/jpeg');

        try {
            const response = await fetch(urlAPI, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', },
                body: JSON.stringify({
                    base64String: base64String
                }),
            });
            const data = await response.json();
            // Установим полученное изображение с альфа-каналом как фоновое изображение
            overlayImage.src = 'data:image/png;base64,' + data.base64String;
            hideErrorOverlay(); // Скрыть плашку ошибки
        } catch (error) {
            console.error('Ошибка при отправке изображения:', error);
            showErrorOverlay(); // Показать плашку ошибки
        }
    }

    function showErrorOverlay() {
        errorOverlay.style.opacity = 1; // Плавное появление
        errorOverlay.style.pointerEvents = 'auto'; // Включение перехвата событий
    }

    function hideErrorOverlay() {
        errorOverlay.style.opacity = 0; // Плавное затухание
        errorOverlay.style.pointerEvents = 'none'; // Выключение перехвата событий
    }
});
