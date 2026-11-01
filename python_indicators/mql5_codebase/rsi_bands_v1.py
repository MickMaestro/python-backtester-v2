"""RSI_Bands_v1 — converted from MQL5: MQL5 Indicators/RSI with BB/RSI_Bands_v1.mq5

Copyright: Copyright 2020, Fabio Cavalloni; Link: https://www.mql5.com/en/users/kava93; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Fabio Cavalloni', 'link': 'https://www.mql5.com/en/users/kava93', 'version': '1.00', 'indicator_buffers': 6, 'indicator_plots': 6, 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'RSI_Bands_v1', 'source': 'MQL5 Indicators/RSI with BB/RSI_Bands_v1.mq5', 'folder': 'RSI with BB', 'inputs': [{'mql': 'iRSIPeriod', 'py': 'iRSIPeriod', 'param': 'iRSIPeriod', 'type': 'int', 'default': 14, 'label': 'RSI periods', 'sinput': False}, {'mql': 'iBandsPeriod', 'py': 'iBandsPeriod', 'param': 'iBandsPeriod', 'type': 'int', 'default': 34, 'label': 'BB periods', 'sinput': False}, {'mql': 'iBandsDeviation', 'py': 'iBandsDeviation', 'param': 'iBandsDeviation', 'type': 'double', 'default': 2.5, 'label': 'BB deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iRSIPeriod = _input('iRSIPeriod', 14)  # RSI periods
iBandsPeriod = _input('iBandsPeriod', 34)  # BB periods
iBandsDeviation = _input('iBandsDeviation', 2.5)  # BB deviation
ExtRSI = Arr(0, 0.0)
ExtUp = Arr(0, 0.0)
ExtDn = Arr(0, 0.0)
ExtMd = Arr(0, 0.0)
ExtBuyArrow = Arr(0, 0.0)
ExtSellArrow = Arr(0, 0.0)
RSI = Arr(0, 0.0)
BBUp = Arr(0, 0.0)
BBMd = Arr(0, 0.0)
BBDn = Arr(0, 0.0)
RSI_Handle = 0
BB_Handle = 0

def OnInit():
    global BB_Handle, RSI_Handle
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI(' + _str(iRSIPeriod) + ') Bands(' + _str(iBandsPeriod) + ',' + DoubleToString(iBandsDeviation, 2) + ')')
    SetIndexBuffer(0, ExtRSI)
    SetIndexStyle(0, DRAW_LINE, STYLE_SOLID, 1, clrDodgerBlue)
    SetIndexLabel(0, 'RSI')
    SetIndexBuffer(1, ExtUp)
    SetIndexStyle(1, DRAW_LINE, STYLE_DOT, 1, clrBlack)
    SetIndexLabel(1, 'Upper band')
    SetIndexBuffer(2, ExtDn)
    SetIndexStyle(2, DRAW_LINE, STYLE_DOT, 1, clrBlack)
    SetIndexLabel(2, 'Lower band')
    SetIndexBuffer(3, ExtMd)
    SetIndexStyle(3, DRAW_LINE, STYLE_DOT, 1, clrBlack)
    SetIndexLabel(3, 'Middle band')
    SetIndexBuffer(4, ExtBuyArrow)
    SetIndexStyle(4, DRAW_ARROW, 0, 1, clrGreen)
    PlotIndexSetInteger(4, PLOT_ARROW, 225)
    SetIndexLabel(4, 'Buy arrow')
    SetIndexBuffer(5, ExtSellArrow)
    SetIndexStyle(5, DRAW_ARROW, 0, 1, clrRed)
    PlotIndexSetInteger(5, PLOT_ARROW, 226)
    SetIndexLabel(5, 'Sell arrow')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, iRSIPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, iRSIPeriod + iBandsPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, iRSIPeriod + iBandsPeriod)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, iRSIPeriod + iBandsPeriod)
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(BBUp, True)
    ArraySetAsSeries(BBDn, True)
    ArraySetAsSeries(BBMd, True)
    ArraySetAsSeries(ExtRSI, True)
    ArraySetAsSeries(ExtUp, True)
    ArraySetAsSeries(ExtDn, True)
    ArraySetAsSeries(ExtMd, True)
    ArraySetAsSeries(ExtBuyArrow, True)
    ArraySetAsSeries(ExtSellArrow, True)
    RSI_Handle = iRSI(None, 0, iRSIPeriod, PRICE_CLOSE)
    BB_Handle = iBands(None, 0, iBandsPeriod, 0, iBandsDeviation, RSI_Handle)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((not SymbolIsSynchronized(Symbol())) or rates_total < 0) or (not IndicatorsOk(rates_total)):
        return 0
    limit = MathMin(rates_total - prev_calculated + 1, rates_total - 1)
    if not FillArrayFromBuffer(RSI, 0, RSI_Handle, limit, 0):
        return rates_total
    if not FillArrayFromBuffer(BBMd, 0, BB_Handle, limit, 0):
        return rates_total
    if not FillArrayFromBuffer(BBUp, 0, BB_Handle, limit, 1):
        return rates_total
    if not FillArrayFromBuffer(BBDn, 0, BB_Handle, limit, 2):
        return rates_total
    for i in range(0, limit):
        ExtRSI[i] = RSI[i]
    for i in range(0, limit):
        ExtUp[i] = BBUp[i]
        ExtMd[i] = BBMd[i]
        ExtDn[i] = BBDn[i]
        ExtBuyArrow[i] = EMPTY_VALUE
        ExtSellArrow[i] = EMPTY_VALUE
    for i in range(1, limit):
        BuyArrow = ExtRSI[i] > ExtDn[i] and ExtRSI[i + 1] <= ExtDn[i + 1]
        SellArrow = ExtRSI[i] < ExtUp[i] and ExtRSI[i + 1] >= ExtUp[i + 1]
        if BuyArrow:
            ExtBuyArrow[i] = ExtDn[i]
        if SellArrow:
            ExtSellArrow[i] = ExtUp[i]
    return rates_total

def IndicatorsOk(rates):
    if BarsCalculated(RSI_Handle) < rates:
        return False
    if BarsCalculated(BB_Handle) < rates:
        return False
    return True

def FillArrayFromBuffer(values, shift, ind_handle, amount, buffer):
    ResetLastError()
    if CopyBuffer(ind_handle, buffer, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the indicator handle, error code %d', GetLastError())
        return False
    return True

def SetIndexStyle(index, type_, style=1, width=1, clr=clrNONE):
    if width > -1:
        PlotIndexSetInteger(index, PLOT_LINE_WIDTH, width)
    if clr != CLR_NONE:
        PlotIndexSetInteger(index, PLOT_LINE_COLOR, clr)
    _sw1 = type_
    if _sw1 == 0:
        PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_LINE)
    elif _sw1 == 1:
        PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_SECTION)
    elif _sw1 == 2:
        PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    elif _sw1 == 3:
        PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_ARROW)
    elif _sw1 == 4:
        PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_ZIGZAG)
    elif _sw1 == 12:
        PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_NONE)
    else:
        PlotIndexSetInteger(index, PLOT_DRAW_TYPE, DRAW_LINE)
    _sw2 = style
    if _sw2 == STYLE_SOLID:
        PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_SOLID)
    elif _sw2 == STYLE_DASH:
        PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DASH)
    elif _sw2 == STYLE_DOT:
        PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DOT)
    elif _sw2 == STYLE_DASHDOT:
        PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DASHDOT)
    elif _sw2 == STYLE_DASHDOTDOT:
        PlotIndexSetInteger(index, PLOT_LINE_STYLE, STYLE_DASHDOTDOT)
    else:
        return

def SetIndexLabel(index, label):
    PlotIndexSetString(index, PLOT_LABEL, label)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIBandsV1(_MQL5Indicator):
    name = 'RSI_Bands_v1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iRSIPeriod': 14,  # RSI periods
        'iBandsPeriod': 34,  # BB periods
        'iBandsDeviation': 2.5,  # BB deviation
    }
    y_range = (0.0, 100.0)

