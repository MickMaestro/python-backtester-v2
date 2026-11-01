"""Multi-colored_trend_indicator — converted from MQL5: MQL5 Indicators/Multi colored trend indicator MT5/Multi-colored_trend_indicator.mq5

Questions about the code? DM me
Contact me on https://www.mql5.com/en/users/sakhawatdhrubo
Copyright: Copyright 2023, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [25600, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Trend'}, 'levels': [], 'description': ['Questions about the code? DM me', 'Contact me on https://www.mql5.com/en/users/sakhawatdhrubo'], 'name': 'Multi-colored_trend_indicator', 'source': 'MQL5 Indicators/Multi colored trend indicator MT5/Multi-colored_trend_indicator.mq5', 'folder': 'Multi colored trend indicator MT5', 'inputs': [{'mql': 'InpFastMAPeriod', 'py': 'InpFastMAPeriod', 'param': 'InpFastMAPeriod', 'type': 'int', 'default': 10, 'label': 'Fast moving average period', 'sinput': False}, {'mql': 'InpFastMAMethod', 'py': 'InpFastMAMethod', 'param': 'InpFastMAMethod', 'type': 'int', 'default': 0, 'label': 'Fast moving average method', 'sinput': False}, {'mql': 'InpFastMAAppliedPrice', 'py': 'InpFastMAAppliedPrice', 'param': 'InpFastMAAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Fast moving average applyed price', 'sinput': False}, {'mql': 'InpSlowMAPeriod', 'py': 'InpSlowMAPeriod', 'param': 'InpSlowMAPeriod', 'type': 'int', 'default': 50, 'label': 'Slow moving average period', 'sinput': False}, {'mql': 'InpSlowMAMethod', 'py': 'InpSlowMAMethod', 'param': 'InpSlowMAMethod', 'type': 'int', 'default': 0, 'label': 'Slow moving average method', 'sinput': False}, {'mql': 'InpSlowMAAppliedPrice', 'py': 'InpSlowMAAppliedPrice', 'param': 'InpSlowMAAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Slow moving average applyed price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFastMAPeriod = _input('InpFastMAPeriod', 10)  # Fast moving average period
InpFastMAMethod = _input('InpFastMAMethod', MODE_SMA)  # Fast moving average method
InpFastMAAppliedPrice = _input('InpFastMAAppliedPrice', PRICE_CLOSE)  # Fast moving average applyed price
InpSlowMAPeriod = _input('InpSlowMAPeriod', 50)  # Slow moving average period
InpSlowMAMethod = _input('InpSlowMAMethod', MODE_SMA)  # Slow moving average method
InpSlowMAAppliedPrice = _input('InpSlowMAAppliedPrice', PRICE_CLOSE)  # Slow moving average applyed price
MainBuffer = Arr(0, 0.0)
ColorsBuffer = Arr(0, 0.0)
HandleFastMA = 0
HandleSlowMA = 0
FastMAValues = Arr(0, 0.0)
SlowMAValues = Arr(0, 0.0)

def OnInit():
    global HandleFastMA, HandleSlowMA
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorsBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(MainBuffer, True)
    ArraySetAsSeries(ColorsBuffer, True)
    ArraySetAsSeries(FastMAValues, True)
    ArraySetAsSeries(SlowMAValues, True)
    HandleFastMA = iMA(Symbol(), Period(), InpFastMAPeriod, 0, InpFastMAMethod, InpFastMAAppliedPrice)
    HandleSlowMA = iMA(Symbol(), Period(), InpSlowMAPeriod, 0, InpSlowMAMethod, InpSlowMAAppliedPrice)
    if HandleFastMA == INVALID_HANDLE or HandleSlowMA == INVALID_HANDLE:
        printf('Error Creating Moving Average Handle: [%d]', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(HandleFastMA)
    IndicatorRelease(HandleSlowMA)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    count = rates_total - prev_calculated
    if prev_calculated > 0:
        count += 1
    if CopyBuffer(HandleFastMA, 0, 0, count, FastMAValues) < count:
        return 0
    if CopyBuffer(HandleSlowMA, 0, 0, count, SlowMAValues) < count:
        return 0
    for i in range(count - 1, 0 - 1, -1):
        fast = FastMAValues[i]
        slow = SlowMAValues[i]
        main = (fast + slow) / 2
        MainBuffer[i] = main
        if fast > slow:
            ColorsBuffer[i] = 0.0
        else:
            ColorsBuffer[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiColoredTrendIndicator(_MQL5Indicator):
    name = 'Multi-colored_trend_indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastMAPeriod': 10,  # Fast moving average period
        'InpFastMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Fast moving average method
        'InpFastMAAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Fast moving average applyed price
        'InpSlowMAPeriod': 50,  # Slow moving average period
        'InpSlowMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Slow moving average method
        'InpSlowMAAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Slow moving average applyed price
    }

