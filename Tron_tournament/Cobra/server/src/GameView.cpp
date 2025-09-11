/*
** EPITECH PROJECT, 2025
** Delivery
** File description:
** GameView
*/

#include <cmath>
#include "GameView.h"
#include <QPainter>
#include <QPainterPath>
#include <QLinearGradient>
#include <QRadialGradient>
#include <QPen>
#include <QFont>
#include <QFontMetrics>
#include <algorithm>

QColor GameView::colorForId(int id) const
{
    static const QColor lut[9] = {
        QColor(20,20,20),
        QColor("#ff2d55"),   // rouge néon
        QColor("#2bff88"),   // vert néon
        QColor("#ffe75a"),   // jaune néon
        QColor("#29a8ff"),   // bleu néon
        QColor("#ff8a33"),   // orange néon
        QColor("#b066ff"),   // violet néon
        QColor("#60ffff"),   // cyan néon
        QColor("#ff57ff"),   // magenta néon
    };
    if(id>=1 && id<=8) return lut[id];
    return QColor(50,50,50);
}

void GameView::paintEvent(QPaintEvent*)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing, true);
    p.setRenderHint(QPainter::TextAntialiasing, true);
    drawBackground(p);

    if (!model) { drawScanlines(p); return; }
    const int W = model->width();
    const int H = model->height();
    if (W<=0 || H<=0) { drawScanlines(p); return; }

    const auto& grid = model->map();
    const auto& players = model->players();

    const double cw = std::floor(width()  / double(W));
    const double ch = std::floor(height() / double(H));
    const double cs = std::max(1.0, std::floor(std::min(cw, ch)));
    const double ox = (width()  - cs*W) / 2.0;
    const double oy = (height() - cs*H) / 2.0;

    drawOrthoGrid(p, ox, oy, cs, W, H);

    for(int y = 0; y < H; ++y) {
        for(int x = 0; x < W; ++x) {
            uint8_t v = grid[y * W + x];
            if(v == 0) continue;
            QRectF r(ox + x * cs + 0.5, oy + y * cs + 0.5, cs - 1.0, cs - 1.0);
            drawNeonCell(p, r, colorForId((int)v), /*glow=*/4);
        }
    }

    struct JetInfo { QRectF r; const Player* pl; };
    QVector<JetInfo> jets;
    jets.reserve(8);

    for(const auto& pl : players) {
        if(!pl.alive) continue;
        QRectF r(ox + pl.pos.x * cs + 0.5, oy + pl.pos.y * cs + 0.5, cs - 1.0, cs - 1.0);
        drawNeonHead(p, r, colorForId(pl.id));
        jets.push_back({r, &pl});
    }

    p.save();
    p.setCompositionMode(QPainter::CompositionMode_Plus);
    for (const auto& j : jets) {
        drawJetTrail(p, j.r, model, *j.pl, cs, ox, oy);
    }
    p.restore();

    drawPlayerNameList(p);

    drawScanlines(p);
}

void GameView::drawBackground(QPainter& p)
{
    QRadialGradient g(rect().center(), std::max(width(), height()) * 0.85);
    g.setColorAt(0.0, QColor(5, 10, 18));
    g.setColorAt(1.0, QColor(0, 0, 0));
    p.fillRect(rect(), g);

    p.save();
    QPen framePen(QColor(0, 200, 255, 70));
    framePen.setWidth(2);
    p.setPen(framePen);
    p.drawRect(rect().adjusted(1,1,-2,-2));
    p.restore();
}

