/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** TickLoop
*/

#include "TickLoop.h"

TickLoop::TickLoop(QObject* parent):QObject(parent)
{

}

void TickLoop::setup(GameModel* m, GameServer* s, const AppConfig& cfg)
{
    model = m; server = s; conf = cfg;
    int intervalMs = 1000 / (conf.tickrate > 0 ?conf.tickrate:25);
    tickTimer.setInterval(intervalMs);
    step3s.setInterval(3000);
    connect(&tickTimer, &QTimer::timeout, this, &TickLoop::onTick);
    connect(&step3s, &QTimer::timeout, [this](){
        if(model) model->on3sStep();
    });
}

void TickLoop::start()
{
    tickCounter=0;
    tickTimer.start();
    step3s.start();
}

void TickLoop::stop()
{
    tickTimer.stop();
    step3s.stop();
}

void TickLoop::onTick()
{
    if(model){
        model->onTick();
        if(server && (model->getTick() % conf.maps_every == 0)){
            server->broadcastState();
        }
    }
}
