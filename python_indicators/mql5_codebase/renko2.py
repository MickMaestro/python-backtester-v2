"""renko2 — converted from MQL5: MQL5 Indicators/Renko 2.0/renko2.mq5

Renko 2.0, A complete Renko indicator
Copyright: Copyright 2018, Guilherme Santos.; Link: www.facebook.com/RenkoCharts2; Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: CustomRatesDelete, CustomRatesReplace, CustomRatesUpdate, CustomSymbolCreate, CustomSymbolDelete, CustomSymbolSetDouble, CustomSymbolSetInteger, CustomSymbolSetString, CustomTicksAdd, CustomTicksReplace
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Guilherme Santos.', 'link': 'www.facebook.com/RenkoCharts2', 'version': '2.0', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 17}, 'colors': {1: [16777215, 255, 16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Renko Open;Renko High;Renko Low;Renko Close', 2: 'Tick Volume', 3: 'Volume', 4: 'Real Time'}, 'levels': [], 'description': ['Renko 2.0, A complete Renko indicator'], 'name': 'renko2', 'source': 'MQL5 Indicators/Renko 2.0/renko2.mq5', 'folder': 'Renko 2.0', 'inputs': [{'mql': 'RenkoType', 'py': 'RenkoType', 'param': 'RenkoType', 'type': 'int', 'default': 0, 'label': 'Type', 'sinput': False}, {'mql': 'RenkoSize', 'py': 'RenkoSize', 'param': 'RenkoSize', 'type': 'double', 'default': 20.0, 'label': 'Brick Size (Ticks, Pips or Points)', 'sinput': False}, {'mql': 'RenkoWicks', 'py': 'RenkoWicks', 'param': 'RenkoWicks', 'type': 'bool', 'default': True, 'label': 'Show Wicks', 'sinput': False}, {'mql': 'RenkoTime', 'py': 'RenkoTime', 'param': 'RenkoTime', 'type': 'bool', 'default': True, 'label': 'Brick Open Time', 'sinput': False}, {'mql': 'RenkoAsymetricReversal', 'py': 'RenkoAsymetricReversal', 'param': 'RenkoAsymetricReversal', 'type': 'bool', 'default': False, 'label': 'Asymetric Reversals', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

COPY_TICKS_ALL = 0  # MQL5 constant unknown to the converter
MQL5_DEBUG = 0  # MQL5 constant unknown to the converter
MQL5_DEBUGGING = 0  # MQL5 constant unknown to the converter
MQL5_OPTIMIZATION = 0  # MQL5 constant unknown to the converter
MQL5_TESTER = 0  # MQL5 constant unknown to the converter
MQL5_VISUAL_MODE = 0  # MQL5 constant unknown to the converter
SYMBOL_BACKGROUND_COLOR = 0  # MQL5 constant unknown to the converter
SYMBOL_CHART_MODE = 0  # MQL5 constant unknown to the converter
SYMBOL_CUSTOM = 0  # MQL5 constant unknown to the converter
SYMBOL_EXPIRATION_TIME = 0  # MQL5 constant unknown to the converter
SYMBOL_FORMULA = 0  # MQL5 constant unknown to the converter
SYMBOL_MARGIN_HEDGED = 0  # MQL5 constant unknown to the converter
SYMBOL_MARGIN_HEDGED_USE_LEG = 0  # MQL5 constant unknown to the converter
SYMBOL_MARGIN_MAINTENANCE = 0  # MQL5 constant unknown to the converter
SYMBOL_OPTION_MODE = 0  # MQL5 constant unknown to the converter
SYMBOL_OPTION_RIGHT = 0  # MQL5 constant unknown to the converter
SYMBOL_OPTION_STRIKE = 0  # MQL5 constant unknown to the converter
SYMBOL_ORDER_GTC_MODE = 0  # MQL5 constant unknown to the converter
SYMBOL_PAGE = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_PRICE_LIMIT_MAX = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_PRICE_LIMIT_MIN = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_PRICE_SETTLEMENT = 0  # MQL5 constant unknown to the converter
SYMBOL_START_TIME = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_MODE = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_ROLLOVER3DAYS = 0  # MQL5 constant unknown to the converter
SYMBOL_TICKS_BOOKDEPTH = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_ACCRUED_INTEREST = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_FACE_VALUE = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_LIQUIDITY_RATE = 0  # MQL5 constant unknown to the converter
SYMBOL_VOLUME_LIMIT = 0  # MQL5 constant unknown to the converter

# enum ENUM_RENKO_TYPE
RENKO_TYPE_TICKS = 0
RENKO_TYPE_PIPS = 1
RENKO_TYPE_POINTS = 2
RENKO_TYPE_R = 3
_enum('ENUM_RENKO_TYPE', {0: 'RENKO_TYPE_TICKS', 1: 'RENKO_TYPE_PIPS', 2: 'RENKO_TYPE_POINTS', 3: 'RENKO_TYPE_R'})

# enum ENUM_RENKO_WINDOW
RENKO_NO_WINDOW = 0
RENKO_CURRENT_WINDOW = 1
RENKO_NEW_WINDOW = 2
RENKO_MINI_CHART = 3
_enum('ENUM_RENKO_WINDOW', {0: 'RENKO_NO_WINDOW', 1: 'RENKO_CURRENT_WINDOW', 2: 'RENKO_NEW_WINDOW', 3: 'RENKO_MINI_CHART'})

# ---- inputs and global variables
RenkoType = _input('RenkoType', RENKO_TYPE_TICKS)  # Type
RenkoSize = _input('RenkoSize', 20.0)  # Brick Size (Ticks, Pips or Points)
RenkoWicks = _input('RenkoWicks', True)  # Show Wicks
RenkoTime = _input('RenkoTime', True)  # Brick Open Time
RenkoAsymetricReversal = _input('RenkoAsymetricReversal', False)  # Asymetric Reversals
open_buffer = Arr(0, 0.0)
high_buffer = Arr(0, 0.0)
low_buffer = Arr(0, 0.0)
close_buffer = Arr(0, 0.0)
color_buffer = Arr(0, 0.0)
tick_volume_buffer = Arr(0, 0.0)
real_volume_buffer = Arr(0, 0.0)
time_buffer = Arr(0, 0.0)
RenkoOffline = None

class SYMBOL(MqlObject):
    _q_fields = ('Name',)
    def __init__(self, Symb=None, Path=None):
        self.Name = ""
        self.Name = (Symbol() if (Symb == "") else Symb)
        if not SYMBOL.SymbolIsExist(self.Name):
            _missing('CustomSymbolCreate')(self.Name, Path)
    @staticmethod
    def SymbolIsExist(Symb=None):
        ResetLastError()
        SymbolInfoInteger((Symbol() if (Symb == "") else Symb), SYMBOL_CUSTOM)
        return GetLastError() != ERR_MARKET_UNKNOWN_SYMBOL
    def SetProperty_1(self, Property, Value):
        return _bool(_missing('CustomSymbolSetDouble')(self.Name, Property, Value))
    def SetProperty_2(self, Property, Value):
        return _bool(_missing('CustomSymbolSetInteger')(self.Name, Property, Value))
    def SetProperty_3(self, Property, Value):
        return _bool(_missing('CustomSymbolSetString')(self.Name, Property, Value))
    def GetProperty_1(self, Property):
        return SymbolInfoInteger(self.Name, Property)
    def GetProperty_2(self, Property):
        return SymbolInfoDouble(self.Name, Property)
    def GetProperty_3(self, Property):
        return SymbolInfoString(self.Name, Property)
    def Delete(self):
        return (self.IsCustom() and self.Off()) and _bool(_missing('CustomSymbolDelete')(self.Name))
    def CloneProperties(self, Symb=None):
        Source = SYMBOL(Symb)
        return ((((((((((((((((((((((((((((((((((((((((((((((((((SYMBOL.SymbolIsExist(Symb) and self.IsCustom()) and self.SetProperty_2(SYMBOL_BASIS, Source.GetProperty_1(SYMBOL_BASIS))) and self.SetProperty_2(SYMBOL_CURRENCY_BASE, Source.GetProperty_1(SYMBOL_CURRENCY_BASE))) and self.SetProperty_2(SYMBOL_CURRENCY_MARGIN, Source.GetProperty_1(SYMBOL_CURRENCY_MARGIN))) and self.SetProperty_2(SYMBOL_CURRENCY_PROFIT, Source.GetProperty_1(SYMBOL_CURRENCY_PROFIT))) and self.SetProperty_2(SYMBOL_DESCRIPTION, Source.GetProperty_1(SYMBOL_DESCRIPTION))) and self.SetProperty_2(_int(SYMBOL_FORMULA), Source.GetProperty_1(_int(SYMBOL_FORMULA)))) and self.SetProperty_2(SYMBOL_ISIN, Source.GetProperty_1(SYMBOL_ISIN))) and self.SetProperty_2(_int(SYMBOL_PAGE), Source.GetProperty_1(_int(SYMBOL_PAGE)))) and self.SetProperty_2(_int(SYMBOL_MARGIN_HEDGED), Source.GetProperty_1(_int(SYMBOL_MARGIN_HEDGED)))) and self.SetProperty_2(SYMBOL_MARGIN_INITIAL, Source.GetProperty_1(SYMBOL_MARGIN_INITIAL))) and self.SetProperty_2(_int(SYMBOL_MARGIN_MAINTENANCE), Source.GetProperty_1(_int(SYMBOL_MARGIN_MAINTENANCE)))) and self.SetProperty_2(_int(SYMBOL_OPTION_STRIKE), Source.GetProperty_1(_int(SYMBOL_OPTION_STRIKE)))) and self.SetProperty_2(SYMBOL_POINT, Source.GetProperty_1(SYMBOL_POINT))) and self.SetProperty_2(_int(SYMBOL_SESSION_PRICE_LIMIT_MAX), Source.GetProperty_1(_int(SYMBOL_SESSION_PRICE_LIMIT_MAX)))) and self.SetProperty_2(_int(SYMBOL_SESSION_PRICE_LIMIT_MIN), Source.GetProperty_1(_int(SYMBOL_SESSION_PRICE_LIMIT_MIN)))) and self.SetProperty_2(_int(SYMBOL_SESSION_PRICE_SETTLEMENT), Source.GetProperty_1(_int(SYMBOL_SESSION_PRICE_SETTLEMENT)))) and self.SetProperty_2(SYMBOL_SWAP_LONG, Source.GetProperty_1(SYMBOL_SWAP_LONG))) and self.SetProperty_2(SYMBOL_SWAP_SHORT, Source.GetProperty_1(SYMBOL_SWAP_SHORT))) and self.SetProperty_2(_int(SYMBOL_TRADE_ACCRUED_INTEREST), Source.GetProperty_1(_int(SYMBOL_TRADE_ACCRUED_INTEREST)))) and self.SetProperty_2(SYMBOL_TRADE_CONTRACT_SIZE, Source.GetProperty_1(SYMBOL_TRADE_CONTRACT_SIZE))) and self.SetProperty_2(_int(SYMBOL_TRADE_FACE_VALUE), Source.GetProperty_1(_int(SYMBOL_TRADE_FACE_VALUE)))) and self.SetProperty_2(_int(SYMBOL_TRADE_LIQUIDITY_RATE), Source.GetProperty_1(_int(SYMBOL_TRADE_LIQUIDITY_RATE)))) and self.SetProperty_2(SYMBOL_TRADE_TICK_SIZE, Source.GetProperty_1(SYMBOL_TRADE_TICK_SIZE))) and self.SetProperty_2(SYMBOL_TRADE_TICK_VALUE, Source.GetProperty_1(SYMBOL_TRADE_TICK_VALUE))) and self.SetProperty_2(_int(SYMBOL_VOLUME_LIMIT), Source.GetProperty_1(_int(SYMBOL_VOLUME_LIMIT)))) and self.SetProperty_2(SYMBOL_VOLUME_MAX, Source.GetProperty_1(SYMBOL_VOLUME_MAX))) and self.SetProperty_2(SYMBOL_VOLUME_MIN, Source.GetProperty_1(SYMBOL_VOLUME_MIN))) and self.SetProperty_2(SYMBOL_VOLUME_STEP, Source.GetProperty_1(SYMBOL_VOLUME_STEP))) and self.SetProperty_2(_int(SYMBOL_BACKGROUND_COLOR), Source.GetProperty_1(_int(SYMBOL_BACKGROUND_COLOR)))) and self.SetProperty_2(_int(SYMBOL_CHART_MODE), Source.GetProperty_1(_int(SYMBOL_CHART_MODE)))) and self.SetProperty_2(SYMBOL_DIGITS, Source.GetProperty_1(SYMBOL_DIGITS))) and self.SetProperty_2(SYMBOL_EXPIRATION_MODE, Source.GetProperty_1(SYMBOL_EXPIRATION_MODE))) and self.SetProperty_2(_int(SYMBOL_EXPIRATION_TIME), Source.GetProperty_1(_int(SYMBOL_EXPIRATION_TIME)))) and self.SetProperty_2(SYMBOL_FILLING_MODE, Source.GetProperty_1(SYMBOL_FILLING_MODE))) and self.SetProperty_2(_int(SYMBOL_MARGIN_HEDGED_USE_LEG), Source.GetProperty_1(_int(SYMBOL_MARGIN_HEDGED_USE_LEG)))) and self.SetProperty_2(_int(SYMBOL_OPTION_MODE), Source.GetProperty_1(_int(SYMBOL_OPTION_MODE)))) and self.SetProperty_2(_int(SYMBOL_OPTION_RIGHT), Source.GetProperty_1(_int(SYMBOL_OPTION_RIGHT)))) and self.SetProperty_2(_int(SYMBOL_ORDER_GTC_MODE), Source.GetProperty_1(_int(SYMBOL_ORDER_GTC_MODE)))) and self.SetProperty_2(SYMBOL_ORDER_MODE, Source.GetProperty_1(SYMBOL_ORDER_MODE))) and self.SetProperty_2(SYMBOL_SPREAD, Source.GetProperty_1(SYMBOL_SPREAD))) and self.SetProperty_2(SYMBOL_SPREAD_FLOAT, Source.GetProperty_1(SYMBOL_SPREAD_FLOAT))) and self.SetProperty_2(_int(SYMBOL_START_TIME), Source.GetProperty_1(_int(SYMBOL_START_TIME)))) and self.SetProperty_2(_int(SYMBOL_SWAP_MODE), Source.GetProperty_1(_int(SYMBOL_SWAP_MODE)))) and self.SetProperty_2(_int(SYMBOL_SWAP_ROLLOVER3DAYS), Source.GetProperty_1(_int(SYMBOL_SWAP_ROLLOVER3DAYS)))) and self.SetProperty_2(_int(SYMBOL_TICKS_BOOKDEPTH), Source.GetProperty_1(_int(SYMBOL_TICKS_BOOKDEPTH)))) and self.SetProperty_2(SYMBOL_TRADE_CALC_MODE, Source.GetProperty_1(SYMBOL_TRADE_CALC_MODE))) and self.SetProperty_2(SYMBOL_TRADE_EXEMODE, Source.GetProperty_1(SYMBOL_TRADE_EXEMODE))) and self.SetProperty_2(SYMBOL_TRADE_FREEZE_LEVEL, Source.GetProperty_1(SYMBOL_TRADE_FREEZE_LEVEL))) and self.SetProperty_2(SYMBOL_TRADE_MODE, Source.GetProperty_1(SYMBOL_TRADE_MODE))) and self.SetProperty_2(SYMBOL_TRADE_STOPS_LEVEL, Source.GetProperty_1(SYMBOL_TRADE_STOPS_LEVEL))
    def CloneHistory(self, Symb=None):
        return MathMax(self.CloneRates_2(Symb), self.CloneTicks_2(Symb))
    def CloneRates_1(self, Rates):
        return (_missing('CustomRatesReplace')(self.Name, 0, LONG_MAX, Rates) if self.IsCustom() else -1)
    def CloneRates_2(self, Symb=None):
        Res = (0 if (self.IsCustom() and SYMBOL.SymbolIsExist(Symb)) else -1)
        if Res != -1:
            Symb = (Symbol() if (Symb == "") else Symb)
            Rates = Arr(0, 0, factory=MqlRates)
            CopyRates(Symb, PERIOD_M1, 0, Bars(Symb, PERIOD_M1), Rates)
            Res = self.CloneRates_1(Rates)
        return Res
    def CloneTicks_1(self, Ticks):
        return (_missing('CustomTicksReplace')(self.Name, 0, LONG_MAX, Ticks) if self.IsCustom() else -1)
    def CloneTicks_2(self, Symb=None):
        Symb = (Symbol() if (Symb == "") else Symb)
        Res = (0 if (self.IsCustom() and SymbolInfoInteger(Symb, SYMBOL_CUSTOM)) else -1)
        if Res != -1:
            Ticks = Arr(0, 0, factory=MqlTick)
            CopyTicksRange(Symb, Ticks, COPY_TICKS_ALL, 0, LONG_MAX)
            Res = self.CloneTicks_1(Ticks)
        return Res
    def Clone(self, Symb=None):
        return self.CloneProperties(Symb) and self.CloneHistory(Symb) != -1
    def _q_assign(self, Symb):
        return self.Clone(Symb)
    def On(self):
        return SymbolSelect(self.Name, True)
    def Off(self):
        return SymbolSelect(self.Name, False)
    def IsCustom(self):
        return (self.GetProperty_1(_int(SYMBOL_CUSTOM)) != 0)
    def IsExist(self):
        return SYMBOL.SymbolIsExist(self.Name)

class RenkoCharts(MqlObject):
    _q_fields = ('rates', 'renko_buffer', 'renko_symbol', 'custom_symbol', 'renko_size', 'brick_size', 'up_wick', 'down_wick', 'tick_volumes', 'volumes', 'show_wicks', 'open_time', 'asymetric_reversal', 'renko_type')
    def __init__(self):
        self.rates = Arr(0, 0, factory=MqlRates)
        self.renko_buffer = Arr(0, 0, factory=MqlRates)
        self.renko_symbol = ""
        self.custom_symbol = ""
        self.renko_size = 0.0
        self.brick_size = 0.0
        self.up_wick = 0.0
        self.down_wick = 0.0
        self.tick_volumes = 0
        self.volumes = 0
        self.show_wicks = False
        self.open_time = False
        self.asymetric_reversal = False
        self.renko_type = 0
        return
    def _q_dtor(self):
        ArrayFree(self.rates)
        ArrayFree(self.renko_buffer)
        SymbolSelect(self.custom_symbol, False)
        _missing('CustomSymbolDelete')(self.custom_symbol)
    def Setup(self, symbol, type_=RENKO_TYPE_TICKS, size=20.0, wicks=True, times=True, asymetric=False):
        if symbol == '' or symbol == "":
            Print('Line:', 111, ' - Invalid symbol selected.')
            return False
        if SymbolInfoInteger(symbol, SYMBOL_CUSTOM):
            if (((MQL5InfoInteger(MQL5_TESTER) or MQL5InfoInteger(MQL5_DEBUG)) or MQL5InfoInteger(MQL5_DEBUGGING)) or MQL5InfoInteger(MQL5_OPTIMIZATION)) or MQL5InfoInteger(MQL5_VISUAL_MODE):
                pass
            else:
                Print('Line:', 122, ' - Custom Symbol selected. Please Change for the original symbol.')
                return False
        if SymbolSelect(symbol, True) == False:
            Print('Line:', 129, ' - Symbol selection error.')
            return False
        self.renko_symbol = symbol
        self.renko_type = type_
        self.renko_size = size
        self.show_wicks = wicks
        self.open_time = times
        self.asymetric_reversal = asymetric
        digits = _int(SymbolInfoInteger(symbol, SYMBOL_DIGITS))
        points = SymbolInfoDouble(symbol, SYMBOL_POINT)
        tick_size = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
        pip_size = ((points * 10) if (digits == 5 or digits == 3) else points)
        if self.renko_type == RENKO_TYPE_TICKS:
            self.brick_size = self.renko_size * tick_size
        elif self.renko_type == RENKO_TYPE_PIPS:
            self.brick_size = self.renko_size * pip_size
        elif self.renko_type == RENKO_TYPE_R:
            self.brick_size = (self.renko_size * tick_size) - tick_size
        else:
            self.brick_size = self.renko_size
        if self.brick_size <= 0:
            Print('Line:', 151, ' - Invalid brick size. Value of ', self.brick_size, ' selected.')
            return False
        if self.brick_size < tick_size:
            self.brick_size = tick_size
            Print('Line:', 158, ' - Invalid brick size. Minimum value of ', self.brick_size, ' will be used.')
        self.brick_size = NormalizeDouble(self.brick_size, digits)
        return True
    def LoadFrom(self, start=0):
        ResetLastError()
        total = 0
        size = ArraySize(self.renko_buffer)
        if size == 0:
            total = CopyRates(self.renko_symbol, PERIOD_M1, 0, 1000000, self.rates)
        else:
            total = CopyRates(self.renko_symbol, PERIOD_M1, start - 59, _DT(TimeCurrent()), self.rates)
        if total <= 0:
            return 0
        elif total == 1:
            size = self.LoadPrice_1(self.rates[0])
        else:
            for i in range(0, total):
                size = self.LoadPriceOHLC(self.rates[i])
        return size
    def LoadVolumes(self, start, ticks):
        pass
    def UpdateRates(self):
        global _s_RenkoCharts_UpdateRates_last_update
        size = self.LoadFrom(_s_RenkoCharts_UpdateRates_last_update)
        _s_RenkoCharts_UpdateRates_last_update = TimeCurrent()
        return size
    def UpdatePrice(self, price, time, tick_volume, volume, spread):
        pass
    def ClearRates(self):
        return ArrayResize(self.renko_buffer, 0)
    def GetValue(self, buffer=0, index=-1):
        index = ((ArraySize(self.renko_buffer) - 1) if (index < 0) else index)
        if index < 0:
            return EMPTY_VALUE
        _sw1 = buffer
        if _sw1 == 0:
            return float(self.renko_buffer[index].time)
        elif _sw1 == 1:
            return self.renko_buffer[index].open
        elif _sw1 == 2:
            return self.renko_buffer[index].high
        elif _sw1 == 3:
            return self.renko_buffer[index].low
        elif _sw1 == 4:
            return self.renko_buffer[index].close
        elif _sw1 == 5:
            return float(self.renko_buffer[index].tick_volume)
        elif _sw1 == 6:
            return float(self.renko_buffer[index].real_volume)
        elif _sw1 == 7:
            return float(self.renko_buffer[index].spread)
        elif _sw1 == 8:
            return (1 if (self.renko_buffer[index].open < self.renko_buffer[index].close) else 0 if (self.renko_buffer[index].open == self.renko_buffer[index].close) else -1)
        else:
            return EMPTY_VALUE
    def GetValueAsSeries(self, buffer=0, index=-1):
        index = ArraySize(self.renko_buffer) - index
        index = ((ArraySize(self.renko_buffer) - 1) if (index <= 0) else (index - 1))
        if index < 0:
            return EMPTY_VALUE
        _sw2 = buffer
        if _sw2 == 0:
            return float(self.renko_buffer[index].time)
        elif _sw2 == 1:
            return self.renko_buffer[index].open
        elif _sw2 == 2:
            return self.renko_buffer[index].high
        elif _sw2 == 3:
            return self.renko_buffer[index].low
        elif _sw2 == 4:
            return self.renko_buffer[index].close
        elif _sw2 == 5:
            return float(self.renko_buffer[index].tick_volume)
        elif _sw2 == 6:
            return float(self.renko_buffer[index].real_volume)
        elif _sw2 == 7:
            return float(self.renko_buffer[index].spread)
        elif _sw2 == 8:
            return (1 if (self.renko_buffer[index].open < self.renko_buffer[index].close) else 0 if (self.renko_buffer[index].open == self.renko_buffer[index].close) else -1)
        else:
            return EMPTY_VALUE
    def GetSymbolName(self):
        return self.custom_symbol
    def CreateCustomSymbol(self, name=''):
        self.custom_symbol = name
        if name == '' or name == "":
            sufix = StringFormat('%g', self.renko_size)
            if self.renko_type == RENKO_TYPE_TICKS:
                sufix += 'TICKS'
            elif self.renko_type == RENKO_TYPE_PIPS:
                sufix += 'PIPS'
            elif self.renko_type == RENKO_TYPE_R:
                sufix += 'R'
            else:
                sufix += 'POINTS'
            self.custom_symbol = self.renko_symbol + '_' + sufix
        Symb = SYMBOL(self.custom_symbol, 'RenkoCharts')
        Symb.CloneProperties(self.renko_symbol)
        Symb.On()
        if SymbolSelect(self.custom_symbol, True) == False:
            Print('Custom Symbol selection error.')
        return
    def CheckCustomSymbol(self):
        if self.custom_symbol == '' or self.custom_symbol == "":
            return False
        return (SymbolInfoInteger(self.custom_symbol, SYMBOL_CUSTOM) != 0)
    def ClearCustomSymbol(self):
        if not self.CheckCustomSymbol():
            return 0
        return _int(_missing('CustomRatesDelete')(self.custom_symbol, 0, 32535129600))
    def ReplaceCustomSymbol(self):
        if not self.CheckCustomSymbol():
            return 0
        return _int(_missing('CustomRatesUpdate')(self.custom_symbol, self.renko_buffer))
    def OpenCustomSymbol(self):
        if not self.CheckCustomSymbol():
            return -1
        chart_id = ChartOpen(self.custom_symbol, PERIOD_M1)
        ChartSetInteger(chart_id, CHART_MODE, CHART_CANDLES)
        ChartSetInteger(chart_id, CHART_SHOW_PERIOD_SEP, 0, True)
        ChartSetInteger(chart_id, CHART_SHOW_GRID, 0, False)
        return chart_id
    def SetCustomSymbol(self, chart_id=0):
        if not self.CheckCustomSymbol():
            return
        ChartSetSymbolPeriod(chart_id, self.custom_symbol, PERIOD_M1)
        ChartSetInteger(chart_id, CHART_MODE, CHART_CANDLES)
        ChartSetInteger(chart_id, CHART_SHOW_PERIOD_SEP, 0, True)
        ChartSetInteger(chart_id, CHART_SHOW_GRID, 0, False)
    def ValidateSymbol(self, name):
        if name.v == '' or name.v == "":
            name.v = Symbol()
        if SymbolInfoInteger(name.v, SYMBOL_CUSTOM):
            new_name = StringAt(name.v, '_')
            if SymbolInfoInteger(new_name, SYMBOL_CUSTOM):
                return False
            else:
                name.v = new_name
        return True
    def UpdateCustomRates(self, count=0):
        if not self.CheckCustomSymbol():
            return 0
        update_buffer = Arr(0, 0, factory=MqlRates)
        ArraySetAsSeries(update_buffer, True)
        if count <= 0:
            count = WHOLE_ARRAY
        copied = ArrayCopy(update_buffer, self.renko_buffer, 0, 0, count)
        if copied <= 0:
            return 0
        copied = _int(_missing('CustomRatesUpdate')(self.custom_symbol, update_buffer))
        return copied
    def UpdateCustomTick(self):
        global _s_RenkoCharts_UpdateCustomTick_last_tick
        if not self.CheckCustomSymbol():
            return 0
        update_buffer = Arr(0, 0, factory=MqlTick)
        ArraySetAsSeries(update_buffer, True)
        copied = CopyTicks(self.renko_symbol, update_buffer, COPY_TICKS_ALL, 0, 1)
        if copied <= 0:
            return 0
        if _s_RenkoCharts_UpdateCustomTick_last_tick != update_buffer[0].time_msc:
            _s_RenkoCharts_UpdateCustomTick_last_tick = update_buffer[0].time_msc
        else:
            return 0
        update_buffer[0].time_msc = 1000 * _long(self.GetValue(0))
        if update_buffer[0].bid == 0:
            update_buffer[0].bid = self.GetValue(4)
        if update_buffer[0].ask == 0:
            update_buffer[0].ask = self.GetValue(4)
        if update_buffer[0].last == 0:
            update_buffer[0].last = self.GetValue(4)
        copied = _int(_missing('CustomTicksAdd')(self.custom_symbol, update_buffer))
        return copied
    def Start(self, window=RENKO_NO_WINDOW, event_timer=0, event_book=False):
        Print('Updating Custom Symbol: ', self.custom_symbol)
        if window == RENKO_NEW_WINDOW:
            Comment('Updating Custom Symbol: ', self.custom_symbol)
            self.OpenCustomSymbol()
        elif window == RENKO_CURRENT_WINDOW:
            self.SetCustomSymbol()
        elif window == RENKO_MINI_CHART:
            self.MiniChartCustomSymbol()
        if event_timer > 0:
            EventSetMillisecondTimer(event_timer)
        if event_book:
            MarketBookAdd(self.renko_symbol)
    def Stop(self):
        Comment('')
        MarketBookRelease(self.renko_symbol)
        ObjectDelete(0, self.custom_symbol)
        SymbolSelect(self.custom_symbol, False)
        _missing('CustomSymbolDelete')(self.custom_symbol)
    def Refresh(self):
        global _s_RenkoCharts_Refresh_last_size, _s_RenkoCharts_Refresh_last_update
        size = self.UpdateRates()
        if _s_RenkoCharts_Refresh_last_size == 0:
            self.ReplaceCustomSymbol()
        if _s_RenkoCharts_Refresh_last_size != size:
            if (TimeCurrent() - _s_RenkoCharts_Refresh_last_update) > 60:
                self.ReplaceCustomSymbol()
            else:
                self.UpdateCustomRates(_s_RenkoCharts_Refresh_last_size - size)
        self.UpdateCustomTick()
        _s_RenkoCharts_Refresh_last_update = TimeCurrent()
        _s_RenkoCharts_Refresh_last_size = size
    def AddOne(self, time=0):
        index = ArrayResize(self.renko_buffer, ArraySize(self.renko_buffer) + 1, 100000) - 1
        if index <= 0:
            return 0
        if time == 0:
            time = TimeCurrent()
        if not self.open_time:
            time = time - _imod(time, 86400)
        if time <= self.renko_buffer[index - 1].time:
            self.renko_buffer[index].time = self.renko_buffer[index - 1].time + 60
        else:
            self.renko_buffer[index].time = time
        self.renko_buffer[index].close = self.renko_buffer[index - 1].close
        self.renko_buffer[index].low = self.renko_buffer[index].close
        self.renko_buffer[index].high = self.renko_buffer[index].low
        self.renko_buffer[index].open = self.renko_buffer[index].high
        self.renko_buffer[index].real_volume = 0
        self.renko_buffer[index].tick_volume = self.renko_buffer[index].real_volume
        self.renko_buffer[index].spread = 0
        return index
    def CloseUp(self, points, time=0, spread=0):
        index = ArraySize(self.renko_buffer) - 1
        if self.asymetric_reversal:
            self.renko_buffer[index].open = self.renko_buffer[index - 1].close
        else:
            self.renko_buffer[index].open = self.renko_buffer[index - 1].close + points - self.brick_size
        self.renko_buffer[index].high = self.renko_buffer[index - 1].close + points
        self.renko_buffer[index].close = self.renko_buffer[index - 1].close + points
        if self.show_wicks:
            self.renko_buffer[index].low = self.down_wick
        else:
            self.renko_buffer[index].low = self.renko_buffer[index].open
        self.down_wick = self.renko_buffer[index].close
        self.up_wick = self.down_wick
        self.renko_buffer[index].tick_volume = self.tick_volumes
        self.renko_buffer[index].real_volume = self.volumes
        self.renko_buffer[index].spread = spread
        self.volumes = 0
        self.tick_volumes = self.volumes
        return self.AddOne(time)
    def CloseDown(self, points, time=0, spread=0):
        index = ArraySize(self.renko_buffer) - 1
        if self.asymetric_reversal:
            self.renko_buffer[index].open = self.renko_buffer[index - 1].close
        else:
            self.renko_buffer[index].open = self.renko_buffer[index - 1].close - points + self.brick_size
        self.renko_buffer[index].low = self.renko_buffer[index - 1].close - points
        self.renko_buffer[index].close = self.renko_buffer[index - 1].close - points
        if self.show_wicks:
            self.renko_buffer[index].high = self.up_wick
        else:
            self.renko_buffer[index].high = self.renko_buffer[index].open
        self.down_wick = self.renko_buffer[index].close
        self.up_wick = self.down_wick
        self.renko_buffer[index].tick_volume = self.tick_volumes
        self.renko_buffer[index].real_volume = self.volumes
        self.renko_buffer[index].spread = spread
        self.volumes = 0
        self.tick_volumes = self.volumes
        return self.AddOne(time)
    def LoadPrice_5(self, price, time=0, tick_volume=0, volume=0, spread=0):
        global _s_RenkoCharts_LoadPrice_last_tick_volume, _s_RenkoCharts_LoadPrice_last_time, _s_RenkoCharts_LoadPrice_last_volume
        if time == 0:
            time = TimeCurrent()
        size = ArraySize(self.renko_buffer)
        index = size - 1
        if size == 0:
            ArrayResize(self.renko_buffer, 2, 1000)
            self.renko_buffer[1].time = time - 60
            self.renko_buffer[1].high = NormalizeDouble(MathFloor(_fdiv(price, self.brick_size)) * self.brick_size, Digits())
            self.renko_buffer[1].close = self.renko_buffer[1].high
            self.renko_buffer[1].low = self.renko_buffer[1].close - self.brick_size
            self.renko_buffer[1].open = self.renko_buffer[1].low
            self.renko_buffer[1].real_volume = 0
            self.renko_buffer[1].tick_volume = self.renko_buffer[1].real_volume
            self.renko_buffer[1].spread = 0
            self.renko_buffer[0].time = time - 120
            self.renko_buffer[0].low = self.renko_buffer[1].open - self.brick_size
            self.renko_buffer[0].open = self.renko_buffer[0].low
            self.renko_buffer[0].close = self.renko_buffer[1].open
            self.renko_buffer[0].high = self.renko_buffer[0].close
            self.renko_buffer[0].real_volume = 0
            self.renko_buffer[0].tick_volume = self.renko_buffer[0].real_volume
            self.renko_buffer[0].spread = 0
            index = self.AddOne(time)
        if time != _s_RenkoCharts_LoadPrice_last_time:
            _s_RenkoCharts_LoadPrice_last_time = time
            self.tick_volumes += _s_RenkoCharts_LoadPrice_last_tick_volume
            self.volumes += _s_RenkoCharts_LoadPrice_last_volume
        _s_RenkoCharts_LoadPrice_last_tick_volume = tick_volume
        _s_RenkoCharts_LoadPrice_last_volume = volume
        self.up_wick = MathMax(self.up_wick, price)
        self.down_wick = MathMin(self.down_wick, price)
        if self.down_wick <= 0:
            self.down_wick = price
        if self.renko_type == RENKO_TYPE_R:
            if self.renko_buffer[index - 1].close > self.renko_buffer[index - 2].close:
                if price > (self.renko_buffer[index - 1].close + self.brick_size):
                    while price > (self.renko_buffer[index - 1].close + self.brick_size):
                        index = self.CloseUp(self.brick_size, time, spread)
                elif price < (self.renko_buffer[index - 1].close - (self.brick_size * 2.0)):
                    index = self.CloseDown(self.brick_size * 2.0, time, spread)
                    while price < (self.renko_buffer[index - 1].close - self.brick_size):
                        index = self.CloseDown(self.brick_size, time, spread)
            if self.renko_buffer[index - 1].close < self.renko_buffer[index - 2].close:
                if price < (self.renko_buffer[index - 1].close - self.brick_size):
                    while price < (self.renko_buffer[index - 1].close - self.brick_size):
                        index = self.CloseDown(self.brick_size, time, spread)
                elif price > (self.renko_buffer[index - 1].close + (self.brick_size * 2.0)):
                    index = self.CloseUp(self.brick_size * 2.0, time, spread)
                    while price > (self.renko_buffer[index - 1].close + self.brick_size):
                        index = self.CloseUp(self.brick_size, time, spread)
        else:
            if self.renko_buffer[index - 1].close >= self.renko_buffer[index - 2].close:
                if price >= (self.renko_buffer[index - 1].close + self.brick_size):
                    while price >= (self.renko_buffer[index - 1].close + self.brick_size):
                        index = self.CloseUp(self.brick_size, time, spread)
                elif price <= (self.renko_buffer[index - 1].close - (self.brick_size * 2.0)):
                    index = self.CloseDown(self.brick_size * 2.0, time, spread)
                    while price <= (self.renko_buffer[index - 1].close - self.brick_size):
                        index = self.CloseDown(self.brick_size, time, spread)
            if self.renko_buffer[index - 1].close <= self.renko_buffer[index - 2].close:
                if price <= (self.renko_buffer[index - 1].close - self.brick_size):
                    while price <= (self.renko_buffer[index - 1].close - self.brick_size):
                        index = self.CloseDown(self.brick_size, time, spread)
                elif price >= (self.renko_buffer[index - 1].close + (self.brick_size * 2.0)):
                    index = self.CloseUp(self.brick_size * 2.0, time, spread)
                    while price >= (self.renko_buffer[index - 1].close + self.brick_size):
                        index = self.CloseUp(self.brick_size, time, spread)
        self.renko_buffer[index].open = self.renko_buffer[index - 1].close
        self.renko_buffer[index].high = self.up_wick
        self.renko_buffer[index].low = self.down_wick
        self.renko_buffer[index].close = price
        self.renko_buffer[index].tick_volume = self.tick_volumes + tick_volume
        self.renko_buffer[index].real_volume = self.volumes + volume
        self.renko_buffer[index].spread = spread
        return index + 1
    def LoadPrice_1(self, price):
        return self.LoadPrice_5(price.close, price.time, price.tick_volume, price.real_volume, price.spread)
    def LoadPriceOHLC(self, price):
        self.LoadPrice_5(price.open, price.time, 0, 0, price.spread)
        if price.close > price.open:
            self.LoadPrice_5(price.low, price.time, 0, 0, price.spread)
            self.LoadPrice_5(price.high, price.time, 0, 0, price.spread)
        else:
            self.LoadPrice_5(price.high, price.time, 0, 0, price.spread)
            self.LoadPrice_5(price.low, price.time, 0, 0, price.spread)
        return self.LoadPrice_5(price.close, price.time, price.tick_volume, price.real_volume, price.spread)
    def MiniChartCustomSymbol(self):
        ObjectCreate(0, self.custom_symbol, OBJ_CHART, 0, 0, 0)
        ObjectSetString(0, self.custom_symbol, OBJPROP_SYMBOL, self.custom_symbol)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_XDISTANCE, 0)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_YDISTANCE, 200)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_XSIZE, 300)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_YSIZE, 200)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_CORNER, CORNER_LEFT_LOWER)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_PERIOD, PERIOD_M1)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_CHART_SCALE, 3)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_DATE_SCALE, False)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_BACK, False)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_SELECTED, False)
        ObjectSetInteger(0, self.custom_symbol, OBJPROP_HIDDEN, True)

def StringAt(text, separator, position=0):
    result = Arr(0, "")
    s = StringGetCharacter(separator, 0)
    n = StringSplit(text, s, result)
    if position < n:
        return result[position]
    else:
        return ''

def OnInit():
    global RenkoOffline
    SetIndexBuffer(0, open_buffer, INDICATOR_DATA)
    SetIndexBuffer(1, high_buffer, INDICATOR_DATA)
    SetIndexBuffer(2, low_buffer, INDICATOR_DATA)
    SetIndexBuffer(3, close_buffer, INDICATOR_DATA)
    SetIndexBuffer(4, color_buffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, tick_volume_buffer, INDICATOR_DATA)
    SetIndexBuffer(6, real_volume_buffer, INDICATOR_DATA)
    SetIndexBuffer(7, time_buffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if RenkoOffline is None:
        if (RenkoOffline := RenkoCharts()) is None:
            MessageBox('Renko create class error. Check error log!', 'renko2.mq5', MB_OK)
            return INIT_FAILED
    if not RenkoOffline.Setup(Symbol(), RenkoType, RenkoSize, RenkoWicks, RenkoTime, RenkoAsymetricReversal):
        MessageBox('Renko setup error. Check error log!', 'renko2.mq5', MB_OK)
        return INIT_FAILED
    RenkoOffline.UpdateRates()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    global RenkoOffline
    if RenkoOffline is not None:
        RenkoOffline.Stop()
        _delete(RenkoOffline)
        RenkoOffline = None

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_prev_total
    index = rates_total - 1
    total = RenkoOffline.UpdateRates()
    if total <= 0:
        return 0
    if rates_total != prev_calculated or total != _s_OnCalculate_prev_total:
        i = index
        j = total - 1
        while i > 0 and j > 0:
            open_buffer[i] = RenkoOffline.GetValue(1, j)
            high_buffer[i] = RenkoOffline.GetValue(2, j)
            low_buffer[i] = RenkoOffline.GetValue(3, j)
            close_buffer[i] = RenkoOffline.GetValue(4, j)
            close_buffer[i - 1] = RenkoOffline.GetValue(4, j - 1)
            tick_volume_buffer[i] = RenkoOffline.GetValue(5, j)
            real_volume_buffer[i] = RenkoOffline.GetValue(6, j)
            time_buffer[i] = RenkoOffline.GetValue(0, j)
            if tick_volume_buffer[i] == 0:
                color_buffer[i] = 0.0
            elif close_buffer[i] > close_buffer[i - 1]:
                color_buffer[i] = 2.0
            else:
                color_buffer[i] = 1.0
            i -= 1
            j -= 1
    _s_OnCalculate_prev_total = total
    open_buffer[index] = RenkoOffline.GetValue(1, total - 1)
    high_buffer[index] = RenkoOffline.GetValue(2, total - 1)
    low_buffer[index] = RenkoOffline.GetValue(3, total - 1)
    close_buffer[index] = RenkoOffline.GetValue(4, total - 1)
    color_buffer[index] = color_buffer[index - 1]
    tick_volume_buffer[index] = RenkoOffline.GetValue(5, total - 1)
    real_volume_buffer[index] = RenkoOffline.GetValue(6, total - 1)
    time_buffer[index] = RenkoOffline.GetValue(0, total - 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, price[index])
    return rates_total

# ---- static local variables
_s_RenkoCharts_UpdateRates_last_update = 0
_s_RenkoCharts_UpdateCustomTick_last_tick = 0
_s_RenkoCharts_Refresh_last_update = 0
_s_RenkoCharts_Refresh_last_size = 0
_s_RenkoCharts_LoadPrice_last_time = 0
_s_RenkoCharts_LoadPrice_last_tick_volume = 0
_s_RenkoCharts_LoadPrice_last_volume = 0
_s_OnCalculate_prev_total = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Renko2(_MQL5Indicator):
    name = 'renko2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RenkoType': _Choice({0: 'Ticks', 1: 'Pips', 2: 'Points', 3: 'R Type (-1 Tick)'}, default=0),  # Type
        'RenkoSize': 20.0,  # Brick Size (Ticks, Pips or Points)
        'RenkoWicks': True,  # Show Wicks
        'RenkoTime': True,  # Brick Open Time
        'RenkoAsymetricReversal': False,  # Asymetric Reversals
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

