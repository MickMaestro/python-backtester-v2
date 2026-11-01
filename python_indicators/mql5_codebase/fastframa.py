"""fastframa — converted from MQL5: MQL5 Indicators/Fast FrAMA/fastframa.mq5

FasrFrAMA
Copyright: Copyright 2013, Roman Pritulyak; Link: c1664@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Roman Pritulyak', 'link': 'c1664@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'FasrFrAMA'}, 'levels': [], 'description': ['FasrFrAMA'], 'name': 'fastframa', 'source': 'MQL5 Indicators/Fast FrAMA/fastframa.mq5', 'folder': 'Fast FrAMA', 'inputs': [{'mql': 'Inp_period', 'py': 'Inp_period', 'param': 'Inp_period', 'type': 'int', 'default': 7, 'label': 'Period', 'sinput': False}, {'mql': 'Inp_shift', 'py': 'Inp_shift', 'param': 'Inp_shift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'Inp_price', 'py': 'Inp_price', 'param': 'Inp_price', 'type': 'int', 'default': 2, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_JPRICE
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('ENUM_JPRICE', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Inp_period = _input('Inp_period', 7)  # Period
Inp_shift = _input('Inp_shift', 0)  # Shift
Inp_price = _input('Inp_price', PRICE_OPEN_)  # Applied price
b_FrAMA = Arr(0, 0.0)
first = False
limit1 = 0
FRAMA = None

class CFRAMA(MqlObject):
    _q_fields = ('m_min_near', 'm_max_near', 'm_min_far', 'm_max_far', 'm_min_all', 'm_max_all')
    def __init__(self, *args):
        self.m_min_near = 0.0
        self.m_max_near = 0.0
        self.m_min_far = 0.0
        self.m_max_far = 0.0
        self.m_min_all = 0.0
        self.m_max_all = 0.0
    def FRAMASeries(self, begin, prev_calculated, rates_total, period, price, low, high, bar):
        global _s_CFRAMA_FRAMASeries_ALFA, _s_CFRAMA_FRAMASeries_bar_prev, _s_CFRAMA_FRAMASeries_frama, _s_CFRAMA_FRAMASeries_frama_prev
        period = Box(period)
        if _int(rates_total) < (2 * period.v) or begin >= (rates_total - 1):
            return EMPTY_VALUE
        if bar < begin:
            return EMPTY_VALUE
        if _int(bar) < (2 * period.v):
            return price
        if _s_CFRAMA_FRAMASeries_frama_prev == EMPTY_VALUE:
            self.m_min_near = self.LOWEST(bar, period.v, low)
            self.m_max_near = self.HIGHEST(bar, period.v, high)
            self.m_min_far = self.LOWEST(bar - period.v, period.v, low)
            self.m_max_far = self.HIGHEST(bar - period.v, period.v, high)
            self.m_min_all = MathMin(self.m_min_near, self.m_min_far)
            self.m_max_all = MathMax(self.m_max_near, self.m_max_far)
            _s_CFRAMA_FRAMASeries_frama = price
            _s_CFRAMA_FRAMASeries_frama_prev = _s_CFRAMA_FRAMASeries_frama
            _s_CFRAMA_FRAMASeries_bar_prev = bar
            return price
        if _s_CFRAMA_FRAMASeries_bar_prev < bar:
            if low[bar - period.v] == self.m_min_near:
                self.m_min_near = self.LOWEST(bar, period.v, low)
            if high[bar - period.v] == self.m_max_near:
                self.m_max_near = self.HIGHEST(bar, period.v, high)
            if low[bar - period.v] < self.m_min_far:
                self.m_min_far = low[bar - period.v]
            elif low[bar - (2 * period.v)] == self.m_min_far:
                self.m_min_far = self.LOWEST(bar - period.v, period.v, low)
            if high[bar - period.v] > self.m_max_far:
                self.m_max_far = high[bar - period.v]
            elif high[bar - (2 * period.v)] == self.m_max_far:
                self.m_max_far = self.HIGHEST(bar - period.v, period.v, high)
            self.m_min_all = MathMin(self.m_min_near, self.m_min_far)
            self.m_max_all = MathMax(self.m_max_near, self.m_max_far)
            _s_CFRAMA_FRAMASeries_ALFA = self.ALFA_CALC(period)
            _s_CFRAMA_FRAMASeries_frama_prev = _s_CFRAMA_FRAMASeries_frama
            _s_CFRAMA_FRAMASeries_bar_prev = bar
        if low[bar] < self.m_min_near:
            self.m_min_near = low[bar]
            self.m_min_all = MathMin(self.m_min_near, self.m_min_far)
            _s_CFRAMA_FRAMASeries_ALFA = self.ALFA_CALC(period)
        if high[bar] > self.m_max_near:
            self.m_max_near = high[bar]
            self.m_max_all = MathMax(self.m_max_near, self.m_max_far)
            _s_CFRAMA_FRAMASeries_ALFA = self.ALFA_CALC(period)
        _s_CFRAMA_FRAMASeries_frama = (_s_CFRAMA_FRAMASeries_ALFA * price) + ((1 - _s_CFRAMA_FRAMASeries_ALFA) * _s_CFRAMA_FRAMASeries_frama_prev)
        return _s_CFRAMA_FRAMASeries_frama
    def LOWEST(self, StartPos, Depth, low):
        res = low[StartPos]
        for i in range(StartPos - Depth + 1, StartPos):
            if low[i] < res:
                res = low[i]
        return res
    def HIGHEST(self, StartPos, Depth, high):
        res = high[StartPos]
        for i in range(StartPos - Depth + 1, StartPos):
            if high[i] > res:
                res = high[i]
        return res
    def ALFA_CALC(self, period):
        N1 = 0.0
        N2 = 0.0
        N3 = 0.0
        D = 0.0
        N1 = _fdiv(self.m_max_near - self.m_min_near, period.v)
        N2 = _fdiv(self.m_max_far - self.m_min_far, period.v)
        N3 = _fdiv(self.m_max_all - self.m_min_all, 2 * period.v)
        D = _fdiv(MathLog(N1 + N2) - MathLog(N3), MathLog(2.0))
        return MathExp(-4.6 * (D - 1.0))

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    elif _sw1 == 13:
        return ((Close[bar] * 5) + (Open[bar] * 2) + High[bar] + Low[bar]) / 9
    else:
        return Close[bar]

def OnInit():
    global first, limit1
    if Inp_period < 2 or Inp_shift < 0:
        Print('Error: invalid inputs')
        return INIT_FAILED
    SetIndexBuffer(0, b_FrAMA, INDICATOR_DATA)
    first = True
    limit1 = (2 * Inp_period) + 1
    PlotIndexSetInteger(0, PLOT_SHIFT, Inp_shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, limit1)
    PlotIndexSetString(0, PLOT_LABEL, 'FastFrAMA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global FRAMA, first
    i = 0
    from_ = 0
    price = 0.0
    if first:
        FRAMA = CFRAMA()
        first = False
    from_ = prev_calculated - 1
    if from_ < limit1:
        from_ = limit1
    i = from_
    for i in range(i, rates_total):
        price = PriceSeries(Inp_price, i, open, low, high, close)
        if CheckPointer(FRAMA) != POINTER_INVALID:
            b_FrAMA[i] = FRAMA.FRAMASeries(limit1, prev_calculated, rates_total, Inp_period, price, low, high, i)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def OnDeinit(reason):
    _delete(FRAMA)

# ---- static local variables
_s_CFRAMA_FRAMASeries_bar_prev = 0
_s_CFRAMA_FRAMASeries_ALFA = 0.0
_s_CFRAMA_FRAMASeries_frama = 0.0
_s_CFRAMA_FRAMASeries_frama_prev = EMPTY_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fastframa(_MQL5Indicator):
    name = 'fastframa'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_period': 7,  # Period
        'Inp_shift': 0,  # Shift
        'Inp_price': _Choice({1: 'CLOSE', 2: 'OPEN', 3: 'HIGH', 4: 'LOW', 5: 'MEDIAN', 6: 'TYPICAL', 7: 'WEIGHTED', 8: 'SIMPLE', 9: 'QUARTER', 10: 'TRENDFOLLOW', 11: 'HALFTRENDFOLLOW'}, default=2),  # Applied price
    }

