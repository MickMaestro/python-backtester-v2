"""nrtr_atr_stop — converted from MQL5: MQL5 Indicators/NRTR_ATR_STOP/nrtr_atr_stop.mq5

Copyright: Copyright 2014, PunkBASSter.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, PunkBASSter.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up', 2: 'Dn'}, 'levels': [], 'description': [], 'name': 'nrtr_atr_stop', 'source': 'MQL5 Indicators/NRTR_ATR_STOP/nrtr_atr_stop.mq5', 'folder': 'NRTR_ATR_STOP', 'inputs': [{'mql': 'ATR', 'py': 'ATR', 'param': 'ATR', 'type': 'int', 'default': 20, 'label': 'ATR period', 'sinput': False}, {'mql': 'K', 'py': 'K', 'param': 'K', 'type': 'int', 'default': 2, 'label': 'Coefficient', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MODE
MODE_UP = 0
MODE_DN = 1
_enum('MODE', {0: 'MODE_UP', 1: 'MODE_DN'})

# ---- inputs and global variables
ATR = _input('ATR', 20)  # ATR period
K = _input('K', 2)  # Coefficient
Up = Arr(0, 0.0)
Dn = Arr(0, 0.0)
sym = ""
first = False
hATR = INVALID_HANDLE
mode = 0

def OnInit():
    global first, hATR
    SetIndexBuffer(0, Up)
    SetIndexBuffer(1, Dn)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(Up, True)
    ArraySetAsSeries(Dn, True)
    hATR = iATR(Symbol(), Period(), ATR)
    if hATR == INVALID_HANDLE:
        Print('Failed to initialize ATR.')
        return INIT_FAILED
    first = True
    return INIT_SUCCEEDED

def OnCalculate(rates_total, calculated, time, open, high, low, close, tick_volume, volume, spread):
    global first, mode
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    i = 0
    limit = 0
    REZ = 0.0
    md = 0.0
    buf = Arr(1, 0.0, dyn=False)
    limit = rates_total - ATR - 1
    if first:
        md = 0.0
        i = 0
        for i in range(i, limit):
            CopyBuffer(hATR, 0, i, 1, buf)
            md += buf[0]
        else:
            i = _range_end(i, limit, 1)
        CopyBuffer(hATR, 0, limit, 1, buf)
        REZ = K * buf[0]
        if buf[0] < _fdiv(md, limit):
            Up[limit + 1] = low[limit + 1] - REZ
            mode = MODE_UP
        if buf[0] > _fdiv(md, limit):
            Dn[limit + 1] = high[limit + 1] + REZ
            mode = MODE_DN
        first = False
    i = limit - 1
    for i in range(i, 0 - 1, -1):
        Dn[i] = EMPTY_VALUE
        Up[i] = EMPTY_VALUE
        CopyBuffer(hATR, 0, i, 1, buf)
        REZ = K * buf[0]
        if mode == MODE_DN and low[i + 1] > Dn[i + 1]:
            Up[i + 1] = low[i + 1] - REZ
            mode = MODE_UP
        if mode == MODE_UP and high[i + 1] < Up[i + 1]:
            Dn[i + 1] = high[i + 1] + REZ
            mode = MODE_DN
        if mode == MODE_UP:
            if low[i + 1] > (Up[i + 1] + REZ):
                Up[i] = low[i + 1] - REZ
                Dn[i] = EMPTY_VALUE
            else:
                Up[i] = Up[i + 1]
                Dn[i] = EMPTY_VALUE
        if mode == MODE_DN:
            if high[i + 1] < (Dn[i + 1] - REZ):
                Dn[i] = high[i + 1] + REZ
                Up[i] = EMPTY_VALUE
            else:
                Dn[i] = Dn[i + 1]
                Up[i] = EMPTY_VALUE
    else:
        i = _range_end(i, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NrtrAtrStop(_MQL5Indicator):
    name = 'nrtr_atr_stop'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR': 20,  # ATR period
        'K': 2,  # Coefficient
    }

