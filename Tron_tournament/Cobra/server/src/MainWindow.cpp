/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** MainWindow
*/


#include "MainWindow.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QWidget>
#include <QMessageBox>

MainWindow::MainWindow(const AppConfig& cfg, QWidget* parent)
    : QMainWindow(parent), conf(cfg)
{
    buildUi();
    model.configure(conf);
    model.reset();
    server.setModel(&model);
    server.setConfig(conf);
    loop.setup(&model, &server, conf);

    connect(&model, &GameModel::winnerDecided, this, &MainWindow::onWinner);
    connect(&server, &GameServer::playerJoined, this, &MainWindow::onPlayerJoined);
    connect(&server, &GameServer::playerLeft, this, &MainWindow::onPlayerLeft);
    connect(&model, &GameModel::playerDied, &server, &GameServer::kickPlayer);

    server.startListen(5555);
}


void MainWindow::buildUi()
{
    auto* cw = new QWidget; setCentralWidget(cw);
    auto* v = new QVBoxLayout(cw);

    statusLbl = new QLabel("Lobby: en attente de joueurs (max 8).");
    v->addWidget(statusLbl);

    stack = new QStackedWidget;
    v->addWidget(stack, 1);

    lobbyPage = new QWidget;
    auto* lv = new QVBoxLayout(lobbyPage);
    playerList = new QListWidget;
    lv->addWidget(playerList);
    auto* h = new QHBoxLayout;
    startBtn = new QPushButton("Start");
    resetBtn = new QPushButton("Reset");
    h->addWidget(startBtn);
    h->addWidget(resetBtn);
    lv->addLayout(h);
    stack->addWidget(lobbyPage);

    gameView = new GameView;
    gameView->setModel(&model);
    stack->addWidget(gameView);

    connect(startBtn, &QPushButton::clicked, this, &MainWindow::onStart);
    connect(resetBtn, &QPushButton::clicked, this, &MainWindow::onReset);

    connect(&model, &GameModel::stateChanged, this, [this](){
        if(model.isRunning()){
            gameView->update();
            statusLbl->setText(QString("Partie en cours — tick %1").arg(model.getTick()));
        } else {
            refreshLobby();
        }
    });

    stack->setCurrentWidget(lobbyPage);
    refreshLobby();
}

void MainWindow::refreshLobby()
{
    playerList->clear();
    int count=0;
    for(const auto& p: model.players()){
        if(p.alive){
            playerList->addItem(QString("#%1 %2").arg(p.id).arg(p.name));
            ++count;
        }
    }
    startBtn->setEnabled(count>=2 && !model.isRunning());
    resetBtn->setEnabled(!model.isRunning());
    if(!model.isRunning()){
        statusLbl->setText(QString("Lobby: %1 joueur(s) connecté(s).").arg(count));
    } else {
        statusLbl->setText(QString("Partie en cours — tick %1").arg(model.getTick()));
    }
}

void MainWindow::onStart()
{
    stack->setCurrentWidget(gameView);
    if(model.aliveCount()<2){
        QMessageBox::information(this, "Info", "Au moins 2 joueurs requis.");
        return;
    }
    model.start();
    loop.start();
    refreshLobby();
}

void MainWindow::onReset()
{
    stack->setCurrentWidget(lobbyPage);
    loop.stop();
    model.reset();
    server.stopListen();
    server.startListen(5555);
    refreshLobby();
}

void MainWindow::onWinner(int id)
{
    stack->setCurrentWidget(lobbyPage);
    loop.stop();
    QString msg;
    if(id>0){
        const auto& p = model.players()[id-1];
        msg = QString("Le gagnant est #%1 %2").arg(id).arg(p.name);
    } else {
        msg = "Égalité / aucun gagnant";
    }
    QMessageBox::information(this, "Fin de partie", msg);
    statusLbl->setText(msg + " — Cliquez Reset pour relancer.");
    startBtn->setEnabled(false);
    resetBtn->setEnabled(true);
}

void MainWindow::onPlayerJoined(int id, QString name)
{
    Q_UNUSED(name);
    refreshLobby();
}

void MainWindow::onPlayerLeft(int id)
{
    Q_UNUSED(id);
    refreshLobby();
}
