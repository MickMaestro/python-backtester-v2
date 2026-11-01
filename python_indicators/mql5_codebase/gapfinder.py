"""GapFinder — converted from MQL5: MQL5 Indicators/GapFinder/GapFinder.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 5, 6: 5}, 'colors': {1: [16748574], 2: [36095], 3: [16748574], 4: [36095], 5: [16748574], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Upper up area', 2: 'Lower up area', 3: 'Upper down area', 4: 'Lower down area', 5: 'Arrow up', 6: 'Arrow down'}, 'levels': [], 'description': [], 'name': 'GapFinder', 'source': 'MQL5 Indicators/GapFinder/GapFinder.mq5', 'folder': 'GapFinder', 'inputs': [{'mql': 'InpMinGapSize', 'py': 'InpMinGapSize', 'param': 'InpMinGapSize', 'type': 'uint', 'default': 2, 'label': 'Minimum gap size (in points)', 'sinput': False}, {'mql': 'InpDrawArea', 'py': 'InpDrawArea', 'param': 'InpDrawArea', 'type': 'int', 'default': 1, 'label': 'Whether to draw a gap area', 'sinput': False}, {'mql': 'InpColorToUP', 'py': 'InpColorToUP', 'param': None, 'type': 'color', 'default': 13422920, 'label': 'Color of the gap area up', 'sinput': False}, {'mql': 'InpColorToDN', 'py': 'InpColorToDN', 'param': None, 'type': 'color', 'default': 55295, 'label': 'Color of the gap area down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpMinGapSize = _input('InpMinGapSize', 2)  # Minimum gap size (in points)
InpDrawArea = _input('InpDrawArea', INPUT_YES)  # Whether to draw a gap area
InpColorToUP = _input('InpColorToUP', clrMediumTurquoise)  # Color of the gap area up
InpColorToDN = _input('InpColorToDN', clrGold)  # Color of the gap area down
BufferLineToUpUP = Arr(0, 0.0)
BufferLineToUpDN = Arr(0, 0.0)
BufferLineToDnUP = Arr(0, 0.0)
BufferLineToDnDN = Arr(0, 0.0)
BufferArrowUP = Arr(0, 0.0)
BufferArrowDN = Arr(0, 0.0)
min_gap_size = 0.0
prefix = ""

def OnInit():
    global min_gap_size, prefix
    min_gap_size = (1 if (InpMinGapSize < 1) else InpMinGapSize) * Point()
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    SetIndexBuffer(0, BufferLineToUpUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLineToUpDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLineToDnUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLineToDnDN, INDICATOR_DATA)
    SetIndexBuffer(4, BufferArrowUP, INDICATOR_DATA)
    SetIndexBuffer(5, BufferArrowDN, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_ARROW, 241)
    PlotIndexSetInteger(5, PLOT_ARROW, 242)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Gap finder(' + _str(min_gap_size) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferLineToUpUP, True)
    ArraySetAsSeries(BufferLineToUpDN, True)
    ArraySetAsSeries(BufferLineToDnUP, True)
    ArraySetAsSeries(BufferLineToDnDN, True)
    ArraySetAsSeries(BufferArrowUP, True)
    ArraySetAsSeries(BufferArrowDN, True)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 5
        BuffersInitialize()
    for i in range(limit, 0 - 1, -1):
        if (low[i] - high[i + 1]) >= min_gap_size:
            BufferArrowUP[i] = high[i + 1]
            if BufferArrowUP[i + 1] != EMPTY_VALUE:
                up = fmin(open[i + 1], close[i + 1])
                dn = fmax(open[i + 2], close[i + 2])
                SetGapToUP(0.0, 0.0, i + 2)
            up = fmin(open[i], close[i])
            dn = fmax(open[i + 1], close[i + 1])
            SetGapToUP(up, dn, i)
            DrawArea(i, up, dn, time, InpColorToUP, 1)
        else:
            BufferArrowUP[i] = EMPTY_VALUE
            if BufferArrowUP[i + 1] == EMPTY_VALUE:
                SetGapToUP(0.0, 0.0, i)
        if (low[i + 1] - high[i]) >= min_gap_size:
            BufferArrowDN[i] = low[i + 1]
            if BufferArrowDN[i + 1] != EMPTY_VALUE:
                up = fmin(open[i + 2], close[i + 2])
                dn = fmax(open[i + 1], close[i + 1])
                SetGapToDN(0.0, 0.0, i + 2)
            up = fmin(open[i + 1], close[i + 1])
            dn = fmax(open[i], close[i])
            SetGapToDN(up, dn, i)
            DrawArea(i, up, dn, time, InpColorToDN, 0)
        else:
            BufferArrowDN[i] = EMPTY_VALUE
            if BufferArrowDN[i + 1] == EMPTY_VALUE:
                SetGapToDN(0.0, 0.0, i)
    return rates_total

def BuffersInitialize():
    ArrayInitialize(BufferLineToUpUP, EMPTY_VALUE)
    ArrayInitialize(BufferLineToUpDN, EMPTY_VALUE)
    ArrayInitialize(BufferLineToDnUP, EMPTY_VALUE)
    ArrayInitialize(BufferLineToDnDN, EMPTY_VALUE)
    ArrayInitialize(BufferArrowUP, EMPTY_VALUE)
    ArrayInitialize(BufferArrowDN, EMPTY_VALUE)

def SetGapToUP(price_up, price_dn, shift):
    BufferLineToUpUP[shift + 1] = (price_up if (price_up > 0) else EMPTY_VALUE)
    BufferLineToUpUP[shift] = BufferLineToUpUP[shift + 1]
    BufferLineToUpDN[shift + 1] = (price_dn if (price_dn > 0) else EMPTY_VALUE)
    BufferLineToUpDN[shift] = BufferLineToUpDN[shift + 1]

def SetGapToDN(price_up, price_dn, shift):
    BufferLineToDnUP[shift + 1] = (price_up if (price_up > 0) else EMPTY_VALUE)
    BufferLineToDnUP[shift] = BufferLineToDnUP[shift + 1]
    BufferLineToDnDN[shift + 1] = (price_dn if (price_dn > 0) else EMPTY_VALUE)
    BufferLineToDnDN[shift] = BufferLineToDnDN[shift + 1]

def DrawArea(index, price_up, price_dn, time, color_area, dir):
    if not InpDrawArea:
        return
    name = prefix + ('up_' if (dir > 0) else 'dn_') + TimeToString(time[index])
    if ObjectFind(0, name) < 0:
        ObjectCreate(0, name, OBJ_RECTANGLE, 0, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_FILL, True)
    ObjectSetInteger(0, name, OBJPROP_BACK, True)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(0, name, OBJPROP_COLOR, color_area)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time[index + 1])
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, time[index])
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price_up)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price_dn)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GapFinder(_MQL5Indicator):
    name = 'GapFinder'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMinGapSize': 2,  # Minimum gap size (in points)
        'InpDrawArea': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Whether to draw a gap area
    }

