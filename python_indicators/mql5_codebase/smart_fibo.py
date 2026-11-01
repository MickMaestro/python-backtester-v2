"""Smart Fibo — converted from MQL5: MQL5 Indicators/Smart Fibonacci/Smart Fibo.mq5

Copyright: Copyright 2025

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {}, 'colors': {1: [4678655], 2: [16711680], 3: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Smart Fibo', 'source': 'MQL5 Indicators/Smart Fibonacci/Smart Fibo.mq5', 'folder': 'Smart Fibonacci', 'inputs': [{'mql': 'AF_Period', 'py': 'AF_Period', 'param': 'AF_Period', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'AF_NumBars', 'py': 'AF_NumBars', 'param': 'AF_NumBars', 'type': 'int', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'AF_MinLevelDiplayed', 'py': 'AF_MinLevelDiplayed', 'param': 'AF_MinLevelDiplayed', 'type': 'double', 'default': -5.0, 'label': '', 'sinput': False}, {'mql': 'AF_LevelStyle', 'py': 'AF_LevelStyle', 'param': 'AF_LevelStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'AF_LabelsVisible', 'py': 'AF_LabelsVisible', 'param': 'AF_LabelsVisible', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'AF_LabelFont', 'py': 'AF_LabelFont', 'param': None, 'type': 'string', 'default': 'Arial', 'label': '', 'sinput': False}, {'mql': 'AF_LabelSize', 'py': 'AF_LabelSize', 'param': 'AF_LabelSize', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'AF_PriceCycleAlgo', 'py': 'AF_PriceCycleAlgo', 'param': None, 'type': 'string', 'default': 'ZigZag', 'label': '', 'sinput': False}, {'mql': 'AF_DrawBody2Body', 'py': 'AF_DrawBody2Body', 'param': 'AF_DrawBody2Body', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AF_NumFibos', 'py': 'AF_NumFibos', 'param': 'AF_NumFibos', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'AF_FiboColor', 'py': 'AF_FiboColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'AF_FiboColor2', 'py': 'AF_FiboColor2', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'AF_FiboColor3', 'py': 'AF_FiboColor3', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'AF_FiboColor4', 'py': 'AF_FiboColor4', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ZigZag_Visible', 'py': 'ZigZag_Visible', 'param': 'ZigZag_Visible', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Aqua = 0xFFFF00  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Orange = 0x00A5FF  # MQL4 colour name
Silver = 0xC0C0C0  # MQL4 colour name

# ---- inputs and global variables
AF_Period = _input('AF_Period', 0)
AF_NumBars = _input('AF_NumBars', 200)
AF_MinLevelDiplayed = _input('AF_MinLevelDiplayed', -5.0)
AF_LevelStyle = _input('AF_LevelStyle', 0)
AF_LabelsVisible = _input('AF_LabelsVisible', True)
AF_LabelFont = _input('AF_LabelFont', 'Arial')
AF_LabelSize = _input('AF_LabelSize', 7)
AF_PriceCycleAlgo = _input('AF_PriceCycleAlgo', 'ZigZag')
AF_DrawBody2Body = _input('AF_DrawBody2Body', False)
AF_NumFibos = _input('AF_NumFibos', 1)
ExtDepth = _input('ExtDepth', 5)
ExtDeviation = _input('ExtDeviation', 3)
ExtBackstep = _input('ExtBackstep', 1)
ZigZag_Visible = _input('ZigZag_Visible', False)
AF_Name = ""
AF_NumFibosInt = 0
NB_FIBO_LEVELS = 23.0
FiboRatios = Arr.of([0.0, 1.0, 0.114, 0.236, 0.382, 0.5, 0.618, 0.764, 0.886, 1.272, 1.382, 1.618, 2.0, 2.618, 4.236, 4.618, -0.272, -0.382, -0.618, -1.0, -1.618, -3.236, -3.618], fill=0.0, dyn=False, size=23)
FiboLabels = Arr.of(['0.0', '100.0', '88.6', '76.4', '61.8', '50.0', '61.8', '76.4', '88.6', '127.2', '138.2', '161.8', '200.0', '261.8', '423.6', '461.8', '127.2', '138.2', '161.8', '200.0', '261.8', '423.6', '461.8'], fill="", dyn=False, size=23)
af_fibo_colors = Arr(4, 0.0, dyn=False)
af_fibo_history = Arr(4, 0.0, dyn=False, dims=(4,))
vc_NUM_BARS = 5
level = 3  # recounting's depth
downloadhistory = False
ZigzagBuffer = Arr(0, 0.0)
HighMapBuffer = Arr(0, 0.0)
LowMapBuffer = Arr(0, 0.0)
High = Arr(0, 0.0)
Low = Arr(0, 0.0)
Close = Arr(0, 0.0)
Open = Arr(0, 0.0)
Time = Arr(0, 0)
IndicatorCounted = 0
error_alert_triggered = (0 != 0)

def OnInit():
    global AF_Name, AF_NumFibosInt
    i = 0
    j = 0
    AF_Name = MQLInfoString(MQL_PROGRAM_NAME)
    ArraySetAsSeries(ZigzagBuffer, True)
    ArraySetAsSeries(HighMapBuffer, True)
    ArraySetAsSeries(LowMapBuffer, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Time, True)
    SetIndexBuffer(0, ZigzagBuffer)
    SetIndexBuffer(1, HighMapBuffer)
    SetIndexBuffer(2, LowMapBuffer)
    if ZigZag_Visible == True:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_SECTION)
    else:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetString(0, PLOT_LABEL, 'AF_ZigZag')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    AF_NumFibosInt = AF_NumFibos
    if AF_NumFibos > 4:
        AF_NumFibosInt = 4
    i = 0
    for i in range(i, 4):
        j = 0
        for j in range(j, 4):
            af_fibo_history[i][j] = 0.0
        else:
            j = _range_end(j, 4, 1)
    else:
        i = _range_end(i, 4, 1)
    af_fibo_colors[0] = AF_FiboColor
    af_fibo_colors[1] = AF_FiboColor2
    af_fibo_colors[2] = AF_FiboColor3
    af_fibo_colors[3] = AF_FiboColor4
    IndicatorSetString(INDICATOR_SHORTNAME, AF_Name + '(' + IntegerToString(AF_Period) + ',' + IntegerToString(ExtDepth) + ',' + IntegerToString(ExtDeviation) + ',' + IntegerToString(ExtBackstep) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global IndicatorCounted, error_alert_triggered
    if prev_calculated > 0 and rates_total == prev_calculated:
        return rates_total
    ArrayInitialize(ZigzagBuffer, 0.0)
    ArrayInitialize(HighMapBuffer, 0.0)
    ArrayInitialize(LowMapBuffer, 0.0)
    ArrayInitialize(High, 0.0)
    ArrayInitialize(Low, 0.0)
    ArrayInitialize(Close, 0.0)
    ArrayInitialize(Open, 0.0)
    ArrayInitialize(Time, 0.0)
    IndicatorCounted = 0
    if prev_calculated > 0:
        IndicatorCounted = prev_calculated - 1
    IndicatorCounted = rates_total
    to_copy = rates_total
    CopyHigh(Symbol(), Period(), 0, to_copy, High)
    CopyLow(Symbol(), Period(), 0, to_copy, Low)
    CopyClose(Symbol(), Period(), 0, to_copy, Close)
    CopyOpen(Symbol(), Period(), 0, to_copy, Open)
    CopyTime(Symbol(), Period(), 0, to_copy, Time)
    if AF_Period == 0 or AF_Period == Period():
        zigzag()
        auto_fibo()
    elif AF_Period < Period() and AF_Period != 0:
        if error_alert_triggered == False:
            Alert('AutoFibo: AF_Period must be larger than the period of the current chart!')
            error_alert_triggered = True
        return 0
    else:
        error_alert_triggered = False
        iCustom(None, TFMigrate(AF_Period), AF_Name, AF_Name, AF_Period, AF_NumBars, AF_FiboColor, AF_PriceCycleAlgo, ExtDepth, ExtDeviation, ExtBackstep, ZigZag_Visible, 0, 0)
    return rates_total

def OnDeinit(reason):
    af_delete()
    Comment('')

def zigzag():
    global downloadhistory
    i = 0
    counted_bars = IndicatorCounted
    limit = 0
    counterZ = 0
    whatlookfor = 0
    shift = 0
    back = 0
    lasthighpos = 0
    lastlowpos = 0
    val = 0.0
    res = 0.0
    curlow = 0.0
    curhigh = 0.0
    lasthigh = 0.0
    lastlow = 0.0
    if counted_bars == 0 and downloadhistory:
        ArrayInitialize(ZigzagBuffer, 0.0)
        ArrayInitialize(HighMapBuffer, 0.0)
        ArrayInitialize(LowMapBuffer, 0.0)
    if counted_bars == 0:
        limit = Bars(Symbol(), Period()) - ExtDepth
        downloadhistory = True
    limit = Bars(Symbol(), Period()) - ExtDepth
    counted_bars = 0
    if counted_bars > 0:
        while counterZ < level and i < 100:
            res = ZigzagBuffer[i]
            if res != 0:
                counterZ += 1
            i += 1
        i -= 1
        limit = i
        if LowMapBuffer[i] != 0:
            curlow = LowMapBuffer[i]
            whatlookfor = 1
        else:
            curhigh = HighMapBuffer[i]
            whatlookfor = -1
        i = limit - 1
        for i in range(i, 0 - 1, -1):
            ZigzagBuffer[i] = 0.0
            LowMapBuffer[i] = 0.0
            HighMapBuffer[i] = 0.0
        else:
            i = _range_end(i, 0 - 1, -1)
    shift = limit
    for shift in range(shift, 0 - 1, -1):
        val = Low[ArrayMinimum(Low, shift, ExtDepth)]
        if val == lastlow:
            val = 0.0
        else:
            lastlow = val
            if (Low[shift] - val) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = LowMapBuffer[shift + back]
                    if res != 0 and res > val:
                        LowMapBuffer[shift + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        if Low[shift] == val:
            LowMapBuffer[shift] = val
        else:
            LowMapBuffer[shift] = 0.0
        val = High[ArrayMaximum(High, shift, ExtDepth)]
        if val == lasthigh:
            val = 0.0
        else:
            lasthigh = val
            if (val - High[shift]) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = HighMapBuffer[shift + back]
                    if res != 0 and res < val:
                        HighMapBuffer[shift + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        if High[shift] == val:
            HighMapBuffer[shift] = val
        else:
            HighMapBuffer[shift] = 0.0
    else:
        shift = _range_end(shift, 0 - 1, -1)
    if whatlookfor == 0:
        lastlow = 0.0
        lasthigh = 0.0
    else:
        lastlow = curlow
        lasthigh = curhigh
    shift = limit
    for shift in range(shift, 0 - 1, -1):
        res = 0.0
        _sw1 = whatlookfor
        if _sw1 == 0:
            if lastlow == 0 and lasthigh == 0:
                if HighMapBuffer[shift] != 0:
                    lasthigh = High[shift]
                    lasthighpos = shift
                    whatlookfor = -1
                    ZigzagBuffer[shift] = lasthigh
                    res = 1.0
                if LowMapBuffer[shift] != 0:
                    lastlow = Low[shift]
                    lastlowpos = shift
                    whatlookfor = 1
                    ZigzagBuffer[shift] = lastlow
                    res = 1.0
        elif _sw1 == 1:
            if ((LowMapBuffer[shift] != 0.0 and LowMapBuffer[shift] < lastlow) and HighMapBuffer[shift] == 0.0) and lastlowpos > -1:
                ZigzagBuffer[lastlowpos] = 0.0
                lastlowpos = shift
                lastlow = LowMapBuffer[shift]
                ZigzagBuffer[shift] = lastlow
                res = 1.0
            if HighMapBuffer[shift] != 0.0 and LowMapBuffer[shift] == 0.0:
                lasthigh = HighMapBuffer[shift]
                lasthighpos = shift
                ZigzagBuffer[shift] = lasthigh
                whatlookfor = -1
                res = 1.0
        elif _sw1 == -1:
            if ((HighMapBuffer[shift] != 0.0 and HighMapBuffer[shift] > lasthigh) and LowMapBuffer[shift] == 0.0) and lasthighpos > -1:
                ZigzagBuffer[lasthighpos] = 0.0
                lasthighpos = shift
                lasthigh = HighMapBuffer[shift]
                ZigzagBuffer[shift] = lasthigh
            if LowMapBuffer[shift] != 0.0 and HighMapBuffer[shift] == 0.0:
                lastlow = LowMapBuffer[shift]
                lastlowpos = shift
                ZigzagBuffer[shift] = lastlow
                whatlookfor = 1
        else:
            return 0
    else:
        shift = _range_end(shift, 0 - 1, -1)
    return 0

def auto_fibo():
    i = 0
    j = 0
    y = 0
    zz = Arr(4, 0.0, dyn=False)
    ArrayInitialize(zz, 0)
    zzpos = Arr(4, 0, dyn=False)
    ArrayInitialize(zzpos, 0)
    new_fibo = False
    time1 = 0
    time2 = 0
    low = 0.0
    high = 0.0
    price1 = 0.0
    price2 = 0.0
    af_delete()
    i = 0
    y = 0
    while i < AF_NumBars and y < 4:
        if ZigzagBuffer[i] != 0.0:
            zz[y] = ZigzagBuffer[i]
            zzpos[y] = i
            y += 1
        i += 1
    if ((zz[3] < zz[2] and zz[1] < zz[2]) and zz[3] <= zz[1]) and zz[1] < zz[0]:
        if AF_DrawBody2Body:
            low = Close[zzpos[3]]
            high = Close[zzpos[2]]
            if Open[zzpos[3]] < Close[zzpos[3]]:
                low = Open[zzpos[3]]
            if Open[zzpos[2]] > Close[zzpos[2]]:
                high = Open[zzpos[2]]
            time1 = Time[zzpos[3]]
            price1 = low
            time2 = Time[zzpos[2]]
            price2 = high
            new_fibo = True
        else:
            time1 = Time[zzpos[3]]
            price1 = zz[3]
            time2 = Time[zzpos[2]]
            price2 = zz[2]
            new_fibo = True
    elif ((zz[3] > zz[2] and zz[1] > zz[2]) and zz[3] >= zz[1]) and zz[1] > zz[0]:
        if AF_DrawBody2Body:
            low = Close[zzpos[2]]
            high = Close[zzpos[3]]
            if Open[zzpos[2]] < Close[zzpos[2]]:
                low = Open[zzpos[2]]
            if Open[zzpos[3]] > Close[zzpos[3]]:
                high = Open[zzpos[3]]
            time1 = Time[zzpos[3]]
            price1 = high
            time2 = Time[zzpos[2]]
            price2 = low
            new_fibo = True
        else:
            time1 = Time[zzpos[3]]
            price1 = zz[3]
            time2 = Time[zzpos[2]]
            price2 = zz[2]
            new_fibo = True
    elif (zz[3] < zz[2] and zz[1] < zz[3]) and zz[0] > zz[1]:
        if AF_DrawBody2Body:
            low = Close[zzpos[1]]
            high = Close[zzpos[2]]
            if Open[zzpos[1]] < Close[zzpos[1]]:
                low = Open[zzpos[1]]
            if Open[zzpos[2]] > Close[zzpos[2]]:
                high = Open[zzpos[2]]
            time1 = Time[zzpos[1]]
            price1 = low
            time2 = Time[zzpos[2]]
            price2 = high
            new_fibo = True
        else:
            time1 = Time[zzpos[1]]
            price1 = zz[1]
            time2 = Time[zzpos[2]]
            price2 = zz[2]
            new_fibo = True
    elif (zz[3] > zz[2] and zz[1] > zz[3]) and zz[0] < zz[1]:
        if AF_DrawBody2Body:
            low = Close[zzpos[2]]
            high = Close[zzpos[1]]
            if Open[zzpos[2]] < Close[zzpos[2]]:
                low = Open[zzpos[2]]
            if Open[zzpos[1]] > Close[zzpos[1]]:
                high = Open[zzpos[1]]
            time1 = Time[zzpos[1]]
            price1 = high
            time2 = Time[zzpos[2]]
            price2 = low
            new_fibo = True
        else:
            time1 = Time[zzpos[1]]
            price1 = zz[1]
            time2 = Time[zzpos[2]]
            price2 = zz[2]
            new_fibo = True
    if new_fibo:
        if time1 != af_fibo_history[0][0] and time2 != af_fibo_history[0][0]:
            i = AF_NumFibosInt - 1
            for i in range(i, 0, -1):
                j = 0
                for j in range(j, 4):
                    af_fibo_history[i][j] = af_fibo_history[i - 1][j]
                else:
                    j = _range_end(j, 4, 1)
            else:
                i = _range_end(i, 0, -1)
            af_fibo_history[0][0] = float(time1)
            af_fibo_history[0][1] = price1
            af_fibo_history[0][2] = float(time2)
            af_fibo_history[0][3] = price2
    i = 0
    while i < AF_NumFibosInt and af_fibo_history[i][0] > 0.0:
        draw_fibo(_long(af_fibo_history[i][0]), af_fibo_history[i][1], _long(af_fibo_history[i][2]), af_fibo_history[i][3], _uint(af_fibo_colors[i]), i)
        i += 1

def draw_fibo(time1, price1, time2, price2, fibo_color, id_):
    i = 0
    start = time1
    end = Time[0]
    range_ = price2 - price1
    draw_base(time1, price1, time2, price2, fibo_color, id_)
    i = 0
    while i < NB_FIBO_LEVELS:
        if FiboRatios[i] >= AF_MinLevelDiplayed:
            draw_line(start, price1 + (FiboRatios[i] * range_), FiboLabels[i], fibo_color, 0, id_)
        i += 1

def draw_line(start, level2, label, col, style, id_):
    line_name = 'CHT_AF_FiboLine' + IntegerToString(id_) + '(' + label + ',' + DoubleToString(level2, Digits()) + ',' + IntegerToString(AF_Period) + ',' + IntegerToString(ExtDepth) + ',' + IntegerToString(ExtDeviation) + ',' + IntegerToString(ExtBackstep) + ')'
    label_name = 'CHT_AF_FiboLabel' + IntegerToString(id_) + '(' + label + ',' + DoubleToString(level2, Digits()) + ',' + IntegerToString(AF_Period) + ',' + IntegerToString(ExtDepth) + ',' + IntegerToString(ExtDeviation) + ',' + IntegerToString(ExtBackstep) + ')'
    ObjectCreate(0, line_name, OBJ_TREND, 0, start, level2, Time[0] + (800 * Period()), level2)
    ObjectSetInteger(0, line_name, OBJPROP_STYLE, AF_LevelStyle)
    ObjectSetInteger(0, line_name, OBJPROP_COLOR, col)
    ObjectSetInteger(0, line_name, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, line_name, OBJPROP_RAY_RIGHT, False)
    if AF_LabelsVisible == True:
        ObjectCreate(0, label_name, OBJ_TEXT, 0, Time[0] + (500 * Period()), level2)
        ObjectSetString(0, label_name, OBJPROP_TEXT, label + ' - ' + DoubleToString(level2, Digits()))
        ObjectSetInteger(0, label_name, OBJPROP_FONTSIZE, AF_LabelSize)
        ObjectSetString(0, label_name, OBJPROP_FONT, AF_LabelFont)
        ObjectSetInteger(0, label_name, OBJPROP_COLOR, col)
    if style != 0:
        if style == 3:
            ObjectSetInteger(0, line_name, OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(0, line_name, OBJPROP_WIDTH, 3)
        elif style == 2:
            ObjectSetInteger(0, line_name, OBJPROP_STYLE, STYLE_DOT)
            ObjectSetInteger(0, line_name, OBJPROP_WIDTH, 2)
        elif style == 1:
            ObjectSetInteger(0, line_name, OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(0, line_name, OBJPROP_WIDTH, 2)

def draw_base(time1, price1, time2, price2, col, id_):
    base_name = 'CHT_AF_FiboBase' + IntegerToString(id_) + '(' + ',' + IntegerToString(AF_Period) + ',' + IntegerToString(ExtDepth) + ',' + IntegerToString(ExtDeviation) + ',' + IntegerToString(ExtBackstep) + ')'
    ObjectCreate(0, base_name, OBJ_TREND, 0, time1, price1, time2, price2)
    ObjectSetInteger(0, base_name, OBJPROP_COLOR, col)
    ObjectSetInteger(0, base_name, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, base_name, OBJPROP_RAY_RIGHT, False)

def af_delete():
    ObjectsDeleteAll(0, 'CHT_AF')

def TFMigrate(tf):
    _sw2 = tf
    if _sw2 == 0:
        return PERIOD_CURRENT
    elif _sw2 == 1:
        return PERIOD_M1
    elif _sw2 == 5:
        return PERIOD_M5
    elif _sw2 == 15:
        return PERIOD_M15
    elif _sw2 == 30:
        return PERIOD_M30
    elif _sw2 == 60:
        return PERIOD_H1
    elif _sw2 == 240:
        return PERIOD_H4
    elif _sw2 == 1440:
        return PERIOD_D1
    elif _sw2 == 10080:
        return PERIOD_W1
    elif _sw2 == 43200:
        return PERIOD_MN1
    elif _sw2 == 2:
        return PERIOD_M2
    elif _sw2 == 3:
        return PERIOD_M3
    elif _sw2 == 4:
        return PERIOD_M4
    elif _sw2 == 6:
        return PERIOD_M6
    elif _sw2 == 10:
        return PERIOD_M10
    elif _sw2 == 12:
        return PERIOD_M12
    elif _sw2 == 16385:
        return PERIOD_H1
    elif _sw2 == 16386:
        return PERIOD_H2
    elif _sw2 == 16387:
        return PERIOD_H3
    elif _sw2 == 16388:
        return PERIOD_H4
    elif _sw2 == 16390:
        return PERIOD_H6
    elif _sw2 == 16392:
        return PERIOD_H8
    elif _sw2 == 16396:
        return PERIOD_H12
    elif _sw2 == 16408:
        return PERIOD_D1
    elif _sw2 == 32769:
        return PERIOD_W1
    elif _sw2 == 49153:
        return PERIOD_MN1
    else:
        return PERIOD_CURRENT

# ---- global variables initialised from expressions
AF_FiboColor = _input('AF_FiboColor', _uint(Silver))
AF_FiboColor2 = _input('AF_FiboColor2', _uint(Orange))
AF_FiboColor3 = _input('AF_FiboColor3', _uint(Magenta))
AF_FiboColor4 = _input('AF_FiboColor4', _uint(Aqua))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmartFibo(_MQL5Indicator):
    name = 'Smart Fibo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'AF_Period': 0,
        'AF_NumBars': 200,
        'AF_MinLevelDiplayed': -5.0,
        'AF_LevelStyle': 0,
        'AF_LabelsVisible': True,
        'AF_LabelSize': 7,
        'AF_DrawBody2Body': False,
        'AF_NumFibos': 1,
        'ExtDepth': 5,
        'ExtDeviation': 3,
        'ExtBackstep': 1,
        'ZigZag_Visible': False,
    }

