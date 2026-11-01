"""RSI_candles_lite — converted from MQL5: MQL5 Indicators/RSI candles - lite ressource/RSI_candles_lite.mq5

Rsi candles - improved version
based on RSI_candles by (C) mladen, 2018
https://www.mql5.com/en/code/20968
Copyright: Copyright 2019, Soewono Effendi; Link: https://www.mql5.com/en/users/seffx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019, Soewono Effendi', 'link': 'https://www.mql5.com/en/users/seffx', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421504, 16748574, 3937500]}, 'widths': {}, 'styles': {1: 2, 2: 2}, 'labels': {}, 'levels': [70.0, 30.0], 'description': ['Rsi candles - improved version', 'based on RSI_candles by (C) mladen, 2018', 'https://www.mql5.com/en/code/20968'], 'name': 'RSI_candles_lite', 'source': 'MQL5 Indicators/RSI candles - lite ressource/RSI_candles_lite.mq5', 'folder': 'RSI candles - lite ressource', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
rsio = Arr(0, 0.0)
rsih = Arr(0, 0.0)
rsil = Arr(0, 0.0)
rsic = Arr(0, 0.0)
rsicl = Arr(0, 0.0)
hRsiO = 0
hRsiC = 0
hRsiH = 0
hRsiL = 0
last_bars = 0

def getValue(handle, pos):
    buffer = Arr(1, 0.0, dyn=False)
    if CopyBuffer(handle, 0, pos, 1, buffer) == 1:
        return buffer[0]
    return EMPTY_VALUE

def OnInit():
    global hRsiC, hRsiH, hRsiL, hRsiO
    ArraySetAsSeries(rsio, True)
    ArraySetAsSeries(rsih, True)
    ArraySetAsSeries(rsil, True)
    ArraySetAsSeries(rsic, True)
    ArraySetAsSeries(rsicl, True)
    SetIndexBuffer(0, rsio, INDICATOR_DATA)
    SetIndexBuffer(1, rsih, INDICATOR_DATA)
    SetIndexBuffer(2, rsil, INDICATOR_DATA)
    SetIndexBuffer(3, rsic, INDICATOR_DATA)
    SetIndexBuffer(4, rsicl, INDICATOR_COLOR_INDEX)
    name = 'Rsi candles (' + _str(inpRsiPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, name)
    PlotIndexSetString(0, PLOT_LABEL, name)
    hRsiO = iRSI(None, 0, inpRsiPeriod, PRICE_OPEN)
    hRsiC = iRSI(None, 0, inpRsiPeriod, PRICE_CLOSE)
    hRsiH = iRSI(None, 0, inpRsiPeriod, PRICE_HIGH)
    hRsiL = iRSI(None, 0, inpRsiPeriod, PRICE_LOW)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(hRsiO)
    IndicatorRelease(hRsiC)
    IndicatorRelease(hRsiH)
    IndicatorRelease(hRsiL)
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global last_bars
    _rsi = Arr(4, 0.0, dyn=False)
    rsiO = 0.0
    rsiC = 0.0
    rsiH = 0.0
    rsiL = 0.0
    i = 0
    calculated = BarsCalculated(hRsiC)
    if calculated < inpRsiPeriod:
        return prev_calculated
    last_bars = calculated
    if prev_calculated == 0:
        i = rates_total - 1
    else:
        i = rates_total - prev_calculated
    while i >= 0:
        rsiO = getValue(hRsiO, i)
        rsiC = getValue(hRsiC, i)
        rsiH = getValue(hRsiH, i)
        rsiL = getValue(hRsiL, i)
        _rsi[0] = rsiO
        _rsi[1] = rsiH
        _rsi[2] = rsiL
        _rsi[3] = rsiC
        rsio[i] = _rsi[0]
        rsic[i] = _rsi[3]
        rsih[i] = _rsi[ArrayMaximum(_rsi)]
        rsil[i] = _rsi[ArrayMinimum(_rsi)]
        rsicl[i] = (1 if (rsiC > rsiO) else 2 if (rsiC < rsiO) else 0)
        i -= 1
    return rates_total - 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSICandlesLite(_MQL5Indicator):
    name = 'RSI_candles_lite'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
    }

