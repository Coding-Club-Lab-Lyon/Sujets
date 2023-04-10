const EVENTS = [];

class Renderer {
    constructor() {
        this.canvas = document.getElementById('canvas');
        this.context = this.canvas.getContext('2d');
        this.context.webkitImageSmoothingEnabled = false;
        this.context.mozImageSmoothingEnabled = false;
        this.context.imageSmoothingEnabled = false;
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight - 10;
    }

    setBackgroundColor(color) {
        this.canvas.style.backgroundColor = color;
    }

    setBackgroundGradient(color1, color2) {
        this.canvas.style.background = `linear-gradient(${color1}, ${color2})`;
    }

    clear() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    drawSprite(sprite, x, y) {
        this.context.drawImage(sprite.image, x, this.canvas.height / 2 - y - sprite.height, sprite.width, sprite.height);
    }

    drawText(text, size, x, y) {
        this.context.font = `${size}px Arial`;
        this.context.fillText(text, x, y);
    }

    pollEvents() {
        const events = [...EVENTS]
        EVENTS.length = 0;
        return events;
    }

    mainLoop(cb) {
        setInterval(cb, 10);
    }
}

class Sprite {
    constructor(url, width, height) {
        this.image = new Image();
        this.image.src = url;
        this.width = width;
        this.height = height;
    }
}

class Utils {
    static isKeyDown(events, key) {
        for (const event of events) {
            if (event.key === key) {
                return true;
            }
        }
        return false;
    }
}

document.addEventListener('keydown', (event) => {
    EVENTS.push(event);
});