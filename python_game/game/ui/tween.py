"""
game/ui/tween.py
Lightweight tween manager for animating any numeric attribute over time.
Used by HUD, menus, boon cards, boss intros, and death sequences.
"""
from game.ui.easing import ease_out_cubic, lerp, clamp


class Tween:
    """Animate a single attribute on a target object from start → end."""
    __slots__ = ("_target", "_attr", "start", "end", "duration",
                 "elapsed", "ease", "on_done", "delay", "_started")

    def __init__(self, target, attr: str, end: float, duration: float,
                 ease=ease_out_cubic, on_done=None, delay: float = 0.0,
                 start=None):
        self._target = target
        self._attr = attr
        self.start = start if start is not None else getattr(target, attr, 0.0)
        self.end = end
        self.duration = max(0.001, duration)
        self.elapsed = 0.0
        self.ease = ease
        self.on_done = on_done
        self.delay = delay
        self._started = delay <= 0

    @property
    def done(self) -> bool:
        return self._started and self.elapsed >= self.duration

    @property
    def progress(self) -> float:
        if not self._started:
            return 0.0
        return clamp(self.elapsed / self.duration)

    def update(self, dt: float) -> None:
        if not self._started:
            self.delay -= dt
            if self.delay <= 0:
                self._started = True
                # Re-read start value at the moment the tween actually begins
                if self.start is None:
                    self.start = getattr(self._target, self._attr, 0.0)
            else:
                return

        self.elapsed += dt
        t = clamp(self.elapsed / self.duration)
        eased = self.ease(t)
        val = lerp(self.start, self.end, eased)
        setattr(self._target, self._attr, val)

        if t >= 1.0 and self.on_done:
            cb = self.on_done
            self.on_done = None  # prevent double-fire
            cb()


class TweenSequence:
    """Run a list of tweens one after another on the same target."""
    __slots__ = ("tweens", "_index")

    def __init__(self, tweens: list):
        self.tweens = tweens
        self._index = 0

    @property
    def done(self) -> bool:
        return self._index >= len(self.tweens)

    def update(self, dt: float) -> None:
        if self.done:
            return
        tw = self.tweens[self._index]
        tw.update(dt)
        if tw.done:
            self._index += 1


class TweenManager:
    """Manages a pool of active tweens, automatically pruning completed ones."""
    def __init__(self):
        self.tweens: list = []

    def add(self, tween) -> None:
        """Add a Tween or TweenSequence."""
        self.tweens.append(tween)
        return tween

    def tween(self, target, attr: str, end: float, duration: float,
              ease=ease_out_cubic, on_done=None, delay: float = 0.0,
              start=None):
        """Convenience: create and add a Tween in one call."""
        t = Tween(target, attr, end, duration, ease=ease, on_done=on_done,
                  delay=delay, start=start)
        self.tweens.append(t)
        return t

    def cancel_all(self) -> None:
        self.tweens.clear()

    def update(self, dt: float) -> None:
        for t in self.tweens:
            t.update(dt)
        self.tweens = [t for t in self.tweens if not t.done]

    @property
    def active(self) -> bool:
        return len(self.tweens) > 0
