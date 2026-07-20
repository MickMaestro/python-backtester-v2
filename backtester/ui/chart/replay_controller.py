"""Drives a backtest's event stream on a timer for the visual replay.

One "bar step" pulls events from ``Backtester.run()`` up to and including the
bar's terminating ``EquityEvent``. A QTimer ticks ~30x/sec and advances
``speed`` bars per second (fractional speeds accumulate); every tick emits a
single ``events_batch`` so the chart repaints once regardless of how many
bars advanced.
"""

from __future__ import annotations

from PySide6.QtCore import QObject, QTimer, Signal

from backtester.engine.backtester import Backtester
from backtester.engine.events import EquityEvent

TICK_MS = 33


class ReplayController(QObject):
    events_batch = Signal(list)
    progress = Signal(int, int)          # bars done, total
    finished = Signal(object)            # BacktestResult
    state_changed = Signal(bool)         # playing?

    def __init__(self, backtester: Backtester, parent: QObject | None = None):
        super().__init__(parent)
        self._bt = backtester
        self._gen = backtester.run()
        self._total = len(backtester.df)
        self._bars_done = 0
        self._carry = 0.0
        self._speed = 10.0               # bars per second
        self._done = False
        self._finished_sent = False
        self._timer = QTimer(self)
        self._timer.setInterval(TICK_MS)
        self._timer.timeout.connect(self._on_tick)

    # ------------------------------------------------------------ controls

    def play(self) -> None:
        if not self._done and not self._timer.isActive():
            self._timer.start()
            self.state_changed.emit(True)

    def pause(self) -> None:
        if self._timer.isActive():
            self._timer.stop()
            self.state_changed.emit(False)

    def toggle(self) -> None:
        if self._timer.isActive():
            self.pause()
        else:
            self.play()

    def step(self) -> None:
        """Advance exactly one bar (usable while paused)."""
        self._advance(1)

    def advance(self, bars: int) -> None:
        """Advance ``bars`` bars immediately, in one batch (e.g. replay warm-up)."""
        if bars > 0:
            self._advance(bars)

    def fast_forward(self) -> None:
        """Finish the rest of the run without animation."""
        self.pause()
        # The stream has one terminal chunk beyond the last bar (end-of-data
        # closes), so drain until the generator is truly exhausted.
        while not self._done:
            self._advance(max(1, self._total))

    def set_speed(self, bars_per_second: float) -> None:
        self._speed = max(0.1, float(bars_per_second))

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def playing(self) -> bool:
        return self._timer.isActive()

    @property
    def done(self) -> bool:
        return self._done

    @property
    def bars_done(self) -> int:
        return self._bars_done

    @property
    def total_bars(self) -> int:
        return self._total

    # ------------------------------------------------------------- driving

    def _on_tick(self) -> None:
        self._carry += self._speed * self._timer.interval() / 1000.0
        bars = int(self._carry)
        if bars >= 1:
            self._carry -= bars
            self._advance(bars)

    def _advance(self, bars: int) -> None:
        if self._done:
            return
        events: list = []
        for _ in range(bars):
            bar_events, ended = self._next_bar()
            events.extend(bar_events)
            if ended:
                break
        if events:
            self.events_batch.emit(events)
        self.progress.emit(self._bars_done, self._total)
        if self._done and not self._finished_sent:
            self._finished_sent = True
            self.pause()
            self.finished.emit(self._bt.result())

    def _next_bar(self) -> tuple[list, bool]:
        """Events up to the next bar boundary; (events, stream_ended)."""
        events: list = []
        for event in self._gen:
            events.append(event)
            if isinstance(event, EquityEvent):
                self._bars_done = event.index + 1
                return events, False
        self._done = True
        return events, True
