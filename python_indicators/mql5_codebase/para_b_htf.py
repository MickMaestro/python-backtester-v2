"""Para_B_HTF — converted from MQL5: MQL5 Indicators/Para_B_HTF/Para_B_HTF.mq5

десять параболиков  с фиксированными во входных параметрах таймфреймами
Copyright: Copyright © 2017, Leonid Basis; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Leonid Basis', 'link': '', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 10}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5}, 'colors': {1: [13850042], 2: [13850042], 3: [13850042], 4: [13850042], 5: [13850042], 6: [13850042], 7: [13850042], 8: [13850042], 9: [13850042], 10: [13850042]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2}, 'styles': {}, 'labels': {1: 'Sar', 2: 'Sar2', 3: 'Sar3', 4: 'Sar4', 5: 'Sar5', 6: 'Sar6', 7: 'Sar7', 8: 'Sar8', 9: 'Sar9', 10: 'Sar10'}, 'levels': [], 'description': ['десять параболиков  с фиксированными во входных параметрах таймфреймами'], 'name': 'Para_B_HTF', 'source': 'MQL5 Indicators/Para_B_HTF/Para_B_HTF.mq5', 'folder': 'Para_B_HTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 30, 'label': 'Период графика индикатора 1', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'Период графика индикатора 2', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16386, 'label': 'Период графика индикатора 3', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16387, 'label': 'Период графика индикатора 4', 'sinput': False}, {'mql': 'TimeFrame5', 'py': 'TimeFrame5', 'param': 'TimeFrame5', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора 5', 'sinput': False}, {'mql': 'TimeFrame6', 'py': 'TimeFrame6', 'param': 'TimeFrame6', 'type': 'int', 'default': 16390, 'label': 'Период графика индикатора 6', 'sinput': False}, {'mql': 'TimeFrame7', 'py': 'TimeFrame7', 'param': 'TimeFrame7', 'type': 'int', 'default': 16392, 'label': 'Период графика индикатора 7', 'sinput': False}, {'mql': 'TimeFrame8', 'py': 'TimeFrame8', 'param': 'TimeFrame8', 'type': 'int', 'default': 16396, 'label': 'Период графика индикатора 8', 'sinput': False}, {'mql': 'TimeFrame9', 'py': 'TimeFrame9', 'param': 'TimeFrame9', 'type': 'int', 'default': 16408, 'label': 'Период графика индикатора 9', 'sinput': False}, {'mql': 'TimeFrame10', 'py': 'TimeFrame10', 'param': 'TimeFrame10', 'type': 'int', 'default': 32769, 'label': 'Период графика индикатора 10', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'double', 'default': 0.01, 'label': '', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_M30)  # Период графика индикатора 1
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # Период графика индикатора 2
TimeFrame3 = _input('TimeFrame3', PERIOD_H2)  # Период графика индикатора 3
TimeFrame4 = _input('TimeFrame4', PERIOD_H3)  # Период графика индикатора 4
TimeFrame5 = _input('TimeFrame5', PERIOD_H4)  # Период графика индикатора 5
TimeFrame6 = _input('TimeFrame6', PERIOD_H6)  # Период графика индикатора 6
TimeFrame7 = _input('TimeFrame7', PERIOD_H8)  # Период графика индикатора 7
TimeFrame8 = _input('TimeFrame8', PERIOD_H12)  # Период графика индикатора 8
TimeFrame9 = _input('TimeFrame9', PERIOD_D1)  # Период графика индикатора 9
TimeFrame10 = _input('TimeFrame10', PERIOD_W1)  # Период графика индикатора 10
Step = _input('Step', 0.01)
Maximum = _input('Maximum', 0.5)
min_rates_total = 0
TimeFrame = Arr(10, 0, dyn=False)
Ind_Handle = Arr(10, 0, dyn=False)

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 2
    TimeFrame[0] = TimeFrame1
    TimeFrame[1] = TimeFrame2
    TimeFrame[2] = TimeFrame3
    TimeFrame[3] = TimeFrame4
    TimeFrame[4] = TimeFrame5
    TimeFrame[5] = TimeFrame6
    TimeFrame[6] = TimeFrame7
    TimeFrame[7] = TimeFrame8
    TimeFrame[8] = TimeFrame9
    TimeFrame[9] = TimeFrame10
    for numb in range(0, 10):
        Ind_Handle[numb] = iSAR(Symbol(), TimeFrame[numb], Step, Maximum)
        if Ind_Handle[numb] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iSAR ' + _str(numb) + '!')
            return INIT_FAILED
    for numb in range(0, 10):
        IndInit(numb, Ind[numb].IndBuffer, EMPTY_VALUE, min_rates_total, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Para_B_HTF')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for numb in range(0, 10):
        if BarsCalculated(Ind_Handle[numb]) < Bars(Symbol(), TimeFrame[numb]):
            return prev_calculated
    ArraySetAsSeries(time, True)
    for numb in range(0, 10):
        if not CountIndicator(numb, Symbol(), TimeFrame[numb], Ind_Handle[numb], 0, Ind[numb].IndBuffer, time, rates_total, prev_calculated, min_rates_total):
            return prev_calculated
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

# ---- global variables initialised from expressions
Ind = Arr(10, 0, dyn=False, factory=CIndicatorsBuffers)

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(10, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ParaBHTF(_MQL5Indicator):
    name = 'Para_B_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # Период графика индикатора 1
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Период графика индикатора 2
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # Период графика индикатора 3
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16387),  # Период графика индикатора 4
        'TimeFrame5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора 5
        'TimeFrame6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Период графика индикатора 6
        'TimeFrame7': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16392),  # Период графика индикатора 7
        'TimeFrame8': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # Период графика индикатора 8
        'TimeFrame9': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Период графика индикатора 9
        'TimeFrame10': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=32769),  # Период графика индикатора 10
        'Step': 0.01,
        'Maximum': 0.5,
    }

