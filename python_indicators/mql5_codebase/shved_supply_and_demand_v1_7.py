"""shved_supply_and_demand_v1.7 — converted from MQL5: MQL5 Indicators/Shved Supply and Demand/shved_supply_and_demand_v1.7.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 11}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'shved_supply_and_demand_v1.7', 'source': 'MQL5 Indicators/Shved Supply and Demand/shved_supply_and_demand_v1.7.mq5', 'folder': 'Shved Supply and Demand', 'inputs': [{'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 0, 'label': 'Timeframe', 'sinput': False}, {'mql': 'BackLimit', 'py': 'BackLimit', 'param': 'BackLimit', 'type': 'int', 'default': 1000, 'label': 'Back Limit', 'sinput': False}, {'mql': 'HistoryMode', 'py': 'HistoryMode', 'param': 'HistoryMode', 'type': 'bool', 'default': False, 'label': 'History Mode (with double click)', 'sinput': False}, {'mql': 'zone_settings', 'py': 'zone_settings', 'param': None, 'type': 'string', 'default': '--- Zone Settings ---', 'label': '', 'sinput': False}, {'mql': 'zone_show_weak', 'py': 'zone_show_weak', 'param': 'zone_show_weak', 'type': 'bool', 'default': False, 'label': 'Show Weak Zones', 'sinput': False}, {'mql': 'zone_show_untested', 'py': 'zone_show_untested', 'param': 'zone_show_untested', 'type': 'bool', 'default': True, 'label': 'Show Untested Zones', 'sinput': False}, {'mql': 'zone_show_turncoat', 'py': 'zone_show_turncoat', 'param': 'zone_show_turncoat', 'type': 'bool', 'default': True, 'label': 'Show Broken Zones', 'sinput': False}, {'mql': 'zone_fuzzfactor', 'py': 'zone_fuzzfactor', 'param': 'zone_fuzzfactor', 'type': 'double', 'default': 0.75, 'label': 'Zone ATR Factor', 'sinput': False}, {'mql': 'zone_merge', 'py': 'zone_merge', 'param': 'zone_merge', 'type': 'bool', 'default': True, 'label': 'Zone Merge', 'sinput': False}, {'mql': 'zone_extend', 'py': 'zone_extend', 'param': 'zone_extend', 'type': 'bool', 'default': True, 'label': 'Zone Extend', 'sinput': False}, {'mql': 'fractal_fast_factor', 'py': 'fractal_fast_factor', 'param': 'fractal_fast_factor', 'type': 'double', 'default': 3.0, 'label': 'Fractal Fast Factor', 'sinput': False}, {'mql': 'fractal_slow_factor', 'py': 'fractal_slow_factor', 'param': 'fractal_slow_factor', 'type': 'double', 'default': 6.0, 'label': 'Fractal slow Factor', 'sinput': False}, {'mql': 'alert_settings', 'py': 'alert_settings', 'param': None, 'type': 'string', 'default': '--- Alert Settings ---', 'label': '', 'sinput': False}, {'mql': 'zone_show_alerts', 'py': 'zone_show_alerts', 'param': 'zone_show_alerts', 'type': 'bool', 'default': False, 'label': 'Trigger alert when entering a zone', 'sinput': False}, {'mql': 'zone_alert_popups', 'py': 'zone_alert_popups', 'param': 'zone_alert_popups', 'type': 'bool', 'default': True, 'label': 'Show alert window', 'sinput': False}, {'mql': 'zone_alert_sounds', 'py': 'zone_alert_sounds', 'param': 'zone_alert_sounds', 'type': 'bool', 'default': True, 'label': 'Play alert sound', 'sinput': False}, {'mql': 'zone_send_notification', 'py': 'zone_send_notification', 'param': 'zone_send_notification', 'type': 'bool', 'default': False, 'label': 'Send notification when entering a zone', 'sinput': False}, {'mql': 'zone_alert_waitseconds', 'py': 'zone_alert_waitseconds', 'param': 'zone_alert_waitseconds', 'type': 'int', 'default': 300, 'label': 'Delay between alerts (seconds)', 'sinput': False}, {'mql': 'drawing_settings', 'py': 'drawing_settings', 'param': None, 'type': 'string', 'default': '--- Drawing Settings ---', 'label': '', 'sinput': False}, {'mql': 'string_prefix', 'py': 'string_prefix', 'param': None, 'type': 'string', 'default': 'SRRR', 'label': 'Change prefix to add multiple indicators to chart', 'sinput': False}, {'mql': 'zone_solid', 'py': 'zone_solid', 'param': 'zone_solid', 'type': 'bool', 'default': True, 'label': 'Fill zone with color', 'sinput': False}, {'mql': 'zone_linewidth', 'py': 'zone_linewidth', 'param': 'zone_linewidth', 'type': 'int', 'default': 1, 'label': 'Zone border width', 'sinput': False}, {'mql': 'zone_style', 'py': 'zone_style', 'param': 'zone_style', 'type': 'int', 'default': 0, 'label': 'Zone border style', 'sinput': False}, {'mql': 'zone_show_info', 'py': 'zone_show_info', 'param': 'zone_show_info', 'type': 'bool', 'default': True, 'label': 'Show info labels', 'sinput': False}, {'mql': 'zone_label_shift', 'py': 'zone_label_shift', 'param': 'zone_label_shift', 'type': 'int', 'default': 10, 'label': 'Info label shift', 'sinput': False}, {'mql': 'sup_name', 'py': 'sup_name', 'param': None, 'type': 'string', 'default': 'Sup', 'label': 'Support Name', 'sinput': False}, {'mql': 'res_name', 'py': 'res_name', 'param': None, 'type': 'string', 'default': 'Res', 'label': 'Resistance Name', 'sinput': False}, {'mql': 'test_name', 'py': 'test_name', 'param': None, 'type': 'string', 'default': 'Retests', 'label': 'Retest Name', 'sinput': False}, {'mql': 'Text_size', 'py': 'Text_size', 'param': 'Text_size', 'type': 'int', 'default': 8, 'label': 'Text Size', 'sinput': False}, {'mql': 'Text_font', 'py': 'Text_font', 'param': None, 'type': 'string', 'default': 'Courier New', 'label': 'Text Font', 'sinput': False}, {'mql': 'Text_color', 'py': 'Text_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Text Color', 'sinput': False}, {'mql': 'color_support_weak', 'py': 'color_support_weak', 'param': None, 'type': 'color', 'default': 5197615, 'label': 'Color for weak support zone', 'sinput': False}, {'mql': 'color_support_untested', 'py': 'color_support_untested', 'param': None, 'type': 'color', 'default': 5737262, 'label': 'Color for untested support zone', 'sinput': False}, {'mql': 'color_support_verified', 'py': 'color_support_verified', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Color for verified support zone', 'sinput': False}, {'mql': 'color_support_proven', 'py': 'color_support_proven', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Color for proven support zone', 'sinput': False}, {'mql': 'color_support_turncoat', 'py': 'color_support_turncoat', 'param': None, 'type': 'color', 'default': 2330219, 'label': 'Color for turncoat(broken) support zone', 'sinput': False}, {'mql': 'color_resist_weak', 'py': 'color_resist_weak', 'param': None, 'type': 'color', 'default': 8519755, 'label': 'Color for weak resistance zone', 'sinput': False}, {'mql': 'color_resist_untested', 'py': 'color_resist_untested', 'param': None, 'type': 'color', 'default': 14053594, 'label': 'Color for untested resistance zone', 'sinput': False}, {'mql': 'color_resist_verified', 'py': 'color_resist_verified', 'param': None, 'type': 'color', 'default': 3937500, 'label': 'Color for verified resistance zone', 'sinput': False}, {'mql': 'color_resist_proven', 'py': 'color_resist_proven', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color for proven resistance zone', 'sinput': False}, {'mql': 'color_resist_turncoat', 'py': 'color_resist_turncoat', 'param': None, 'type': 'color', 'default': 36095, 'label': 'Color for broken resistance zone', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Timeframe = _input('Timeframe', PERIOD_CURRENT)  # Timeframe
BackLimit = _input('BackLimit', 1000)  # Back Limit
HistoryMode = _input('HistoryMode', False)  # History Mode (with double click)
zone_settings = _input('zone_settings', '--- Zone Settings ---')
zone_show_weak = _input('zone_show_weak', False)  # Show Weak Zones
zone_show_untested = _input('zone_show_untested', True)  # Show Untested Zones
zone_show_turncoat = _input('zone_show_turncoat', True)  # Show Broken Zones
zone_fuzzfactor = _input('zone_fuzzfactor', 0.75)  # Zone ATR Factor
zone_merge = _input('zone_merge', True)  # Zone Merge
zone_extend = _input('zone_extend', True)  # Zone Extend
fractal_fast_factor = _input('fractal_fast_factor', 3.0)  # Fractal Fast Factor
fractal_slow_factor = _input('fractal_slow_factor', 6.0)  # Fractal slow Factor
alert_settings = _input('alert_settings', '--- Alert Settings ---')
zone_show_alerts = _input('zone_show_alerts', False)  # Trigger alert when entering a zone
zone_alert_popups = _input('zone_alert_popups', True)  # Show alert window
zone_alert_sounds = _input('zone_alert_sounds', True)  # Play alert sound
zone_send_notification = _input('zone_send_notification', False)  # Send notification when entering a zone
zone_alert_waitseconds = _input('zone_alert_waitseconds', 300)  # Delay between alerts (seconds)
drawing_settings = _input('drawing_settings', '--- Drawing Settings ---')
string_prefix = _input('string_prefix', 'SRRR')  # Change prefix to add multiple indicators to chart
zone_solid = _input('zone_solid', True)  # Fill zone with color
zone_linewidth = _input('zone_linewidth', 1)  # Zone border width
zone_style = _input('zone_style', STYLE_SOLID)  # Zone border style
zone_show_info = _input('zone_show_info', True)  # Show info labels
zone_label_shift = _input('zone_label_shift', 10)  # Info label shift
sup_name = _input('sup_name', 'Sup')  # Support Name
res_name = _input('res_name', 'Res')  # Resistance Name
test_name = _input('test_name', 'Retests')  # Retest Name
Text_size = _input('Text_size', 8)  # Text Size
Text_font = _input('Text_font', 'Courier New')  # Text Font
Text_color = _input('Text_color', clrBlack)  # Text Color
color_support_weak = _input('color_support_weak', clrDarkSlateGray)  # Color for weak support zone
color_support_untested = _input('color_support_untested', clrSeaGreen)  # Color for untested support zone
color_support_verified = _input('color_support_verified', clrGreen)  # Color for verified support zone
color_support_proven = _input('color_support_proven', clrLimeGreen)  # Color for proven support zone
color_support_turncoat = _input('color_support_turncoat', clrOliveDrab)  # Color for turncoat(broken) support zone
color_resist_weak = _input('color_resist_weak', clrIndigo)  # Color for weak resistance zone
color_resist_untested = _input('color_resist_untested', clrOrchid)  # Color for untested resistance zone
color_resist_verified = _input('color_resist_verified', clrCrimson)  # Color for verified resistance zone
color_resist_proven = _input('color_resist_proven', clrRed)  # Color for proven resistance zone
color_resist_turncoat = _input('color_resist_turncoat', clrDarkOrange)  # Color for broken resistance zone
timeframe = 0
FastDnPts = Arr(0, 0.0)
FastUpPts = Arr(0, 0.0)
SlowDnPts = Arr(0, 0.0)
SlowUpPts = Arr(0, 0.0)
zone_hi = Arr(1000, 0.0, dyn=False)
zone_lo = Arr(1000, 0.0, dyn=False)
zone_start = Arr(1000, 0, dyn=False)
zone_hits = Arr(1000, 0, dyn=False)
zone_type = Arr(1000, 0, dyn=False)
zone_strength = Arr(1000, 0, dyn=False)
zone_count = 0
zone_turn = Arr(1000, False, dyn=False)
time_offset = 0
ner_lo_zone_P1 = Arr(0, 0.0)
ner_lo_zone_P2 = Arr(0, 0.0)
ner_hi_zone_P1 = Arr(0, 0.0)
ner_hi_zone_P2 = Arr(0, 0.0)
ner_hi_zone_strength = Arr(0, 0.0)
ner_lo_zone_strength = Arr(0, 0.0)
ner_price_inside_zone = Arr(0, 0.0)
iATR_handle = 0
ATR = Arr(0, 0.0)
cnt = 0
try_again = False
comment = 'Updating Chart...'
prefix = ""

def OnInit():
    global iATR_handle, prefix, timeframe
    prefix = string_prefix + '#'
    if Timeframe == PERIOD_CURRENT:
        timeframe = Period()
    else:
        timeframe = Timeframe
    iATR_handle = iATR(None, timeframe, 7)
    SetIndexBuffer(0, SlowDnPts, INDICATOR_DATA)
    SetIndexBuffer(1, SlowUpPts, INDICATOR_DATA)
    SetIndexBuffer(2, FastDnPts, INDICATOR_DATA)
    SetIndexBuffer(3, FastUpPts, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_NONE)
    SetIndexBuffer(4, ner_hi_zone_P1, INDICATOR_DATA)
    SetIndexBuffer(5, ner_hi_zone_P2, INDICATOR_DATA)
    SetIndexBuffer(6, ner_lo_zone_P1, INDICATOR_DATA)
    SetIndexBuffer(7, ner_lo_zone_P2, INDICATOR_DATA)
    SetIndexBuffer(8, ner_hi_zone_strength, INDICATOR_DATA)
    SetIndexBuffer(9, ner_lo_zone_strength, INDICATOR_DATA)
    SetIndexBuffer(10, ner_price_inside_zone, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(6, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(7, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(8, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(9, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(10, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetString(4, PLOT_LABEL, 'Resistant Zone High')
    PlotIndexSetString(5, PLOT_LABEL, 'Resistant Zone Low')
    PlotIndexSetString(6, PLOT_LABEL, 'Support Zone High')
    PlotIndexSetString(7, PLOT_LABEL, 'Support Zone Low')
    PlotIndexSetString(8, PLOT_LABEL, 'Resistant Zone Strength')
    PlotIndexSetString(9, PLOT_LABEL, 'Support Zone Strength')
    PlotIndexSetString(10, PLOT_LABEL, 'Price Inside Zone')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(9, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(10, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(SlowDnPts, True)
    ArraySetAsSeries(SlowUpPts, True)
    ArraySetAsSeries(FastDnPts, True)
    ArraySetAsSeries(FastUpPts, True)
    ArraySetAsSeries(ner_hi_zone_P1, True)
    ArraySetAsSeries(ner_hi_zone_P2, True)
    ArraySetAsSeries(ner_lo_zone_P1, True)
    ArraySetAsSeries(ner_lo_zone_P2, True)
    ArraySetAsSeries(ner_hi_zone_strength, True)
    ArraySetAsSeries(ner_lo_zone_strength, True)
    ArraySetAsSeries(ner_price_inside_zone, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    DeleteZones()
    if StringFind(ChartGetString(0, CHART_COMMENT), comment) >= 0:
        Comment('')
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if NewBar() == True or (timeframe != PERIOD_CURRENT and try_again == True):
        old_zone_count = zone_count
        FastFractals()
        SlowFractals()
        DeleteZones()
        FindZones()
        DrawZones()
        if zone_show_info == True:
            showLabels()
    CheckAlerts()
    return rates_total

def CheckAlerts():
    global _s_CheckAlerts_lastalert
    if zone_show_alerts == False and zone_send_notification == False:
        return
    Time = Arr(0, 0)
    if CopyTime(Symbol(), timeframe, 0, 1, Time) == -1:
        return
    ArraySetAsSeries(Time, True)
    if (Time[0] - _s_CheckAlerts_lastalert) > zone_alert_waitseconds:
        if CheckEntryAlerts() == True:
            _s_CheckAlerts_lastalert = _int(Time[0])

def CheckEntryAlerts():
    Close = Arr(0, 0.0)
    ArraySetAsSeries(Close, True)
    CopyClose(Symbol(), timeframe, 0, 1, Close)
    i = 0
    while i < zone_count:
        if zone_strength[i] == 0 and zone_show_weak == False:
            i += 1
            continue
        if zone_strength[i] == 2 and zone_show_untested == False:
            i += 1
            continue
        if zone_strength[i] == 1 and zone_show_turncoat == False:
            i += 1
            continue
        if Close[0] >= zone_lo[i] and Close[0] < zone_hi[i]:
            if zone_show_alerts == True:
                if zone_alert_popups == True:
                    if zone_type[i] == 1:
                        Alert(Symbol() + ' ' + TFTS(timeframe) + ': Support Zone Entered.')
                    else:
                        Alert(Symbol() + ' ' + TFTS(timeframe) + ': Resistance Zone Entered.')
                if zone_alert_sounds == True:
                    PlaySound('alert.wav')
            if zone_send_notification == True:
                if zone_type[i] == 1:
                    SendNotification(Symbol() + ' ' + TFTS(timeframe) + ': Support Zone Entered.')
                else:
                    SendNotification(Symbol() + ' ' + TFTS(timeframe) + ': Resistance Zone Entered.')
            return True
        i += 1
    return False

def FindZones():
    global try_again, zone_count
    i = 0
    j = 0
    shift = 0
    bustcount = 0
    testcount = 0
    hival = 0.0
    loval = 0.0
    turned = False
    hasturned = False
    temp_hi = Arr(1000, 0.0, dyn=False)
    temp_lo = Arr(1000, 0.0, dyn=False)
    temp_start = Arr(1000, 0, dyn=False)
    temp_hits = Arr(1000, 0, dyn=False)
    temp_strength = Arr(1000, 0, dyn=False)
    temp_count = 0
    temp_turn = Arr(1000, False, dyn=False)
    temp_merge = Arr(1000, False, dyn=False)
    merge1 = Arr(1000, 0, dyn=False)
    merge2 = Arr(1000, 0, dyn=False)
    merge_count = 0
    shift = MathMin(Bars(Symbol(), timeframe) - 1, BackLimit + cnt)
    shift = MathMin(shift, ArraySize(FastUpPts) - 1)
    Close = Arr(0, 0.0)
    High = Arr(0, 0.0)
    Low = Arr(0, 0.0)
    ArraySetAsSeries(Close, True)
    CopyClose(Symbol(), timeframe, 0, shift + 1, Close)
    ArraySetAsSeries(High, True)
    CopyHigh(Symbol(), timeframe, 0, shift + 1, High)
    ArraySetAsSeries(Low, True)
    CopyLow(Symbol(), timeframe, 0, shift + 1, Low)
    ArraySetAsSeries(ATR, True)
    if CopyBuffer(iATR_handle, 0, 0, shift + 1, ATR) == -1:
        try_again = True
        Comment(comment)
        return
    else:
        if StringFind(ChartGetString(0, CHART_COMMENT), comment) >= 0:
            Comment('')
        try_again = False
    for ii in range(shift, cnt + 5, -1):
        atr = ATR[ii]
        fu = (atr / 2) * zone_fuzzfactor
        isWeak = False
        touchOk = False
        isBust = False
        if FastUpPts[ii] > 0.001:
            isWeak = True
            if SlowUpPts[ii] > 0.001:
                isWeak = False
            hival = High[ii]
            if zone_extend == True:
                hival += fu
            loval = MathMax(MathMin(Close[ii], High[ii] - fu), High[ii] - (fu * 2))
            turned = False
            hasturned = False
            isBust = False
            bustcount = 0
            testcount = 0
            i = ii - 1
            for i in range(i, cnt + 0 - 1, -1):
                if ((turned == False and FastUpPts[i] >= loval) and FastUpPts[i] <= hival) or ((turned == True and FastDnPts[i] <= hival) and FastDnPts[i] >= loval):
                    touchOk = True
                    j = i + 1
                    for j in range(j, i + 11):
                        if ((turned == False and FastUpPts[j] >= loval) and FastUpPts[j] <= hival) or ((turned == True and FastDnPts[j] <= hival) and FastDnPts[j] >= loval):
                            touchOk = False
                            break
                    else:
                        j = _range_end(j, i + 11, 1)
                    if touchOk == True:
                        bustcount = 0
                        testcount += 1
                if (turned == False and High[i] > hival) or (turned == True and Low[i] < loval):
                    bustcount += 1
                    if bustcount > 1 or isWeak == True:
                        isBust = True
                        break
                    if turned == True:
                        turned = False
                    elif turned == False:
                        turned = True
                    hasturned = True
                    testcount = 0
            else:
                i = _range_end(i, cnt + 0 - 1, -1)
            if isBust == False:
                temp_hi[temp_count] = hival
                temp_lo[temp_count] = loval
                temp_turn[temp_count] = hasturned
                temp_hits[temp_count] = testcount
                temp_start[temp_count] = ii
                temp_merge[temp_count] = False
                if testcount > 3:
                    temp_strength[temp_count] = 4
                elif testcount > 0:
                    temp_strength[temp_count] = 3
                elif hasturned == True:
                    temp_strength[temp_count] = 1
                elif isWeak == False:
                    temp_strength[temp_count] = 2
                else:
                    temp_strength[temp_count] = 0
                temp_count += 1
        elif FastDnPts[ii] > 0.001:
            isWeak = True
            if SlowDnPts[ii] > 0.001:
                isWeak = False
            loval = Low[ii]
            if zone_extend == True:
                loval -= fu
            hival = MathMin(MathMax(Close[ii], Low[ii] + fu), Low[ii] + (fu * 2))
            turned = False
            hasturned = False
            bustcount = 0
            testcount = 0
            isBust = False
            i = ii - 1
            for i in range(i, cnt + 0 - 1, -1):
                if ((turned == True and FastUpPts[i] >= loval) and FastUpPts[i] <= hival) or ((turned == False and FastDnPts[i] <= hival) and FastDnPts[i] >= loval):
                    touchOk = True
                    j = i + 1
                    for j in range(j, i + 11):
                        if ((turned == True and FastUpPts[j] >= loval) and FastUpPts[j] <= hival) or ((turned == False and FastDnPts[j] <= hival) and FastDnPts[j] >= loval):
                            touchOk = False
                            break
                    else:
                        j = _range_end(j, i + 11, 1)
                    if touchOk == True:
                        bustcount = 0
                        testcount += 1
                if (turned == True and High[i] > hival) or (turned == False and Low[i] < loval):
                    bustcount += 1
                    if bustcount > 1 or isWeak == True:
                        isBust = True
                        break
                    if turned == True:
                        turned = False
                    elif turned == False:
                        turned = True
                    hasturned = True
                    testcount = 0
            else:
                i = _range_end(i, cnt + 0 - 1, -1)
            if isBust == False:
                temp_hi[temp_count] = hival
                temp_lo[temp_count] = loval
                temp_turn[temp_count] = hasturned
                temp_hits[temp_count] = testcount
                temp_start[temp_count] = ii
                temp_merge[temp_count] = False
                if testcount > 3:
                    temp_strength[temp_count] = 4
                elif testcount > 0:
                    temp_strength[temp_count] = 3
                elif hasturned == True:
                    temp_strength[temp_count] = 1
                elif isWeak == False:
                    temp_strength[temp_count] = 2
                else:
                    temp_strength[temp_count] = 0
                temp_count += 1
    if zone_merge == True:
        merge_count = 1
        iterations = 0
        while merge_count > 0 and iterations < 3:
            merge_count = 0
            iterations += 1
            i = 0
            for i in range(i, temp_count):
                temp_merge[i] = False
            else:
                i = _range_end(i, temp_count, 1)
            i = 0
            for i in range(i, temp_count - 1):
                if temp_hits[i] == -1 or temp_merge[i] == True:
                    continue
                j = i + 1
                for j in range(j, temp_count):
                    if temp_hits[j] == -1 or temp_merge[j] == True:
                        continue
                    if (((temp_hi[i] >= temp_lo[j] and temp_hi[i] <= temp_hi[j]) or (temp_lo[i] <= temp_hi[j] and temp_lo[i] >= temp_lo[j])) or (temp_hi[j] >= temp_lo[i] and temp_hi[j] <= temp_hi[i])) or (temp_lo[j] <= temp_hi[i] and temp_lo[j] >= temp_lo[i]):
                        merge1[merge_count] = i
                        merge2[merge_count] = j
                        temp_merge[i] = True
                        temp_merge[j] = True
                        merge_count += 1
                else:
                    j = _range_end(j, temp_count, 1)
            else:
                i = _range_end(i, temp_count - 1, 1)
            i = 0
            for i in range(i, merge_count):
                target = merge1[i]
                source = merge2[i]
                temp_hi[target] = MathMax(temp_hi[target], temp_hi[source])
                temp_lo[target] = MathMin(temp_lo[target], temp_lo[source])
                temp_hits[target] += temp_hits[source]
                temp_start[target] = MathMax(temp_start[target], temp_start[source])
                temp_strength[target] = MathMax(temp_strength[target], temp_strength[source])
                if temp_hits[target] > 3:
                    temp_strength[target] = 4
                if temp_hits[target] == 0 and temp_turn[target] == False:
                    temp_hits[target] = 1
                    if temp_strength[target] < 3:
                        temp_strength[target] = 3
                if temp_turn[target] == False or temp_turn[source] == False:
                    temp_turn[target] = False
                if temp_turn[target] == True:
                    temp_hits[target] = 0
                temp_hits[source] = -1
            else:
                i = _range_end(i, merge_count, 1)
    zone_count = 0
    i = 0
    for i in range(i, temp_count):
        if temp_hits[i] >= 0 and zone_count < 1000:
            zone_hi[zone_count] = temp_hi[i]
            zone_lo[zone_count] = temp_lo[i]
            zone_hits[zone_count] = temp_hits[i]
            zone_turn[zone_count] = temp_turn[i]
            zone_start[zone_count] = temp_start[i]
            zone_strength[zone_count] = temp_strength[i]
            if zone_hi[zone_count] < Close[cnt + 0]:
                zone_type[zone_count] = 1
            elif zone_lo[zone_count] > Close[cnt + 0]:
                zone_type[zone_count] = 2
            else:
                sh = MathMin(Bars(Symbol(), timeframe) - 1, BackLimit + cnt)
                j = cnt + 1
                for j in range(j, sh):
                    if Close[j] < zone_lo[zone_count]:
                        zone_type[zone_count] = 2
                        break
                    elif Close[j] > zone_hi[zone_count]:
                        zone_type[zone_count] = 1
                        break
                else:
                    j = _range_end(j, sh, 1)
                if j == sh:
                    zone_type[zone_count] = 1
            zone_count += 1
    else:
        i = _range_end(i, temp_count, 1)

def DrawZones():
    lower_nerest_zone_P1 = 0.0
    lower_nerest_zone_P2 = 0.0
    higher_nerest_zone_P1 = 99999.0
    higher_nerest_zone_P2 = 99999.0
    higher_zone_type = 0.0
    higher_zone_strength = 0.0
    lower_zone_type = 0.0
    lower_zone_strength = 0.0
    for i in range(0, zone_count):
        if zone_strength[i] == 0 and zone_show_weak == False:
            continue
        if zone_strength[i] == 2 and zone_show_untested == False:
            continue
        if zone_strength[i] == 1 and zone_show_turncoat == False:
            continue
        s = ""
        if zone_type[i] == 1:
            s = prefix + 'S' + _str(i) + ' Strength='
        else:
            s = prefix + 'R' + _str(i) + ' Strength='
        if zone_strength[i] == 4:
            s = s + 'Proven, Test Count=' + _str(zone_hits[i])
        elif zone_strength[i] == 3:
            s = s + 'Verified, Test Count=' + _str(zone_hits[i])
        elif zone_strength[i] == 2:
            s = s + 'Untested'
        elif zone_strength[i] == 1:
            s = s + 'Turncoat'
        else:
            s = s + 'Weak'
        Time = Arr(0, 0)
        if CopyTime(Symbol(), timeframe, 0, zone_start[i] + 1, Time) == -1:
            Comment(comment)
            return
        else:
            if StringFind(ChartGetString(0, CHART_COMMENT), comment) >= 0:
                Comment('')
        ArraySetAsSeries(Time, True)
        current_time = 0
        start_time = 0
        if cnt == 0:
            current_time = iTime(None, 0, 0)
        else:
            current_time = Time[cnt + 0]
        if iTime(None, 0, TerminalInfoInteger(TERMINAL_MAXBARS) - 1) > Time[zone_start[i]]:
            start_time = iTime(None, 0, TerminalInfoInteger(TERMINAL_MAXBARS) - 1)
        else:
            start_time = Time[zone_start[i]]
        ObjectCreate(0, s, OBJ_RECTANGLE, 0, 0, 0, 0, 0)
        ObjectSetInteger(0, s, OBJPROP_TIME, 0, start_time)
        ObjectSetInteger(0, s, OBJPROP_TIME, 1, current_time)
        ObjectSetDouble(0, s, OBJPROP_PRICE, 0, zone_hi[i])
        ObjectSetDouble(0, s, OBJPROP_PRICE, 1, zone_lo[i])
        ObjectSetInteger(0, s, OBJPROP_BACK, True)
        ObjectSetInteger(0, s, OBJPROP_FILL, zone_solid)
        ObjectSetInteger(0, s, OBJPROP_WIDTH, zone_linewidth)
        ObjectSetInteger(0, s, OBJPROP_STYLE, zone_style)
        if zone_type[i] == 1:
            if zone_strength[i] == 1:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_support_turncoat)
            elif zone_strength[i] == 4:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_support_proven)
            elif zone_strength[i] == 3:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_support_verified)
            elif zone_strength[i] == 2:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_support_untested)
            else:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_support_weak)
        else:
            if zone_strength[i] == 1:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_resist_turncoat)
            elif zone_strength[i] == 4:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_resist_proven)
            elif zone_strength[i] == 3:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_resist_verified)
            elif zone_strength[i] == 2:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_resist_untested)
            else:
                ObjectSetInteger(0, s, OBJPROP_COLOR, color_resist_weak)
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
        if zone_lo[i] > lower_nerest_zone_P2 and price > zone_lo[i]:
            lower_nerest_zone_P1 = zone_hi[i]
            lower_nerest_zone_P2 = zone_lo[i]
            higher_zone_type = zone_type[i]
            lower_zone_strength = zone_strength[i]
        if zone_hi[i] < higher_nerest_zone_P1 and price < zone_hi[i]:
            higher_nerest_zone_P1 = zone_hi[i]
            higher_nerest_zone_P2 = zone_lo[i]
            lower_zone_type = zone_type[i]
            higher_zone_strength = zone_strength[i]
    ner_hi_zone_P1[0] = higher_nerest_zone_P1
    ner_hi_zone_P2[0] = higher_nerest_zone_P2
    ner_lo_zone_P1[0] = lower_nerest_zone_P1
    ner_lo_zone_P2[0] = lower_nerest_zone_P2
    ner_hi_zone_strength[0] = higher_zone_strength
    ner_lo_zone_strength[0] = lower_zone_strength
    if ner_hi_zone_P1[0] == ner_lo_zone_P1[0]:
        ner_price_inside_zone[0] = higher_zone_type
    else:
        ner_price_inside_zone[0] = 0.0

def Fractal(M, P, shift):
    if timeframe > P:
        P = timeframe
    P = _int((_idiv(P, timeframe) * 2) + MathCeil(_idiv(_idiv(P, timeframe), 2)))
    if shift < P:
        return False
    if shift > (Bars(Symbol(), timeframe) - P - 1):
        return False
    High = Arr(0, 0.0)
    Low = Arr(0, 0.0)
    ArraySetAsSeries(High, True)
    CopyHigh(Symbol(), timeframe, 0, shift + P + 1, High)
    ArraySetAsSeries(Low, True)
    CopyLow(Symbol(), timeframe, 0, shift + P + 1, Low)
    for i in range(1, P + 1):
        if M == 1:
            if High[shift + i] > High[shift]:
                return False
            if High[shift - i] >= High[shift]:
                return False
        if M == -1:
            if Low[shift + i] < Low[shift]:
                return False
            if Low[shift - i] <= Low[shift]:
                return False
    return True

def NewBar():
    global _s_NewBar_LastTime
    if (iTime(Symbol(), timeframe, 0) + time_offset) != _s_NewBar_LastTime:
        _s_NewBar_LastTime = iTime(Symbol(), timeframe, 0) + time_offset
        return True
    else:
        return False

def DeleteZones():
    len_ = StringLen(prefix)
    i = 0
    while i < ObjectsTotal(0, 0, -1):
        objName = ObjectName(0, i, 0, -1)
        if StringSubstr(objName, 0, len_) != prefix:
            i += 1
            continue
        ObjectDelete(0, objName)

def TFTS(tf):
    tfs = ""
    _sw1 = tf
    if _sw1 == PERIOD_M1:
        tfs = 'M1'
    elif _sw1 == PERIOD_M2:
        tfs = 'M2'
    elif _sw1 == PERIOD_M3:
        tfs = 'M3'
    elif _sw1 == PERIOD_M4:
        tfs = 'M4'
    elif _sw1 == PERIOD_M5:
        tfs = 'M5'
    elif _sw1 == PERIOD_M6:
        tfs = 'M6'
    elif _sw1 == PERIOD_M10:
        tfs = 'M10'
    elif _sw1 == PERIOD_M12:
        tfs = 'M12'
    elif _sw1 == PERIOD_M15:
        tfs = 'M15'
    elif _sw1 == PERIOD_M20:
        tfs = 'M20'
    elif _sw1 == PERIOD_M30:
        tfs = 'M30'
    elif _sw1 == PERIOD_H1:
        tfs = 'H1'
    elif _sw1 == PERIOD_H2:
        tfs = 'H2'
    elif _sw1 == PERIOD_H3:
        tfs = 'H3'
    elif _sw1 == PERIOD_H4:
        tfs = 'H4'
    elif _sw1 == PERIOD_H6:
        tfs = 'H6'
    elif _sw1 == PERIOD_H8:
        tfs = 'H8'
    elif _sw1 == PERIOD_H12:
        tfs = 'H12'
    elif _sw1 == PERIOD_D1:
        tfs = 'D1'
    elif _sw1 == PERIOD_W1:
        tfs = 'W1'
    elif _sw1 == PERIOD_MN1:
        tfs = 'MN1'
    return tfs

def FastFractals():
    shift = 0
    limit = MathMin(Bars(Symbol(), timeframe) - 1, BackLimit + cnt)
    limit = MathMin(limit, ArraySize(FastUpPts) - 1)
    P1 = _int(timeframe * fractal_fast_factor)
    High = Arr(0, 0.0)
    Low = Arr(0, 0.0)
    ArraySetAsSeries(High, True)
    CopyHigh(Symbol(), timeframe, 0, limit + 1, High)
    ArraySetAsSeries(Low, True)
    CopyLow(Symbol(), timeframe, 0, limit + 1, Low)
    FastUpPts[0] = 0.0
    FastUpPts[1] = 0.0
    FastDnPts[0] = 0.0
    FastDnPts[1] = 0.0
    shift = limit
    while shift > (cnt + 1):
        if Fractal(1, P1, shift) == True:
            FastUpPts[shift] = High[shift]
        else:
            FastUpPts[shift] = 0.0
        if Fractal(-1, P1, shift) == True:
            FastDnPts[shift] = Low[shift]
        else:
            FastDnPts[shift] = 0.0
        shift -= 1

def SlowFractals():
    shift = 0
    limit = MathMin(Bars(Symbol(), timeframe) - 1, BackLimit + cnt)
    limit = MathMin(limit, ArraySize(SlowUpPts) - 1)
    P2 = _int(timeframe * fractal_slow_factor)
    High = Arr(0, 0.0)
    Low = Arr(0, 0.0)
    ArraySetAsSeries(High, True)
    CopyHigh(Symbol(), timeframe, 0, limit + 1, High)
    ArraySetAsSeries(Low, True)
    CopyLow(Symbol(), timeframe, 0, limit + 1, Low)
    SlowUpPts[0] = 0.0
    SlowUpPts[1] = 0.0
    SlowDnPts[0] = 0.0
    SlowDnPts[1] = 0.0
    shift = limit
    while shift > (cnt + 1):
        if Fractal(1, P2, shift) == True:
            SlowUpPts[shift] = High[shift]
        else:
            SlowUpPts[shift] = 0.0
        if Fractal(-1, P2, shift) == True:
            SlowDnPts[shift] = Low[shift]
        else:
            SlowDnPts[shift] = 0.0
        ner_hi_zone_P1[shift] = 0.0
        ner_hi_zone_P2[shift] = 0.0
        ner_lo_zone_P1[shift] = 0.0
        ner_lo_zone_P2[shift] = 0.0
        ner_hi_zone_strength[shift] = 0.0
        ner_lo_zone_strength[shift] = 0.0
        ner_price_inside_zone[shift] = 0.0
        shift -= 1

def OnChartEvent(id_, lparam, dparam, sparam):
    global _s_OnChartEvent_clickTimeMemory, cnt
    if HistoryMode == True:
        if id_ == CHARTEVENT_CLICK:
            clickTime = GetTickCount()
            if clickTime < (_s_OnChartEvent_clickTimeMemory + 500):
                _s_OnChartEvent_clickTimeMemory = 0
                x = _int(lparam)
                y = _int(dparam)
                dt = Box(0)
                price = Box(0.0)
                window = Box(0)
                if ChartXYToTimePrice(0, x, y, window, dt, price):
                    cnt = iBarShift(Symbol(), timeframe, dt.v, False)
                    old_zone_count = zone_count
                    FastFractals()
                    SlowFractals()
                    DeleteZones()
                    FindZones()
                    DrawZones()
                    showLabels()
                    ChartRedraw(0)
            else:
                _s_OnChartEvent_clickTimeMemory = clickTime
        elif id_ == CHARTEVENT_MOUSE_MOVE:
            pass
        elif id_ == CHARTEVENT_KEYDOWN:
            return

def showLabels():
    Time = iTime(None, timeframe, cnt)
    for i in range(0, zone_count):
        lbl = ""
        if zone_strength[i] == 4:
            lbl = 'Proven'
        elif zone_strength[i] == 3:
            lbl = 'Verified'
        elif zone_strength[i] == 2:
            lbl = 'Untested'
        elif zone_strength[i] == 1:
            lbl = 'Turncoat'
        else:
            lbl = 'Weak'
        if zone_type[i] == 1:
            lbl = lbl + ' ' + sup_name
        else:
            lbl = lbl + ' ' + res_name
        if zone_hits[i] > 0 and zone_strength[i] > 2:
            if zone_hits[i] == 1:
                lbl = lbl + ', ' + test_name + '=' + _str(zone_hits[i])
            else:
                lbl = lbl + ', ' + test_name + '=' + _str(zone_hits[i])
        adjust_hpos = 0
        wbpc = ChartGetInteger(0, CHART_VISIBLE_BARS)
        k = _idiv(PeriodSeconds(timeframe), 10) + StringLen(lbl)
        if wbpc < 80:
            adjust_hpos = _int(Time) + (k * 1)
        elif wbpc < 125:
            adjust_hpos = _int(Time) + (k * 2)
        elif wbpc < 250:
            adjust_hpos = _int(Time) + (k * 4)
        elif wbpc < 480:
            adjust_hpos = _int(Time) + (k * 8)
        elif wbpc < 950:
            adjust_hpos = _int(Time) + (k * 16)
        else:
            adjust_hpos = _int(Time) + (k * 32)
        shift = k * zone_label_shift
        vpos = zone_hi[i] - ((zone_hi[i] - zone_lo[i]) / 3)
        if zone_strength[i] == 0 and zone_show_weak == False:
            continue
        if zone_strength[i] == 2 and zone_show_untested == False:
            continue
        if zone_strength[i] == 1 and zone_show_turncoat == False:
            continue
        s = prefix + _str(i) + 'LBL'
        ObjectCreate(0, s, OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, s, OBJPROP_TIME, adjust_hpos + shift)
        ObjectSetDouble(0, s, OBJPROP_PRICE, vpos)
        ObjectSetString(0, s, OBJPROP_TEXT, lbl)
        ObjectSetString(0, s, OBJPROP_FONT, Text_font)
        ObjectSetInteger(0, s, OBJPROP_FONTSIZE, Text_size)
        ObjectSetInteger(0, s, OBJPROP_COLOR, Text_color)

# ---- static local variables
_s_CheckAlerts_lastalert = 0
_s_NewBar_LastTime = 0
_s_OnChartEvent_clickTimeMemory = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ShvedSupplyAndDemandV17(_MQL5Indicator):
    name = 'shved_supply_and_demand_v1.7'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe
        'BackLimit': 1000,  # Back Limit
        'HistoryMode': False,  # History Mode (with double click)
        'zone_show_weak': False,  # Show Weak Zones
        'zone_show_untested': True,  # Show Untested Zones
        'zone_show_turncoat': True,  # Show Broken Zones
        'zone_fuzzfactor': 0.75,  # Zone ATR Factor
        'zone_merge': True,  # Zone Merge
        'zone_extend': True,  # Zone Extend
        'fractal_fast_factor': 3.0,  # Fractal Fast Factor
        'fractal_slow_factor': 6.0,  # Fractal slow Factor
        'zone_show_alerts': False,  # Trigger alert when entering a zone
        'zone_alert_popups': True,  # Show alert window
        'zone_alert_sounds': True,  # Play alert sound
        'zone_send_notification': False,  # Send notification when entering a zone
        'zone_alert_waitseconds': 300,  # Delay between alerts (seconds)
        'zone_solid': True,  # Fill zone with color
        'zone_linewidth': 1,  # Zone border width
        'zone_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Zone border style
        'zone_show_info': True,  # Show info labels
        'zone_label_shift': 10,  # Info label shift
        'Text_size': 8,  # Text Size
    }

