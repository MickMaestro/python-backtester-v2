"""ytg_ma_tf — converted from MQL5: MQL5 Indicators/ytg_MA_TF/ytg_ma_tf.mq5

ytg_MA_TF
 
site:  http://ytg.com.ua
 
mail:  ytg@ytg.com.ua 
 
Skype:  yuriy.g.t
Copyright: Yuriy Tokman (YTG); Link: http://ytg.com.ua; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Yuriy Tokman (YTG)', 'link': 'http://ytg.com.ua', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'ytg_MA_TF'}, 'levels': [], 'description': ['ytg_MA_TF', ' ', 'site:  http://ytg.com.ua', ' ', 'mail:  ytg@ytg.com.ua ', ' ', 'Skype:  yuriy.g.t'], 'name': 'ytg_ma_tf', 'source': 'MQL5 Indicators/ytg_MA_TF/ytg_ma_tf.mq5', 'folder': 'ytg_MA_TF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'Period_MA', 'py': 'Period_MA', 'param': 'Period_MA', 'type': 'int', 'default': 5, 'label': 'Moving Average period', 'sinput': False}, {'mql': 'Method', 'py': 'Method', 'param': 'Method', 'type': 'int', 'default': 0, 'label': 'method of averaging', 'sinput': False}, {'mql': 'Applied', 'py': 'Applied', 'param': 'Applied', 'type': 'int', 'default': 3, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
Period_MA = _input('Period_MA', 5)  # Moving Average period
Method = _input('Method', MODE_SMA)  # method of averaging
Applied = _input('Applied', PRICE_HIGH)  # Applied price
MaBuffer_High = Arr(0, 0.0)  # indicator buffer
MaArray_TF2 = Arr(0, 0.0)
MaHandle_High = 0
label_name = 'ytg_1'
label_nama = 'ytg_2'

def OnInit():
    global MaHandle_High
    SetIndexBuffer(0, MaBuffer_High, INDICATOR_DATA)
    ArraySetAsSeries(MaBuffer_High, True)
    ArraySetAsSeries(MaArray_TF2, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'ytg_MA_TF(' + _str(Period_MA) + ')')
    MaHandle_High = iMA(None, TimeFrame, Period_MA, 0, Method, Applied)
    ytg_label2()
    ytg_label1()
    return 0

def OnDeinit(reason):
    if ObjectFind(0, label_name) >= 0:
        ObjectDelete(0, label_name)
    if ObjectFind(0, label_nama) >= 0:
        ObjectDelete(0, label_nama)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    bars_TF2 = Bars(None, TimeFrame)
    if bars_TF2 < Period_MA:
        return 0
    calculated_TF2 = 0
    calculated_TF2 = BarsCalculated(MaHandle_High)
    if calculated_TF2 < bars_TF2:
        Print('Not all data of MaHandle_High has been calculated (', calculated_TF2, ' bars). Error', GetLastError())
        return 0
    limit = 0
    if prev_calculated <= 0 or prev_calculated > rates_total:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    for i in range(limit, 0 - 1, -1):
        tempTimeArray_TF2 = Arr(0, 0)
        CopyTime(None, TimeFrame, calculated_TF2 - 1, 1, tempTimeArray_TF2)
        if time[i] < tempTimeArray_TF2[0]:
            MaBuffer_High[i] = EMPTY_VALUE
            continue
        if CopyBuffer(MaHandle_High, 0, _DT(time[i]), 1, MaArray_TF2) <= 0:
            Print('Getting MA TF failed! Error', GetLastError())
            return 0
        else:
            MaBuffer_High[i] = MaArray_TF2[0]
    return rates_total

def ytg_label1():
    if ObjectFind(0, label_name) >= 0:
        ObjectDelete(0, label_name)
    ObjectCreate(0, label_name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, label_name, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, label_name, OBJPROP_XDISTANCE, 10)
    ObjectSetInteger(0, label_name, OBJPROP_YDISTANCE, 25)
    ObjectSetInteger(0, label_name, OBJPROP_COLOR, clrLime)
    ObjectSetString(0, label_name, OBJPROP_TEXT, 'YTG.COM.UA')
    ObjectSetString(0, label_name, OBJPROP_FONT, 'Arial Black')
    ObjectSetInteger(0, label_name, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, label_name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, label_nama, OBJPROP_BACK, False)
    ChartRedraw(0)

def ytg_label2():
    if ObjectFind(0, label_nama) >= 0:
        ObjectDelete(0, label_nama)
    ObjectCreate(0, label_nama, OBJ_RECTANGLE_LABEL, 0, 0, 0)
    ObjectSetInteger(0, label_nama, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, label_nama, OBJPROP_XDISTANCE, 5)
    ObjectSetInteger(0, label_nama, OBJPROP_YDISTANCE, 26)
    ObjectSetInteger(0, label_nama, OBJPROP_BGCOLOR, clrGray)
    ObjectSetInteger(0, label_nama, OBJPROP_BORDER_TYPE, BORDER_RAISED)
    ObjectSetInteger(0, label_nama, OBJPROP_XSIZE, 102)
    ObjectSetInteger(0, label_nama, OBJPROP_YSIZE, 21)
    ObjectSetInteger(0, label_nama, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, label_nama, OBJPROP_BACK, False)
    ChartRedraw(0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YtgMaTf(_MQL5Indicator):
    name = 'ytg_ma_tf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'Period_MA': 5,  # Moving Average period
        'Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # method of averaging
        'Applied': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=3),  # Applied price
    }

