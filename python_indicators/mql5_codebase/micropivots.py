"""MicroPivots — converted from MQL5: MQL5 Indicators/MicroPivots/MicroPivots.mq5

Micro Pivots
Shows selected Fibonacci levels between two moving averages
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 17, 'indicator_plots': 15}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}, 'colors': {1: [255], 2: [16748574], 3: [11119017], 4: [11119017], 5: [11119017], 6: [11119017], 7: [11119017], 8: [11119017], 9: [11119017], 10: [11119017], 11: [11119017], 12: [11119017], 13: [11119017], 14: [11119017], 15: [11119017]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}, 'labels': {1: 'MA 1', 2: 'MA 2', 3: 'Level 1', 4: 'Level 2', 5: 'Level 3', 6: 'Level 4', 7: 'Level 5', 8: 'Level 6', 9: 'Level 7', 10: 'Level 8', 11: 'Level 9', 12: 'Level 10', 13: 'Level 11', 14: 'Level 12', 15: 'Level 13'}, 'levels': [], 'description': ['Micro Pivots', 'Shows selected Fibonacci levels between two moving averages'], 'name': 'MicroPivots', 'source': 'MQL5 Indicators/MicroPivots/MicroPivots.mq5', 'folder': 'MicroPivots', 'inputs': [{'mql': 'InpPeriodMA1', 'py': 'InpPeriodMA1', 'param': 'InpPeriodMA1', 'type': 'uint', 'default': 30, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 0, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpAppliedPrice1', 'py': 'InpAppliedPrice1', 'param': 'InpAppliedPrice1', 'type': 'int', 'default': 1, 'label': 'First MA applied price', 'sinput': False}, {'mql': 'InpPeriodMA2', 'py': 'InpPeriodMA2', 'param': 'InpPeriodMA2', 'type': 'uint', 'default': 100, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 0, 'label': 'Second MA method', 'sinput': False}, {'mql': 'InpAppliedPrice2', 'py': 'InpAppliedPrice2', 'param': 'InpAppliedPrice2', 'type': 'int', 'default': 1, 'label': 'Second MA applied price', 'sinput': False}, {'mql': 'InpShowLevel1', 'py': 'InpShowLevel1', 'param': 'InpShowLevel1', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 1', 'sinput': False}, {'mql': 'InpValueLevel1', 'py': 'InpValueLevel1', 'param': 'InpValueLevel1', 'type': 'double', 'default': -423.6, 'label': 'Fibo-level 1 value', 'sinput': False}, {'mql': 'InpShowLevel2', 'py': 'InpShowLevel2', 'param': 'InpShowLevel2', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 2', 'sinput': False}, {'mql': 'InpValueLevel2', 'py': 'InpValueLevel2', 'param': 'InpValueLevel2', 'type': 'double', 'default': -261.8, 'label': 'Fibo-level 2 value', 'sinput': False}, {'mql': 'InpShowLevel3', 'py': 'InpShowLevel3', 'param': 'InpShowLevel3', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 3', 'sinput': False}, {'mql': 'InpValueLevel3', 'py': 'InpValueLevel3', 'param': 'InpValueLevel3', 'type': 'double', 'default': -81.8, 'label': 'Fibo-level 3 value', 'sinput': False}, {'mql': 'InpShowLevel4', 'py': 'InpShowLevel4', 'param': 'InpShowLevel4', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 4', 'sinput': False}, {'mql': 'InpValueLevel4', 'py': 'InpValueLevel4', 'param': 'InpValueLevel4', 'type': 'double', 'default': -27.1, 'label': 'Fibo-level 4 value', 'sinput': False}, {'mql': 'InpShowLevel5', 'py': 'InpShowLevel5', 'param': 'InpShowLevel5', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 5', 'sinput': False}, {'mql': 'InpValueLevel5', 'py': 'InpValueLevel5', 'param': 'InpValueLevel5', 'type': 'double', 'default': 23.6, 'label': 'Fibo-level 5 value', 'sinput': False}, {'mql': 'InpShowLevel6', 'py': 'InpShowLevel6', 'param': 'InpShowLevel6', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 6', 'sinput': False}, {'mql': 'InpValueLevel6', 'py': 'InpValueLevel6', 'param': 'InpValueLevel6', 'type': 'double', 'default': 38.5, 'label': 'Fibo-level 6 value', 'sinput': False}, {'mql': 'InpShowLevel7', 'py': 'InpShowLevel7', 'param': 'InpShowLevel7', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 7', 'sinput': False}, {'mql': 'InpValueLevel7', 'py': 'InpValueLevel7', 'param': 'InpValueLevel7', 'type': 'double', 'default': 50.0, 'label': 'Fibo-level 7 value', 'sinput': False}, {'mql': 'InpShowLevel8', 'py': 'InpShowLevel8', 'param': 'InpShowLevel8', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 8', 'sinput': False}, {'mql': 'InpValueLevel8', 'py': 'InpValueLevel8', 'param': 'InpValueLevel8', 'type': 'double', 'default': 61.8, 'label': 'Fibo-level 8 value', 'sinput': False}, {'mql': 'InpShowLevel9', 'py': 'InpShowLevel9', 'param': 'InpShowLevel9', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 9', 'sinput': False}, {'mql': 'InpValueLevel9', 'py': 'InpValueLevel9', 'param': 'InpValueLevel9', 'type': 'double', 'default': 76.4, 'label': 'Fibo-level 9 value', 'sinput': False}, {'mql': 'InpShowLevel10', 'py': 'InpShowLevel10', 'param': 'InpShowLevel10', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 10', 'sinput': False}, {'mql': 'InpValueLevel10', 'py': 'InpValueLevel10', 'param': 'InpValueLevel10', 'type': 'double', 'default': 127.2, 'label': 'Fibo-level 10 value', 'sinput': False}, {'mql': 'InpShowLevel11', 'py': 'InpShowLevel11', 'param': 'InpShowLevel11', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 11', 'sinput': False}, {'mql': 'InpValueLevel11', 'py': 'InpValueLevel11', 'param': 'InpValueLevel11', 'type': 'double', 'default': 161.8, 'label': 'Fibo-level 11 value', 'sinput': False}, {'mql': 'InpShowLevel12', 'py': 'InpShowLevel12', 'param': 'InpShowLevel12', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 12', 'sinput': False}, {'mql': 'InpValueLevel12', 'py': 'InpValueLevel12', 'param': 'InpValueLevel12', 'type': 'double', 'default': 261.8, 'label': 'Fibo-level 12 value', 'sinput': False}, {'mql': 'InpShowLevel13', 'py': 'InpShowLevel13', 'param': 'InpShowLevel13', 'type': 'int', 'default': 1, 'label': 'Show Fibo-level 13', 'sinput': False}, {'mql': 'InpValueLevel13', 'py': 'InpValueLevel13', 'param': 'InpValueLevel13', 'type': 'double', 'default': 423.6, 'label': 'Fibo-level 13 value', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MA_MODE
METHOD_SMA = 0
METHOD_EMA = 1
METHOD_SMMA = 2
METHOD_LWMA = 3
METHOD_WILDER_EMA = 4
METHOD_SINE_WMA = 5
METHOD_TRI_MA = 6
METHOD_LSMA = 7
METHOD_HMA = 8
METHOD_ZL_EMA = 9
METHOD_ITREND_MA = 10
METHOD_MOVING_MEDIAN = 11
METHOD_GEO_MEAN = 12
METHOD_REMA = 13
METHOD_ILRS = 14
METHOD_IE_2 = 15
METHOD_TRI_MA_GEN = 16
METHOD_VWMA = 17
_enum('ENUM_MA_MODE', {0: 'METHOD_SMA', 1: 'METHOD_EMA', 2: 'METHOD_SMMA', 3: 'METHOD_LWMA', 4: 'METHOD_WILDER_EMA', 5: 'METHOD_SINE_WMA', 6: 'METHOD_TRI_MA', 7: 'METHOD_LSMA', 8: 'METHOD_HMA', 9: 'METHOD_ZL_EMA', 10: 'METHOD_ITREND_MA', 11: 'METHOD_MOVING_MEDIAN', 12: 'METHOD_GEO_MEAN', 13: 'METHOD_REMA', 14: 'METHOD_ILRS', 15: 'METHOD_IE_2', 16: 'METHOD_TRI_MA_GEN', 17: 'METHOD_VWMA'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodMA1 = _input('InpPeriodMA1', 30)  # First MA period
InpMethod1 = _input('InpMethod1', METHOD_SMA)  # First MA method
InpAppliedPrice1 = _input('InpAppliedPrice1', PRICE_CLOSE)  # First MA applied price
InpPeriodMA2 = _input('InpPeriodMA2', 100)  # Second MA period
InpMethod2 = _input('InpMethod2', METHOD_SMA)  # Second MA method
InpAppliedPrice2 = _input('InpAppliedPrice2', PRICE_CLOSE)  # Second MA applied price
InpShowLevel1 = _input('InpShowLevel1', INPUT_YES)  # Show Fibo-level 1
InpValueLevel1 = _input('InpValueLevel1', -423.6)  # Fibo-level 1 value
InpShowLevel2 = _input('InpShowLevel2', INPUT_YES)  # Show Fibo-level 2
InpValueLevel2 = _input('InpValueLevel2', -261.8)  # Fibo-level 2 value
InpShowLevel3 = _input('InpShowLevel3', INPUT_YES)  # Show Fibo-level 3
InpValueLevel3 = _input('InpValueLevel3', -81.8)  # Fibo-level 3 value
InpShowLevel4 = _input('InpShowLevel4', INPUT_YES)  # Show Fibo-level 4
InpValueLevel4 = _input('InpValueLevel4', -27.1)  # Fibo-level 4 value
InpShowLevel5 = _input('InpShowLevel5', INPUT_YES)  # Show Fibo-level 5
InpValueLevel5 = _input('InpValueLevel5', 23.6)  # Fibo-level 5 value
InpShowLevel6 = _input('InpShowLevel6', INPUT_YES)  # Show Fibo-level 6
InpValueLevel6 = _input('InpValueLevel6', 38.5)  # Fibo-level 6 value
InpShowLevel7 = _input('InpShowLevel7', INPUT_YES)  # Show Fibo-level 7
InpValueLevel7 = _input('InpValueLevel7', 50.0)  # Fibo-level 7 value
InpShowLevel8 = _input('InpShowLevel8', INPUT_YES)  # Show Fibo-level 8
InpValueLevel8 = _input('InpValueLevel8', 61.8)  # Fibo-level 8 value
InpShowLevel9 = _input('InpShowLevel9', INPUT_YES)  # Show Fibo-level 9
InpValueLevel9 = _input('InpValueLevel9', 76.4)  # Fibo-level 9 value
InpShowLevel10 = _input('InpShowLevel10', INPUT_YES)  # Show Fibo-level 10
InpValueLevel10 = _input('InpValueLevel10', 127.2)  # Fibo-level 10 value
InpShowLevel11 = _input('InpShowLevel11', INPUT_YES)  # Show Fibo-level 11
InpValueLevel11 = _input('InpValueLevel11', 161.8)  # Fibo-level 11 value
InpShowLevel12 = _input('InpShowLevel12', INPUT_YES)  # Show Fibo-level 12
InpValueLevel12 = _input('InpValueLevel12', 261.8)  # Fibo-level 12 value
InpShowLevel13 = _input('InpShowLevel13', INPUT_YES)  # Show Fibo-level 13
InpValueLevel13 = _input('InpValueLevel13', 423.6)  # Fibo-level 13 value
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferLevel1 = Arr(0, 0.0)
BufferLevel2 = Arr(0, 0.0)
BufferLevel3 = Arr(0, 0.0)
BufferLevel4 = Arr(0, 0.0)
BufferLevel5 = Arr(0, 0.0)
BufferLevel6 = Arr(0, 0.0)
BufferLevel7 = Arr(0, 0.0)
BufferLevel8 = Arr(0, 0.0)
BufferLevel9 = Arr(0, 0.0)
BufferLevel10 = Arr(0, 0.0)
BufferLevel11 = Arr(0, 0.0)
BufferLevel12 = Arr(0, 0.0)
BufferLevel13 = Arr(0, 0.0)
BufferPrice1 = Arr(0, 0.0)
BufferPrice2 = Arr(0, 0.0)
level1 = 0.0
level2 = 0.0
level3 = 0.0
level4 = 0.0
level5 = 0.0
level6 = 0.0
level7 = 0.0
level8 = 0.0
level9 = 0.0
level10 = 0.0
level11 = 0.0
level12 = 0.0
level13 = 0.0
period_ma1 = 0
period_ma2 = 0
period_max = 0
handle_ma1 = 0
handle_ma2 = 0

def OnInit():
    global handle_ma1, handle_ma2, level1, level10, level11, level12, level13, level2, level3, level4, level5, level6, level7, level8, level9, period_ma1, period_ma2, period_max
    period_ma1 = (2 if (InpPeriodMA1 < 2) else InpPeriodMA1)
    period_ma2 = (2 if (InpPeriodMA2 < 2) else InpPeriodMA2)
    period_max = fmax(period_ma1, period_ma2)
    level1 = InpValueLevel1
    level2 = InpValueLevel2
    level3 = InpValueLevel3
    level4 = InpValueLevel4
    level5 = InpValueLevel5
    level6 = InpValueLevel6
    level7 = InpValueLevel7
    level8 = InpValueLevel8
    level9 = InpValueLevel9
    level10 = InpValueLevel10
    level11 = InpValueLevel11
    level12 = InpValueLevel12
    level13 = InpValueLevel13
    SetIndexBuffer(0, BufferMA1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLevel1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLevel2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferLevel3, INDICATOR_DATA)
    SetIndexBuffer(5, BufferLevel4, INDICATOR_DATA)
    SetIndexBuffer(6, BufferLevel5, INDICATOR_DATA)
    SetIndexBuffer(7, BufferLevel6, INDICATOR_DATA)
    SetIndexBuffer(8, BufferLevel7, INDICATOR_DATA)
    SetIndexBuffer(9, BufferLevel8, INDICATOR_DATA)
    SetIndexBuffer(10, BufferLevel9, INDICATOR_DATA)
    SetIndexBuffer(11, BufferLevel10, INDICATOR_DATA)
    SetIndexBuffer(12, BufferLevel11, INDICATOR_DATA)
    SetIndexBuffer(13, BufferLevel12, INDICATOR_DATA)
    SetIndexBuffer(14, BufferLevel13, INDICATOR_DATA)
    SetIndexBuffer(15, BufferPrice1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, BufferPrice2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MicroPivots (' + _str(period_ma1) + ', ' + _str(period_ma2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(9, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(10, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(11, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(12, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(13, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(14, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetString(0, PLOT_LABEL, 'MP MA1 (' + _str(period_ma1) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'MP MA2 (' + _str(period_ma2) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Fibo1 (' + DoubleToString(level1, 1) + ')')
    PlotIndexSetString(3, PLOT_LABEL, 'Fibo2 (' + DoubleToString(level2, 1) + ')')
    PlotIndexSetString(4, PLOT_LABEL, 'Fibo3 (' + DoubleToString(level3, 1) + ')')
    PlotIndexSetString(5, PLOT_LABEL, 'Fibo4 (' + DoubleToString(level4, 1) + ')')
    PlotIndexSetString(6, PLOT_LABEL, 'Fibo5 (' + DoubleToString(level5, 1) + ')')
    PlotIndexSetString(7, PLOT_LABEL, 'Fibo6 (' + DoubleToString(level6, 1) + ')')
    PlotIndexSetString(8, PLOT_LABEL, 'Fibo7 (' + DoubleToString(level7, 1) + ')')
    PlotIndexSetString(9, PLOT_LABEL, 'Fibo8 (' + DoubleToString(level8, 1) + ')')
    PlotIndexSetString(10, PLOT_LABEL, 'Fibo9 (' + DoubleToString(level9, 1) + ')')
    PlotIndexSetString(11, PLOT_LABEL, 'Fibo10 (' + DoubleToString(level10, 1) + ')')
    PlotIndexSetString(12, PLOT_LABEL, 'Fibo11 (' + DoubleToString(level11, 1) + ')')
    PlotIndexSetString(13, PLOT_LABEL, 'Fibo12 (' + DoubleToString(level12, 1) + ')')
    PlotIndexSetString(14, PLOT_LABEL, 'Fibo13 (' + DoubleToString(level13, 1) + ')')
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, InpShowLevel1)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, InpShowLevel2)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, InpShowLevel3)
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, InpShowLevel4)
    PlotIndexSetInteger(6, PLOT_DRAW_TYPE, InpShowLevel5)
    PlotIndexSetInteger(7, PLOT_DRAW_TYPE, InpShowLevel6)
    PlotIndexSetInteger(8, PLOT_DRAW_TYPE, InpShowLevel7)
    PlotIndexSetInteger(9, PLOT_DRAW_TYPE, InpShowLevel8)
    PlotIndexSetInteger(10, PLOT_DRAW_TYPE, InpShowLevel9)
    PlotIndexSetInteger(11, PLOT_DRAW_TYPE, InpShowLevel10)
    PlotIndexSetInteger(12, PLOT_DRAW_TYPE, InpShowLevel11)
    PlotIndexSetInteger(13, PLOT_DRAW_TYPE, InpShowLevel12)
    PlotIndexSetInteger(14, PLOT_DRAW_TYPE, InpShowLevel13)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferLevel1, True)
    ArraySetAsSeries(BufferLevel2, True)
    ArraySetAsSeries(BufferLevel3, True)
    ArraySetAsSeries(BufferLevel4, True)
    ArraySetAsSeries(BufferLevel5, True)
    ArraySetAsSeries(BufferLevel6, True)
    ArraySetAsSeries(BufferLevel7, True)
    ArraySetAsSeries(BufferLevel8, True)
    ArraySetAsSeries(BufferLevel9, True)
    ArraySetAsSeries(BufferLevel10, True)
    ArraySetAsSeries(BufferLevel11, True)
    ArraySetAsSeries(BufferLevel12, True)
    ArraySetAsSeries(BufferLevel13, True)
    ArraySetAsSeries(BufferPrice1, True)
    ArraySetAsSeries(BufferPrice2, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice1)
    if handle_ma1 == INVALID_HANDLE:
        Print(315, ': The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice2)
    if handle_ma2 == INVALID_HANDLE:
        Print(321, ': The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferLevel1, 0)
        ArrayInitialize(BufferLevel2, 0)
        ArrayInitialize(BufferLevel3, 0)
        ArrayInitialize(BufferLevel4, 0)
        ArrayInitialize(BufferLevel5, 0)
        ArrayInitialize(BufferLevel6, 0)
        ArrayInitialize(BufferLevel7, 0)
        ArrayInitialize(BufferLevel8, 0)
        ArrayInitialize(BufferLevel9, 0)
        ArrayInitialize(BufferLevel10, 0)
        ArrayInitialize(BufferLevel11, 0)
        ArrayInitialize(BufferLevel12, 0)
        ArrayInitialize(BufferLevel13, 0)
        ArrayInitialize(BufferPrice1, 0)
        ArrayInitialize(BufferPrice2, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferPrice1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferPrice2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        _sw1 = InpMethod1
        if _sw1 == METHOD_EMA:
            BufferMA1[i] = EMA(rates_total, BufferPrice1[i], BufferMA1[i + 1], period_ma1, i)
        elif _sw1 == METHOD_SMMA:
            BufferMA1[i] = SMMA(rates_total, BufferPrice1, BufferMA1[i + 1], period_ma1, i)
        elif _sw1 == METHOD_LWMA:
            BufferMA1[i] = LWMA(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_WILDER_EMA:
            BufferMA1[i] = Wilder(rates_total, BufferPrice1[i], BufferMA1[i + 1], period_ma1, i)
        elif _sw1 == METHOD_SINE_WMA:
            BufferMA1[i] = SineWMA(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_TRI_MA:
            BufferMA1[i] = TriMA(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_LSMA:
            BufferMA1[i] = LSMA(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_HMA:
            BufferMA1[i] = HMA(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_ZL_EMA:
            BufferMA1[i] = ZeroLagEMA(rates_total, BufferPrice1, BufferMA1[i + 1], period_ma1, i)
        elif _sw1 == METHOD_ITREND_MA:
            BufferMA1[i] = ITrend(rates_total, BufferPrice1, BufferMA1, period_ma1, i)
        elif _sw1 == METHOD_MOVING_MEDIAN:
            BufferMA1[i] = Median(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_GEO_MEAN:
            BufferMA1[i] = GeoMean(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_REMA:
            BufferMA1[i] = REMA(rates_total, BufferPrice1[i], BufferMA1, period_ma1, 0.5, i)
        elif _sw1 == METHOD_ILRS:
            BufferMA1[i] = ILRS(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_IE_2:
            BufferMA1[i] = IE2(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_TRI_MA_GEN:
            BufferMA1[i] = TriMA_gen(rates_total, BufferPrice1, period_ma1, i)
        elif _sw1 == METHOD_VWMA:
            BufferMA1[i] = VWMA(rates_total, BufferPrice1, tick_volume, period_ma1, i)
        else:
            BufferMA1[i] = SMA(rates_total, BufferPrice1, period_ma1, i)
        _sw2 = InpMethod2
        if _sw2 == METHOD_EMA:
            BufferMA2[i] = EMA(rates_total, BufferPrice2[i], BufferMA2[i + 1], period_ma2, i)
        elif _sw2 == METHOD_SMMA:
            BufferMA2[i] = SMMA(rates_total, BufferPrice2, BufferMA2[i + 1], period_ma2, i)
        elif _sw2 == METHOD_LWMA:
            BufferMA2[i] = LWMA(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_WILDER_EMA:
            BufferMA2[i] = Wilder(rates_total, BufferPrice2[i], BufferMA2[i + 1], period_ma2, i)
        elif _sw2 == METHOD_SINE_WMA:
            BufferMA2[i] = SineWMA(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_TRI_MA:
            BufferMA2[i] = TriMA(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_LSMA:
            BufferMA2[i] = LSMA(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_HMA:
            BufferMA2[i] = HMA(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_ZL_EMA:
            BufferMA2[i] = ZeroLagEMA(rates_total, BufferPrice2, BufferMA2[i + 1], period_ma2, i)
        elif _sw2 == METHOD_ITREND_MA:
            BufferMA2[i] = ITrend(rates_total, BufferPrice2, BufferMA2, period_ma2, i)
        elif _sw2 == METHOD_MOVING_MEDIAN:
            BufferMA2[i] = Median(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_GEO_MEAN:
            BufferMA2[i] = GeoMean(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_REMA:
            BufferMA2[i] = REMA(rates_total, BufferPrice2[i], BufferMA2, period_ma2, 0.5, i)
        elif _sw2 == METHOD_ILRS:
            BufferMA2[i] = ILRS(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_IE_2:
            BufferMA2[i] = IE2(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_TRI_MA_GEN:
            BufferMA2[i] = TriMA_gen(rates_total, BufferPrice2, period_ma2, i)
        elif _sw2 == METHOD_VWMA:
            BufferMA2[i] = VWMA(rates_total, BufferPrice2, tick_volume, period_ma2, i)
        else:
            BufferMA2[i] = SMA(rates_total, BufferPrice2, period_ma2, i)
        abs_ = (fabs(BufferMA1[i] - BufferMA2[i]) if (BufferMA1[i] > BufferMA2[i]) else (-fabs(BufferMA1[i] - BufferMA2[i])))
        BufferLevel1[i] = BufferMA2[i] + (abs_ * (level1 / 100.0))
        BufferLevel2[i] = BufferMA2[i] + (abs_ * (level2 / 100.0))
        BufferLevel3[i] = BufferMA2[i] + (abs_ * (level3 / 100.0))
        BufferLevel4[i] = BufferMA2[i] + (abs_ * (level4 / 100.0))
        BufferLevel5[i] = BufferMA2[i] + (abs_ * (level5 / 100.0))
        BufferLevel6[i] = BufferMA2[i] + (abs_ * (level6 / 100.0))
        BufferLevel7[i] = BufferMA2[i] + (abs_ * (level7 / 100.0))
        BufferLevel8[i] = BufferMA2[i] + (abs_ * (level8 / 100.0))
        BufferLevel9[i] = BufferMA2[i] + (abs_ * (level9 / 100.0))
        BufferLevel10[i] = BufferMA2[i] + (abs_ * (level10 / 100.0))
        BufferLevel11[i] = BufferMA2[i] + (abs_ * (level11 / 100.0))
        BufferLevel12[i] = BufferMA2[i] + (abs_ * (level12 / 100.0))
        BufferLevel13[i] = BufferMA2[i] + (abs_ * (level13 / 100.0))
    return rates_total

def SMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return array_src[shift]
    sum_ = 0.0
    for i in range(0, period):
        sum_ += array_src[shift + i]
    return _fdiv(sum_, period)

def EMA(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + (_fdiv(2.0, 1 + period) * (price - prev))))

def Wilder(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + _fdiv(price - prev, period)))

def LWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += period - i
        sum_ += array_src[shift + i] * (period - i)
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def SineWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += sin(_fdiv(M_PI * (i + 1), period + 1))
        sum_ += array_src[shift + i] * sin(_fdiv(M_PI * (i + 1), period + 1))
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def TriMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sma = 0.0
    len_ = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len_):
        sma = SMA(rates_total, array_src, len_, shift + i)
        sum_ += sma
    trima = _fdiv(sum_, len_)
    return trima

def LSMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    for i in range(period, 1 - 1, -1):
        sum_ += (i - ((period + 1) / 3.0)) * array_src[shift + period - i]
    lsma = _fdiv(sum_ * 6.0, period * (period + 1))
    return lsma

def SMMA(rates_total, array_src, prev, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    smma = 0.0
    if shift == (rates_total - period - 1):
        smma = SMA(rates_total, array_src, period, shift)
    elif shift < (rates_total - period - 1):
        sum_ = 0.0
        for i in range(0, period):
            sum_ += array_src[shift + i + 1]
        smma = _fdiv(sum_ - prev + array_src[shift], period)
    return smma

def HMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    tmp1 = Arr(0, 0.0)
    hma = 0.0
    len_ = _int(sqrt(period))
    ArrayResize(tmp1, len_)
    if shift == (rates_total - period - 1):
        hma = array_src[shift]
    elif shift < (rates_total - period - 1):
        for i in range(0, len_):
            tmp1[i] = (2.0 * LWMA(rates_total, array_src, _idiv(period, 2), shift + i)) - LWMA(rates_total, array_src, period, shift + i)
        hma = LWMA(rates_total, tmp1, len_, 0)
    return hma

def ZeroLagEMA(rates_total, array_src, prev, period, shift):
    alfa = _fdiv(2.0, 1 + period)
    lag = _int(0.5 * (period - 1))
    return (array_src[shift] if (shift >= (rates_total - lag)) else ((alfa * ((2.0 * array_src[shift]) - array_src[shift + lag])) + ((1 - alfa) * prev)))

def ITrend(rates_total, array_src, array, period, shift):
    alfa = _fdiv(2.0, period + 1)
    return ((((alfa - (0.25 * alfa * alfa)) * array_src[shift]) + (0.5 * alfa * alfa * array_src[shift + 1]) - ((alfa - (0.75 * alfa * alfa)) * array_src[shift + 2]) + (2 * (1 - alfa) * array[shift + 1]) - ((1 - alfa) * (1 - alfa) * array[shift + 2])) if (shift < (rates_total - 7)) else ((array_src[shift] + (2 * array_src[shift + 1]) + array_src[shift + 2]) / 4.0))

def Median(rates_total, array_src, period, shift):
    if period < 2 or shift > (rates_total - period - 1):
        return 0.0
    array = Arr(0, 0.0)
    ArrayResize(array, period)
    for i in range(0, period):
        array[i] = array_src[shift + i]
    ArraySort(array)
    num = _int(round(_idiv(period - 1, 2)))
    return (array_src[num] if (fmod(period, 2) > 0) else (0.5 * (array_src[num] + array[num + 1])))

def GeoMean(rates_total, array_src, period, shift):
    gmean = 0.0
    if shift < (rates_total - period):
        gmean = pow(array_src[shift], _fdiv(1.0, period))
        for i in range(1, period):
            gmean *= pow(array_src[shift + i], _fdiv(1.0, period))
    return gmean

def REMA(rates_total, price, array, period, lambda_, shift):
    alpha = _fdiv(2.0, period + 1)
    return (price if (shift >= (rates_total - 3)) else _fdiv((array[shift + 1] * (1 + (2 * lambda_))) + (alpha * (price - array[shift + 1])) - (lambda_ * array[shift + 2]), 1 + lambda_))

def ILRS(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = period * (period - 1) * 0.5
    sum2 = ((period - 1) * period * ((2 * period) - 1)) / 6.0
    sum1 = 0.0
    sumy = 0.0
    for i in range(0, period):
        sum1 += i * array_src[shift + i]
        sumy += array_src[shift + i]
    num1 = (period * sum1) - (sum_ * sumy)
    num2 = (sum_ * sum_) - (period * sum2)
    slope = (_fdiv(num1, num2) if (num2 != 0) else 0)
    return slope + SMA(rates_total, array_src, period, shift)

def IE2(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    return 0.5 * (ILRS(rates_total, array_src, period, shift) + LSMA(rates_total, array_src, period, shift))

def TriMA_gen(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    len1 = _int(floor((period + 1) * 0.5))
    len2 = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len2):
        sum_ += SMA(rates_total, array_src, len1, shift + i)
    return _fdiv(sum_, len2)

def VWMA(rates_total, array_src, volume, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += float(volume[shift + i])
        sum_ += array_src[shift + i] * volume[shift + i]
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_MODE'), 7)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MicroPivots(_MQL5Indicator):
    name = 'MicroPivots'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA1': 30,  # First MA period
        'InpMethod1': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=0),  # First MA method
        'InpAppliedPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # First MA applied price
        'InpPeriodMA2': 100,  # Second MA period
        'InpMethod2': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=0),  # Second MA method
        'InpAppliedPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Second MA applied price
        'InpShowLevel1': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 1
        'InpValueLevel1': -423.6,  # Fibo-level 1 value
        'InpShowLevel2': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 2
        'InpValueLevel2': -261.8,  # Fibo-level 2 value
        'InpShowLevel3': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 3
        'InpValueLevel3': -81.8,  # Fibo-level 3 value
        'InpShowLevel4': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 4
        'InpValueLevel4': -27.1,  # Fibo-level 4 value
        'InpShowLevel5': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 5
        'InpValueLevel5': 23.6,  # Fibo-level 5 value
        'InpShowLevel6': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 6
        'InpValueLevel6': 38.5,  # Fibo-level 6 value
        'InpShowLevel7': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 7
        'InpValueLevel7': 50.0,  # Fibo-level 7 value
        'InpShowLevel8': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 8
        'InpValueLevel8': 61.8,  # Fibo-level 8 value
        'InpShowLevel9': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 9
        'InpValueLevel9': 76.4,  # Fibo-level 9 value
        'InpShowLevel10': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 10
        'InpValueLevel10': 127.2,  # Fibo-level 10 value
        'InpShowLevel11': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 11
        'InpValueLevel11': 161.8,  # Fibo-level 11 value
        'InpShowLevel12': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 12
        'InpValueLevel12': 261.8,  # Fibo-level 12 value
        'InpShowLevel13': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Fibo-level 13
        'InpValueLevel13': 423.6,  # Fibo-level 13 value
    }

