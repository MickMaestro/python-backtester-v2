"""Bottom axis that maps bar indices to timestamps."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pyqtgraph as pg


class TimeAxisItem(pg.AxisItem):
    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "bottom")
        super().__init__(**kwargs)
        self._times: np.ndarray | None = None
        self._intraday = True

    def set_times(self, times: np.ndarray) -> None:
        self._times = times
        if len(times) >= 2:
            seconds = np.diff(times).astype("timedelta64[s]").astype(float)
            self._intraday = float(np.median(seconds)) < 86_400
        self.picture = None
        self.update()

    def tickStrings(self, values, scale, spacing):
        times = self._times
        if times is None or len(times) == 0:
            return ["" for _ in values]
        labels = []
        for value in values:
            i = int(round(value))
            if i < 0 or i >= len(times):
                labels.append("")
                continue
            t = pd.Timestamp(times[i])
            if not self._intraday:
                labels.append(t.strftime("%Y-%m-%d"))
            elif spacing >= 30:  # ticks far apart: include the date
                labels.append(t.strftime("%d %b %H:%M"))
            else:
                labels.append(t.strftime("%H:%M"))
        return labels
