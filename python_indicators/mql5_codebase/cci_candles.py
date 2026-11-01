"""CCI candles — converted from MQL5: MQL5 Indicators/CCI Candles/CCI candles.mq5

CCI candles
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421504, 16748574, 6333684]}, 'widths': {}, 'styles': {}, 'labels': {1: 'cci'}, 'levels': [], 'description': ['CCI candles'], 'name': 'CCI candles', 'source': 'MQL5 Indicators/CCI Candles/CCI candles.mq5', 'folder': 'CCI Candles', 'inputs': [{'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 32, 'label': 'CCI period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpCciPeriod = _input('inpCciPeriod', 32)  # CCI period
ccio = Arr(0, 0.0)
ccih = Arr(0, 0.0)
ccil = Arr(0, 0.0)
ccic = Arr(0, 0.0)
ccicl = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ccio, INDICATOR_DATA)
    SetIndexBuffer(1, ccih, INDICATOR_DATA)
    SetIndexBuffer(2, ccil, INDICATOR_DATA)
    SetIndexBuffer(3, ccic, INDICATOR_DATA)
    SetIndexBuffer(4, ccicl, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI candles (' + _str(inpCciPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _cci = Arr(4, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        avgh = 0.0
        avgl = 0.0
        avgo = 0.0
        avgc = 0.0
        k = 0
        while k < inpCciPeriod and (i - k) >= 0:
            avgh += high[i - k]
            avgl += low[i - k]
            avgo += open[i - k]
            avgc += close[i - k]
            k += 1
        avgh = avgh / inpCciPeriod
        avgl = avgl / inpCciPeriod
        avgo = avgo / inpCciPeriod
        avgc = avgc / inpCciPeriod
        devh = 0.0
        devl = 0.0
        devo = 0.0
        devc = 0.0
        k = 0
        while k < inpCciPeriod and (i - k) >= 0:
            devh += MathAbs(high[i - k] - avgh)
            devl += MathAbs(low[i - k] - avgl)
            devo += MathAbs(open[i - k] - avgo)
            devc += MathAbs(close[i - k] - avgc)
            k += 1
        devh = devh / inpCciPeriod
        devl = devl / inpCciPeriod
        devo = devo / inpCciPeriod
        devc = devc / inpCciPeriod
        _cci[0] = (_fdiv(high[i] - avgh, 0.015 * devh) if (devh != 0) else 0)
        _cci[1] = (_fdiv(low[i] - avgl, 0.015 * devl) if (devl != 0) else 0)
        _cci[2] = (_fdiv(open[i] - avgo, 0.015 * devo) if (devo != 0) else 0)
        _cci[3] = (_fdiv(close[i] - avgc, 0.015 * devc) if (devc != 0) else 0)
        ccio[i] = _cci[2]
        ccic[i] = _cci[3]
        ccih[i] = _cci[ArrayMaximum(_cci, 0, 4)]
        ccil[i] = _cci[ArrayMinimum(_cci, 0, 4)]
        ccicl[i] = (1 if (ccic[i] > ccio[i]) else 2 if (ccic[i] < ccio[i]) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCICandles(_MQL5Indicator):
    name = 'CCI candles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCciPeriod': 32,  # CCI period
    }

