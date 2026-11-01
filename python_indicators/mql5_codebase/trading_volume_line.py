"""Trading Volume Line — converted from MQL5: MQL5 Indicators/Trading Volume Line/Trading Volume Line.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16760576], 2: [5275647]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bulls', 2: 'Bears'}, 'levels': [50.0], 'description': [], 'name': 'Trading Volume Line', 'source': 'MQL5 Indicators/Trading Volume Line/Trading Volume Line.mq5', 'folder': 'Trading Volume Line', 'inputs': [{'mql': 'InpRatio', 'py': 'InpRatio', 'param': 'InpRatio', 'type': 'int', 'default': 0, 'label': 'Ratio type:', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_RATIO
ratio_close = 0
ratio_open = 1
ratio_body = 2
_enum('ENUM_RATIO', {0: 'ratio_close', 1: 'ratio_open', 2: 'ratio_body'})

# ---- inputs and global variables
InpRatio = _input('InpRatio', ratio_close)  # Ratio type:
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    str_ratio = '-'
    _sw1 = InpRatio
    if _sw1 == ratio_close:
        str_ratio = 'Close'
    elif _sw1 == ratio_open:
        str_ratio = 'Open'
    else:
        str_ratio = 'Body'
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trading Volume Line(' + str_ratio + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        _sw2 = InpRatio
        if _sw2 == ratio_close:
            BidRatio = 0.0
            PairH = high[i]
            PairL = low[i]
            PairB = close[i]
            PRange = (PairH - PairL) * Point()
            if PRange > 0:
                BidRatio = _fdiv(PairB - PairL, PairH - PairL)
            BullsBuffer[i] = BidRatio * 100.0
            BearsBuffer[i] = (1.0 - BidRatio) * 100.0
        elif _sw2 == ratio_open:
            BidRatio = 0.0
            PairH = high[i]
            PairL = low[i]
            PairB = open[i]
            PRange = (PairH - PairL) * Point()
            if PRange > 0:
                BidRatio = _fdiv(PairH - PairB, PairH - PairL)
            BullsBuffer[i] = BidRatio * 100.0
            BearsBuffer[i] = (1.0 - BidRatio) * 100.0
        else:
            Percent = 0.0
            Bulls = 0.0
            Bears = 0.0
            Length0 = high[i] - low[i]
            Body0 = MathAbs(open[i] - close[i])
            if Length0 > 0:
                Percent = _fdiv(Body0, Length0)
            Remain = 1.0 - Percent
            if open[i] > close[i]:
                BullsBuffer[i] = (Remain / 2.0) * 100.0
                BearsBuffer[i] = (Percent + (Remain / 2.0)) * 100.0
            else:
                BearsBuffer[i] = (Remain / 2.0) * 100.0
                BullsBuffer[i] = (Percent + (Remain / 2.0)) * 100.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradingVolumeLine(_MQL5Indicator):
    name = 'Trading Volume Line'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpRatio': _Choice({0: 'Close Ratio', 1: 'Open Ratio', 2: 'Body Ratio'}, default=0),  # Ratio type:
    }
    y_range = (0.0, 100.0)

