document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('webcam');
    const overlayImage = document.getElementById('overlayImage');
    const errorOverlay = document.getElementById('error-overlay');
    let averageResponseTime = 0;
    let resultResponseTime = 0;
    const numberOfRequests = 10;
    const commonResponseTime = 1000 / 25;
    const alignmentCoefficient = 0.8;
    const urlAPI = 'http://localhost:8080/img/get-result';

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
                // Измеряем время для 10 запросов
                for (let i = 0; i < numberOfRequests; i++) {
                    const startTime = performance.now();
                    await sendImageToServer();
                    const endTime = performance.now();
                    const responseTime = endTime - startTime;
                    console.log(`Время ответа для запроса ${i + 1}: ${responseTime} мс`);
                    averageResponseTime += responseTime;
                }

                // Вычисляем среднее время
                console.log(`Среднее время ответа: ${averageResponseTime / numberOfRequests} мс`);

                averageResponseTime = (averageResponseTime / numberOfRequests) * alignmentCoefficient;

                console.log(`Среднее время ответа с коэффициентом: ${averageResponseTime} мс`);

                resultResponseTime = Math.max(averageResponseTime, commonResponseTime);

                // Запускаем регулярные запросы с частотой 1/30 секунды
                setInterval(async () => {
                    await sendImageToServer();
                }, resultResponseTime);
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

        const imageBase64 = canvas.toDataURL('image/jpeg');

        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        try {
            const response = await fetch(urlAPI, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    imageBase64: imageBase64,
                    responseTime: resultResponseTime,
                    windowSize: {
                        width: windowWidth,
                        height: windowHeight,
                    },
                }),
            });

            const data = await response.json();
            // Установим полученное изображение с альфа-каналом как фоновое изображение
            overlayImage.src = 'data:image/png;base64,' + data.overlayImageBase64;
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
