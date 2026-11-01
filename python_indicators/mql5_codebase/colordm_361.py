"""colordm_361 — converted from MQL5: MQL5 Indicators/ColorDM_361_HTF/colordm_361.mq5

Copyright: Copyright 2002, Finware.ru Ltd.; Link: http://www.finware.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2002, Finware.ru Ltd.', 'link': 'http://www.finware.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [16711935, 8421504, 8421376]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'ColorDM_361'}, 'levels': [], 'description': [], 'name': 'colordm_361', 'source': 'MQL5 Indicators/ColorDM_361_HTF/colordm_361.mq5', 'folder': 'ColorDM_361_HTF', 'inputs': [{'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
InBuffer = Arr(0, 0.0)
ColorInBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 65
    SetIndexBuffer(0, InBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorInBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ColorDM_361')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    Res1 = 0.0
    Res2 = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Res1 = (-0.0579436862774459 * PriceSeries(IPC, bar - 0, open, low, high, close)) - (0.0436582666343197 * PriceSeries(IPC, bar - 1, open, low, high, close)) + (0.0168933393379673 * PriceSeries(IPC, bar - 2, open, low, high, close)) + (0.110448213843891 * PriceSeries(IPC, bar - 3, open, low, high, close)) + (0.20522024711311 * PriceSeries(IPC, bar - 4, open, low, high, close)) + (0.264664029548369 * PriceSeries(IPC, bar - 5, open, low, high, close)) + (0.264664029548369 * PriceSeries(IPC, bar - 6, open, low, high, close)) + (0.20522024711311 * PriceSeries(IPC, bar - 7, open, low, high, close)) + (0.110448213843891 * PriceSeries(IPC, bar - 8, open, low, high, close)) + (0.0168933393379673 * PriceSeries(IPC, bar - 9, open, low, high, close)) - (0.0436582666343197 * PriceSeries(IPC, bar - 10, open, low, high, close)) - (0.0579436862774459 * PriceSeries(IPC, bar - 11, open, low, high, close)) - (0.0348346366317942 * PriceSeries(IPC, bar - 12, open, low, high, close)) + (0.00221235473421834 * PriceSeries(IPC, bar - 13, open, low, high, close)) + (0.0289331217219094 * PriceSeries(IPC, bar - 14, open, low, high, close)) + (0.0324244017763432 * PriceSeries(IPC, bar - 15, open, low, high, close)) + (0.0155698339961958 * PriceSeries(IPC, bar - 16, open, low, high, close)) - (0.00766055486881318 * PriceSeries(IPC, bar - 17, open, low, high, close)) - (0.0221383478294209 * PriceSeries(IPC, bar - 18, open, low, high, close)) - (0.0205529903682718 * PriceSeries(IPC, bar - 19, open, low, high, close)) - (0.00643334760273044 * PriceSeries(IPC, bar - 20, open, low, high, close)) + (0.00962748150382101 * PriceSeries(IPC, bar - 21, open, low, high, close)) + (0.0173944693332311 * PriceSeries(IPC, bar - 22, open, low, high, close)) + (0.0131760869975097 * PriceSeries(IPC, bar - 23, open, low, high, close)) + (0.00120942458662409 * PriceSeries(IPC, bar - 24, open, low, high, close)) - (0.0100027091335947 * PriceSeries(IPC, bar - 25, open, low, high, close)) - (0.0135055787778998 * PriceSeries(IPC, bar - 26, open, low, high, close)) - (0.00803583151940507 * PriceSeries(IPC, bar - 27, open, low, high, close)) + (0.00190389109551071 * PriceSeries(IPC, bar - 28, open, low, high, close)) + (0.00948046725746693 * PriceSeries(IPC, bar - 29, open, low, high, close)) + (0.0101660909790824 * PriceSeries(IPC, bar - 30, open, low, high, close)) + (0.00430310478968843 * PriceSeries(IPC, bar - 31, open, low, high, close)) - (0.00365978720396328 * PriceSeries(IPC, bar - 32, open, low, high, close)) - (0.00841195685924682 * PriceSeries(IPC, bar - 33, open, low, high, close)) - (0.0072828460058001 * PriceSeries(IPC, bar - 34, open, low, high, close)) - (0.00162070447070519 * PriceSeries(IPC, bar - 35, open, low, high, close)) + (0.00446601446733231 * PriceSeries(IPC, bar - 36, open, low, high, close)) + (0.00704898572229122 * PriceSeries(IPC, bar - 37, open, low, high, close)) + (0.0048477999271653 * PriceSeries(IPC, bar - 38, open, low, high, close)) - (0.000217319809293247 * PriceSeries(IPC, bar - 39, open, low, high, close)) - (0.00460353885204705 * PriceSeries(IPC, bar - 40, open, low, high, close)) - (0.00557481706302029 * PriceSeries(IPC, bar - 41, open, low, high, close)) - (0.0028770471916742 * PriceSeries(IPC, bar - 42, open, low, high, close)) + (0.00137150496947603 * PriceSeries(IPC, bar - 43, open, low, high, close)) + (0.00428050657042468 * PriceSeries(IPC, bar - 44, open, low, high, close)) + (0.00413626988519937 * PriceSeries(IPC, bar - 45, open, low, high, close)) + (0.00136151337463329 * PriceSeries(IPC, bar - 46, open, low, high, close)) - (0.00197382022845936 * PriceSeries(IPC, bar - 47, open, low, high, close)) - (0.00367569927752237 * PriceSeries(IPC, bar - 48, open, low, high, close)) - (0.00283678858956286 * PriceSeries(IPC, bar - 49, open, low, high, close)) - (0.00028463168971981 * PriceSeries(IPC, bar - 50, open, low, high, close)) + (0.00215338773173264 * PriceSeries(IPC, bar - 51, open, low, high, close)) + (0.00293485520510334 * PriceSeries(IPC, bar - 52, open, low, high, close)) + (0.00175896282134328 * PriceSeries(IPC, bar - 53, open, low, high, close)) - (0.000389897847025107 * PriceSeries(IPC, bar - 54, open, low, high, close)) - (0.00203100698386829 * PriceSeries(IPC, bar - 55, open, low, high, close)) - (0.00219727740869414 * PriceSeries(IPC, bar - 56, open, low, high, close)) - (0.000975033303736501 * PriceSeries(IPC, bar - 57, open, low, high, close)) + (0.000693883112457725 * PriceSeries(IPC, bar - 58, open, low, high, close)) + (0.00175105610512485 * PriceSeries(IPC, bar - 59, open, low, high, close)) + (0.00168381712349721 * PriceSeries(IPC, bar - 60, open, low, high, close)) + (0.000645916394658871 * PriceSeries(IPC, bar - 61, open, low, high, close)) - (0.00122951364590661 * PriceSeries(IPC, bar - 62, open, low, high, close)) - (0.00549716561545307 * PriceSeries(IPC, bar - 63, open, low, high, close)) + (0.00171989273244504 * PriceSeries(IPC, bar - 64, open, low, high, close))
        Res2 = (0.21064209031795 * PriceSeries(IPC, bar - 0, open, low, high, close)) + (0.271656355551084 * PriceSeries(IPC, bar - 1, open, low, high, close)) + (0.271656355551084 * PriceSeries(IPC, bar - 2, open, low, high, close)) + (0.21064209031795 * PriceSeries(IPC, bar - 3, open, low, high, close)) + (0.113366214899538 * PriceSeries(IPC, bar - 4, open, low, high, close)) + (0.0173396551298304 * PriceSeries(IPC, bar - 5, open, low, high, close)) - (0.0448117019294051 * PriceSeries(IPC, bar - 6, open, low, high, close)) - (0.0594745370883487 * PriceSeries(IPC, bar - 7, open, low, high, close)) - (0.0357549548780298 * PriceSeries(IPC, bar - 8, open, low, high, close)) + (0.00227080432996318 * PriceSeries(IPC, bar - 9, open, low, high, close)) + (0.0296975241218164 * PriceSeries(IPC, bar - 10, open, low, high, close)) + (0.0332810425070465 * PriceSeries(IPC, bar - 11, open, low, high, close)) + (0.0159811832652874 * PriceSeries(IPC, bar - 12, open, low, high, close)) - (0.00786294390179145 * PriceSeries(IPC, bar - 13, open, low, high, close)) - (0.022723234810281 * PriceSeries(IPC, bar - 14, open, low, high, close)) - (0.0210959927899868 * PriceSeries(IPC, bar - 15, open, low, high, close)) - (0.00660331427256404 * PriceSeries(IPC, bar - 16, open, low, high, close)) + (0.00988183601272311 * PriceSeries(IPC, bar - 17, open, low, high, close)) + (0.0178540247946579 * PriceSeries(IPC, bar - 18, open, low, high, close)) + (0.0135241943541608 * PriceSeries(IPC, bar - 19, open, low, high, close)) + (0.00124137713793908 * PriceSeries(IPC, bar - 20, open, low, high, close)) - (0.0102669770180208 * PriceSeries(IPC, bar - 21, open, low, high, close)) - (0.0138623911858102 * PriceSeries(IPC, bar - 22, open, low, high, close)) - (0.00824813522301926 * PriceSeries(IPC, bar - 23, open, low, high, close)) + (0.00195419119574041 * PriceSeries(IPC, bar - 24, open, low, high, close)) + (0.00973093770422689 * PriceSeries(IPC, bar - 25, open, low, high, close)) + (0.0104346753515803 * PriceSeries(IPC, bar - 26, open, low, high, close)) + (0.00441679123043631 * PriceSeries(IPC, bar - 27, open, low, high, close)) - (0.00375647743147302 * PriceSeries(IPC, bar - 28, open, low, high, close)) - (0.00863419765555374 * PriceSeries(IPC, bar - 29, open, low, high, close)) - (0.00747525610998775 * PriceSeries(IPC, bar - 30, open, low, high, close)) - (0.0016635228848001 * PriceSeries(IPC, bar - 31, open, low, high, close)) + (0.00458400492165176 * PriceSeries(IPC, bar - 32, open, low, high, close)) + (0.0072352173240803 * PriceSeries(IPC, bar - 33, open, low, high, close)) + (0.00497587701245914 * PriceSeries(IPC, bar - 34, open, low, high, close)) - (0.000223061318466289 * PriceSeries(IPC, bar - 35, open, low, high, close)) - (0.00472516264986577 * PriceSeries(IPC, bar - 36, open, low, high, close)) - (0.00572210167278254 * PriceSeries(IPC, bar - 37, open, low, high, close)) - (0.00295305771688123 * PriceSeries(IPC, bar - 38, open, low, high, close)) + (0.00140773962470019 * PriceSeries(IPC, bar - 39, open, low, high, close)) + (0.00439359597455809 * PriceSeries(IPC, bar - 40, open, low, high, close)) + (0.0042455486093308 * PriceSeries(IPC, bar - 41, open, low, high, close)) + (0.00139748405560848 * PriceSeries(IPC, bar - 42, open, low, high, close)) - (0.00202596783057852 * PriceSeries(IPC, bar - 43, open, low, high, close)) - (0.00377280989614416 * PriceSeries(IPC, bar - 44, open, low, high, close)) - (0.00291173549735707 * PriceSeries(IPC, bar - 45, open, low, high, close)) - (0.000292151553936419 * PriceSeries(IPC, bar - 46, open, low, high, close)) + (0.00221027944102996 * PriceSeries(IPC, bar - 47, open, low, high, close)) + (0.00301239299669469 * PriceSeries(IPC, bar - 48, open, low, high, close)) + (0.00180543397004632 * PriceSeries(IPC, bar - 49, open, low, high, close)) - (0.000400198804275733 * PriceSeries(IPC, bar - 50, open, low, high, close)) - (0.0020846654389641 * PriceSeries(IPC, bar - 51, open, low, high, close)) - (0.002255328667062 * PriceSeries(IPC, bar - 52, open, low, high, close)) - (0.00100079332384525 * PriceSeries(IPC, bar - 53, open, low, high, close)) + (0.000712215248254048 * PriceSeries(IPC, bar - 54, open, low, high, close)) + (0.00179731836130289 * PriceSeries(IPC, bar - 55, open, low, high, close)) + (0.00172830295059105 * PriceSeries(IPC, bar - 56, open, low, high, close)) + (0.000662981267470111 * PriceSeries(IPC, bar - 57, open, low, high, close)) - (0.0012619969427552 * PriceSeries(IPC, bar - 58, open, low, high, close)) - (0.00564239870262307 * PriceSeries(IPC, bar - 59, open, low, high, close)) + (0.0017653316638158 * PriceSeries(IPC, bar - 60, open, low, high, close))
        InBuffer[bar] = Res2 - Res1
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 1
        if InBuffer[bar - 1] < InBuffer[bar]:
            clr = 2
        if InBuffer[bar - 1] > InBuffer[bar]:
            clr = 0
        ColorInBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colordm361(_MQL5Indicator):
    name = 'colordm_361'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

