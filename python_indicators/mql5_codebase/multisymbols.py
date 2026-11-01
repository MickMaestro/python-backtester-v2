"""MultiSymbols — converted from MQL5: MQL5 Indicators/Multi-Symbol Momentum/MultiSymbols.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 0, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [16711680], 2: [255], 3: [32768], 4: [8388608], 5: [16776960], 6: [16711935], 7: [55295], 8: [4678655]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, 'labels': {1: 'Symbol 1', 2: 'Symbol 2', 3: 'Symbol 3', 4: 'Symbol 4', 5: 'Symbol 5', 6: 'Symbol 6', 7: 'Symbol 7', 8: 'Symbol 8'}, 'levels': [], 'description': [], 'name': 'MultiSymbols', 'source': 'MQL5 Indicators/Multi-Symbol Momentum/MultiSymbols.mq5', 'folder': 'Multi-Symbol Momentum', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 1, 'label': 'Period of MA', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Calculation method', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 1000, 'label': 'Vertical shift', 'sinput': False}, {'mql': 'InpSymbol1', 'py': 'InpSymbol1', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'Symbol 1', 'sinput': False}, {'mql': 'InpSymbol2', 'py': 'InpSymbol2', 'param': None, 'type': 'string', 'default': 'EURJPY', 'label': 'Symbol 2', 'sinput': False}, {'mql': 'InpSymbol3', 'py': 'InpSymbol3', 'param': None, 'type': 'string', 'default': 'USDJPY', 'label': 'Symbol 3', 'sinput': False}, {'mql': 'InpSymbol4', 'py': 'InpSymbol4', 'param': None, 'type': 'string', 'default': 'EURGBP', 'label': 'Symbol 4', 'sinput': False}, {'mql': 'InpSymbol5', 'py': 'InpSymbol5', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Symbol 5', 'sinput': False}, {'mql': 'InpSymbol6', 'py': 'InpSymbol6', 'param': None, 'type': 'string', 'default': 'EURCHF', 'label': 'Symbol 6', 'sinput': False}, {'mql': 'InpSymbol7', 'py': 'InpSymbol7', 'param': None, 'type': 'string', 'default': 'USDCHF', 'label': 'Symbol 7', 'sinput': False}, {'mql': 'InpSymbol8', 'py': 'InpSymbol8', 'param': None, 'type': 'string', 'default': 'USDCAD', 'label': 'Symbol 8', 'sinput': False}, {'mql': 'InpColor1', 'py': 'InpColor1', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color of symbols line 1', 'sinput': False}, {'mql': 'InpColor2', 'py': 'InpColor2', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color of symbols line 2', 'sinput': False}, {'mql': 'InpColor3', 'py': 'InpColor3', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Color of symbols line 3', 'sinput': False}, {'mql': 'InpColor4', 'py': 'InpColor4', 'param': None, 'type': 'color', 'default': 8388608, 'label': 'Color of symbols line 4', 'sinput': False}, {'mql': 'InpColor5', 'py': 'InpColor5', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'Color of symbols line 5', 'sinput': False}, {'mql': 'InpColor6', 'py': 'InpColor6', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Color of symbols line 6', 'sinput': False}, {'mql': 'InpColor7', 'py': 'InpColor7', 'param': None, 'type': 'color', 'default': 55295, 'label': 'Color of symbols line 7', 'sinput': False}, {'mql': 'InpColor8', 'py': 'InpColor8', 'param': None, 'type': 'color', 'default': 4678655, 'label': 'Color of symbols line 8', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 1)  # Period of MA
InpMethod = _input('InpMethod', MODE_SMA)  # Calculation method
InpPrice = _input('InpPrice', PRICE_CLOSE)  # Applied price
InpShift = _input('InpShift', 1000)  # Vertical shift
InpSymbol1 = _input('InpSymbol1', 'EURUSD')  # Symbol 1
InpSymbol2 = _input('InpSymbol2', 'EURJPY')  # Symbol 2
InpSymbol3 = _input('InpSymbol3', 'USDJPY')  # Symbol 3
InpSymbol4 = _input('InpSymbol4', 'EURGBP')  # Symbol 4
InpSymbol5 = _input('InpSymbol5', 'GBPUSD')  # Symbol 5
InpSymbol6 = _input('InpSymbol6', 'EURCHF')  # Symbol 6
InpSymbol7 = _input('InpSymbol7', 'USDCHF')  # Symbol 7
InpSymbol8 = _input('InpSymbol8', 'USDCAD')  # Symbol 8
InpColor1 = _input('InpColor1', clrBlue)  # Color of symbols line 1
InpColor2 = _input('InpColor2', clrRed)  # Color of symbols line 2
InpColor3 = _input('InpColor3', clrGreen)  # Color of symbols line 3
InpColor4 = _input('InpColor4', clrNavy)  # Color of symbols line 4
InpColor5 = _input('InpColor5', clrCyan)  # Color of symbols line 5
InpColor6 = _input('InpColor6', clrMagenta)  # Color of symbols line 6
InpColor7 = _input('InpColor7', clrGold)  # Color of symbols line 7
InpColor8 = _input('InpColor8', clrTomato)  # Color of symbols line 8
period = 0

class SDataMA(MqlObject):
    _q_fields = ('symbol_name', 'line_color', 'handle', 'use_flag', 'point', 'BufferTMP', 'BufferMA')
    def __init__(self, *args):
        self.symbol_name = ""
        self.line_color = 0
        self.handle = 0
        self.use_flag = False
        self.point = 0.0
        self.BufferTMP = Arr(0, 0.0)
        self.BufferMA = Arr(0, 0.0)

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    ArrayResize(DataMA, 8)
    DataMA[0].symbol_name = InpSymbol1
    DataMA[0].line_color = InpColor1
    DataMA[1].symbol_name = InpSymbol2
    DataMA[1].line_color = InpColor2
    DataMA[2].symbol_name = InpSymbol3
    DataMA[2].line_color = InpColor3
    DataMA[3].symbol_name = InpSymbol4
    DataMA[3].line_color = InpColor4
    DataMA[4].symbol_name = InpSymbol5
    DataMA[4].line_color = InpColor5
    DataMA[5].symbol_name = InpSymbol6
    DataMA[5].line_color = InpColor6
    DataMA[6].symbol_name = InpSymbol7
    DataMA[6].line_color = InpColor7
    DataMA[7].symbol_name = InpSymbol8
    DataMA[7].line_color = InpColor8
    IndicatorSetString(INDICATOR_SHORTNAME, 'Multi symbols(' + _str(period) + ')')
    for i in range(0, 8):
        SetIndexBuffer(i, DataMA[i].BufferMA, INDICATOR_DATA)
        SetIndexBuffer(i + 8, DataMA[i].BufferTMP, INDICATOR_CALCULATIONS)
        PlotIndexSetString(i, PLOT_LABEL, DataMA[i].symbol_name)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, DataMA[i].line_color)
        ArraySetAsSeries(DataMA[i].BufferMA, True)
        ArraySetAsSeries(DataMA[i].BufferTMP, True)
        DataMA[i].use_flag = True
        if not _bool(SymbolInfoInteger(DataMA[i].symbol_name, SYMBOL_SELECT)):
            if not SymbolSelect(DataMA[i].symbol_name, True):
                Print('Could not select ', DataMA[i].symbol_name, ' in MarketWatch')
                DataMA[i].use_flag = False
                continue
        DataMA[i].point = SymbolInfoDouble(DataMA[i].symbol_name, SYMBOL_POINT)
        if DataMA[i].use_flag:
            DataMA[i].handle = iMA(DataMA[i].symbol_name, PERIOD_CURRENT, period, 0, InpMethod, InpPrice)
        if DataMA[i].handle == INVALID_HANDLE:
            Print('Error creating MA', i, ' handle for ', DataMA[i].symbol_name)
            return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period + 1):
        return 0
    limit = rates_total - prev_calculated
    total = 0
    if limit > 1:
        limit = rates_total - 2
        total = _uchar(ArraySize(DataMA))
        for i in range(0, total):
            ArrayInitialize(DataMA[i].BufferMA, EMPTY_VALUE)
            ArrayInitialize(DataMA[i].BufferTMP, EMPTY_VALUE)
            copied = CopyBuffer(DataMA[i].handle, 0, 0, rates_total, DataMA[i].BufferTMP)
    for i in range(limit, 0 - 1, -1):
        total = _uchar(ArraySize(DataMA))
        for j in range(0, total):
            if BarsCalculated(DataMA[j].handle) < 0:
                return 0
            if CopyBuffer(DataMA[j].handle, 0, 0, (1 if (limit == 0) else (limit + 1)), DataMA[j].BufferTMP) < 0:
                continue
            if DataMA[j].point > 0:
                DataMA[j].BufferMA[i] = _fdiv(DataMA[j].BufferTMP[i] - DataMA[j].BufferTMP[i + 1], DataMA[j].point) - (j * InpShift)
    return rates_total

# ---- global variables initialised from expressions
DataMA = Arr(0, 0, factory=SDataMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiSymbols(_MQL5Indicator):
    name = 'MultiSymbols'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 1,  # Period of MA
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Calculation method
        'InpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpShift': 1000,  # Vertical shift
    }

