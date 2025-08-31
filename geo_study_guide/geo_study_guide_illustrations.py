# geo_study_guide_illustrations.py
from __future__ import annotations
import math
from typing import Callable, Optional, Union, Dict

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon, Rectangle

# -----------------------------------------------------------------------------
# Registry
# -----------------------------------------------------------------------------
DRAWERS: Dict[str, Callable] = {}

def register(name: str):
    """Decorator to register a drawer function by plain-text key."""
    def _wrap(fn: Callable):
        DRAWERS[name] = fn
        return fn
    return _wrap

def resolve_drawer(drawer: Optional[Union[str, Callable]]) -> Optional[Callable]:
    """Return a callable drawer given a string key or function; else None."""
    if drawer is None:
        return None
    if callable(drawer):
        return drawer
    if isinstance(drawer, str):
        return DRAWERS.get(drawer)
    return None

# -----------------------------------------------------------------------------
# Shared primitives
# -----------------------------------------------------------------------------
def _setup_axes(ax, margin=0.18):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1 - margin, 1 + margin)
    ax.set_ylim(-1 - margin, 1 + margin)
    ax.axis("off")

def _draw_point(ax, xy=(0, 0)):
    ax.plot([xy[0]], [xy[1]], marker="o")

def _draw_ray(ax, angle_deg, length=1.1, origin=(0, 0)):
    a = math.radians(angle_deg)
    x = origin[0] + length * math.cos(a)
    y = origin[1] + length * math.sin(a)
    ax.plot([origin[0], x], [origin[1], y])

def _draw_line(ax, angle_deg, length=1.6):
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)
    s = length
    ax.plot([-s*dx, s*dx], [-s*dy, s*dy])

def _draw_segment(ax, p, q, mark_ends=True):
    ax.plot([p[0], q[0]], [p[1], q[1]])
    if mark_ends:
        _draw_point(ax, p); _draw_point(ax, q)

def _draw_arc(ax, start_deg, end_deg, radius=0.48, origin=(0, 0)):
    s = start_deg % 360; e = end_deg % 360
    if e <= s: e += 360
    ax.add_patch(Arc(origin, 2*radius, 2*radius, angle=0, theta1=s, theta2=e))

def _right_angle_marker(ax, corner=(0,0), size=0.18, angle_deg=0):
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    p1 = (corner[0] + size*ux, corner[1] + size*uy)
    p2 = (p1[0] + size*vx, p1[1] + size*vy)
    p3 = (corner[0] + size*vx, corner[1] + size*vy)
    ax.plot([corner[0], p1[0], p2[0], p3[0], corner[0]],
            [corner[1], p1[1], p2[1], p3[1], corner[1]])

def _placeholder(ax, label: str):
    _setup_axes(ax)
    ax.text(0.5, 0.5, f"[{label}]", ha="center", va="center")

def _draw_arrow_ray(ax, angle_deg, length=1.1, origin=(0, 0), head_scale=12):
    """
    Draw a ray with an arrowhead indicating direction.
    Monochrome; linewidth=1.
    """
    import math
    a = math.radians(angle_deg)
    ex = origin[0] + length * math.cos(a)
    ey = origin[1] + length * math.sin(a)
    ax.annotate(
        "",
        xy=(ex, ey), xytext=origin,
        arrowprops=dict(arrowstyle="-|>", lw=1, mutation_scale=head_scale, color="black")
    )

