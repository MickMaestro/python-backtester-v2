"""WPR candles — converted from MQL5: MQL5 Indicators/WPR Candles/WPR candles.mq5

WPR candles
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421504, 16748574, 3937500]}, 'widths': {}, 'styles': {}, 'labels': {1: 'WPR'}, 'levels': [0.0, -100.0], 'description': ['WPR candles'], 'name': 'WPR candles', 'source': 'MQL5 Indicators/WPR Candles/WPR candles.mq5', 'folder': 'WPR Candles', 'inputs': [{'mql': 'inpWprPeriod', 'py': 'inpWprPeriod', 'param': 'inpWprPeriod', 'type': 'int', 'default': 50, 'label': 'WPR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpWprPeriod = _input('inpWprPeriod', 50)  # WPR period
wpro = Arr(0, 0.0)
wprh = Arr(0, 0.0)
wprl = Arr(0, 0.0)
wprc = Arr(0, 0.0)
wprcl = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, wpro, INDICATOR_DATA)
    SetIndexBuffer(1, wprh, INDICATOR_DATA)
    SetIndexBuffer(2, wprl, INDICATOR_DATA)
    SetIndexBuffer(3, wprc, INDICATOR_DATA)
    SetIndexBuffer(4, wprcl, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WPR candles (' + _str(inpWprPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _wpr = Arr(4, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - inpWprPeriod, 0)
        _omax = open[ArrayMaximum(open, _start, inpWprPeriod)]
        _omin = open[ArrayMinimum(open, _start, inpWprPeriod)]
        _cmax = close[ArrayMaximum(close, _start, inpWprPeriod)]
        _cmin = close[ArrayMinimum(close, _start, inpWprPeriod)]
        _hmax = high[ArrayMaximum(high, _start, inpWprPeriod)]
        _hmin = high[ArrayMinimum(high, _start, inpWprPeriod)]
        _lmax = low[ArrayMaximum(low, _start, inpWprPeriod)]
        _lmin = low[ArrayMinimum(low, _start, inpWprPeriod)]
        _wpr[0] = (_fdiv((-(_omax - open[i])) * 100, _omax - _omin) if ((_omax - _omin) != 0) else 0)
        _wpr[1] = (_fdiv((-(_hmax - high[i])) * 100, _hmax - _hmin) if ((_hmax - _hmin) != 0) else 0)
        _wpr[2] = (_fdiv((-(_lmax - low[i])) * 100, _lmax - _lmin) if ((_lmax - _lmin) != 0) else 0)
        _wpr[3] = (_fdiv((-(_cmax - close[i])) * 100, _cmax - _cmin) if ((_cmax - _cmin) != 0) else 0)
        wpro[i] = _wpr[0]
        wprc[i] = _wpr[3]
        wprh[i] = _wpr[ArrayMaximum(_wpr, 0, 4)]
        wprl[i] = _wpr[ArrayMinimum(_wpr, 0, 4)]
        wprcl[i] = (1 if (wprc[i] > wpro[i]) else 2 if (wprc[i] < wpro[i]) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WPRCandles(_MQL5Indicator):
    name = 'WPR candles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpWprPeriod': 50,  # WPR period
    }

