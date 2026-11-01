"""RSIOMA — converted from MQL5: MQL5 Indicators/RSIOMA MT5/RSIOMA.mq5

RSIOMA displays a Relative Strenfth Index built based on relative MA strength, instead of the normal Close values.
The thin line is the MA of RSIOMA.
Main signal: RSIOMA crosses 20 from below or 80 from above.
Auxiliary signal: RSIOMA starts rising below 20 or starts falling above 80.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3, 'indicator_minimum': -10.0, 'indicator_maximum': 100.0}, 'types': {1: 1, 2: 10, 3: 1}, 'colors': {1: [16711680], 2: [255, 32768, 16711935, 16748574], 3: [14822282]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'RSIOMA', 2: 'Trend Down', 3: 'MA of RSIOMA'}, 'levels': [], 'description': ['RSIOMA displays a Relative Strenfth Index built based on relative MA strength, instead of the normal Close values.', 'The thin line is the MA of RSIOMA.', 'Main signal: RSIOMA crosses 20 from below or 80 from above.', 'Auxiliary signal: RSIOMA starts rising below 20 or starts falling above 80.'], 'name': 'RSIOMA', 'source': 'MQL5 Indicators/RSIOMA MT5/RSIOMA.mq5', 'folder': 'RSIOMA MT5', 'inputs': [{'mql': 'RSIOMA', 'py': 'RSIOMA', 'param': 'RSIOMA', 'type': 'int', 'default': 14, 'label': 'RSIOMA Period', 'sinput': False}, {'mql': 'RSIOMA_MODE', 'py': 'RSIOMA_MODE', 'param': 'RSIOMA_MODE', 'type': 'int', 'default': 1, 'label': 'RSIOMA Mode', 'sinput': False}, {'mql': 'RSIOMA_PRICE', 'py': 'RSIOMA_PRICE', 'param': 'RSIOMA_PRICE', 'type': 'int', 'default': 1, 'label': 'RSIOMA Price', 'sinput': False}, {'mql': 'Ma_RSIOMA', 'py': 'Ma_RSIOMA', 'param': 'Ma_RSIOMA', 'type': 'int', 'default': 21, 'label': 'MA of RSIOMA Period', 'sinput': False}, {'mql': 'Ma_RSIOMA_MODE', 'py': 'Ma_RSIOMA_MODE', 'param': 'Ma_RSIOMA_MODE', 'type': 'int', 'default': 1, 'label': 'MA of RSIOMA Mode', 'sinput': False}, {'mql': 'BuyTrigger', 'py': 'BuyTrigger', 'param': 'BuyTrigger', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'SellTrigger', 'py': 'SellTrigger', 'param': 'SellTrigger', 'type': 'int', 'default': 80, 'label': '', 'sinput': False}, {'mql': 'BuyTriggerColor', 'py': 'BuyTriggerColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}, {'mql': 'SellTriggerColor', 'py': 'SellTriggerColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': '', 'sinput': False}, {'mql': 'MainTrendLong', 'py': 'MainTrendLong', 'param': 'MainTrendLong', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'MainTrendShort', 'py': 'MainTrendShort', 'param': 'MainTrendShort', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'MainTrendLongColor', 'py': 'MainTrendLongColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'MainTrendShortColor', 'py': 'MainTrendShortColor', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'MainAlerts', 'py': 'MainAlerts', 'param': 'MainAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AuxiliaryAlerts', 'py': 'AuxiliaryAlerts', 'param': 'AuxiliaryAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
RSIOMA = _input('RSIOMA', 14)  # RSIOMA Period
RSIOMA_MODE = _input('RSIOMA_MODE', MODE_EMA)  # RSIOMA Mode
RSIOMA_PRICE = _input('RSIOMA_PRICE', PRICE_CLOSE)  # RSIOMA Price
Ma_RSIOMA = _input('Ma_RSIOMA', 21)  # MA of RSIOMA Period
Ma_RSIOMA_MODE = _input('Ma_RSIOMA_MODE', MODE_EMA)  # MA of RSIOMA Mode
BuyTrigger = _input('BuyTrigger', 20)
SellTrigger = _input('SellTrigger', 80)
BuyTriggerColor = _input('BuyTriggerColor', clrMagenta)
SellTriggerColor = _input('SellTriggerColor', clrDodgerBlue)
MainTrendLong = _input('MainTrendLong', 50)
MainTrendShort = _input('MainTrendShort', 50)
MainTrendLongColor = _input('MainTrendLongColor', clrRed)
MainTrendShortColor = _input('MainTrendShortColor', clrGreen)
MainAlerts = _input('MainAlerts', False)
AuxiliaryAlerts = _input('AuxiliaryAlerts', False)
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
TriggerCandle = _input('TriggerCandle', Previous)
RSIBuffer = Arr(0, 0.0)
PosBuffer = Arr(0, 0.0)
NegBuffer = Arr(0, 0.0)
Histogram = Arr(0, 0.0)
Histogram_Color = Arr(0, 0.0)
marsioma = Arr(0, 0.0)
MA_Buffer = Arr(0, 0.0)
short_name = ""
LastAlertTime = 0
MA_Handle = 0

def OnInit():
    global MA_Handle, short_name
    SetIndexBuffer(0, RSIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Histogram, INDICATOR_DATA)
    SetIndexBuffer(2, Histogram_Color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, marsioma, INDICATOR_DATA)
    SetIndexBuffer(4, PosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, NegBuffer, INDICATOR_CALCULATIONS)
    PlotIndexGetInteger(0, PLOT_DRAW_BEGIN, RSIOMA)
    PlotIndexGetInteger(1, PLOT_DRAW_BEGIN, RSIOMA)
    PlotIndexGetInteger(2, PLOT_DRAW_BEGIN, RSIOMA)
    short_name = 'RSIOMA(' + IntegerToString(RSIOMA) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    drawLine(MainTrendLong, 'MainTrendLong', MainTrendLongColor)
    drawLine(MainTrendShort, 'MainTrendShort', MainTrendShortColor)
    drawLine(BuyTrigger, 'BuyTrigger', BuyTriggerColor)
    drawLine(SellTrigger, 'SellTrigger', SellTriggerColor)
    MA_Handle = iMA(Symbol(), Period(), RSIOMA, 0, RSIOMA_MODE, RSIOMA_PRICE)
    ArraySetAsSeries(RSIBuffer, True)
    ArraySetAsSeries(Histogram, True)
    ArraySetAsSeries(Histogram_Color, True)
    ArraySetAsSeries(marsioma, True)
    ArraySetAsSeries(PosBuffer, True)
    ArraySetAsSeries(NegBuffer, True)
    ArraySetAsSeries(MA_Buffer, True)

def OnCalculate(rates_total, prev_calculated, Time, open, high, low, close, tick_volume, volume, spread):
    global LastAlertTime
    i = 0
    counted_bars = prev_calculated
    if rates_total <= RSIOMA:
        return 0
    if counted_bars < 1:
        i = 1
        for i in range(i, RSIOMA + 1):
            RSIBuffer[rates_total - i] = 0.0
        else:
            i = _range_end(i, RSIOMA + 1, 1)
    i = rates_total - RSIOMA - 1
    ma = i
    if counted_bars >= RSIOMA:
        i = rates_total - (counted_bars - 1)
    if i == (rates_total - RSIOMA - 1):
        if CopyBuffer(MA_Handle, 0, 0, rates_total, MA_Buffer) != rates_total:
            return 0
    else:
        if CopyBuffer(MA_Handle, 0, 0, i + 2, MA_Buffer) != (i + 2):
            return 0
    ArraySetAsSeries(Time, True)
    while i >= 0:
        sumn = 0.0
        sump = 0.0
        rel = 0.0
        negative = 0.0
        positive = 0.0
        if i == (rates_total - RSIOMA - 1):
            k = rates_total - 2
            while k >= i:
                cma = MA_Buffer[k]
                pma = MA_Buffer[k + 1]
                rel = cma - pma
                if rel > 0:
                    sump += rel
                else:
                    sumn -= rel
                k -= 1
            positive = sump / RSIOMA
            negative = sumn / RSIOMA
        else:
            ccma = MA_Buffer[i]
            ppma = MA_Buffer[i + 1]
            rel = ccma - ppma
            if rel > 0:
                sump = rel
            else:
                sumn = -rel
            positive = ((PosBuffer[i + 1] * (RSIOMA - 1)) + sump) / RSIOMA
            negative = ((NegBuffer[i + 1] * (RSIOMA - 1)) + sumn) / RSIOMA
        PosBuffer[i] = positive
        NegBuffer[i] = negative
        if negative == 0.0:
            RSIBuffer[i] = 0.0
        else:
            RSIBuffer[i] = 100.0 - _fdiv(100.0, 1 + _fdiv(positive, negative))
            if RSIBuffer[i] > MainTrendLong:
                Histogram[i] = -10.0
                Histogram_Color[i] = 1.0
            if RSIBuffer[i] < MainTrendShort:
                Histogram[i] = -10.0
                Histogram_Color[i] = 0.0
            if RSIBuffer[i] < BuyTrigger and RSIBuffer[i] > RSIBuffer[i + 1]:
                Histogram[i] = -10.0
                Histogram_Color[i] = 3.0
            if RSIBuffer[i] > SellTrigger and RSIBuffer[i] < RSIBuffer[i + 1]:
                Histogram[i] = -10.0
                Histogram_Color[i] = 2.0
        i -= 1
    iMAOnArray_u(RSIBuffer, Ma_RSIOMA, Ma_RSIOMA_MODE)
    if (TriggerCandle > 0 and Time[0] > LastAlertTime) or TriggerCandle == 0:
        Text = ""
        if MainAlerts:
            if RSIBuffer[TriggerCandle] < SellTrigger and RSIBuffer[TriggerCandle + 1] >= SellTrigger:
                Text = 'RSIOMA: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Crossed ' + IntegerToString(SellTrigger) + ' from above.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('RSIOMA Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[0]
            if RSIBuffer[TriggerCandle] > BuyTrigger and RSIBuffer[TriggerCandle + 1] <= BuyTrigger:
                Text = 'RSIOMA: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Crossed ' + IntegerToString(BuyTrigger) + ' from below.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('RSIOMA Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[0]
        if AuxiliaryAlerts:
            if Histogram_Color[TriggerCandle] == 2 and Histogram_Color[TriggerCandle + 1] != 2:
                Text = 'RSIOMA: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Bearish reversal imminent.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('RSIOMA Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[0]
            if Histogram_Color[TriggerCandle] == 3 and Histogram_Color[TriggerCandle + 1] != 3:
                Text = 'RSIOMA: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Bullish reversal imminent.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('RSIOMA Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[0]
    return rates_total

def drawLine(lvl, name, Col):
    ObjectDelete(ChartID(), name)
    ObjectCreate(ChartID(), name, OBJ_HLINE, ChartWindowFind(ChartID(), short_name), 0, lvl, 0, lvl)
    ObjectSetInteger(ChartID(), name, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(ChartID(), name, OBJPROP_COLOR, Col)
    ObjectSetInteger(ChartID(), name, OBJPROP_WIDTH, 1)
    ObjectSetInteger(ChartID(), name, OBJPROP_SELECTABLE, False)

def iMAOnArray_u(array, period, ma_method):
    total = ArraySize(array)
    if total <= period:
        return 0.0
    _sw1 = ma_method
    if _sw1 == MODE_SMA:
        sum_ = 0.0
        pos = total - 1
        i = 1
        while i < period:
            sum_ += array[pos]
            i += 1
            pos -= 1
        while pos >= 0:
            sum_ += array[pos]
            marsioma[pos] = _fdiv(sum_, period)
            sum_ -= array[pos + period - 1]
            pos -= 1
    elif _sw1 == MODE_EMA:
        pr = _fdiv(2.0, period + 1)
        pos = total - 2
        while pos >= 0:
            if pos == (total - 2):
                marsioma[pos + 1] = array[pos + 1]
            marsioma[pos] = (array[pos] * pr) + (marsioma[pos + 1] * (1 - pr))
            pos -= 1
    elif _sw1 == MODE_SMMA:
        sum_ = 0.0
        pos = total - period
        while pos >= 0:
            if pos == (total - period):
                i = 0
                k = pos
                while i < period:
                    sum_ += array[k]
                    marsioma[k] = 0.0
                    i += 1
                    k += 1
            else:
                sum_ = (marsioma[pos + 1] * (period - 1)) + array[pos]
            marsioma[pos] = _fdiv(sum_, period)
            pos -= 1
    elif _sw1 == MODE_LWMA:
        sum_ = 0.0
        lsum = 0.0
        price = 0.0
        i = 0
        weight = 0
        pos = total - 1
        i = 1
        while i <= period:
            price = array[pos]
            sum_ += price * i
            lsum += price
            weight += i
            i += 1
            pos -= 1
        pos += 1
        i = pos + period
        while pos >= 0:
            marsioma[pos] = _fdiv(sum_, weight)
            if pos == 0:
                break
            pos -= 1
            i -= 1
            price = array[pos]
            sum_ = sum_ - lsum + (price * period)
            lsum -= array[i]
            lsum += price
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIOMAIndicator(_MQL5Indicator):
    name = 'RSIOMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIOMA': 14,  # RSIOMA Period
        'RSIOMA_MODE': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # RSIOMA Mode
        'RSIOMA_PRICE': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSIOMA Price
        'Ma_RSIOMA': 21,  # MA of RSIOMA Period
        'Ma_RSIOMA_MODE': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA of RSIOMA Mode
        'BuyTrigger': 20,
        'SellTrigger': 80,
        'MainTrendLong': 50,
        'MainTrendShort': 50,
        'MainAlerts': False,
        'AuxiliaryAlerts': False,
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
    }
    y_range = (-10.0, 100.0)

