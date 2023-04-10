const renderer = new Renderer();

const acceleration = { x: 0, y: 0 };
const position = { x: renderer.canvas.width / 2, y: 0 };

const bunny = new Sprite("assets/lapinou.png", 100, 100)
const platform = new Sprite("assets/platform.png", 200, 30)

const nPlatforms = 4;

const platforms = []

var highest = 0;
var isDead = false;

const screenHeight = renderer.canvas.height;

var last_generation = -screenHeight * 2

const isOnPlatform = () => {
    for (i = 0; i < platforms.length; i++) {
        if (position.x + bunny.width > platforms[i].x && position.x < platforms[i].x + platform.width && position.y + bunny.height > platforms[i].y && position.y < platforms[i].y + platform.height) {
            return true;
        }
    }
    return false;
}
const randomPlatform = () => {
    if (platforms.length == 0)
        return renderer.canvas.width / 2;
    const old = platforms[platforms.length - 1].x;

    let newX;
    do {
        newX = Math.floor(Math.random() * (renderer.canvas.width - 400)) + 100; // 100 away from canvas edge
    } while (
        newX < old - 500 || newX > old + 500 || // 500 away from old platform
        newX < old + 100 && newX > old - 100 // 100 away from the edge of the old platform
    );

    return newX;
}

const handleInput = (events) => {
    if (Utils.isKeyDown(events, 'ArrowRight')) {
        acceleration.x = 10;
    } else if (Utils.isKeyDown(events, 'ArrowLeft')) {
        acceleration.x = -10;
    } else {
        acceleration.x -= acceleration.x / 10;
    }
}

const updatePosition = () => {
    position.x += acceleration.x;
    position.y += acceleration.y;
    if (position.y > 0) {
        acceleration.y -= 0.5;
    }
    if (isOnPlatform()) {
        acceleration.y = 20;
    }
}

const generatePlatformsIfNeeded = () => {
    if (position.y > highest) {
        highest = position.y;
    }
    while (highest >= last_generation + screenHeight) {
        for (i = 0; i < nPlatforms; i++) {
            platforms.push({ x: randomPlatform(), y: last_generation + screenHeight * 2 + i * (screenHeight / nPlatforms) });
        }
        last_generation += screenHeight;
    }
}

const render = () => {
    renderer.clear();
    renderer.drawText("Score: " + Math.floor(highest / 100), 30, 10, 30);
    for (i = 0; i < platforms.length; i++) {
        renderer.drawSprite(platform, platforms[i].x, platforms[i].y - position.y);
    }
    renderer.drawSprite(bunny, position.x, 0)
}

const checkDeath = () => {
    if (position.y < highest - renderer.canvas.height * 2) {
        isDead = true;
    }
}

const deadScreen = () => {
    renderer.drawText("You died", 70, renderer.canvas.width / 2 - 150, renderer.canvas.height / 2);
    renderer.drawText("Press <R> to restart", 30, renderer.canvas.width / 2 - 150, renderer.canvas.height / 2 + 50);
    if (Utils.isKeyDown(renderer.pollEvents(), 'r')) {
        isDead = false;
        position.x = renderer.canvas.width / 2;
        position.y = 0;
        acceleration.x = 0;
        acceleration.y = 0;
        highest = 0;
        platforms = [];
        last_generation = -screenHeight * 2;
    }
}

renderer.setBackgroundGradient("#0ea5e9", "#e0f2fe")

renderer.mainLoop(() => {
    if (isDead) {
        deadScreen();
        return;
    }
    const events = renderer.pollEvents();
    handleInput(events);
    updatePosition();
    checkDeath();
    generatePlatformsIfNeeded();
    render();
});