# Helper: draw a line with two arrowheads (both directions)
# Helper: draw a line with outward arrowheads that don't overlap the line body
def _draw_double_arrow_line(ax, angle_deg, span=1.05, origin=(0, 0), gap=0.14, lw=1, head_scale=12):
    """
    angle_deg: line angle in degrees
    span: half-length of the full line (tip-to-tip)
    gap: clearance between each arrowhead and the line body
    """
    import math
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)

    # Tips (where arrowheads point)
    p1_tip = (origin[0] - span * dx, origin[1] - span * dy)
    p2_tip = (origin[0] + span * dx, origin[1] + span * dy)

    # Shorten the visible line so arrowheads don't sit "inside" it
    p1_line = (p1_tip[0] + gap * dx, p1_tip[1] + gap * dy)
    p2_line = (p2_tip[0] - gap * dx, p2_tip[1] - gap * dy)

    # Line body
    ax.plot([p1_line[0], p2_line[0]], [p1_line[1], p2_line[1]], lw=lw, color="black")

    # Arrowheads (outward)
    ax.annotate("", xy=p2_tip, xytext=p2_line,
                arrowprops=dict(arrowstyle="-|>", lw=lw, mutation_scale= head_scale, color="black"))
    ax.annotate("", xy=p1_tip, xytext=p1_line,
                arrowprops=dict(arrowstyle="-|>", lw=lw, mutation_scale= head_scale, color="black"))


# -----------------------------------------------------------------------------
# Foundations / Incidence
# -----------------------------------------------------------------------------
@register("line")
def drawer_line(ax):
    _setup_axes(ax)
    ax.set_prop_cycle(color=["black"])  # monochrome
    # 10° tilt; use 0 for horizontal if you prefer
    _draw_double_arrow_line(ax, angle_deg=10, span=1.05, gap=0.14, lw=1, head_scale=12)

@register("finite_plane")
def drawer_finite_plane(ax):
    _setup_axes(ax)
    ax.add_patch(Rectangle((-0.8, -0.5), 1.6, 1.0, fill=False))
    ax.text(0, -0.9, "bounded region", ha="center")

@register("collinear")
def drawer_collinear(ax):
    _setup_axes(ax, margin=2.4)           # keeps tips visible up to ~±2.40
    ax.set_prop_cycle(color=["black"])    # monochrome

    # Points stay exactly where you placed them
    MS = 3; y = 0.0
    xs = [-1.9, 0.0, 1.9]
    labels = ["A", "B", "C"]
    ax.plot(xs, [y]*len(xs), marker="o", linestyle="", color="black", markersize=MS)
    for x, lbl in zip(xs, labels):
        ax.text(x, y + 0.30, lbl, ha="center", fontsize=10)

    # Make arrows longer but ensure the base of each arrowhead starts beyond the outer point
    span = 3.36                         # was 2.24; tips at ±2.36 (still inside ±2.40 view)
    farthest = 1.9  # from your xs
    epsilon = 0.06  # just-beyond distance past the last point
    gap = max(0.06, span - farthest - epsilon)  # ~0.24 with span=3.20

    # (Optional) slightly smaller heads so they feel lighter
    head_scale = 10   # was 12

    _draw_double_arrow_line(ax, angle_deg=0, span=span, gap=gap, lw=1, head_scale=head_scale)


@register("coplanar")
def drawer_coplanar(ax):
    _setup_axes(ax)
    # simple skewed plane with a couple of points/segments
    poly = Polygon([(-0.9, -0.4), (0.7, -0.6), (0.9, 0.4), (-0.7, 0.6)], closed=True, fill=False)
    ax.add_patch(poly)
    _draw_point(ax, (0.0, 0.1)); _draw_point(ax, (-0.2, -0.1))
    _draw_segment(ax, (-0.3, 0.2), (0.4, -0.15), mark_ends=False)

# -----------------------------------------------------------------------------
# Segments / Rays
# -----------------------------------------------------------------------------
@register("segment")
def drawer_segment(ax):
    _setup_axes(ax)
    _draw_segment(ax, (-0.8, 0), (0.8, 0))

@register("midpoint")
def drawer_midpoint(ax):
    _setup_axes(ax)
    p, q = (-0.8, 0), (0.8, 0)
    _draw_segment(ax, p, q)
    m = ((p[0]+q[0])/2, (p[1]+q[1])/2)
    ax.plot([m[0]], [m[1]], marker="s")
    ax.text(m[0], m[1]+0.25, "midpoint", ha="center")

