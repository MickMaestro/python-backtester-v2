"""bigbarsound — converted from MQL5: MQL5 Indicators/BigBarSound/bigbarsound.mq5

Indicator plays WavFile when bar size is lager of BarPoint value
Copyright: Alexey Volchanskiy; Link: http://www.robo-forex.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Alexey Volchanskiy', 'link': 'http://www.robo-forex.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Indicator plays WavFile when bar size is lager of BarPoint value'], 'name': 'bigbarsound', 'source': 'MQL5 Indicators/BigBarSound/bigbarsound.mq5', 'folder': 'BigBarSound', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'BarPoint', 'py': 'BarPoint', 'param': 'BarPoint', 'type': 'uint', 'default': 200, 'label': 'Минимальный размер свечного хода для сигнала', 'sinput': False}, {'mql': 'SP', 'py': 'SP', 'param': 'SP', 'type': 'int', 'default': 1, 'label': 'Вариант движения', 'sinput': False}, {'mql': 'WavFile', 'py': 'WavFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Имя звукового файла', 'sinput': False}, {'mql': 'TimeDeley', 'py': 'TimeDeley', 'param': 'TimeDeley', 'type': 'uint', 'default': 10, 'label': 'Минимальная задержка между двумя сигналами', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum START_POINT
OPEN_CLOSE = 0
HIGH_LOW = 1
_enum('START_POINT', {0: 'OPEN_CLOSE', 1: 'HIGH_LOW'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
BarPoint = _input('BarPoint', 200)  # Минимальный размер свечного хода для сигнала
SP = _input('SP', HIGH_LOW)  # Вариант движения
WavFile = _input('WavFile', 'alert.wav')  # Имя звукового файла
TimeDeley = _input('TimeDeley', 10)  # Минимальная задержка между двумя сигналами

def OnInit():
    shortname = Box("")
    StringConcatenate(shortname, 'BigBarSound', '(', EnumToString(TimeFrame, 'ENUM_TIMEFRAMES'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_itime, _s_OnCalculate_lasttime
    if Bars(Symbol(), TimeFrame) < 1:
        return 0
    ArraySetAsSeries(time, True)
    range_ = 0
    iTime_ = Arr(1, 0, dyn=False)
    if SP == HIGH_LOW:
        iLow_ = Arr(1, 0.0, dyn=False)
        iHigh_ = Arr(1, 0.0, dyn=False)
        if CopyLow(Symbol(), TimeFrame, _DT(time[0]), 1, iLow_) <= 0:
            return 0
        if CopyHigh(Symbol(), TimeFrame, _DT(time[0]), 1, iHigh_) <= 0:
            return 0
        range_ = _int(_fdiv(iHigh_[0] - iLow_[0], Point()))
    else:
        iOpen_ = Arr(1, 0.0, dyn=False)
        iClose_ = Arr(1, 0.0, dyn=False)
        if CopyOpen(Symbol(), TimeFrame, _DT(time[0]), 1, iOpen_) <= 0:
            return 0
        if CopyClose(Symbol(), TimeFrame, _DT(time[0]), 1, iClose_) <= 0:
            return 0
        range_ = _int(_fdiv(MathAbs(iClose_[0] - iOpen_[0]), Point()))
    if CopyTime(Symbol(), TimeFrame, _DT(time[0]), 1, iTime_) <= 0:
        return 0
    if iTime_[0] != _s_OnCalculate_itime:
        _s_OnCalculate_lasttime = 0
        _s_OnCalculate_itime = iTime_[0]
    if (TimeCurrent() - _s_OnCalculate_lasttime) >= TimeDeley and range_ > _int(BarPoint):
        PlaySound(WavFile)
        _s_OnCalculate_lasttime = TimeCurrent()
    return rates_total

# ---- static local variables
_s_OnCalculate_lasttime = 0
_s_OnCalculate_itime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bigbarsound(_MQL5Indicator):
    name = 'bigbarsound'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'BarPoint': 200,  # Минимальный размер свечного хода для сигнала
        'SP': _Choice({0: 'ход цены от открытия open до close', 1: 'размер свечи от low до high'}, default=1),  # Вариант движения
        'TimeDeley': 10,  # Минимальная задержка между двумя сигналами
    }

