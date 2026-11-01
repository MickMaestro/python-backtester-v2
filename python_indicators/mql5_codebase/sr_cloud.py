"""SR_Cloud — converted from MQL5: MQL5 Indicators/SR_Cloud/SR_Cloud.mq5

Copyright: Copyright © 2013, HgCl2; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, HgCl2', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [9234160]}, 'widths': {}, 'styles': {}, 'labels': {1: 'SR_Cloud'}, 'levels': [], 'description': [], 'name': 'SR_Cloud', 'source': 'MQL5 Indicators/SR_Cloud/SR_Cloud.mq5', 'folder': 'SR_Cloud', 'inputs': [{'mql': 'k_std', 'py': 'k_std', 'param': 'k_std', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_'})

# ---- inputs and global variables
k_std = _input('k_std', 1.0)
Price = _input('Price', PRICE_OPEN_)
m = Arr(10000, 0.0, dyn=False)
o = Arr(10000, 0.0, dyn=False)
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SR_Cloud(' + DoubleToString(k_std, 4) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_LastHigh, _s_OnCalculate_LastLow
    if rates_total < min_rates_total:
        return 0
    g1 = 0.0
    g2 = 0.0
    limit = 0
    x = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        for bar in range(rates_total - 1, 0 - 1, -1):
            ExtABuffer[bar] = 0.0
            ExtBBuffer[bar] = 0.0
        _s_OnCalculate_LastHigh = 0.0
        _s_OnCalculate_LastLow = 999999999.0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    if Price == PRICE_OPEN_:
        ArraySetAsSeries(Open, True)
    else:
        ArraySetAsSeries(Close, True)
    for bar in range(limit, 0 - 1, -1):
        _s_OnCalculate_LastHigh = MathMax(_s_OnCalculate_LastHigh, High[bar + 1])
        _s_OnCalculate_LastLow = MathMin(_s_OnCalculate_LastLow, Low[bar + 1])
        tm0 = MqlDateTime()
        tm1 = MqlDateTime()
        TimeToStruct(Time[bar], tm0)
        TimeToStruct(Time[bar + 1], tm1)
        if tm0.day != tm1.day:
            x += 1
            if Price == PRICE_OPEN_:
                o[x] = Open[bar]
            else:
                o[x] = Close[bar]
            m[x] = _s_OnCalculate_LastHigh - o[x - 1]
            if (_s_OnCalculate_LastHigh - o[x - 1]) > (o[x - 1] - _s_OnCalculate_LastLow):
                m[x] = o[x - 1] - _s_OnCalculate_LastLow
            _s_OnCalculate_LastLow = 999999999.0
            _s_OnCalculate_LastHigh = 0.0
            if x > 15:
                a1 = m[x]
                a2 = m[x - 1]
                a3 = m[x - 2]
                a4 = m[x - 3]
                a5 = m[x - 4]
                a6 = m[x - 5]
                a7 = m[x - 6]
                a8 = m[x - 7]
                a9 = m[x - 8]
                a10 = m[x - 9]
                a11 = m[x - 10]
                a12 = m[x - 11]
                a13 = m[x - 12]
                a14 = m[x - 13]
                ax = 0.1111111 * (a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9)
                ay = 0.0714285 * (a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9 + a10 + a11 + a12 + a13 + a14)
                stx = 0.1111111 * (((a1 - ax) * (a1 - ax)) + ((a2 - ax) * (a2 - ax)) + ((a3 - ax) * (a3 - ax)) + ((a4 - ax) * (a4 - ax)) + ((a5 - ax) * (a5 - ax)) + ((a6 - ax) * (a6 - ax)) + ((a7 - ax) * (a7 - ax)) + ((a8 - ax) * (a8 - ax)) + ((a9 - ax) * (a9 - ax)))
                sty = 0.0714285 * (((a1 - ay) * (a1 - ay)) + ((a2 - ay) * (a2 - ay)) + ((a3 - ay) * (a3 - ay)) + ((a4 - ay) * (a4 - ay)) + ((a5 - ay) * (a5 - ay)) + ((a6 - ay) * (a6 - ay)) + ((a7 - ay) * (a7 - ay)) + ((a8 - ay) * (a8 - ay)) + ((a9 - ay) * (a9 - ay)) + ((a10 - ay) * (a10 - ay)) + ((a11 - ay) * (a11 - ay)) + ((a12 - ay) * (a12 - ay)) + ((a13 - ay) * (a13 - ay)) + ((a14 - ay) * (a14 - ay)))
                st1 = ax + (k_std * MathPow(stx, 0.5))
                st2 = ay + (k_std * MathPow(sty, 0.5))
                std = st2
                if st1 > st2:
                    std = st1
                g1 = o[x] + std
                g2 = o[x] - std
        if x > 15:
            ExtABuffer[bar] = g1
            ExtBBuffer[bar] = g2
    return rates_total

# ---- static local variables
_s_OnCalculate_LastHigh = 0.0
_s_OnCalculate_LastLow = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SRCloud(_MQL5Indicator):
    name = 'SR_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'k_std': 1.0,
        'Price': _Choice({1: 'Close', 2: 'Open'}, default=2),
    }

