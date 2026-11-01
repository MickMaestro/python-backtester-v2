"""cmybuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class CMyBuffer(MqlObject):
    _q_fields = ('mColor', 'mParam', 'mParam1', 'mParam2', 'mhandle', 'mbuffer')
    def __init__(self):
        self.mColor = 0
        self.mParam = 0
        self.mParam1 = 0
        self.mParam2 = 0
        self.mhandle = 0
        self.mbuffer = Arr(0, 0.0)
    def _q_dtor(self):
        pass
    def Init(self):
        pass
    def Deinit(self):
        ArrayFree(self.mbuffer)
    def mArraySetAsSeries(self, set_):
        return ArraySetAsSeries(self.mbuffer, set_)
    def mSetIndexBuffer(self, index, data_type=INDICATOR_DATA):
        return SetIndexBuffer(index, self.mbuffer, data_type)
    def mPlotIndexSetInteger(self, plot_index, prop_id=PLOT_DRAW_TYPE, prop_value=DRAW_LINE):
        return PlotIndexSetInteger(plot_index, prop_id, prop_value)
    def mPlotIndexSetDouble(self, plot_index, prop_id=PLOT_EMPTY_VALUE, prop_value=0.0):
        return PlotIndexSetDouble(plot_index, prop_id, prop_value)
    def mPlotIndexSetString(self, plot_index, prop_id=PLOT_LABEL, prop_value=''):
        return PlotIndexSetString(plot_index, prop_id, prop_value)
    def mCopyBuffer(self, prev_calculated, total):
        return CopyBuffer(self.mhandle, 0, 0, total - prev_calculated + 1, self.mbuffer)

__all__ = ['CMyBuffer']
