import math

# ---- grid geometry ----
COLS = 52
ROWS = 7
CELL = 12
GAP = 3
STEP = CELL + GAP
PAD_X = 30
PAD_Y = 60   # space for title on top

W = PAD_X*2 + COLS*STEP - GAP
H = PAD_Y + ROWS*STEP - GAP + 20

# contribution palette (dark on dark, matching theme)
palette = {
    0:"#161b22",  # empty (background)
    1:"#0e4429",
    2:"#006d32",
    3:"#26a641",
    4:"#39d353",
}

# grid per column -> intensity pattern (looks organic)
import random
random.seed(42)
grid = []
for c in range(COLS):
    col = []
    for r in range(ROWS):
        # pseudo random but with clusters
        base = random.random()
        if base < 0.42: v = 0
        elif base < 0.62: v = 1
        elif base < 0.80: v = 2
        elif base < 0.93: v = 3
        else: v = 4
        col.append(v)
    grid.append(col)

def cell_pos(c, r):
    x = PAD_X + c*STEP
    y = PAD_Y + r*STEP
    return x, y

lines = []
lines.append('<svg width="%d" height="%d" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" font-family="Fira Code, monospace" role="img" aria-label="GitHub Contribution Ninja">' % (W,H,W,H))

# subtle background rect
lines.append('  <rect width="%d" height="%d" fill="#0d1117"/>' % (W,H))

# Title
lines.append('  <text x="%d" y="30" text-anchor="middle" fill="#00d9ff" font-size="17" font-weight="700">🥷 NINJA CONTRIBUTIONS</text>' % (W/2))

# Draw grid cells
delay = 0.0
for c in range(COLS):
    for r in range(ROWS):
        v = grid[c][r]
        x, y = cell_pos(c, r)
        base = palette[v]
        # each cell: fill = base, then animate to eaten (dark) when ninja passes
        # stagger begin by column so trail follows ninja
        begin = 0.0 + c*0.18   # trail delay
        dur = 1.2
        lines.append('    <rect x="%d" y="%d" width="%d" height="%d" rx="2" fill="%s">' % (x, y, CELL, CELL, base))
        # eaten: animate fill to #0d1117 (the trail the ninja leaves), only some cells "eaten"
        if v >= 1:
            lines.append('      <animate attributeName="fill" values="%s;%s;%s" keyTimes="0;0.5;1" begin="%fs" dur="%fs" repeatCount="indefinite"/>' % (base, "#39d353", "#0d1117", begin, dur))
        lines.append('    </rect>')

# ---- NINJA SPRITE ----
# A running ninja drawn as a group; we animate its x translation across the grid.
# Build ninja at origin (0,0) then translate.
ninja = []
ninja.append('  <g>')
# body (torso) - dark purple/black
ninja.append('    <rect x="-6" y="-22" width="14" height="16" rx="3" fill="#2b2d42"/>')
# head
ninja.append('    <rect x="-7" y="-40" width="16" height="16" rx="5" fill="#3a3f52"/>')
# headband
ninja.append('    <rect x="-8" y="-36" width="18" height="5" fill="#00d9ff"/>')
# eyes (ninja headband) - two cyan dots
ninja.append('    <rect x="-4" y="-30" width="3" height="2" fill="#00ff88"/>')
ninja.append('    <rect x="1"  y="-30" width="3" height="2" fill="#00ff88"/>')
# trailing scarf - animated flowing path (dashes move), trails BEHIND (left) since ninja runs right
scarf = '    <path d="M-8 -36 C -20 -38, -26 -30, -34 -34 C -40 -36, -42 -30, -48 -33" fill="none" stroke="#00d9ff" stroke-width="3" stroke-linecap="round">'
ninja.append(scarf)
ninja.append('      <animate attributeName="stroke-dashoffset" values="0;40;0" dur="1.1s" repeatCount="indefinite"/>')
ninja.append('    </path>')
# arms
ninja.append('    <rect x="-14" y="-20" width="8" height="5" rx="2" fill="#2b2d42"><animateTransform attributeName="transform" type="rotate" values="-20 -10 -18;20 -10 -18;-20 -10 -18" dur="0.55s" repeatCount="indefinite"/></rect>')
ninja.append('    <rect x="8" y="-20" width="8" height="5" rx="2" fill="#2b2d42"><animateTransform attributeName="transform" type="rotate" values="20 12 -18;-20 12 -18;20 12 -18" dur="0.55s" repeatCount="indefinite"/></rect>')
# legs (running motion)
ninja.append('    <rect x="-5" y="-6" width="5" height="10" rx="2" fill="#1f2233"><animateTransform attributeName="transform" type="rotate" values="-30 -2 -6;40 -2 -6;-30 -2 -6" dur="0.5s" repeatCount="indefinite"/></rect>')
ninja.append('    <rect x="1" y="-6" width="5" height="10" rx="2" fill="#1f2233"><animateTransform attributeName="transform" type="rotate" values="40 3 -6;-30 3 -6;40 3 -6" dur="0.5s" repeatCount="indefinite"/></rect>')
# feet
ninja.append('    <rect x="-4" y="3" width="6" height="3" rx="1.5" fill="#00ff88"/>')
ninja.append('    <rect x="1" y="3" width="6" height="3" rx="1.5" fill="#00ff88"/>')
# a ninja star (shuriken) occasionally spins ahead
ninja.append('    <g><path d="M0 -3 L2 -1 L4 -3 L3 0 L5 1 L3 2 L4 5 L1 3 L0 5 L-1 3 L-4 5 L-2 2 L-5 1 L-3 0 L-4 -3 L-2 -1 L0 -3" fill="#00ff88" opacity="0.9">')
ninja.append('      <animateTransform attributeName="transform" type="rotate" values="0 0 0;360 0 0" dur="0.6s" repeatCount="indefinite"/></path></g>')
ninja.append('  </g>')

# The ninja group translated across the grid, bobbing up/down
ninja_block = '\n'.join(ninja)
# y-center of grid
grid_cy = PAD_Y + (ROWS*STEP-GAP)/2
animate_move = ('  <g>\n    <animateTransform attributeName="transform" type="translate" '
                'values="%d %d;%d %d;%d %d" keyTimes="0;0.5;1" '
                'dur="14s" repeatCount="indefinite"/>') % (PAD_X, grid_cy, W-PAD_X-20, grid_cy-14, PAD_X, grid_cy)
lines.append(animate_move)
# bobbing via nested group y
lines.append('    <g>')
lines.append('      <animateTransform attributeName="transform" type="translate" values="0 0;0 -16;0 0" dur="0.5s" repeatCount="indefinite"/>')
lines.append(ninja_block)
lines.append('    </g>')
lines.append('  </g>')

lines.append('</svg>')
open('github-contribution-grid-ninja-dark.svg','w').write('\n'.join(lines))
print("SVG generated:", W, "x", H)