# --- Replace your existing segment_bisector drawer with this one ---
@register("segment_bisector")
def drawer_segment_bisector(ax):
    """
    Segment bisector: perpendicular (left) and oblique (right), monochrome.
    Labels A, M, B are lowered; M is nudged right ~half-letter width.
    """
    import math

    # Two side-by-side panels
    left  = ax.inset_axes([0.05, 0.12, 0.42, 0.76])   # perpendicular
    right = ax.inset_axes([0.53, 0.12, 0.42, 0.76])   # oblique

    def draw_base(panel):
        _setup_axes(panel)
        panel.set_prop_cycle(color=["black"])  # monochrome

        # Base segment A—M—B
        A, M, B = (-0.90, 0.0), (0.0, 0.0), (0.90, 0.0)
        panel.plot([A[0], B[0]], [A[1], B[1]], lw=1, color="black")

        # Endpoints + midpoint (small markers)
        panel.plot([A[0], M[0], B[0]], [A[1], M[1], B[1]],
                   marker="o", linestyle="", color="black", markersize=3)

        # Midpoint tick marks (AM = MB)
        for x in (-0.45, 0.45):
            panel.plot([x, x], [-0.06, 0.06], lw=1, color="black")

        # Labels: move down ~one letter; shift M slightly right (~half-letter)
        LABEL_DOWN = 0.34
        M_DX = 0.2
        panel.text(A[0], -LABEL_DOWN - 0.10, "A", ha="center", fontsize=10)
        panel.text(M[0] + M_DX, -LABEL_DOWN - 0.10, "M", ha="center", fontsize=10)
        panel.text(B[0], -LABEL_DOWN - 0.10, "B", ha="center", fontsize=10)

        return A, M, B

    # Left panel: perpendicular bisector
    A, M, B = draw_base(left)
    # draw vertical line through M with thin stroke
    ang = math.radians(90)
    s = 1.2
    left.plot([-s*math.cos(ang), s*math.cos(ang)],
              [-s*math.sin(ang), s*math.sin(ang)], lw=1, color="black")
    # _right_angle_marker(left, (0.0, 0.0), 0.12, 0)

    # Right panel: oblique (not perpendicular) bisector through M
    A, M, B = draw_base(right)
    ang = math.radians(30)  # any non-90° angle
    s = 1.2
    right.plot([-s*math.cos(ang), s*math.cos(ang)],
               [-s*math.sin(ang), s*math.sin(ang)], lw=1, color="black")



# ---- Replace these three drawers ----
@register("ray")
def drawer_ray(ax):
    _setup_axes(ax)
    _draw_point(ax, (0, 0))  # small origin dot
    _draw_arrow_ray(ax, 25)  # arrow shows direction

@register("origin_of_ray")
def drawer_origin_of_ray(ax):
    _setup_axes(ax)
    origin = (0, 0)
    _draw_point(ax, origin)
    ax.text(origin[0], origin[1] - 0.35, "origin", ha="center", fontsize=9)
    _draw_arrow_ray(ax, 60, origin=origin)

@register("opposite_rays")
def drawer_opposite_rays(ax):
    _setup_axes(ax)
    origin = (0, 0)
    _draw_point(ax, origin)
    _draw_arrow_ray(ax,   0, origin=origin)   # → direction
    _draw_arrow_ray(ax, 180, origin=origin)   # ← direction


@register("betweenness")
def drawer_betweenness(ax):
    _setup_axes(ax)
    _draw_line(ax, 0)
    A, B, C = (-0.7, 0), (0.0, 0), (0.7, 0)
    for pt, label in [(A, "A"), (B, "B"), (C, "C")]:
        _draw_point(ax, pt); ax.text(pt[0], pt[1]+0.12, label, ha="center")
    ax.text(0, -0.35, "AB + BC = AC", ha="center")

# -----------------------------------------------------------------------------
# Angles (basics & types)
# -----------------------------------------------------------------------------
@register("angle")
def drawer_angle(ax):
    _setup_axes(ax)
    _draw_ray(ax, 0); _draw_ray(ax, 45); _draw_arc(ax, 0, 45)

