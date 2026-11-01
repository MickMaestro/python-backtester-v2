"""woodiescci — converted from MQL5: MQL5 Indicators/WoodiesCCI/woodiescci.mq5

Copyright: Dmitry Voronkov; Link: vdv_2001@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Dmitry Voronkov', 'link': 'vdv_2001@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_maximum': 300.0, 'indicator_minimum': -300.0, 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 10, 2: 1, 3: 1, 4: 8}, 'colors': {1: [12632256, 55295, 9498256, 4678655], 2: [0], 3: [255], 4: [32768, 255]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 3}, 'styles': {}, 'labels': {}, 'levels': [50.0, -50.0, 100.0, -100.0, 200.0, -200.0], 'description': [], 'name': 'woodiescci', 'source': 'MQL5 Indicators/WoodiesCCI/woodiescci.mq5', 'folder': 'WoodiesCCI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 0, 'label': 'Time period', 'sinput': False}, {'mql': 'InpSlowCCIPeriod', 'py': 'InpSlowCCIPeriod', 'param': 'InpSlowCCIPeriod', 'type': 'int', 'default': 14, 'label': 'Slow CCI', 'sinput': False}, {'mql': 'InpFastCCIPeriod', 'py': 'InpFastCCIPeriod', 'param': 'InpFastCCIPeriod', 'type': 'int', 'default': 6, 'label': 'Fast CCI', 'sinput': False}, {'mql': 'InpLSMAPeriod', 'py': 'InpLSMAPeriod', 'param': 'InpLSMAPeriod', 'type': 'int', 'default': 25, 'label': 'Period LSMA', 'sinput': False}, {'mql': 'InpSignalBar', 'py': 'InpSignalBar', 'param': 'InpSignalBar', 'type': 'int', 'default': 6, 'label': 'Bar of change of a trend', 'sinput': False}, {'mql': 'InpHowLong', 'py': 'InpHowLong', 'param': 'InpHowLong', 'type': 'int', 'default': 300, 'label': 'How many bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', PERIOD_CURRENT)  # Time period
InpSlowCCIPeriod = _input('InpSlowCCIPeriod', 14)  # Slow CCI
InpFastCCIPeriod = _input('InpFastCCIPeriod', 6)  # Fast CCI
InpLSMAPeriod = _input('InpLSMAPeriod', 25)  # Period LSMA
InpSignalBar = _input('InpSignalBar', 6)  # Bar of change of a trend
InpHowLong = _input('InpHowLong', 300)  # How many bars
CountPeriodBar = 0
ExtSlowCCIHistogram = Arr(0, 0.0)
ExtSlowCCIHistogramColor = Arr(0, 0.0)
ExtSlowCCILine = Arr(0, 0.0)
ExtFastCCILine = Arr(0, 0.0)
ExtLSMA = Arr(0, 0.0)
ExtColorLSMA = Arr(0, 0.0)
HSlowCCI = 0
HFastCCI = 0

def OnInit():
    global HFastCCI, HSlowCCI
    SetIndexBuffer(0, ExtSlowCCIHistogram, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSlowCCIHistogramColor, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtSlowCCILine, INDICATOR_DATA)
    SetIndexBuffer(3, ExtFastCCILine, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLSMA, INDICATOR_DATA)
    SetIndexBuffer(5, ExtColorLSMA, INDICATOR_COLOR_INDEX)
    PlotIndexSetString(0, PLOT_LABEL, 'Histogram (' + IntegerToString(InpSlowCCIPeriod) + ') CCI')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpSlowCCIPeriod - 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpSlowCCIPeriod - 1)
    PlotIndexSetString(2, PLOT_LABEL, 'Turbo(' + IntegerToString(InpFastCCIPeriod) + ') CCI')
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpFastCCIPeriod - 1)
    PlotIndexSetString(3, PLOT_LABEL, 'LSMA(' + IntegerToString(InpLSMAPeriod) + ')')
    IndicatorSetString(INDICATOR_SHORTNAME, 'WoodiesCCI ' + PeriodToString(InpPeriod))
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    HSlowCCI = iCCI(None, InpPeriod, InpSlowCCIPeriod, PRICE_TYPICAL)
    HFastCCI = iCCI(None, InpPeriod, InpFastCCIPeriod, PRICE_TYPICAL)
    EventSetTimer(1)
    return 0

def OnDeinit(reason):
    EventKillTimer()

def OnTimer():
    second = TimeEndOfPeriod(InpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WoodiesCCI ' + PeriodToString(InpPeriod) + ' [' + IntegerToString(second) + ' sec ]')
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global CountPeriodBar
    start_buf = 0
    pos = 0
    counter_bars = 0
    Buff = Arr(0, 0.0)
    price = Arr(0, 0.0)
    fup = False
    fdn = False
    count = BarsCalculated(HSlowCCI)
    count_fast = BarsCalculated(HFastCCI)
    if count <= 0 or count_fast <= 0:
        Print('Not all data of iCCI is calculated. Error', GetLastError())
        return 0
    if CountPeriodBar != count or prev_calculated != rates_total:
        CountPeriodBar = count
        if count > rates_total:
            start_buf = count - rates_total
            count = rates_total
        if count == rates_total:
            start_buf = 0
        if InpHowLong <= 0:
            pos = count
        else:
            pos = InpHowLong
        if CopyBuffer(HSlowCCI, 0, start_buf, count, ExtSlowCCIHistogram) <= 0:
            Print('Getting of iCCI data has failed! Error', GetLastError())
            return 0
        ArrayCopy(ExtSlowCCILine, ExtSlowCCIHistogram)
        if CopyBuffer(HFastCCI, 0, start_buf, count, ExtFastCCILine) <= 0:
            Print('Getting of iCCI data has failed! Error', GetLastError())
            return 0
        ArrayInitialize(ExtSlowCCIHistogramColor, 0)
        ArrayInitialize(ExtColorLSMA, 0)
    else:
        if CopyBuffer(HSlowCCI, 0, 0, 1, Buff) <= 0:
            Print('Getting of iCCI data has failed! Error', GetLastError())
            return 0
        ExtSlowCCIHistogram[rates_total - 1] = Buff[0]
        ExtSlowCCILine[rates_total - 1] = ExtSlowCCIHistogram[rates_total - 1]
        if CopyBuffer(HFastCCI, 0, 0, 1, Buff) <= 0:
            Print('Getting of iCCI data has failed! Error', GetLastError())
            return 0
        ExtFastCCILine[rates_total - 1] = Buff[0]
    for i in range(rates_total - pos, rates_total):
        if (ExtSlowCCIHistogram[i - 1] * ExtSlowCCIHistogram[i]) < 0:
            counter_bars = 1
        else:
            counter_bars += 1
        if counter_bars == (InpSignalBar - 1):
            ExtSlowCCIHistogramColor[i] = 1.0
        if counter_bars >= InpSignalBar and ExtSlowCCIHistogram[i] > 0:
            ExtSlowCCIHistogramColor[i] = 2.0
        if counter_bars >= InpSignalBar and ExtSlowCCIHistogram[i] < 0:
            ExtSlowCCIHistogramColor[i] = 3.0
    close_count = CopyClose(None, InpPeriod, 0, pos + InpLSMAPeriod, price)
    if close_count <= 0:
        Print('Getting Close data has failed! Error', GetLastError())
        return 0
    for i in range(1, pos):
        tmp = CalcLsma(close_count - i, InpLSMAPeriod, price)
        if price[close_count - i] == tmp:
            ExtColorLSMA[rates_total - i] = ExtColorLSMA[rates_total - i - 1]
        if price[close_count - i] > tmp:
            ExtColorLSMA[rates_total - i] = 0.0
        if price[close_count - i] < tmp:
            ExtColorLSMA[rates_total - i] = 1.0
    return rates_total

def PeriodToString(period):
    tmp = 0
    if period == PERIOD_CURRENT:
        tmp = Period()
    else:
        tmp = period
    _sw1 = tmp
    if _sw1 == PERIOD_M1:
        return 'M1'
    elif _sw1 == PERIOD_M2:
        return 'M2'
    elif _sw1 == PERIOD_M3:
        return 'M3'
    elif _sw1 == PERIOD_M4:
        return 'M4'
    elif _sw1 == PERIOD_M5:
        return 'M5'
    elif _sw1 == PERIOD_M6:
        return 'M6'
    elif _sw1 == PERIOD_M10:
        return 'M10'
    elif _sw1 == PERIOD_M12:
        return 'M12'
    elif _sw1 == PERIOD_M15:
        return 'M15'
    elif _sw1 == PERIOD_M20:
        return 'M20'
    elif _sw1 == PERIOD_M30:
        return 'M30'
    elif _sw1 == PERIOD_H1:
        return 'H1'
    elif _sw1 == PERIOD_H2:
        return 'H2'
    elif _sw1 == PERIOD_H3:
        return 'H3'
    elif _sw1 == PERIOD_H4:
        return 'H4'
    elif _sw1 == PERIOD_H6:
        return 'H6'
    elif _sw1 == PERIOD_H8:
        return 'H8'
    elif _sw1 == PERIOD_H12:
        return 'H12'
    elif _sw1 == PERIOD_D1:
        return 'Daily'
    elif _sw1 == PERIOD_W1:
        return 'Weekly'
    elif _sw1 == PERIOD_MN1:
        return 'Monthly'
    return ""

def TimeEndOfPeriod(_TimePeriod):
    tmpDateTime = 0
    tmp = 0
    last_time = MqlDateTime()
    TimeToStruct(TimeTradeServer(), last_time)
    last_time.sec = 0
    if _TimePeriod <= PERIOD_H1:
        tmp = _idiv(PeriodSeconds(_TimePeriod), PeriodSeconds(PERIOD_M1))
        tmp = _idiv(last_time.min, tmp)
        last_time.min = _idiv((tmp + 1) * PeriodSeconds(_TimePeriod), PeriodSeconds(PERIOD_M1))
    elif _TimePeriod > PERIOD_H1 and Period() <= PERIOD_D1:
        tmp = _idiv(PeriodSeconds(_TimePeriod), PeriodSeconds(PERIOD_H1))
        tmp = _idiv(last_time.hour, tmp)
        last_time.hour = _idiv((tmp + 1) * PeriodSeconds(_TimePeriod), PeriodSeconds(PERIOD_H1))
        last_time.min = 0
    tmpDateTime = StructToTime(last_time)
    tmpDateTime = tmpDateTime - TimeTradeServer()
    return tmpDateTime

def CalcLsma(index, period, price):
    sum_ = 0.0
    for i in range(1, period + 1):
        tmp = i - ((period + 1) / 3.0)
        sum_ += tmp * price[index - period + i] * 6
    return _fdiv(sum_, period * (period + 1))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Woodiescci(_MQL5Indicator):
    name = 'woodiescci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time period
        'InpSlowCCIPeriod': 14,  # Slow CCI
        'InpFastCCIPeriod': 6,  # Fast CCI
        'InpLSMAPeriod': 25,  # Period LSMA
        'InpSignalBar': 6,  # Bar of change of a trend
        'InpHowLong': 300,  # How many bars
    }
    y_range = (-300.0, 300.0)

