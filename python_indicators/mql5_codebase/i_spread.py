"""i-spread — converted from MQL5: MQL5 Indicators/i-Spread/i-spread.mq5

Copyright: Copyright © 2013, Ким Игорь В. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Ким Игорь В. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [55295], 3: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Max', 2: 'Current', 3: 'Min'}, 'levels': [], 'description': [], 'name': 'i-spread', 'source': 'MQL5 Indicators/i-Spread/i-spread.mq5', 'folder': 'i-Spread', 'inputs': [{'mql': 'WriteInFile', 'py': 'WriteInFile', 'param': 'WriteInFile', 'type': 'bool', 'default': False, 'label': 'Записывать в файл', 'sinput': False}, {'mql': 'FileName', 'py': 'FileName', 'param': None, 'type': 'string', 'default': '', 'label': 'Имя файла', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
WriteInFile = _input('WriteInFile', False)  # Записывать в файл
FileName = _input('FileName', '')  # Имя файла
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
buf0 = Arr(0, 0.0)
buf1 = Arr(0, 0.0)
buf2 = Arr(0, 0.0)
FileName_ = ""
min_rates_total = 0
prevH1 = 0
prevH4 = 0
prevD1 = 0
maxH1 = 0.0
maxH4 = 0.0
maxD1 = 0.0
prevSpread = 0.0
minH1 = 0.0
minH4 = 0.0
minD1 = 0.0

def OnInit():
    global FileName_, min_rates_total
    min_rates_total = 3
    FileName_ = FileName
    if StringLen(FileName_) == 0:
        FileName_ = 'spr_' + StringLower(Symbol()) + '_' + GetStringTimeframe(Period()) + '.csv'
    SetIndexBuffer(0, buf0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, buf1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, buf2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-Spread')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global maxD1, maxH1, maxH4, minD1, minH1, minH4, prevD1, prevH1, prevH4, prevSpread
    if rates_total < min_rates_total:
        return 0
    bar0 = rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        for bar in range(0, bar0 + 1):
            buf0[bar] = EMPTY_VALUE
            buf1[bar] = EMPTY_VALUE
            buf2[bar] = EMPTY_VALUE
    if prev_calculated != rates_total:
        buf0[bar0] = 0.0
        buf2[bar0] = 99999999.0
    sp = spread[bar0]
    st = Box('')
    iTimeH1 = Arr(1, 0, dyn=False)
    iTimeH4 = Arr(1, 0, dyn=False)
    iTimeD1 = Arr(1, 0, dyn=False)
    if CopyTime(Symbol(), PERIOD_H1, _DT(time[bar0]), 1, iTimeH1) <= 0:
        return 0
    if CopyTime(Symbol(), PERIOD_H4, _DT(time[bar0]), 1, iTimeH4) <= 0:
        return 0
    if CopyTime(Symbol(), PERIOD_D1, _DT(time[bar0]), 1, iTimeD1) <= 0:
        return 0
    buf1[bar0] = sp
    if buf0[bar0] == EMPTY_VALUE:
        buf0[bar0] = sp
    if sp > buf0[bar0]:
        buf0[bar0] = sp
    if sp < buf2[bar0] and sp:
        buf2[bar0] = sp
    if prevH1 < iTimeH1[0]:
        maxH1 = sp
        minH1 = sp
    prevH1 = iTimeH1[0]
    if maxH1 < sp:
        maxH1 = sp
    if minH1 > sp:
        minH1 = sp
    if prevH4 < iTimeH4[0]:
        maxH4 = sp
        minH4 = sp
    prevH4 = iTimeH4[0]
    if maxH4 < sp:
        maxH4 = sp
    if minH4 > sp:
        minH4 = sp
    if prevD1 < iTimeD1[0]:
        maxD1 = sp
        minD1 = sp
    prevD1 = iTimeD1[0]
    if maxD1 < sp:
        maxD1 = sp
    if minD1 > sp:
        minD1 = sp
    StringConcatenate(st, 'Maximum on H1 = ', DoubleToString(maxH1, 2), '\n', 'Maximum on H4 = ', DoubleToString(maxH4, 2), '\n', 'Maximum on D1 = ', DoubleToString(maxD1, 2), '\n', 'Current spread = ', DoubleToString(sp, 2), '\n', 'Minimum on D1 = ', DoubleToString(minD1, 2), '\n', 'Minimum on H4 = ', DoubleToString(minH4, 2), '\n', 'Minimum on H1 = ', DoubleToString(minH1, 2), '\n')
    Comment(st.v)
    if WriteInFile:
        if prevSpread != sp:
            StringConcatenate(st, TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS), ';', DoubleToString(sp, 2))
            WritingLineInFile(FileName_, st.v)
    prevSpread = sp
    return rates_total

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def StringLower(s):
    s = Box(s)
    c = 0
    i = 0
    k = StringLen(s.v)
    n = 0
    i = 0
    for i in range(i, k):
        n = 0
        c = StringGetCharacter(s.v, i)
        if c > 64 and c < 91:
            n = c + 32
        if c > 191 and c < 224:
            n = c + 32
        if c == 168:
            n = 184
        if n > 0:
            StringSetCharacter(s, i, _ushort(n))
    else:
        i = _range_end(i, k, 1)
    return s.v

def WritingLineInFile(File_Name, text):
    file_handle = FileOpen(File_Name, FILE_READ | FILE_WRITE, ' ')
    if file_handle > 0:
        FileSeek(file_handle, 0, SEEK_END)
        FileWrite(file_handle, text)
        FileClose(file_handle)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ISpread(_MQL5Indicator):
    name = 'i-spread'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'WriteInFile': False,  # Записывать в файл
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