@register("angle_regions")
def drawer_angle_regions(ax):
    _setup_axes(ax)
    _draw_ray(ax, 0); _draw_ray(ax, 60); _draw_arc(ax, 0, 60)
    ax.text(0.85, 0.3, "interior", ha="center")
    ax.text(-0.4, -0.4, "exterior", ha="center")

@register("degree_measure")
def drawer_degree_measure(ax):
    _setup_axes(ax)
    # unit circle and arc
    theta = [math.radians(t) for t in range(0, 361, 10)]
    ax.plot([math.cos(t) for t in theta], [math.sin(t) for t in theta])
    _draw_arc(ax, 0, 90, 0.7)
    ax.text(0.6, 0.05, "90°", ha="center")


@register("degree_measure_image")
def drawer_degree_measure_image(ax, filename: str | None = None):
    """
    Renders Protractor.jpg instead of a plotted drawing.
    Place Protractor.jpg next to your .py files, or pass a custom path via `filename`.
    """
    import os
    from matplotlib import image as mpimg

    # Try common locations / names
    here = os.path.dirname(__file__)
    candidates = [
        filename,
        "Protractor.jpg",
        "protractor.jpg",
        os.path.join(here, "Protractor.jpg"),
        os.path.join(here, "protractor.jpg"),
    ]
    img = None
    for p in candidates:
        if p and os.path.exists(p):
            img = mpimg.imread(p)
            break

    if img is None:
        # Silently skip if not found (no placeholder text)
        ax.set_axis_off()
        return

    # Show image; preserve aspect; no axes
    ax.imshow(img)
    ax.set_axis_off()

@register("acute_angle")
def drawer_acute_angle(ax):
    _setup_axes(ax); _draw_ray(ax, 0); _draw_ray(ax, 30); _draw_arc(ax, 0, 30)

@register("right_angle")
def drawer_right_angle(ax):
    _setup_axes(ax); _draw_ray(ax, 0); _draw_ray(ax, 90); _right_angle_marker(ax, (0,0), 0.18, 0)

@register("obtuse_angle")
def drawer_obtuse_angle(ax):
    _setup_axes(ax); _draw_ray(ax, 0); _draw_ray(ax, 120); _draw_arc(ax, 0, 120)

@register("straight_angle")
def drawer_straight_angle(ax):
    _setup_axes(ax); _draw_ray(ax, 0); _draw_ray(ax, 180); _draw_arc(ax, 0, 180)

@register("reflex_angle")
def drawer_reflex_angle(ax):
    _setup_axes(ax); _draw_ray(ax, 0); _draw_ray(ax, 250); _draw_arc(ax, 0, 250)

@register("full_angle")
def drawer_full_angle(ax):
    _setup_axes(ax)
    _draw_ray(ax, 0); _draw_arc(ax, 0, 360); ax.text(0.0, -0.2, "360°", ha="center")

# -----------------------------------------------------------------------------
# Angle relationships / lines
# -----------------------------------------------------------------------------
@register("complementary")
def drawer_complementary(ax):
    """
    Two angles that sum to 90°. Use distinct radii so the arcs don't overlap.
    """
    _setup_axes(ax)
    # baseline + interior ray
    _draw_ray(ax, 0)     # along +x
    _draw_ray(ax, 90)    # along +y
    _draw_ray(ax, 30)    # example split (30° + 60°)

    # different radii to keep arcs visually separate
    r_small, r_large = 0.50, 0.70
    _draw_arc(ax, 0, 30,  r_small)   # first angle (30°)
    _draw_arc(ax, 30, 90, r_large)   # second angle (60°)

    # optional: indicate total is a right angle
    _right_angle_marker(ax, (0, 0), 0.16, 0)

