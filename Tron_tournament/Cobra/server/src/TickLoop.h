/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** TickLoop
*/

#ifndef TICKLOOP_H_
    #define TICKLOOP_H_

    #include <QObject>
    #include <QTimer>
    #include "GameModel.h"
    #include "GameServer.h"
    #include "AppConfig.h"

class TickLoop : public QObject {
    Q_OBJECT
public:
    explicit TickLoop(QObject* parent=nullptr);
    void setup(GameModel* model, GameServer* server, const AppConfig& cfg);
    void start();
    void stop();

private slots:
    void onTick();

private:
    QTimer tickTimer;
    QTimer step3s;
    GameModel* model=nullptr;
    GameServer* server=nullptr;
    AppConfig conf;
    int tickCounter=0;
};

#endif /* !TICKLOOP_H_ */
