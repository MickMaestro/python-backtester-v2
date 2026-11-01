"""PMF — converted from MQL5: MQL5 Indicators/PMF/PMF.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'PMF'}, 'levels': [], 'description': [], 'name': 'PMF', 'source': 'MQL5 Indicators/PMF/PMF.mq5', 'folder': 'PMF', 'inputs': [{'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpCumulative', 'py': 'InpCumulative', 'param': 'InpCumulative', 'type': 'int', 'default': 1, 'label': 'Cumulative', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_ON_OFF
INPUT_ON = 1
INPUT_OFF = 0
_enum('ENUM_INPUT_ON_OFF', {1: 'INPUT_ON', 0: 'INPUT_OFF'})

# ---- inputs and global variables
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpCumulative = _input('InpCumulative', INPUT_ON)  # Cumulative
BufferPMF = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferPMF, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PMF')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPMF, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferPMF, 0)
    for i in range(limit, 0 - 1, -1):
        if limit == (rates_total - 3):
            BufferPMF[i] = 0.0
        Current = ValueByPrice(InpAppliedPrice, i, open, high, low, close)
        Previous = ValueByPrice(InpAppliedPrice, i + 1, open, high, low, close)
        PrePrevious = ValueByPrice(InpAppliedPrice, i + 2, open, high, low, close)
        DiffCurrent = (Current - Previous) * tick_volume[i]
        DiffPrevious = (Previous - PrePrevious) * tick_volume[i + 1]
        if InpCumulative:
            BufferPMF[i] = BufferPMF[i + 1] + DiffCurrent
        else:
            BufferPMF[i] = DiffCurrent + DiffPrevious
    return rates_total

def ValueByPrice(price, index, open, high, low, close):
    return (close[index] if (price == PRICE_CLOSE) else open[index] if (price == PRICE_OPEN) else high[index] if (price == PRICE_HIGH) else low[index] if (price == PRICE_LOW) else ((high[index] + low[index]) / 2.0) if (price == PRICE_MEDIAN) else ((high[index] + low[index] + close[index]) / 3.0) if (price == PRICE_TYPICAL) else ((high[index] + low[index] + (2 * close[index])) / 4.0))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PMF(_MQL5Indicator):
    name = 'PMF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpCumulative': _Choice({1: 'On', 0: 'Off'}, default=1),  # Cumulative
    }

