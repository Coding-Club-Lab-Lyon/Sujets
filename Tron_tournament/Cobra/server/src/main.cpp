/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** main
*/

#include <QApplication>
#include "MainWindow.h"
#include "AppConfig.h"
#include <QFile>
#include <QIODevice>

int main(int argc, char** argv)
{
    QApplication app(argc, argv);
    AppConfig cfg;
    applyOverridesFromArgs(cfg, app.arguments());
    cfg = loadConfigFromFile(cfg.confPath, cfg);
    applyOverridesFromArgs(cfg, app.arguments());

    // Charger le thème si présent
    QFile qss("neon.qss");
    if (qss.open(QIODevice::ReadOnly | QIODevice::Text)) {
        app.setStyleSheet(QString::fromUtf8(qss.readAll()));
    }

    MainWindow w(cfg);
    w.resize(480, 360);
    w.show();
    return app.exec();
}
