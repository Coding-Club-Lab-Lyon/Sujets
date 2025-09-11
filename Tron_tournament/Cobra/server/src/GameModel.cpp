/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** GameModel
*/

#include "GameModel.h"
#include <QtMath>
#include <algorithm>

static inline int idx(int x,int y,int W)
{
    return y*W + x;
}

GameModel::GameModel(QObject* parent):QObject(parent)
{

}

void GameModel::configure(const AppConfig& cfg)
{
    tickrate = cfg.tickrate;
    startSpeed = cfg.start_speed;
    endSpeed = cfg.end_speed;
    autoKill = cfg.auto_kill;
    lengthTick = cfg.length_tick;
    mapsEvery = cfg.maps_every;
    W = cfg.width;
    H = cfg.height;
    grid.assign(W * H, 0);
}

void GameModel::reset()
{
    stop();
    tick = 0;
    speedStep = 0;
    stepCounter = 0;
    stepsThisTick.fill(0);
    totalStepsThisTick = 0;
    prevStepCounter = 0;
    growRRIndex = 0;
    clearGrid();
    for (int i=0; i < 8; ++i) {
        pls[i] = Player{};
        pls[i].id = i + 1;
        pls[i].alive = false;
    }
    placeSpawns();
    emit stateChanged();
}

void GameModel::start()
{
    running=true;
}

void GameModel::stop()
{
    running=false;
}

int GameModel::aliveCount() const
{
    int c = 0;
    
    for(auto& p:pls) if(p.alive) ++c;
    return c;
}

float GameModel::currentSpeed() const
{
    float t = (float)speedStep / 100.0f;
    return startSpeed + (endSpeed - startSpeed) * t;
}

void GameModel::on3sStep()
{
    if (speedStep < 100)
        ++speedStep;
}

void GameModel::onTick()
{
    if(!running)
        return;
    ++tick;
    stepsThisTick.fill(0);
    totalStepsThisTick = 0;
    prevStepCounter = stepCounter;
    applyTurns();
    advancePlayers();
    handleCollisions();
    markTrailAndShrinkOrGrow();

    if (aliveCount() <= 1) {
        int winnerId = 0;
        for(auto& p:pls) if(p.alive) {
            winnerId = p.id; break;
        }
        stop();
        emit stateChanged();
        emit winnerDecided(winnerId);
        return;
    }
    emit stateChanged();
}

void GameModel::setPlayerTurn(int id, int turn)
{
    if (id < 1 || id > 8)
        return;
    pls[id - 1].lastTurn = (turn < 0 ? - 1: (turn > 0 ? + 1 : 0));
}

void GameModel::clearGrid()
{
    std::fill(grid.begin(), grid.end(), 0);
}

void GameModel::placeSpawns()
{
    float cx = (W - 1) / 2.0f; 
    float cy = (H - 1) / 2.0f;
    float radius = std::min(W, H)/2.0f - 2.0f;
    for (int i = 0; i < 8; ++i) {
        float ang = (2 * M_PI * i) / 8;
        int sx = (int)qRound(cx + radius * qCos(ang));
        int sy = (int)qRound(cy + radius * qSin(ang));
        auto& p = pls[i];
        p.pos = { sx, sy };
        int dx = (cx > sx) ? 1 : (cx < sx ? -1 : 0);
        int dy = (cy > sy) ? 1 : (cy < sy ? -1 : 0);
        p.dir = (qAbs(cx - sx) >= qAbs(cy - sy)) ? (dx>0?Right:Left) : (dy>0?Down:Up);
        p.alive = false;
        p.trail.clear();
        p.accum = 0.0f; p.lastTurn=0;
    }
}

void GameModel::applyTurns(){
    for(auto& p:pls){
        if (!p.alive)
            continue;
        int t = p.lastTurn;
        if (t==0)
            continue;
        // -1 = gauche, +1 = droite
        int d = (int)p.dir;
        if (t == -1)
            d = (d+3)%4;
        else if(t == +1)
            d = (d+1)%4;
        p.dir = (Direction)d;
        p.lastTurn = 0;
    }
}

Coord GameModel::wrapNext(Coord pos, Direction d) const
{
    switch(d){
        case Up: pos.y = (pos.y-1 + H)%H;
            break;
        case Down: pos.y = (pos.y+1)%H;
            break;
        case Left: pos.x = (pos.x-1 + W)%W;
            break;
        case Right: pos.x = (pos.x+1)%W;
            break;
    }
    return pos;
}

