/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** Player
*/

#ifndef PLAYER_H_
    #define PLAYER_H_
    #include <QString>
    #include <deque>
    #include <cstdint>

struct Coord { int x=0, y=0; };

enum Direction : uint8_t { Up=0, Right=1, Down=2, Left=3 };

struct Player {
    int id = 0;              // 1..8
    QString name;
    bool alive = false;
    Coord pos;
    Direction dir = Right;
    float accum = 0.0f;
    std::deque<Coord> trail;
    int lastTurn = 0;        // -1/0/+1
};

#endif /* !PLAYER_H_ */
