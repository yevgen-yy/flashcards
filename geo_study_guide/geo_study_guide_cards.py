# geo_study_guide_cards.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Card:
    term: str
    description: str
    drawer: Optional[str] = None   # plain-text reference to an illustration function
    notes: Optional[str] = None    # optional extra explanation/examples

# The cards below are rendered in order by geo_study_guide.py
DEFINITIONS: List[Card] = [
    # ---------------- Reasoning / Logic (top cards) ----------------
    Card(
        term="Axiom (postulate)",
        description="A statement accepted as true without proof; used as a starting point for logical reasoning in geometry.",
        notes="Example: 'Through any two (distinct) points, there is exactly one line.'"
    ),
    Card(
        term="Theorem",
        description="A statement that has been proven true using axioms, definitions, and previously established theorems.",
        notes=(
            "Example: The sum of the interior angles of any triangle is 180°.\n"
            "This can be proven using parallel lines and alternate interior angles."
        )
    ),
    Card(
        term="Conjecture",
        description="An unproven statement believed to be true based on observations or patterns; requires proof or a counterexample.",
        notes=(
            "Consider the expression f(n) = n² + n + 41.\n"
            "For n = 0, 1, 2, ..., 10, the values of f(n) are:\n"
            "41, 43, 47, 53, 61, 71, 83, 97, 113, 131, 151 — all prime numbers.\n"
            "This leads to the conjecture:\nf(n) is a prime number for every natural number n.\n"
            "This is a conjecture until someone proves or disproves it.\n"
            "Try to prove or disprove this conjecture — without using AI or Google search!"
        )
    ),
    # ---------------- Foundations ----------------
    Card(
        term="Point",
        description="An undefined term representing an exact location in space; has no length, width, or thickness."
        # no drawer (simple)
    ),
    Card(
        term="Line",
        description="An undefined term: a straight path extending infinitely in both directions with no thickness.",
        drawer="line"
    ),
    Card(
        term="Plane",
        description="An undefined term: a flat surface extending infinitely in all directions."
    ),
    Card(
        term="Space",
        description="The three-dimensional setting in which geometric objects exist."
    ),
    Card(
        term="Finite plane",
        description="A bounded portion of a plane; for example, the interior region enclosed by a polygon or a circle.",
        drawer="finite_plane"
    ),

    # ---------------- Incidence relations ----------------
    Card(
        term="Collinear points",
        description="Points that lie on the same line.",
        drawer="collinear"
    ),
    Card(
        term="Coplanar points (or lines)",
        description="Points or lines that lie in the same plane.",
        drawer="coplanar"
    ),

    # ---------------- Segments / Rays ----------------
    Card(
        term="Segment",
        description="A part of a line bounded by two distinct endpoints.",
        drawer="segment"
    ),
    Card(
        term="Midpoint",
        description="The point on a segment that is equidistant from both endpoints.",
        drawer="midpoint"
    ),
    Card(
        term="Segment bisector",
        description="A line, ray, or segment that passes through the midpoint of a segment, dividing it into two equal parts.",
        drawer="segment_bisector"
    ),
    Card(
        term="Ray",
        description="A part of a line that starts at an endpoint (origin) and extends infinitely in one direction.",
        drawer="ray"
    ),
    Card(
        term="Origin of a ray",
        description="The common endpoint from which a ray begins.",
        drawer="origin_of_ray"
    ),
    Card(
        term="Opposite rays",
        description="Two rays with the same origin that lie on the same line but extend in opposite directions.",
        drawer="opposite_rays"
    ),
    Card(
        term="Betweenness of points",
        description="For distinct collinear points A, B, and C, point B is between A and C iff AB + BC = AC.",
        drawer="betweenness"
    ),

    # ---------------- Angle basics ----------------
    Card(
        term="Angle",
        description="A figure formed by two rays (sides) sharing a common endpoint (the vertex).",
        drawer="angle"
    ),
    Card(
        term="Interior and exterior of an angle",
        description="The plane regions defined by an angle: the interior lies between the sides; the exterior is outside that region.",
        drawer="angle_regions"
    ),
    Card(
        term="Degree measure of an angle",
        description="A measure of rotation based on dividing a full turn into 360 equal parts (degrees).",
        drawer="degree_measure_image"
    ),

    # ---------------- Angle types ----------------
    Card(
        term="Acute angle",
        description="An angle whose measure is less than 90°.",
        drawer="acute_angle"
    ),
    Card(
        term="Right angle",
        description="An angle whose measure is exactly 90°.",
        drawer="right_angle"
    ),
    Card(
        term="Obtuse angle",
        description="An angle whose measure is greater than 90° but less than 180°.",
        drawer="obtuse_angle"
    ),
    Card(
        term="Straight angle",
        description="An angle whose measure is exactly 180°.",
        drawer="straight_angle"
    ),
    Card(
        term="Reflex angle",
        description="An angle whose measure is greater than 180° and less than 360°.",
        drawer="reflex_angle"
    ),
    Card(
        term="Full angle (complete angle)",
        description="An angle equal to a full turn (360°).",
        drawer="full_angle"
    ),

    # ---------------- Angle relationships ----------------
    Card(
        term="Complementary angles",
        description="Two angles whose measures add to 90°.",
        drawer="complementary"
    ),
    Card(
        term="Supplementary angles",
        description="Two angles whose measures add to 180°.",
        drawer="supplementary"
    ),
    Card(
        term="Vertical angles",
        description="A pair of nonadjacent angles formed by two intersecting lines; they are congruent.",
        drawer="vertical_angles"
    ),

    # ---------------- Parallel & Perpendicular / Transversals ----------------
    Card(
        term="Perpendicular lines",
        description="Lines that intersect to form right angles.",
        drawer="perpendicular_lines"
    ),
    Card(
        term="Parallel Lines with Transversal",
        description="Two parallel lines cut by a third line (a transversal), creating special angle pairs (corresponding, alternate interior, etc.).",
        drawer="parallel_with_transversal"
    ),

    # ---------------- Concurrency / Intersection ----------------
    Card(
        term="Intersection",
        description="The set of points common to two or more geometric objects (e.g., lines, segments, or planes).",
        drawer="intersection"
    ),
    Card(
        term="Concurrent lines",
        description="Three or more lines that intersect at a single point.",
        drawer="concurrent_lines"
    ),

    # ---------------- Distance / Locus ----------------
    Card(
        term="Equidistant",
        description="At the same distance from two or more objects or points.",
        drawer="equidistant"
    ),
    Card(
        term="Locus",
        description="The set of all points that satisfy a given condition or rule.",
        drawer="locus"
    ),

    # ---------------- Transformations BEFORE congruence ----------------
    Card(
        term="Rigid transformation",
        description="A transformation (translation, rotation, reflection) that preserves distances and angle measures.",
        drawer="rigid_transformation"
    ),
    Card(
        term="Congruent angles",
        description="Angles that have equal measure.",
        drawer="congruent_angles"
    ),
    Card(
        term="Congruent figures",
        description="Figures that are the same size and shape; one can be mapped to the other by a rigid transformation.",
        drawer="congruent_figures"
    ),

    # ---------------- Construction & final skill ----------------
    Card(
        term="Construction",
        description="A precise drawing made using only allowed tools (typically compass and straightedge).",
        drawer="midpoint_construction"
    ),
    Card(
        term="Angle bisector",
        description="A ray or segment that divides an angle into two congruent angles.",
        drawer="angle_bisector"
    ),

Card(
    term="Euclidean axioms (Pogorelov–Hilbert system)",
    description="A modern, formal set of axioms for Euclidean geometry as presented by A.V. Pogorelov. This system was inspired by Hilbert's work.",
    notes=(
        "• Axioms of Incidence:\n"
        "  1. Through any two distinct points, there exists exactly one line.\n"
        "  2. Every line contains at least two points.\n"
        "  3. There exist at least three non-collinear points.\n"
        "\n"
        "• Axioms of Order:\n"
        "  4. If point B lies between A and C, then A, B, C are distinct and collinear, and B lies between C and A.\n"
        "  5. Of any three collinear points, one and only one lies between the other two.\n"
        "\n"
        "• Axioms of Congruence:\n"
        "  6. Every segment is congruent to itself.\n"
        "  7. If AB ≅ CD and CD ≅ EF, then AB ≅ EF (transitivity).\n"
        "  8. Congruent segments and angles can be copied from one location to another.\n"
        "\n"
        "• Axiom of Parallelism:\n"
        "  9. Through any point not on a given line, there is exactly one line parallel to the given line.\n"
    ))
]
