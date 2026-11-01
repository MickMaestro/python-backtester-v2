"""indmatema — converted from MQL5: MQL5 Indicators/The IndMATEMA indicator based on crossing of two MA and two TEMA/indmatema.mq5

Copyright: Shovel; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Shovel', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 16748574, 55295, 8421504]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'MATEMA'}, 'levels': [0.0], 'description': [], 'name': 'indmatema', 'source': 'MQL5 Indicators/The IndMATEMA indicator based on crossing of two MA and two TEMA/indmatema.mq5', 'folder': 'The IndMATEMA indicator based on crossing of two MA and two TEMA', 'inputs': [{'mql': 'InpMA1Period', 'py': 'InpMA1Period', 'param': 'InpMA1Period', 'type': 'int', 'default': 10, 'label': 'Period MA Close', 'sinput': False}, {'mql': 'InpMA1Method', 'py': 'InpMA1Method', 'param': 'InpMA1Method', 'type': 'int', 'default': 2, 'label': 'Method MA Close', 'sinput': False}, {'mql': 'InpMA2Period', 'py': 'InpMA2Period', 'param': 'InpMA2Period', 'type': 'int', 'default': 10, 'label': 'Period MA Open', 'sinput': False}, {'mql': 'InpMA2Method', 'py': 'InpMA2Method', 'param': 'InpMA2Method', 'type': 'int', 'default': 2, 'label': 'Method MA Open', 'sinput': False}, {'mql': 'delta', 'py': 'delta', 'param': 'delta', 'type': 'double', 'default': 0.0002, 'label': 'Delta', 'sinput': False}, {'mql': 'InpTEMA1Period', 'py': 'InpTEMA1Period', 'param': 'InpTEMA1Period', 'type': 'int', 'default': 20, 'label': 'Period TEMA Close', 'sinput': False}, {'mql': 'InpTEMA2Period', 'py': 'InpTEMA2Period', 'param': 'InpTEMA2Period', 'type': 'int', 'default': 20, 'label': 'Period TEMA Open', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMA1Period = _input('InpMA1Period', 10)  # Period MA Close
InpMA1Method = _input('InpMA1Method', MODE_SMMA)  # Method MA Close
InpMA1Shift = 0  # Shift  MA Close
InpMA1Price = PRICE_CLOSE  # PriceClose MA Close
InpMA2Period = _input('InpMA2Period', 10)  # Period MA Open
InpMA2Method = _input('InpMA2Method', MODE_SMMA)  # Method MA Open
InpMA2Shift = 0  # Shift  MA Open
InpMA2Price = PRICE_OPEN  # PriceOpen MA Open
delta = _input('delta', 0.0002)  # Delta
InpTEMA1Period = _input('InpTEMA1Period', 20)  # Period TEMA Close
InpTEMA1Shift = 0  # Shift TEMA Close
InpTEMA1Price = PRICE_CLOSE  # PriceClose TEMA Close
InpTEMA2Period = _input('InpTEMA2Period', 20)  # Period TEMA Open
InpTEMA2Shift = 0  # Shift  TEMA Open
InpTEMA2Price = PRICE_OPEN  # PriceOpen TEMA Open
ExtBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
ExtMAOpenBuffer = Arr(0, 0.0)
ExtMACloseBuffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ExtTEMAOpenBuffer = Arr(0, 0.0)
ExtTEMACloseBuffer = Arr(0, 0.0)
ExtTEMABuffer = Arr(0, 0.0)
ExtMAOpenHandle = 0
ExtMACloseHandle = 0
ExtTEMAOpenHandle = 0
ExtTEMACloseHandle = 0
DATA_LIMIT = 0

def OnInit():
    global DATA_LIMIT, ExtMACloseHandle, ExtMAOpenHandle, ExtTEMACloseHandle, ExtTEMAOpenHandle
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtMAOpenBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtMACloseBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtTEMAOpenBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtTEMACloseBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ExtTEMABuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, DATA_LIMIT)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MATEMA (' + _str(InpMA1Period) + ' - ' + _str(InpMA2Period) + ' : ' + _str(InpTEMA1Period) + ' - ' + _str(InpTEMA2Period) + ')')
    ExtMAOpenHandle = iMA(None, 0, InpMA1Period, InpMA1Shift, InpMA1Method, InpMA1Price)
    ExtMACloseHandle = iMA(None, 0, InpMA2Period, InpMA2Shift, InpMA2Method, InpMA2Price)
    ExtTEMAOpenHandle = iTEMA(None, 0, InpTEMA1Period, InpTEMA1Shift, InpTEMA1Price)
    ExtTEMACloseHandle = iTEMA(None, 0, InpTEMA2Period, InpTEMA2Shift, InpTEMA2Price)
    per1 = MathMax(InpMA1Period, InpMA2Period)
    per2 = MathMax(InpTEMA1Period, InpTEMA2Period)
    DATA_LIMIT = MathMax(per1, per2)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= DATA_LIMIT:
        return 0
    calculated = BarsCalculated(ExtTEMACloseHandle)
    if calculated < rates_total:
        Print('Not all data of ExtTEMACloseHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtMAOpenHandle, 0, 0, to_copy, ExtMAOpenBuffer) <= 0:
        Print('Getting MAOpenBuffer is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtMACloseHandle, 0, 0, to_copy, ExtMACloseBuffer) <= 0:
        Print('Getting MACloseBuffer is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtTEMAOpenHandle, 0, 0, to_copy, ExtTEMAOpenBuffer) <= 0:
        Print('Getting TEMAOpenBuffer is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtTEMACloseHandle, 0, 0, to_copy, ExtTEMACloseBuffer) <= 0:
        Print('Getting TEMACloseBuffer is failed! Error', GetLastError())
        return 0
    i = 0
    limit = 0
    if prev_calculated <= DATA_LIMIT:
        i = 0
        for i in range(i, DATA_LIMIT):
            ExtBuffer[i] = 0.0
        else:
            i = _range_end(i, DATA_LIMIT, 1)
        limit = DATA_LIMIT
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtMABuffer[i] = ExtMAOpenBuffer[i] - ExtMACloseBuffer[i]
        ExtTEMABuffer[i] = ExtTEMAOpenBuffer[i] - ExtTEMACloseBuffer[i]
        ExtBuffer[i] = ExtMABuffer[i] + ExtTEMABuffer[i]
        if ExtBuffer[i] > 0.0:
            ExtColorBuffer[i] = 0.0
        else:
            ExtColorBuffer[i] = 1.0
        if MathAbs(ExtBuffer[i]) < delta and ExtColorBuffer[i] < 2.0:
            ExtColorBuffer[i] = 4.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Indmatema(_MQL5Indicator):
    name = 'indmatema'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMA1Period': 10,  # Period MA Close
        'InpMA1Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method MA Close
        'InpMA2Period': 10,  # Period MA Open
        'InpMA2Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method MA Open
        'delta': 0.0002,  # Delta
        'InpTEMA1Period': 20,  # Period TEMA Close
        'InpTEMA2Period': 20,  # Period TEMA Open
    }

