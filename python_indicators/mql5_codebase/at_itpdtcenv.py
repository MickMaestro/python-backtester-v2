"""at_itpdtcenv — converted from MQL5: MQL5 Indicators/at_Itp(t)Env/at_itpdtcenv.mq5

Redrawing curvelinear channel
Copyright: Copyright © 2011, ; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, ', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8388736], 2: [9639167], 3: [9639167]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'at_Itp(t)Env', 2: '+Envelope', 3: '-Envelope'}, 'levels': [], 'description': ['Redrawing curvelinear channel'], 'name': 'at_itpdtcenv', 'source': 'MQL5 Indicators/at_Itp(t)Env/at_itpdtcenv.mq5', 'folder': 'at_Itp(t)Env', 'inputs': [{'mql': 'hours', 'py': 'hours', 'param': 'hours', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 's', 'py': 's', 'param': 's', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'cb', 'py': 'cb', 'param': 'cb', 'type': 'uint', 'default': 500, 'label': 'Bars estimated number', 'sinput': False}, {'mql': 'Envelope_Shift', 'py': 'Envelope_Shift', 'param': 'Envelope_Shift', 'type': 'double', 'default': 0.2, 'label': 'Channel width', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
hours = _input('hours', 4)
s = _input('s', 10)
cb = _input('cb', 500)  # Bars estimated number
Envelope_Shift = _input('Envelope_Shift', 0.2)  # Channel width
IPC = _input('IPC', PRICE_CLOSE)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
min_rates_total = 0
pt = 0

def OnInit():
    global min_rates_total, pt
    pt = _int(_idiv(hours * 60 * 60, PeriodSeconds()))
    min_rates_total = _int(cb + (2 * pt)) + 1
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer0, True)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'at_Itp(t)Env')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    bar = 0
    x = 0
    m = 0
    aa = 0
    bb = 0
    cc = 0
    empty_rates = 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    empty_rates = rates_total - min_rates_total
    bar = 0
    for bar in range(bar, empty_rates + 1):
        ExtLineBuffer0[bar] = EMPTY_VALUE
        ExtLineBuffer1[bar] = EMPTY_VALUE
        ExtLineBuffer2[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, empty_rates + 1, 1)
    m = 0
    for m in range(m, _int(s) + 1):
        bar = 0
        while bar <= _int(cb):
            if not m:
                ExtLineBuffer0[cb + pt] = PriceSeries(IPC, cb + pt, open, low, high, close)
                ExtLineBuffer0[bar] = PriceSeries(IPC, bar, open, low, high, close)
                ExtLineBuffer0[cb + (2 * pt)] = PriceSeries(IPC, cb + (2 * pt), open, low, high, close)
            if m and m != s:
                ExtLineBuffer0[bar + pt] = 0.5 * (ExtLineBuffer0[bar] + ExtLineBuffer0[bar + (2 * pt)])
                ExtLineBuffer0[0] = 0.5 * (ExtLineBuffer0[0] + ExtLineBuffer0[pt])
                ExtLineBuffer0[cb + (2 * pt)] = 0.5 * (ExtLineBuffer0[cb + (2 * pt)] + ExtLineBuffer0[cb + pt])
            if m == s:
                aa = bar
                bb = bar + pt
                cc = bar + (2 * pt)
                x = bar
                for x in range(x, bar + pt - 1 + 1):
                    ExtLineBuffer0[x] = _fdiv(ExtLineBuffer0[aa] * ((x - bb) * (x - cc)), (aa - bb) * (aa - cc)) + _fdiv(ExtLineBuffer0[bb] * ((x - aa) * (x - cc)), (bb - aa) * (bb - cc)) + _fdiv(ExtLineBuffer0[cc] * ((x - aa) * (x - bb)), (cc - aa) * (cc - bb))
                else:
                    x = _range_end(x, bar + pt - 1 + 1, 1)
            bar += pt
    else:
        m = _range_end(m, _int(s) + 1, 1)
    bar = 0
    while bar <= _int(cb + pt):
        ExtLineBuffer1[bar] = ExtLineBuffer0[bar] * (1 + (Envelope_Shift / 100))
        ExtLineBuffer2[bar] = _fdiv(ExtLineBuffer0[bar], 1 + (Envelope_Shift / 100))
        bar += 1
    return rates_total

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
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AtItpdtcenv(_MQL5Indicator):
    name = 'at_itpdtcenv'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'hours': 4,
        's': 10,
        'cb': 500,  # Bars estimated number
        'Envelope_Shift': 0.2,  # Channel width
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

