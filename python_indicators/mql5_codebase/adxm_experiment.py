"""ADXm (experiment) — converted from MQL5: MQL5 Indicators/ADXm (experiment)/ADXm (experiment).mq5

Copyright: © mladen, 2022; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2022', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [11119017], 2: [11119017, 16748574, 6333684]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'DI', 2: 'ADXm'}, 'levels': [], 'description': [], 'name': 'ADXm (experiment)', 'source': 'MQL5 Indicators/ADXm (experiment)/ADXm (experiment).mq5', 'folder': 'ADXm (experiment)', 'inputs': [{'mql': 'inpAdxmPeriod', 'py': 'inpAdxmPeriod', 'param': 'inpAdxmPeriod', 'type': 'double', 'default': 14.0, 'label': 'ADXm period', 'sinput': False}, {'mql': 'inpDouble', 'py': 'inpDouble', 'param': 'inpDouble', 'type': 'int', 'default': 0, 'label': 'ADXm calculating mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDouble
adxm_regular = 0
adxm_double = 1
_enum('enDouble', {0: 'adxm_regular', 1: 'adxm_double'})

# ---- inputs and global variables
inpAdxmPeriod = _input('inpAdxmPeriod', 14.0)  # ADXm period
inpDouble = _input('inpDouble', adxm_regular)  # ADXm calculating mode
adxm = Arr(0, 0.0)
adxmc = Arr(0, 0.0)
di = Arr(0, 0.0)

class sDataStruct(MqlObject):
    _q_fields = ('di', 'adx', 'close', 'high', 'low', 'sdh', 'sdl')
    def __init__(self, *args):
        self.di = 0.0
        self.adx = 0.0
        self.close = 0.0
        self.high = 0.0
        self.low = 0.0
        self.sdh = 0.0
        self.sdl = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('data',)
    def __init__(self, *args):
        self.data = Arr(2, 0, dyn=False, factory=sDataStruct)

def OnInit():
    SetIndexBuffer(0, di, INDICATOR_DATA)
    SetIndexBuffer(1, adxm, INDICATOR_DATA)
    SetIndexBuffer(2, adxmc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('ADXm experiment (%.2f,%s)', inpAdxmPeriod, StringSubstr(EnumToString(inpDouble, 'enDouble'), 5)))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(limit, rates_total):
        if inpDouble == adxm_double:
            _di = Box(0.0)
            _adxm = iAdxm(close[i], high[i], low[i], inpAdxmPeriod, _di, i, rates_total, 0)
            adxm[i] = iAdxm(_adxm, _adxm, _adxm, inpAdxmPeriod, _ElemRef(di, i), i, rates_total, 1)
        else:
            adxm[i] = iAdxm(close[i], high[i], low[i], inpAdxmPeriod, _ElemRef(di, i), i, rates_total)
        adxmc[i] = ((1 if (adxm[i] > adxm[i - 1]) else 2 if (adxm[i] < adxm[i - 1]) else adxmc[i - 1]) if (i > 0) else 0)
    return rates_total

def iAdxm(_close, _high, _low, _period, _di, i, _bars, instance=0):
    global _s_iAdxm_m_workSize
    if _s_iAdxm_m_workSize < _bars:
        _s_iAdxm_m_workSize = ArrayResize(_s_iAdxm_m_work, _bars + 500, 2000)
    _s_iAdxm_m_work[i].data[instance].close = _close
    _s_iAdxm_m_work[i].data[instance].high = _high
    _s_iAdxm_m_work[i].data[instance].low = _low
    hc = _high
    lc = _low
    cp = (_s_iAdxm_m_work[i - 1].data[instance].close if (i > 0) else _close)
    hp = (_s_iAdxm_m_work[i - 1].data[instance].high if (i > 0) else _high)
    lp = (_s_iAdxm_m_work[i - 1].data[instance].low if (i > 0) else _low)
    dh = ((hc - hp) if (hc > hp) else 0)
    dl = ((lp - lc) if (lp > lc) else 0)
    if dh < dl:
        dh = 0.0
    elif dl < dh:
        dl = 0.0
    else:
        dl = 0.0
        dh = dl
    tr = (hc if (hc > cp) else cp) - (lc if (lc < cp) else cp)
    dhk = (_fdiv(100.0 * dh, tr) if (tr != 0) else 0)
    dlk = (_fdiv(100.0 * dl, tr) if (tr != 0) else 0)
    alpha = (_fdiv(2.0, _period + 1.0) if (_period > 1) else 1)
    _s_iAdxm_m_work[i].data[instance].sdh = ((_s_iAdxm_m_work[i - 1].data[instance].sdh + (alpha * (dhk - _s_iAdxm_m_work[i - 1].data[instance].sdh))) if (i > 0) else dhk)
    _s_iAdxm_m_work[i].data[instance].sdl = ((_s_iAdxm_m_work[i - 1].data[instance].sdl + (alpha * (dlk - _s_iAdxm_m_work[i - 1].data[instance].sdl))) if (i > 0) else dlk)
    _di.v = _s_iAdxm_m_work[i].data[instance].sdh - _s_iAdxm_m_work[i].data[instance].sdl
    _s_iAdxm_m_work[i].data[instance].di = _di.v
    div = _s_iAdxm_m_work[i].data[instance].sdh + _s_iAdxm_m_work[i].data[instance].sdl
    div = (div if (div > 0.0) else (-div))
    temp = (_fdiv(100.0 * _s_iAdxm_m_work[i].data[instance].di, div) if (div != 0.0) else 0)
    _s_iAdxm_m_work[i].data[instance].adx = ((_s_iAdxm_m_work[i - 1].data[instance].adx + (alpha * (temp - _s_iAdxm_m_work[i - 1].data[instance].adx))) if (i > 0) else 0)
    return _s_iAdxm_m_work[i].data[instance].adx

# ---- static local variables
_s_iAdxm_m_work = Arr(0, 0, factory=sWorkStruct)
_s_iAdxm_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXmExperiment(_MQL5Indicator):
    name = 'ADXm (experiment)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAdxmPeriod': 14.0,  # ADXm period
        'inpDouble': _Choice({0: 'Regular ADXm', 1: 'ADXm of ADXm'}, default=0),  # ADXm calculating mode
    }

