"""Rainbow — converted from MQL5: MQL5 Indicators/Rainbow indicator for mt5/Rainbow.mq5

Copyright: Müller Péter; Link: https://www.mql5.com/en/users/mullerp04/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Müller Péter', 'link': 'https://www.mql5.com/en/users/mullerp04/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [255], 2: [42495], 3: [65535], 4: [3329434], 5: [16775408], 6: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Rainbow', 'source': 'MQL5 Indicators/Rainbow indicator for mt5/Rainbow.mq5', 'folder': 'Rainbow indicator for mt5', 'inputs': [{'mql': 'AtrMultiplier', 'py': 'AtrMultiplier', 'param': 'AtrMultiplier', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
High = 0
Low = 0
Atr = 0
AtrMultiplier = _input('AtrMultiplier', 1.0)
period = _input('period', 20)
FirstBuffer = Arr(0, 0.0)
SecondBuffer = Arr(0, 0.0)
ThirdBuffer = Arr(0, 0.0)
FourthBuffer = Arr(0, 0.0)
FifthBuffer = Arr(0, 0.0)
SixthBuffer = Arr(0, 0.0)

def OnInit():
    global Atr, High, Low
    SetIndexBuffer(0, FirstBuffer)
    SetIndexBuffer(1, SecondBuffer)
    SetIndexBuffer(2, ThirdBuffer)
    SetIndexBuffer(3, FourthBuffer)
    SetIndexBuffer(4, FifthBuffer)
    SetIndexBuffer(5, SixthBuffer)
    short_name = 'Period( ' + IntegerToString(period) + ' )' + Symbol()
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 100)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 100)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, 100)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, 100)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, 100)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, 100)
    High = iMA(Symbol(), PERIOD_CURRENT, period, 0, MODE_SMA, PRICE_HIGH)
    Low = iMA(Symbol(), PERIOD_CURRENT, period, 0, MODE_SMA, PRICE_LOW)
    Atr = iATR(Symbol(), PERIOD_CURRENT, period)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(FirstBuffer, False)
    ArraySetAsSeries(SecondBuffer, False)
    ArraySetAsSeries(ThirdBuffer, False)
    ArraySetAsSeries(FourthBuffer, False)
    ArraySetAsSeries(FifthBuffer, False)
    ArraySetAsSeries(SixthBuffer, False)
    for i in range(prev_calculated, rates_total):
        HighMa = Arr(1, 0.0, dyn=False)
        LowMa = Arr(1, 0.0, dyn=False)
        currAtr = Arr(1, 0.0, dyn=False)
        CopyBuffer(High, 0, rates_total - i, 1, HighMa)
        CopyBuffer(Low, 0, rates_total - i, 1, LowMa)
        CopyBuffer(Atr, 0, rates_total - i, 1, currAtr)
        FirstBuffer[i] = HighMa[0] + (2 * AtrMultiplier * currAtr[0])
        SecondBuffer[i] = HighMa[0] + (AtrMultiplier * currAtr[0])
        ThirdBuffer[i] = HighMa[0]
        FourthBuffer[i] = LowMa[0]
        FifthBuffer[i] = LowMa[0] - (AtrMultiplier * currAtr[0])
        SixthBuffer[i] = LowMa[0] - (2 * AtrMultiplier * currAtr[0])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rainbow(_MQL5Indicator):
    name = 'Rainbow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AtrMultiplier': 1.0,
        'period': 20,
    }

