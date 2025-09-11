/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** GameServer
*/

#ifndef GAMESERVER_H_
    #define GAMESERVER_H_
    #include <QTcpServer>
    #include <QTcpSocket>
    #include <QHash>
    #include <QObject>
    #include "Protocol.h"
    #include "GameModel.h"
    #include "AppConfig.h"

struct ClientInfo {
    QTcpSocket* sock=nullptr;
    int playerId=0;       // 1..8
    QString name;
    QByteArray rxBuf;
    bool alive=false;
};

class GameServer : public QTcpServer {
    Q_OBJECT
public:
    explicit GameServer(QObject* parent=nullptr);
    bool startListen(quint16 port=5555); ///////////////////////////////////////////////////////////////////////////////////
    void stopListen();

    void setModel(GameModel* m){ model=m; }
    void setConfig(const AppConfig& cfg){ conf=cfg; }

    // networking
    void broadcastState();
    void sendWelcome(ClientInfo* c);
    void sendBye(ClientInfo* c, uint8_t reason);
    void sendWinner(int playerId);

    int connectedCount() const { return clients.size(); }
    void kickPlayer(int id);
signals:
    void playerJoined(int id, QString name);
    void playerLeft(int id);
    void logMsg(QString);

protected:
    void incomingConnection(qintptr handle) override;

private slots:
    void onReadyRead();
    void onDisconnected();

private:
    QHash<QTcpSocket*, ClientInfo*> clients;
    GameModel* model=nullptr;
    AppConfig conf;

    int assignFreePlayerId();
    void releasePlayerId(int id);
    bool readOneMessage(ClientInfo* c, QByteArray& out);
    void processPacket(ClientInfo* c, const QByteArray& pkt);
};

#endif /* !GAMESERVER_H_ */