void GameView::drawOrthoGrid(QPainter& p, double ox, double oy, double cs, int W, int H)
{
    p.save();
    p.setRenderHint(QPainter::Antialiasing, false);

    const QColor lineCore(40,160,255,140);
    const QColor lineGlow(40,160,255,40);

    QPen pen(lineCore);
    pen.setWidthF(std::max(1.0, cs * 0.06));
    const double x0 = ox;
    const double y0 = oy;
    const double x1 = ox + cs * W;
    const double y1 = oy + cs * H;

    QPen glow(lineGlow);
    glow.setWidthF(std::max(1.0, cs * 0.22));
    p.setPen(glow);
    for (int x = 0; x <= W; ++x) {
        double xx = x0 + x * cs;
        p.drawLine(QPointF(xx, y0), QPointF(xx, y1));
    }
    for (int y = 0; y <= H; ++y) {
        double yy = y0 + y * cs;
        p.drawLine(QPointF(x0, yy), QPointF(x1, yy));
    }

    p.setPen(pen);
    for (int x = 0; x <= W; ++x) {
        double xx = x0 + x * cs;
        p.drawLine(QPointF(xx, y0), QPointF(xx, y1));
    }
    for (int y = 0; y <= H; ++y) {
        double yy = y0 + y * cs;
        p.drawLine(QPointF(x0, yy), QPointF(x1, yy));
    }

    p.restore();
}

void GameView::drawScanlines(QPainter& p)
{
    p.save();
    QPen pen(QColor(255,255,255,12));
    pen.setWidth(1);
    p.setPen(pen);
    for (int y = 0; y < height(); y += 3) {
        p.drawLine(0, y, width(), y);
    }
    p.restore();
}

void GameView::drawNeonCell(QPainter& p, const QRectF& r, const QColor& base, int glow)
{
    QColor c = base;
    for (int i = glow; i >= 1; --i) {
        QRectF ri = r.adjusted(-i, -i, i, i);
        c.setAlpha(18 + i*6);
        p.fillRect(ri, c);
    }
    QColor core = base.lighter(140);
    core.setAlpha(220);
    p.fillRect(r, core);
    QPen pen(base.lighter(160));
    pen.setWidthF(std::max(1.0, std::min(r.width(), r.height()) * 0.08));
    p.setPen(pen);
    p.drawRect(r);
}

void GameView::drawNeonHead(QPainter& p, const QRectF& r, const QColor& base)
{
    p.save();
    QPointF c = r.center();
    double rad = std::min(r.width(), r.height()) * 0.42;

    for (int i = 6; i >= 1; --i) {
        QRadialGradient gl(c, rad + i*2);
        QColor cc = base;
        cc.setAlpha(20 + i*12);
        gl.setColorAt(0.0, cc);
        QColor edge = base; edge.setAlpha(0);
        gl.setColorAt(1.0, edge);
        p.setBrush(gl);
        p.setPen(Qt::NoPen);
        p.drawEllipse(c, rad + i*2, rad + i*2);
    }

    QRadialGradient core(c, rad);
    core.setColorAt(0.0, base.lighter(180));
    core.setColorAt(0.8, base);
    core.setColorAt(1.0, QColor(255,255,255,40));
    p.setBrush(core);
    p.setPen(QPen(base.lighter(180), std::max(1.5, r.width()*0.1)));
    p.drawEllipse(c, rad, rad);

    QRadialGradient spec(c + QPointF(rad*0.25, -rad*0.25), rad*0.6);
    spec.setColorAt(0.0, QColor(255,255,255,160));
    spec.setColorAt(1.0, QColor(255,255,255,0));
    p.setBrush(spec);
    p.setPen(Qt::NoPen);
    p.drawEllipse(c + QPointF(rad*0.25, -rad*0.25), rad*0.35, rad*0.35);

    p.restore();
}

