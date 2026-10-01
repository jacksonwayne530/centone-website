"""Isometric SVG helpers for the Built to Last case-study drawings.

World coordinates are in feet: x runs along the street (screen right-down), y runs back to front
(screen left-down), z is up. The viewer looks from +x,+y,+z, so the visible faces of a box are its
top, its y = y1 face ("left face", the street front), and its x = x1 face ("right face").
Shapes are drawn in call order (painter's algorithm): back and low things first.
"""
import math

C = math.cos(math.radians(30))
S = 0.5

INK = '#2a2420'


def f(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


class Canvas:
    def __init__(self, k=3.2):
        self.k = k
        self.out = []
        self.minx = self.miny = 1e9
        self.maxx = self.maxy = -1e9

    def p(self, x, y, z):
        sx = (x - y) * C * self.k
        sy = ((x + y) * S - z) * self.k
        self.minx = min(self.minx, sx)
        self.maxx = max(self.maxx, sx)
        self.miny = min(self.miny, sy)
        self.maxy = max(self.maxy, sy)
        return sx, sy

    def raw(self, s):
        self.out.append(s)

    def poly(self, pts, fill, stroke=INK, sw=1.0, opacity=None, join='round'):
        d = ' '.join(f'{f(a)},{f(b)}' for a, b in (self.p(*q) for q in pts))
        op = f' fill-opacity="{opacity}"' if opacity is not None else ''
        st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="{join}"' if stroke else ''
        self.out.append(f'<polygon points="{d}" fill="{fill}"{op}{st}/>')

    def line(self, a, b, stroke=INK, sw=1.0, dash=None, cap='round'):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        style = f'fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{da}'
        seg = f'M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}'
        # Consecutive lines with the same style share one <path>.
        if self.out and isinstance(self.out[-1], list) and self.out[-1][0] == style:
            self.out[-1][1].append(seg)
        else:
            self.out.append([style, [seg]])

    def circle_at(self, pt, r_ft, fill, stroke=INK, sw=1.0):
        x, y = self.p(*pt)
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        self.out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r_ft * self.k)}" fill="{fill}"{st}/>')

    def circle_px(self, x, y, r, fill, stroke=INK, sw=1.0):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        self.out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}"{st}/>')

    # ---- boxes and faces ----

    def box(self, x0, y0, z0, x1, y1, z1, top, left, right, stroke=INK, sw=1.0, faces='tlr'):
        if 'l' in faces:
            self.poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], left, stroke, sw)
        if 'r' in faces:
            self.poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], right, stroke, sw)
        if 't' in faces:
            self.poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, stroke, sw)

    def svg(self, pad=24, bg=None, extra_defs=''):
        w = self.maxx - self.minx + 2 * pad
        h = self.maxy - self.miny + 2 * pad
        vb = f'{f(self.minx - pad)} {f(self.miny - pad)} {f(w)} {f(h)}'
        bgrect = f'<rect x="{f(self.minx - pad)}" y="{f(self.miny - pad)}" width="{f(w)}" height="{f(h)}" fill="{bg}"/>' if bg else ''
        body = '\n'.join(o if isinstance(o, str) else f'<path d="{"".join(o[1])}" {o[0]}/>' for o in self.out)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{f(w)}" height="{f(h)}" '
            f'font-family="Inter, system-ui, sans-serif">{extra_defs}{bgrect}\n{body}\n</svg>\n'
        )