@register("supplementary")
def drawer_supplementary(ax):
    """
    Two angles that sum to 180°. Use distinct radii so the arcs don't overlap.
    """
    _setup_axes(ax)
    # baseline + interior ray
    _draw_ray(ax, 0)      # along +x
    _draw_ray(ax, 180)    # along -x
    _draw_ray(ax, 110)    # example split (110° + 70°)

    # different radii to keep arcs visually separate
    r_small, r_large = 0.52, 0.72
    _draw_arc(ax, 0,   110, r_small)  # first angle (110°)
    _draw_arc(ax, 110, 180, r_large)  # second angle (70°)

@register("vertical_angles")
def drawer_vertical_angles(ax):
    """
    Vertical angles: draw the left-and-right pair (not top/bottom).
    Lines at ±45°, arcs pulled back a few degrees from each ray.
    """
    _setup_axes(ax)

    # Intersecting lines
    _draw_line(ax, 45)
    _draw_line(ax, -45)

    gap = 12    # degrees to back off from each bordering ray
    r   = 0.52  # arc radius

    # Left vertical angle: between 135° and 225°
    _draw_arc(ax, 135 + gap, 225 - gap, radius=r)

    # Right vertical angle: between 315° and 45° (wraps past 360)
    _draw_arc(ax, 315 + gap, 45 - gap, radius=r)

    # Optional tiny vertex mark
    ax.plot(0, 0, marker="o", markersize=3)

@register("perpendicular_lines")
def drawer_perpendicular_lines(ax):
    _setup_axes(ax)
    _draw_line(ax, 0); _draw_line(ax, 90); _right_angle_marker(ax, (0,0), 0.2, 0)

@register("parallel_with_transversal")
def drawer_parallel_with_transversal(ax):
    _setup_axes(ax)
    ax.plot([-1.2, 1.2], [0.6, 0.6])
    ax.plot([-1.2, 1.2], [-0.6, -0.6])
    ax.plot([-1.0, 1.0], [-0.9, 0.9])

# -----------------------------------------------------------------------------
# Concurrency / intersection
# -----------------------------------------------------------------------------
@register("intersection")
def drawer_intersection(ax):
    _setup_axes(ax)
    _draw_line(ax, 20); _draw_line(ax, -40)

@register("concurrent_lines")
def drawer_concurrent_lines(ax):
    _setup_axes(ax)
    for ang in (0, 60, 120):
        _draw_line(ax, ang)

# -----------------------------------------------------------------------------
# Distance / locus
# -----------------------------------------------------------------------------
@register("equidistant")
def drawer_equidistant(ax):
    """
    The perpendicular bisector as the locus of points equidistant from A and B.
    Adds a bottom caption per your request.
    """
    _setup_axes(ax)

    # Points A and B on a horizontal line
    A, B = (-0.65, 0.0), (0.65, 0.0)
    _draw_point(ax, A); ax.text(A[0], A[1]-0.15, "A", ha="center", fontsize=9)
    _draw_point(ax, B); ax.text(B[0], B[1]-0.15, "B", ha="center", fontsize=9)

    # The perpendicular bisector (the line whose points are equidistant from A and B)
    _draw_line(ax, 90)

    # Optional: show one sample point P on the line with dashed distances to A and B
    P = (0.0, 0.55)
    ax.plot([A[0], P[0]], [A[1], P[1]], linestyle="--")
    ax.plot([B[0], P[0]], [B[1], P[1]], linestyle="--")
    _draw_point(ax, P)

    # Bottom caption (as requested)
    ax.text(0.0, -0.88, "The line is equidistant from points A and B", ha="center", fontsize=9)


@register("locus")
def drawer_locus(ax):
    """
    Locus example with explicit condition:
    A circle as the set of all points P such that PO = r (fixed distance r from O).
    """
    _setup_axes(ax)

    import math
    O = (0.0, 0.0)
    r = 0.72

    # Circle = { P : |PO| = r }
    theta = [math.radians(t) for t in range(0, 361, 2)]
    xs = [O[0] + r * math.cos(t) for t in theta]
    ys = [O[1] + r * math.sin(t) for t in theta]
    ax.plot(xs, ys)

    # Center and a sample point on the circle
    _draw_point(ax, O); ax.text(O[0], O[1]-0.14, "O", ha="center", fontsize=9)
    ang = math.radians(35)
    P = (O[0] + r * math.cos(ang), O[1] + r * math.sin(ang))
    _draw_point(ax, P); ax.text(P[0]+0.05, P[1]+0.05, "P", fontsize=9)

    # Radius segment (dashed) to show |PO| = r
    ax.plot([O[0], P[0]], [O[1], P[1]], linestyle="--")

    # Caption stating the condition
    ax.text(0.0, -0.98, "Condition: all points P with PO = r (fixed distance r from O)",
            ha="center", fontsize=9)


