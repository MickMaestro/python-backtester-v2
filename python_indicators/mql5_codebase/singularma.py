"""singularma — converted from MQL5: MQL5 Indicators/Trend indicator based on singular spectrum analysis/singularma.mq5

Copyright: Copyright 2016, Roman Korotchenko; Link: https://login.mql5.com/ru/users/Solitonic; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Missing include files: Math\\Alglib\\linalg.mqh
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.ssa_ccaterpillar import *  # #include CCaterpillar.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2016, Roman Korotchenko', 'link': 'https://login.mql5.com/ru/users/Solitonic', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Trend SSA'}, 'levels': [], 'description': [], 'name': 'singularma', 'source': 'MQL5 Indicators/Trend indicator based on singular spectrum analysis/singularma.mq5', 'folder': 'Trend indicator based on singular spectrum analysis', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 0, 'label': 'Calculation period to build the chart', 'sinput': False}, {'mql': 'period_to_redraw', 'py': 'period_to_redraw', 'param': 'period_to_redraw', 'type': 'int', 'default': 3, 'label': 'Refresh period chart', 'sinput': False}, {'mql': 'SegmentLength', 'py': 'SegmentLength', 'param': 'SegmentLength', 'type': 'int', 'default': 120, 'label': 'Фрагмент истории', 'sinput': False}, {'mql': 'SegmentLag', 'py': 'SegmentLag', 'param': 'SegmentLag', 'type': 'int', 'default': 50, 'label': 'Окно (в пределах от 1/4 до 1/2 длины сегмента)', 'sinput': False}, {'mql': 'EigMax', 'py': 'EigMax', 'param': 'EigMax', 'type': 'int', 'default': 10, 'label': 'Число мод (размерность подпространства сигнала. "Вне" - ошибки)', 'sinput': False}, {'mql': 'EigNoiseLevel', 'py': 'EigNoiseLevel', 'param': 'EigNoiseLevel', 'type': 'double', 'default': 2.0, 'label': 'Допускаемый процент вклада шума в суммарную "энергию колебаний" ряда', 'sinput': False}, {'mql': 'EigNoiseFlag', 'py': 'EigNoiseFlag', 'param': 'EigNoiseFlag', 'type': 'int', 'default': 0, 'label': 'Метод ограничения числа мод', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': ['Math\\Alglib\\linalg.mqh'], 'imports': [], 'libraries': ['CCaterpillar.mqh']}

# ---- inputs and global variables
period = _input('period', PERIOD_CURRENT)  # Calculation period to build the chart
period_to_redraw = _input('period_to_redraw', PERIOD_M3)  # Refresh period chart
SegmentLength = _input('SegmentLength', 120)  # Фрагмент истории
SegmentLag = _input('SegmentLag', 50)  # Окно (в пределах от 1/4 до 1/2 длины сегмента)
EigMax = _input('EigMax', 10)  # Число мод (размерность подпространства сигнала. "Вне" - ошибки)
EigNoiseLevel = _input('EigNoiseLevel', 2.0)  # Допускаемый процент вклада шума в суммарную "энергию колебаний" ряда
EigNoiseFlag = _input('EigNoiseFlag', 0)  # Метод ограничения числа мод
TrendBuffer = Arr(0, 0.0)
ResultBuffer = Arr(0, 0.0)
EigMin = 1
wrkData = Arr(0, 0.0)
OldSegmentLength = 0
OldSegmentLag = 0
start_data = 0  # Start time to build the chart
stop_data = 0  # Текущее время
reCalcOn = 0
curCalcFinish = 1
ReCalcLim = 7

def OnInit():
    global OldSegmentLag, OldSegmentLength
    SetIndexBuffer(0, TrendBuffer, INDICATOR_DATA)
    OldSegmentLength = 0
    OldSegmentLag = 0
    ArrayResize(wrkData, SegmentLength, 32768)
    ArrayResize(ResultBuffer, SegmentLength, 32768)
    shortname = Box("")
    StringConcatenate(shortname, 'SSA(', SegmentLength, ',', SegmentLag, ')', 'C.Ф. 1-', EigMax)
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global OldSegmentLag, OldSegmentLength, curCalcFinish, reCalcOn, start_data, stop_data
    idx = 0
    nshift = 0
    ntime = 0
    fEigMin = 1
    fEigMax = EigMax
    if rates_total < SegmentLength:
        PrintFormat('Число данных меньше длины индикатора. Без расчета.')
        return 0
    reCalcOn += 1
    curCalcFinish = (0 if (reCalcOn != 1) else 1)
    reCalcOn = _int(MathMod(reCalcOn, ReCalcLim))
    if not curCalcFinish:
        if prev_calculated != 0:
            ArrayCopy(TrendBuffer, ResultBuffer, rates_total - SegmentLength, 0, SegmentLength)
        else:
            ArrayFill(TrendBuffer, 0, rates_total, EMPTY_VALUE)
        return rates_total
    if ArraySize(wrkData) < SegmentLength:
        ArrayResize(wrkData, SegmentLength, 32768)
        reCalcOn = 1
    if OldSegmentLength != SegmentLength or OldSegmentLag != SegmentLag:
        Caterpillar.TrendSize(SegmentLength, SegmentLag)
        OldSegmentLength = SegmentLength
        OldSegmentLag = SegmentLag
        reCalcOn = 1
        if ArraySize(ResultBuffer) < SegmentLength:
            ArrayResize(ResultBuffer, 2 * SegmentLength, 32768)
        ArrayFill(ResultBuffer, 0, SegmentLength, EMPTY_VALUE)
        ArrayFill(TrendBuffer, 0, rates_total, EMPTY_VALUE)
    curCalcFinish = 0
    ntime = ArraySize(time)
    nshift = ntime - SegmentLength
    for i in range(0, SegmentLength):
        idx = i + nshift
        wrkData[i] = (high[idx] + low[idx] + close[idx]) / 3
    Caterpillar.SetNoiseRegime(EigNoiseFlag, EigNoiseLevel)
    Caterpillar.DoAnalyse(wrkData, SegmentLength, SegmentLag, fEigMin, fEigMax)
    start_data = time[nshift]
    stop_data = time[nshift + SegmentLength - 1]
    ArrayFill(ResultBuffer, 0, SegmentLength, EMPTY_VALUE)
    for i in range(0, SegmentLength):
        ResultBuffer[i] = Caterpillar.Trend[i]
    ArrayCopy(TrendBuffer, ResultBuffer, rates_total - SegmentLength, 0, SegmentLength)
    ChartRedraw(0)
    curCalcFinish = 1
    return rates_total

# ---- global variables initialised from expressions
Caterpillar = _alloc(CCaterpillar)
Caterpillar.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Singularma(_MQL5Indicator):
    name = 'singularma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Calculation period to build the chart
        'period_to_redraw': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=3),  # Refresh period chart
        'SegmentLength': 120,  # Фрагмент истории
        'SegmentLag': 50,  # Окно (в пределах от 1/4 до 1/2 длины сегмента)
        'EigMax': 10,  # Число мод (размерность подпространства сигнала. "Вне" - ошибки)
        'EigNoiseLevel': 2.0,  # Допускаемый процент вклада шума в суммарную "энергию колебаний" ряда
        'EigNoiseFlag': 0,  # Метод ограничения числа мод
    }

