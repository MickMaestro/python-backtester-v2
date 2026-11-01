"""CandleStop_Cloud — converted from MQL5: MQL5 Indicators/CandleStop_Cloud_HTF/CandleStop_Cloud.mq5

Индикатор для подтягивания трейлинстопов с цветовым фоновым заполнением канала и с отображением последних значений в виде ценовых меток
Copyright: Copyright © 2009, CrushD; Link: CrushD; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, CrushD', 'link': 'CrushD', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1}, 'colors': {1: [13959039], 2: [12695295], 3: [13458026], 4: [3329330], 5: [9639167]}, 'widths': {3: 1, 4: 1, 5: 1}, 'styles': {3: 4, 4: 0, 5: 0}, 'labels': {1: 'Upper Cloud', 2: 'Lower Cloud', 3: 'Middle Candle Stop', 4: 'Upper Trail Stop', 5: 'Lower Trail Stop'}, 'levels': [], 'description': ['Индикатор для подтягивания трейлинстопов с цветовым фоновым заполнением канала и с отображением последних значений в виде ценовых меток'], 'name': 'CandleStop_Cloud', 'source': 'MQL5 Indicators/CandleStop_Cloud_HTF/CandleStop_Cloud.mq5', 'folder': 'CandleStop_Cloud_HTF', 'inputs': [{'mql': 'UpTrailPeriods', 'py': 'UpTrailPeriods', 'param': 'UpTrailPeriods', 'type': 'uint', 'default': 5, 'label': 'Период поиска для хая', 'sinput': False}, {'mql': 'DnTrailPeriods', 'py': 'DnTrailPeriods', 'param': 'DnTrailPeriods', 'type': 'uint', 'default': 5, 'label': 'Период поиска для лоу', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 7451452, 'label': '', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpTrailPeriods = _input('UpTrailPeriods', 5)  # Период поиска для хая
DnTrailPeriods = _input('DnTrailPeriods', 5)  # Период поиска для лоу
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Middle_color = _input('Middle_color', clrBlue)
Upper_color = _input('Upper_color', clrMediumSeaGreen)
Lower_color = _input('Lower_color', clrRed)
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
upper_name = ""
middle_name = ""
lower_name = ""

def OnInit():
    global lower_name, middle_name, min_rates_total, upper_name
    min_rates_total = _int(MathMax(UpTrailPeriods, DnTrailPeriods))
    upper_name = 'CandleStop_Cloud Upper text lable'
    middle_name = 'CandleStop_Cloud middle text lable'
    lower_name = 'CandleStop_Cloud lower text lable'
    BufferInit(0, ExtLineBuffer0)
    BufferInit(1, ExtLineBuffer1)
    BufferInit(2, ExtLineBuffer2)
    BufferInit(3, ExtLineBuffer3)
    BufferInit(4, ExtLineBuffer4)
    BufferInit(5, ExtLineBuffer5)
    BufferInit(6, ExtLineBuffer6)
    IndInit(0, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(1, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(2, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(3, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(4, EMPTY_VALUE, min_rates_total, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CandleStop_Cloud')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnDeinit(reason):
    ObjectDelete(0, upper_name)
    ObjectDelete(0, middle_name)
    ObjectDelete(0, lower_name)

def BufferInit(Number, Buffer):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Buffer, True)

def IndInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    HL = 0.0
    limit = 0
    bar = 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(time, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, UpTrailPeriods)]
        LL = low[ArrayMinimum(low, bar, DnTrailPeriods)]
        HL = (HH + LL) / 2.0
        ExtLineBuffer5[bar] = HH
        ExtLineBuffer0[bar] = ExtLineBuffer5[bar]
        ExtLineBuffer4[bar] = HL
        ExtLineBuffer2[bar] = ExtLineBuffer4[bar]
        ExtLineBuffer1[bar] = ExtLineBuffer2[bar]
        ExtLineBuffer6[bar] = LL
        ExtLineBuffer3[bar] = ExtLineBuffer6[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    SetRightPrice(0, middle_name, 0, time[0], ExtLineBuffer1[0], Middle_color, 'Georgia')
    SetRightPrice(0, upper_name, 0, time[0], ExtLineBuffer0[0], Upper_color, 'Georgia')
    SetRightPrice(0, lower_name, 0, time[0], ExtLineBuffer3[0], Lower_color, 'Georgia')
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color, Font):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color, Font):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color, Font)
    else:
        ObjectMove(chart_id, name, 0, time, price)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleStopCloud(_MQL5Indicator):
    name = 'CandleStop_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'UpTrailPeriods': 5,  # Период поиска для хая
        'DnTrailPeriods': 5,  # Период поиска для лоу
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