# -----------------------------------------------------------------------------
# Transformations / congruence
# -----------------------------------------------------------------------------
# --- Rigid transformation: show a rectangle and a rotated copy (distances/angles preserved) ---
@register("rigid_transformation")
def drawer_rigid_transformation(ax):
    """
    Rigid transformation via rotation.
    Left panel: triangles (original + rotated).
    Right panel: rectangles (original + rotated).
    Larger shapes, extra spacing, and no arrow overlay.
    """
    import math
    from matplotlib.patches import Polygon

    # Two wide panels side-by-side
    ax_tri  = ax.inset_axes([0.05, 0.10, 0.44, 0.80])  # left: triangles
    ax_rect = ax.inset_axes([0.51, 0.10, 0.44, 0.80])  # right: rectangles

    def _setup(panel): _setup_axes(panel)

    def rotated_rect_points(cx, cy, w, h, angle_deg):
        a = math.radians(angle_deg); ca, sa = math.cos(a), math.sin(a)
        pts = [(-w/2, -h/2), (w/2, -h/2), (w/2,  h/2), (-w/2,  h/2)]
        return [(cx + ca*x - sa*y, cy + sa*x + ca*y) for (x, y) in pts]

    def rotated_triangle_points(cx, cy, w, h, angle_deg):
        base = [(-w/2, -h/2), (w/2, -h/2), (0.0, h/2)]
        a = math.radians(angle_deg); ca, sa = math.cos(a), math.sin(a)
        return [(cx + ca*x - sa*y, cy + sa*x + ca*y) for (x, y) in base]

    # ---- Left: triangles (bigger, spaced; no overlay arrow) ----
    _setup(ax_tri)
    cxL, cxR, cy = -0.58, 0.58, 0.00
    wT, hT = 0.90, 0.75
    phi = 25
    T_left  = rotated_triangle_points(cxL, cy, wT, hT, 0)
    T_right = rotated_triangle_points(cxR, cy, wT, hT, phi)
    ax_tri.add_patch(Polygon(T_left,  closed=True, fill=False))
    ax_tri.add_patch(Polygon(T_right, closed=True, fill=False))

    # ---- Right: rectangles (more spacing so they don't touch; no overlay arrow) ----
    _setup(ax_rect)
    cxLr, cxRr, cyr = -0.64, 0.64, 0.00   # ↑ increased separation
    wR, hR = 0.90, 0.56                   # slightly smaller to avoid clipping when rotated
    theta = 30
    R_left  = rotated_rect_points(cxLr, cyr, wR, hR, 0)
    R_right = rotated_rect_points(cxRr, cyr, wR, hR, theta)
    ax_rect.add_patch(Polygon(R_left,  closed=True, fill=False))
    ax_rect.add_patch(Polygon(R_right, closed=True, fill=False))




@register("congruent_angles")
def drawer_congruent_angles(ax):
    _setup_axes(ax)
    # two separate equal angles
    # left
    _draw_ray(ax, 190); _draw_ray(ax, 240); _draw_arc(ax, 190, 240, 0.35, origin=(-0.4, -0.1))
    # right
    _draw_ray(ax, -10); _draw_ray(ax, 40); _draw_arc(ax, -10, 40, 0.35, origin=(0.4, 0.1))
    ax.text(0, -0.85, "equal measures", ha="center")

