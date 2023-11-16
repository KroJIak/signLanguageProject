async function setupCamera() {
    const video = document.getElementById("camera");
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error accessing camera:", err);
    }
}

function captureImage() {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const image_data = canvas.toDataURL("image/jpeg");

    fetch("/img/get-test", {
        method: "POST",
        body: image_data,
    });
}

setupCamera().then(() => {
    setInterval(captureImage, 1000/60); // Захват и отправка изображения с интервалом 1/60 секунды
});