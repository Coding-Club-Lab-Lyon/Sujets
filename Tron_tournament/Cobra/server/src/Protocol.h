/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** Protocol
*/

#ifndef PROTOCOL_H_
#define PROTOCOL_H_

#include <cstdint>

#pragma pack(push,1)
enum : uint16_t {
    MSG_HELLO = 0x0001, // C->S
    MSG_WELCOME = 0x0002, // S->C
    MSG_INPUT = 0x0003, // C->S
    MSG_STATE = 0x0004, // S->C
    MSG_PING = 0x0005, // S<->C (optionnel, non utilisé V1)
    MSG_BYE = 0x0006, // S->C
};

struct MsgHeader {
    uint16_t type; // voir ci-dessus
    uint16_t len; // longueur totale, header inclus
    uint16_t ver; // version protocole (1)
    uint16_t reserved;
};

struct HelloC2S {
    MsgHeader h;
    uint32_t want_player; // 0 = auto
    char name[32]; // UTF-8, non-null-terminated si plein
};

struct WelcomeS2C {
    MsgHeader h;
    uint32_t assigned_id; // 1..8
    uint16_t width, height;
    uint16_t tickrate;
    float start_speed;
    float end_speed;
    uint8_t auto_kill; // 0/1
    uint16_t length_tick;
    uint16_t maps_every;
};

struct InputC2S {
    MsgHeader h;
    int8_t turn; // -1,0,+1
    uint32_t tick; // optionnel (0 si non utilisé)
};

struct PlayerState {
    uint8_t id;
    uint16_t x, y;
    uint8_t dir; // 0:Up 1:Right 2:Down 3:Left
    uint8_t alive; // 0/1
};

struct StateS2C {
    MsgHeader h;
    uint32_t tick;
    uint16_t width, height;
    uint8_t player_count;
    // payload : map[width*height] (uint8_t)
    // puis player_count * PlayerState
};

struct ByeS2C {
    MsgHeader h;
    uint8_t reason; // 0=server closing,1=dead,2=winner,3=kick
};
#pragma pack(pop)

static_assert(sizeof(MsgHeader)==8, "MsgHeader should be 8 bytes");

#endif /* !PROTOCOL_H_ */
