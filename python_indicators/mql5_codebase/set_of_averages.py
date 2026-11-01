"""Set_Of_Averages — converted from MQL5: MQL5 Indicators/A set of eight Moving Averages/Set_Of_Averages.mq5

Draws the sets of Moving Averages
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [16711680], 2: [255], 3: [32768], 4: [8388608], 5: [16776960], 6: [16711935], 7: [55295], 8: [4678655]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, 'labels': {1: 'MA1', 2: 'MA2', 3: 'MA3', 4: 'MA4', 5: 'MA5', 6: 'MA6', 7: 'MA7', 8: 'MA8'}, 'levels': [], 'description': ['Draws the sets of Moving Averages'], 'name': 'Set_Of_Averages', 'source': 'MQL5 Indicators/A set of eight Moving Averages/Set_Of_Averages.mq5', 'folder': 'A set of eight Moving Averages', 'inputs': [{'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Calculated method MA', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 1, 'label': 'Calculated price MA', 'sinput': False}, {'mql': 'InpPeriods', 'py': 'InpPeriods', 'param': None, 'type': 'string', 'default': '10,20,30,40,50,60,70,80', 'label': 'Periods of all MA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMethod = _input('InpMethod', MODE_SMA)  # Calculated method MA
InpPrice = _input('InpPrice', PRICE_CLOSE)  # Calculated price MA
InpPeriods = _input('InpPeriods', '10,20,30,40,50,60,70,80')  # Periods of all MA
MAPeriods = Arr(0, 0)
total = 0

class SDataMA(MqlObject):
    _q_fields = ('buffer', 'period', 'handle')
    def __init__(self, *args):
        self.buffer = Arr(0, 0.0)
        self.period = 0
        self.handle = 0

def OnInit():
    global total
    IndicatorSetString(INDICATOR_SHORTNAME, 'Set of averages')
    total = StringValueToArray(InpPeriods, ',', MAPeriods)
    if total < 1:
        Print('An error occurred while retrieving the MA periods data. Check settings "Periods of all MA"')
        return INIT_FAILED
    ArrayResize(data_ma, total)
    for i in range(0, total):
        data_ma[i].period = MAPeriods[i]
        data_ma[i].handle = iMA(Symbol(), PERIOD_CURRENT, MAPeriods[i], 0, InpMethod, InpPrice)
        if data_ma[i].handle == INVALID_HANDLE:
            Print('Error creating MA', i, ' handle')
            return INIT_FAILED
        SetIndexBuffer(i, data_ma[i].buffer, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < data_ma[total - 1].period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        for i in range(0, total):
            ArrayInitialize(data_ma[i].buffer, EMPTY_VALUE)
    for i in range(0, total):
        if BarsCalculated(data_ma[i].handle) < 0:
            continue
        if CopyBuffer(data_ma[i].handle, 0, 0, (1 if (limit == 0) else limit), data_ma[i].buffer) < 0:
            continue
    return rates_total

def StringValueToArray(string_value, separator, array_dest):
    tmp = Arr(0, "")
    num = StringSplit(string_value, StringGetCharacter(separator, 0), tmp)
    if num > 0:
        ArrayResize(array_dest, num)
        for i in range(0, num):
            value = _int(StringToInteger(tmp[i]))
            array_dest[i] = (1 if (value == 0) else value)
    return num

# ---- global variables initialised from expressions
data_ma = Arr(0, 0, factory=SDataMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SetOfAverages(_MQL5Indicator):
    name = 'Set_Of_Averages'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Calculated method MA
        'InpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Calculated price MA
    }

