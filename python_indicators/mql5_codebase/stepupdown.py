"""StepUpDown — converted from MQL5: MQL5 Indicators/StepUpDown/StepUpDown.mq5

Price Direction movement Step Up and Down Forex Indicator for MetaTrader 5.
Copyright: Copyright 2017, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 11/01/2017; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 11/01/2017', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': ['Price Direction movement Step Up and Down Forex Indicator for MetaTrader 5.'], 'name': 'StepUpDown', 'source': 'MQL5 Indicators/StepUpDown/StepUpDown.mq5', 'folder': 'StepUpDown', 'inputs': [{'mql': 'MsgSignalAlerts', 'py': 'MsgSignalAlerts', 'param': 'MsgSignalAlerts', 'type': 'bool', 'default': True, 'label': 'PopUp Message Alert', 'sinput': False}, {'mql': 'SoundAlertsSignal', 'py': 'SoundAlertsSignal', 'param': 'SoundAlertsSignal', 'type': 'bool', 'default': True, 'label': 'Sound Alert', 'sinput': False}, {'mql': 'eMailSignalAlerts', 'py': 'eMailSignalAlerts', 'param': 'eMailSignalAlerts', 'type': 'bool', 'default': False, 'label': 'Send Email Alert', 'sinput': False}, {'mql': 'FileSoundAlert', 'py': 'FileSoundAlert', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound Alert file name', 'sinput': False}, {'mql': 'UpsColor', 'py': 'UpsColor', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'UP Color', 'sinput': False}, {'mql': 'DnsColor', 'py': 'DnsColor', 'param': None, 'type': 'color', 'default': 17919, 'label': 'Down Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum TimeReturn
year = 0
mon = 1
day = 2
hour = 3
min_ = 4
sec = 5
day_of_week = 6
day_of_year = 7
_enum('TimeReturn', {0: 'year', 1: 'mon', 2: 'day', 3: 'hour', 4: 'min', 5: 'sec', 6: 'day_of_week', 7: 'day_of_year'})

# ---- inputs and global variables
MsgSignalAlerts = _input('MsgSignalAlerts', True)  # PopUp Message Alert
SoundAlertsSignal = _input('SoundAlertsSignal', True)  # Sound Alert
eMailSignalAlerts = _input('eMailSignalAlerts', False)  # Send Email Alert
FileSoundAlert = _input('FileSoundAlert', 'alert.wav')  # Sound Alert file name
UpsColor = _input('UpsColor', clrAqua)  # UP Color
DnsColor = _input('DnsColor', clrOrangeRed)  # Down Color
naik = Arr(0, 0.0)
turun = Arr(0, 0.0)
barcount = 77
wavecount = 13
periodturn = 3
slowperiod = 36
limit = 0
mina = 0
minx = 0
posH = 0
posL = 0
curAlert = 0
prvAlert = 0
Chart_Id = 0
ups = False
dns = False
name_arr_ups = ""
name_arr_dns = ""
name_dir_ups = ""
name_dir_dwn = ""
ind_name = ""
Sibase = ""
SiSubj = ""
SiMsg = ""

def OnInit():
    global Chart_Id, ind_name
    SetIndexBuffer(0, naik, INDICATOR_DATA)
    SetIndexBuffer(1, turun, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Up')
    PlotIndexSetString(1, PLOT_LABEL, 'Down')
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, True)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    Chart_Id = ChartID()
    ind_name = 'StepUpDown'
    IndicatorSetString(INDICATOR_SHORTNAME, ind_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(ChartID(), name_arr_dns)
    ObjectDelete(ChartID(), name_arr_ups)
    ObjectDelete(ChartID(), name_dir_dwn)
    ObjectDelete(ChartID(), name_dir_ups)
    GlobalVariablesDeleteAll()
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global curAlert, dns, limit, name_arr_dns, name_arr_ups, name_dir_dwn, name_dir_ups, posH, posL, ups
    ResetLastError()
    i = 0
    j = 0
    mlhi = 0
    mllo = 0
    wbar = wavecount
    if rates_total < barcount:
        return 0
    if prev_calculated == 0:
        limit = barcount
    if prev_calculated > 0:
        limit += 1
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    ups = False
    dns = False
    divma0 = 0.0
    divma1 = 0.0
    mahi = iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, 1)
    malo = iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, 1)
    i = wbar - 1
    for i in range(i, 0 - 1, -1):
        if iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, i) > mahi:
            mahi = iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, i)
            mlhi = i
        if iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, i) < malo:
            malo = iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, i)
            mllo = i
        divma0 = iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, i) - iMA_u(Symbol(), PERIOD_CURRENT, slowperiod, 0, MODE_SMMA, PRICE_TYPICAL, i)
        divma1 = iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, i + 1) - iMA_u(Symbol(), PERIOD_CURRENT, slowperiod, 0, MODE_SMMA, PRICE_TYPICAL, i + 1)
    else:
        i = _range_end(i, 0 - 1, -1)
    j = limit - 1
    for j in range(j, 0 - 1, -1):
        if mlhi > mllo and iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, j) > malo:
            ups = True
            dns = False
        if mlhi > mllo and divma0 < divma1:
            dns = True
            ups = False
        if mlhi < mllo and iMA_u(Symbol(), PERIOD_CURRENT, periodturn, 0, MODE_EMA, PRICE_TYPICAL, j) > mahi:
            dns = True
            ups = False
        if mlhi < mllo and divma0 > divma1:
            ups = True
            dns = False
        if j == 0:
            posH = iHighest_u(Symbol(), PERIOD_CURRENT, wavecount, j)
            posL = iLowest_u(Symbol(), PERIOD_CURRENT, wavecount, j)
            if ups == True:
                name_arr_ups = 'uparrow'
                name_dir_ups = 'updirec'
                pos_price = low[posL]
                pos_dir_time = time[posL]
                naik[j] = low[posL]
                turun[j] = EMPTY_VALUE
                ObjectDelete(Chart_Id, name_arr_dns)
                ObjectDelete(Chart_Id, name_dir_dwn)
                CreateDirection(Chart_Id, name_dir_ups, '  UP ', 'Bodoni MT Black', 9, UpsColor, pos_dir_time, pos_price - (5 * Point()), ANCHOR_LEFT_UPPER)
                CreateDirection(Chart_Id, name_arr_ups, CharToString(217), 'Wingdings', 15, UpsColor, pos_dir_time, pos_price - (5 * Point()), ANCHOR_RIGHT_UPPER)
                curAlert = 0
                SendAlerts(curAlert, naik[j])
            if dns == True:
                name_arr_dns = 'dnarrow'
                name_dir_dwn = 'dndirec'
                pos_price = high[posH]
                pos_dir_time = time[posH]
                turun[j] = high[posH]
                naik[j] = EMPTY_VALUE
                ObjectDelete(Chart_Id, name_arr_ups)
                ObjectDelete(Chart_Id, name_dir_ups)
                CreateDirection(Chart_Id, name_dir_dwn, '  DOWN', 'Bodoni MT Black', 9, DnsColor, pos_dir_time, pos_price + (5 * Point()), ANCHOR_LEFT_LOWER)
                CreateDirection(Chart_Id, name_arr_dns, CharToString(218), 'Wingdings', 15, DnsColor, pos_dir_time, pos_price + (5 * Point()), ANCHOR_RIGHT_LOWER)
                curAlert = 1
                SendAlerts(curAlert, turun[j])
    else:
        j = _range_end(j, 0 - 1, -1)
    ChartRedraw(0)
    Sleep(500)
    return rates_total

def CreateDirection(chart_id, obj_name, obj_text, font_model, font_size, obj_color, text_time, text_pos, anchor):
    if ObjectFind(chart_id, obj_name) > 0:
        ObjectDelete(chart_id, obj_name)
    ObjectCreate(chart_id, obj_name, OBJ_TEXT, 0, text_time, text_pos)
    ObjectSetString(chart_id, obj_name, OBJPROP_FONT, font_model)
    ObjectSetInteger(chart_id, obj_name, OBJPROP_FONTSIZE, font_size)
    ObjectSetInteger(chart_id, obj_name, OBJPROP_COLOR, obj_color)
    ObjectSetString(chart_id, obj_name, OBJPROP_TEXT, obj_text)
    ObjectSetInteger(chart_id, obj_name, OBJPROP_ANCHOR, anchor)
    ChartRedraw()

def iMA_u(symbol, tf, period, ma_shift, method, mprice, shift):
    handle = iMA(symbol, tf, period, ma_shift, method, mprice)
    buf = Arr(0, 0.0)
    if handle < 0:
        Print('The iMA object is not created: Error', GetLastError())
        return -1.0
    else:
        CopyBuffer(handle, 0, shift, 1, buf)
    return buf[0]

def iHighest_u(symbol, tf, countbar, startpos):
    index = startpos
    if startpos < 0:
        return -1
    if countbar <= 0:
        countbar = Bars(symbol, tf)
    high = Arr(0, 0.0)
    ArraySetAsSeries(high, True)
    CopyHigh(symbol, tf, startpos, countbar, high)
    index = ArrayMaximum(high, startpos, countbar - startpos + 1)
    return index

def iLowest_u(symbol, tf, countbar, startpos):
    index = startpos
    if startpos < 0:
        return -1
    if countbar <= 0:
        countbar = Bars(symbol, tf)
    low = Arr(0, 0.0)
    ArraySetAsSeries(low, True)
    CopyLow(symbol, tf, startpos, countbar, low)
    index = ArrayMinimum(low, startpos, countbar - startpos + 1)
    return index

def MqlReturnDateTime(reqtime, mode):
    mqltm = MqlDateTime()
    TimeToStruct(reqtime, mqltm)
    valdate = 0
    _sw1 = mode
    if _sw1 == 0:
        valdate = mqltm.year
    elif _sw1 == 1:
        valdate = mqltm.mon
    elif _sw1 == 2:
        valdate = mqltm.day
    elif _sw1 == 3:
        valdate = mqltm.hour
    elif _sw1 == 4:
        valdate = mqltm.min
    elif _sw1 == 5:
        valdate = mqltm.sec
    elif _sw1 == 6:
        valdate = mqltm.day_of_week
    elif _sw1 == 7:
        valdate = mqltm.day_of_year
    return valdate

def DoSignalAlerts(msgSignalText, eMailSignalSub):
    if MsgSignalAlerts:
        Alert(msgSignalText)
    if SoundAlertsSignal:
        PlaySound(FileSoundAlert)
    if eMailSignalAlerts:
        SendMail(eMailSignalSub, msgSignalText)

def strTF(period):
    _sw2 = period
    if _sw2 == PERIOD_M1:
        return 'M1'
    elif _sw2 == PERIOD_M5:
        return 'M5'
    elif _sw2 == PERIOD_M15:
        return 'M15'
    elif _sw2 == PERIOD_M30:
        return 'M30'
    elif _sw2 == PERIOD_H1:
        return 'H1'
    elif _sw2 == PERIOD_H4:
        return 'H4'
    elif _sw2 == PERIOD_D1:
        return 'D1'
    elif _sw2 == PERIOD_W1:
        return 'W1'
    elif _sw2 == PERIOD_MN1:
        return 'MN'
    else:
        return 'Unknown'

def SendAlerts(alerts, position):
    global SiMsg, SiSubj, Sibase, mina, minx, prvAlert
    mina = MqlReturnDateTime(TimeCurrent(), min_)
    if mina != minx:
        if alerts != prvAlert and alerts == 0:
            Sibase = ind_name + ' ' + Symbol() + ', TF: ' + strTF(Period())
            SiSubj = Sibase + ' Step to Up Above: ' + DoubleToString(position, Digits())
            SiMsg = SiSubj + ' @ ' + TimeToString(TimeCurrent(), TIME_SECONDS)
            DoSignalAlerts(SiMsg, SiSubj)
            prvAlert = alerts
            minx = mina
        if alerts != prvAlert and alerts == 1:
            Sibase = ind_name + ' ' + Symbol() + ', TF: ' + strTF(Period())
            SiSubj = Sibase + ' Step to Down Below: ' + DoubleToString(position, Digits())
            SiMsg = SiSubj + ' @ ' + TimeToString(TimeCurrent(), TIME_SECONDS)
            DoSignalAlerts(SiMsg, SiSubj)
            prvAlert = alerts
            minx = mina
    return


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepUpDown(_MQL5Indicator):
    name = 'StepUpDown'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MsgSignalAlerts': True,  # PopUp Message Alert
        'SoundAlertsSignal': True,  # Sound Alert
        'eMailSignalAlerts': False,  # Send Email Alert
    }

