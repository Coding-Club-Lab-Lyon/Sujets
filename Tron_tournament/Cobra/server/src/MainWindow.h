
#pragma once
#include <QMainWindow>
#include <QListWidget>
#include <QPushButton>
#include <QLabel>
#include "GameModel.h"
#include "GameServer.h"
#include "TickLoop.h"
#include "AppConfig.h"
#include <QStackedWidget>
#include "GameView.h"

class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    explicit MainWindow(const AppConfig& cfg, QWidget* parent=nullptr);
private slots:
    void onStart();
    void onReset();
    void onWinner(int id);
    void onPlayerJoined(int id, QString name);
    void onPlayerLeft(int id);

private:
    AppConfig conf;
    GameModel model;
    GameServer server;
    TickLoop  loop;

    // Views
    QStackedWidget* stack=nullptr;
    QWidget* lobbyPage=nullptr;
    GameView* gameView=nullptr;

    // Lobby UI
    QListWidget* playerList=nullptr;
    QPushButton* startBtn=nullptr;
    QPushButton* resetBtn=nullptr;
    QLabel* statusLbl=nullptr;

    void buildUi();
    void refreshLobby();
};