void GameView::drawJetTrail(QPainter& p, const QRectF& headRect, GameModel const* m, const Player& pl,
                            double cs, double ox, double oy)
{
    Q_UNUSED(m); Q_UNUSED(ox); Q_UNUSED(oy);
    p.save();

    QColor base = colorForId(pl.id);
    base.setAlpha(215);

    QPointF dir(0,0);
    switch (pl.dir) {
        case Up:    dir = QPointF(0, -1); break;
        case Down:  dir = QPointF(0,  1); break;
        case Left:  dir = QPointF(-1, 0); break;
        case Right: dir = QPointF( 1, 0); break;
        default: break;
    }

    QPointF back = -dir;
    double len  = cs * 2.2;
    double half = headRect.width()*0.34;

    QPointF c = headRect.center();
    QPointF tip  = c + back * (len*1.05);
    QPointF left = c + QPointF(-back.y(), back.x()) * half;
    QPointF right= c + QPointF(back.y(), -back.x()) * half;

    for (int i=3;i>=1;--i) {
        QLinearGradient g(c, tip);
        QColor a = base; a.setAlpha(70 + i*25);
        QColor b = base; b.setAlpha(0);
        g.setColorAt(0.0, a);
        g.setColorAt(1.0, b);

        QPainterPath path;
        double grow = i * 1.8;
        path.moveTo(left + QPointF(-grow, -grow));
        path.lineTo(right + QPointF(grow, grow));
        path.lineTo(tip  + back * (grow*0.8));
        path.closeSubpath();

        p.setBrush(g);
        p.setPen(Qt::NoPen);
        p.drawPath(path);
    }

    QLinearGradient inner(c, tip);
    QColor ia = base.lighter(200); ia.setAlpha(230);
    QColor ib = base.lighter(120); ib.setAlpha(0);
    inner.setColorAt(0.0, ia);
    inner.setColorAt(0.75, ib);
    inner.setColorAt(1.0, ib);

    QPainterPath core;
    core.moveTo(left);
    core.lineTo(right);
    core.lineTo(tip);
    core.closeSubpath();

    p.setBrush(inner);
    p.setPen(Qt::NoPen);
    p.drawPath(core);

    p.restore();
}

void GameView::drawPlayerNameList(QPainter& p)
{
    if (!model) return;

    const int pad = 12;
    int panelW = std::max(120, width() / 5);
    QRect panel(pad, pad, panelW, height() - pad*2);

    p.save();
    p.setRenderHint(QPainter::Antialiasing, true);

    QColor bg(0, 0, 0, 110);
    QColor border(0, 200, 255, 70);
    p.fillRect(panel, bg);
    p.setPen(QPen(border, 1.5));
    p.drawRoundedRect(panel.adjusted(0,0,-1,-1), 8, 8);

    QVector<const Player*> alive;
    alive.reserve(8);
    for (const auto& pl : model->players())
        if (pl.alive) alive.push_back(&pl);

    std::sort(alive.begin(), alive.end(),
              [](const Player* a, const Player* b){ return a->id < b->id; });

    int n = std::max(1, alive.size());
    int lineH = std::max(18, std::min(36, (panel.height() - pad * 2) / n));
    int px = std::clamp(lineH - 6, 12, 26);
    QFont f = font();
    f.setBold(true);
    f.setPixelSize(px);
    p.setFont(f);

    int y = panel.top() + pad + lineH - lineH/5;
    int xText = panel.left() + pad;

    for (const Player* pl : alive) {
        QColor c = colorForId(pl->id);
        QString label = QString("#%1  %2").arg(pl->id).arg(pl->name.isEmpty() ? "Player" : pl->name);

        p.setPen(Qt::NoPen);
        for (int r = 4; r >= 2; --r) {
            QColor halo = c; halo.setAlpha(28);
            QPainterPath path;
            path.addText(xText, y, f, label);
            p.save();
            p.translate(0.5, 0.5);
            p.setBrush(halo);
            p.drawPath(path);
            p.restore();
        }

        QPainterPath path;
        path.addText(xText, y, f, label);
        p.setBrush(Qt::NoBrush);
        p.setPen(QPen(QColor(0,0,0,160), 3.0));
        p.drawPath(path);

        p.setPen(c.lighter(130));
        p.drawText(QRect(xText, y - lineH + lineH/5, panel.width() - pad*2, lineH),
            Qt::AlignLeft | Qt::AlignVCenter,
            p.fontMetrics().elidedText(label, Qt::ElideRight, panel.width() - pad*2));

        y += lineH;
        if (y > panel.bottom() - pad)
            break;
    }

    p.restore();
}
