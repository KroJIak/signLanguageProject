document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('webcam');
    const overlayImage = document.getElementById('overlay-image');
    const errorOverlay = document.getElementById('error-overlay');
    const cameraSwitch = document.getElementById('camera-switch');
    const urlHost = window.location.origin;
    const dictionariesUrlAPI = `${urlHost}/db/dictionaries/get-dictionaries`;
    let responseTime;
    if (window.location.href.includes('ngrok')) responseTime = 1000 / 5;
    else responseTime = 1000 / 25;
    let lastStartTime = 0;

    // Функция для определения типа устройства
    function detectDeviceType() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ? 'mobile' : 'desktop';
    }

    function serviceUrlAPI(dictId, gestureName) {
        return `${urlHost}/service/detection/dictionary/${dictId}/gesture/${gestureName}`;
    }

    // Функция для создания кнопки на мобильных устройствах
    function createMobileCameraSwitch() {
        const button = document.createElement('button');
        button.innerHTML = '<img src="static/assets/camera-white.png" alt="Switch Camera">';
        button.onclick = toggleCamera;
        cameraSwitch.appendChild(button);
    }

    async function createDesktopCameraSwitch() {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(device => device.kind === 'videoinput');

        if (videoDevices.length > 1) {
            const select = document.createElement('select');
            select.onchange = changeCamera;
            cameraSwitch.appendChild(select);

            videoDevices.forEach(device => {
                const option = document.createElement('option');
                option.value = device.deviceId;
                option.text = device.label || `Camera ${select.length + 1}`;
                select.appendChild(option);
            });

            // Добавим класс для стилизации
            select.classList.add('transparent-select');
            }
        }


    // Функция для переключения между фронтальной и основной камерами на мобильных устройствах
    async function toggleCamera() {
        const stream = video.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => {
            track.stop();
        });

        const facingMode = video.getAttribute('facingMode');
        const newFacingMode = facingMode === 'user' ? 'environment' : 'user';

        const newStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: newFacingMode } });
        video.srcObject = newStream;
        video.setAttribute('facingMode', newFacingMode);

        // Отзеркаливание изображения, если переключили на основную камеру
        if (newFacingMode === 'environment') {
            video.style.transform = 'scaleX(1)';
            overlayImage.style.transform = 'scaleX(-1)';
        } else {
            video.style.transform = 'scaleX(-1)';
            overlayImage.style.transform = 'scaleX(1)';
        }
    }



    // Функция для смены камеры на компьютерах
    async function changeCamera() {
        const deviceId = this.value;
        const stream = await navigator.mediaDevices.getUserMedia({ video: { deviceId: deviceId } });
        video.srcObject = stream;
    }

    // Выбор соответствующего способа создания переключателя камеры в зависимости от типа устройства
    const blackOverlay = document.getElementById('black-overlay');
    if (detectDeviceType() === 'mobile') {
        blackOverlay.style.display = 'block';
        video.setAttribute('facingMode', 'user');
        createMobileCameraSwitch();
    } else {
        blackOverlay.style.display = 'none';
        createDesktopCameraSwitch();
    }



    // Добавлено обновление размера canvas
    function updateCanvasSize() {
        overlayImage.width = video.videoWidth;
        overlayImage.height = video.videoHeight;
    }

    async function loadDictionaries() {
        try {
            const response = await fetch(dictionariesUrlAPI);
            const data = await response.json();
            const dictionarySelect = document.getElementById('dictionary-select');

            if (data && data.dictionaries) {
                for (const index in data.dictionaries) {
                    if (data.dictionaries.hasOwnProperty(index)) {
                        const option = document.createElement('option');
                        option.value = index;
                        option.text = data.dictionaries[index];
                        dictionarySelect.appendChild(option);
                    }
                }
            }
        } catch (error) {
            console.error('Ошибка при загрузке словаря:', error);
        }
    }

    // Вызываем функцию загрузки словаря
    loadDictionaries();

    const dictionarySelect = document.getElementById('dictionary-select');
    const gestureSelect = document.getElementById('gesture-select');

    // Функция для загрузки жестов по выбранному словарю
    async function loadGestures() {
        const selectedDictId = dictionarySelect.value;
        // Очищаем список жестов при выборе "Пусто" или если словарь не выбран
        if (selectedDictId === "") {
            gestureSelect.innerHTML = '';
            gestureSelect.style.display = 'none'; // Скрываем список
            return;
        }

        try {
            const response = await fetch(`${urlHost}/db/gestures/get-gesture-names/dictionary/${selectedDictId}`);
            const data = await response.json();
            gestureSelect.innerHTML = ''; // Очищаем список перед добавлением новых элементов
            if (data && data.gestureNames) {
                // Сортируем список жестов перед добавлением в выпадающий список
                const sortedGestureNames = data.gestureNames.sort();
                sortedGestureNames.forEach(gestureName => {
                    const option = document.createElement('option');
                    option.value = gestureName;
                    option.text = gestureName;
                    gestureSelect.appendChild(option);
                });
                gestureSelect.style.display = 'block'; // Отображаем список
            }
        } catch (error) {
            console.error('Ошибка при загрузке жестов:', error);
        }
    }

    // Добавляем обработчик события change к элементу dictionarySelect
    dictionarySelect.addEventListener('change', loadGestures);


    // Функция для очистки canvas overlay-image
    function clearOverlayCanvas() {
        const overlayCanvas = document.getElementById('overlay-image');
        const context = overlayCanvas.getContext('2d');
        context.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
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
            let dictId, gestureName;
            const selectedDictId = dictionarySelect.value;
            const selectedGestureName = gestureSelect.value;
            if (selectedDictId !== "") {
                dictId = selectedDictId;
                gestureName = selectedGestureName;
            } else {
                dictId = -1;
                gestureName = '';
                clearOverlayCanvas();
            }
            if (dictId !== -1) {
                const response = await fetch(serviceUrlAPI(dictId, gestureName), {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({base64String}),
                });
                const data = await response.json();
                if (lastStartTime < data.startTime) {
                    drawPoints(data.points);
                    drawLines(data.lines);
                }
                lastStartTime = data.startTime;
            }
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
