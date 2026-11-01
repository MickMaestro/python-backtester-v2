"""catfx50 — converted from MQL5: MQL5 Indicators/CatFX50/catfx50.mq5

CatFX50
Copyright: Copyright © 2011, Nikolay Kositsin; Link: http://www.forex-tsd.com/showthread.php?t=523; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'http://www.forex-tsd.com/showthread.php?t=523', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [14822282], 2: [16711680], 3: [16711935]}, 'widths': {1: 1, 2: 4, 3: 4}, 'styles': {1: 0}, 'labels': {1: 'CatFX50 EMA', 2: 'CatFX50 Buy', 3: 'CatFX50 Sell'}, 'levels': [], 'description': ['CatFX50'], 'name': 'catfx50', 'source': 'MQL5 Indicators/CatFX50/catfx50.mq5', 'folder': 'CatFX50', 'inputs': [{'mql': 'confirm_StepMA_Bars', 'py': 'confirm_StepMA_Bars', 'param': 'confirm_StepMA_Bars', 'type': 'int', 'default': 2, 'label': 'amount of bars for the signal confirmation', 'sinput': False}, {'mql': 'TradeTimeFrom', 'py': 'TradeTimeFrom', 'param': 'TradeTimeFrom', 'type': 'int', 'default': 0, 'label': 'trading start', 'sinput': False}, {'mql': 'TradeTimeTo', 'py': 'TradeTimeTo', 'param': 'TradeTimeTo', 'type': 'int', 'default': 22, 'label': 'trading end', 'sinput': False}, {'mql': 'alert_ON', 'py': 'alert_ON', 'param': 'alert_ON', 'type': 'bool', 'default': False, 'label': 'allow to put alert', 'sinput': False}, {'mql': 'Kfast', 'py': 'Kfast', 'param': 'Kfast', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Kslow', 'py': 'Kslow', 'param': 'Kslow', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'EMA_Period', 'py': 'EMA_Period', 'param': 'EMA_Period', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum HourCount
D00 = 0
D01 = 1
D02 = 2
D03 = 3
D04 = 4
D05 = 5
D06 = 6
D07 = 7
D08 = 8
D09 = 9
D10 = 10
D11 = 11
D12 = 12
D13 = 13
D14 = 14
D15 = 15
D16 = 16
D17 = 17
D18 = 18
D19 = 19
D21 = 20
D22 = 21
D23 = 22
_enum('HourCount', {0: 'D00', 1: 'D01', 2: 'D02', 3: 'D03', 4: 'D04', 5: 'D05', 6: 'D06', 7: 'D07', 8: 'D08', 9: 'D09', 10: 'D10', 11: 'D11', 12: 'D12', 13: 'D13', 14: 'D14', 15: 'D15', 16: 'D16', 17: 'D17', 18: 'D18', 19: 'D19', 20: 'D21', 21: 'D22', 22: 'D23'})

# ---- inputs and global variables
confirm_StepMA_Bars = _input('confirm_StepMA_Bars', 2)  # amount of bars for the signal confirmation
TradeTimeFrom = _input('TradeTimeFrom', D00)  # trading start
TradeTimeTo = _input('TradeTimeTo', D23)  # trading end
alert_ON = _input('alert_ON', False)  # allow to put alert
Kfast = _input('Kfast', 1.0)
Kslow = _input('Kslow', 1.0)
EMA_Period = _input('EMA_Period', 50)
EMABuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
EMA_Handle = 0
ATR_Handle = 0
StSt_Handle = 0

def OnInit():
    global ATR_Handle, EMA_Handle, StSt_Handle, min_rates_total
    ATR_Period = 5
    StSt_Period = 10
    min_rates_total = _int(MathMax(MathMax(ATR_Period, EMA_Period), StSt_Period) + confirm_StepMA_Bars + 5)
    EMA_Handle = iMA(None, 0, EMA_Period, 0, MODE_EMA, PRICE_MEDIAN)
    if EMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    StSt_Handle = iCustom(None, 0, 'StepSto_v1', Kfast, Kslow, 0)
    if StSt_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of StepSto_v1 indicator')
    SetIndexBuffer(0, EMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(EMABuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 119)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'CatFX50'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(StSt_Handle) < rates_total or BarsCalculated(EMA_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    ATR = Arr(0, 0.0)
    STSTM = Arr(0, 0.0)
    STSTS = Arr(0, 0.0)
    stepma00 = 0.0
    stepma01 = 0.0
    stepma10 = 0.0
    stepma11 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(STSTM, True)
    ArraySetAsSeries(STSTS, True)
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(EMA_Handle, 0, 0, to_copy, EMABuffer) <= 0:
        return 0
    if CopyBuffer(StSt_Handle, MAIN_LINE, 0, to_copy + confirm_StepMA_Bars + 1, STSTM) <= 0:
        return 0
    if CopyBuffer(StSt_Handle, SIGNAL_LINE, 0, to_copy + confirm_StepMA_Bars + 1, STSTS) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        if tm.hour >= TradeTimeFrom and tm.hour <= TradeTimeTo:
            if (open[bar + 1] < EMABuffer[bar + 1] and close[bar + 1] > EMABuffer[bar + 1]) and open[bar] > EMABuffer[bar]:
                for j in range(confirm_StepMA_Bars, 0 - 1, -1):
                    barj = bar + j
                    stepma00 = STSTM[barj]
                    stepma01 = STSTS[barj]
                    stepma10 = STSTM[barj + 1]
                    stepma11 = STSTS[barj + 1]
                    if stepma10 < stepma11 and stepma00 > stepma01:
                        BuyBuffer[bar] = low[bar] - (ATR[bar] / 2)
                        if (not bar) and alert_ON:
                            Alert(TimeToString(time[bar], TIME_MINUTES), ' CatFX50 ', Symbol(), ' BUY')
            if (open[bar + 1] > EMABuffer[bar + 1] and close[bar + 1] < EMABuffer[bar + 1]) and open[bar] < EMABuffer[bar]:
                for j in range(confirm_StepMA_Bars, 0 - 1, -1):
                    barj = bar + j
                    stepma00 = STSTM[barj]
                    stepma01 = STSTS[barj]
                    stepma10 = STSTM[barj + 1]
                    stepma11 = STSTS[barj + 1]
                    if stepma10 > stepma11 and stepma00 < stepma01:
                        SellBuffer[bar] = high[bar] + (ATR[bar] / 2)
                        if (not bar) and alert_ON:
                            Alert(TimeToString(time[bar], TIME_MINUTES), ' CatFX50 ', Symbol(), ' SELL')
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Catfx50(_MQL5Indicator):
    name = 'catfx50'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'confirm_StepMA_Bars': 2,  # amount of bars for the signal confirmation
        'TradeTimeFrom': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '21', 21: '22', 22: '23'}, default=0),  # trading start
        'TradeTimeTo': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '21', 21: '22', 22: '23'}, default=22),  # trading end
        'alert_ON': False,  # allow to put alert
        'Kfast': 1.0,
        'Kslow': 1.0,
        'EMA_Period': 50,
    }

