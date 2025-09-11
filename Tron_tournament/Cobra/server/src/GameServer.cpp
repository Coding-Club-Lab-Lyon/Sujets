/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** GameServer
*/

#include "GameServer.h"
#include <QDataStream>
#include <QHostAddress>
#include <algorithm>

static QString safeName(const char* name, int maxLen)
{
    QByteArray ba(name, maxLen);
    int nul = ba.indexOf('\0');
    if (nul>=0) ba.truncate(nul);
    QString s = QString::fromUtf8(ba);
    if(s.isEmpty())
        s = "Player";
    return s.left(32);
}

GameServer::GameServer(QObject* parent):QTcpServer(parent)
{

}

bool GameServer::startListen(quint16 port)
{
    if(!listen(QHostAddress::Any, port)){
        emit logMsg(QString("Listen failed on %1").arg(port));
        return false;
    }
    emit logMsg(QString("Listening on %1").arg(serverPort()));
    return true;
}

void GameServer::stopListen()
{
    close();
    for(auto c: clients.values()){
        sendBye(c, 0);
        c->sock->disconnectFromHost();
        c->sock->deleteLater();
        delete c;
    }
    clients.clear();
}

void GameServer::incomingConnection(qintptr handle)
{
    if(clients.size() >= 8) {
        QTcpSocket* s = new QTcpSocket(this);
        s->setSocketDescriptor(handle);
        s->disconnectFromHost();
        s->deleteLater();
        return;
    }
    QTcpSocket* s = new QTcpSocket(this);
    s->setSocketDescriptor(handle);
    auto* ci = new ClientInfo();
    ci->sock = s;
    clients.insert(s, ci);
    connect(s, &QTcpSocket::readyRead, this, &GameServer::onReadyRead);
    connect(s, &QTcpSocket::disconnected, this, &GameServer::onDisconnected);
    emit logMsg("Client connected");
}

void GameServer::onDisconnected()
{
    auto* s = qobject_cast<QTcpSocket*>(sender());
    if(!s) return;
    auto it = clients.find(s);
    if(it==clients.end()) return;
    auto* ci = it.value();
    if(ci->playerId){
        emit playerLeft(ci->playerId);
        releasePlayerId(ci->playerId);
    }
    clients.erase(it);
    if (model && ci->playerId) model->onPlayerLeave(ci->playerId);
    s->deleteLater();
    delete ci;
    emit logMsg("Client disconnected");
}

int GameServer::assignFreePlayerId()
{
    bool used[9]={false};
    for(auto c:clients.values()) {
        if(c->playerId >= 1 && c->playerId <= 8) used[c->playerId]=true;
    }
    for(int i = 1; i <= 8; ++i)
        if(!used[i])
            return i;
    return 0;
}

void GameServer::releasePlayerId(int)
{

}

void GameServer::onReadyRead()
{
    auto* s = qobject_cast<QTcpSocket*>(sender());
    if(!s) return;
    auto* ci = clients.value(s, nullptr);
    if(!ci) return;
    ci->rxBuf.append(s->readAll());

    QByteArray pkt;
    while (readOneMessage(ci, pkt)) {
        processPacket(ci, pkt);
    }
}

bool GameServer::readOneMessage(ClientInfo* c, QByteArray& out)
{
    if(c->rxBuf.size() < (int)sizeof(MsgHeader)) return false;
    MsgHeader h;
    memcpy(&h, c->rxBuf.constData(), sizeof(MsgHeader));
    if(c->rxBuf.size() < h.len) return false;
    out = c->rxBuf.left(h.len);
    c->rxBuf.remove(0, h.len);
    return true;
}

void GameServer::processPacket(ClientInfo* c, const QByteArray& pkt)
{
    if (pkt.size() < (int)sizeof(MsgHeader)) return;
    MsgHeader h; memcpy(&h, pkt.constData(), sizeof(MsgHeader));

    switch (h.type) {
    case MSG_HELLO: {
        if ((int)pkt.size() < (int)sizeof(HelloC2S)) return;
        HelloC2S hello; memcpy(&hello, pkt.constData(), sizeof(HelloC2S));

        int pid = assignFreePlayerId();
        if (pid == 0) { sendBye(c,3); c->sock->disconnectFromHost(); return; }

        c->playerId = pid;
        c->name = safeName(hello.name, 32);

        if (model) {
            model->onPlayerJoin(pid, c->name);
        }

        emit playerJoined(pid, c->name);
        sendWelcome(c);
        break;
    }
    case MSG_INPUT: {
        if ((int)pkt.size() < (int)sizeof(InputC2S)) return;
        if (!c->playerId || !model) return;
        InputC2S in; memcpy(&in, pkt.constData(), sizeof(InputC2S));
        int t = std::clamp((int)in.turn, -1, +1);
        model->setPlayerTurn(c->playerId, t);
        break;
    }
    default: break;
    }
}

