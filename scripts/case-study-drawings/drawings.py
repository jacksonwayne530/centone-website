"""Case-study drawings for the Built to Last essay: an exploded axonometric and a finished isometric
on a site tile. Run from the repo root:
    python3 scripts/case-study-drawings/drawings.py public/knowledge/built-to-last
"""
import sys
from iso import Canvas, Face, INK, tree, shrub

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'

# ---- Palette ----
BASALT = dict(top='#6a6c6f', left='#4b4e52', right='#3b3d41', joint='#676b70')
CAP = dict(top='#d9d2c4', left='#5f6266', right='#4c4f53')
TERRA = dict(top='#dc9670', left='#c47852', right='#a86242', joint_l='#b06a47', joint_r='#95553a', band_l='#e3b08c', band_r='#c8906e')
GLASS_L, GLASS_R = '#a7c3d0', '#86a5b4'
CMU = dict(top='#d9d4c9', left='#c5bfb3', right='#aca69a', joint='#968f83')
CONC = dict(top='#dcd8d0', left='#c6c2ba', right='#aeaaa2')
CLT = dict(top='#efcd98', left='#deb37a', right='#c69962', seam='#c39158')
GLULAM = dict(top='#e2b77e', left='#d4a467', right='#b98a52')
WOOD = dict(top='#b98a5c', left='#a8794f', right='#8f6440')
SOIL_TOP = '#6f8f4c'
PAVE = '#ddd5c6'
PAPER = '#f5f0e6'
RAIL = '#cfe6ee'
AWNING = dict(top='#3f7363', left='#2f5d50', right='#284f44')

# ---- Building dimensions (feet) ----
PX0, PX1, PY0, PY1 = 0, 100, 0, 64          # podium footprint
P_TOP = 29                                   # top of podium walls
DECK = 31                                    # podium deck (top of the cap / slab)
TX0, TX1, TY0, TY1 = 14, 86, 6, 50          # tower footprint
FLOOR = 10.5
FLOORS = 8
T_TOP = DECK + FLOOR * FLOORS               # 115
ROOF = T_TOP + 1                             # 116: terrace level
CORE = (62, 15, 75, 26)                      # stair, elevator, and service riser core


# ---- Podium facade (basalt) ----

def bays(width, piers, pier_w=3.0):
    n = piers - 1
    w = (width - piers * pier_w) / n
    return [(pier_w + i * (w + pier_w), pier_w + i * (w + pier_w) + w) for i in range(n)]


def podium_facade(face, glass, cutout=False, awnings=True, lobby_bay=None):
    """Basalt coursing, storefronts, and upper windows on one podium face (0..31 tall)."""
    face.rect(0, 0, face.w, 1.2, '#2f3134', INK, 0.6)  # dark plinth
    face.coursing(2.0, 5.0, BASALT['joint'], 0.45, v0=1.2, v1=P_TOP)
    fill = PAPER if cutout else glass
    for i, (u0, u1) in enumerate(bays(face.w, 7 if face.kind == 'left' else 5)):
        if cutout:
            face.rect(u0, 1.2, u1, 14.5, fill, INK, 0.9)
        else:
            door = i == lobby_bay
            third = (u1 - u0) / 3
            face.window(u0, 1.2, u1, 14.5, '#7f9aa6' if door else glass, mullions=(u0 + third, u0 + 2 * third), transom=11.8)
        # Upper floor: two windows per bay.
        bw = u1 - u0
        for a, b in ((u0 + 1.3, u0 + bw / 2 - 0.7), (u0 + bw / 2 + 0.7, u1 - 1.3)):
            if cutout:
                face.rect(a, 18.8, b, 26.2, fill, INK, 0.9)
            else:
                face.window(a, 18.8, b, 26.2, glass, mullions=((a + b) / 2,))
                face.rect(a - 0.3, 18.3, b + 0.3, 18.8, '#7a7d81', INK, 0.6)  # stone sill
        if not cutout and awnings:
            if i == lobby_bay:
                # Flat steel canopy over the lobby door.
                cv = face.cv
                cv.poly([face.at(u0 - 0.5, 15.2, 0), face.at(u1 + 0.5, 15.2, 0), face.at(u1 + 0.5, 15.2, 5), face.at(u0 - 0.5, 15.2, 5)], '#3a3c40')
                cv.poly([face.at(u0 - 0.5, 14.6, 5), face.at(u1 + 0.5, 14.6, 5), face.at(u1 + 0.5, 15.2, 5), face.at(u0 - 0.5, 15.2, 5)], '#2a2c2f')
            else:
                cv = face.cv
                cv.poly([face.at(u0, 15.3, 0), face.at(u1, 15.3, 0), face.at(u1, 12.9, 4.2), face.at(u0, 12.9, 4.2)], AWNING['left'] if face.kind == 'left' else AWNING['right'])
                cv.poly([face.at(u0, 12.2, 4.2), face.at(u1, 12.2, 4.2), face.at(u1, 12.9, 4.2), face.at(u0, 12.9, 4.2)], AWNING['top'])


