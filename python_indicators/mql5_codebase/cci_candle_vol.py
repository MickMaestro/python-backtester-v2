"""CCI_Candle_Vol — converted from MQL5: MQL5 Indicators/CCI_Candle_Vol/CCI_Candle_Vol.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 17, 4: 1}, 'colors': {1: [16443110], 2: [8421376], 3: [16776960, 16711680, 8421376, 17919, 2763429, 55295], 4: [3937500]}, 'widths': {2: 1, 4: 1}, 'styles': {2: 4, 4: 4}, 'labels': {1: 'CCI_Candle_Vol Channel', 2: 'CCI_Candle_Vol Res', 3: 'CCI_Candle_Vol Open;CCI_Candle_Vol High;CCI_Candle_Vol Low;CCI_Candle_Vol Close', 4: 'CCI_Candle_Vol Supr'}, 'levels': [], 'description': [], 'name': 'CCI_Candle_Vol', 'source': 'MQL5 Indicators/CCI_Candle_Vol/CCI_Candle_Vol.mq5', 'folder': 'CCI_Candle_Vol', 'inputs': [{'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 100, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -100, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCIPeriod = _input('CCIPeriod', 14)  # период индикатора
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
HighLevel = _input('HighLevel', 100)  # уровень перекупленности
LowLevel = _input('LowLevel', -100)  # уровень перепроданности
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpCldIndBuffer = Arr(0, 0.0)
DnCldIndBuffer = Arr(0, 0.0)
CCI_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = _int(CCIPeriod)
    CCI_Handle[0] = iCCI(None, 0, CCIPeriod, PRICE_OPEN)
    if CCI_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI 1')
        return INIT_FAILED
    CCI_Handle[1] = iCCI(None, 0, CCIPeriod, PRICE_HIGH)
    if CCI_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI 2')
        return INIT_FAILED
    CCI_Handle[2] = iCCI(None, 0, CCIPeriod, PRICE_LOW)
    if CCI_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI 3')
        return INIT_FAILED
    CCI_Handle[3] = iCCI(None, 0, CCIPeriod, PRICE_CLOSE)
    if CCI_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI 4')
        return INIT_FAILED
    SetIndexBuffer(0, UpCldIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpCldIndBuffer, True)
    SetIndexBuffer(1, DnCldIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnCldIndBuffer, True)
    SetIndexBuffer(2, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(3, OpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, CloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(OpenBuffer, True)
    ArraySetAsSeries(HighBuffer, True)
    ArraySetAsSeries(LowBuffer, True)
    ArraySetAsSeries(CloseBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    SetIndexBuffer(8, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(DnIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI_Candle_Vol(' + _str(CCIPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if (((BarsCalculated(CCI_Handle[0]) < rates_total or BarsCalculated(CCI_Handle[1]) < rates_total) or BarsCalculated(CCI_Handle[2]) < rates_total) or BarsCalculated(CCI_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    vol = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Open, True)
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(Tick_Volume, True)
    else:
        ArraySetAsSeries(Volume, True)
    if CopyBuffer(CCI_Handle[0], 0, 0, to_copy, OpenBuffer) <= 0:
        return 0
    if CopyBuffer(CCI_Handle[1], 0, 0, to_copy, HighBuffer) <= 0:
        return 0
    if CopyBuffer(CCI_Handle[2], 0, 0, to_copy, LowBuffer) <= 0:
        return 0
    if CopyBuffer(CCI_Handle[3], 0, 0, to_copy, CloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(OpenBuffer[bar], CloseBuffer[bar])
        Max = MathMax(Max, LowBuffer[bar])
        Max = MathMax(Max, HighBuffer[bar])
        Min = MathMin(OpenBuffer[bar], CloseBuffer[bar])
        Min = MathMin(Min, LowBuffer[bar])
        Min = MathMin(Min, HighBuffer[bar])
        HighBuffer[bar] = Max
        LowBuffer[bar] = Min
        if VolumeType == VOLUME_TICK:
            vol = float(Tick_Volume[bar])
        else:
            vol = float(Volume[bar])
        OpenBuffer[bar] *= vol
        HighBuffer[bar] *= vol
        LowBuffer[bar] *= vol
        CloseBuffer[bar] *= vol
        if MathAbs(Open[bar] - Close[bar]) <= Gap:
            OpenBuffer[bar] = CloseBuffer[bar + 1]
        UpCldIndBuffer[bar] = HighLevel * vol
        UpIndBuffer[bar] = UpCldIndBuffer[bar]
        DnCldIndBuffer[bar] = LowLevel * vol
        DnIndBuffer[bar] = DnCldIndBuffer[bar]
        clr = _int(2.0)
        if CloseBuffer[bar] > UpIndBuffer[bar]:
            if CloseBuffer[bar] >= OpenBuffer[bar]:
                clr = _int(0.0)
            else:
                clr = _int(1.0)
        elif CloseBuffer[bar] < DnIndBuffer[bar]:
            if CloseBuffer[bar] <= OpenBuffer[bar]:
                clr = _int(5.0)
            else:
                clr = _int(4.0)
        else:
            if CloseBuffer[bar] >= OpenBuffer[bar]:
                clr = _int(2.0)
            else:
                clr = _int(3.0)
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCICandleVol(_MQL5Indicator):
    name = 'CCI_Candle_Vol'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCIPeriod': 14,  # период индикатора
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'HighLevel': 100,  # уровень перекупленности
        'LowLevel': -100,  # уровень перепроданности
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

