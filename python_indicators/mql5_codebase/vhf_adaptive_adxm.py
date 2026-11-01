"""VHF adaptive ADXm — converted from MQL5: MQL5 Indicators/VHF adaptive ADXm/VHF adaptive ADXm.mq5

VHF adaptive ADXm
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [11119017], 2: [11119017, 16748574, 6333684]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'DI', 2: 'ADXm'}, 'levels': [], 'description': ['VHF adaptive ADXm'], 'name': 'VHF adaptive ADXm', 'source': 'MQL5 Indicators/VHF adaptive ADXm/VHF adaptive ADXm.mq5', 'folder': 'VHF adaptive ADXm', 'inputs': [{'mql': 'inpAdxmPeriod', 'py': 'inpAdxmPeriod', 'param': 'inpAdxmPeriod', 'type': 'int', 'default': 14, 'label': 'ADXm period', 'sinput': False}, {'mql': 'inpAdaptive', 'py': 'inpAdaptive', 'param': 'inpAdaptive', 'type': 'bool', 'default': True, 'label': 'VHF adaptive ADXm?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAdxmPeriod = _input('inpAdxmPeriod', 14)  # ADXm period
inpAdaptive = _input('inpAdaptive', True)  # VHF adaptive ADXm?
adxm = Arr(0, 0.0)
adxmc = Arr(0, 0.0)
di = Arr(0, 0.0)
vhfDiff = Arr(0, 0.0)
vhfNoise = Arr(0, 0.0)
_adxmWork = Arr(6, 0.0, dyn=False, dims=(8,))

def OnInit():
    SetIndexBuffer(0, di, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, adxm, INDICATOR_DATA)
    SetIndexBuffer(2, adxmc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, vhfDiff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, vhfNoise, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, ('VHF adaptive ' if inpAdaptive else ' ') + 'ADXm (' + _str(inpAdxmPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        period = inpAdxmPeriod
        if inpAdaptive:
            vhfDiff[i] = (((close[i] - close[i - 1]) if (close[i] > close[i - 1]) else (close[i - 1] - close[i])) if (i > 0) else 0)
            if i >= inpAdxmPeriod:
                vhfNoise[i] = vhfNoise[i - 1] - vhfDiff[i - inpAdxmPeriod] + vhfDiff[i]
            else:
                vhfNoise[i] = 0.0
                k = 0
                while k < inpAdxmPeriod and (i - k) >= 0:
                    vhfNoise[i] += vhfDiff[i - k]
                    k += 1
            start = ((i - inpAdxmPeriod + 1) if (i >= inpAdxmPeriod) else 0)
            HCP = close[ArrayMaximum(close, start, inpAdxmPeriod)]
            LCP = close[ArrayMinimum(close, start, inpAdxmPeriod)]
            vhf = (_fdiv(HCP - LCP, vhfNoise[i]) if (vhfNoise[i] != 0) else 0)
            if vhf != 0:
                period = inpAdxmPeriod * vhf * 2.0
        _di = Box(0.0)
        adxm[i] = iAdxm(close[i], high[i], low[i], period, _di, i)
        di[i] = _di.v
        adxmc[i] = ((1 if (adxm[i] > adxm[i - 1]) else 2 if (adxm[i] < adxm[i - 1]) else adxmc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iAdxm(_close, _high, _low, _period, _di, i, instance=0):
    _indC = _imod(i, 6)
    _indP = _imod(i - 1, 6)
    _inst = instance * 8
    _adxmWork[_indC][_inst + 3] = _close
    _adxmWork[_indC][_inst + 4] = _high
    _adxmWork[_indC][_inst + 5] = _low
    hc = _adxmWork[_indC][_inst + 4]
    lc = _adxmWork[_indC][_inst + 5]
    cp = (_adxmWork[_indP][_inst + 3] if (i > 0) else _adxmWork[_indC][_inst + 3])
    hp = (_adxmWork[_indP][_inst + 4] if (i > 0) else _adxmWork[_indC][_inst + 4])
    lp = (_adxmWork[_indP][_inst + 5] if (i > 0) else _adxmWork[_indC][_inst + 5])
    dh = ((hc - hp) if (hc > hp) else 0)
    dl = ((lp - lc) if (lp > lc) else 0)
    if dh == dl:
        dh = 0.0
        dl = 0.0
    elif dh < dl:
        dh = 0.0
    elif dl < dh:
        dl = 0.0
    tr = (hc if (hc > cp) else cp) - (lc if (lc < cp) else cp)
    dhk = (_fdiv(100.0 * dh, tr) if (tr != 0) else 0)
    dlk = (_fdiv(100.0 * dl, tr) if (tr != 0) else 0)
    alpha = _fdiv(2.0, _period + 1.0)
    _adxmWork[_indC][_inst + 0] = ((_adxmWork[_indP][_inst + 0] + (alpha * (dhk - _adxmWork[_indP][_inst + 0]))) if (i > 0) else dhk)
    _adxmWork[_indC][_inst + 1] = ((_adxmWork[_indP][_inst + 1] + (alpha * (dlk - _adxmWork[_indP][_inst + 1]))) if (i > 0) else dlk)
    _adxmWork[_indC][_inst + 6] = _adxmWork[_indC][_inst + 0] - _adxmWork[_indC][_inst + 1]
    div = _adxmWork[_indC][_inst + 0] + _adxmWork[_indC][_inst + 1]
    div = (div if (div > 0.0) else (-div))
    temp = (_fdiv(100.0 * _adxmWork[_indC][_inst + 6], div) if (div != 0.0) else 0)
    _adxmWork[_indC][_inst + 7] = ((_adxmWork[_indP][_inst + 7] + (alpha * (temp - _adxmWork[_indP][_inst + 7]))) if (i > 0) else 0)
    _di.v = _adxmWork[_indC][_inst + 6]
    return _adxmWork[_indC][_inst + 7]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VHFAdaptiveADXm(_MQL5Indicator):
    name = 'VHF adaptive ADXm'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAdxmPeriod': 14,  # ADXm period
        'inpAdaptive': True,  # VHF adaptive ADXm?
    }