def podium_cmu_facade(face, glass):
    face.coursing(2.0, 4.0, CMU['joint'], 0.45, v0=0, v1=P_TOP)
    for u0, u1 in bays(face.w, 7 if face.kind == 'left' else 5):
        face.rect(u0, 1.2, u1, 14.5, '#57595c', INK, 0.9)  # openings
        bw = u1 - u0
        for a, b in ((u0 + 1.3, u0 + bw / 2 - 0.7), (u0 + bw / 2 + 0.7, u1 - 1.3)):
            face.rect(a, 18.8, b, 26.2, '#57595c', INK, 0.9)


# ---- Tower facade (terracotta rainscreen) ----

def tower_facade(face, glass, cutout=False):
    side = 'l' if face.kind == 'left' else 'r'
    face.coursing(1.75, 4.0, TERRA['joint_' + side], 0.4, v0=0, v1=FLOOR * FLOORS)
    nb = 9 if face.kind == 'left' else 5
    bw = face.w / nb
    for fl in range(FLOORS):
        base = fl * FLOOR
        # Floor band: the edge of each CLT floor, expressed on the skin.
        face.rect(0, base, face.w, base + 0.7, TERRA['band_' + side], INK, 0.5)
        for b in range(nb):
            u0 = b * bw + (bw - 5.0) / 2
            u1 = u0 + 5.0
            if cutout:
                face.rect(u0, base + 2.6, u1, base + 8.8, PAPER, INK, 0.8)
            else:
                face.window(u0, base + 2.6, u1, base + 8.8, glass, mullions=((u0 + u1) / 2,), transom=base + 7.3)
                face.rect(u0 - 0.25, base + 2.2, u1 + 0.25, base + 2.6, TERRA['band_' + side], INK, 0.5)
    # Coping at the top.
    face.rect(0, FLOOR * FLOORS, face.w, FLOOR * FLOORS + 1.0, TERRA['band_' + side], INK, 0.6)


def glass_rail(cv, a, b, z, h=3.5):
    (x0, y0), (x1, y1) = a, b
    cv.poly([(x0, y0, z), (x1, y1, z), (x1, y1, z + h), (x0, y0, z + h)], RAIL, INK, 0.6, opacity=0.45)
    cv.line((x0, y0, z + h), (x1, y1, z + h), '#3a3c40', 1.4)


