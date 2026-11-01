"""Wilson Relative Price Channel - mod — converted from MQL5: MQL5 Indicators/Wilson Relative Price Channel - mod/Wilson Relative Price Channel - mod.mq5

Wilson Relative Price Channel
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [10025880, 10025880], 2: [15134970, 15134970], 3: [12632256], 4: [12632256], 5: [12632256], 6: [12632256]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper filling', 2: 'Lower filling'}, 'levels': [], 'description': ['Wilson Relative Price Channel'], 'name': 'Wilson Relative Price Channel - mod', 'source': 'MQL5 Indicators/Wilson Relative Price Channel - mod/Wilson Relative Price Channel - mod.mq5', 'folder': 'Wilson Relative Price Channel - mod', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'RSI price', 'sinput': False}, {'mql': 'inpSmoothing', 'py': 'inpSmoothing', 'param': 'inpSmoothing', 'type': 'int', 'default': 14, 'label': 'Smoothing period for RSI and EMA', 'sinput': False}, {'mql': 'inpOverbought', 'py': 'inpOverbought', 'param': 'inpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought level %', 'sinput': False}, {'mql': 'inpOversold', 'py': 'inpOversold', 'param': 'inpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold level %', 'sinput': False}, {'mql': 'inpUpperNeutral', 'py': 'inpUpperNeutral', 'param': 'inpUpperNeutral', 'type': 'double', 'default': 55.0, 'label': 'Upper neutral level %', 'sinput': False}, {'mql': 'inpLowerNeutral', 'py': 'inpLowerNeutral', 'param': 'inpLowerNeutral', 'type': 'double', 'default': 45.0, 'label': 'Lower neutral level %', 'sinput': False}, {'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 100, 'label': 'ATR period', 'sinput': False}, {'mql': 'inpAtrMultuplicator', 'py': 'inpAtrMultuplicator', 'param': 'inpAtrMultuplicator', 'type': 'double', 'default': 25.0, 'label': 'ATR multiplicator', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # RSI price
inpSmoothing = _input('inpSmoothing', 14)  # Smoothing period for RSI and EMA
inpOverbought = _input('inpOverbought', 70.0)  # Overbought level %
inpOversold = _input('inpOversold', 30.0)  # Oversold level %
inpUpperNeutral = _input('inpUpperNeutral', 55.0)  # Upper neutral level %
inpLowerNeutral = _input('inpLowerNeutral', 45.0)  # Lower neutral level %
inpAtrPeriod = _input('inpAtrPeriod', 100)  # ATR period
inpAtrMultuplicator = _input('inpAtrMultuplicator', 25.0)  # ATR multiplicator
filluu = Arr(0, 0.0)
fillud = Arr(0, 0.0)
filldu = Arr(0, 0.0)
filldd = Arr(0, 0.0)
bupu = Arr(0, 0.0)
bupd = Arr(0, 0.0)
bdnu = Arr(0, 0.0)
bdnd = Arr(0, 0.0)
rsi = Arr(0, 0.0)
atr = Arr(0, 0.0)
_rsiHandle = 0
_atrHandle = 0
workEma = Arr(6, 0.0, dyn=False, dims=(5,))

def OnInit():
    global _atrHandle, _rsiHandle
    SetIndexBuffer(0, filluu, INDICATOR_DATA)
    SetIndexBuffer(1, fillud, INDICATOR_DATA)
    SetIndexBuffer(2, filldu, INDICATOR_DATA)
    SetIndexBuffer(3, filldd, INDICATOR_DATA)
    SetIndexBuffer(4, bupu, INDICATOR_DATA)
    SetIndexBuffer(5, bupd, INDICATOR_DATA)
    SetIndexBuffer(6, bdnu, INDICATOR_DATA)
    SetIndexBuffer(7, bdnd, INDICATOR_DATA)
    SetIndexBuffer(8, rsi, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, atr, INDICATOR_CALCULATIONS)
    _rsiHandle = iRSI(Symbol(), 0, inpRsiPeriod, inpPrice)
    if _rsiHandle == INVALID_HANDLE:
        return INIT_FAILED
    _atrHandle = iATR(Symbol(), 0, inpAtrPeriod)
    if _atrHandle == INVALID_HANDLE:
        IndicatorRelease(_rsiHandle)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wilson rpc (' + _str(inpRsiPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_rsiHandle) < rates_total:
        return prev_calculated
    if BarsCalculated(_atrHandle) < rates_total:
        return prev_calculated
    _copyCount = MathMin(rates_total - prev_calculated + 1, rates_total)
    if CopyBuffer(_rsiHandle, 0, 0, _copyCount, rsi) != _copyCount:
        return prev_calculated
    if CopyBuffer(_atrHandle, 0, 0, _copyCount, atr) != _copyCount:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _rsi = (rsi[i] if (rsi[i] != EMPTY_VALUE) else 0)
        _atr = ((atr[i] * inpAtrMultuplicator) if (atr[i] != EMPTY_VALUE) else 0)
        _ob = iEma(_rsi - inpOverbought, inpSmoothing, i, 0) / 100.0
        _os = iEma(_rsi - inpOversold, inpSmoothing, i, 1) / 100.0
        _nzu = iEma(_rsi - inpUpperNeutral, inpSmoothing, i, 2) / 100.0
        _nzd = iEma(_rsi - inpLowerNeutral, inpSmoothing, i, 3) / 100.0
        _ema = iEma(close[i], inpSmoothing, i, 4)
        bupu[i] = _ema - (_atr * _ob)
        filluu[i] = bupu[i]
        bupd[i] = _ema - (_atr * _nzu)
        fillud[i] = bupd[i]
        bdnu[i] = _ema - (_atr * _os)
        filldu[i] = bdnu[i]
        bdnd[i] = _ema - (_atr * _nzd)
        filldd[i] = bdnd[i]
        i += 1
    return i

def iEma(price, period, i, _inst=0):
    _indC = _imod(i, 6)
    _indP = _imod(i - 1, 6)
    if i > 0 and period > 1:
        workEma[_indC][_inst] = workEma[_indP][_inst] + (_fdiv(2.0, 1.0 + period) * (price - workEma[_indP][_inst]))
    else:
        workEma[_indC][_inst] = price
    return workEma[_indC][_inst]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WilsonRelativePriceChannelMod(_MQL5Indicator):
    name = 'Wilson Relative Price Channel - mod'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI price
        'inpSmoothing': 14,  # Smoothing period for RSI and EMA
        'inpOverbought': 70.0,  # Overbought level %
        'inpOversold': 30.0,  # Oversold level %
        'inpUpperNeutral': 55.0,  # Upper neutral level %
        'inpLowerNeutral': 45.0,  # Lower neutral level %
        'inpAtrPeriod': 100,  # ATR period
        'inpAtrMultuplicator': 25.0,  # ATR multiplicator
    }

