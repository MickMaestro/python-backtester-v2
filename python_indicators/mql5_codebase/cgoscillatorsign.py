"""cgoscillatorsign — converted from MQL5: MQL5 Indicators/CGOscillatorSign/cgoscillatorsign.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'CGOscillator Sell', 2: 'CGOscillator Buy'}, 'levels': [], 'description': [], 'name': 'cgoscillatorsign', 'source': 'MQL5 Indicators/CGOscillatorSign/cgoscillatorsign.mq5', 'folder': 'CGOscillatorSign', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 10)  # Период индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
CGshift = 0.0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, CGshift, min_rates_total
    min_rates_total = Length
    ATR_Period = 10
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    CGshift = (Length + 1.0) / 2.0
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 172)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 172)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'CGOscillatorSign(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_CG1, _s_OnCalculate_Trigger1
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    Num = 0.0
    Denom = 0.0
    CG = 0.0
    Trigger = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Num = 0.0
        Denom = 0.0
        for count in range(0, Length):
            price = (high[bar - count] + low[bar - count]) / 2.0
            Num += (1.0 + count) * price
            Denom += price
        if Denom != 0.0:
            CG = _fdiv(-Num, Denom) + CGshift
        else:
            CG = 0.0
        Trigger = _s_OnCalculate_CG1
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_CG1 < _s_OnCalculate_Trigger1 and CG > Trigger:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_CG1 > _s_OnCalculate_Trigger1 and CG < Trigger:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            _s_OnCalculate_CG1 = CG
            _s_OnCalculate_Trigger1 = Trigger
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_CG1 = 0.0
_s_OnCalculate_Trigger1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Cgoscillatorsign(_MQL5Indicator):
    name = 'cgoscillatorsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Период индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

