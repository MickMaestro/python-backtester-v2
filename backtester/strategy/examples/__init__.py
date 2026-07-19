"""Built-in example strategies, keyed by CLI/GUI name."""

from .ma_cross import MaCross
from .rsi_reversion import RsiReversion

STRATEGIES = {
    "ma_cross": MaCross,
    "rsi_reversion": RsiReversion,
}
