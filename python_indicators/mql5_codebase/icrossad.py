"""iCrossAD — converted from MQL5: MQL5 Indicators/iCrossAD/iCrossAD.mq5

Copyright: Copyright 2016, Artem A. Trishkin, Skype artmedia70; Link: https://login.mql5.com/ru/users/artmedia70; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Artem A. Trishkin, Skype artmedia70', 'link': 'https://login.mql5.com/ru/users/artmedia70', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [255], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'AD', 2: 'Arrow to Up', 3: 'Arrow to Down'}, 'levels': [], 'description': [''], 'name': 'iCrossAD', 'source': 'MQL5 Indicators/iCrossAD/iCrossAD.mq5', 'folder': 'iCrossAD', 'inputs': [{'mql': 'InpAppliedVolime', 'py': 'InpAppliedVolime', 'param': 'InpAppliedVolime', 'type': 'int', 'default': 0, 'label': 'AD applied volume', 'sinput': False}, {'mql': 'InpPeriodFind', 'py': 'InpPeriodFind', 'param': 'InpPeriodFind', 'type': 'uint', 'default': 60, 'label': 'Bars for calculate', 'sinput': False}, {'mql': 'InpUnheckedBars', 'py': 'InpUnheckedBars', 'param': 'InpUnheckedBars', 'type': 'uint', 'default': 3, 'label': 'Unchecked bars', 'sinput': False}, {'mql': 'InpFilterBy', 'py': 'InpFilterBy', 'param': 'InpFilterBy', 'type': 'int', 'default': 1, 'label': 'Filtering indicator', 'sinput': False}, {'mql': 'InpUseDefaultSetting', 'py': 'InpUseDefaultSetting', 'param': 'InpUseDefaultSetting', 'type': 'int', 'default': 1, 'label': 'Use settings by default CCI parameters', 'sinput': False}, {'mql': 'InpPeriodIND', 'py': 'InpPeriodIND', 'param': 'InpPeriodIND', 'type': 'uint', 'default': 14, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpAppliedPriceCCI', 'py': 'InpAppliedPriceCCI', 'param': 'InpAppliedPriceCCI', 'type': 'int', 'default': 6, 'label': 'CCI applied price', 'sinput': False}, {'mql': 'InpUpperLevelIND', 'py': 'InpUpperLevelIND', 'param': 'InpUpperLevelIND', 'type': 'double', 'default': 100.0, 'label': 'The upper level of the filter indicator', 'sinput': False}, {'mql': 'InpLowerLevelIND', 'py': 'InpLowerLevelIND', 'param': 'InpLowerLevelIND', 'type': 'double', 'default': -100.0, 'label': 'The lower level of the filter indicator', 'sinput': False}, {'mql': 'InpDrawChartsArrow', 'py': 'InpDrawChartsArrow', 'param': 'InpDrawChartsArrow', 'type': 'int', 'default': 1, 'label': 'Draw arrows on chart', 'sinput': True}, {'mql': 'InpArrowSize', 'py': 'InpArrowSize', 'param': 'InpArrowSize', 'type': 'int', 'default': 2, 'label': 'The size of the arrows on the chart', 'sinput': True}, {'mql': 'InpColorBullishArrow', 'py': 'InpColorBullishArrow', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Bullish arrows color', 'sinput': True}, {'mql': 'InpColorBearishArrow', 'py': 'InpColorBearishArrow', 'param': None, 'type': 'color', 'default': 255, 'label': 'Bearish arrows color', 'sinput': True}, {'mql': 'InpDrawTrendLine', 'py': 'InpDrawTrendLine', 'param': 'InpDrawTrendLine', 'type': 'int', 'default': 0, 'label': 'Draw a trend line', 'sinput': True}, {'mql': 'InpWidthTrendLine', 'py': 'InpWidthTrendLine', 'param': 'InpWidthTrendLine', 'type': 'int', 'default': 1, 'label': 'Trend line thickness', 'sinput': True}, {'mql': 'InpStyleTrendLine', 'py': 'InpStyleTrendLine', 'param': 'InpStyleTrendLine', 'type': 'int', 'default': 2, 'label': 'Trend line style', 'sinput': True}, {'mql': 'InpColorTrendDN', 'py': 'InpColorTrendDN', 'param': None, 'type': 'color', 'default': 255, 'label': 'Downtrend line color', 'sinput': True}, {'mql': 'InpColorTrendUP', 'py': 'InpColorTrendUP', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Uptrend line color', 'sinput': True}, {'mql': 'InpDrawArea', 'py': 'InpDrawArea', 'param': 'InpDrawArea', 'type': 'int', 'default': 0, 'label': 'Draw the search area', 'sinput': True}, {'mql': 'InpStyleFrame', 'py': 'InpStyleFrame', 'param': 'InpStyleFrame', 'type': 'int', 'default': 0, 'label': 'Search area style', 'sinput': True}, {'mql': 'InpWidthLineArea', 'py': 'InpWidthLineArea', 'param': 'InpWidthLineArea', 'type': 'int', 'default': 1, 'label': 'Search area line width (if Frame mode)', 'sinput': True}, {'mql': 'InpStyleLineFrame', 'py': 'InpStyleLineFrame', 'param': 'InpStyleLineFrame', 'type': 'int', 'default': 0, 'label': 'Search area line style (if Frame mode)', 'sinput': True}, {'mql': 'InpColorArea', 'py': 'InpColorArea', 'param': None, 'type': 'color', 'default': 14599344, 'label': 'Search area color', 'sinput': True}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_STYLE
STYLE_FILL = 1
STYLE_FRAME = 0
_enum('ENUM_STYLE', {1: 'STYLE_FILL', 0: 'STYLE_FRAME'})

# enum ENUM_WIDTH
WIDTH1 = 1
WIDTH2 = 2
WIDTH3 = 3
WIDTH4 = 4
_enum('ENUM_WIDTH', {1: 'WIDTH1', 2: 'WIDTH2', 3: 'WIDTH3', 4: 'WIDTH4'})

# enum ENUM_FILTER
FILTER_NO = 0
FILTER_CCI = 1
_enum('ENUM_FILTER', {0: 'FILTER_NO', 1: 'FILTER_CCI'})

# enum ENUM_LINE_STOCH
LINE_STOCH_MAIN = 0
LINE_STOCH_SIG = 1
_enum('ENUM_LINE_STOCH', {0: 'LINE_STOCH_MAIN', 1: 'LINE_STOCH_SIG'})

# ---- inputs and global variables
InpAppliedVolime = _input('InpAppliedVolime', VOLUME_TICK)  # AD applied volume
InpPeriodFind = _input('InpPeriodFind', 60)  # Bars for calculate
InpUnheckedBars = _input('InpUnheckedBars', 3)  # Unchecked bars
InpFilterBy = _input('InpFilterBy', FILTER_CCI)  # Filtering indicator
InpUseDefaultSetting = _input('InpUseDefaultSetting', INPUT_YES)  # Use settings by default CCI parameters
InpPeriodIND = _input('InpPeriodIND', 14)  # CCI period
InpAppliedPriceCCI = _input('InpAppliedPriceCCI', PRICE_TYPICAL)  # CCI applied price
InpUpperLevelIND = _input('InpUpperLevelIND', 100.0)  # The upper level of the filter indicator
InpLowerLevelIND = _input('InpLowerLevelIND', -100.0)  # The lower level of the filter indicator
InpDrawChartsArrow = _input('InpDrawChartsArrow', INPUT_YES)  # Draw arrows on chart
InpArrowSize = _input('InpArrowSize', WIDTH2)  # The size of the arrows on the chart
InpColorBullishArrow = _input('InpColorBullishArrow', clrBlue)  # Bullish arrows color
InpColorBearishArrow = _input('InpColorBearishArrow', clrRed)  # Bearish arrows color
InpDrawTrendLine = _input('InpDrawTrendLine', INPUT_NO)  # Draw a trend line
InpWidthTrendLine = _input('InpWidthTrendLine', WIDTH1)  # Trend line thickness
InpStyleTrendLine = _input('InpStyleTrendLine', STYLE_DOT)  # Trend line style
InpColorTrendDN = _input('InpColorTrendDN', clrRed)  # Downtrend line color
InpColorTrendUP = _input('InpColorTrendUP', clrBlue)  # Uptrend line color
InpDrawArea = _input('InpDrawArea', INPUT_NO)  # Draw the search area
InpStyleFrame = _input('InpStyleFrame', STYLE_FRAME)  # Search area style
InpWidthLineArea = _input('InpWidthLineArea', WIDTH1)  # Search area line width (if Frame mode)
InpStyleLineFrame = _input('InpStyleLineFrame', STYLE_SOLID)  # Search area line style (if Frame mode)
InpColorArea = _input('InpColorArea', clrLightSteelBlue)  # Search area color
BufferAD = Arr(0, 0.0)
BufferUpperArrow = Arr(0, 0.0)
BufferLowerArrow = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
BufferPeakUP = Arr(0, 0.0, dims=(2,))  # array of peak up [i][0] - time, [i][1] - value
BufferPeakDN = Arr(0, 0.0, dims=(2,))  # array of peak down [i][0] - time, [i][1] - value
AppliedPriceCCI = 0
upper_level = 0.0
lower_level = 0.0
period_find = 0  # Number bars for calculate
unhecked_bars = 0  # Unchecked bars
period_cci = 0
checkFilter = False
prefix = ""
wnd = 0
handle_ad = 0
handle_cci = 0

def OnInit():
    global AppliedPriceCCI, checkFilter, handle_ad, handle_cci, lower_level, period_cci, period_find, prefix, unhecked_bars, upper_level, wnd
    AppliedPriceCCI = InpAppliedPriceCCI
    period_find = (6 if (InpPeriodFind < 6) else InpPeriodFind)
    unhecked_bars = (2 if (InpUnheckedBars < 2) else InpUnheckedBars)
    period_cci = (1 if (InpPeriodIND < 1) else InpPeriodIND)
    upper_level = InpUpperLevelIND
    lower_level = InpLowerLevelIND
    prefix = 'SCAD(' + _str(period_find) + ')'
    wnd = ChartWindowFind()
    checkFilter = True
    if InpUseDefaultSetting:
        CorrectInputValue(InpFilterBy)
    SetIndexBuffer(0, BufferAD)
    SetIndexBuffer(1, BufferUpperArrow)
    SetIndexBuffer(2, BufferLowerArrow)
    SetIndexBuffer(3, BufferCCI)
    PlotIndexSetInteger(1, PLOT_ARROW, 241)
    PlotIndexSetInteger(2, PLOT_ARROW, 242)
    IndicatorSetString(INDICATOR_SHORTNAME, prefix)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferAD, True)
    ArraySetAsSeries(BufferUpperArrow, True)
    ArraySetAsSeries(BufferLowerArrow, True)
    ArraySetAsSeries(BufferCCI, True)
    ResetLastError()
    handle_ad = iAD(None, PERIOD_CURRENT, InpAppliedVolime)
    if handle_ad == INVALID_HANDLE:
        Print('The iAD() by ', EnumToString(InpAppliedVolime, 'ENUM_APPLIED_VOLUME'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    if InpFilterBy == FILTER_CCI:
        handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, AppliedPriceCCI)
        if handle_cci == INVALID_HANDLE:
            Print('The iCCI(' + _str(period_cci) + ') by ', EnumToString(AppliedPriceCCI, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
            return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global checkFilter
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(time, True)
    if rates_total < (period_find + unhecked_bars + 1):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_find - unhecked_bars - 1
        ArrayInitialize(BufferAD, EMPTY_VALUE)
        ArrayInitialize(BufferUpperArrow, EMPTY_VALUE)
        ArrayInitialize(BufferLowerArrow, EMPTY_VALUE)
        ArrayInitialize(BufferCCI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ad, 0, 0, count, BufferAD)
    if copied != count:
        return 0
    if InpFilterBy == FILTER_CCI:
        copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
        if copied != count:
            return 0
    nm = ''
    p1 = 0.0
    p2 = 0.0
    value_left_dn = DBL_MAX
    value_left_up = -DBL_MAX
    value_right_dn = DBL_MAX
    value_right_up = -DBL_MAX
    time_right_dn = 0
    time_right_up = 0
    bar_max = 0
    bar_min = 0
    ArrayResize(BufferPeakUP, 0)
    ArrayResize(BufferPeakDN, 0)
    for i in range(limit, 0 - 1, -1):
        BufferUpperArrow[i] = EMPTY_VALUE
        BufferLowerArrow[i] = EMPTY_VALUE
        jup = 0
        jdn = 0
        j = i
        while j <= (i + period_find + unhecked_bars - 1):
            if j > (i + unhecked_bars):
                if DirectionExtremum(BufferAD[j + 1], BufferAD[j], BufferAD[j - 1]) == 1:
                    jup += 1
                    ArrayResize(BufferPeakUP, jup, period_find)
                    BufferPeakUP[jup - 1][0] = _int(time[j])
                    BufferPeakUP[jup - 1][1] = BufferAD[j]
                if DirectionExtremum(BufferAD[j + 1], BufferAD[j], BufferAD[j - 1]) == 0:
                    jdn += 1
                    ArrayResize(BufferPeakDN, jdn, period_find)
                    BufferPeakDN[jdn - 1][0] = _int(time[j])
                    BufferPeakDN[jdn - 1][1] = BufferAD[j]
            j += 1
        size_mass_up = ArrayRange(BufferPeakUP, 0)
        if size_mass_up > 0:
            time_right_up = _int(BufferPeakUP[0][0])
            bar_right_up = BarShift("", PERIOD_CURRENT, time_right_up)
            value_right_up = BufferPeakUP[0][1]
            index_max = ArrayMaximumInXDimm(BufferPeakUP, 1)
            time_max = _int(BufferPeakUP[index_max][0])
            bar_max = BarShift("", PERIOD_CURRENT, time_max)
            value_left_up = BufferPeakUP[index_max][1]
            if time_right_up > time_max and BufferAD[bar_max] > value_right_up:
                for k in range(index_max - 0, 0, -1):
                    bar_k = BarShift("", PERIOD_CURRENT, _long(BufferPeakUP[k][0]))
                    virtual_price = EquationDirect(bar_max, value_left_up, bar_right_up, value_right_up, bar_k)
                    if BufferAD[bar_k] > virtual_price:
                        bar_max = BarShift("", PERIOD_CURRENT, _int(BufferPeakUP[k][0]))
                        value_left_up = BufferPeakUP[k][1]
                if EquationDirect(bar_max, value_left_up, bar_right_up, value_right_up, i + 1) < BufferAD[i + 1] and (EquationDirect(bar_max, value_left_up, bar_right_up, value_right_up, i + 2) >= BufferAD[i + 2] or EquationDirect(bar_max, value_left_up, bar_right_up, value_right_up, i + 3) >= BufferAD[i + 3]):
                    if InpFilterBy != FILTER_NO:
                        filter_1 = GetDataIND(InpFilterBy, i + 1)
                        filter_2 = GetDataIND(InpFilterBy, i + 2)
                        filter_3 = GetDataIND(InpFilterBy, i + 3)
                        checkFilter = (True if (filter_1 <= lower_level and filter_2 < lower_level) else False)
                    else:
                        checkFilter = True
                    if checkFilter:
                        BufferUpperArrow[i] = BufferAD[i + 1]
                        if InpDrawChartsArrow:
                            SetArrow(prefix + 'ChartArrowUP_' + TimeToString(time[i]), InpColorBullishArrow, time[i], open[i], _char(241), ANCHOR_TOP, InpArrowSize)
        size_mass_dn = ArrayRange(BufferPeakDN, 0)
        if size_mass_dn > 0:
            time_right_dn = _int(BufferPeakDN[0][0])
            bar_right_dn = BarShift("", PERIOD_CURRENT, time_right_dn)
            value_right_dn = BufferPeakDN[0][1]
            index_min = ArrayMinimumInXDimm(BufferPeakDN, 1)
            time_min = _int(BufferPeakDN[index_min][0])
            bar_min = BarShift("", PERIOD_CURRENT, time_min)
            value_left_dn = BufferPeakDN[index_min][1]
            if time_right_dn > time_min and BufferAD[bar_min] < value_right_dn:
                for k in range(index_min - 0, 0, -1):
                    bar_k = BarShift("", PERIOD_CURRENT, _long(BufferPeakDN[k][0]))
                    virtual_price = EquationDirect(bar_min, value_left_dn, bar_right_dn, value_right_dn, bar_k)
                    if BufferAD[bar_k] < virtual_price:
                        bar_min = BarShift("", PERIOD_CURRENT, _int(BufferPeakDN[k][0]))
                        value_left_dn = BufferPeakDN[k][1]
                if EquationDirect(bar_min, value_left_dn, bar_right_dn, value_right_dn, i + 1) > BufferAD[i + 1] and (EquationDirect(bar_min, value_left_dn, bar_right_dn, value_right_dn, i + 2) <= BufferAD[i + 2] or EquationDirect(bar_min, value_left_dn, bar_right_dn, value_right_dn, i + 3) <= BufferAD[i + 3]):
                    if InpFilterBy != FILTER_NO:
                        filter_1 = GetDataIND(InpFilterBy, i + 1)
                        filter_2 = GetDataIND(InpFilterBy, i + 2)
                        filter_3 = GetDataIND(InpFilterBy, i + 3)
                        checkFilter = (True if (filter_1 >= upper_level and filter_2 > upper_level) else False)
                    else:
                        checkFilter = True
                    if checkFilter:
                        BufferLowerArrow[i] = BufferAD[i + 1]
                        if InpDrawChartsArrow:
                            SetArrow(prefix + 'ChartArrowDN_' + TimeToString(time[i]), InpColorBearishArrow, time[i], open[i], _char(242), ANCHOR_BOTTOM, InpArrowSize)
    if InpDrawArea:
        SetRectangle(prefix + '_range', InpColorArea, time[period_find + unhecked_bars], BufferAD[ArrayMaximum(BufferAD, unhecked_bars, period_find)], time[unhecked_bars], BufferAD[ArrayMinimum(BufferAD, unhecked_bars, period_find)], InpWidthLineArea, InpStyleLineFrame, (InpStyleFrame != 0))
    if InpDrawTrendLine:
        SetTLine(prefix + '_TLineDN', InpColorTrendDN, time[bar_max], BufferAD[bar_max], time_right_up, BufferPeakUP[0][1], InpWidthTrendLine, InpStyleTrendLine, True)
        SetTLine(prefix + '_TLineUP', InpColorTrendUP, time[bar_min], BufferAD[bar_min], time_right_dn, BufferPeakDN[0][1], InpWidthTrendLine, InpStyleTrendLine, True)
    return rates_total

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))

def DirectionExtremum(a, b, c):
    if ((a - b) * (b - c)) < 0:
        if c > b:
            return 0
        if c < b:
            return 1
    return WRONG_VALUE

def ArrayMaximumInXDimm(array, rank_index=1, count=0, start_find=0):
    if ArrayRange(array, 0) == 0:
        return WRONG_VALUE
    res = 0
    num = (ArrayRange(array, 0) if (count <= 0) else count)
    value = array[start_find][rank_index]
    for i in range(start_find + 1, num):
        if array[i][rank_index] > value:
            value = array[i][rank_index]
            res = i
    return res

def ArrayMinimumInXDimm(array, rank_index=1, count=0, start_find=0):
    if ArrayRange(array, 0) <= 0:
        return WRONG_VALUE
    res = 0
    num = (ArrayRange(array, 0) if (count == 0) else count)
    value = array[start_find][rank_index]
    for i in range(start_find + 1, num):
        if array[i][rank_index] < value:
            value = array[i][rank_index]
            res = i
    return res

def SetRectangle(obj_name, obj_color, obj_time1, obj_price1, obj_time2, obj_price2, obj_width=1, obj_style=0, obj_fill=False, obj_tooltip='\n'):
    if ObjectFind(0, obj_name) < 0:
        ObjectCreate(0, obj_name, OBJ_RECTANGLE, wnd, 0, 0, 0, 0)
    ObjectSetInteger(0, obj_name, OBJPROP_TIME, 0, obj_time1)
    ObjectSetDouble(0, obj_name, OBJPROP_PRICE, 0, obj_price1)
    ObjectSetInteger(0, obj_name, OBJPROP_TIME, 1, obj_time2)
    ObjectSetDouble(0, obj_name, OBJPROP_PRICE, 1, obj_price2)
    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, obj_color)
    ObjectSetInteger(0, obj_name, OBJPROP_STYLE, obj_style)
    ObjectSetInteger(0, obj_name, OBJPROP_WIDTH, obj_width)
    ObjectSetInteger(0, obj_name, OBJPROP_FILL, obj_fill)
    ObjectSetInteger(0, obj_name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, obj_name, OBJPROP_SELECTED, False)
    ObjectSetInteger(0, obj_name, OBJPROP_HIDDEN, True)
    ObjectSetString(0, obj_name, OBJPROP_TOOLTIP, obj_tooltip)

def SetTLine(obj_name, obj_color, obj_time1, obj_price1, obj_time2, obj_price2, obj_width=1, obj_style=0, obj_ray_right=False, obj_text='', obj_tooltip='\n'):
    if ObjectFind(0, obj_name) < 0:
        ObjectCreate(0, obj_name, OBJ_TREND, wnd, 0, 0, 0, 0)
    ObjectSetInteger(0, obj_name, OBJPROP_TIME, 0, obj_time1)
    ObjectSetDouble(0, obj_name, OBJPROP_PRICE, 0, obj_price1)
    ObjectSetInteger(0, obj_name, OBJPROP_TIME, 1, obj_time2)
    ObjectSetDouble(0, obj_name, OBJPROP_PRICE, 1, obj_price2)
    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, obj_color)
    ObjectSetInteger(0, obj_name, OBJPROP_RAY_RIGHT, obj_ray_right)
    ObjectSetInteger(0, obj_name, OBJPROP_RAY_LEFT, False)
    ObjectSetInteger(0, obj_name, OBJPROP_STYLE, obj_style)
    ObjectSetInteger(0, obj_name, OBJPROP_WIDTH, obj_width)
    ObjectSetString(0, obj_name, OBJPROP_TEXT, obj_text)
    ObjectSetString(0, obj_name, OBJPROP_FONT, 'Calibri')
    ObjectSetInteger(0, obj_name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, obj_name, OBJPROP_SELECTED, False)
    ObjectSetInteger(0, obj_name, OBJPROP_HIDDEN, True)
    ObjectSetString(0, obj_name, OBJPROP_TOOLTIP, obj_tooltip)

def SetArrow(obj_name, obj_color, obj_time, obj_price, obj_code, obj_anchor, obj_size=0, obj_tooltip='\n'):
    if ObjectFind(0, obj_name) < 0:
        ObjectCreate(0, obj_name, OBJ_ARROW, 0, 0, 0)
    ObjectSetInteger(0, obj_name, OBJPROP_TIME, 0, obj_time)
    ObjectSetDouble(0, obj_name, OBJPROP_PRICE, 0, obj_price)
    ObjectSetInteger(0, obj_name, OBJPROP_ARROWCODE, obj_code)
    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, obj_color)
    ObjectSetInteger(0, obj_name, OBJPROP_WIDTH, obj_size)
    ObjectSetInteger(0, obj_name, OBJPROP_ANCHOR, obj_anchor)
    ObjectSetInteger(0, obj_name, OBJPROP_SELECTED, False)
    ObjectSetInteger(0, obj_name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, obj_name, OBJPROP_HIDDEN, True)
    ObjectSetString(0, obj_name, OBJPROP_TOOLTIP, obj_tooltip)

def GetDataIND(filtered_indicator, index):
    _sw1 = filtered_indicator
    return BufferCCI[index]

def CorrectInputValue(filtered_indicator):
    global AppliedPriceCCI, period_cci
    _sw2 = filtered_indicator
    period_cci = 14
    AppliedPriceCCI = PRICE_TYPICAL

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ICrossAD(_MQL5Indicator):
    name = 'iCrossAD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAppliedVolime': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # AD applied volume
        'InpPeriodFind': 60,  # Bars for calculate
        'InpUnheckedBars': 3,  # Unchecked bars
        'InpFilterBy': _Choice({0: 'Without filtration', 1: 'Filter by CCI'}, default=1),  # Filtering indicator
        'InpUseDefaultSetting': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use settings by default CCI parameters
        'InpPeriodIND': 14,  # CCI period
        'InpAppliedPriceCCI': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # CCI applied price
        'InpUpperLevelIND': 100.0,  # The upper level of the filter indicator
        'InpLowerLevelIND': -100.0,  # The lower level of the filter indicator
        'InpDrawChartsArrow': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Draw arrows on chart
        'InpArrowSize': _Choice({1: '1', 2: '2', 3: '3', 4: '4'}, default=2),  # The size of the arrows on the chart
        'InpDrawTrendLine': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Draw a trend line
        'InpWidthTrendLine': _Choice({1: '1', 2: '2', 3: '3', 4: '4'}, default=1),  # Trend line thickness
        'InpStyleTrendLine': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Trend line style
        'InpDrawArea': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Draw the search area
        'InpStyleFrame': _Choice({1: 'Fill', 0: 'Frame'}, default=0),  # Search area style
        'InpWidthLineArea': _Choice({1: '1', 2: '2', 3: '3', 4: '4'}, default=1),  # Search area line width (if Frame mode)
        'InpStyleLineFrame': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Search area line style (if Frame mode)
    }

