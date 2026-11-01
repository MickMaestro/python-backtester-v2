"""AMA_STL_Color — converted from MQL5: MQL5 Indicators/AMA STL Color MetaTrader 5/AMA_STL_Color.mq5

Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [4678655]}, 'widths': {1: 3, 2: 3}, 'styles': {}, 'labels': {1: 'Up Line', 2: 'Dn Line'}, 'levels': [], 'description': [], 'name': 'AMA_STL_Color', 'source': 'MQL5 Indicators/AMA STL Color MetaTrader 5/AMA_STL_Color.mq5', 'folder': 'AMA STL Color MetaTrader 5', 'inputs': [{'mql': 'InpRange', 'py': 'InpRange', 'param': 'InpRange', 'type': 'uint', 'default': 9, 'label': 'Range', 'sinput': False}, {'mql': 'InpFastPeriod', 'py': 'InpFastPeriod', 'param': 'InpFastPeriod', 'type': 'uint', 'default': 2, 'label': 'Fast Period', 'sinput': False}, {'mql': 'InpSlowPeriod', 'py': 'InpSlowPeriod', 'param': 'InpSlowPeriod', 'type': 'uint', 'default': 30, 'label': 'Slow Period', 'sinput': False}, {'mql': 'InpMaxBars', 'py': 'InpMaxBars', 'param': 'InpMaxBars', 'type': 'uint', 'default': 200, 'label': 'Count Bars', 'sinput': False}, {'mql': 'InpFilter', 'py': 'InpFilter', 'param': 'InpFilter', 'type': 'uint', 'default': 25, 'label': 'Filter', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpRange = _input('InpRange', 9)  # Range
InpFastPeriod = _input('InpFastPeriod', 2)  # Fast Period
InpSlowPeriod = _input('InpSlowPeriod', 30)  # Slow Period
InpMaxBars = _input('InpMaxBars', 200)  # Count Bars
InpFilter = _input('InpFilter', 25)  # Filter
Up = Arr(0, 0.0)
Down = Arr(0, 0.0)
trend = Arr(0, 0.0)
fAMA = Arr(0, 0.0)
mAMA = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, Up, INDICATOR_DATA)
    SetIndexBuffer(1, Down, INDICATOR_DATA)
    SetIndexBuffer(2, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, fAMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, mAMA, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Up, True)
    ArraySetAsSeries(Down, True)
    ArraySetAsSeries(trend, True)
    ArraySetAsSeries(fAMA, True)
    ArraySetAsSeries(mAMA, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    limit = 0
    if prev_calculated == 0:
        limit = rates_total - _int(InpRange) - 2
        if InpMaxBars > 0:
            limit = _int(fmin(limit, InpMaxBars))
        ArrayInitialize(Up, EMPTY_VALUE)
        ArrayInitialize(Down, EMPTY_VALUE)
    else:
        limit = rates_total - prev_calculated
    k1 = 2.0 / (InpSlowPeriod + 1)
    k2 = (2.0 / (InpFastPeriod + 1)) - k1
    AMA = close[InpMaxBars - InpRange]
    mAMA[InpMaxBars - InpRange] = close[InpMaxBars - InpRange + 1]
    for cb in range(_int(InpMaxBars), 0 - 1, -1):
        Noise = 0.0
        for i in range(cb, cb + _int(InpRange)):
            Noise += fabs(close[i] - close[i + 1])
        ER = 0.0
        if Noise != 0.0:
            ER = _fdiv(fabs(close[cb] - close[cb + InpRange]), Noise)
        SSC = (ER * k2) + k1
        AMA += NormalizeDouble(SSC * SSC * (close[cb] - AMA), Digits())
        mAMA[cb] = AMA
        if InpFilter < 1:
            fAMA[cb] = mAMA[cb]
        else:
            sdAMA = 0.0
            for i in range(cb, cb + _int(InpSlowPeriod)):
                sdAMA += fabs(mAMA[i] - mAMA[i + 1])
            dAMA = mAMA[cb] - mAMA[cb + 1]
            if dAMA >= 0.0:
                if dAMA < NormalizeDouble((InpFilter * sdAMA) / (100 * InpSlowPeriod), Digits()) and high[cb] <= (high[ArrayMaximum(high, 4, cb)] + (10 * Point())):
                    fAMA[cb] = fAMA[cb + 1]
                else:
                    fAMA[cb] = mAMA[cb]
            else:
                if fabs(dAMA) < NormalizeDouble((InpFilter * sdAMA) / (100 * InpSlowPeriod), Digits()) and low[cb] > (low[ArrayMinimum(low, 4, cb)] - (10 * Point())):
                    fAMA[cb] = fAMA[cb + 1]
                else:
                    fAMA[cb] = mAMA[cb]
            sdAMA = 0.0
    for i in range(_int(InpMaxBars), 0 - 1, -1):
        trend[i] = trend[i + 1]
        if fAMA[i] > fAMA[i + 1]:
            trend[i] = 1.0
        if fAMA[i] < fAMA[i + 1]:
            trend[i] = -1.0
        if trend[i] > 0:
            Up[i] = fAMA[i]
            if trend[i + 1] < 0:
                Up[i + 1] = fAMA[i + 1]
            Down[i] = EMPTY_VALUE
        elif trend[i] < 0:
            Down[i] = fAMA[i]
            if trend[i + 1] > 0:
                Down[i + 1] = fAMA[i + 1]
            Up[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AMASTLColor(_MQL5Indicator):
    name = 'AMA_STL_Color'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpRange': 9,  # Range
        'InpFastPeriod': 2,  # Fast Period
        'InpSlowPeriod': 30,  # Slow Period
        'InpMaxBars': 200,  # Count Bars
        'InpFilter': 25,  # Filter
    }

