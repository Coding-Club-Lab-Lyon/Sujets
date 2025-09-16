/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** AppConfig
*/

#include "AppConfig.h"
#include <QFile>
#include <QTextStream>
#include <QStringList>
#include <QDebug>

static bool toBoolOnOff(const QString& v)
{
    auto s = v.trimmed().toLower();
    return (s=="on" || s=="1" || s=="true" || s=="y" || s=="yes");
}

AppConfig loadConfigFromFile(const QString& path, const AppConfig& defaults)
{
    AppConfig c = defaults;
    QFile f(path);
    if (!f.open(QIODevice::ReadOnly | QIODevice::Text))
        return c;
    QTextStream in(&f);
    while (!in.atEnd()) {
        QString line = in.readLine().trimmed();
        if (line.isEmpty() || line.startsWith('#')) continue;
        auto parts = line.split(':');
        if (parts.size() < 2) continue;
        QString k = parts[0].trimmed().toLower();
        QString v = parts[1].trimmed();
        if (k=="tickrate") c.tickrate = v.toInt();
        else if (k=="start speed") c.start_speed = v.toFloat();
        else if (k=="end speed") c.end_speed = v.toFloat();
        else if (k=="auto kill") c.auto_kill = toBoolOnOff(v);
        else if (k=="lenght") c.length_tick = v.toInt();
        else if (k=="maps") c.maps_every = v.toInt();
    }
    return c;
}

void applyOverridesFromArgs(AppConfig& cfg, const QStringList& args)
{
    for (int i=1; i<args.size(); ++i) {
        const QString& a = args[i];
        if (a == "-d" && i+1 < args.size()) {
            cfg.debug = toBoolOnOff(args[i+1]); ++i;
        } else if (a == "-f" && i+1 < args.size()) {
            cfg.confPath = args[i+1]; ++i;
        } else if (a == "-s" && i+2 < args.size()) {
            cfg.width  = args[i+1].toInt();
            cfg.height = args[i+2].toInt();
            i += 2;
        }
    }
}
