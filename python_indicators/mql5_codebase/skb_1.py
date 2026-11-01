"""skb-1 — converted from MQL5: MQL5 Indicators/SKB-1/skb-1.mq5

Copyright: Copyright © 2005, Kara Software Corp.; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Kara Software Corp.', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16436871]}, 'widths': {}, 'styles': {}, 'labels': {1: 'SKB-1'}, 'levels': [], 'description': [], 'name': 'skb-1', 'source': 'MQL5 Indicators/SKB-1/skb-1.mq5', 'folder': 'SKB-1', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
FRA_Handle = 0

def OnInit():
    global FRA_Handle, min_rates_total
    min_rates_total = 7
    FRA_Handle = iFractals(Symbol(), PERIOD_CURRENT)
    if FRA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iFractals indicator')
        return INIT_FAILED
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SKB-1')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(FRA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    CCU1 = 0
    CCU2 = 0
    CCL1 = 0
    CCL2 = 0
    i = 0
    j = 0
    UpFractal = Arr(1, 0.0, dyn=False)
    DnFractal = Arr(1, 0.0, dyn=False)
    FU = 0.0
    FL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        if CopyBuffer(FRA_Handle, 0, bar + 3, 1, UpFractal) <= 0:
            return 0
        if CopyBuffer(FRA_Handle, 1, bar + 3, 1, DnFractal) <= 0:
            return 0
        FU = UpFractal[0]
        FL = DnFractal[0]
        if FU and FU != EMPTY_VALUE:
            i = bar + 3 + 1
            if CopyBuffer(FRA_Handle, 0, i, 1, UpFractal) <= 0:
                return 0
            while (not UpFractal[0]) or UpFractal[0] == EMPTY_VALUE:
                i += 1
                if i == (rates_total - 1):
                    break
                if CopyBuffer(FRA_Handle, 0, i, 1, UpFractal) <= 0:
                    return 0
            j = bar + 3
            for j in range(j, i + 1):
                if CopyBuffer(FRA_Handle, 1, j, 1, DnFractal) <= 0:
                    return 0
                if DnFractal[0] and DnFractal[0] != EMPTY_VALUE:
                    CCU1 = bar + 3
                    CCU2 = i
                    if not CCL1:
                        CCL1 = j
                    elif Low[j] < Low[CCL1]:
                        CCL1 = j
                    CCL2 = 0
            else:
                j = _range_end(j, i + 1, 1)
            if j == i and High[i] > High[bar + 3]:
                FU = 0.0
        if FL and FL != EMPTY_VALUE:
            i = bar + 3 + 1
            if CopyBuffer(FRA_Handle, 1, i, 1, DnFractal) <= 0:
                return 0
            while (not DnFractal[0]) or DnFractal[0] == EMPTY_VALUE:
                i += 1
                if i == (rates_total - 1):
                    break
                if CopyBuffer(FRA_Handle, 1, i, 1, DnFractal) <= 0:
                    return 0
            j = bar + 3
            for j in range(j, i + 1):
                if CopyBuffer(FRA_Handle, 0, j, 1, UpFractal) <= 0:
                    return 0
                if UpFractal[0] and UpFractal[0] != EMPTY_VALUE:
                    if not CCU1:
                        CCU1 = j
                    elif High[j] > High[CCU1]:
                        CCU1 = j
                    CCU2 = 0
                    CCL1 = bar + 3
                    CCL2 = i
            else:
                j = _range_end(j, i + 1, 1)
        CCU1 = MathMin(CCU1, rates_total - 1)
        CCU2 = MathMin(CCU2, rates_total - 1)
        CCL1 = MathMin(CCL1, rates_total - 1)
        CCL2 = MathMin(CCL2, rates_total - 1)
        if CCU1 > 0 and CCU2 > 0:
            if High[CCU1] > High[CCU2]:
                ExtABuffer[bar] = High[CCU1] + (_fdiv(High[CCU1] - High[CCU2], CCU2 - CCU1) * (CCU1 - bar))
                ExtBBuffer[bar] = Low[CCL1] + (_fdiv(High[CCU1] - High[CCU2], CCU2 - CCU1) * (CCL1 - bar))
            if High[CCU1] < High[CCU2]:
                ExtABuffer[bar] = High[CCU1] - (_fdiv(High[CCU2] - High[CCU1], CCU2 - CCU1) * (CCU1 - bar))
                ExtBBuffer[bar] = Low[CCL1] - (_fdiv(High[CCU2] - High[CCU1], CCU2 - CCU1) * (CCL1 - bar))
        if CCL1 > 0 and CCL2 > 0:
            if Low[CCL1] < Low[CCL2]:
                ExtABuffer[bar] = High[CCU1] - (_fdiv(Low[CCL2] - Low[CCL1], CCL2 - CCL1) * (CCU1 - bar))
                ExtBBuffer[bar] = Low[CCL1] - (_fdiv(Low[CCL2] - Low[CCL1], CCL2 - CCL1) * (CCL1 - bar))
            if Low[CCL1] > Low[CCL2]:
                ExtABuffer[bar] = High[CCU1] + (_fdiv(Low[CCL1] - Low[CCL2], CCL2 - CCL1) * (CCU1 - bar))
                ExtBBuffer[bar] = Low[CCL1] + (_fdiv(Low[CCL1] - Low[CCL2], CCL2 - CCL1) * (CCL1 - bar))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Skb1(_MQL5Indicator):
    name = 'skb-1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

