"""demand_index — converted from MQL5: MQL5 Indicators/Demand_Index_HTF/demand_index.mq5

Demand Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15624315]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Demand Index'}, 'levels': [], 'description': ['Demand Index'], 'name': 'demand_index', 'source': 'MQL5 Indicators/Demand_Index_HTF/demand_index.mq5', 'folder': 'Demand_Index_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 9, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объем', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XLength = _input('XLength', 12)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
IPC = _input('IPC', PRICE_QUARTER_)  # Ценовая константа
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объем
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
DIBuffer = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = XMA1.GetStartBars(XMA_Method, XLength, XPhase) + 1
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    SetIndexBuffer(0, DIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Demand Index')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_BuyPres_, _s_OnCalculate_SellPres_, _s_OnCalculate_VolAvg_
    if rates_total < StartBars:
        return 0
    first = 0
    bar = 0
    Sign = 0
    AvgTR = 0.0
    Avg = 0.0
    VolAvg = 0.0
    price0 = 0.0
    price1 = 0.0
    WtCRatio = 0.0
    VolRatio = 0.0
    Constant = 0.0
    DMI = 0.0
    TempDI = 0.0
    BuyPres = 0.0
    SellPres = 0.0
    BuyP = 0.0
    SellP = 0.0
    Volume = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_BuyPres_ = 1.0
        _s_OnCalculate_SellPres_ = 1.0
        if VolumeType == VOLUME_TICK:
            _s_OnCalculate_VolAvg_ = float(tick_volume[0])
        else:
            _s_OnCalculate_VolAvg_ = float(volume[0])
    else:
        first = prev_calculated - 1
    VolAvg = _s_OnCalculate_VolAvg_
    BuyPres = _s_OnCalculate_BuyPres_
    SellPres = _s_OnCalculate_SellPres_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_VolAvg_ = VolAvg
            _s_OnCalculate_BuyPres_ = BuyPres
            _s_OnCalculate_SellPres_ = SellPres
        price0 = PriceSeries(IPC, bar, open, low, high, close)
        price1 = PriceSeries(IPC, bar - 1, open, low, high, close)
        if VolumeType == VOLUME_TICK:
            Volume = tick_volume[bar]
        else:
            Volume = volume[bar]
        Avg = MathMax(high[bar], high[bar - 1]) - MathMin(low[bar], low[bar - 1])
        AvgTR = XMA1.XMASeries(1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, Avg, bar, False)
        VolAvg = ((VolAvg * (XLength - 1)) + Volume) / XLength
        if ((price0 != 0 and price1 != 0) and AvgTR != 0) and VolAvg != 0:
            WtCRatio = _fdiv(price0 - price1, MathMin(price0, price1))
        if VolAvg != 0:
            VolRatio = _fdiv(Volume, VolAvg)
        else:
            VolRatio = 1.0
        Constant = _fdiv(price0 * 3, AvgTR) * MathAbs(WtCRatio)
        if Constant > 88:
            Constant = 88.0
        Constant = _fdiv(VolRatio, MathExp(Constant))
        if WtCRatio > 0:
            BuyP = VolRatio
            SellP = Constant
        else:
            BuyP = Constant
            SellP = VolRatio
        BuyPres = ((BuyPres * (XLength - 1)) + BuyP) / XLength
        SellPres = ((SellPres * (XLength - 1)) + SellP) / XLength
        TempDI = 1.0
        if SellPres > BuyPres:
            Sign = -1
            if SellPres != 0:
                TempDI = _fdiv(BuyPres, SellPres)
        else:
            Sign = 1
            if BuyPres != 0:
                TempDI = _fdiv(SellPres, BuyPres)
        TempDI *= Sign
        if TempDI < 0:
            DMI = -1 - TempDI
        else:
            DMI = 1 - TempDI
        DIBuffer[bar] = DMI * 100.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_VolAvg_ = 0.0
_s_OnCalculate_BuyPres_ = 0.0
_s_OnCalculate_SellPres_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DemandIndex(_MQL5Indicator):
    name = 'demand_index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 12,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=9),  # Ценовая константа
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объем
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

