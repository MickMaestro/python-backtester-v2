"""multisignals_pch — converted from MQL5: MQL5 Indicators/MultiSignals_PCH/multisignals_pch.mq5

email: hello.tol64@gmail.com
Copyright: Copyright 2012, tol64.; Link: https://login.mql5.com/ru/users/tol64; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, tol64.', 'link': 'https://login.mql5.com/ru/users/tol64', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 29, 'indicator_plots': 29}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5, 15: 5, 16: 5, 17: 5, 18: 5, 19: 5, 20: 5, 21: 5, 22: 5, 23: 5, 24: 5, 25: 5, 26: 5, 27: 5, 28: 5, 29: 5}, 'colors': {1: [55295], 2: [3145645], 3: [12632256], 4: [12632256], 5: [12632256], 6: [128], 7: [16711680], 8: [128], 9: [16711680], 10: [128], 11: [16711680], 12: [2763429], 13: [14772545], 14: [2763429], 15: [14772545], 16: [2763429], 17: [14772545], 18: [255], 19: [15570276], 20: [255], 21: [15570276], 22: [255], 23: [15570276], 24: [42495], 25: [16776960], 26: [42495], 27: [16776960], 28: [42495], 29: [16776960]}, 'widths': {}, 'styles': {1: 0, 2: 0, 3: 2, 4: 2, 5: 2}, 'labels': {1: 'Channel upper', 2: 'Channel lower', 3: 'Channel median', 4: 'Channel UPmedian', 5: 'Channel DWmedian'}, 'levels': [], 'description': ['email: hello.tol64@gmail.com'], 'name': 'multisignals_pch', 'source': 'MQL5 Indicators/MultiSignals_PCH/multisignals_pch.mq5', 'folder': 'MultiSignals_PCH', 'inputs': [{'mql': 'Period_PCH', 'py': 'Period_PCH', 'param': 'Period_PCH', 'type': 'int', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'MLMH_signal', 'py': 'MLMH_signal', 'param': 'MLMH_signal', 'type': 'bool', 'default': True, 'label': 'ML/MH_PCH signals', 'sinput': False}, {'mql': 'M_signal', 'py': 'M_signal', 'param': 'M_signal', 'type': 'bool', 'default': False, 'label': 'M_PCH signals', 'sinput': False}, {'mql': 'MHML_signal', 'py': 'MHML_signal', 'param': 'MHML_signal', 'type': 'bool', 'default': False, 'label': 'MH/ML_PCH signals', 'sinput': False}, {'mql': 'HL_signal', 'py': 'HL_signal', 'param': 'HL_signal', 'type': 'bool', 'default': False, 'label': 'H/L_PCH signals', 'sinput': False}, {'mql': 'TP_MLMH', 'py': 'TP_MLMH', 'param': 'TP_MLMH', 'type': 'int', 'default': 100, 'label': 'Take Profit MLMH', 'sinput': False}, {'mql': 'TP_M', 'py': 'TP_M', 'param': 'TP_M', 'type': 'int', 'default': 100, 'label': 'Take Profit M', 'sinput': False}, {'mql': 'TP_MHML', 'py': 'TP_MHML', 'param': 'TP_MHML', 'type': 'int', 'default': 100, 'label': 'Take Profit MHML', 'sinput': False}, {'mql': 'TP_HL', 'py': 'TP_HL', 'param': 'TP_HL', 'type': 'int', 'default': 100, 'label': 'Take Profit HL', 'sinput': False}, {'mql': 'SL_MLMH', 'py': 'SL_MLMH', 'param': 'SL_MLMH', 'type': 'int', 'default': 50, 'label': 'Stop Loss MLMH', 'sinput': False}, {'mql': 'SL_M', 'py': 'SL_M', 'param': 'SL_M', 'type': 'int', 'default': 50, 'label': 'Stop Loss M', 'sinput': False}, {'mql': 'SL_MHML', 'py': 'SL_MHML', 'param': 'SL_MHML', 'type': 'int', 'default': 50, 'label': 'Stop Loss MHML', 'sinput': False}, {'mql': 'SL_HL', 'py': 'SL_HL', 'param': 'SL_HL', 'type': 'int', 'default': 50, 'label': 'Stop Loss HL', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_PCH = _input('Period_PCH', 10)  # Period
MLMH_signal = _input('MLMH_signal', True)  # ML/MH_PCH signals
M_signal = _input('M_signal', False)  # M_PCH signals
MHML_signal = _input('MHML_signal', False)  # MH/ML_PCH signals
HL_signal = _input('HL_signal', False)  # H/L_PCH signals
TP_MLMH = _input('TP_MLMH', 100)  # Take Profit MLMH
TP_M = _input('TP_M', 100)  # Take Profit M
TP_MHML = _input('TP_MHML', 100)  # Take Profit MHML
TP_HL = _input('TP_HL', 100)  # Take Profit HL
SL_MLMH = _input('SL_MLMH', 50)  # Stop Loss MLMH
SL_M = _input('SL_M', 50)  # Stop Loss M
SL_MHML = _input('SL_MHML', 50)  # Stop Loss MHML
SL_HL = _input('SL_HL', 50)  # Stop Loss HL
j = 0
tp_MLMH = 0
tp_M = 0
tp_MHML = 0
tp_HL = 0
sl_MLMH = 0
sl_M = 0
sl_MHML = 0
sl_HL = 0
High_Buffer = Arr(0, 0.0)  # Buffers of Lines
Low_Buffer = Arr(0, 0.0)  # Buffers of Lines
Mid_Buffer = Arr(0, 0.0)  # Buffers of Lines
High_Mid_Buffer = Arr(0, 0.0)  # Buffers of Lines
Low_Mid_Buffer = Arr(0, 0.0)  # Buffers of Lines
sCross_MH_Buffer = Arr(0, 0.0)  # Sell
sCross_M_Buffer = Arr(0, 0.0)  # Sell
sCross_ML_Buffer = Arr(0, 0.0)  # Sell
sCross_L_Buffer = Arr(0, 0.0)  # Sell
bCross_ML_Buffer = Arr(0, 0.0)  # Buy
bCross_M_Buffer = Arr(0, 0.0)  # Buy
bCross_MH_Buffer = Arr(0, 0.0)  # Buy
bCross_H_Buffer = Arr(0, 0.0)  # Buy
sTP_MH_Buffer = Arr(0, 0.0)  # Take Profit Sell
sTP_M_Buffer = Arr(0, 0.0)  # Take Profit Sell
sTP_ML_Buffer = Arr(0, 0.0)  # Take Profit Sell
sTP_L_Buffer = Arr(0, 0.0)  # Take Profit Sell
bTP_ML_Buffer = Arr(0, 0.0)  # Take Profit Buy
bTP_M_Buffer = Arr(0, 0.0)  # Take Profit Buy
bTP_MH_Buffer = Arr(0, 0.0)  # Take Profit Buy
bTP_H_Buffer = Arr(0, 0.0)  # Take Profit Buy
sSL_MH_Buffer = Arr(0, 0.0)  # Stop Loss Sell
sSL_M_Buffer = Arr(0, 0.0)  # Stop Loss Sell
sSL_ML_Buffer = Arr(0, 0.0)  # Stop Loss Sell
sSL_L_Buffer = Arr(0, 0.0)  # Stop Loss Sell
bSL_ML_Buffer = Arr(0, 0.0)  # Stop Loss Buy
bSL_M_Buffer = Arr(0, 0.0)  # Stop Loss Buy
bSL_MH_Buffer = Arr(0, 0.0)  # Stop Loss Buy
bSL_H_Buffer = Arr(0, 0.0)  # Stop Loss Buy
ArrayPlotShift = Arr(29, 0, dyn=False)
ArrayPlotDrawBegin = Arr(29, 0, dyn=False)
ArrayPlotEmptyValue = Arr(29, 0, dyn=False)
ArrayPlotLineWidth = Arr(29, 0, dyn=False)

def OnInit():
    global j
    SetIndexBuffer(0, High_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Low_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, Mid_Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, High_Mid_Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, Low_Mid_Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, sCross_MH_Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, bCross_ML_Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, sTP_MH_Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, bTP_ML_Buffer, INDICATOR_DATA)
    SetIndexBuffer(9, sSL_MH_Buffer, INDICATOR_DATA)
    SetIndexBuffer(10, bSL_ML_Buffer, INDICATOR_DATA)
    SetIndexBuffer(11, sCross_M_Buffer, INDICATOR_DATA)
    SetIndexBuffer(12, bCross_M_Buffer, INDICATOR_DATA)
    SetIndexBuffer(13, sTP_M_Buffer, INDICATOR_DATA)
    SetIndexBuffer(14, bTP_M_Buffer, INDICATOR_DATA)
    SetIndexBuffer(15, sSL_M_Buffer, INDICATOR_DATA)
    SetIndexBuffer(16, bSL_M_Buffer, INDICATOR_DATA)
    SetIndexBuffer(17, sCross_ML_Buffer, INDICATOR_DATA)
    SetIndexBuffer(18, bCross_MH_Buffer, INDICATOR_DATA)
    SetIndexBuffer(19, sTP_ML_Buffer, INDICATOR_DATA)
    SetIndexBuffer(20, bTP_MH_Buffer, INDICATOR_DATA)
    SetIndexBuffer(21, sSL_ML_Buffer, INDICATOR_DATA)
    SetIndexBuffer(22, bSL_MH_Buffer, INDICATOR_DATA)
    SetIndexBuffer(23, sCross_L_Buffer, INDICATOR_DATA)
    SetIndexBuffer(24, bCross_H_Buffer, INDICATOR_DATA)
    SetIndexBuffer(25, sTP_L_Buffer, INDICATOR_DATA)
    SetIndexBuffer(26, bTP_H_Buffer, INDICATOR_DATA)
    SetIndexBuffer(27, sSL_L_Buffer, INDICATOR_DATA)
    SetIndexBuffer(28, bSL_H_Buffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() - 1)
    j = 0
    while j < 29:
        PlotIndexSetInteger(j, PLOT_DRAW_BEGIN, Period_PCH)
        j += 1
    j = 0
    while j < 29:
        PlotIndexSetInteger(j, PLOT_SHIFT, 1)
        j += 1
    j = 0
    while j < 29:
        PlotIndexSetInteger(j, PLOT_LINE_WIDTH, 1)
        j += 1
    PlotIndexSetInteger(5, PLOT_ARROW_SHIFT, -40)
    PlotIndexSetInteger(6, PLOT_ARROW_SHIFT, 40)
    PlotIndexSetInteger(11, PLOT_ARROW_SHIFT, -30)
    PlotIndexSetInteger(12, PLOT_ARROW_SHIFT, 30)
    PlotIndexSetInteger(17, PLOT_ARROW_SHIFT, -20)
    PlotIndexSetInteger(18, PLOT_ARROW_SHIFT, 20)
    PlotIndexSetInteger(23, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(24, PLOT_ARROW_SHIFT, 10)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MultiSignals_PCH (' + _str(Period_PCH) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'H_PCH')
    PlotIndexSetString(1, PLOT_LABEL, 'L_PCH')
    PlotIndexSetString(2, PLOT_LABEL, 'M_PCH')
    PlotIndexSetString(3, PLOT_LABEL, 'MH_PCH')
    PlotIndexSetString(4, PLOT_LABEL, 'ML_PCH')
    PlotIndexSetString(5, PLOT_LABEL, 'sell Cross MH')
    PlotIndexSetString(6, PLOT_LABEL, 'buy Cross ML')
    PlotIndexSetString(7, PLOT_LABEL, 'sell TP MH')
    PlotIndexSetString(8, PLOT_LABEL, 'buy TP ML')
    PlotIndexSetString(9, PLOT_LABEL, 'sell SL MH')
    PlotIndexSetString(10, PLOT_LABEL, 'buy SL ML')
    PlotIndexSetString(11, PLOT_LABEL, 'sell Cross M')
    PlotIndexSetString(12, PLOT_LABEL, 'buy Cross M')
    PlotIndexSetString(13, PLOT_LABEL, 'sell TP M')
    PlotIndexSetString(14, PLOT_LABEL, 'buy TP M')
    PlotIndexSetString(15, PLOT_LABEL, 'sell SL M')
    PlotIndexSetString(16, PLOT_LABEL, 'buy SL M')
    PlotIndexSetString(17, PLOT_LABEL, 'sell Cross ML')
    PlotIndexSetString(18, PLOT_LABEL, 'buy Cross MH')
    PlotIndexSetString(19, PLOT_LABEL, 'sell TP ML')
    PlotIndexSetString(20, PLOT_LABEL, 'buy TP MH')
    PlotIndexSetString(21, PLOT_LABEL, 'sell SL ML')
    PlotIndexSetString(22, PLOT_LABEL, 'buy SL MH')
    PlotIndexSetString(23, PLOT_LABEL, 'sell Cross L')
    PlotIndexSetString(24, PLOT_LABEL, 'buy Cross H')
    PlotIndexSetString(25, PLOT_LABEL, 'sell TP L')
    PlotIndexSetString(26, PLOT_LABEL, 'buy TP H')
    PlotIndexSetString(27, PLOT_LABEL, 'sell SL L')
    PlotIndexSetString(28, PLOT_LABEL, 'buy SL H')
    PlotIndexSetInteger(5, PLOT_ARROW, 159)
    PlotIndexSetInteger(6, PLOT_ARROW, 159)
    PlotIndexSetInteger(7, PLOT_ARROW, 167)
    PlotIndexSetInteger(8, PLOT_ARROW, 167)
    PlotIndexSetInteger(9, PLOT_ARROW, 6)
    PlotIndexSetInteger(10, PLOT_ARROW, 6)
    PlotIndexSetInteger(11, PLOT_ARROW, 159)
    PlotIndexSetInteger(12, PLOT_ARROW, 159)
    PlotIndexSetInteger(13, PLOT_ARROW, 167)
    PlotIndexSetInteger(14, PLOT_ARROW, 167)
    PlotIndexSetInteger(15, PLOT_ARROW, 6)
    PlotIndexSetInteger(16, PLOT_ARROW, 6)
    PlotIndexSetInteger(17, PLOT_ARROW, 159)
    PlotIndexSetInteger(18, PLOT_ARROW, 159)
    PlotIndexSetInteger(19, PLOT_ARROW, 167)
    PlotIndexSetInteger(20, PLOT_ARROW, 167)
    PlotIndexSetInteger(21, PLOT_ARROW, 6)
    PlotIndexSetInteger(22, PLOT_ARROW, 6)
    PlotIndexSetInteger(23, PLOT_ARROW, 159)
    PlotIndexSetInteger(24, PLOT_ARROW, 159)
    PlotIndexSetInteger(25, PLOT_ARROW, 167)
    PlotIndexSetInteger(26, PLOT_ARROW, 167)
    PlotIndexSetInteger(27, PLOT_ARROW, 6)
    PlotIndexSetInteger(28, PLOT_ARROW, 6)
    j = 0
    while j < 29:
        PlotIndexSetDouble(j, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        j += 1

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total < Period_PCH:
        return 0
    if prev_calculated == 0:
        limit = Period_PCH
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        High_Buffer[i] = Highest(High, Period_PCH, i)
        Low_Buffer[i] = Lowest(Low, Period_PCH, i)
        Mid_Buffer[i] = (High_Buffer[i] + Low_Buffer[i]) / 2.0
        High_Mid_Buffer[i] = (Mid_Buffer[i] + High_Buffer[i]) / 2.0
        Low_Mid_Buffer[i] = (Low_Buffer[i] + Mid_Buffer[i]) / 2.0
        if MLMH_signal:
            if Open[i] >= High_Mid_Buffer[i - 1] and Close[i] < High_Mid_Buffer[i - 1]:
                sCross_MH_Buffer[i] = High_Buffer[i]
                if TP_MLMH > 0:
                    sTP_MH_Buffer[i] = Close[i] - (vDgtMlt(TP_MLMH) * Point())
                else:
                    sTP_MH_Buffer[i] = EMPTY_VALUE
                if SL_MLMH > 0:
                    sSL_MH_Buffer[i] = Close[i] + (vDgtMlt(SL_MLMH) * Point())
                else:
                    sSL_MH_Buffer[i] = EMPTY_VALUE
            else:
                sCross_MH_Buffer[i] = EMPTY_VALUE
                sTP_MH_Buffer[i] = EMPTY_VALUE
                sSL_MH_Buffer[i] = EMPTY_VALUE
            if Open[i] <= Low_Mid_Buffer[i - 1] and Close[i] > Low_Mid_Buffer[i - 1]:
                bCross_ML_Buffer[i] = Low_Buffer[i]
                if TP_MLMH > 0:
                    bTP_ML_Buffer[i] = Close[i] + (vDgtMlt(TP_MLMH) * Point())
                else:
                    bTP_ML_Buffer[i] = EMPTY_VALUE
                if SL_MLMH > 0:
                    bSL_ML_Buffer[i] = Close[i] - (vDgtMlt(SL_MLMH) * Point())
                else:
                    bSL_ML_Buffer[i] = EMPTY_VALUE
            else:
                bCross_ML_Buffer[i] = EMPTY_VALUE
                bTP_ML_Buffer[i] = EMPTY_VALUE
                bSL_ML_Buffer[i] = EMPTY_VALUE
        elif not MLMH_signal:
            sCross_MH_Buffer[i] = EMPTY_VALUE
            bCross_ML_Buffer[i] = EMPTY_VALUE
            sTP_MH_Buffer[i] = EMPTY_VALUE
            bTP_ML_Buffer[i] = EMPTY_VALUE
            sSL_MH_Buffer[i] = EMPTY_VALUE
            bSL_ML_Buffer[i] = EMPTY_VALUE
        if M_signal:
            if Open[i] >= Mid_Buffer[i - 1] and Close[i] < Mid_Buffer[i - 1]:
                sCross_M_Buffer[i] = High_Buffer[i]
                if TP_M > 0:
                    sTP_M_Buffer[i] = Close[i] - (vDgtMlt(TP_M) * Point())
                else:
                    sTP_M_Buffer[i] = EMPTY_VALUE
                if SL_M > 0:
                    sSL_M_Buffer[i] = Close[i] + (vDgtMlt(SL_M) * Point())
                else:
                    sSL_M_Buffer[i] = EMPTY_VALUE
            else:
                sCross_M_Buffer[i] = EMPTY_VALUE
                sTP_M_Buffer[i] = EMPTY_VALUE
                sSL_M_Buffer[i] = EMPTY_VALUE
            if Open[i] <= Mid_Buffer[i - 1] and Close[i] > Mid_Buffer[i - 1]:
                bCross_M_Buffer[i] = Low_Buffer[i]
                if TP_M > 0:
                    bTP_M_Buffer[i] = Close[i] + (vDgtMlt(TP_M) * Point())
                else:
                    bTP_M_Buffer[i] = EMPTY_VALUE
                if SL_M > 0:
                    bSL_M_Buffer[i] = Close[i] - (vDgtMlt(SL_M) * Point())
                else:
                    bSL_M_Buffer[i] = EMPTY_VALUE
            else:
                bCross_M_Buffer[i] = EMPTY_VALUE
                bTP_M_Buffer[i] = EMPTY_VALUE
                bSL_M_Buffer[i] = EMPTY_VALUE
        elif not M_signal:
            bCross_M_Buffer[i] = EMPTY_VALUE
            bTP_M_Buffer[i] = EMPTY_VALUE
            bSL_M_Buffer[i] = EMPTY_VALUE
            sCross_M_Buffer[i] = EMPTY_VALUE
            sTP_M_Buffer[i] = EMPTY_VALUE
            sSL_M_Buffer[i] = EMPTY_VALUE
        if MHML_signal:
            if Open[i] >= Low_Mid_Buffer[i - 1] and Close[i] < Low_Mid_Buffer[i - 1]:
                sCross_ML_Buffer[i] = High_Buffer[i]
                if TP_MHML > 0:
                    sTP_ML_Buffer[i] = Close[i] - (vDgtMlt(TP_MHML) * Point())
                else:
                    sTP_ML_Buffer[i] = EMPTY_VALUE
                if SL_MHML > 0:
                    sSL_ML_Buffer[i] = Close[i] + (vDgtMlt(SL_MHML) * Point())
                else:
                    sSL_ML_Buffer[i] = EMPTY_VALUE
            else:
                sCross_ML_Buffer[i] = EMPTY_VALUE
                sTP_ML_Buffer[i] = EMPTY_VALUE
                sSL_ML_Buffer[i] = EMPTY_VALUE
            if Open[i] <= High_Mid_Buffer[i - 1] and Close[i] > High_Mid_Buffer[i - 1]:
                bCross_MH_Buffer[i] = Low_Buffer[i]
                if TP_MHML > 0:
                    bTP_MH_Buffer[i] = Close[i] + (vDgtMlt(TP_MHML) * Point())
                else:
                    bTP_MH_Buffer[i] = EMPTY_VALUE
                if SL_MHML > 0:
                    bSL_MH_Buffer[i] = Close[i] - (vDgtMlt(SL_MHML) * Point())
                else:
                    bSL_MH_Buffer[i] = EMPTY_VALUE
            else:
                bCross_MH_Buffer[i] = EMPTY_VALUE
                bTP_MH_Buffer[i] = EMPTY_VALUE
                bSL_MH_Buffer[i] = EMPTY_VALUE
        elif not MHML_signal:
            bCross_MH_Buffer[i] = EMPTY_VALUE
            bTP_MH_Buffer[i] = EMPTY_VALUE
            bSL_MH_Buffer[i] = EMPTY_VALUE
            sCross_ML_Buffer[i] = EMPTY_VALUE
            sTP_ML_Buffer[i] = EMPTY_VALUE
            sSL_ML_Buffer[i] = EMPTY_VALUE
        if HL_signal:
            if Open[i] >= Low_Buffer[i - 1] and Close[i] < Low_Buffer[i - 1]:
                sCross_L_Buffer[i] = High_Buffer[i]
                if TP_HL > 0:
                    sTP_L_Buffer[i] = Close[i] - (vDgtMlt(TP_HL) * Point())
                else:
                    sTP_L_Buffer[i] = EMPTY_VALUE
                if SL_HL > 0:
                    sSL_L_Buffer[i] = Close[i] + (vDgtMlt(SL_HL) * Point())
                else:
                    sSL_L_Buffer[i] = EMPTY_VALUE
            else:
                sCross_L_Buffer[i] = EMPTY_VALUE
                sTP_L_Buffer[i] = EMPTY_VALUE
                sSL_L_Buffer[i] = EMPTY_VALUE
            if Open[i] <= High_Buffer[i - 1] and Close[i] > High_Buffer[i - 1]:
                bCross_H_Buffer[i] = Low_Buffer[i]
                if TP_HL > 0:
                    bTP_H_Buffer[i] = Close[i] + (vDgtMlt(TP_HL) * Point())
                else:
                    bTP_H_Buffer[i] = EMPTY_VALUE
                if SL_HL > 0:
                    bSL_H_Buffer[i] = Close[i] - (vDgtMlt(SL_HL) * Point())
                else:
                    bSL_H_Buffer[i] = EMPTY_VALUE
            else:
                bCross_H_Buffer[i] = EMPTY_VALUE
                bTP_H_Buffer[i] = EMPTY_VALUE
                bSL_H_Buffer[i] = EMPTY_VALUE
        elif not HL_signal:
            sCross_L_Buffer[i] = EMPTY_VALUE
            sTP_L_Buffer[i] = EMPTY_VALUE
            sSL_L_Buffer[i] = EMPTY_VALUE
            bCross_H_Buffer[i] = EMPTY_VALUE
            bTP_H_Buffer[i] = EMPTY_VALUE
            bSL_H_Buffer[i] = EMPTY_VALUE
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def Highest(array, range_, fromIndex):
    i = 0
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res < array[i]:
            res = array[i]
        i -= 1
    return res

def Lowest(array, range_, fromIndex):
    i = 0
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res > array[i]:
            res = array[i]
        i -= 1
    return res

def vDgtMlt(value):
    if Digits() == 3 or Digits() == 5:
        return (value := value * 10)
    else:
        return value


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultisignalsPch(_MQL5Indicator):
    name = 'multisignals_pch'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_PCH': 10,  # Period
        'MLMH_signal': True,  # ML/MH_PCH signals
        'M_signal': False,  # M_PCH signals
        'MHML_signal': False,  # MH/ML_PCH signals
        'HL_signal': False,  # H/L_PCH signals
        'TP_MLMH': 100,  # Take Profit MLMH
        'TP_M': 100,  # Take Profit M
        'TP_MHML': 100,  # Take Profit MHML
        'TP_HL': 100,  # Take Profit HL
        'SL_MLMH': 50,  # Stop Loss MLMH
        'SL_M': 50,  # Stop Loss M
        'SL_MHML': 50,  # Stop Loss MHML
        'SL_HL': 50,  # Stop Loss HL
    }

