"""AFStar — converted from MQL5: MQL5 Indicators/AFStar/AFStar.mq5

Copyright: Copyright © 2005, Forex-Experts; Link: http://www.forex-experts.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Forex-Experts', 'link': 'http://www.forex-experts.com', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [42495], 2: [16711680]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'AFStar Sell', 2: 'AFStar Buy'}, 'levels': [], 'description': [], 'name': 'AFStar', 'source': 'MQL5 Indicators/AFStar/AFStar.mq5', 'folder': 'AFStar', 'inputs': [{'mql': 'StartFast', 'py': 'StartFast', 'param': 'StartFast', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'EndFast', 'py': 'EndFast', 'param': 'EndFast', 'type': 'double', 'default': 3.5, 'label': '', 'sinput': False}, {'mql': 'StartSlow', 'py': 'StartSlow', 'param': 'StartSlow', 'type': 'double', 'default': 8.0, 'label': '', 'sinput': False}, {'mql': 'EndSlow', 'py': 'EndSlow', 'param': 'EndSlow', 'type': 'double', 'default': 9.0, 'label': '', 'sinput': False}, {'mql': 'StepPeriod', 'py': 'StepPeriod', 'param': 'StepPeriod', 'type': 'double', 'default': 0.2, 'label': '', 'sinput': False}, {'mql': 'StartRisk', 'py': 'StartRisk', 'param': 'StartRisk', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'EndRisk', 'py': 'EndRisk', 'param': 'EndRisk', 'type': 'double', 'default': 2.8, 'label': '', 'sinput': False}, {'mql': 'StepRisk', 'py': 'StepRisk', 'param': 'StepRisk', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StartFast = _input('StartFast', 3.0)
EndFast = _input('EndFast', 3.5)
StartSlow = _input('StartSlow', 8.0)
EndSlow = _input('EndSlow', 9.0)
StepPeriod = _input('StepPeriod', 0.2)
StartRisk = _input('StartRisk', 1.0)
EndRisk = _input('EndRisk', 2.8)
StepRisk = _input('StepRisk', 0.5)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
Table_value2 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 12
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    SetIndexBuffer(2, Table_value2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Table_value2, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'AFStar'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Buy1_prev, _s_OnCalculate_Buy2_prev, _s_OnCalculate_Sell1_prev, _s_OnCalculate_Sell2_prev
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    Buy = 0.0
    Sell = 0.0
    RiskCnt = 0.0
    Counter = 0
    i1 = 0
    value10 = 0.0
    value11 = 0.0
    Sell1 = 0
    Buy1 = 0
    Sell2 = 0.0
    Buy2 = 0.0
    EndScan1 = 0
    EndScan2 = 0
    x1 = 0.0
    x2 = 0.0
    FastCnt = 0.0
    SlowCnt = 0.0
    value2 = 0.0
    value3 = 0.0
    FastPer = 0.0
    SlowPer = 0.0
    TrueCount = 0.0
    Range = 0.0
    AvgRange = 0.0
    MRO1 = 0.0
    MRO2 = 0.0
    iMaSlowPrevious = 0.0
    iMaSlowCurrent = 0.0
    iMaFastPrevious = 0.0
    iMaFastCurrent = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        bar = rates_total - 1
        for bar in range(bar, 0 - 1, -1):
            Table_value2[bar] = 0.0
        else:
            bar = _range_end(bar, 0 - 1, -1)
        _s_OnCalculate_Sell1_prev = 0
        _s_OnCalculate_Buy1_prev = 0
        _s_OnCalculate_Sell2_prev = 0.0
        _s_OnCalculate_Buy2_prev = 999999999.0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Table_value2[bar] = 0.0
        Sell1 = 0
        Buy1 = 0
        EndScan1 = 0
        SlowCnt = StartSlow
        while SlowCnt <= EndSlow:
            if EndScan1 == 1:
                break
            FastCnt = StartFast
            while FastCnt <= EndFast:
                if EndScan1 == 1:
                    break
                SlowPer = _fdiv(2.0, SlowCnt + 1.0)
                FastPer = _fdiv(2.0, FastCnt + 1.0)
                iMaSlowCurrent = (close[bar] * SlowPer) + (close[bar + 1] * (1 - SlowPer))
                iMaSlowPrevious = (close[bar + 1] * SlowPer) + (close[bar + 2] * (1 - SlowPer))
                iMaFastCurrent = (close[bar] * FastPer) + (close[bar + 1] * (1 - FastPer))
                iMaFastPrevious = (close[bar + 1] * FastPer) + (close[bar + 2] * (1 - FastPer))
                if iMaFastPrevious < iMaSlowPrevious and iMaFastCurrent > iMaSlowCurrent:
                    EndScan1 = 1
                    Buy1 = 1
                if iMaFastPrevious > iMaSlowPrevious and iMaFastCurrent < iMaSlowCurrent:
                    EndScan1 = 1
                    Sell1 = 1
                FastCnt += StepPeriod
            SlowCnt += StepPeriod
        EndScan2 = 0
        Sell2 = 0.0
        Buy2 = 0.0
        RiskCnt = StartRisk
        if RiskCnt <= EndRisk:
            if EndScan2 != 1:
                value10 = 3 + (RiskCnt * 2)
                x1 = 67 + RiskCnt
                x2 = 33 - RiskCnt
                value11 = value10
                Range = 0.0
                AvgRange = 0.0
                Counter = bar + 9
                for Counter in range(Counter, bar - 1, -1):
                    AvgRange += MathAbs(high[Counter] - low[Counter])
                else:
                    Counter = _range_end(Counter, bar - 1, -1)
                Range = AvgRange / 10
                Counter = bar
                TrueCount = 0.0
                while Counter < (bar + 9) and TrueCount < 1:
                    if MathAbs(open[Counter] - close[Counter + 1]) >= (Range * 2.0):
                        TrueCount += 1
                    Counter += 1
                if TrueCount >= 1:
                    MRO1 = Counter
                else:
                    MRO1 = -1.0
                Counter = bar
                TrueCount = 0.0
                while Counter < (bar + 6) and TrueCount < 1:
                    if MathAbs(close[Counter + 3] - close[Counter]) >= (Range * 4.6):
                        TrueCount += 1
                    Counter += 1
                if TrueCount >= 1:
                    MRO2 = Counter
                else:
                    MRO2 = -1.0
                if MRO1 > -1:
                    value11 = 3.0
                else:
                    value11 = value10
                if MRO2 > -1:
                    value11 = 4.0
                else:
                    value11 = value10
                value2 = 100 - MathAbs(GetWPR(_int(value11), bar, high, low, close))
                Table_value2[bar] = value2
                value3 = 0.0
                if value2 < x2:
                    i1 = 1
                    while Table_value2[bar + i1] >= x2 and Table_value2[bar + i1] <= x1:
                        i1 += 1
                    if Table_value2[bar + i1] > x1:
                        value3 = high[bar] + (Range * 0.5)
                        Sell2 = value3
                if value2 > x1:
                    i1 = 1
                    while Table_value2[bar + i1] >= x2 and Table_value2[bar + i1] <= x1:
                        i1 += 1
                    if Table_value2[bar + i1] < x2:
                        value3 = low[bar] - (Range * 0.5)
                        Buy2 = value3
            if Buy2 > 0 or Sell2 > 0:
                EndScan2 = 1
            RiskCnt += StepRisk
        Buy = 0.0
        Sell = 0.0
        if ((Buy1 > 0 and Buy2 > 0) or (Buy1 > 0 and _s_OnCalculate_Buy2_prev > 0)) or (_s_OnCalculate_Buy1_prev > 0 and Buy2 > 0):
            Buy = low[bar] - (0.3 * Range)
        if ((Sell1 > 0 and Sell2 > 0) or (Sell1 > 0 and _s_OnCalculate_Sell2_prev > 0)) or (_s_OnCalculate_Sell1_prev > 0 and Sell2 > 0):
            Sell = high[bar] + (0.3 * Range)
        if Buy and Sell:
            Buy = 0.0
            Sell = 0.0
        BuyBuffer[bar] = Buy
        SellBuffer[bar] = Sell
        if bar:
            _s_OnCalculate_Sell1_prev = Sell1
            _s_OnCalculate_Buy1_prev = Buy1
            _s_OnCalculate_Sell2_prev = Sell2
            _s_OnCalculate_Buy2_prev = Buy2
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def GetWPR(period, index, High, Low, Close):
    global _s_GetWPR_WPR_prev
    WPR = -50.0
    dMaxHigh = High[ArrayMaximum(High, index, period)]
    dMinLow = Low[ArrayMinimum(Low, index, period)]
    res = dMaxHigh - dMinLow
    if res:
        WPR = _fdiv((-(dMaxHigh - Close[index])) * 100, res)
    else:
        WPR = _s_GetWPR_WPR_prev
    if index:
        _s_GetWPR_WPR_prev = WPR
    return WPR

# ---- static local variables
_s_OnCalculate_Sell1_prev = 0
_s_OnCalculate_Buy1_prev = 0
_s_OnCalculate_Sell2_prev = 0.0
_s_OnCalculate_Buy2_prev = 0.0
_s_GetWPR_WPR_prev = -50.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AFStar(_MQL5Indicator):
    name = 'AFStar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartFast': 3.0,
        'EndFast': 3.5,
        'StartSlow': 8.0,
        'EndSlow': 9.0,
        'StepPeriod': 0.2,
        'StartRisk': 1.0,
        'EndRisk': 2.8,
        'StepRisk': 0.5,
    }

