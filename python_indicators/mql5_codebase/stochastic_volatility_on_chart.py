"""Stochastic volatility on-chart — converted from MQL5: MQL5 Indicators/Stochastic volatility - on chart/Stochastic volatility on-chart.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [17919]}, 'widths': {}, 'styles': {1: 2}, 'labels': {1: 'ranging candles'}, 'levels': [], 'description': [], 'name': 'Stochastic volatility on-chart', 'source': 'MQL5 Indicators/Stochastic volatility - on chart/Stochastic volatility on-chart.mq5', 'folder': 'Stochastic volatility - on chart', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 30, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 5, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'int', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'BandsLength', 'py': 'BandsLength', 'param': 'BandsLength', 'type': 'int', 'default': 126, 'label': 'Bands period', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'Bands deviation', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'OriginalStoch', 'py': 'OriginalStoch', 'param': 'OriginalStoch', 'type': 'bool', 'default': True, 'label': 'Calculate using original stochastic', 'sinput': False}, {'mql': 'OriginalVolatility', 'py': 'OriginalVolatility', 'param': 'OriginalVolatility', 'type': 'bool', 'default': True, 'label': 'Calculate using original volatility', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 30)  # Stochastic period
Slowing = _input('Slowing', 5)  # Stochastic slowing
Signal = _input('Signal', 5)  # Signal period
BandsLength = _input('BandsLength', 126)  # Bands period
BandsDeviation = _input('BandsDeviation', 1.0)  # Bands deviation
Price = _input('Price', PRICE_CLOSE)  # Price
OriginalStoch = _input('OriginalStoch', True)  # Calculate using original stochastic
OriginalVolatility = _input('OriginalVolatility', True)  # Calculate using original volatility
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
cano = Arr(0, 0.0)
canc = Arr(0, 0.0)
cancl = Arr(0, 0.0)
valc = Arr(0, 0.0)
_viHandle = 0
_shortName = ""

def OnInit():
    global _shortName, _viHandle
    SetIndexBuffer(0, cano, INDICATOR_DATA)
    SetIndexBuffer(1, canh, INDICATOR_DATA)
    SetIndexBuffer(2, canl, INDICATOR_DATA)
    SetIndexBuffer(3, canc, INDICATOR_DATA)
    SetIndexBuffer(4, cancl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, valc, INDICATOR_CALCULATIONS)
    _uniqueID = 'Stochastic volatility ' + _str(MathRand())
    _shortName = _uniqueID + ' (' + _str(Length) + ',' + _str(Slowing) + ',' + _str(Signal) + ')'
    _viHandle = iCustom(Symbol(), 0, '::Stochastic volatility 2.ex5', Length, Slowing, Signal, BandsLength, BandsDeviation, Price, OriginalStoch, OriginalVolatility, _uniqueID)
    if not _checkHandle(_viHandle, 'Stochastic volatility'):
        return INIT_FAILED
    ChartIndicatorAdd(0, _int(ChartGetInteger(0, CHART_WINDOWS_TOTAL)), _viHandle)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic volatility on chart (' + _str(Length) + ',' + _str(Slowing) + ',' + _str(Signal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    windows = _int(ChartGetInteger(0, CHART_WINDOWS_TOTAL))
    for w in range(0, windows):
        total = ChartIndicatorsTotal(0, w)
        for i in range(0, total):
            _name = ChartIndicatorName(0, w, i)
            if _name == _shortName:
                ChartIndicatorDelete(0, w, _name)
                ChartRedraw()
    IndicatorRelease(_viHandle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_viHandle) < rates_total:
        return prev_calculated
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_viHandle, 3, 0, _copyCount, valc) != _copyCount:
        Comment('Error copying states')
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        cancl[i] = 0.0
        if valc[i] != 0:
            canc[i] = close[i]
            cano[i] = open[i]
            canh[i] = high[i]
            canl[i] = low[i]
        else:
            cano[i] = EMPTY_VALUE
            canl[i] = cano[i]
            canh[i] = canl[i]
            canc[i] = canh[i]
        i += 1
    return i

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__handles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__handles[i])
        ArrayResize(_s__checkHandle__handles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticVolatilityOnChart(_MQL5Indicator):
    name = 'Stochastic volatility on-chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 30,  # Stochastic period
        'Slowing': 5,  # Stochastic slowing
        'Signal': 5,  # Signal period
        'BandsLength': 126,  # Bands period
        'BandsDeviation': 1.0,  # Bands deviation
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'OriginalStoch': True,  # Calculate using original stochastic
        'OriginalVolatility': True,  # Calculate using original volatility
    }

