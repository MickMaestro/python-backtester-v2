"""SRm_Cloud — converted from MQL5: MQL5 Indicators/SRm_Cloud/SRm_Cloud.mq5

Copyright: Copyright © 2013, HgCl2; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, HgCl2', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [15658671]}, 'widths': {}, 'styles': {}, 'labels': {1: 'SRm_Cloud'}, 'levels': [], 'description': [], 'name': 'SRm_Cloud', 'source': 'MQL5 Indicators/SRm_Cloud/SRm_Cloud.mq5', 'folder': 'SRm_Cloud', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'k_std', 'py': 'k_std', 'param': 'k_std', 'type': 'double', 'default': 1.0, 'label': 'Коэффициент стандартного отклонения Std', 'sinput': False}, {'mql': 'k', 'py': 'k', 'param': 'k', 'type': 'double', 'default': 1.0, 'label': 'Коэффициент среднего минимального колебания AV', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_'})

# ---- inputs and global variables
period = _input('period', 14)
k_std = _input('k_std', 1.0)  # Коэффициент стандартного отклонения Std
k = _input('k', 1.0)  # Коэффициент среднего минимального колебания AV
Price = _input('Price', PRICE_OPEN_)
m = Arr(10000, 0.0, dyn=False)
o = Arr(10000, 0.0, dyn=False)
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(period + 1)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SRm_Cloud(' + DoubleToString(k_std, 4) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_LastHigh, _s_OnCalculate_LastLow
    if rates_total < min_rates_total:
        return 0
    w = 0.0
    gsv1 = 0.0
    gsv2 = 0.0
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
        if tm0.day != tm1.day and ((tm1.day_of_week > 0 and tm1.day_of_week < 6) or Period() > PERIOD_D1):
            x += 1
            if Price == PRICE_OPEN_:
                o[x] = Open[bar]
            else:
                o[x] = Close[bar]
            m[x] = _s_OnCalculate_LastHigh - o[x - 1]
            if (_s_OnCalculate_LastHigh - o[x - 1]) > (o[x - 1] - _s_OnCalculate_LastLow):
                m[x] = o[x - 1] - _s_OnCalculate_LastLow
            _s_OnCalculate_LastLow = 100000.0
            _s_OnCalculate_LastHigh = 0.0
            if x > _int(period):
                w = 0.0
                for y in range(0, _int(period)):
                    w += m[x - y]
                v = w / period
                w = 0.0
                for y in range(0, _int(period)):
                    w += MathPow(m[x - y] - v, 2)
                e = w / period
                std = (k * v) + (k_std * MathPow(e, 0.5))
                gsv1 = o[x] + std
                gsv2 = o[x] - std
        if x > _int(period):
            ExtABuffer[bar] = gsv1
            ExtBBuffer[bar] = gsv2
    return rates_total

# ---- static local variables
_s_OnCalculate_LastHigh = 0.0
_s_OnCalculate_LastLow = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SRmCloud(_MQL5Indicator):
    name = 'SRm_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'period': 14,
        'k_std': 1.0,  # Коэффициент стандартного отклонения Std
        'k': 1.0,  # Коэффициент среднего минимального колебания AV
        'Price': _Choice({1: 'Close', 2: 'Open'}, default=2),
    }

