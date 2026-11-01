"""copyticksind — converted from MQL5: MQL5 Indicators/CopyTicksInd/copyticksind.mq5

Indicator for comparing the three modes of receiving ticks
Индикатор для сравнения трёх режимов получения тиков
Copyright: Copyright © 2015, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.442

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.442', 'indicator_plots': 0, 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Indicator for comparing the three modes of receiving ticks', 'Индикатор для сравнения трёх режимов получения тиков'], 'name': 'copyticksind', 'source': 'MQL5 Indicators/CopyTicksInd/copyticksind.mq5', 'folder': 'CopyTicksInd', 'inputs': [{'mql': 'ticks', 'py': 'ticks', 'param': 'ticks', 'type': 'int', 'default': 30, 'label': 'number of requested tics/количество запрашиваемых тиков', 'sinput': False}, {'mql': 'type', 'py': 'type_', 'param': 'type_', 'type': 'int', 'default': -1, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

TICK_FLAG_ASK = 0  # MQL5 constant unknown to the converter
TICK_FLAG_BID = 0  # MQL5 constant unknown to the converter
TICK_FLAG_BUY = 0  # MQL5 constant unknown to the converter
TICK_FLAG_LAST = 0  # MQL5 constant unknown to the converter
TICK_FLAG_SELL = 0  # MQL5 constant unknown to the converter
TICK_FLAG_VOLUME = 0  # MQL5 constant unknown to the converter

# enum ENUM_COPY_TICKS
TICKS_INFO = 1
TICKS_TRADE = 2
TICKS_ALL = -1
_enum('ENUM_COPY_TICKS', {1: 'TICKS_INFO', 2: 'TICKS_TRADE', -1: 'TICKS_ALL'})

# ---- inputs and global variables
ticks = _input('ticks', 30)  # number of requested tics/количество запрашиваемых тиков
type_ = _input('type_', TICKS_ALL)

def OnInit():
    Print(TICK_FLAG_BID, ' - tick has changed a Bid price/тик изменил цену бид')
    Print(TICK_FLAG_ASK, '  - a tick has changed an Ask price/тик изменил цену аск')
    Print(TICK_FLAG_LAST, ' - a tick has changed the last deal price/тик изменил цену последней сделки')
    Print(TICK_FLAG_VOLUME, ' - a tick has changed a volume/тик изменил объем')
    Print(TICK_FLAG_BUY, ' - a tick is a result of a buy deal/тик возник в результате сделки на покупку')
    Print(TICK_FLAG_SELL, ' - a tick is a result of a sell deal/тик возник в результате сделки на продажу')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    tick_array = Arr(0, 0, factory=MqlTick)
    copied = CopyTicks(Symbol(), tick_array, type_, 0, ticks)
    if copied > 0:
        comment = EnumToString(type_, 'ENUM_COPY_TICKS') + ' ,requested ' + IntegerToString(ticks) + ', copied ' + IntegerToString(copied) + '\r\n'
        comment += '#      Time         Bid        Ask       Last    Volume            time_msc            flags\r\n'
        j = copied
        if ticks > 42 and copied > 42:
            j = 42
        flags = ''
        for i in range(copied - 1, copied - 1 - j, -1):
            tick = _copy(tick_array[i])
            flags = ''
            if (tick.flags & TICK_FLAG_BID) == TICK_FLAG_BID:
                flags = ' TICK_FLAG_BID '
            if (tick.flags & TICK_FLAG_ASK) == TICK_FLAG_ASK:
                flags += ' TICK_FLAG_ASK '
            if (tick.flags & TICK_FLAG_LAST) == TICK_FLAG_LAST:
                flags += ' TICK_FLAG_LAST '
            if (tick.flags & TICK_FLAG_VOLUME) == TICK_FLAG_VOLUME:
                flags += ' TICK_FLAG_VOLUME '
            if (tick.flags & TICK_FLAG_BUY) == TICK_FLAG_BUY:
                flags += ' TICK_FLAG_BUY '
            if (tick.flags & TICK_FLAG_SELL) == TICK_FLAG_SELL:
                flags += ' TICK_FLAG_SELL '
            tick_string = IntegerToString(i, 2, 48) + '  ' + TimeToString(tick.time, TIME_MINUTES | TIME_SECONDS) + '  ' + DoubleToString(tick.bid, Digits()) + '  ' + DoubleToString(tick.ask, Digits()) + '  ' + DoubleToString(tick.last, Digits()) + '  ' + IntegerToString(tick.volume, 7, 48) + '  ' + IntegerToString(tick.time_msc, 19, 48) + '  ' + IntegerToString(tick.flags, 2, 48)
            tick_string += flags
            comment = comment + tick_string + '\r\n'
        Comment(comment)
    else:
        Comment('Ticks could not be loaded/Не удалось загрузить тики. GetLastError()=', GetLastError())
    return rates_total

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Copyticksind(_MQL5Indicator):
    name = 'copyticksind'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ticks': 30,  # number of requested tics/количество запрашиваемых тиков
        'type_': _Choice({1: 'only/только Bid и Ask', 2: 'only/только Last и Volume', -1: 'all ticks/все тики'}, default=-1),
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