class Face:
    """Maps 2D (u, v) on a box face to 3D. u runs left to right on screen, v runs up."""

    def __init__(self, cv, kind, x0, y0, z0, x1, y1, z1):
        self.cv, self.kind = cv, kind
        self.x0, self.y0, self.z0, self.x1, self.y1, self.z1 = x0, y0, z0, x1, y1, z1
        self.w = (x1 - x0) if kind == 'left' else (y1 - y0)
        self.h = z1 - z0

    def at(self, u, v, out=0.0):
        """`out` pushes the point off the face toward the viewer (positive) or into it (negative)."""
        if self.kind == 'left':
            return (self.x0 + u, self.y1 + out, self.z0 + v)
        return (self.x1 + out, self.y1 - u, self.z0 + v)

    def rect(self, u0, v0, u1, v1, fill, stroke=INK, sw=1.0, out=0.0):
        self.cv.poly([self.at(u0, v0, out), self.at(u1, v0, out), self.at(u1, v1, out), self.at(u0, v1, out)], fill, stroke, sw)

    def hline(self, v, u0=0, u1=None, stroke=INK, sw=0.6, out=0.0):
        u1 = self.w if u1 is None else u1
        self.cv.line(self.at(u0, v, out), self.at(u1, v, out), stroke, sw)

    def vline(self, u, v0=0, v1=None, stroke=INK, sw=0.6, out=0.0):
        v1 = self.h if v1 is None else v1
        self.cv.line(self.at(u, v0, out), self.at(u, v1, out), stroke, sw)

    def coursing(self, row, unit, stroke, sw=0.5, v0=0, v1=None, u0=0, u1=None):
        """Running-bond joints: horizontal lines every `row`, vertical joints every `unit`, staggered."""
        v1 = self.h if v1 is None else v1
        u1 = self.w if u1 is None else u1
        v = v0
        i = 0
        while v < v1 - 1e-6:
            top = min(v + row, v1)
            if v > v0:
                self.hline(v, u0, u1, stroke, sw)
            u = u0 + (unit / 2 if i % 2 else unit)
            while u < u1 - 0.3:
                self.vline(u, v, top, stroke, sw)
                u += unit
            v += row
            i += 1

    def window(self, u0, v0, u1, v1, glass, frame=INK, mullions=(), transom=None, reveal='#00000033', sw=0.9):
        """A recessed window: glass, a shadow along the head and one jamb, and mullions."""
        self.rect(u0, v0, u1, v1, glass, frame, sw)
        d = min(0.7, (v1 - v0) * 0.12)
        # Shadow cast by the head and the left jamb (light comes from the upper left).
        self.cv.poly([self.at(u0, v1), self.at(u1, v1), self.at(u1, v1 - d), self.at(u0 + d, v1 - d), self.at(u0 + d, v0), self.at(u0, v0)], reveal, None)
        for m in mullions:
            self.vline(m, v0, v1, frame, 0.8)
        if transom is not None:
            self.hline(transom, u0, u1, frame, 0.8)
        # Glint.
        self.cv.line(self.at(u0 + (u1 - u0) * 0.62, v0 + (v1 - v0) * 0.3), self.at(u0 + (u1 - u0) * 0.8, v0 + (v1 - v0) * 0.62), '#ffffff', 0.9)


def tree(cv, x, y, z, h=24, r=7.5, trunk='#6b4a33', dark='#4f7a3e', mid='#6b9a4f', light='#8fbd68'):
    """A rounded, cloud-like street tree like the ones on the homepage drawings."""
    cv.line((x, y, z), (x, y, z + h * 0.62), INK, 3.4 * cv.k / 3.2)
    cv.line((x, y, z), (x, y, z + h * 0.62), trunk, 2.0 * cv.k / 3.2)
    cx, cy = cv.p(x, y, z + h * 0.7)
    k = cv.k
    blobs = [(-0.55, 0.15, 0.55), (0.55, 0.2, 0.55), (0, 0.35, 0.6), (-0.3, -0.35, 0.55), (0.35, -0.3, 0.55), (0, -0.55, 0.5)]
    for dx, dy, rr in blobs:
        cv.circle_px(cx + dx * r * k, cy + dy * r * k, rr * r * k, dark, INK, 1.0)
    for dx, dy, rr in [(-0.3, -0.05, 0.42), (0.3, -0.05, 0.42), (0, -0.4, 0.38)]:
        cv.circle_px(cx + dx * r * k, cy + dy * r * k, rr * r * k, mid, None)
    for dx, dy, rr in [(-0.35, -0.35, 0.18), (0.1, -0.6, 0.15), (0.4, -0.25, 0.14)]:
        cv.circle_px(cx + dx * r * k, cy + dy * r * k, rr * r * k, light, None)


def shrub(cv, x, y, z, r=2.2, dark='#4f7a3e', light='#7fae5c', flowers=None):
    cx, cy = cv.p(x, y, z + r * 0.6)
    k = cv.k
    for dx, dy, rr in [(-0.6, 0.1, 0.7), (0.6, 0.1, 0.7), (0, -0.3, 0.8)]:
        cv.circle_px(cx + dx * r * k, cy + dy * r * k, rr * r * k, dark, INK, 0.8)
    cv.circle_px(cx - 0.15 * r * k, cy - 0.45 * r * k, 0.35 * r * k, light, None)
    if flowers:
        for dx, dy in [(-0.5, -0.1), (0.4, -0.35), (0.1, 0.15)]:
            cv.circle_px(cx + dx * r * k, cy + dy * r * k, 0.13 * r * k, flowers, None)
