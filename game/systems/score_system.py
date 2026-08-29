"""
game/systems/score_system.py
Score tracking with combo multiplier.
Kills within COMBO_WINDOW seconds of each other chain the multiplier.
"""
from constants import COMBO_WINDOW, MAX_COMBO


class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.combo = 1          # current multiplier
        self._combo_timer = 0.0  # counts down; reset on each kill
        self.highest_combo = 1

    def register_kill(self, base_score: int) -> int:
        """
        Call when an enemy dies. Returns the actual points awarded.
        """
        if self._combo_timer > 0:
            # Chain! Increment combo (cap at MAX_COMBO)
            self.combo = min(self.combo + 1, MAX_COMBO)
        else:
            # Reset to x1 for the first kill after a gap
            self.combo = 1

        self._combo_timer = COMBO_WINDOW
        self.highest_combo = max(self.highest_combo, self.combo)

        earned = base_score * self.combo
        self.score += earned
        return earned

    def update(self, delta_time: float) -> None:
        if self._combo_timer > 0:
            self._combo_timer -= delta_time
            if self._combo_timer <= 0:
                self._combo_timer = 0
                self.combo = 1   # combo expired

    @property
    def combo_active(self) -> bool:
        return self.combo > 1

    @property
    def combo_timer(self) -> float:
        return self._combo_timer

    @property
    def combo_timeout(self) -> float:
        return COMBO_WINDOW