def roof_terrace(cv, z, overrun=True):
    """Planters, trees, lawn, pergola, and rails on the tower roof at height z."""
    # Paver joints on the deck.
    for x in range(TX0 + 6, TX1, 6):
        cv.line((x, TY0, z), (x, TY1, z), '#c7bead', 0.5)
    # Back rails first.
    glass_rail(cv, (TX0, TY0), (TX1, TY0), z)
    glass_rail(cv, (TX0, TY0), (TX0, TY1), z)
    # Lawn.
    cv.poly([(27, 20, z + 0.05), (49, 20, z + 0.05), (49, 42, z + 0.05), (27, 42, z + 0.05)], '#9cc06f', INK, 0.6)
    # Back planter with trees.
    cv.box(TX0 + 1.5, TY0 + 1.5, z, TX1 - 1.5, TY0 + 7.5, z + 2.5, SOIL_TOP, WOOD['left'], WOOD['right'], sw=0.8)
    for x in (24, 40, 56, 72):
        shrub(cv, x + 6, TY0 + 4.5, z + 2.5, 1.8, flowers='#e9a3b5')
    for x in (22, 46, 70):
        tree(cv, x, TY0 + 4.5, z + 2.5, h=15, r=4.6)
    # Left planter.
    cv.box(TX0 + 1.5, TY0 + 7.5, z, TX0 + 7.5, TY1 - 1.5, z + 2.5, SOIL_TOP, WOOD['left'], WOOD['right'], sw=0.8)
    for y in (16, 24, 32, 40):
        shrub(cv, TX0 + 4.5, y, z + 2.5, 1.9, flowers='#f2cf63' if y % 16 else None)
    # Elevator and stair overrun (services reach the roof here).
    if overrun:
        cv.box(CORE[0], CORE[1], z, CORE[2], CORE[3], z + 8.5, TERRA['top'], TERRA['left'], TERRA['right'], sw=0.9)
        cv.box(CORE[0] - 0.5, CORE[1] - 0.5, z + 8.5, CORE[2] + 0.5, CORE[3] + 0.5, z + 9.2, '#e3b08c', '#d29a74', '#b9805c', sw=0.8)
    # Pergola over the lawn.
    posts = [(30, 23), (46, 23), (30, 39), (46, 39)]
    for x, y in posts:
        cv.box(x - 0.4, y - 0.4, z, x + 0.4, y + 0.4, z + 9, GLULAM['top'], GLULAM['left'], GLULAM['right'], sw=0.7)
    for y in (23, 39):
        cv.box(28.5, y - 0.4, z + 9, 47.5, y + 0.4, z + 10, GLULAM['top'], GLULAM['left'], GLULAM['right'], sw=0.7)
    for x in range(30, 47, 3):
        cv.box(x - 0.25, 21.5, z + 10, x + 0.25, 40.5, z + 10.6, GLULAM['top'], GLULAM['left'], GLULAM['right'], sw=0.6)
    # Benches and a table.
    cv.box(54, 34, z, 60, 35.5, z + 1.6, WOOD['top'], WOOD['left'], WOOD['right'], sw=0.7)
    cv.box(66, 36, z, 70, 40, z + 2.4, '#e8e2d6', '#cfc8bb', '#b8b1a4', sw=0.7)
    # Planters along the front edge.
    cv.box(TX1 - 6.5, TY0 + 9, z, TX1 - 1.5, TY1 - 1.5, z + 2.5, SOIL_TOP, WOOD['left'], WOOD['right'], sw=0.8)
    for y in (16, 26, 36, 45):
        shrub(cv, TX1 - 4, y, z + 2.5, 1.9, flowers='#e9a3b5' if y in (26, 45) else None)
    tree(cv, TX1 - 4, TY1 - 5, z + 2.5, h=13, r=4)
    # Front rails last.
    glass_rail(cv, (TX0, TY1), (TX1, TY1), z)
    glass_rail(cv, (TX1, TY0), (TX1, TY1), z)


def deck_planters(cv, z):
    """Planters on the podium deck, in front of the tower."""
    items = []
    for x0 in (3, 27, 53, 77):
        items.append(('front', x0))
    for y0 in (4, 28):
        items.append(('side', y0))
    items.sort(key=lambda it: (it[1] + 10 + 58) if it[0] == 'front' else (93 + it[1] + 10))
    for kind, a in items:
        if kind == 'front':
            cv.box(a, 55, z, a + 20, 62, z + 3.2, SOIL_TOP, CAP['left'], CAP['right'], sw=0.8)
            for x in (a + 4, a + 10, a + 16):
                shrub(cv, x, 58.5, z + 3.2, 2.0, flowers='#f2cf63' if x % 3 == 0 else None)
        else:
            cv.box(91, a, z, 98, a + 20, z + 3.2, SOIL_TOP, CAP['left'], CAP['right'], sw=0.8)
            for y in (a + 4, a + 10, a + 16):
                shrub(cv, 94.5, y, z + 3.2, 2.0, flowers='#e9a3b5' if y % 4 == 0 else None)
    tree(cv, 94.5, 58.5, z + 3.2, h=14, r=4.4)


# =====================================================================
# Finished building on a site tile
# =====================================================================

