"""AMA three timeframes — converted from MQL5: MQL5 Indicators/AMA three timeframes/AMA three timeframes.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'AMA three timeframes', 'source': 'MQL5 Indicators/AMA three timeframes/AMA three timeframes.mq5', 'folder': 'AMA three timeframes', 'inputs': [{'mql': 'InpHLineOrArrow', 'py': 'InpHLineOrArrow', 'param': 'InpHLineOrArrow', 'type': 'int', 'default': 2, 'label': 'Use object', 'sinput': False}, {'mql': 'InpTimeFrames_1', 'py': 'InpTimeFrames_1', 'param': 'InpTimeFrames_1', 'type': 'int', 'default': 16385, 'label': 'TimeFrames 1st AMA', 'sinput': False}, {'mql': 'InpTimeFrames_2', 'py': 'InpTimeFrames_2', 'param': 'InpTimeFrames_2', 'type': 'int', 'default': 16388, 'label': 'TimeFrames 2nd AMA', 'sinput': False}, {'mql': 'InpTimeFrames_3', 'py': 'InpTimeFrames_3', 'param': 'InpTimeFrames_3', 'type': 'int', 'default': 16408, 'label': 'TimeFrames 3nd AMA', 'sinput': False}, {'mql': 'ama_period', 'py': 'ama_period', 'param': 'ama_period', 'type': 'int', 'default': 15, 'label': 'period of calculation', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'int', 'default': 2, 'label': 'period of fast MA', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'int', 'default': 30, 'label': 'period of slow MA', 'sinput': False}, {'mql': 'ama_shift', 'py': 'ama_shift', 'param': 'ama_shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum HLineOrArrow
hline = 0
arrow = 1
hline_arrow = 2
_enum('HLineOrArrow', {0: 'hline', 1: 'arrow', 2: 'hline_arrow'})

# ---- inputs and global variables
InpHLineOrArrow = _input('InpHLineOrArrow', hline_arrow)  # Use object
InpTimeFrames_1 = _input('InpTimeFrames_1', PERIOD_H1)  # TimeFrames 1st AMA
InpTimeFrames_2 = _input('InpTimeFrames_2', PERIOD_H4)  # TimeFrames 2nd AMA
InpTimeFrames_3 = _input('InpTimeFrames_3', PERIOD_D1)  # TimeFrames 3nd AMA
ama_period = _input('ama_period', 15)  # period of calculation
fast_ma_period = _input('fast_ma_period', 2)  # period of fast MA
slow_ma_period = _input('slow_ma_period', 30)  # period of slow MA
ama_shift = _input('ama_shift', 0)  # horizontal shift
applied_price = _input('applied_price', PRICE_CLOSE)  # type of price
handle_1 = 0
handle_2 = 0
handle_3 = 0
short_name = ""
name_1 = ''
name_2 = ''
name_3 = ''

def OnInit():
    global handle_1, handle_2, handle_3, name_1, name_2, name_3, short_name
    handle_1 = iAMA(Symbol(), InpTimeFrames_1, ama_period, fast_ma_period, slow_ma_period, ama_shift, applied_price)
    if handle_1 == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iAMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(InpTimeFrames_1, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    handle_2 = iAMA(Symbol(), InpTimeFrames_2, ama_period, fast_ma_period, slow_ma_period, ama_shift, applied_price)
    if handle_2 == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iAMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(InpTimeFrames_2, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    handle_3 = iAMA(Symbol(), InpTimeFrames_3, ama_period, fast_ma_period, slow_ma_period, ama_shift, applied_price)
    if handle_3 == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iAMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(InpTimeFrames_3, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    short_name = StringFormat('AMA three timeframes (%d,%d,%d)', ama_period, fast_ma_period, slow_ma_period)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    name_1 = StringSubstr(EnumToString(InpTimeFrames_1, 'ENUM_TIMEFRAMES'), 7)
    if InpHLineOrArrow == hline or InpHLineOrArrow == hline_arrow:
        if not HLineCreate(0, 'HLine ' + name_1, 0, 0.0, clrRed, STYLE_DASH):
            return INIT_FAILED
    if InpHLineOrArrow == arrow or InpHLineOrArrow == hline_arrow:
        if not ArrowRightPriceCreate(0, 'Arrow ' + name_1, 0, 0, 0.0, clrRed):
            return INIT_FAILED
    name_2 = StringSubstr(EnumToString(InpTimeFrames_2, 'ENUM_TIMEFRAMES'), 7)
    if InpHLineOrArrow == hline or InpHLineOrArrow == hline_arrow:
        if not HLineCreate(0, 'HLine ' + name_2, 0, 0.0, clrGold, STYLE_DASH):
            return INIT_FAILED
    if InpHLineOrArrow == arrow or InpHLineOrArrow == hline_arrow:
        if not ArrowRightPriceCreate(0, 'Arrow ' + name_2, 0, 0, 0.0, clrGold):
            return INIT_FAILED
    name_3 = StringSubstr(EnumToString(InpTimeFrames_3, 'ENUM_TIMEFRAMES'), 7)
    if InpHLineOrArrow == hline or InpHLineOrArrow == hline_arrow:
        if not HLineCreate(0, 'HLine ' + name_3, 0, 0.0, clrBlueViolet, STYLE_DASH):
            return INIT_FAILED
    if InpHLineOrArrow == arrow or InpHLineOrArrow == hline_arrow:
        if not ArrowRightPriceCreate(0, 'Arrow ' + name_3, 0, 0, 0.0, clrBlueViolet):
            return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if InpHLineOrArrow == hline or InpHLineOrArrow == hline_arrow:
        HLineDelete(0, 'HLine ' + name_1)
        HLineDelete(0, 'HLine ' + name_2)
        HLineDelete(0, 'HLine ' + name_3)
    if InpHLineOrArrow == arrow or InpHLineOrArrow == hline_arrow:
        ArrowRightPriceDelete(0, 'Arrow ' + name_1)
        ArrowRightPriceDelete(0, 'Arrow ' + name_2)
        ArrowRightPriceDelete(0, 'Arrow ' + name_3)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    iAMABuffer_1 = Arr(0, 0.0)
    iAMABuffer_2 = Arr(0, 0.0)
    iAMABuffer_3 = Arr(0, 0.0)
    if not FillArrayFromBuffer(iAMABuffer_1, ama_shift, handle_1, 1):
        return 0
    if not FillArrayFromBuffer(iAMABuffer_2, ama_shift, handle_2, 1):
        return 0
    if not FillArrayFromBuffer(iAMABuffer_3, ama_shift, handle_3, 1):
        return 0
    if InpHLineOrArrow == hline or InpHLineOrArrow == hline_arrow:
        HLineMove(0, 'HLine ' + name_1, iAMABuffer_1[0])
        HLineMove(0, 'HLine ' + name_2, iAMABuffer_2[0])
        HLineMove(0, 'HLine ' + name_3, iAMABuffer_3[0])
    if InpHLineOrArrow == arrow or InpHLineOrArrow == hline_arrow:
        ArrowRightPriceMove(0, 'Arrow ' + name_1, time[rates_total - 1], iAMABuffer_1[0])
        ArrowRightPriceMove(0, 'Arrow ' + name_2, time[rates_total - 1], iAMABuffer_2[0])
        ArrowRightPriceMove(0, 'Arrow ' + name_3, time[rates_total - 1], iAMABuffer_3[0])
    return rates_total

def FillArrayFromBuffer(ama_buffer, a_shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -a_shift, amount, ama_buffer) < 0:
        PrintFormat('Failed to copy data from the iAMA indicator, error code %d', GetLastError())
        return False
    return True

def HLineCreate(chart_ID=0, name='HLine', sub_window=0, price=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=False, hidden=True, z_order=0):
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_HLINE, sub_window, 0, price):
        Print('HLineCreate', ': failed to create a horizontal line! Error code = ', GetLastError())
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

def HLineMove(chart_ID=0, name='HLine', price=0.0):
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, 0, 0, price):
        Print('HLineMove', ': failed to move the horizontal line! Error code = ', GetLastError())
        return False
    return True

def HLineDelete(chart_ID=0, name='HLine'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('HLineDelete', ': failed to delete a horizontal line! Error code = ', GetLastError())
        return False
    return True

def ArrowRightPriceCreate(chart_ID=0, name='RightPrice', sub_window=0, time=0, price=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=False, hidden=True, z_order=0):
    time = Box(time)
    price = Box(price)
    ChangeArrowEmptyPoint(time, price)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_ARROW_RIGHT_PRICE, sub_window, time.v, price.v):
        Print('ArrowRightPriceCreate', ': failed to create the right price label! Error code = ', GetLastError())
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

def ArrowRightPriceMove(chart_ID=0, name='RightPrice', time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, 0, time, price):
        Print('ArrowRightPriceMove', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True

def ArrowRightPriceDelete(chart_ID=0, name='RightPrice'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('ArrowRightPriceDelete', ': failed to delete the right price label! Error code = ', GetLastError())
        return False
    return True

def ChangeArrowEmptyPoint(time, price):
    if not time.v:
        time.v = TimeCurrent()
    if not price.v:
        price.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AMAThreeTimeframes(_MQL5Indicator):
    name = 'AMA three timeframes'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpHLineOrArrow': _Choice({0: 'HLine', 1: 'Arrow', 2: 'HLine and Arrow'}, default=2),  # Use object
        'InpTimeFrames_1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # TimeFrames 1st AMA
        'InpTimeFrames_2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # TimeFrames 2nd AMA
        'InpTimeFrames_3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # TimeFrames 3nd AMA
        'ama_period': 15,  # period of calculation
        'fast_ma_period': 2,  # period of fast MA
        'slow_ma_period': 30,  # period of slow MA
        'ama_shift': 0,  # horizontal shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
    }

