"""mpc — converted from MQL5: MQL5 Indicators/MPC/mpc.mq5

Middle Point Channel
Copyright: Copyright © 2007, Alexandre; Link: http://www.kroufr.ru/content/view/885/124/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Alexandre', 'link': 'http://www.kroufr.ru/content/view/885/124/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711935], 3: [16776960]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Middle MPC', 2: 'Upper MPC', 3: 'Lower MPC'}, 'levels': [], 'description': ['Middle Point Channel'], 'name': 'mpc', 'source': 'MQL5 Indicators/MPC/mpc.mq5', 'folder': 'MPC', 'inputs': [{'mql': 'MPC_Range', 'py': 'MPC_Range', 'param': 'MPC_Range', 'type': 'uint', 'default': 40, 'label': 'Period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MPC_Range = _input('MPC_Range', 40)  # Period
Shift = _input('Shift', 0)  # Shift
MDBuffer = Arr(0, 0.0)
UpMDBuffer = Arr(0, 0.0)
DnMDBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(MPC_Range)
    SetIndexBuffer(0, MDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(MDBuffer, True)
    SetIndexBuffer(1, UpMDBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, DnMDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpMDBuffer, True)
    ArraySetAsSeries(DnMDBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Middle Point Channel')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    HH = 0.0
    LL = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    for bar in range(limit, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, MPC_Range)]
        LL = low[ArrayMinimum(low, bar, MPC_Range)]
        UpMDBuffer[bar] = HH
        MDBuffer[bar] = (HH + LL) / 2
        DnMDBuffer[bar] = LL
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Mpc(_MQL5Indicator):
    name = 'mpc'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MPC_Range': 40,  # Period
        'Shift': 0,  # Shift
    }

