// static/js/script.js

const updateCountdown = () => {
    const events = JSON.parse(document.getElementById('events-data').textContent);

    // コンソールにevents_infoを表示
    // console.log(events);

    const now = new Date().getTime();
    const imgElement = document.getElementById('satellite-img');
    const maxDistance = 20 * 60 * 60 * 1000; // 20時間をミリ秒に変換

    events.forEach((event, index) => {
        const eventTime = new Date(event.time).getTime();
        const distance = eventTime - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        const countdownElement = document.getElementById(`countdown-${index}`);
        countdownElement.innerHTML = `${days}日 ${hours}時間 ${minutes}分 ${seconds}秒`;

        // 移動範囲を設定 (例として、0から80%の範囲で移動)
        const totalDistance = 1000 * 60 * 60 * 20; // 20時間をミリ秒に変換
        const maxLeft = window.innerWidth * 0.8; // 80%の範囲で移動
        const leftPosition = Math.max(0, Math.min(maxLeft, maxLeft * (1 - distance / totalDistance)));

        const satelliteImg = document.getElementById(`satellite-img-${index}`);
        satelliteImg.style.left = `${leftPosition}px`;

        if (distance < 0) {
            countdownElement.innerHTML = "通過済み";
        }
    });
};

setInterval(updateCountdown, 1000);
