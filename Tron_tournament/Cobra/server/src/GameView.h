/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** GameView (Tron neon 2.5D)
*/

#ifndef GAMEVIEW_H_
    #define GAMEVIEW_H_

    #include <QWidget>
    #include <QColor>
    #include "GameModel.h"

class GameView : public QWidget {
    Q_OBJECT
public:
    explicit GameView(QWidget* parent=nullptr) : QWidget(parent) {
        setMinimumSize(320, 240);
        setAutoFillBackground(true);
    }
    void setModel(GameModel* m){ model=m; }
protected:
    void paintEvent(QPaintEvent*) override;
private:
    GameModel* model=nullptr;
    QColor colorForId(int id) const;

    void drawBackground(QPainter& p);
    void drawScanlines(QPainter& p);
    void drawNeonCell(QPainter& p, const QRectF& r, const QColor& base, int glow=5);
    void drawNeonHead(QPainter& p, const QRectF& r, const QColor& base);
    void drawJetTrail(QPainter& p, const QRectF& headRect, GameModel const* m, const Player& pl,
        double cs, double ox, double oy);
    void drawOrthoGrid(QPainter& p, double ox, double oy, double cs, int W, int H);

    void drawPlayerNameList(QPainter& p);
};

#endif /* !GAMEVIEW_H_ */
