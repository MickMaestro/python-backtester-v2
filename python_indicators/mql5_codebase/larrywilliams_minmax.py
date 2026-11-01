"""larrywilliams_minmax — converted from MQL5: MQL5 Indicators/LarryWilliams_MinMax/larrywilliams_minmax.mq5

Copyright: Copyright 2014, PunkBASSter; Link: https://login.mql5.com/en/users/punkbasster; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, PunkBASSter', 'link': 'https://login.mql5.com/en/users/punkbasster', 'version': '1.1', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [32768], 2: [32768], 3: [16711680], 4: [16711680], 5: [255], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Max1', 2: 'Min1', 3: 'Max2', 4: 'Min2', 5: 'Max3', 6: 'Min3'}, 'levels': [], 'description': [], 'name': 'larrywilliams_minmax', 'source': 'MQL5 Indicators/LarryWilliams_MinMax/larrywilliams_minmax.mq5', 'folder': 'LarryWilliams_MinMax', 'inputs': [{'mql': 'IgnoreInsideBars', 'py': 'IgnoreInsideBars', 'param': 'IgnoreInsideBars', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
IgnoreInsideBars = _input('IgnoreInsideBars', True)
Max1Buffer = Arr(0, 0.0)
Min1Buffer = Arr(0, 0.0)
Max2Buffer = Arr(0, 0.0)
Min2Buffer = Arr(0, 0.0)
Max3Buffer = Arr(0, 0.0)
Min3Buffer = Arr(0, 0.0)

class LastExtremums(MqlObject):
    _q_fields = ('m_price', 'm_pos')
    def __init__(self):
        self.m_price = Arr(2, 0.0, dyn=False)
        self.m_pos = Arr(2, 0, dyn=False)
        ArrayInitialize(self.m_price, 0)
        ArrayInitialize(self.m_pos, 0)
    def _q_dtor(self):
        pass
    def push(self, price, pos):
        self.m_price[0] = self.m_price[1]
        self.m_price[1] = price
        self.m_pos[0] = self.m_pos[1]
        self.m_pos[1] = pos
    def checkMax(self, last):
        if self.m_price[0] <= self.m_price[1] and self.m_price[1] >= last:
            return self.m_pos[1]
        else:
            return 0
    def checkMin(self, last):
        if self.m_price[0] >= self.m_price[1] and self.m_price[1] <= last:
            return self.m_pos[1]
        else:
            return 0

def OnInit():
    SetIndexBuffer(0, Max1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Min1Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, Max2Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, Min2Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, Max3Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, Min3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 3)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 3)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, 3)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, 3)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, 3)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, 3)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetInteger(5, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, -4)
    PlotIndexSetInteger(3, PLOT_ARROW_SHIFT, 4)
    PlotIndexSetInteger(4, PLOT_ARROW_SHIFT, -8)
    PlotIndexSetInteger(5, PLOT_ARROW_SHIFT, 8)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def CheckShortMax(high, low, pos):
    if not IgnoreInsideBars:
        if high[pos] >= high[pos + 1] and high[pos] > high[pos - 1]:
            return high[pos]
    else:
        if high[pos - 1] >= high[pos] and low[pos - 1] <= low[pos]:
            return 0.0
        i = pos - 1
        while i > 2:
            if high[i - 1] >= high[i] and low[i - 1] <= low[i]:
                i -= 1
            else:
                break
        limit = ArraySize(high) - 2
        j = pos + 1
        while j <= limit:
            if high[j - 1] >= high[j] and low[j - 1] <= low[j]:
                j += 1
            else:
                break
        if high[pos] >= high[i] and high[pos] > high[j]:
            return high[pos]
    return 0.0

def CheckShortMin(high, low, pos):
    if not IgnoreInsideBars:
        if low[pos] <= low[pos + 1] and low[pos] < low[pos - 1]:
            return low[pos]
    else:
        if high[pos - 1] >= high[pos] and low[pos - 1] <= low[pos]:
            return 0.0
        i = pos - 1
        while i > 2:
            if high[i - 1] >= high[i] and low[i - 1] <= low[i]:
                i -= 1
            else:
                break
        limit = ArraySize(high) - 2
        j = pos + 1
        while j <= limit:
            if high[j - 1] >= high[j] and low[j - 1] <= low[j]:
                j += 1
            else:
                break
        if low[pos] <= low[i] and low[pos] < low[j]:
            return low[pos]
    return 0.0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    Max1Buffer[rates_total - 1] = 0.0
    Min1Buffer[rates_total - 1] = 0.0
    Max2Buffer[rates_total - 1] = 0.0
    Min2Buffer[rates_total - 1] = 0.0
    Max3Buffer[rates_total - 1] = 0.0
    Min3Buffer[rates_total - 1] = 0.0
    Max1Buffer[rates_total - 2] = 0.0
    Min1Buffer[rates_total - 2] = 0.0
    Max2Buffer[rates_total - 2] = 0.0
    Min2Buffer[rates_total - 2] = 0.0
    Max3Buffer[rates_total - 2] = 0.0
    Min3Buffer[rates_total - 2] = 0.0
    for i in range(((prev_calculated - 2) if (prev_calculated >= 3) else 3), rates_total - 2):
        newmax = CheckShortMax(high, low, i)
        newmin = CheckShortMin(high, low, i)
        Max1Buffer[i] = newmax
        Min1Buffer[i] = newmin
        Max2Buffer[i] = 0.0
        Min2Buffer[i] = 0.0
        Max3Buffer[i] = 0.0
        Min3Buffer[i] = 0.0
        pos = 0
        lpos = 0
        poz = 0
        lpoz = 0
        if newmax != EMPTY_VALUE and newmax > 0:
            pos = MaxTemp1.checkMax(newmax)
            if pos and pos != i:
                Max2Buffer[pos] = Max1Buffer[pos]
                lpos = MaxTemp2.checkMax(Max2Buffer[pos])
                if lpos:
                    Max3Buffer[lpos] = Max2Buffer[lpos]
                MaxTemp2.push(Max2Buffer[pos], pos)
            MaxTemp1.push(newmax, i)
        if newmin != EMPTY_VALUE and newmin > 0:
            poz = MinTemp1.checkMin(newmin)
            if poz and poz != i:
                Min2Buffer[poz] = Min1Buffer[poz]
                lpoz = MinTemp2.checkMin(Min2Buffer[poz])
                if lpoz:
                    Min3Buffer[lpoz] = Min2Buffer[lpoz]
                MinTemp2.push(Min2Buffer[poz], poz)
            MinTemp1.push(newmin, i)
    return rates_total

# ---- global variables initialised from expressions
MaxTemp1 = _alloc(LastExtremums)
MaxTemp1.__init__()
MaxTemp2 = _alloc(LastExtremums)
MaxTemp2.__init__()
MinTemp1 = _alloc(LastExtremums)
MinTemp1.__init__()
MinTemp2 = _alloc(LastExtremums)
MinTemp2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LarrywilliamsMinmax(_MQL5Indicator):
    name = 'larrywilliams_minmax'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'IgnoreInsideBars': True,
    }

