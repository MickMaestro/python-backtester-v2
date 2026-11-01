"""Elliott_Wave_Oscillator_Sign — converted from MQL5: MQL5 Indicators/Elliott_Wave_Oscillator_HTF_Signal/Elliott_Wave_Oscillator_Sign.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Elliott_Wave_Oscillator Sell', 2: 'Elliott_Wave_Oscillator Buy'}, 'levels': [], 'description': [], 'name': 'Elliott_Wave_Oscillator_Sign', 'source': 'MQL5 Indicators/Elliott_Wave_Oscillator_HTF_Signal/Elliott_Wave_Oscillator_Sign.mq5', 'folder': 'Elliott_Wave_Oscillator_HTF_Signal', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'Алгоритм определения сигнала', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения первого мувинга', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 5, 'label': 'Глубина усреднения первого мувинга', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого мувинга,', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 5, 'label': 'Ценовая константа первого мувинга', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Метод усреднения второго мувинга', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 35, 'label': 'Глубина усреднения второго мувинга', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Параметр второго мувинга,', 'sinput': False}, {'mql': 'IPC2', 'py': 'IPC2', 'param': 'IPC2', 'type': 'int', 'default': 5, 'label': 'Ценовая константа второго мувинга', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Sign', 'py': 'Sign', 'param': 'Sign', 'type': 'bool', 'default': True, 'label': 'Подача одноразового звукового сигнала при появлении стрелки на закрытом баре', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# enum ENUM_MODE
MODE1 = 1
MODE2 = 2
_enum('ENUM_MODE', {1: 'MODE1', 2: 'MODE2'})

# ---- inputs and global variables
Mode = _input('Mode', MODE1)  # Алгоритм определения сигнала
MA_Method1 = _input('MA_Method1', MODE_SMA_)  # Метод усреднения первого мувинга
Length1 = _input('Length1', 5)  # Глубина усреднения первого мувинга
Phase1 = _input('Phase1', 15)  # Параметр первого мувинга,
IPC1 = _input('IPC1', PRICE_MEDIAN_)  # Ценовая константа первого мувинга
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Метод усреднения второго мувинга
Length2 = _input('Length2', 35)  # Глубина усреднения второго мувинга
Phase2 = _input('Phase2', 15)  # Параметр второго мувинга,
IPC2 = _input('IPC2', PRICE_MEDIAN_)  # Ценовая константа второго мувинга
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Sign = _input('Sign', True)  # Подача одноразового звукового сигнала при появлении стрелки на закрытом баре
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = MathMax(GetStartBars(MA_Method1, Length1, Phase1), GetStartBars(MA_Method2, Length2, Phase2)) + 3
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'Elliott_Wave_Oscillator(', Length1, ',', Length2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ewo_prev, _s_OnCalculate_ewo_prev_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    price = 0.0
    x1xma = 0.0
    x2xma = 0.0
    ewo = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_ewo_prev = 0.0
        _s_OnCalculate_ewo_prev_prev = 0.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC1, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price, bar, False)
        price = PriceSeries(IPC2, bar, open, low, high, close)
        x2xma = XMA2.XMASeries(0, prev_calculated, rates_total, MA_Method2, Phase2, Length2, price, bar, False)
        ewo = x1xma - x2xma
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if Mode == MODE1:
            if _s_OnCalculate_ewo_prev_prev > _s_OnCalculate_ewo_prev and _s_OnCalculate_ewo_prev < ewo:
                if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                    return 0
                BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
                if Sign and bar == (rates_total - 2):
                    PlaySound('alert.wav')
            if _s_OnCalculate_ewo_prev_prev < _s_OnCalculate_ewo_prev and _s_OnCalculate_ewo_prev > ewo:
                if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                    return 0
                SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
                if Sign and bar == (rates_total - 2):
                    PlaySound('alert.wav')
        if Mode == MODE2:
            if _s_OnCalculate_ewo_prev < 0.0 and ewo > 0.0:
                if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                    return 0
                BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
                if Sign and bar == (rates_total - 2):
                    PlaySound('alert.wav')
            if _s_OnCalculate_ewo_prev > 0.0 and ewo < 0.0:
                if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                    return 0
                SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
                if Sign and bar == (rates_total - 2):
                    PlaySound('alert.wav')
        if bar < (rates_total - 1):
            _s_OnCalculate_ewo_prev_prev = _s_OnCalculate_ewo_prev
            _s_OnCalculate_ewo_prev = ewo
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_ewo_prev = 0.0
_s_OnCalculate_ewo_prev_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ElliottWaveOscillatorSign(_MQL5Indicator):
    name = 'Elliott_Wave_Oscillator_Sign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Mode': _Choice({1: 'Изменение направления движения', 2: 'Пробой нулевой линии'}, default=1),  # Алгоритм определения сигнала
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения первого мувинга
        'Length1': 5,  # Глубина усреднения первого мувинга
        'Phase1': 15,  # Параметр первого мувинга,
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=5),  # Ценовая константа первого мувинга
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения второго мувинга
        'Length2': 35,  # Глубина усреднения второго мувинга
        'Phase2': 15,  # Параметр второго мувинга,
        'IPC2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=5),  # Ценовая константа второго мувинга
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'Sign': True,  # Подача одноразового звукового сигнала при появлении стрелки на закрытом баре
    }

