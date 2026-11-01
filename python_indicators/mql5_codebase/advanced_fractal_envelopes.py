"""Advanced_Fractal_Envelopes — converted from MQL5: MQL5 Indicators/Advanced_Fractal_Envelopes/Advanced_Fractal_Envelopes.mq5

Advanced Fractal Envelopes
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [255], 2: [16711680], 3: [3329330], 4: [255], 5: [3329330]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Top', 2: 'Central', 3: 'Bottom', 4: 'Fractal up', 5: 'Fractal down'}, 'levels': [], 'description': ['Advanced Fractal Envelopes'], 'name': 'Advanced_Fractal_Envelopes', 'source': 'MQL5 Indicators/Advanced_Fractal_Envelopes/Advanced_Fractal_Envelopes.mq5', 'folder': 'Advanced_Fractal_Envelopes', 'inputs': [{'mql': 'InpPeriodAVG', 'py': 'InpPeriodAVG', 'param': 'InpPeriodAVG', 'type': 'uint', 'default': 5, 'label': 'Average', 'sinput': False}, {'mql': 'InpShowCentral', 'py': 'InpShowCentral', 'param': 'InpShowCentral', 'type': 'int', 'default': 1, 'label': 'Show central line', 'sinput': False}, {'mql': 'InpShowFractals', 'py': 'InpShowFractals', 'param': 'InpShowFractals', 'type': 'int', 'default': 1, 'label': 'Show fractals', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodAVG = _input('InpPeriodAVG', 5)  # Average
InpShowCentral = _input('InpShowCentral', INPUT_YES)  # Show central line
InpShowFractals = _input('InpShowFractals', INPUT_YES)  # Show fractals
BufferTop = Arr(0, 0.0)
BufferCentral = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferFractUP = Arr(0, 0.0)
BufferFractDN = Arr(0, 0.0)
period_avg = 0
handle_fr = 0

def OnInit():
    global handle_fr, period_avg
    period_avg = (1 if (InpPeriodAVG < 1) else InpPeriodAVG)
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCentral, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferFractUP, INDICATOR_DATA)
    SetIndexBuffer(4, BufferFractDN, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Advanced Fractal Envelopes (' + _str(period_avg) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, (DRAW_SECTION if InpShowCentral else DRAW_NONE))
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, (DRAW_ARROW if InpShowFractals else DRAW_NONE))
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, (DRAW_ARROW if InpShowFractals else DRAW_NONE))
    PlotIndexSetInteger(3, PLOT_ARROW, 217)
    PlotIndexSetInteger(4, PLOT_ARROW, 218)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferCentral, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferFractUP, True)
    ArraySetAsSeries(BufferFractDN, True)
    ResetLastError()
    handle_fr = iFractals(None, PERIOD_CURRENT)
    if handle_fr == INVALID_HANDLE:
        Print('The iFractals object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_avg, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_avg - 2
        ArrayInitialize(BufferTop, 0)
        ArrayInitialize(BufferCentral, 0)
        ArrayInitialize(BufferBottom, 0)
        ArrayInitialize(BufferFractUP, 0)
        ArrayInitialize(BufferFractDN, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fr, UPPER_LINE, 0, count, BufferFractUP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_fr, LOWER_LINE, 0, count, BufferFractDN)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        average = 0.0
        fractal = BufferFractUP[i]
        k = 1
        total = 1
        if fractal > 0 and fractal < EMPTY_VALUE:
            average = fractal
            while total < period_avg and (i + k) < (rates_total - 2):
                if BufferFractUP[i + k] > 0 and BufferFractUP[i + k] < EMPTY_VALUE:
                    average += BufferFractUP[i + k]
                    total += 1
                k += 1
            BufferTop[i] = _fdiv(average, period_avg)
            m = 1
            next_ = WRONG_VALUE
            while next_ == WRONG_VALUE and (i - m) > WRONG_VALUE:
                if (i - m) <= 0:
                    next_ = 0
                    break
                else:
                    if BufferFractUP[i - m] > 0 and BufferFractUP[i - m] < EMPTY_VALUE:
                        next_ = i - m
                m += 1
            j = i
            while j >= next_ and j >= 0:
                BufferTop[j] = BufferTop[i]
                j -= 1
    for i in range(limit, 0 - 1, -1):
        average = 0.0
        fractal = BufferFractDN[i]
        k = 1
        total = 1
        if fractal > 0 and fractal < EMPTY_VALUE:
            average = fractal
            while total < period_avg and (i + k) < (rates_total - 2):
                if BufferFractDN[i + k] > 0 and BufferFractDN[i + k] < EMPTY_VALUE:
                    average += BufferFractDN[i + k]
                    total += 1
                k += 1
            BufferBottom[i] = _fdiv(average, period_avg)
            m = 1
            next_ = WRONG_VALUE
            while next_ == WRONG_VALUE and (i - m) > WRONG_VALUE:
                if (i - m) <= 0:
                    next_ = 0
                    break
                else:
                    if BufferFractDN[i - m] > 0 and BufferFractDN[i - m] < EMPTY_VALUE:
                        next_ = i - m
                m += 1
            j = i
            while j >= next_ and j >= 0:
                BufferBottom[j] = BufferBottom[i]
                j -= 1
        BufferCentral[i] = (BufferTop[i] + BufferBottom[i]) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdvancedFractalEnvelopes(_MQL5Indicator):
    name = 'Advanced_Fractal_Envelopes'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodAVG': 5,  # Average
        'InpShowCentral': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show central line
        'InpShowFractals': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show fractals
    }

