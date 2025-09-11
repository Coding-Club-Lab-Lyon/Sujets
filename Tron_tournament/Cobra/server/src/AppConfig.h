/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** AppConfig
*/

#ifndef APPCONFIG_H_
    #define APPCONFIG_H_
    #include <QString>

struct AppConfig {
    int tickrate = 25;
    float start_speed = 0.025f;
    float end_speed   = 0.25f;
    bool auto_kill = true;
    int length_tick = 125;
    int maps_every = 1;
    int width = 64;
    int height = 48;
    bool debug = false;
    QString confPath = "game.conf";
};

AppConfig loadConfigFromFile(const QString& path, const AppConfig& defaults);
void applyOverridesFromArgs(AppConfig& cfg, const QStringList& args);

#endif /* !APPCONFIG_H_ */
