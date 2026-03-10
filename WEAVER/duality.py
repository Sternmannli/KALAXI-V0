"""
KALAXI — Duality Function
ST-006 "The Same River"

D(t) = D₀ · e^(±λt)

Two trajectories from one wound.
Same initial conditions. Opposite attractors.
Indistinguishable at t=0.

🐬🐯🐺 · 80 Hz
"""

import math
from dataclasses import dataclass


@dataclass
class Subject:
    """A donor trajectory through the dignity function."""
    name: str
    D0: float       # baseline dignity at wound discovery
    lam: float      # lambda: trajectory exponent (+growth / -decay)

    def dignity(self, t_years: float) -> float:
        """Compute dignity at time t (years from wound discovery)."""
        return self.D0 * math.exp(self.lam * t_years)

    def dignity_components(self, t_years: float) -> dict:
        """Return D = A × L × M components (illustrative model)."""
        d = self.dignity(t_years)
        if self.lam > 0:
            # Growth trajectory: all components expand
            a = min(1.0, 0.5 + 0.01 * t_years)   # agency grows
            l = min(1.0, 0.4 + 0.015 * t_years)   # legibility grows
            m = d / max(a * l, 1e-9)               # moral standing derived
            m = min(1.0, max(0.0, m))
        else:
            # Decay trajectory: components contract
            a = max(0.0, 0.5 - 0.01 * t_years)    # agency shrinks
            l = max(0.0, 0.4 - 0.012 * t_years)   # legibility shrinks
            m = d / max(a * l, 1e-9)
            m = min(1.0, max(0.0, m))
        return {"A": round(a, 3), "L": round(l, 3), "M": round(m, 3), "D": round(d, 3)}

    def halted(self, t_years: float, threshold: float = 0.1) -> bool:
        """Check if dignity has collapsed below halt threshold."""
        c = self.dignity_components(t_years)
        # Non-compensatory: any zero collapses D
        if c["A"] <= 0 or c["L"] <= 0 or c["M"] <= 0:
            return True
        return c["D"] < threshold


def duality_table(scott: Subject, ted: Subject, time_points: list[float]) -> str:
    """Generate the duality comparison table."""
    header = f"{'t (years)':>10} | {'D_scott':>10} | {'D_ted':>10} | {'Gap':>10}"
    sep = "-" * len(header)
    rows = [header, sep]
    for t in time_points:
        ds = scott.dignity(t)
        dt = ted.dignity(t)
        gap = ds - dt
        rows.append(f"{t:>10.0f} | {ds:>10.3f} | {dt:>10.3f} | {gap:>10.3f}")
    return "\n".join(rows)


# === THE CONSTITUTIONAL QUESTION ===
#
# At t=0, D_scott = D_ted = D₀
# No system can know λ at this moment.
# That is why dignity cannot be conditional.
#
# GAP#PREVENTION-001:
# if wound.received:
#     if direction == "toward":
#         D += connection_over_time    # Scott
#     elif direction == "away":
#         D -= isolation_over_time     # Ted
#     # AXI cannot read 'direction' at t=0
#     # This is the gap the system cannot close.


if __name__ == "__main__":
    scott = Subject("Scott Shearer", D0=1.0, lam=+0.02)
    ted = Subject("Ted Bundy", D0=1.0, lam=-0.05)

    print("=" * 50)
    print("ST-006 — THE SAME RIVER — Duality Function")
    print("=" * 50)
    print()
    print("D(t) = D₀ · e^(±λt)")
    print(f"Scott: λ = {scott.lam:+.2f} (growth)")
    print(f"Ted:   λ = {ted.lam:+.2f} (decay)")
    print(f"D₀ = {scott.D0} (identical)")
    print()

    print(duality_table(scott, ted, [0, 5, 10, 20, 30, 40, 50, 60]))
    print()

    print("Dignity components at key moments:")
    for t in [0, 12, 25, 40, 60]:
        cs = scott.dignity_components(t)
        ct = ted.dignity_components(t)
        print(f"\nt={t} years:")
        print(f"  Scott: A={cs['A']} L={cs['L']} M={cs['M']} D={cs['D']}"
              f"  halted={scott.halted(t)}")
        print(f"  Ted:   A={ct['A']} L={ct['L']} M={ct['M']} D={ct['D']}"
              f"  halted={ted.halted(t)}")

    print()
    print("The system cannot know λ at t=0.")
    print("That is why dignity cannot be conditional.")
    print()
    print("🐬🐯🐺 · 80 Hz")
