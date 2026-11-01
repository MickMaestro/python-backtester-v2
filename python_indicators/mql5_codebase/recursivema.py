"""RecursiveMA — converted from MQL5: MQL5 Indicators/Recursive Moving Average/RecursiveMA.mq5

Recursive Moving Average Unlimited
Copyright: 2009-2022, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009-2022, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.1', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [11823615], 2: [65535]}, 'widths': {2: 1}, 'styles': {}, 'labels': {2: 'Trigger'}, 'levels': [], 'description': ['Recursive Moving Average Unlimited'], 'name': 'RecursiveMA', 'source': 'MQL5 Indicators/Recursive Moving Average/RecursiveMA.mq5', 'folder': 'Recursive Moving Average', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'int', 'default': 2, 'label': 'period', 'sinput': False}, {'mql': 'InpIteration', 'py': 'InpIteration', 'param': 'InpIteration', 'type': 'int', 'default': 20, 'label': 'number of iterations', 'sinput': False}, {'mql': 'InpMethodMA', 'py': 'InpMethodMA', 'param': 'InpMethodMA', 'type': 'int', 'default': 0, 'label': 'Moving average method', 'sinput': False}, {'mql': 'inpDisplaySignal', 'py': 'inpDisplaySignal', 'param': 'inpDisplaySignal', 'type': 'bool', 'default': False, 'label': 'display arrow', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MA_METHOD_EXT
MOD_EMA = 0
MOD_SMMA = 1
_enum('ENUM_MA_METHOD_EXT', {0: 'MOD_EMA', 1: 'MOD_SMMA'})

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 2)  # period
InpIteration = _input('InpIteration', 20)  # number of iterations
InpMethodMA = _input('InpMethodMA', MOD_EMA)  # Moving average method
inpDisplaySignal = _input('inpDisplaySignal', False)  # display arrow
XemaBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
Ema = Arr(0, 0.0)

def OnInit():
    ObjectsDeleteAll(0, MQLInfoString(MQL_PROGRAM_NAME), 0)
    SetIndexBuffer(0, XemaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Recursive MA')
    PlotIndexSetString(0, PLOT_LABEL, 'Recursive EMA(' + _str(InpPeriodMA) + ',' + _str(InpIteration) + ',' + EnumToString(InpMethodMA, 'ENUM_MA_METHOD_EXT') + ',' + _str(inpDisplaySignal) + ')')
    ArrayResize(Ema, InpIteration)

def OnDeinit(reason):
    ObjectsDeleteAll(0, MQLInfoString(MQL_PROGRAM_NAME), 0)
    Print('OnDeinit', ' Deinitialization reason code = ', reason)
    Print('OnDeinit', ' _UninitReason = ', getUninitReasonText(0))
    Print('OnDeinit', ' UninitializeReason() = ', getUninitReasonText(UninitializeReason()))

def getUninitReasonText(reasonCode):
    text = ''
    _sw1 = reasonCode
    if _sw1 == REASON_ACCOUNT:
        text = 'Account was changed'
    elif _sw1 == REASON_CHARTCHANGE:
        text = 'Symbol or timeframe was changed'
    elif _sw1 == REASON_CHARTCLOSE:
        text = 'Chart was closed'
    elif _sw1 == REASON_PARAMETERS:
        text = 'Input-parameter was changed'
    elif _sw1 == REASON_RECOMPILE:
        text = 'Program ' + 'RecursiveMA.mq5' + ' was recompiled'
    elif _sw1 == REASON_REMOVE:
        text = 'Program ' + 'RecursiveMA.mq5' + ' was removed from chart'
    elif _sw1 == REASON_TEMPLATE:
        text = 'New template was applied to chart'
    else:
        text = 'Another reason'
    return text

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < ((3 * InpPeriodMA) - 3):
        return 0
    limit = 0
    if prev_calculated == 0:
        ArrayInitialize(XemaBuffer, 0)
        ArrayInitialize(TriggerBuffer, 0)
        for i in range(0, ArraySize(Ema)):
            Ema[i] = Open[0]
    else:
        limit = prev_calculated - 1
    if rates_total == prev_calculated:
        return rates_total
    for i in range(limit, rates_total):
        if i > 0:
            for j in range(0, InpIteration):
                if j == 0:
                    if InpMethodMA == MOD_EMA:
                        Ema[j] = _fdiv(Open[i] * 2.0, InpPeriodMA + 1.0) + (Ema[j] * (1 - _fdiv(2.0, InpPeriodMA + 1.0)))
                    else:
                        Ema[j] = _fdiv(Open[i] + (Ema[j] * (MathMin(i, InpPeriodMA) - 1.0)), MathMin(i, InpPeriodMA))
                elif InpMethodMA == MOD_EMA:
                    Ema[j] = _fdiv(Ema[j - 1] * 2.0, InpPeriodMA + 1.0) + (Ema[j] * (1 - _fdiv(2.0, InpPeriodMA + 1.0)))
                else:
                    Ema[j] = _fdiv(Ema[j - 1] + (Ema[j] * (MathMin(i, InpPeriodMA) - 1.0)), MathMin(i, InpPeriodMA))
                if j == 0:
                    TriggerBuffer[i] = _fdiv(((InpIteration - j) * Ema[j]) / InpIteration, InpIteration + 1.0) * 2.0
                else:
                    TriggerBuffer[i] += _fdiv(((InpIteration - j) * Ema[j]) / InpIteration, InpIteration + 1.0) * 2.0
            XemaBuffer[i] = Ema[InpIteration - 1]
            if i > 1 and inpDisplaySignal:
                if TriggerBuffer[i - 0] > XemaBuffer[i - 0] and TriggerBuffer[i - 1] < XemaBuffer[i - 1]:
                    if not ArrowCreate(0, MQLInfoString(MQL_PROGRAM_NAME) + '_ArrowBuy_' + _str(i), 0, Time[i], Open[i] + (SymbolInfoInteger(None, SYMBOL_SPREAD) * Point()), clrLime):
                        return rates_total
                    else:
                        pass
                elif TriggerBuffer[i - 0] < XemaBuffer[i - 0] and TriggerBuffer[i - 1] > XemaBuffer[i - 1]:
                    if not ArrowCreate(0, MQLInfoString(MQL_PROGRAM_NAME) + '_ArrowSell_' + _str(i), 0, Time[i], Open[i], clrRed):
                        return rates_total
    return rates_total

def ArrowCreate(chart_ID=0, name='ArrowBuy', sub_window=0, time=0, price=0.0, clr=0xAC5F03, style=STYLE_SOLID, width=3, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, (OBJ_ARROW_BUY if (clr == clrLime) else OBJ_ARROW_SELL), sub_window, time, price):
        Print('ArrowCreate', ': failed to create "Buy" sign! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RecursiveMA(_MQL5Indicator):
    name = 'RecursiveMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 2,  # period
        'InpIteration': 20,  # number of iterations
        'InpMethodMA': _Choice({0: 'MOD_EMA', 1: 'MOD_SMMA'}, default=0),  # Moving average method
        'inpDisplaySignal': False,  # display arrow
    }