# --- Congruent figures: same rectangle, one rotated (can be mapped by a rigid transformation) ---
@register("congruent_figures")
def drawer_congruent_figures(ax):
    """
    Congruent figures: pairs have the same size & shape (one is a rotation of the other).
    Left panel: triangles A and B. Right panel: rectangles A and B.
    Larger shapes with extra spacing and no overlay arrow.
    """
    import math
    from matplotlib.patches import Polygon

    ax_tri  = ax.inset_axes([0.05, 0.10, 0.44, 0.80])  # left
    ax_rect = ax.inset_axes([0.51, 0.10, 0.44, 0.80])  # right

    def _setup(panel): _setup_axes(panel)

    def rotated_rect_points(cx, cy, w, h, angle_deg):
        a = math.radians(angle_deg); ca, sa = math.cos(a), math.sin(a)
        pts = [(-w/2, -h/2), (w/2, -h/2), (w/2,  h/2), (-w/2,  h/2)]
        return [(cx + ca*x - sa*y, cy + sa*x + ca*y) for (x, y) in pts]

    def rotated_triangle_points(cx, cy, w, h, angle_deg):
        base = [(-w/2, -h/2), (w/2, -h/2), (0.0, h/2)]
        a = math.radians(angle_deg); ca, sa = math.cos(a), math.sin(a)
        return [(cx + ca*x - sa*y, cy + sa*x + ca*y) for (x, y) in base]

    # ---- Left: triangles A, B (spaced) ----
    _setup(ax_tri)
    cxL, cxR, cy = -0.58, 0.58, 0.00
    wT, hT = 0.90, 0.75
    angT = 25
    A2 = rotated_triangle_points(cxL, cy, wT, hT, 0)
    B2 = rotated_triangle_points(cxR, cy, wT, hT, angT)
    ax_tri.add_patch(Polygon(A2, closed=True, fill=False))
    ax_tri.add_patch(Polygon(B2, closed=True, fill=False))
    ax_tri.text(cxL, cy - 0.78, "A", ha="center", fontsize=9)
    ax_tri.text(cxR, cy - 0.78, "B", ha="center", fontsize=9)

    # ---- Right: rectangles A, B (more spacing; smaller width to prevent touching) ----
    _setup(ax_rect)
    cxLr, cxRr, cyr = -0.64, 0.64, 0.00   # ↑ increased separation
    wR, hR = 0.90, 0.56
    angR = 30
    A = rotated_rect_points(cxLr, cyr, wR, hR, 0)
    B = rotated_rect_points(cxRr, cyr, wR, hR, angR)
    ax_rect.add_patch(Polygon(A, closed=True, fill=False))
    ax_rect.add_patch(Polygon(B, closed=True, fill=False))
    ax_rect.text(cxLr, cyr - 0.72, "A", ha="center", fontsize=9)
    ax_rect.text(cxRr, cyr - 0.72, "B", ha="center", fontsize=9)


