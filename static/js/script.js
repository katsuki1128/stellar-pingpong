// static/js/script.js
let maxDistance = 1000 * 60 * 60 * 20; // 20時間をミリ秒に変換
let maxLeft = window.innerWidth * 0.8; // 80%の範囲で移動

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

        // const days = Math.floor(distance / (1000 * 60 * 60 * 24)).toString().padStart(2, '0');
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toString().padStart(2, '0');
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toString().padStart(2, '0');
        const seconds = Math.floor((distance % (1000 * 60)) / 1000).toString().padStart(2, '0');
        // const milliseconds = Math.floor(distance % 1000 / 10).toString().padStart(2, '0');  // ミリ秒の上2桁


        const countdownElement = document.getElementById(`countdown-${index}`);
        countdownElement.innerHTML = `${hours}:${minutes}:${seconds}`;

        // 移動範囲を設定 (例として、0から80%の範囲で移動)
        // const totalDistance = 1000 * 60 * 60 * 20; // 20時間をミリ秒に変換
        // const maxLeft = window.innerWidth * 0.8; // 80%の範囲で移動
        const leftPosition = Math.max(0, Math.min(maxLeft, maxLeft * (1 - distance / maxDistance)));
        // const rightPosition = Math.max(0, Math.min(maxLeft, maxLeft * (1 - distance / maxDistance)));

        const satelliteWrapper = document.getElementById(`satellite-wrapper-${index}`);
        satelliteWrapper.style.left = `${leftPosition}px`;
        // satelliteWrapper.style.right = `${rightPosition}px`;

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

const threshold = 15; // 閾値 (加速度の変化の大きさ)

const deviceMotionRequest = () => {
    if (typeof DeviceMotionEvent.requestPermission === 'function') {
        DeviceMotionEvent.requestPermission()
            .then(permissionState => {
                if (permissionState === 'granted') {
                    window.addEventListener("devicemotion", (event) => {
                        if (!event.accelerationIncludingGravity) {
                            alert('event.accelerationIncludingGravity is null');
                            return;
                        }
                        const x = event.accelerationIncludingGravity.x.toFixed(2);
                        const y = event.accelerationIncludingGravity.y.toFixed(2);
                        const z = event.accelerationIncludingGravity.z.toFixed(2);

                        const accelerationMagnitude = Math.sqrt(x * x + y * y + z * z);

                        if (accelerationMagnitude > threshold) {
                            document.getElementById('message').textContent = "⚫︎";
                            triggerBallAnimation();
                        } else {
                            document.getElementById('message').textContent = "";
                        }
                        document.getElementById('x').innerHTML = event.accelerationIncludingGravity.x.toFixed(2);
                        document.getElementById('y').innerHTML = event.accelerationIncludingGravity.y.toFixed(2);
                        document.getElementById('z').innerHTML = event.accelerationIncludingGravity.z.toFixed(2);
                    });
                }
            })
            .catch(console.error);
    } else {
        // alert('DeviceMotionEvent.requestPermission is not found');
        // if (!('ontouchstart' in window)) {
        console.log("ontouchstart")
        document.getElementById('triggerButton').style.display = 'block';
        // }
    }
};


let ballDirectionY = -1; // ボールのy方向の初期方向
let ballDirectionX = 1; // ボールのx方向の初期方向

const triggerBallAnimation = () => {
    const canvas = document.getElementById('animationCanvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const ctx = canvas.getContext('2d');
    const ball = { x: canvas.width / 2, y: canvas.height, radius: 10 };
    const satellites = document.querySelectorAll('.satellite-wrapper');
    let targetX = 0;

    satellites.forEach(satellite => {
        const rect = satellite.getBoundingClientRect();
        if (rect.right > targetX) {
            targetX = rect.right;
        }
    });

    let animationId;
    const drawBall = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        ctx.fillStyle = "#000";
        ctx.fill();
        ctx.closePath();
    };

    const animateBall = () => {
        ball.y += 5 * ballDirectionY;
        ball.x += 5 * ballDirectionX;

        // 衛星との衝突判定
        satellites.forEach(satellite => {
            const rect = satellite.getBoundingClientRect();
            const satelliteLeft = rect.left + window.scrollX;
            const satelliteRight = rect.right + window.scrollX;
            const satelliteTop = rect.top + window.scrollY;
            const satelliteBottom = rect.bottom + window.scrollY;
            if (ball.x > satelliteLeft && ball.x < satelliteRight && ball.y > satelliteTop && ball.y < satelliteBottom) {
                ballDirectionY *= -1; // ボールのy方向を逆にする
            }
        });

        // キャンバスの端に当たったら跳ね返る
        if (ball.y < 0 || ball.y > canvas.height) {
            ballDirectionY *= -1;
        }
        if (ball.x < 0 || ball.x > canvas.width) {
            ballDirectionX *= -1;
        }

        drawBall();
        animationId = requestAnimationFrame(animateBall);
    };

    ball.x = canvas.width / 2;
    ball.y = canvas.height;
    ballDirectionY = -1;
    ballDirectionX = 1;
    cancelAnimationFrame(animationId);
    animateBall();
};

// PCブラウザの場合はボール発射ボタンを表示

//     const startX = canvas.width / 2;
//     const startY = canvas.height;
//     const endX = targetX;
//     const endY = 0;
//     const duration = 1000;
//     const startTime = Date.now();

//     const animate = () => {
//         const currentTime = Date.now();
//         const elapsedTime = currentTime - startTime;
//         const t = Math.min(elapsedTime / duration, 1);

//         const x = startX + (endX - startX) * t;
//         const y = startY + (endY - startY) * t;

//         ctx.clearRect(0, 0, canvas.width, canvas.height);
//         ctx.beginPath();
//         ctx.arc(x, y, 10, 0, Math.PI * 2);
//         ctx.fillStyle = 'black';
//         ctx.fill();

//         if (t < 1) {
//             requestAnimationFrame(animate);
//         }
//     };

//     canvas.width = window.innerWidth;
//     canvas.height = window.innerHeight;
//     ctx.clearRect(0, 0, canvas.width, canvas.height);
//     animate();
// };

// const triggerBallAnimation = () => {
//     const ball = document.getElementById('ball');
//     const satellites = document.querySelectorAll('.satellite-wrapper');
//     let targetX = 0;

//     satellites.forEach(satellite => {
//         const rect = satellite.getBoundingClientRect();
//         if (rect.right > targetX) {
//             targetX = rect.right;
//         }
//     });

//     ball.style.display = 'block';
//     ball.style.transition = 'left 1s, top 1s';
//     ball.style.left = `${targetX}px`;
//     ball.style.top = '0';

//     setTimeout(() => {
//         ball.style.display = 'none';
//     }, 1000);
// };