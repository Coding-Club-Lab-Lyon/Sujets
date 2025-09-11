/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** GameModel
*/

#ifndef GAMEMODEL_H_
    #define GAMEMODEL_H_
    #include <vector>
    #include <array>
    #include <QObject>
    #include "Player.h"
    #include "AppConfig.h"

class GameModel : public QObject {
    Q_OBJECT
public:
    explicit GameModel(QObject* parent=nullptr);

    void configure(const AppConfig& cfg);
    void reset();
    void start();
    void stop();

    bool isRunning() const { return running; }
    int  getTick() const { return tick; }

    void onTick();
    void on3sStep();
    void setPlayerTurn(int id, int turn);
    const std::vector<uint8_t>& map() const { return grid; }
    int width() const { return W; }
    int height() const { return H; }
    const std::array<Player,8>& players() const { return pls; }
    int aliveCount() const;

    void onPlayerJoin(int id, const QString& name);
    void onPlayerLeave(int id);

signals:
    void stateChanged();
    void winnerDecided(int id);
    void playerDied(int id);

private:
    int W=64, H=48;
    std::vector<uint8_t> grid;
    std::array<Player,8> pls{};

    bool running=false;
    int tick=0;
    int lengthTick=125;
    int stepCounter = 0;
    std::array<int,8> stepsThisTick{{}};
    int totalStepsThisTick = 0;
    int prevStepCounter = 0;
    int mapsEvery=1;
    int tickrate=25;

    float startSpeed=0.025f;
    float endSpeed=0.25f;
    bool autoKill=true;
    int speedStep=0;

    int initialTrailLen = 3;
    int growRRIndex = 0;

    float currentSpeed() const;
    void placeSpawns();
    void clearGrid();
    void applyTurns();
    void advancePlayers();
    void markTrailAndShrinkOrGrow();
    void handleCollisions();
    Coord wrapNext(Coord p, Direction d) const;
};

#endif /* !GAMEMODEL_H_ */
