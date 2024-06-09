// static/js/script.js
let maxDistance = 1000 * 60 * 60 * 20; // 20時間をミリ秒に変換

const updateRangeValue = (value) => {
    document.getElementById('range-value').textContent = value;
    maxDistance = 1000 * 60 * 60 * value; // スライダーの値をミリ秒に変換
    updateCountdown(); // 値が変更されたら即座に反映する
};

const updateCountdown = () => {
    const events = JSON.parse(document.getElementById('events-data').textContent);

    // コンソールにevents_infoを表示
    // console.log(events);

    const now = new Date().getTime();

    // const imgElement = document.getElementById('satellite-img');
    // const maxDistance = 20 * 60 * 60 * 1000; // 20時間をミリ秒に変換

    events.forEach((event, index) => {
        const eventTime = new Date(event.time).getTime();
        const distance = eventTime - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24)).toString().padStart(2, '0');
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toString().padStart(2, '0');
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toString().padStart(2, '0');
        const seconds = Math.floor((distance % (1000 * 60)) / 1000).toString().padStart(2, '0');
        // const milliseconds = Math.floor(distance % 1000 / 10).toString().padStart(2, '0');  // ミリ秒の上2桁


        const countdownElement = document.getElementById(`countdown-${index}`);
        countdownElement.innerHTML = `${hours}:${minutes}:${seconds}`;

        // 移動範囲を設定 (例として、0から80%の範囲で移動)
        // const totalDistance = 1000 * 60 * 60 * 20; // 20時間をミリ秒に変換
        const maxLeft = window.innerWidth * 0.8; // 80%の範囲で移動
        // const leftPosition = Math.max(0, Math.min(maxLeft, maxLeft * (1 - distance / maxDistance)));
        const rightPosition = Math.max(0, Math.min(maxLeft, maxLeft * (1 - distance / maxDistance)));

        const satelliteWrapper = document.getElementById(`satellite-wrapper-${index}`);
        // satelliteWrapper.style.left = `${leftPosition}px`;
        satelliteWrapper.style.right = `${rightPosition}px`;

        if (distance < 0) {
            countdownElement.innerHTML = "通過済み";
        }
    });

    // 福岡マーカーの位置を設定
    const fukuokaMarker = document.querySelector('.fukuoka-marker');
    fukuokaMarker.style.left = `${window.innerWidth * 0.8}px`;


};

setInterval(updateCountdown, 1000);

window.onload = () => {
    updateCountdown();
    // 福岡マーカーの位置を設定
    const fukuokaMarker = document.querySelector('.fukuoka-marker');
    fukuokaMarker.style.left = `${window.innerWidth * 0.8}px`;
};

window.onresize = () => {
    // 福岡マーカーの位置を設定
    const fukuokaMarker = document.querySelector('.fukuoka-marker');
    fukuokaMarker.style.left = `${window.innerWidth * 0.8}px`;
};

if (window.DeviceMotionEvent) {
    window.addEventListener('devicemotion', function (event) {
        const acceleration = event.acceleration;
        document.getElementById('acceleration').textContent = `X: ${acceleration.x.toFixed(2)}, Y: ${acceleration.y.toFixed(2)}, Z: ${acceleration.z.toFixed(2)}`;
    }, true);
} else {
    document.getElementById('acceleration').textContent = "DeviceMotionEvent is not supported on your device.";
}

// 加速度センサーのデータを利用して画像の位置を変更
// if (window.DeviceMotionEvent) {
//     window.addEventListener('devicemotion', function (event) {
//         const acceleration = event.accelerationIncludingGravity;
//         const satelliteWrapper = document.querySelector('.satellite-wrapper');

//         // 簡単な例として、加速度センサーのデータを画像の位置に反映
//         const xPos = (window.innerWidth / 2) + acceleration.x * 10; // スケール調整
//         const yPos = (window.innerHeight / 2) + acceleration.y * 10; // スケール調整

//         satelliteWrapper.style.transform = `translate(${xPos}px, ${yPos}px)`;
//     }, true);
// } else {
//     console.log("DeviceMotionEvent is not supported on your device.");
// }