"""donchian_fibo_clouds — converted from MQL5: MQL5 Indicators/Donchian_Fibo_Clouds/donchian_fibo_clouds.mq5

Copyright: Copyright © 2015, Guilherme Santos; Link: fishguil@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Guilherme Santos', 'link': 'fishguil@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7}, 'colors': {1: [16748574], 2: [16760576], 3: [16776960], 4: [65535], 5: [55295], 6: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Fibo 1.000', 2: 'Fibo 0.786', 3: 'Fibo 0.618', 4: 'Fibo 0.500', 5: 'Fibo 0.382', 6: 'Fibo 0.214'}, 'levels': [], 'description': [], 'name': 'donchian_fibo_clouds', 'source': 'MQL5 Indicators/Donchian_Fibo_Clouds/donchian_fibo_clouds.mq5', 'folder': 'Donchian_Fibo_Clouds', 'inputs': [{'mql': 'FiboPeriod', 'py': 'FiboPeriod', 'param': 'FiboPeriod', 'type': 'uint', 'default': 72, 'label': 'Period of averaging', 'sinput': False}, {'mql': 'Extremes', 'py': 'Extremes', 'param': 'Extremes', 'type': 'int', 'default': 0, 'label': 'Type of extreme points', 'sinput': False}, {'mql': 'Margins', 'py': 'Margins', 'param': 'Margins', 'type': 'int', 'default': -2, 'label': '', 'sinput': False}, {'mql': 'Level1', 'py': 'Level1', 'param': 'Level1', 'type': 'double', 'default': 0.786, 'label': '', 'sinput': False}, {'mql': 'Level2', 'py': 'Level2', 'param': 'Level2', 'type': 'double', 'default': 0.618, 'label': '', 'sinput': False}, {'mql': 'Level3', 'py': 'Level3', 'param': 'Level3', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'Level4', 'py': 'Level4', 'param': 'Level4', 'type': 'double', 'default': 0.382, 'label': '', 'sinput': False}, {'mql': 'Level5', 'py': 'Level5', 'param': 'Level5', 'type': 'double', 'default': 0.214, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_Extrem
HIGH_LOW = 0
HIGH_LOW_OPEN = 1
HIGH_LOW_CLOSE = 2
OPEN_HIGH_LOW = 3
CLOSE_HIGH_LOW = 4
_enum('Applied_Extrem', {0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'})

# ---- inputs and global variables
FiboPeriod = _input('FiboPeriod', 72)  # Period of averaging
Extremes = _input('Extremes', HIGH_LOW)  # Type of extreme points
Margins = _input('Margins', -2)
Level1 = _input('Level1', 0.786)
Level2 = _input('Level2', 0.618)
Level3 = _input('Level3', 0.5)
Level4 = _input('Level4', 0.382)
Level5 = _input('Level5', 0.214)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars

class CIndBuffers(MqlObject):
    _q_fields = ('m_UpBuffer', 'm_DnBuffer')
    def __init__(self, *args):
        self.m_UpBuffer = Arr(0, 0.0)
        self.m_DnBuffer = Arr(0, 0.0)

def OnInit():
    for numb in range(0, 6):
        count = numb * 2
        SetIndexBuffer(count, Ind[numb].m_UpBuffer, INDICATOR_DATA)
        SetIndexBuffer(count + 1, Ind[numb].m_DnBuffer, INDICATOR_DATA)
        PlotIndexSetInteger(numb, PLOT_SHIFT, Shift)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, FiboPeriod)
        ArraySetAsSeries(Ind[numb].m_UpBuffer, True)
        ArraySetAsSeries(Ind[numb].m_DnBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Donchian Fibo(Period = ', FiboPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (_int(FiboPeriod) + 1):
        return 0
    smin = 0.0
    smax = 0.0
    sdiff = 0.0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - _int(FiboPeriod)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        _sw1 = Extremes
        if _sw1 == HIGH_LOW:
            smax = high[ArrayMaximum(high, bar, FiboPeriod)]
            smin = low[ArrayMinimum(low, bar, FiboPeriod)]
        elif _sw1 == HIGH_LOW_OPEN:
            smax = (open[ArrayMaximum(open, bar, FiboPeriod)] + high[ArrayMaximum(high, bar, FiboPeriod)]) / 2
            smin = (open[ArrayMinimum(open, bar, FiboPeriod)] + low[ArrayMinimum(low, bar, FiboPeriod)]) / 2
        elif _sw1 == HIGH_LOW_CLOSE:
            smax = (close[ArrayMaximum(close, bar, FiboPeriod)] + high[ArrayMaximum(high, bar, FiboPeriod)]) / 2
            smin = (close[ArrayMinimum(close, bar, FiboPeriod)] + low[ArrayMinimum(low, bar, FiboPeriod)]) / 2
        elif _sw1 == OPEN_HIGH_LOW:
            smax = open[ArrayMinimum(open, bar, FiboPeriod)]
            smin = open[ArrayMaximum(open, bar, FiboPeriod)]
        elif _sw1 == CLOSE_HIGH_LOW:
            smax = close[ArrayMaximum(close, bar, FiboPeriod)]
            smin = close[ArrayMinimum(close, bar, FiboPeriod)]
        sdiff = smax - smin
        Ind[0].m_UpBuffer[bar] = smax
        Ind[1].m_UpBuffer[bar] = smin + (sdiff * Level1)
        Ind[0].m_DnBuffer[bar] = Ind[1].m_UpBuffer[bar]
        Ind[2].m_UpBuffer[bar] = smin + (sdiff * Level2)
        Ind[1].m_DnBuffer[bar] = Ind[2].m_UpBuffer[bar]
        Ind[3].m_UpBuffer[bar] = smin + (sdiff * Level3)
        Ind[2].m_DnBuffer[bar] = Ind[3].m_UpBuffer[bar]
        Ind[4].m_UpBuffer[bar] = smin + (sdiff * Level4)
        Ind[3].m_DnBuffer[bar] = Ind[4].m_UpBuffer[bar]
        Ind[5].m_UpBuffer[bar] = smin + (sdiff * Level5)
        Ind[4].m_DnBuffer[bar] = Ind[5].m_UpBuffer[bar]
        Ind[5].m_DnBuffer[bar] = smin
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(6, 0, dyn=False, factory=CIndBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianFiboClouds(_MQL5Indicator):
    name = 'donchian_fibo_clouds'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FiboPeriod': 72,  # Period of averaging
        'Extremes': _Choice({0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'}, default=0),  # Type of extreme points
        'Margins': -2,
        'Level1': 0.786,
        'Level2': 0.618,
        'Level3': 0.5,
        'Level4': 0.382,
        'Level5': 0.214,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