void GameServer::sendWelcome(ClientInfo* c)
{
    if(!model) return;
    WelcomeS2C w{};
    w.h.type = MSG_WELCOME;
    w.h.ver = 1;
    w.assigned_id = c->playerId;
    w.width = model->width();
    w.height= model->height();
    w.tickrate = (uint16_t)conf.tickrate;
    w.start_speed = conf.start_speed;
    w.end_speed = conf.end_speed;
    w.auto_kill = conf.auto_kill ? 1:0;
    w.length_tick= (uint16_t)conf.length_tick;
    w.maps_every = (uint16_t)conf.maps_every;
    w.h.len = sizeof(WelcomeS2C);
    c->sock->write(reinterpret_cast<const char*>(&w), sizeof(w));
}

void GameServer::sendBye(ClientInfo* c, uint8_t reason)
{
    ByeS2C b{};
    b.h.type=MSG_BYE; b.h.ver=1;
    b.h.len=sizeof(b);
    b.reason = reason;
    if(c && c->sock)
        c->sock->write(reinterpret_cast<const char*>(&b), sizeof(b));
}

void GameServer::broadcastState()
{
    if(!model)
        return;
    const auto& base = model->map();
    uint16_t W = (uint16_t)model->width();
    uint16_t H = (uint16_t)model->height();

    std::vector<uint8_t> grid(base.begin(), base.end());
    for(const auto& p : model->players()){
        if(!p.alive) continue;
        if(p.pos.x >= 0 && p.pos.x<W && p.pos.y >= 0 && p.pos.y < H){
            grid[p.pos.y * W + p.pos.x] = (uint8_t)p.id;
        }
    }

    uint8_t P = 0;
    for(const auto& p:model->players()) if(p.alive) ++P;

    StateS2C s{};
    s.h.type = MSG_STATE; s.h.ver=1;
    s.tick = (uint32_t)model->getTick();
    s.width=W; s.height=H; s.player_count=P;
    s.h.len = sizeof(StateS2C) + grid.size() + P*sizeof(PlayerState);

    QByteArray buf;
    buf.resize(s.h.len);
    memcpy(buf.data(), &s, sizeof(StateS2C));
    memcpy(buf.data()+sizeof(StateS2C), grid.data(), grid.size());
    int off = sizeof(StateS2C) + grid.size();

    for(const auto& p:model->players()){
        if(!p.alive) continue;
        PlayerState ps{};
        ps.id = (uint8_t)p.id;
        ps.x = (uint16_t)p.pos.x; ps.y=(uint16_t)p.pos.y;
        ps.dir = (uint8_t)p.dir;
        ps.alive = p.alive?1:0;
        memcpy(buf.data()+off, &ps, sizeof(PlayerState));
        off += sizeof(PlayerState);
    }

    for(auto c: clients.values()){
        if(c->sock && c->sock->state()==QAbstractSocket::ConnectedState){
            c->sock->write(buf);
        }
    }
}

void GameServer::sendWinner(int playerId){
    for(auto c: clients.values()){
        if(!c->sock) continue;
        ByeS2C b{};
        b.h.type=MSG_BYE; b.h.ver=1; b.h.len=sizeof(b);
        b.reason = 2;
        c->sock->write(reinterpret_cast<const char*>(&b), sizeof(b));
    }
}

void GameServer::kickPlayer(int id) {
    for (auto it = clients.begin(); it != clients.end(); ) {
        ClientInfo* c = it.value();
        if (c->playerId == id) {
            sendBye(c, 1); // 1 = mort
            c->sock->disconnectFromHost();
            c->sock->deleteLater();
            delete c;
            it = clients.erase(it);
        } else {
            ++it;
        }
    }
}
