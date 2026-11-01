"""trendmagic_htf — converted from MQL5: MQL5 Indicators/TrendMagic_HTF/trendmagic_htf.mq5

TrendMagic with the timeframe selection option available in input parameters
Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 16711935]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [], 'description': ['TrendMagic with the timeframe selection option available in input parameters'], 'name': 'trendmagic_htf', 'source': 'MQL5 Indicators/TrendMagic_HTF/trendmagic_htf.mq5', 'folder': 'TrendMagic_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Indicator chart period', 'sinput': False}, {'mql': 'CCI_Period', 'py': 'CCI_Period', 'param': 'CCI_Period', 'type': 'uint', 'default': 50, 'label': 'CCI period', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': 'CCI price', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 5, 'label': 'ATR period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Indicator chart period
CCI_Period = _input('CCI_Period', 50)  # CCI period
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)  # CCI price
ATR_Period = _input('ATR_Period', 5)  # ATR period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if not TimeFramesCheck('TrendMagic', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'TrendMagic' + ' indicator: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'TrendMagic', CCI_Period, CCIPrice, ATR_Period, 0, PriceShift)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the TrendMagic indicator')
        return INIT_FAILED
    IndInit(0, IndBuffer, ColorIndBuffer, 0.0, min_rates_total, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'TrendMagic', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer, 1, ColorIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, ColorBuffer, Empty_Value, Draw_Begin, nShift):
    indnumb = 2 * Number
    plotnumb = indnumb
    SetIndexBuffer(indnumb, Buffer, INDICATOR_DATA)
    SetIndexBuffer(indnumb + 1, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(plotnumb, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(plotnumb, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(plotnumb, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)
    ArraySetAsSeries(ColorBuffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, ColBuffNumb, ColIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol_, TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            ColArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, ColBuffNumb, _DT(iTime_[bar]), 1, ColArr) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
            ColIndBuf[bar] = ColArr[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
            ColIndBuf[bar] = ColIndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Chart period for the ' + IndName + ' indicator cannot be less than the period of the current chart!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendmagicHtf(_MQL5Indicator):
    name = 'trendmagic_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator chart period
        'CCI_Period': 50,  # CCI period
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # CCI price
        'ATR_Period': 5,  # ATR period
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