def finished():
    cv = Canvas(k=3.4)
    # Ground tile with a soil edge, like the homepage drawings.
    cv.box(-14, -12, -7, 114, 84, 0, '#a7c77a', '#8a5a3c', '#71472f', sw=1.2)
    # Back and side planting.
    for x in (-8, 6, 24, 46, 68, 88):
        shrub(cv, x, -6, 0, 2.6)
    for y in (6, 24, 44):
        shrub(cv, -8, y, 0, 2.6, flowers='#e9a3b5')
    # Sidewalks (raised slabs) with joints.
    cv.box(102, -12, 0, 114, 66, 0.6, '#e6e0d5', '#d3ccbf', '#bfb8ab', sw=0.9)
    cv.box(-14, 66, 0, 114, 84, 0.6, '#e6e0d5', '#d3ccbf', '#bfb8ab', sw=0.9)
    for x in range(-6, 114, 8):
        cv.line((x, 66, 0.6), (x, 84, 0.6), '#c5bdaf', 0.7)
    cv.line((-14, 76, 0.6), (114, 76, 0.6), '#c5bdaf', 0.7)
    for y in range(-4, 66, 8):
        cv.line((102, y, 0.6), (114, y, 0.6), '#c5bdaf', 0.7)
    # Curb line.
    cv.line((-14, 82.5, 0.6), (114, 82.5, 0.6), '#b3ab9d', 0.8)
    cv.line((112.5, -12, 0.6), (112.5, 84, 0.6), '#b3ab9d', 0.8)
    # Paving strip between building and sidewalk.
    cv.poly([(PX0 - 2, PY1, 0.05), (PX1 + 2, PY1, 0.05), (PX1 + 2, 66, 0.05), (PX0 - 2, 66, 0.05)], '#e6e0d5', None)
    cv.poly([(PX1, PY0 - 2, 0.05), (102, PY0 - 2, 0.05), (102, PY1 + 2, 0.05), (PX1, PY1 + 2, 0.05)], '#e6e0d5', None)

    # Podium.
    cv.box(PX0, PY0, 0, PX1, PY1, P_TOP, BASALT['top'], BASALT['left'], BASALT['right'], sw=1.2)
    podium_facade(Face(cv, 'right', PX0, PY0, 0, PX1, PY1, DECK), GLASS_R, lobby_bay=None)
    podium_facade(Face(cv, 'left', PX0, PY0, 0, PX1, PY1, DECK), GLASS_L, lobby_bay=4)
    # Cap band and deck.
    cv.box(PX0 - 0.6, PY0 - 0.6, P_TOP, PX1 + 0.6, PY1 + 0.6, DECK, PAVE, CAP['left'], CAP['right'], sw=1.1)
    for x in range(6, 100, 6):
        cv.line((x, 0, DECK), (x, 50 if 14 <= x <= 86 else PY1, DECK), '#c7bead', 0.5)

    # Tower.
    cv.box(TX0, TY0, DECK, TX1, TY1, ROOF, PAVE, TERRA['left'], TERRA['right'], sw=1.2)
    tower_facade(Face(cv, 'right', TX0, TY0, DECK, TX1, TY1, ROOF), GLASS_R)
    tower_facade(Face(cv, 'left', TX0, TY0, DECK, TX1, TY1, ROOF), GLASS_L)
    roof_terrace(cv, ROOF)
    deck_planters(cv, DECK)

    # Street furniture and trees, back to front.
    cv.box(18, 69, 0.6, 25, 70.4, 2.2, WOOD['top'], WOOD['left'], WOOD['right'], sw=0.8)
    cv.box(74, 69, 0.6, 81, 70.4, 2.2, WOOD['top'], WOOD['left'], WOOD['right'], sw=0.8)
    trees = [(108, 6), (108, 34), (6, 79), (34, 79), (62, 79), (90, 79), (108, 60)]
    trees.sort(key=lambda t: t[0] + t[1])
    for x, y in trees:
        cv.poly([(x - 2.2, y - 2.2, 0.62), (x + 2.2, y - 2.2, 0.62), (x + 2.2, y + 2.2, 0.62), (x - 2.2, y + 2.2, 0.62)], '#5b4636', INK, 0.7)
        tree(cv, x, y, 0.6, h=26, r=7.8)
    return cv.svg(pad=20)


# =====================================================================
# Exploded axonometric
# =====================================================================

E = 12                     # how far the skins are pulled out from the structure
Z_POD = 28                 # podium walls start here
Z_SLAB = Z_POD + P_TOP + 22
Z_TWR = Z_SLAB + 2 + 34
Z_TERR = Z_TWR + FLOOR * FLOORS + 1 + 34

COLS_X = [14.65 + i * (85.35 - 14.65) / 6 for i in range(7)]
COLS_Y = [6.65, 20.9, 35.1, 49.35]


