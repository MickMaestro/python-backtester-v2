"""PTL (2) — converted from MQL5: MQL5 Indicators/Perfect Trend Line 2/PTL (2).mq5

Perfect trend line
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 17, 2: 1, 3: 1, 4: 12}, 'colors': {1: [16748574, 3937500], 2: [16748574], 3: [3937500], 4: [16748574, 3937500]}, 'widths': {4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'PTL trend candles', 2: 'PTL slow line', 3: 'PTL fast line', 4: 'PTL trend start'}, 'levels': [], 'description': ['Perfect trend line'], 'name': 'PTL (2)', 'source': 'MQL5 Indicators/Perfect Trend Line 2/PTL (2).mq5', 'folder': 'Perfect Trend Line 2', 'inputs': [{'mql': 'inpFastLength', 'py': 'inpFastLength', 'param': 'inpFastLength', 'type': 'int', 'default': 3, 'label': 'Fast length', 'sinput': False}, {'mql': 'inpSlowLength', 'py': 'inpSlowLength', 'param': 'inpSlowLength', 'type': 'int', 'default': 7, 'label': 'Slow length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastLength = _input('inpFastLength', 3)  # Fast length
inpSlowLength = _input('inpSlowLength', 7)  # Slow length
slowlu = Arr(0, 0.0)
slowln = Arr(0, 0.0)
fastln = Arr(0, 0.0)
arrowar = Arr(0, 0.0)
arrowcl = Arr(0, 0.0)
candleo = Arr(0, 0.0)
candleh = Arr(0, 0.0)
candlel = Arr(0, 0.0)
candlec = Arr(0, 0.0)
candleC = Arr(0, 0.0)
_fastPeriod = 0
_slowPeriod = 0

class sPtlStruct(MqlObject):
    _q_fields = ('time', 'fastHigh', 'fastLow', 'slowHigh', 'slowLow', 'trend', 'trena')
    def __init__(self, *args):
        self.time = 0
        self.fastHigh = 0.0
        self.fastLow = 0.0
        self.slowHigh = 0.0
        self.slowLow = 0.0
        self.trend = 0
        self.trena = 0

def OnInit():
    global _fastPeriod, _slowPeriod
    SetIndexBuffer(0, candleo, INDICATOR_DATA)
    SetIndexBuffer(1, candleh, INDICATOR_DATA)
    SetIndexBuffer(2, candlel, INDICATOR_DATA)
    SetIndexBuffer(3, candlec, INDICATOR_DATA)
    SetIndexBuffer(4, candleC, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, slowln, INDICATOR_DATA)
    SetIndexBuffer(6, fastln, INDICATOR_DATA)
    SetIndexBuffer(7, arrowar, INDICATOR_DATA)
    SetIndexBuffer(8, arrowcl, INDICATOR_COLOR_INDEX)
    _fastPeriod = MathMax(MathMin(inpFastLength, inpSlowLength), 1)
    _slowPeriod = MathMax(MathMax(inpFastLength, inpSlowLength), 1)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    if _s_OnCalculate_m_arraySize < rates_total:
        _s_OnCalculate_m_arraySize = ArrayResize(_s_OnCalculate_m_array, rates_total + 500, 2000)
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if _s_OnCalculate_m_array[i].time != time[i]:
            _s_OnCalculate_m_array[i].time = time[i]
            _startf = i - _fastPeriod + 1
            if _startf < 0:
                _startf = 0
            _starts = i - _slowPeriod + 1
            if _starts < 0:
                _starts = 0
            if i < (rates_total - 1):
                _s_OnCalculate_m_array[i + 1].time = 0
            _s_OnCalculate_m_array[i].fastHigh = high[ArrayMaximum(high, _startf, _fastPeriod - 1)]
            _s_OnCalculate_m_array[i].fastLow = low[ArrayMinimum(low, _startf, _fastPeriod - 1)]
            _s_OnCalculate_m_array[i].slowHigh = high[ArrayMaximum(high, _starts, _slowPeriod - 1)]
            _s_OnCalculate_m_array[i].slowLow = low[ArrayMinimum(low, _starts, _slowPeriod - 1)]
        thighs = (_s_OnCalculate_m_array[i].slowHigh if (high[i] < _s_OnCalculate_m_array[i].slowHigh) else high[i])
        tlows = (_s_OnCalculate_m_array[i].slowLow if (low[i] > _s_OnCalculate_m_array[i].slowLow) else low[i])
        thighf = (_s_OnCalculate_m_array[i].fastHigh if (high[i] < _s_OnCalculate_m_array[i].fastHigh) else high[i])
        tlowf = (_s_OnCalculate_m_array[i].fastLow if (low[i] > _s_OnCalculate_m_array[i].fastLow) else low[i])
        _s_OnCalculate_m_array[i].trend = -1
        if i > 0:
            _s_OnCalculate_m_array[i].trena = _s_OnCalculate_m_array[i - 1].trena
            slowln[i] = (tlows if (close[i] > slowln[i - 1]) else thighs)
            fastln[i] = (tlowf if (close[i] > fastln[i - 1]) else thighf)
            if close[i] < slowln[i] and close[i] < fastln[i]:
                _s_OnCalculate_m_array[i].trend = 1
            if close[i] > slowln[i] and close[i] > fastln[i]:
                _s_OnCalculate_m_array[i].trend = 0
            if slowln[i] > fastln[i] or _s_OnCalculate_m_array[i].trend == 1:
                _s_OnCalculate_m_array[i].trena = 1
            if slowln[i] < fastln[i] or _s_OnCalculate_m_array[i].trend == 0:
                _s_OnCalculate_m_array[i].trena = 0
            arrowar[i] = ((MathMax(fastln[i], slowln[i]) if (_s_OnCalculate_m_array[i].trena == 1) else MathMin(fastln[i], slowln[i])) if (_s_OnCalculate_m_array[i].trena != _s_OnCalculate_m_array[i - 1].trena) else EMPTY_VALUE)
        else:
            arrowcl[i] = 0.0
            arrowar[i] = EMPTY_VALUE
            slowln[i] = close[i]
            fastln[i] = slowln[i]
            _s_OnCalculate_m_array[i].trena = 0
            _s_OnCalculate_m_array[i].trend = _s_OnCalculate_m_array[i].trena
        if _s_OnCalculate_m_array[i].trend != -1:
            candleo[i] = open[i]
            candleh[i] = high[i]
            candlel[i] = low[i]
            candlec[i] = close[i]
        else:
            candlec[i] = EMPTY_VALUE
            candlel[i] = candlec[i]
            candleh[i] = candlel[i]
            candleo[i] = candleh[i]
        candleC[i] = _s_OnCalculate_m_array[i].trend
        arrowcl[i] = _s_OnCalculate_m_array[i].trena
        i += 1
    return rates_total

# ---- static local variables
_s_OnCalculate_m_array = Arr(0, 0, factory=sPtlStruct)
_s_OnCalculate_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PTL2(_MQL5Indicator):
    name = 'PTL (2)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastLength': 3,  # Fast length
        'inpSlowLength': 7,  # Slow length
    }

