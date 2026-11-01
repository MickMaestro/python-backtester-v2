"""PriceDensity_MT5 — converted from MQL5: MQL5 Indicators/Price Density - Market Noise Index/PriceDensity_MT5.mq5

Copyright: WH Trading; Link: https://www.mql5.com/en/users/linkt/seller; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'WH Trading', 'link': 'https://www.mql5.com/en/users/linkt/seller', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [36095]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [5.0], 'description': [], 'name': 'PriceDensity_MT5', 'source': 'MQL5 Indicators/Price Density - Market Noise Index/PriceDensity_MT5.mq5', 'folder': 'Price Density - Market Noise Index', 'inputs': [{'mql': 'InpPeriods', 'py': 'InpPeriods', 'param': 'InpPeriods', 'type': 'int', 'default': 20, 'label': 'Indicator Periods', 'sinput': False}, {'mql': 'InpNoiseThresholdLevel', 'py': 'InpNoiseThresholdLevel', 'param': 'InpNoiseThresholdLevel', 'type': 'double', 'default': 5.0, 'label': 'Price Density Noise Threshold Level', 'sinput': False}, {'mql': 'InpLineColor', 'py': 'InpLineColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Threshold Level Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriods = _input('InpPeriods', 20)  # Indicator Periods
InpNoiseThresholdLevel = _input('InpNoiseThresholdLevel', 5.0)  # Price Density Noise Threshold Level
InpLineColor = _input('InpLineColor', clrBlack)  # Threshold Level Color
PriceDensityBuffer = Arr(0, 0.0)
SumHighsLowsBuffer = Arr(0, 0.0)
HighestHighBuffer = Arr(0, 0.0)
LowestLowBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, PriceDensityBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SumHighsLowsBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, HighestHighBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, LowestLowBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 5)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Price Density - Market Noise Index (' + IntegerToString(InpPeriods) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpPeriods)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, InpNoiseThresholdLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, InpLineColor)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Threshold Level')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= InpPeriods:
        return 0
    currentPosition = prev_calculated - 1
    if currentPosition < InpPeriods:
        currentPosition = InpPeriods
    for i in range(currentPosition, rates_total):
        if rates_total != prev_calculated:
            SumHighsLowsBuffer[i] = 0.0
            HighestHighBuffer[i] = DBL_MIN
            LowestLowBuffer[i] = DBL_MAX
            for j in range(i - 1, i - InpPeriods, -1):
                SumHighsLowsBuffer[i] += high[j] - low[j]
                if high[j] > HighestHighBuffer[i]:
                    HighestHighBuffer[i] = high[j]
                if low[j] < LowestLowBuffer[i]:
                    LowestLowBuffer[i] = low[j]
        highestHigh = MathMax(HighestHighBuffer[i], high[i])
        lowestLow = MathMin(LowestLowBuffer[i], low[i])
        if (highestHigh - lowestLow) != 0:
            PriceDensityBuffer[i] = _fdiv(SumHighsLowsBuffer[i] + (high[i] - low[i]), highestHigh - lowestLow)
        else:
            PriceDensityBuffer[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceDensityMT5(_MQL5Indicator):
    name = 'PriceDensity_MT5'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriods': 20,  # Indicator Periods
        'InpNoiseThresholdLevel': 5.0,  # Price Density Noise Threshold Level
    }