def exploded():
    cv = Canvas(k=3.0)
    guide = dict(stroke='#8a8378', sw=0.8, dash='3 4')
    badges = []

    # 1. Foundation mat.
    cv.box(-2, -2, -3, 102, 66, 0, CONC['top'], CONC['left'], CONC['right'], sw=1.1)
    for x, y in ((0, 64), (100, 64), (100, 0), (0, 0)):
        cv.line((x, y, 0), (x, y, Z_POD), **guide)
    badges.append((1, (6, 66, -1.5), 'left'))

    # 2. Podium structure: reinforced CMU walls.
    cv.box(PX0, PY0, Z_POD, PX1, PY1, Z_POD + P_TOP, CMU['top'], CMU['left'], CMU['right'], sw=1.1)
    podium_cmu_facade(Face(cv, 'right', PX0, PY0, Z_POD, PX1, PY1, Z_POD + P_TOP), GLASS_R)
    podium_cmu_facade(Face(cv, 'left', PX0, PY0, Z_POD, PX1, PY1, Z_POD + P_TOP), GLASS_L)
    # Interior bearing line and columns seen from above.
    for x in (25, 50, 75):
        cv.line((x, 2, Z_POD + P_TOP), (x, 62, Z_POD + P_TOP), '#a9a397', 1.6)
    badges.append((2, (PX1, PY1 - 6, Z_POD + 21), 'right'))

    # 3. Basalt cladding, pulled off the walls.
    for z in (Z_POD, Z_POD + DECK):
        cv.line((PX1, PY0, z), (PX1 + E, PY0, z), **guide)
        cv.line((PX1, PY1, z), (PX1 + E, PY1, z), **guide)
        cv.line((PX0, PY1, z), (PX0, PY1 + E, z), **guide)
        cv.line((PX1, PY1, z), (PX1, PY1 + E, z), **guide)
    cv.box(PX1 + E, PY0, Z_POD, PX1 + E + 1, PY1, Z_POD + DECK, BASALT['top'], BASALT['left'], BASALT['right'], sw=1.1)
    podium_facade(Face(cv, 'right', PX0, PY0, Z_POD, PX1 + E + 1, PY1, Z_POD + DECK), GLASS_R, cutout=True)
    cv.box(PX0, PY1 + E, Z_POD, PX1, PY1 + E + 1, Z_POD + DECK, BASALT['top'], BASALT['left'], BASALT['right'], sw=1.1)
    podium_facade(Face(cv, 'left', PX0, PY0, Z_POD, PX1, PY1 + E + 1, Z_POD + DECK), GLASS_L, cutout=True)
    badges.append((3, (10, PY1 + E + 1, Z_POD + 22), 'left'))

    # 4. Podium slab: the 3-hour concrete separation the timber stands on.
    for x, y in ((0, 64), (100, 64), (100, 0)):
        cv.line((x, y, Z_POD + P_TOP), (x, y, Z_SLAB), **guide)
    cv.box(PX0, PY0, Z_SLAB, PX1, PY1, Z_SLAB + 2, CONC['top'], CONC['left'], CONC['right'], sw=1.1)
    cv.poly([(TX0, TY0, Z_SLAB + 2.02), (TX1, TY0, Z_SLAB + 2.02), (TX1, TY1, Z_SLAB + 2.02), (TX0, TY1, Z_SLAB + 2.02)], '#cfcac1', '#9f9a91', 0.7)
    badges.append((4, (8, 60, Z_SLAB + 1), 'left'))

    # 5 + 6. CLT tower structure: floors on glulam columns around a timber core.
    for x, y in ((TX0, TY1), (TX1, TY1), (TX1, TY0)):
        cv.line((x, y, Z_SLAB + 2), (x, y, Z_TWR), **guide)
    plate_t = 0.9
    for fl in range(FLOORS + 1):
        z = Z_TWR + fl * FLOOR
        if fl > 0:
            zb = z - FLOOR + plate_t
            parts = []
            for x in COLS_X:
                for y in COLS_Y:
                    if CORE[0] - 1 <= x <= CORE[2] + 1 and CORE[1] - 1 <= y <= CORE[3] + 1:
                        continue
                    parts.append(('col', x, y))
            parts.append(('core', (CORE[0] + CORE[2]) / 2, (CORE[1] + CORE[3]) / 2))
            parts.sort(key=lambda p: p[1] + p[2])
            for kind, x, y in parts:
                if kind == 'col':
                    cv.box(x - 0.65, y - 0.65, zb, x + 0.65, y + 0.65, z, GLULAM['top'], GLULAM['left'], GLULAM['right'], sw=0.7)
                else:
                    cv.box(CORE[0], CORE[1], zb, CORE[2], CORE[3], z, '#c69962', '#b98d58', '#a37a49', sw=0.9)
                    # Riser doors on the core's face: services you can reach.
                    f = Face(cv, 'right', CORE[0], CORE[1], zb, CORE[2], CORE[3], z)
                    f.rect(2.0, 0.6, 4.6, 7.8, '#8a6a43', INK, 0.6)
                    f.rect(6.4, 0.6, 9.0, 7.8, '#8a6a43', INK, 0.6)
        cv.box(TX0, TY0, z, TX1, TY1, z + plate_t, CLT['top'], CLT['left'], CLT['right'], sw=0.9)
        for x in range(TX0 + 8, TX1, 8):
            cv.line((x, TY0, z + plate_t), (x, TY1, z + plate_t), CLT['seam'], 0.6)
    top_struct = Z_TWR + FLOORS * FLOOR + plate_t
    # The core rises through the roof (the overrun), which is where you can see it.
    cv.box(CORE[0], CORE[1], top_struct, CORE[2], CORE[3], top_struct + 8.5, '#c69962', '#b98d58', '#a37a49', sw=0.9)
    f = Face(cv, 'right', CORE[0], CORE[1], top_struct, CORE[2], CORE[3], top_struct + 8.5)
    f.rect(2.0, 0.4, 4.8, 7.6, '#8a6a43', INK, 0.6)
    f.rect(6.4, 0.4, 9.2, 7.6, '#8a6a43', INK, 0.6)
    badges.append((5, (TX1, TY1 - 1, Z_TWR + 5 * FLOOR + 0.5), 'right'))
    badges.append((6, (CORE[2], CORE[1] + 2, Z_TWR + FLOORS * FLOOR + plate_t + 5), 'right'))

    # 7. Terracotta rainscreen, pulled off the structure.
    for z in (Z_TWR, Z_TWR + FLOOR * FLOORS + 1):
        cv.line((TX1, TY0, z), (TX1 + E, TY0, z), **guide)
        cv.line((TX1, TY1, z), (TX1 + E, TY1, z), **guide)
        cv.line((TX0, TY1, z), (TX0, TY1 + E, z), **guide)
        cv.line((TX1, TY1, z), (TX1, TY1 + E, z), **guide)
    zt = Z_TWR + FLOOR * FLOORS + 1
    cv.box(TX1 + E, TY0, Z_TWR, TX1 + E + 1, TY1, zt, TERRA['top'], TERRA['left'], TERRA['right'], sw=1.0)
    tower_facade(Face(cv, 'right', TX0, TY0, Z_TWR, TX1 + E + 1, TY1, zt), GLASS_R, cutout=True)
    cv.box(TX0, TY1 + E, Z_TWR, TX1, TY1 + E + 1, zt, TERRA['top'], TERRA['left'], TERRA['right'], sw=1.0)
    tower_facade(Face(cv, 'left', TX0, TY0, Z_TWR, TX1, TY1 + E + 1, zt), GLASS_L, cutout=True)
    badges.append((7, (TX0 + 6, TY1 + E + 1, Z_TWR + 50), 'left'))

    # 8. Roof terrace.
    for x, y in ((TX0, TY1), (TX1, TY1), (TX1, TY0)):
        cv.line((x, y, top_struct), (x, y, Z_TERR), **guide)
    cv.box(TX0, TY0, Z_TERR, TX1, TY1, Z_TERR + 1.5, PAVE, '#8a6a4a', '#74583c', sw=1.0)
    roof_terrace(cv, Z_TERR + 1.5, overrun=False)
    badges.append((8, (TX0 + 2, TY1, Z_TERR + 0.7), 'left'))

    # Numbered callouts, pulled out to the sides.
    xs = [cv.p(*pt)[0] for _, pt, _ in badges]
    left_x = cv.minx - 34
    right_x = cv.maxx + 34
    for n, pt, side in badges:
        ax, ay = cv.p(*pt)
        bx = left_x if side == 'left' else right_x
        cv.circle_px(ax, ay, 3.2, INK, None)
        cv.raw(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{ay:.1f}" stroke="{INK}" stroke-width="1"/>')
        cv.circle_px(bx, ay, 15, '#2f5d50', '#ffffff', 2)
        cv.raw(f'<text x="{bx:.1f}" y="{ay + 6:.1f}" text-anchor="middle" font-size="17" font-weight="700" fill="#ffffff">{n}</text>')
        cv.minx = min(cv.minx, bx - 16)
        cv.maxx = max(cv.maxx, bx + 16)
    return cv.svg(pad=18)


if __name__ == '__main__':
    import os
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'case-study-tower.svg'), 'w') as fh:
        fh.write(finished())
    with open(os.path.join(OUT, 'case-study-exploded.svg'), 'w') as fh:
        fh.write(exploded())
    print('ok')
