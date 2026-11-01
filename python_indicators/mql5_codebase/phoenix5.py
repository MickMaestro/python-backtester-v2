"""phoenix5 — converted from MQL5: MQL5 Indicators/Phoenix5/phoenix5.mq5

Copyright: Copyright © 2006, fryk@tlen.pl; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, fryk@tlen.pl', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Phoenix5 Sell', 2: 'Phoenix5 Buy'}, 'levels': [], 'description': [''], 'name': 'phoenix5', 'source': 'MQL5 Indicators/Phoenix5/phoenix5.mq5', 'folder': 'Phoenix5', 'inputs': [{'mql': 'iSMAPeriod', 'py': 'iSMAPeriod', 'param': 'iSMAPeriod', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'iSMA2Bars', 'py': 'iSMA2Bars', 'param': 'iSMA2Bars', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'iPercent', 'py': 'iPercent', 'param': 'iPercent', 'type': 'double', 'default': 0.0032, 'label': '', 'sinput': False}, {'mql': 'iEnvelopePeriod', 'py': 'iEnvelopePeriod', 'param': 'iEnvelopePeriod', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'iOSMAFast', 'py': 'iOSMAFast', 'param': 'iOSMAFast', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'iOSMASlow', 'py': 'iOSMASlow', 'param': 'iOSMASlow', 'type': 'uint', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'iOSMASignal', 'py': 'iOSMASignal', 'param': 'iOSMASignal', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'iFast_Period', 'py': 'iFast_Period', 'param': 'iFast_Period', 'type': 'uint', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'iFast_Price', 'py': 'iFast_Price', 'param': 'iFast_Price', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'iSlow_Period', 'py': 'iSlow_Period', 'param': 'iSlow_Period', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'iSlow_Price', 'py': 'iSlow_Price', 'param': 'iSlow_Price', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'iDVBuySell', 'py': 'iDVBuySell', 'param': 'iDVBuySell', 'type': 'double', 'default': 0.003, 'label': '', 'sinput': False}, {'mql': 'iDVStayOut', 'py': 'iDVStayOut', 'param': 'iDVStayOut', 'type': 'double', 'default': 0.024, 'label': '', 'sinput': False}, {'mql': 'iPrefSettings', 'py': 'iPrefSettings', 'param': 'iPrefSettings', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iSMAPeriod = _input('iSMAPeriod', 7)
iSMA2Bars = _input('iSMA2Bars', 14)
iPercent = _input('iPercent', 0.0032)
iEnvelopePeriod = _input('iEnvelopePeriod', 2)
iOSMAFast = _input('iOSMAFast', 5)
iOSMASlow = _input('iOSMASlow', 30)
iOSMASignal = _input('iOSMASignal', 2)
iFast_Period = _input('iFast_Period', 25)
iFast_Price = _input('iFast_Price', PRICE_OPEN)
iSlow_Period = _input('iSlow_Period', 15)
iSlow_Price = _input('iSlow_Price', PRICE_OPEN)
iDVBuySell = _input('iDVBuySell', 0.003)
iDVStayOut = _input('iDVStayOut', 0.024)
iPrefSettings = _input('iPrefSettings', True)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
SMA_Handle = 0
FsMA_Handle = 0
SlMA_Handle = 0
Env_Handle = 0
OsMA_Handle = 0
Percent = 0.0
DVBuySell = 0.0
DVStayOut = 0.0
SMAPeriod = 0
SMA2Bars = 0
EnvelopePeriod = 0
OSMAFast = 0
OSMASlow = 0
OSMASignal = 0
Fast_Period = 0
Slow_Period = 0

def OnInit():
    global DVBuySell, DVStayOut, Env_Handle, EnvelopePeriod, Fast_Period, FsMA_Handle, OSMAFast, OSMASignal, OSMASlow, OsMA_Handle, Percent, SMA2Bars, SMAPeriod, SMA_Handle, SlMA_Handle, Slow_Period, min_rates_total
    SMAPeriod = iSMAPeriod
    SMA2Bars = iSMA2Bars
    Percent = iPercent
    EnvelopePeriod = iEnvelopePeriod
    OSMAFast = iOSMAFast
    OSMASlow = iOSMASlow
    OSMASignal = iOSMASignal
    Fast_Period = iFast_Period
    Slow_Period = iSlow_Period
    DVBuySell = iDVBuySell
    DVStayOut = iDVStayOut
    if iPrefSettings == True:
        if Symbol() == 'USDJPY' or Symbol() == 'USDJPYm':
            Percent = 0.0032
            EnvelopePeriod = 2
            SMAPeriod = 2
            SMA2Bars = 18
            OSMAFast = 5
            OSMASlow = 22
            OSMASignal = 2
            Fast_Period = 25
            Slow_Period = 15
            DVBuySell = 0.0029
            DVStayOut = 0.024
        if Symbol() == 'EURJPY' or Symbol() == 'EURJPYm':
            Percent = 0.007
            EnvelopePeriod = 2
            SMAPeriod = 4
            SMA2Bars = 16
            OSMAFast = 11
            OSMASlow = 20
            OSMASignal = 14
            Fast_Period = 20
            Slow_Period = 10
            DVBuySell = 0.0078
            DVStayOut = 0.026
        if Symbol() == 'GBPJPY' or Symbol() == 'GBPJPYm':
            Percent = 0.0072
            EnvelopePeriod = 2
            SMAPeriod = 8
            SMA2Bars = 12
            OSMAFast = 5
            OSMASlow = 36
            OSMASignal = 10
            Fast_Period = 17
            Slow_Period = 28
            DVBuySell = 0.0034
            DVStayOut = 0.063
        if Symbol() == 'USDCHF' or Symbol() == 'USDCHFm':
            Percent = 0.0056
            EnvelopePeriod = 10
            SMAPeriod = 5
            SMA2Bars = 9
            OSMAFast = 5
            OSMASlow = 12
            OSMASignal = 11
            Fast_Period = 5
            Slow_Period = 20
            DVBuySell = 0.00022
            DVStayOut = 0.0015
        if Symbol() == 'GBPUSD' or Symbol() == 'GBPUSDm':
            Percent = 0.0023
            EnvelopePeriod = 6
            SMAPeriod = 3
            SMA2Bars = 14
            OSMAFast = 23
            OSMASlow = 17
            OSMASignal = 15
            Fast_Period = 25
            Slow_Period = 37
            DVBuySell = 0.00042
            DVStayOut = 0.05
    min_rates_OsMA = _uint(MathMax(OSMAFast, OSMASlow) + OSMASignal + 2)
    min_rates_MA = _uint(MathMax(MathMax(SMAPeriod + SMA2Bars, Fast_Period), Slow_Period))
    min_rates_total = _int(MathMax(MathMax(EnvelopePeriod + 1, min_rates_OsMA), min_rates_MA))
    OsMA_Handle = iOsMA(Symbol(), PERIOD_CURRENT, OSMASlow, OSMAFast, OSMASignal, PRICE_CLOSE)
    if OsMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iOsMA indicator')
    SMA_Handle = iMA(Symbol(), PERIOD_CURRENT, SMAPeriod, 0, MODE_SMA, PRICE_MEDIAN)
    if SMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    FsMA_Handle = iMA(Symbol(), PERIOD_CURRENT, Fast_Period, 0, MODE_SMA, iFast_Price)
    if FsMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    SlMA_Handle = iMA(Symbol(), PERIOD_CURRENT, Slow_Period, 0, MODE_SMA, iSlow_Price)
    if SlMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    Env_Handle = iEnvelopes(Symbol(), PERIOD_CURRENT, EnvelopePeriod, 0, MODE_SMA, PRICE_CLOSE, Percent)
    if Env_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of iEnvelopes indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Phoenix5'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(Env_Handle) < rates_total or BarsCalculated(SMA_Handle) < rates_total) or BarsCalculated(FsMA_Handle) < rates_total) or BarsCalculated(SlMA_Handle) < rates_total) or BarsCalculated(OsMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    UpEnv = Arr(0, 0.0)
    DnEnv = Arr(0, 0.0)
    SMA = Arr(0, 0.0)
    FsMA = Arr(0, 0.0)
    SlMA = Arr(0, 0.0)
    OsMA = Arr(0, 0.0)
    Range = 0.0
    AvgRange = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(UpEnv, True)
    ArraySetAsSeries(DnEnv, True)
    ArraySetAsSeries(SMA, True)
    ArraySetAsSeries(FsMA, True)
    ArraySetAsSeries(SlMA, True)
    ArraySetAsSeries(OsMA, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    to_copy += 1
    if CopyBuffer(FsMA_Handle, 0, 0, to_copy, FsMA) <= 0:
        return 0
    if CopyBuffer(SlMA_Handle, 0, 0, to_copy, SlMA) <= 0:
        return 0
    if CopyBuffer(Env_Handle, UPPER_LINE, 0, to_copy, UpEnv) <= 0:
        return 0
    if CopyBuffer(Env_Handle, LOWER_LINE, 0, to_copy, DnEnv) <= 0:
        return 0
    to_copy += 1
    if CopyBuffer(OsMA_Handle, 0, 0, to_copy, OsMA) <= 0:
        return 0
    to_copy = _int(limit + 1 + SMA2Bars)
    if CopyBuffer(SMA_Handle, 0, 0, to_copy, SMA) <= 0:
        return 0
    BuySignal1 = False
    BuySignal2 = False
    BuySignal3 = False
    SellSignal1 = False
    SellSignal2 = False
    SellSignal3 = False
    BuySignal4 = False
    SellSignal4 = False
    HighEnvelope1 = 0.0
    LowEnvelope1 = 0.0
    CloseBar1 = 0.0
    OsMABar1 = 0.0
    OsMABar2 = 0.0
    SMA1 = 0.0
    SMA2 = 0.0
    diverge = 0.0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Range = 0.0
        AvgRange = 0.0
        for count in range(bar, bar + 9 + 1):
            AvgRange = AvgRange + MathAbs(high[count] - low[count])
        Range = AvgRange / (10 * 4)
        BuySignal1 = False
        SellSignal1 = False
        HighEnvelope1 = UpEnv[bar + 1]
        LowEnvelope1 = DnEnv[bar + 1]
        CloseBar1 = close[bar + 1]
        if CloseBar1 > HighEnvelope1:
            SellSignal1 = True
        if CloseBar1 < LowEnvelope1:
            BuySignal1 = True
        BuySignal2 = False
        SellSignal2 = False
        SMA1 = SMA[bar + 1]
        SMA2 = SMA[bar + SMA2Bars]
        if (SMA2 - SMA1) > 0:
            BuySignal2 = True
        if (SMA2 - SMA1) < 0:
            SellSignal2 = True
        BuySignal3 = False
        SellSignal3 = False
        OsMABar2 = OsMA[bar + 2]
        OsMABar1 = OsMA[bar + 1]
        if OsMABar2 > OsMABar1:
            SellSignal3 = True
        if OsMABar2 < OsMABar1:
            BuySignal3 = True
        BuySignal4 = False
        SellSignal4 = False
        diverge = FsMA[bar + 1] - SlMA[bar + 1]
        if diverge >= DVBuySell and diverge <= DVStayOut:
            BuySignal4 = True
        if diverge <= (DVBuySell * -1) and diverge >= (DVStayOut * -1):
            SellSignal4 = True
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if ((BuySignal1 and BuySignal2) and BuySignal3) and BuySignal4:
            BuyBuffer[bar] = low[bar] - Range
        if ((SellSignal1 and SellSignal2) and SellSignal3) and SellSignal4:
            SellBuffer[bar] = high[bar] + Range
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Phoenix5(_MQL5Indicator):
    name = 'phoenix5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iSMAPeriod': 7,
        'iSMA2Bars': 14,
        'iPercent': 0.0032,
        'iEnvelopePeriod': 2,
        'iOSMAFast': 5,
        'iOSMASlow': 30,
        'iOSMASignal': 2,
        'iFast_Period': 25,
        'iFast_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=2),
        'iSlow_Period': 15,
        'iSlow_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=2),
        'iDVBuySell': 0.003,
        'iDVStayOut': 0.024,
        'iPrefSettings': True,
    }