void GameModel::advancePlayers()
{
    float spd = currentSpeed();

    for(int i=0;i<8;++i){
        auto& p = pls[i];
        if(!p.alive) continue;

        p.accum += spd / (float)tickrate;

        while(p.accum >= 1.0f){
            Coord next = wrapNext(p.pos, p.dir);
            p.trail.push_back(p.pos);
            p.pos = next;
            p.accum -= 1.0f;

            stepsThisTick[i]++;
            totalStepsThisTick++;
            stepCounter++;
        }
    }
}

void GameModel::handleCollisions()
{
    std::vector<int> headCount(W * H, 0);
    for(auto& p:pls) {
        if(!p.alive)
            continue;
        int idc = idx(p.pos.x, p.pos.y, W);
        headCount[idc]++;
    }

    for(auto& p:pls) {
        if(!p.alive)
            continue;
        int idc = idx(p.pos.x, p.pos.y, W);
        bool collide = false;
        if(headCount[idc] > 1) collide = true;
        if(!collide) {
            uint8_t cell = grid[idc];
            if(cell!=0) {
                if(cell==p.id && !autoKill) {
                } else {
                    collide = true;
                }
            }
        }
        if(collide) {
            p.alive=false;
            emit playerDied(p.id);
        }
    }
}

void GameModel::markTrailAndShrinkOrGrow()
{
    for(auto& p:pls) {
        if(!p.alive)
            continue;
        for(const auto& c : p.trail) {
            grid[idx(c.x,c.y,W)] = (uint8_t)p.id;
        }
    }

    int growEvents = 0;
    if(totalStepsThisTick > 0) {
        for(int k = prevStepCounter + 1; k <= stepCounter; ++k) {
            if(k % lengthTick == 0)
                ++growEvents;
        }
    }

    std::array<int,8> pops{};
    for(int i = 0; i < 8; ++i)
        pops[i] = stepsThisTick[i];

    int remainingGrows = growEvents;
    int idxRR = growRRIndex;

    for(int count=0; count<8 && remainingGrows>0; ++count) {
        int i = (idxRR + count) % 8;
        if(pops[i] > 0) {
            pops[i] -= 1;
            --remainingGrows;
            growRRIndex = (i+1)%8;
        }
    }
    int guard = 32;
    while(remainingGrows > 0 && guard-- > 0) {
        for(int count=0; count < 8 && remainingGrows > 0; ++count) {
            int i = (idxRR + count) % 8;
            if(pops[i] > 0) {
                pops[i] -= 1;
                --remainingGrows;
                growRRIndex = (i + 1) % 8;
            }
        }
    }
    for(int i=0;i<8;++i) {
        auto& p = pls[i];

        if(!p.alive)
            continue;
        int toPop = pops[i];
        while(toPop-- > 0 && !p.trail.empty()) {
            Coord tail = p.trail.front(); p.trail.pop_front();
            int idc = idx(tail.x, tail.y, W);
            if(grid[idc] == (uint8_t)p.id) grid[idc] = 0;
        }
    }
}

void GameModel::onPlayerJoin(int id, const QString& name)
{
    if(id < 1 || id > 8)
        return;
    auto& p = pls[id - 1];
    p.name = name;
    p.alive = true;
    p.accum = 0.0f;
    p.lastTurn = 0;

    Direction backDir = (p.dir==Up?Down : p.dir==Down?Up : p.dir==Left?Right : Left);
    Coord c = p.pos;
    for (int k=0; k<initialTrailLen; ++k) {
        switch(backDir) {
            case Up: c.y = (c.y - 1 + H) % H; break;
            case Down: c.y = (c.y + 1) % H; break;
            case Left: c.x = (c.x - 1 + W)% W; break;
            case Right: c.x = (c.x + 1)% W; break;
        }
        p.trail.push_back(c);
        grid[idx(c.x,c.y,W)] = (uint8_t)p.id;
    }

    emit stateChanged();
}

void GameModel::onPlayerLeave(int id)
{
    if(id < 1 || id > 8)
        return;
    auto& p = pls[id - 1];
    for(const auto& c : p.trail)
    {
        int k = idx(c.x ,c.y, W);
        if(grid[k] == (uint8_t)p.id) grid[k] = 0;
    }
    p.trail.clear();
    p.alive = false;
    emit stateChanged();
}
