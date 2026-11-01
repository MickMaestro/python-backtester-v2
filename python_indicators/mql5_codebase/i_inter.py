"""i_inter — converted from MQL5: MQL5 Indicators/Inter/i_inter.mq5

Copyright: Copyright 2012, her.human; Link: her.human@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, her.human', 'link': 'her.human@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 10}, 'types': {10: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'colors': {10: [13828244], 1: [255], 2: [42495], 3: [65535], 4: [32768], 5: [65280], 6: [15128749], 7: [16711680], 8: [15631086], 9: [16711935]}, 'widths': {10: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'styles': {10: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'labels': {10: 'in0', 1: 'in1', 2: 'in2', 3: 'in3', 4: 'in4', 5: 'in5', 6: 'in6', 7: 'in7', 8: 'in8', 9: 'in9'}, 'levels': [], 'description': [], 'name': 'i_inter', 'source': 'MQL5 Indicators/Inter/i_inter.mq5', 'folder': 'Inter', 'inputs': [{'mql': 'symbol0', 'py': 'symbol0', 'param': 'symbol0', 'type': 'int', 'default': 1, 'label': '----- Instrument 1 ------', 'sinput': False}, {'mql': 'var0', 'py': 'var0', 'param': 'var0', 'type': 'int', 'default': 1, 'label': 'Variant 1', 'sinput': False}, {'mql': 'tf0', 'py': 'tf0', 'param': 'tf0', 'type': 'int', 'default': 0, 'label': 'Timeframe 1', 'sinput': False}, {'mql': 'param0', 'py': 'param0', 'param': 'param0', 'type': 'int', 'default': 5, 'label': 'Parametr 1', 'sinput': False}, {'mql': 'symbol1', 'py': 'symbol1', 'param': 'symbol1', 'type': 'int', 'default': 2, 'label': '----- Instrument 2 ------', 'sinput': False}, {'mql': 'var1', 'py': 'var1', 'param': 'var1', 'type': 'int', 'default': 1, 'label': 'Variant 2', 'sinput': False}, {'mql': 'tf1', 'py': 'tf1', 'param': 'tf1', 'type': 'int', 'default': 0, 'label': 'Timeframe 2', 'sinput': False}, {'mql': 'param1', 'py': 'param1', 'param': 'param1', 'type': 'int', 'default': 5, 'label': 'Parametr 2', 'sinput': False}, {'mql': 'symbol2', 'py': 'symbol2', 'param': 'symbol2', 'type': 'int', 'default': 1, 'label': '----- Instrument 3 ------', 'sinput': False}, {'mql': 'var2', 'py': 'var2', 'param': 'var2', 'type': 'int', 'default': 1, 'label': 'Variant 3', 'sinput': False}, {'mql': 'tf2', 'py': 'tf2', 'param': 'tf2', 'type': 'int', 'default': 0, 'label': 'Timeframe 3', 'sinput': False}, {'mql': 'param2', 'py': 'param2', 'param': 'param2', 'type': 'int', 'default': 20, 'label': 'Parametr 3', 'sinput': False}, {'mql': 'symbol3', 'py': 'symbol3', 'param': 'symbol3', 'type': 'int', 'default': 2, 'label': '----- Instrument 4 ------', 'sinput': False}, {'mql': 'var3', 'py': 'var3', 'param': 'var3', 'type': 'int', 'default': 1, 'label': 'Variant 4', 'sinput': False}, {'mql': 'tf3', 'py': 'tf3', 'param': 'tf3', 'type': 'int', 'default': 0, 'label': 'Timeframe 4', 'sinput': False}, {'mql': 'param3', 'py': 'param3', 'param': 'param3', 'type': 'int', 'default': 20, 'label': 'Parametr 4', 'sinput': False}, {'mql': 'symbol4', 'py': 'symbol4', 'param': 'symbol4', 'type': 'int', 'default': 1, 'label': '----- Instrument 5 ------', 'sinput': False}, {'mql': 'var4', 'py': 'var4', 'param': 'var4', 'type': 'int', 'default': 1, 'label': 'Variant 5', 'sinput': False}, {'mql': 'tf4', 'py': 'tf4', 'param': 'tf4', 'type': 'int', 'default': 0, 'label': 'Timeframe 5', 'sinput': False}, {'mql': 'param4', 'py': 'param4', 'param': 'param4', 'type': 'int', 'default': 50, 'label': 'Parametr 5', 'sinput': False}, {'mql': 'symbol5', 'py': 'symbol5', 'param': 'symbol5', 'type': 'int', 'default': 2, 'label': '----- Instrument 6 ------', 'sinput': False}, {'mql': 'var5', 'py': 'var5', 'param': 'var5', 'type': 'int', 'default': 1, 'label': 'Variant 6', 'sinput': False}, {'mql': 'tf5', 'py': 'tf5', 'param': 'tf5', 'type': 'int', 'default': 0, 'label': 'Timeframe 6', 'sinput': False}, {'mql': 'param5', 'py': 'param5', 'param': 'param5', 'type': 'int', 'default': 50, 'label': 'Parametr 6', 'sinput': False}, {'mql': 'symbol6', 'py': 'symbol6', 'param': 'symbol6', 'type': 'int', 'default': 1, 'label': '----- Instrument 7 ------', 'sinput': False}, {'mql': 'var6', 'py': 'var6', 'param': 'var6', 'type': 'int', 'default': 0, 'label': 'Variant 7', 'sinput': False}, {'mql': 'tf6', 'py': 'tf6', 'param': 'tf6', 'type': 'int', 'default': 0, 'label': 'Timeframe 7', 'sinput': False}, {'mql': 'param6', 'py': 'param6', 'param': 'param6', 'type': 'int', 'default': 20, 'label': 'Parametr 7', 'sinput': False}, {'mql': 'symbol7', 'py': 'symbol7', 'param': 'symbol7', 'type': 'int', 'default': 2, 'label': '----- Instrument 8 ------', 'sinput': False}, {'mql': 'var7', 'py': 'var7', 'param': 'var7', 'type': 'int', 'default': 0, 'label': 'Variant 8', 'sinput': False}, {'mql': 'tf7', 'py': 'tf7', 'param': 'tf7', 'type': 'int', 'default': 0, 'label': 'Timeframe 8', 'sinput': False}, {'mql': 'param7', 'py': 'param7', 'param': 'param7', 'type': 'int', 'default': 20, 'label': 'Parametr 8', 'sinput': False}, {'mql': 'symbol8', 'py': 'symbol8', 'param': 'symbol8', 'type': 'int', 'default': 0, 'label': '----- Instrument 9 ------', 'sinput': False}, {'mql': 'var8', 'py': 'var8', 'param': 'var8', 'type': 'int', 'default': 7, 'label': 'Variant 9', 'sinput': False}, {'mql': 'tf8', 'py': 'tf8', 'param': 'tf8', 'type': 'int', 'default': 0, 'label': 'Timeframe 9', 'sinput': False}, {'mql': 'param8', 'py': 'param8', 'param': 'param8', 'type': 'int', 'default': 0, 'label': 'Parametr 9', 'sinput': False}, {'mql': 'symbol9', 'py': 'symbol9', 'param': 'symbol9', 'type': 'int', 'default': 0, 'label': '----- Instrument 10 ------', 'sinput': False}, {'mql': 'var9', 'py': 'var9', 'param': 'var9', 'type': 'int', 'default': 7, 'label': 'Variant 10', 'sinput': False}, {'mql': 'tf9', 'py': 'tf9', 'param': 'tf9', 'type': 'int', 'default': 0, 'label': 'Timeframe 10', 'sinput': False}, {'mql': 'param9', 'py': 'param9', 'param': 'param9', 'type': 'int', 'default': 1, 'label': 'Parametr 10', 'sinput': False}, {'mql': 'max_bars', 'py': 'max_bars', 'param': 'max_bars', 'type': 'int', 'default': 100, 'label': 'Maximum Bars Calculate', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter

# enum variant
NONE = 0
HLP = 1
Op0_OpN = 2
RSI = 3
Stoch = 4
Op0_Ma = 5
Ma0_Ma1 = 6
Time = 7
_enum('variant', {0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'})

# enum instrument
CURRENT = 0
EURUSD = 1
GBPUSD = 2
USDCHF = 3
USDJPY = 4
USDCAD = 5
AUDUSD = 6
NZDUSD = 7
EURGBP = 8
EURJPY = 9
EURCAD = 10
XAUUSD = 11
XAGUSD = 12
_enum('instrument', {0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'})

# ---- inputs and global variables
symbol0 = _input('symbol0', EURUSD)  # ----- Instrument 1 ------
var0 = _input('var0', HLP)  # Variant 1
tf0 = _input('tf0', PERIOD_CURRENT)  # Timeframe 1
param0 = _input('param0', 5)  # Parametr 1
symbol1 = _input('symbol1', GBPUSD)  # ----- Instrument 2 ------
var1 = _input('var1', HLP)  # Variant 2
tf1 = _input('tf1', PERIOD_CURRENT)  # Timeframe 2
param1 = _input('param1', 5)  # Parametr 2
symbol2 = _input('symbol2', EURUSD)  # ----- Instrument 3 ------
var2 = _input('var2', HLP)  # Variant 3
tf2 = _input('tf2', PERIOD_CURRENT)  # Timeframe 3
param2 = _input('param2', 20)  # Parametr 3
symbol3 = _input('symbol3', GBPUSD)  # ----- Instrument 4 ------
var3 = _input('var3', HLP)  # Variant 4
tf3 = _input('tf3', PERIOD_CURRENT)  # Timeframe 4
param3 = _input('param3', 20)  # Parametr 4
symbol4 = _input('symbol4', EURUSD)  # ----- Instrument 5 ------
var4 = _input('var4', HLP)  # Variant 5
tf4 = _input('tf4', PERIOD_CURRENT)  # Timeframe 5
param4 = _input('param4', 50)  # Parametr 5
symbol5 = _input('symbol5', GBPUSD)  # ----- Instrument 6 ------
var5 = _input('var5', HLP)  # Variant 6
tf5 = _input('tf5', PERIOD_CURRENT)  # Timeframe 6
param5 = _input('param5', 50)  # Parametr 6
symbol6 = _input('symbol6', EURUSD)  # ----- Instrument 7 ------
var6 = _input('var6', NONE)  # Variant 7
tf6 = _input('tf6', PERIOD_CURRENT)  # Timeframe 7
param6 = _input('param6', 20)  # Parametr 7
symbol7 = _input('symbol7', GBPUSD)  # ----- Instrument 8 ------
var7 = _input('var7', NONE)  # Variant 8
tf7 = _input('tf7', PERIOD_CURRENT)  # Timeframe 8
param7 = _input('param7', 20)  # Parametr 8
symbol8 = _input('symbol8', CURRENT)  # ----- Instrument 9 ------
var8 = _input('var8', Time)  # Variant 9
tf8 = _input('tf8', PERIOD_CURRENT)  # Timeframe 9
param8 = _input('param8', 0)  # Parametr 9
symbol9 = _input('symbol9', CURRENT)  # ----- Instrument 10 ------
var9 = _input('var9', Time)  # Variant 10
tf9 = _input('tf9', PERIOD_CURRENT)  # Timeframe 10
param9 = _input('param9', 1)  # Parametr 10
max_bars = _input('max_bars', 100)  # Maximum Bars Calculate
in0Buffer = Arr(0, 0.0)
in1Buffer = Arr(0, 0.0)
in2Buffer = Arr(0, 0.0)
in3Buffer = Arr(0, 0.0)
in4Buffer = Arr(0, 0.0)
in5Buffer = Arr(0, 0.0)
in6Buffer = Arr(0, 0.0)
in7Buffer = Arr(0, 0.0)
in8Buffer = Arr(0, 0.0)
in9Buffer = Arr(0, 0.0)
handle = Arr(10, 0, dyn=False)
h = Arr(0, 0.0)
l = Arr(0, 0.0)
c = Arr(0, 0.0)
rsi = Arr(0, 0.0)
stoch = Arr(0, 0.0)
ma = Arr(0, 0.0)
knorm = Arr(10, 0.0, dyn=False)
temp = 0.0
point = 0.0
name = ""
begin = 0
value = 0.0

def OnInit():
    global name, point, temp
    SetIndexBuffer(0, in0Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, in1Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, in2Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, in3Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, in4Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, in5Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, in6Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, in7Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, in8Buffer, INDICATOR_DATA)
    SetIndexBuffer(9, in9Buffer, INDICATOR_DATA)
    SetBegin()
    PlotIndexSetString(0, PLOT_LABEL, EnumToString(symbol0, 'instrument') + ' in0-' + EnumToString(var0, 'variant') + ' ' + EnumToString(tf0, 'ENUM_TIMEFRAMES'))
    PlotIndexSetString(1, PLOT_LABEL, EnumToString(symbol1, 'instrument') + ' in1-' + EnumToString(var1, 'variant') + ' ' + EnumToString(tf1, 'ENUM_TIMEFRAMES'))
    PlotIndexSetString(2, PLOT_LABEL, EnumToString(symbol2, 'instrument') + ' in2-' + EnumToString(var2, 'variant') + ' ' + EnumToString(tf2, 'ENUM_TIMEFRAMES'))
    PlotIndexSetString(3, PLOT_LABEL, EnumToString(symbol3, 'instrument') + ' in3-' + EnumToString(var3, 'variant') + ' ' + EnumToString(tf3, 'ENUM_TIMEFRAMES'))
    PlotIndexSetString(4, PLOT_LABEL, EnumToString(symbol4, 'instrument') + ' in4-' + EnumToString(var4, 'variant') + ' ' + EnumToString(tf4, 'ENUM_TIMEFRAMES'))
    PlotIndexSetString(5, PLOT_LABEL, EnumToString(symbol5, 'instrument') + ' in5-' + EnumToString(var5, 'variant') + ' ' + EnumToString(tf5, 'ENUM_TIMEFRAMES'))
    PlotIndexSetString(6, PLOT_LABEL, EnumToString(symbol6, 'instrument') + ' in6-' + EnumToString(var6, 'variant') + ' ' + EnumToString(tf6, 'ENUM_TIMEFRAMES'))
    PlotIndexSetString(7, PLOT_LABEL, EnumToString(symbol7, 'instrument') + ' in7-' + EnumToString(var7, 'variant') + ' ' + EnumToString(tf7, 'ENUM_TIMEFRAMES'))
    PlotIndexSetString(8, PLOT_LABEL, EnumToString(symbol8, 'instrument') + ' in8-' + EnumToString(var8, 'variant') + ' ' + EnumToString(tf8, 'ENUM_TIMEFRAMES'))
    PlotIndexSetString(9, PLOT_LABEL, EnumToString(symbol9, 'instrument') + ' in9-' + EnumToString(var9, 'variant') + ' ' + EnumToString(tf9, 'ENUM_TIMEFRAMES'))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Inter')
    point = SymbolInfoDouble(Symbol(), SYMBOL_POINT)
    name = MQL5InfoString(MQL5_PROGRAM_NAME)
    ArraySetAsSeries(h, True)
    ArraySetAsSeries(l, True)
    ArraySetAsSeries(c, True)
    ArraySetAsSeries(rsi, True)
    ArraySetAsSeries(ma, True)
    ArrayInitialize(handle, INVALID_HANDLE)
    ArrayInitialize(knorm, 1e-07)
    time = TimeLocal()
    if not SymbolInfoInteger(EnumToString(symbol0, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol0, 'instrument'), True)
    if not SymbolInfoInteger(EnumToString(symbol1, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol1, 'instrument'), True)
    if not SymbolInfoInteger(EnumToString(symbol2, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol2, 'instrument'), True)
    if not SymbolInfoInteger(EnumToString(symbol3, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol3, 'instrument'), True)
    if not SymbolInfoInteger(EnumToString(symbol4, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol4, 'instrument'), True)
    if not SymbolInfoInteger(EnumToString(symbol5, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol5, 'instrument'), True)
    if not SymbolInfoInteger(EnumToString(symbol6, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol6, 'instrument'), True)
    if not SymbolInfoInteger(EnumToString(symbol7, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol7, 'instrument'), True)
    if not SymbolInfoInteger(EnumToString(symbol8, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol8, 'instrument'), True)
    if not SymbolInfoInteger(EnumToString(symbol9, 'instrument'), SYMBOL_SELECT):
        SymbolSelect(EnumToString(symbol9, 'instrument'), True)
    if var0 != NONE:
        temp = fmetod(0, EnumToString(symbol0, 'instrument'), tf0, var0, time, param0)
    if var1 != NONE:
        temp = fmetod(1, EnumToString(symbol1, 'instrument'), tf1, var1, time, param1)
    if var2 != NONE:
        temp = fmetod(2, EnumToString(symbol2, 'instrument'), tf2, var2, time, param2)
    if var3 != NONE:
        temp = fmetod(3, EnumToString(symbol3, 'instrument'), tf3, var3, time, param3)
    if var4 != NONE:
        temp = fmetod(4, EnumToString(symbol4, 'instrument'), tf4, var4, time, param4)
    if var5 != NONE:
        temp = fmetod(5, EnumToString(symbol5, 'instrument'), tf5, var5, time, param5)
    if var6 != NONE:
        temp = fmetod(6, EnumToString(symbol6, 'instrument'), tf6, var6, time, param6)
    if var7 != NONE:
        temp = fmetod(7, EnumToString(symbol7, 'instrument'), tf7, var7, time, param7)
    if var8 != NONE:
        temp = fmetod(8, EnumToString(symbol8, 'instrument'), tf8, var8, time, param8)
    if var9 != NONE:
        temp = fmetod(9, EnumToString(symbol9, 'instrument'), tf9, var9, time, param9)

def OnDeinit(reason):
    for i in range(0, 10):
        if handle[i] >= 0:
            IndicatorRelease(handle[i])

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    error = False
    symerror = ''
    ResetLastError()
    SetBegin()
    start = MathMax(begin, prev_calculated - 1)
    i = start
    for i in range(i, rates_total):
        if var0 != NONE:
            in0Buffer[i] = fmetod(0, EnumToString(symbol0, 'instrument'), tf0, var0, time[i], param0)
            if in0Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol0, 'instrument')
        else:
            in0Buffer[i] = EMPTY_VALUE
        if var1 != NONE:
            in1Buffer[i] = fmetod(1, EnumToString(symbol1, 'instrument'), tf1, var1, time[i], param1)
            if in1Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol1, 'instrument')
        else:
            in1Buffer[i] = EMPTY_VALUE
        if var2 != NONE:
            in2Buffer[i] = fmetod(2, EnumToString(symbol2, 'instrument'), tf2, var2, time[i], param2)
            if in2Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol2, 'instrument')
        else:
            in2Buffer[i] = EMPTY_VALUE
        if var3 != NONE:
            in3Buffer[i] = fmetod(3, EnumToString(symbol3, 'instrument'), tf3, var3, time[i], param3)
            if in3Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol3, 'instrument')
        else:
            in3Buffer[i] = EMPTY_VALUE
        if var4 != NONE:
            in4Buffer[i] = fmetod(4, EnumToString(symbol4, 'instrument'), tf4, var4, time[i], param4)
            if in4Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol4, 'instrument')
        else:
            in4Buffer[i] = EMPTY_VALUE
        if var5 != NONE:
            in5Buffer[i] = fmetod(5, EnumToString(symbol5, 'instrument'), tf5, var5, time[i], param5)
            if in5Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol5, 'instrument')
        else:
            in5Buffer[i] = EMPTY_VALUE
        if var6 != NONE:
            in6Buffer[i] = fmetod(6, EnumToString(symbol6, 'instrument'), tf6, var6, time[i], param6)
            if in6Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol6, 'instrument')
        else:
            in6Buffer[i] = EMPTY_VALUE
        if var7 != NONE:
            in7Buffer[i] = fmetod(7, EnumToString(symbol7, 'instrument'), tf7, var7, time[i], param7)
            if in7Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol7, 'instrument')
        else:
            in7Buffer[i] = EMPTY_VALUE
        if var8 != NONE:
            in8Buffer[i] = fmetod(8, EnumToString(symbol8, 'instrument'), tf8, var8, time[i], param8)
            if in8Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol8, 'instrument')
        else:
            in8Buffer[i] = EMPTY_VALUE
        if var9 != NONE:
            in9Buffer[i] = fmetod(9, EnumToString(symbol9, 'instrument'), tf9, var9, time[i], param9)
            if in9Buffer[i] == EMPTY_VALUE:
                error = True
                symerror = EnumToString(symbol9, 'instrument')
        else:
            in9Buffer[i] = EMPTY_VALUE
    else:
        i = _range_end(i, rates_total, 1)
    if error:
        return start
    return rates_total

def fmetod(n, symbol=None, tf=PERIOD_CURRENT, var=NONE, starttime=0, param=10):
    global value
    _sw1 = var
    if _sw1 == HLP:
        value = fHLP(n, symbol, tf, starttime, param)
    elif _sw1 == Op0_OpN:
        value = fOp0_OpN(n, symbol, tf, starttime, param)
    elif _sw1 == RSI:
        value = fRSI(n, symbol, tf, starttime, param)
    elif _sw1 == Stoch:
        value = fStoch(n, symbol, tf, starttime, param)
    elif _sw1 == Op0_Ma:
        value = fOp0_Ma(n, symbol, tf, starttime, param)
    elif _sw1 == Ma0_Ma1:
        value = fMa0_Ma1(n, symbol, tf, starttime, param)
    elif _sw1 == Time:
        value = fTimeDay(starttime, param)
    else:
        value = 0.0
    return value

def fHLP(n, symbol=None, tf=PERIOD_CURRENT, starttime=0, param=10):
    global value
    if symbol == 'CURRENT':
        symbol = Symbol()
    if CopyClose(symbol, tf, _DT(starttime), param, c) < param:
        return EMPTY_VALUE
    if CopyLow(symbol, tf, _DT(starttime), param, l) < param:
        return EMPTY_VALUE
    if CopyHigh(symbol, tf, _DT(starttime), param, h) < param:
        return EMPTY_VALUE
    deviation_minus = h[ArrayMaximum(h, 0, param)] - c[0]
    deviation_plus = c[0] - l[ArrayMinimum(l, 0, param)]
    value = _fdiv(2.0 * deviation_plus, deviation_plus + deviation_minus + 1e-06) - 1
    return value

def fOp0_OpN(n, symbol=None, tf=PERIOD_CURRENT, starttime=0, param=10):
    if symbol == 'CURRENT':
        symbol = Symbol()
    if CopyOpen(symbol, tf, _DT(starttime), param, c) < param:
        return EMPTY_VALUE
    val = c[0] - c[param - 1]
    knorm[n] = MathMax(MathAbs(val), knorm[n])
    return _fdiv(val, knorm[n])

def fRSI(n, symbol=None, tf=PERIOD_CURRENT, starttime=0, param=10):
    if symbol == 'CURRENT':
        symbol = Symbol()
    if handle[n] < 0:
        handle[n] = iRSI(symbol, tf, param, PRICE_CLOSE)
        if handle[n] == INVALID_HANDLE:
            Print('Creat Handle Error RSI ', GetLastError())
        return EMPTY_VALUE
    if CopyBuffer(handle[n], 0, _DT(starttime), 1, rsi) < 1:
        return EMPTY_VALUE
    return (rsi[0] - 50.0) / 50.0

def fStoch(n, symbol=None, tf=PERIOD_CURRENT, starttime=0, param=10):
    if symbol == 'CURRENT':
        symbol = Symbol()
    if handle[n] < 0:
        handle[n] = iStochastic(symbol, tf, param, 3, 3, MODE_SMMA, STO_LOWHIGH)
        if handle[n] == INVALID_HANDLE:
            Print('Creat Handle Error iStochastic ', GetLastError())
        return EMPTY_VALUE
    if CopyBuffer(handle[n], 0, _DT(starttime), 1, stoch) < 1:
        return EMPTY_VALUE
    return (stoch[0] - 50.0) / 50.0

def fOp0_Ma(n, symbol=None, tf=PERIOD_CURRENT, starttime=0, param=10):
    if symbol == 'CURRENT':
        symbol = Symbol()
    if handle[n] < 0:
        handle[n] = iMA(symbol, tf, param, 0, MODE_SMA, PRICE_CLOSE)
        if handle[n] == INVALID_HANDLE:
            Print('Creat Handle Error iMA ', GetLastError())
        return EMPTY_VALUE
    if CopyBuffer(handle[n], 0, _DT(starttime), 1, ma) < 1:
        return EMPTY_VALUE
    if CopyOpen(symbol, tf, _DT(starttime), 1, c) < 1:
        return EMPTY_VALUE
    val = c[0] - ma[0]
    knorm[n] = MathMax(MathAbs(val), knorm[n])
    return _fdiv(val, knorm[n])

def fMa0_Ma1(n, symbol=None, tf=PERIOD_CURRENT, starttime=0, param=10):
    if symbol == 'CURRENT':
        symbol = Symbol()
    if handle[n] < 0:
        handle[n] = iMA(symbol, tf, param, 0, MODE_SMA, PRICE_CLOSE)
        if handle[n] == INVALID_HANDLE:
            Print('Creat Handle Error iMA ', GetLastError())
        return EMPTY_VALUE
    if CopyBuffer(handle[n], 0, _DT(starttime), 2, ma) < 2:
        return EMPTY_VALUE
    val = ma[0] - ma[1]
    knorm[n] = MathMax(MathAbs(val), knorm[n])
    return _fdiv(val, knorm[n])

def fTimeDay(starttime, param):
    val = 0.0
    dt = MqlDateTime()
    TimeToStruct(starttime, dt)
    if param == 0:
        val = 1.0 - MathAbs(((dt.hour * 60) + dt.min - 720) / 720.0)
    if param > 0:
        if dt.hour < 12:
            val = -1.0
        else:
            val = 1.0
    return val

def SetBegin():
    global begin
    begin = MathMax(100, Bars(Symbol(), Period()) - max_bars)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(9, PLOT_DRAW_BEGIN, begin)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IInter(_MQL5Indicator):
    name = 'i_inter'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'symbol0': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=1),  # ----- Instrument 1 ------
        'var0': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=1),  # Variant 1
        'tf0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 1
        'param0': 5,  # Parametr 1
        'symbol1': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=2),  # ----- Instrument 2 ------
        'var1': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=1),  # Variant 2
        'tf1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 2
        'param1': 5,  # Parametr 2
        'symbol2': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=1),  # ----- Instrument 3 ------
        'var2': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=1),  # Variant 3
        'tf2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 3
        'param2': 20,  # Parametr 3
        'symbol3': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=2),  # ----- Instrument 4 ------
        'var3': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=1),  # Variant 4
        'tf3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 4
        'param3': 20,  # Parametr 4
        'symbol4': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=1),  # ----- Instrument 5 ------
        'var4': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=1),  # Variant 5
        'tf4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 5
        'param4': 50,  # Parametr 5
        'symbol5': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=2),  # ----- Instrument 6 ------
        'var5': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=1),  # Variant 6
        'tf5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 6
        'param5': 50,  # Parametr 6
        'symbol6': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=1),  # ----- Instrument 7 ------
        'var6': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=0),  # Variant 7
        'tf6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 7
        'param6': 20,  # Parametr 7
        'symbol7': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=2),  # ----- Instrument 8 ------
        'var7': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=0),  # Variant 8
        'tf7': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 8
        'param7': 20,  # Parametr 8
        'symbol8': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=0),  # ----- Instrument 9 ------
        'var8': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=7),  # Variant 9
        'tf8': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 9
        'param8': 0,  # Parametr 9
        'symbol9': _Choice({0: 'CURRENT', 1: 'EURUSD', 2: 'GBPUSD', 3: 'USDCHF', 4: 'USDJPY', 5: 'USDCAD', 6: 'AUDUSD', 7: 'NZDUSD', 8: 'EURGBP', 9: 'EURJPY', 10: 'EURCAD', 11: 'XAUUSD', 12: 'XAGUSD'}, default=0),  # ----- Instrument 10 ------
        'var9': _Choice({0: 'NONE', 1: 'HLP', 2: 'Op0_OpN', 3: 'RSI', 4: 'Stoch', 5: 'Op0_Ma', 6: 'Ma0_Ma1', 7: 'Time'}, default=7),  # Variant 10
        'tf9': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe 10
        'param9': 1,  # Parametr 10
        'max_bars': 100,  # Maximum Bars Calculate
    }

