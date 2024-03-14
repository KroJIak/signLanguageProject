document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('webcam');
    const overlayImage = document.getElementById('overlay-image');
    const errorOverlay = document.getElementById('error-overlay');
    const urlAPI = 'http://localhost:2468/service/detection/dictionary/0/gesture/В';
    const responseTime = 1000 / 25;
    let lastStartTime = 0;

    // Добавлено обновление размера canvas
    function updateCanvasSize() {
        overlayImage.width = video.videoWidth;
        overlayImage.height = video.videoHeight;
    }

    window.addEventListener('resize', updateCanvasSize);

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            video.onloadedmetadata = async () => {
                updateCanvasSize();
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
            if (lastStartTime < data.startTime) {
                drawPoints(data.points);
                drawLines(data.lines);
            }
            lastStartTime = data.startTime;
            hideErrorOverlay();
        } catch (error) {
            console.error('Ошибка при отправке изображения:', error);
            showErrorOverlay();
        }
    }

    function drawPoints(points) {
        const context = overlayImage.getContext('2d');
        context.clearRect(0, 0, overlayImage.width, overlayImage.height); // Очистка предыдущего кадра

        points.forEach(point => {
            const { pos, color, radius } = point;
            context.beginPath();
            context.arc(pos.x, pos.y, radius, 0, Math.PI * 2); // Рисуем круговую точку
            context.fillStyle = `rgba(${color.join(',')})`; // Устанавливаем цвет точки
            context.fill(); // Закрашиваем точку
        });
    }

    function drawLines(lines) {
        const context = overlayImage.getContext('2d');

        lines.forEach(line => {
            const { start, end, color, thickness } = line;
            context.beginPath();
            context.moveTo(start.x, start.y); // Устанавливаем начальную точку линии
            context.lineTo(end.x, end.y); // Устанавливаем конечную точку линии
            context.strokeStyle = `rgba(${color.join(',')})`; // Устанавливаем цвет линии
            context.lineWidth = thickness; // Устанавливаем толщину линии
            context.stroke(); // Рисуем линию
        });
    }

    function showErrorOverlay() {
        errorOverlay.style.opacity = 1;
        errorOverlay.style.pointerEvents = 'auto';
    }

    function hideErrorOverlay() {
        errorOverlay.style.opacity = 0;
        errorOverlay.style.pointerEvents = 'none';
    }
});
