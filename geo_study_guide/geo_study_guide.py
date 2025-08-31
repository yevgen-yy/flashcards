"""
geo_study_guide.py — build a geometry study guide PDF (3 cards per page)

Requires:
  - matplotlib
  - geo_study_guide_cards.py  (exports: DEFINITIONS [Card...])
  - geo_study_guide_illustrations.py (exports: resolve_drawer)

Run:
    python geo_study_guide.py
Output:
    geometry_study_guide.pdf
"""

import textwrap
from typing import Any, Optional

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from geo_study_guide_cards import DEFINITIONS   # list of Card dataclass instances (or dicts)
from geo_study_guide_illustrations import resolve_drawer

# ---------------- Layout config ----------------
WRAP_WIDTH = 78
PDF_NAME = "geometry_study_guide.pdf"


# ---------------- Small helpers ----------------
def _get(card: Any, key: str, default: Optional[str] = "") -> Any:
    """Access dataclass attribute or dict field uniformly."""
    if hasattr(card, key):
        return getattr(card, key)
    if isinstance(card, dict):
        return card.get(key, default)
    return default


def paginate(items, n):
    for i in range(0, len(items), n):
        yield items[i:i+n]


# ---------------- Drawing ----------------
def draw_card(ax, term: str, description: str, drawer_key: Optional[str], notes: Optional[str] = None):
    ax.set_axis_off()

    drawer_fn = resolve_drawer(drawer_key)

    # Combine description and notes if notes are present
    wrapper = textwrap.TextWrapper(width=WRAP_WIDTH)
    body_lines = wrapper.wrap(description or "")
    if notes:
        body_lines.append("")  # empty line before notes
        for line in notes.strip().splitlines():
            body_lines.extend(wrapper.wrap(line))

    if drawer_fn is not None:
        # Text on top, diagram below
        tbox = ax.inset_axes([0.05, 0.58, 0.90, 0.37])
        dbox = ax.inset_axes([0.05, 0.08, 0.90, 0.42])

        tbox.set_axis_off()
        tbox.text(0, 1.0, term, fontsize=14, fontweight="bold", va="top")
        tbox.text(0, 0.70, "\n".join(body_lines), fontsize=11, va="top")

        drawer_fn(dbox)
    else:
        # Text only
        tbox = ax.inset_axes([0.05, 0.10, 0.90, 0.80])
        tbox.set_axis_off()
        tbox.text(0, 1.0, term, fontsize=14, fontweight="bold", va="top")
        tbox.text(0, 0.85, "\n".join(body_lines), fontsize=11, va="top")


def build_pdf(cards, out_path=PDF_NAME):
    with PdfPages(out_path) as pdf:
        # Cover
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis("off")
        ax.text(0.5, 0.70, "Geometry Basics", fontsize=22, ha="center")
        ax.text(0.5, 0.62, "Study Guide — 3 cards per page", fontsize=13, ha="center")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # Pages of cards
        for chunk in paginate(cards, 3):
            fig = plt.figure(figsize=(8.5, 11))
            gs = fig.add_gridspec(3, 1, left=0.06, right=0.94, top=0.95, bottom=0.06, hspace=0.35)
            for i, card in enumerate(chunk):
                ax = fig.add_subplot(gs[i, 0])
                term = _get(card, "term")
                desc = _get(card, "description")
                notes = _get(card, "notes")
                drawer_key = _get(card, "drawer", None)
                draw_card(ax, term, desc, drawer_key, notes)
            pdf.savefig(fig)
            plt.close(fig)

    return out_path


if __name__ == "__main__":
    print("Generated:", build_pdf(DEFINITIONS))
