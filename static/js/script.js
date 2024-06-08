// static/js/script.js

const updateCountdown = () => {
    const events = JSON.parse(document.getElementById('events-data').textContent);

    // コンソールにevents_infoを表示
    // console.log(events);

    const now = new Date().getTime();

    events.forEach((event, index) => {
        const eventTime = new Date(event.time).getTime();
        const distance = eventTime - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        const countdownElement = document.getElementById(`countdown-${index}`);
        countdownElement.innerHTML = `${days}日 ${hours}時間 ${minutes}分 ${seconds}秒`;

        if (distance < 0) {
            countdownElement.innerHTML = "通過済み";
        }
    });
};

setInterval(updateCountdown, 1000);