# -----------------------------------------------------------------------------
# Construction / angle bisector
# -----------------------------------------------------------------------------
@register("midpoint_construction")
def drawer_midpoint_construction(ax):
    """
    Midpoint construction (compass + straightedge), monochrome.
    - linewidth=1 everywhere
    - smaller markers for A/B/P/Q
    - arcs pass through P and Q, shortened span
    - A,B labels moved down; P moved up+right; Q moved down+right
    - no '90°' text (square only)
    """
    import math
    from matplotlib.patches import Arc, Polygon

    _setup_axes(ax)
    ax.set_prop_cycle(color=["black"])  # monochrome

    # Tunables
    MS = 3              # marker size for points A,B,P,Q
    ARC_SPAN_DEG = 10   # shorter arcs as requested
    LABEL_DX = 0.045    # ~3/4 letter width (approx in these axis units)
    LABEL_DY = 0.13     # ~one letter height

    # --- Base segment AB ---
    A = (-1.0, 0.0)
    B = ( 1.0, 0.0)
    ax.plot([A[0], B[0]], [A[1], B[1]], linewidth=1, color="black")
    ax.plot([A[0], B[0]], [A[1], B[1]], marker="o", linestyle="", color="black", markersize=MS)
    # Move A/B labels further down
    ax.text(A[0], -0.30, "A", ha="center", fontsize=10)
    ax.text(B[0], -0.30, "B", ha="center", fontsize=10)

    # --- Midpoint ticks (AM = MB) ---
    mx = (A[0] + B[0]) / 2.0
    xL = (A[0] + mx) / 2.0
    xR = (mx + B[0]) / 2.0
    tick_h = 0.10
    ax.plot([xL, xL], [-tick_h/2,  tick_h/2], linewidth=1, color="black")
    ax.plot([xR, xR], [-tick_h/2,  tick_h/2], linewidth=1, color="black")

    # --- Compass arcs from A and B (same radius r > |AB|/2) ---
    half_len = (B[0] - A[0]) / 2.0  # = 1.0 here
    r = half_len * 1.12
    y_int = math.sqrt(max(r*r - half_len*half_len, 0.0))  # arc intersection height

    # Directions to P and Q from each center
    alpha = math.degrees(math.atan2(y_int, 1.0))  # from A -> P
    beta  = 180.0 - alpha                          # from B -> P
    span  = ARC_SPAN_DEG

    # A-centered arcs (through P and Q)
    ax.add_patch(Arc(A, 2*r, 2*r, angle=0,
                     theta1= alpha - span, theta2= alpha + span,
                     linewidth=1, edgecolor="black"))
    ax.add_patch(Arc(A, 2*r, 2*r, angle=0,
                     theta1=-alpha - span, theta2=-alpha + span,
                     linewidth=1, edgecolor="black"))

    # B-centered arcs (through P and Q)
    ax.add_patch(Arc(B, 2*r, 2*r, angle=0,
                     theta1= beta - span, theta2= beta + span,
                     linewidth=1, edgecolor="black"))
    ax.add_patch(Arc(B, 2*r, 2*r, angle=0,
                     theta1=-beta - span, theta2=-beta + span,
                     linewidth=1, edgecolor="black"))

    # --- Perpendicular bisector ---
    ax.plot([0, 0], [-1.2, 1.2], linewidth=1, color="black")

    # Right-angle square at the intersection (no text)
    s = 0.12
    ax.add_patch(Polygon([[0, 0], [s, 0], [s, s], [0, s]],
                         closed=False, fill=False, linewidth=1))

    # Intersection points P and Q (small markers)
    ax.plot([0, 0], [ y_int, -y_int], marker="o", linestyle="", color="black", markersize=MS)
    # Label P: move up by ~letter height and right by ~3/4 letter width
    ax.text(LABEL_DX,  y_int + LABEL_DY, "P", ha="left",  va="bottom", fontsize=10)
    # Label Q: move down and right
    ax.text(LABEL_DX, -y_int - LABEL_DY, "Q", ha="left",  va="top",    fontsize=10)



@register("angle_bisector")
def drawer_angle_bisector(ax):
    """
    Angle bisector with two non-touching interior arcs:
      - two rays form the angle
      - a bisector ray splits it evenly
      - two arcs at different radii, with small gaps at the rays and bisector
    """
    _setup_axes(ax)
    ax.set_prop_cycle(color=["black"])  # monochrome

    # Rays forming the angle (feel free to change 0° and 70°)
    a1, a2 = 0, 70
    bis = (a1 + a2) / 2

    # Draw the two rays and the bisector (all thin)
    _draw_ray(ax, a1)                # first side of the angle
    _draw_ray(ax, a2)                # second side
    _draw_ray(ax, bis)               # bisector

    # Arc settings
    gap_deg = 8      # gap from rays and bisector so arcs don't collide
    r1 = 0.52        # inner arc radius
    r2 = 0.68        # outer arc radius

    # Two arcs representing the equal angles (use different radii)
    # Left part: from a1 to bis
    _draw_arc(ax, a1 + gap_deg, bis - gap_deg, radius=r1)
    # Right part: from bis to a2
    _draw_arc(ax, bis + gap_deg, a2 - gap_deg, radius=r2)

