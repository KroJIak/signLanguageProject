async function setupCamera() {
    const video = document.getElementById("camera");
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error accessing camera:", err);
    }
}

const imgElement = document.createElement("img");
document.body.appendChild(imgElement);

async function captureImage() {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const image_data = canvas.toDataURL("image/jpeg");

    const response = await fetch("/img/get-test", {
        method: "POST",
        body: image_data,
    });

    if (response.ok) {
        const imageBytes = await response.arrayBuffer();
        const imageUrl = URL.createObjectURL(new Blob([imageBytes]));
        imgElement.src = imageUrl;
    }
}

setupCamera().then(() => {
    setInterval(captureImage, 1000/30);
});
