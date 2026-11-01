"""FiboPivotCandleBarMT5 — converted from MQL5: MQL5 Indicators/FiboPivotCandleBarMT5/FiboPivotCandleBarMT5.mq5

FiboPivotCandleBar MetaTrader 5 is a composite of several forex indicators, Fibonacci,
Pivot Point, ZigZag, MACD and Moving Average which are combined in this indicator.
This indicator gives advice to buy and sell with the direction of the arrow.
version: 2.0 ~ Last update: 2020/04/15 @ 12:00 PM WIT (Western Indonesian Time)
Copyright: Copyright 2017, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2017/01/12; Link: https://www.mql5.com/en/users/3rjfx; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2017, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2017/01/12', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 0}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['FiboPivotCandleBar MetaTrader 5 is a composite of several forex indicators, Fibonacci,', 'Pivot Point, ZigZag, MACD and Moving Average which are combined in this indicator.', 'This indicator gives advice to buy and sell with the direction of the arrow.', 'version: 2.0 ~ Last update: 2020/04/15 @ 12:00 PM WIT (Western Indonesian Time)'], 'name': 'FiboPivotCandleBarMT5', 'source': 'MQL5 Indicators/FiboPivotCandleBarMT5/FiboPivotCandleBarMT5.mq5', 'folder': 'FiboPivotCandleBarMT5', 'inputs': [{'mql': 'MsgAlerts', 'py': 'MsgAlerts', 'param': 'MsgAlerts', 'type': 'int', 'default': 1, 'label': 'Activate Alert (Yes) or (No)', 'sinput': False}, {'mql': 'eMailAlerts', 'py': 'eMailAlerts', 'param': 'eMailAlerts', 'type': 'int', 'default': 0, 'label': 'Send Email Alert (Yes) or (No)', 'sinput': False}, {'mql': 'UseSendnotify', 'py': 'UseSendnotify', 'param': 'UseSendnotify', 'type': 'int', 'default': 0, 'label': 'Send Notification (Yes) or (No)', 'sinput': False}, {'mql': 'Fonts_Model', 'py': 'Fonts_Model', 'param': 'Fonts_Model', 'type': 'int', 'default': 1, 'label': 'Choose Fonts Model', 'sinput': False}, {'mql': 'FontColors', 'py': 'FontColors', 'param': None, 'type': 'color', 'default': 16448255, 'label': 'colors for font', 'sinput': False}, {'mql': 'BarUp', 'py': 'BarUp', 'param': None, 'type': 'color', 'default': 16448255, 'label': 'color for Bar_Up and Bull Candle', 'sinput': False}, {'mql': 'BarDown', 'py': 'BarDown', 'param': None, 'type': 'color', 'default': 255, 'label': 'color for Bar_Down and Bear Candle', 'sinput': False}, {'mql': 'LineGraph', 'py': 'LineGraph', 'param': None, 'type': 'color', 'default': 65535, 'label': 'color for Line Graph (if Price Close == Price Open)', 'sinput': False}, {'mql': 'EmptyBar', 'py': 'EmptyBar', 'param': None, 'type': 'color', 'default': 10061943, 'label': 'If the bar has not been passed by the price movement', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum fonts
Arial_Black = 0
Bodoni_MT_Black = 1
_enum('fonts', {0: 'Arial_Black', 1: 'Bodoni_MT_Black'})

# enum YN
No = 0
Yes = 1
_enum('YN', {0: 'No', 1: 'Yes'})

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
MsgAlerts = _input('MsgAlerts', Yes)  # Activate Alert (Yes) or (No)
eMailAlerts = _input('eMailAlerts', No)  # Send Email Alert (Yes) or (No)
UseSendnotify = _input('UseSendnotify', No)  # Send Notification (Yes) or (No)
Fonts_Model = _input('Fonts_Model', Bodoni_MT_Black)  # Choose Fonts Model
FontColors = _input('FontColors', clrSnow)  # colors for font
BarUp = _input('BarUp', clrSnow)  # color for Bar_Up and Bull Candle
BarDown = _input('BarDown', clrRed)  # color for Bar_Down and Bear Candle
LineGraph = _input('LineGraph', clrYellow)  # color for Line Graph (if Price Close == Price Open)
EmptyBar = _input('EmptyBar', clrLightSlateGray)  # If the bar has not been passed by the price movement
corner = CORNER_RIGHT_LOWER
distance_x = 157
distance_y = 47
digit = 0
csec = 0
psec = 0
prctick = 0
prcpxl = 170
arrpvt = 22
font_size = 8
font_size_OHLC = 7
font_color = 0
font_ohlc = ""
font_face = 'Arial'
Pvt = 0.0
PvtO = 0.0
PvtL = 0.0
PvtH = 0.0
PvtC = 0.0
PvtO1 = 0.0
PvtL1 = 0.0
PvtH1 = 0.0
PvtC1 = 0.0
pivot = Arr(0, 0.0)
fibolvl = Arr.of([0.0, 23.6, 38.2, 50.0, 61.8], fill=0.0)
label = Arr.of(['S8', 'S7', 'S6', 'S5', 'S4', 'S3', 'S2', 'SS1', 'S1', 'L20', 'L40', 'L60', 'L80', 'R1', 'SR1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8'], fill="")
Price_Up = Arr(0, 0.0)
Price_Dn = Arr(0, 0.0)
depth = 12  # Depth
devia = 5  # Deviation
backs = 3  # Backstep
level = 3  # recounting's depth of extremums
zh = 0
zl = 0
barh = 5
bars = 110
HiLo = 108
ExtZz = Arr(0, 0.0)
ExtHi = Arr(0, 0.0)
ExtLo = Arr(0, 0.0)
EMA5e02 = Arr(0, 0.0)
SMA5s20 = Arr(0, 0.0)
MAONs10 = Arr(0, 0.0)
MAONs62 = Arr(0, 0.0)
MACDM = Arr(0, 0.0)
MACDS = Arr(0, 0.0)
prhh = PERIOD_M30
prh1 = PERIOD_H1
prdp = 0
prfb = 0
cral = 0
pral = 0
crmnt = 0
prmnt = 0
ArrUp = False
ArrDn = False
h_iMa2 = 0
h_iMa20 = 0
h_Macd = 0
chart_id = 0
short_name = ""
alBase = ""
alSubj = ""
alMsg = ""

def OnInit():
    global chart_id, csec, digit, font_color, font_ohlc, h_Macd, h_iMa2, h_iMa20, prctick, prdp, prfb, psec, short_name
    SetIndexBuffer(0, Price_Up, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Price_Up')
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, True)
    SetIndexBuffer(1, Price_Dn, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'Price_Dn')
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    if Digits() == 3 or Digits() == 5:
        digit = Digits()
    else:
        digit = Digits() + 1
    csec = 0
    psec = -1
    chart_id = ChartID()
    font_ohlc = FontsModel(Fonts_Model)
    font_color = FontColors
    prctick = _idiv(prcpxl, 20) * arrpvt
    short_name = 'FiboPivotCandleBar'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '_(' + Symbol() + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, digit)
    if Period() == PERIOD_MN1:
        prdp = PERIOD_MN1
        prfb = PERIOD_D1
    if Period() == PERIOD_W1:
        prdp = PERIOD_W1
        prfb = PERIOD_H4
    if Period() <= PERIOD_D1:
        prdp = PERIOD_D1
        prfb = PERIOD_H1
    h_iMa2 = iMA(Symbol(), PERIOD_M15, 2, 0, MODE_EMA, PRICE_MEDIAN)
    if h_iMa2 == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA PERIOD_M15 indicator period 2 for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    h_iMa20 = iMA(Symbol(), PERIOD_M15, 20, 0, MODE_SMA, PRICE_MEDIAN)
    if h_iMa20 == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA PERIOD_M15 indicator period 20 for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    h_Macd = iMACD(Symbol(), prh1, 12, 26, 9, PRICE_CLOSE)
    if h_Macd == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMACD indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(chart_id, -1, -1)
    if h_iMa2 != INVALID_HANDLE:
        IndicatorRelease(h_iMa2)
    if h_iMa20 != INVALID_HANDLE:
        IndicatorRelease(h_iMa20)
    if h_Macd != INVALID_HANDLE:
        IndicatorRelease(h_Macd)
    Comment('')
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ArrDn, ArrUp, Pvt, PvtC, PvtC1, PvtH, PvtH1, PvtL, PvtL1, PvtO, PvtO1, cral, csec, psec
    ResetLastError()
    limit = 0
    cral = 0
    if rates_total < bars:
        return 0
    limit = rates_total - prev_calculated + 5
    if prev_calculated == 0:
        limit = bars
    if prev_calculated > 0:
        limit += 1
    if limit > bars:
        limit = bars
    ArrayResize(EMA5e02, limit)
    ArrayResize(SMA5s20, limit)
    ArrayResize(MAONs10, limit)
    ArrayResize(MAONs62, limit)
    ArrayResize(MACDM, limit)
    ArrayResize(MACDS, limit)
    ArrayResize(Price_Up, limit)
    ArrayResize(Price_Dn, limit)
    ArraySetAsSeries(Price_Up, True)
    ArraySetAsSeries(Price_Dn, True)
    ArraySetAsSeries(EMA5e02, True)
    ArraySetAsSeries(SMA5s20, True)
    ArraySetAsSeries(MAONs10, True)
    ArraySetAsSeries(MAONs62, True)
    ArraySetAsSeries(MACDM, True)
    ArraySetAsSeries(MACDS, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ob = 0
    ot = 0
    tb = 0
    tt = 0
    bb = 0
    bt = 0
    cb = 0
    ct = 0
    hb = 0
    ht = 0
    lb = 0
    lt = 0
    pso = 0
    psh = 0
    psl = 0
    psc = 0
    stax = 0
    cprz = 5
    dlvl = 5
    fstp = 4
    pstep = 0
    pvtup = 0
    pvtdn = 0
    himax = 0.0
    lomin = 0.0
    opsclr = 0
    clrmove = 0
    colordir = 0
    fbarup = BarUp
    fbardn = BarDown
    fbarnt = LineGraph
    color_fbar = EmptyBar
    stdir = ""
    opsup = False
    opsdn = False
    opsnt = False
    dfl = 61.8
    barlvl = Arr(0, 0.0)
    przlvl = Arr(0, 0.0)
    ArrayResize(barlvl, dlvl)
    ArrayResize(przlvl, dlvl)
    ArrayResize(pivot, arrpvt)
    ArraySetAsSeries(barlvl, False)
    ArraySetAsSeries(przlvl, False)
    ArraySetAsSeries(pivot, False)
    PvtO = iOpen(Symbol(), prdp, 0)
    PvtH = iHigh(Symbol(), prdp, 0)
    PvtL = iLow(Symbol(), prdp, 0)
    PvtC = iClose(Symbol(), prdp, 0)
    PvtO1 = iOpen(Symbol(), prdp, 1)
    PvtH1 = iHigh(Symbol(), prdp, 1)
    PvtL1 = iLow(Symbol(), prdp, 1)
    PvtC1 = iClose(Symbol(), prdp, 1)
    Pvt = (PvtH1 + PvtL1 + PvtC1) / 3
    sup1 = (Pvt * 2) - PvtH1
    res1 = (Pvt * 2) - PvtL1
    disr = res1 - sup1
    disl = disr * 0.2
    pivot[21] = (Pvt * 7) + PvtH1 - (PvtL1 * 7)
    pivot[20] = (Pvt * 6) + PvtH1 - (PvtL1 * 6)
    pivot[19] = (Pvt * 5) + PvtH1 - (PvtL1 * 5)
    pivot[18] = (Pvt * 4) + PvtH1 - (PvtL1 * 4)
    pivot[17] = (Pvt * 3) + PvtH1 - (PvtL1 * 3)
    pivot[16] = (Pvt * 2) + PvtH1 - (PvtL1 * 2)
    pivot[15] = Pvt + PvtH1 - PvtL1
    pivot[14] = res1 + (disl * 0.618)
    pivot[13] = res1
    pivot[12] = sup1 + (disr * 0.8)
    pivot[11] = sup1 + (disr * 0.6)
    pivot[10] = sup1 + (disr * 0.4)
    pivot[9] = sup1 + (disr * 0.2)
    pivot[8] = sup1
    pivot[7] = sup1 - (disl * 0.618)
    pivot[6] = Pvt - PvtH1 + PvtL1
    pivot[5] = (Pvt * 2) - ((PvtH1 * 2) - PvtL1)
    pivot[4] = (Pvt * 3) - ((PvtH1 * 3) - PvtL1)
    pivot[3] = (Pvt * 4) - ((PvtH1 * 4) - PvtL1)
    pivot[2] = (Pvt * 5) - ((PvtH1 * 5) - PvtL1)
    pivot[1] = (Pvt * 6) - ((PvtH1 * 6) - PvtL1)
    pivot[0] = (Pvt * 7) - ((PvtH1 * 7) - PvtL1)
    csec = Seconds()
    if csec != psec:
        IndicatorsCondition(limit)
    psec = csec
    zzM1 = ZigZagDir(prhh)
    zzH1 = ZigZagDir(prh1)
    ma5mv = MA5Trend(limit)
    mcdm0 = MACDM[0]
    mcdm1 = MACDM[1]
    mcds0 = MACDS[0]
    mcds1 = MACDS[1]
    macd0 = mcdm0 - mcds0
    macd1 = mcdm1 - mcds1
    if (zzH1 == 1 and zzM1 == 1) or (macd0 > macd1 and mcdm0 > mcdm1):
        ArrUp = True
        ArrDn = False
    if (zzH1 == -1 and zzM1 == -1) or (macd0 < macd1 and mcdm0 < mcdm1):
        ArrDn = True
        ArrUp = False
    if (ArrUp == True and zzH1 == 2) or (mcdm0 < mcdm1 and macd0 < macd1):
        ArrDn = True
        ArrUp = False
    if (ArrDn == True and zzH1 == -2) or (mcdm0 > mcdm1 and macd0 > macd1):
        ArrUp = True
        ArrDn = False
    if (mcdm0 >= mcdm1 and mcdm0 > mcds0) and mcds0 > mcds1:
        ArrUp = True
        ArrDn = False
    if (mcdm0 <= mcdm1 and mcdm0 < mcds0) and mcds0 < mcds1:
        ArrDn = True
        ArrUp = False
    if ma5mv == 1:
        ArrUp = True
        ArrDn = False
    if ma5mv == -1:
        ArrDn = True
        ArrUp = False
    fpCls0 = (iHigh(Symbol(), prh1, 0) + iLow(Symbol(), prh1, 0) + iClose(Symbol(), prh1, 0) + iClose(Symbol(), prh1, 0)) / 4
    fpCls1 = (iHigh(Symbol(), prh1, 1) + iLow(Symbol(), prh1, 1) + iClose(Symbol(), prh1, 1) + iClose(Symbol(), prh1, 1)) / 4
    hlcc0 = fpCls0 - SMA5s20[0]
    hlcc1 = fpCls1 - SMA5s20[1]
    if ArrUp == True and hlcc0 > hlcc1:
        opsup = True
        opsdn = False
        opsnt = False
        stax = 24
        stdir = 'BUY'
        opsclr = fbarup
        Price_Up[0] = NormalizeDouble(iLow(Symbol(), Period(), 0), Digits())
        Price_Dn[0] = 0.0
    if ArrDn == True and hlcc0 < hlcc1:
        opsdn = True
        opsup = False
        opsnt = False
        stax = 21
        stdir = 'SELL'
        opsclr = fbardn
        Price_Dn[0] = NormalizeDouble(iHigh(Symbol(), Period(), 0), Digits())
        Price_Up[0] = 0.0
    if (not opsup) and (not opsdn):
        opsnt = True
        opsup = False
        opsdn = False
        opsclr = fbarnt
        Price_Up[0] = 0.0
        Price_Dn[0] = 0.0
    inH = iHighest(Symbol(), prfb, MODE_HIGH, HiLo, 0)
    inL = iLowest(Symbol(), prfb, MODE_LOW, HiLo, 0)
    if inH != -1:
        himax = iHigh(Symbol(), prfb, inH)
    if inL != -1:
        lomin = iLow(Symbol(), prfb, inL)
    if PvtH <= pivot[12] and PvtL >= pivot[7]:
        himax = pivot[12]
        lomin = pivot[7]
    dayHi = PvtH
    dayLo = PvtL
    for g in range(0, dlvl):
        barlvl[g] = _fdiv(prctick, dfl) * fibolvl[g]
        przlvl[g] = lomin + (_fdiv(himax - lomin, dfl) * fibolvl[g])
    PvtO = iOpen(Symbol(), prdp, 0)
    PvtH = iHigh(Symbol(), prdp, 0)
    PvtL = iLow(Symbol(), prdp, 0)
    PvtC = iClose(Symbol(), prdp, 0)
    sumfbar = _int(barlvl[4] - barlvl[0])
    fbajs = _int(prctick - sumfbar)
    przHL = przlvl[4] - przlvl[0]
    pso = _int(NotZeroDiv(PvtO - przlvl[0], przHL) * prctick) + fbajs
    psh = _int(NotZeroDiv(PvtH - przlvl[0], przHL) * prctick) + fbajs
    psl = _int(NotZeroDiv(PvtL - przlvl[0], przHL) * prctick) + fbajs
    psc = _int(NotZeroDiv(PvtC - przlvl[0], przHL) * prctick) + fbajs
    fbbar = psh - psl + 1
    fcbar = fabs(psc - pso) + 1
    fcbhi = psh - psc + 1
    fcblo = fabs(psl - psc) + 1
    for b in range(0, arrpvt - 1):
        if PvtO >= pivot[b] and PvtO < pivot[b + 1]:
            ob = b
            ot = b + 1
        if PvtH >= pivot[b] and PvtH < pivot[b + 1]:
            tb = b
            tt = b + 1
        if PvtL >= pivot[b] and PvtL < pivot[b + 1]:
            bb = b
            bt = b + 1
        if PvtC >= pivot[b] and PvtC < pivot[b + 1]:
            cb = b
            ct = b + 1
        ht = tt
        lb = bb
    if (ht - lb) < 5:
        ht = lb + 5
    pstep = ht - lb
    pvtlvl = _idiv(prctick, pstep)
    barop = (NotZeroDiv(PvtO - pivot[ob], pivot[ot] - pivot[ob]) * pvtlvl) + ((ob - lb) * pvtlvl)
    barhi = (NotZeroDiv(PvtH - pivot[tb], pivot[tt] - pivot[tb]) * pvtlvl) + ((tb - lb) * pvtlvl)
    barlo = (NotZeroDiv(PvtL - pivot[bb], pivot[bt] - pivot[bb]) * pvtlvl) + ((bb - lb) * pvtlvl)
    barcl = (NotZeroDiv(PvtC - pivot[cb], pivot[ct] - pivot[cb]) * pvtlvl) + ((cb - lb) * pvtlvl)
    pvop = _int(barop) + 1
    pvhi = _int(barhi) + 1
    pvlo = _int(barlo)
    pvcl = _int(barcl)
    pvbar = pvhi - pvlo
    pvthi = fabs(pvhi - pvcl)
    pvtlo = fabs(pvcl - pvlo)
    pvtup = fabs(pvcl - pvop)
    pvtdn = fabs(pvop - pvcl)
    if PvtC > PvtO:
        clrmove = fbarup
    if PvtC < PvtO:
        clrmove = fbardn
    if PvtC == PvtO:
        clrmove = fbarnt
    bar45 = CharToString(45)
    barcnd = CharToString(151) + CharToString(151) + CharToString(151)
    for d in range(0, arrpvt - 1):
        ObjectDelete(chart_id, 'PivotLevel_' + _str(d))
        ObjectDelete(chart_id, 'PivotLableLevel_' + _str(d))
    for n in range(0, dlvl):
        ObjectDelete(chart_id, 'FiboBarLevel_' + _str(n))
        ObjectDelete(chart_id, 'FiboBar_' + _str(n))
    for s in range(0, prctick + 1 + 1):
        ObjectDelete(chart_id, 'PivotBar' + _str(s))
        ObjectDelete(chart_id, 'CloseBar' + _str(s))
        ObjectDelete(chart_id, 'PivotBarNt' + _str(s))
        ObjectDelete(chart_id, 'FiboBar' + _str(s))
        ObjectDelete(chart_id, 'FiboBar_cu' + _str(s))
        ObjectDelete(chart_id, 'FiboBar_cd' + _str(s))
        ObjectDelete(chart_id, 'FiboBarUph' + _str(s))
        ObjectDelete(chart_id, 'FiboBarDnl' + _str(s))
        ObjectDelete(chart_id, 'FiboBar_clu' + _str(s))
        ObjectDelete(chart_id, 'FiboBar_cld' + _str(s))
        ObjectDelete(chart_id, 'FiboBar' + _str(s))
        ObjectDelete(chart_id, 'FiboBar_nt' + _str(s))
        ObjectDelete(chart_id, 'FiboBar_cln' + _str(s))
        ObjectDelete(chart_id, 'CloseBarUp' + _str(s))
        ObjectDelete(chart_id, 'CloseBarDn' + _str(s))
        ObjectDelete(chart_id, 'CloseBarNt' + _str(s))
    for r in range(0, pstep + 1):
        plevel = bar45 + DoubleToString(pivot[lb + r], digit)
        CreateSetLable(chart_id, 'PivotLevel_' + _str(r), font_face, font_size, font_color, plevel, corner, distance_x - 109, distance_y + (r * pvtlvl), True)
        llevel = label[lb + r] + bar45
        disc = (0 if (StringLen(llevel) > 3) else 5)
        CreateSetLable(chart_id, 'PivotLableLevel_' + _str(r), font_face, font_size, font_color, llevel, corner, distance_x - 52 - disc, distance_y + (r * pvtlvl), True)
    pv = 0
    while pv < prctick:
        CreateSetLable(chart_id, 'PivotBarNt' + _str(pv), font_face, font_size, color_fbar, bar45, corner, distance_x - 89, distance_y + 1 + pv, True)
        CreateSetLable(chart_id, 'FiboBar' + _str(pv), font_face, font_size, color_fbar, bar45, corner, distance_x + 12, distance_y + 1 + fbajs + pv, True)
        pv += 1
    for i in range(0, pvbar):
        CreateSetLable(chart_id, 'PivotBar' + _str(i), font_face, font_size, clrmove, bar45, corner, distance_x - 89, distance_y + pvlo + i, True)
    for n in range(0, dlvl):
        fibbar = bar45 + DoubleToString(przlvl[n], digit)
        CreateSetLable(chart_id, 'FiboBar_' + _str(n), font_face, font_size, font_color, fibbar, corner, distance_x - 7, distance_y + fbajs + _int(barlvl[n]), True)
        fiblevel = DoubleToString(fibolvl[n], 1) + bar45
        CreateSetLable(chart_id, 'FiboBarLevel_' + _str(n), font_face, font_size, font_color, fiblevel, corner, distance_x + 51, distance_y + fbajs + _int(barlvl[n]), True)
    if PvtC > PvtO:
        for v in range(0, pvtup):
            CreateSetLable(chart_id, 'CloseBar' + _str(v), font_face, font_size, clrmove, barcnd, corner, distance_x - 75, distance_y + pvop + v, True)
        for l in range(0, psh - psl + 1):
            CreateSetLable(chart_id, 'FiboBar_cu' + _str(l), font_face, font_size, clrmove, bar45, corner, distance_x + 12, distance_y + fbajs + psl + l, True)
        for fl in range(0, psc - pso + 1):
            CreateSetLable(chart_id, 'FiboBar_clu' + _str(fl), font_face, font_size, fbarup, barcnd, corner, distance_x + 26, distance_y + fbajs + pso + fl, True)
    if PvtC < PvtO:
        for v in range(0, pvtdn):
            CreateSetLable(chart_id, 'CloseBar' + _str(v), font_face, font_size, clrmove, barcnd, corner, distance_x - 75, distance_y + pvcl + v, True)
        for l in range(0, psh - psl + 1):
            CreateSetLable(chart_id, 'FiboBar_cd' + _str(l), font_face, font_size, clrmove, bar45, corner, distance_x + 12, distance_y + fbajs + psl + l - 1, True)
        for fl in range(0, pso - psc):
            CreateSetLable(chart_id, 'FiboBar_cld' + _str(fl), font_face, font_size, fbardn, barcnd, corner, distance_x + 26, distance_y + fbajs + psc + fl - 1, True)
    if PvtC == PvtO:
        for v in range(0, 2):
            CreateSetLable(chart_id, 'CloseBar' + _str(v), font_face, font_size, clrmove, barcnd, corner, distance_x - 75, distance_y + pvop + v, True)
        for l in range(0, psh - psl + 1):
            CreateSetLable(chart_id, 'FiboBar_nt' + _str(l), font_face, font_size, fbarnt, bar45, corner, distance_x + 12, distance_y + fbajs + psl + l, True)
        for fl in range(0, 2):
            CreateSetLable(chart_id, 'FiboBar_cln' + _str(fl), font_face, font_size, fbarnt, barcnd, corner, distance_x + 26, distance_y + fbajs + pso + fl, True)
    for db in range(0, prctick):
        ObjectDelete(chart_id, 'FiboBarUph' + _str(db))
        ObjectDelete(chart_id, 'FiboBarDnl' + _str(db))
    if ArrUp == True:
        if (PvtL == dayLo and PvtC > dayLo) and PvtC < PvtO:
            cral = -2
            for bd in range(0, fcblo):
                CreateSetLable(chart_id, 'FiboBarDnl' + _str(bd), font_face, font_size, fbarup, bar45, corner, distance_x + 12, distance_y + fbajs + psl + bd - 1, True)
        if opsup == True:
            cral = 1
    if ArrDn == True:
        if (PvtH == dayHi and PvtC < dayHi) and PvtC > PvtO:
            cral = 2
            for bu in range(0, fcbhi):
                CreateSetLable(chart_id, 'FiboBarUph' + _str(bu), font_face, font_size, fbardn, bar45, corner, distance_x + 12, distance_y + fbajs + psc + bu + 1, True)
        if opsdn == True:
            cral = -1
    ObjectDelete(chart_id, 'FiboDir')
    ObjectDelete(chart_id, 'PivotDir')
    ObjectDelete(chart_id, 'PivotStr')
    if ArrUp == True:
        if ArrUp == True and opsup == True:
            colordir = fbarup
        else:
            colordir = fbarnt
        CreateSetLable(chart_id, 'PivotDir', 'Wingdings', 20, colordir, CharToString(217), corner, distance_x - 80, distance_y - 17, True)
        CreateSetLable(chart_id, 'FiboDir', 'Wingdings', 20, colordir, CharToString(217), corner, distance_x + 23, distance_y - 17, True)
        if opsup == True:
            CreateSetLable(chart_id, 'PivotStr', font_ohlc, 12, opsclr, stdir, corner, distance_x - stax, distance_y - 22, True)
        else:
            CreateSetLable(chart_id, 'PivotStr', font_ohlc, 11, fbarnt, 'WAIT', corner, distance_x - 18, distance_y - 22, True)
    elif ArrDn == True:
        if ArrDn == True and opsdn == True:
            colordir = fbardn
        else:
            colordir = fbarnt
        CreateSetLable(chart_id, 'PivotDir', 'Wingdings', 20, colordir, CharToString(218), corner, distance_x - 80, distance_y - 17, True)
        CreateSetLable(chart_id, 'FiboDir', 'Wingdings', 20, colordir, CharToString(218), corner, distance_x + 23, distance_y - 17, True)
        if opsdn == True:
            CreateSetLable(chart_id, 'PivotStr', font_ohlc, 12, opsclr, stdir, corner, distance_x - stax, distance_y - 22, True)
        else:
            CreateSetLable(chart_id, 'PivotStr', font_ohlc, 11, fbarnt, 'WAIT', corner, distance_x - 18, distance_y - 22, True)
    else:
        colordir = fbarnt
        CreateSetLable(chart_id, 'PivotDir', 'Wingdings', 20, colordir, CharToString(108), corner, distance_x - 82, distance_y - 17, True)
        CreateSetLable(chart_id, 'FiboDir', 'Wingdings', 20, colordir, CharToString(108), corner, distance_x + 20, distance_y - 17, True)
        CreateSetLable(chart_id, 'PivotStr', font_ohlc, 11, fbarnt, 'WAIT', corner, distance_x - 18, distance_y - 22, True)
    pos_alerts(cral)
    ChartRedraw(0)
    return rates_total

def IndicatorsCondition(barCount):
    CopyBuffer(h_iMa2, 0, 0, barCount, EMA5e02)
    CopyBuffer(h_iMa20, 0, 0, barCount, SMA5s20)
    CopyBuffer(h_Macd, 0, 0, barCount, MACDM)
    CopyBuffer(h_Macd, 1, 0, barCount, MACDS)
    return

def ZigZagDir(ztf):
    global zh, zl
    i = 0
    lmt = 0
    counterZ = 0
    whatlookfor = 0
    back = 0
    pos = 0
    lasthighpos = 0
    lastlowpos = 0
    zz = 0
    extremum = 0.0
    curlow = 0.0
    curhigh = 0.0
    lasthigh = 0.0
    lastlow = 0.0
    ArrayResize(ExtZz, bars)
    ArrayResize(ExtHi, bars)
    ArrayResize(ExtLo, bars)
    ArraySetAsSeries(ExtZz, True)
    ArraySetAsSeries(ExtHi, True)
    ArraySetAsSeries(ExtLo, True)
    lmt = Initialize()
    zl = 0
    zh = zl
    counterZ = zh
    i = counterZ
    while counterZ < level and i < bars:
        if ExtZz[i] != 0.0:
            counterZ += 1
        i += 1
    if counterZ == 0:
        lmt = Initialize()
    else:
        lmt = i - 1
        if ExtLo[i] != 0.0:
            curlow = ExtLo[i]
            whatlookfor = 1
        else:
            curhigh = ExtHi[i]
            whatlookfor = -1
        i = lmt - 1
        for i in range(i, 0 - 1, -1):
            ExtZz[i] = 0.0
            ExtLo[i] = 0.0
            ExtHi[i] = 0.0
        else:
            i = _range_end(i, 0 - 1, -1)
    i = lmt
    for i in range(i, 0 - 1, -1):
        extremum = iLow(Symbol(), ztf, iLowest(Symbol(), ztf, MODE_LOW, depth, i))
        if extremum == lastlow:
            extremum = 0.0
        else:
            lastlow = extremum
            if (iLow(Symbol(), ztf, i) - extremum) > (devia * Point()):
                extremum = 0.0
            else:
                back = 1
                for back in range(back, backs + 1):
                    pos = i + back
                    if ExtLo[pos] != 0 and ExtLo[pos] > extremum:
                        ExtLo[pos] = 0.0
                else:
                    back = _range_end(back, backs + 1, 1)
        if iLow(Symbol(), ztf, i) == extremum:
            ExtLo[i] = extremum
            zl = i
        else:
            ExtLo[i] = 0.0
        extremum = iHigh(Symbol(), ztf, iHighest(Symbol(), ztf, MODE_HIGH, depth, i))
        if extremum == lasthigh:
            extremum = 0.0
        else:
            lasthigh = extremum
            if (extremum - iHigh(Symbol(), ztf, i)) > (devia * Point()):
                extremum = 0.0
            else:
                back = 1
                for back in range(back, backs + 1):
                    pos = i + back
                    if ExtHi[pos] != 0 and ExtHi[pos] < extremum:
                        ExtHi[pos] = 0.0
                else:
                    back = _range_end(back, backs + 1, 1)
        if iHigh(Symbol(), ztf, i) == extremum:
            ExtHi[i] = extremum
            zh = i
        else:
            ExtHi[i] = 0.0
    else:
        i = _range_end(i, 0 - 1, -1)
    if whatlookfor == 0:
        lastlow = 0.0
        lasthigh = 0.0
    else:
        lastlow = curlow
        lasthigh = curhigh
    i = lmt
    for i in range(i, 0 - 1, -1):
        _sw1 = whatlookfor
        if _sw1 == 0:
            if lastlow == 0.0 and lasthigh == 0.0:
                if ExtHi[i] != 0.0:
                    lasthigh = iHigh(Symbol(), ztf, i)
                    lasthighpos = i
                    whatlookfor = -1
                    ExtZz[i] = lasthigh
                    zh = lasthighpos
                if ExtLo[i] != 0.0:
                    lastlow = iLow(Symbol(), ztf, i)
                    lastlowpos = i
                    whatlookfor = 1
                    ExtZz[i] = lastlow
                    zl = lastlowpos
        elif _sw1 == 1:
            if (ExtLo[i] != 0.0 and ExtLo[i] < lastlow) and ExtHi[i] == 0.0:
                ExtZz[lastlowpos] = 0.0
                lastlowpos = i
                lastlow = ExtLo[i]
                ExtZz[i] = lastlow
                zl = lastlowpos
            if ExtHi[i] != 0.0 and ExtLo[i] == 0.0:
                lasthigh = ExtHi[i]
                lasthighpos = i
                ExtZz[i] = lasthigh
                whatlookfor = -1
                zh = lasthighpos
        elif _sw1 == -1:
            if (ExtHi[i] != 0.0 and ExtHi[i] > lasthigh) and ExtLo[i] == 0.0:
                ExtZz[lasthighpos] = 0.0
                lasthighpos = i
                lasthigh = ExtHi[i]
                ExtZz[i] = lasthigh
                zh = lasthighpos
            if ExtLo[i] != 0.0 and ExtHi[i] == 0.0:
                lastlow = ExtLo[i]
                lastlowpos = i
                ExtZz[i] = lastlow
                whatlookfor = 1
                zl = lastlowpos
    else:
        i = _range_end(i, 0 - 1, -1)
    if ztf == PERIOD_H1:
        if (zl < zh and zl > 0) and zl < 4:
            zz = 1
        if (zh < zl and zh > 0) and zh < 4:
            zz = -1
        if zl < zh and zl > 4:
            zz = 2
        if zh < zl and zh > 4:
            zz = -2
    if ztf == PERIOD_M30:
        if zl < zh:
            zz = 1
        if zh < zl:
            zz = -1
    return zz

def Initialize():
    ArrayInitialize(ExtZz, 0.0)
    ArrayInitialize(ExtHi, 0.0)
    ArrayInitialize(ExtLo, 0.0)
    return bars - depth

def MA5Trend(bar):
    m5t = 0
    ArrayResize(EMA5e02, bar)
    ArrayResize(SMA5s20, bar)
    ArrayResize(MAONs10, bar)
    ArrayResize(MAONs62, bar)
    ArraySetAsSeries(EMA5e02, True)
    ArraySetAsSeries(SMA5s20, True)
    ArraySetAsSeries(MAONs10, True)
    ArraySetAsSeries(MAONs62, True)
    SimpleMAOnBuffer(bar, 0, 0, 10, SMA5s20, MAONs10)
    SimpleMAOnBuffer(bar, 0, 0, 62, SMA5s20, MAONs62)
    ma10620 = MAONs10[0] - MAONs62[0]
    ma10621 = MAONs10[1] - MAONs62[1]
    ma20100 = SMA5s20[0] - MAONs10[0]
    ma20101 = SMA5s20[1] - MAONs10[1]
    ma5xupn = ((EMA5e02[0] > EMA5e02[1] and SMA5s20[0] > SMA5s20[1]) and ma10620 >= ma10621) and (MAONs10[2] < MAONs62[2] and MAONs10[0] > MAONs62[0])
    ma5xupc = (((EMA5e02[0] > EMA5e02[1] and SMA5s20[0] > SMA5s20[1]) and ma10620 >= ma10621) and MAONs10[0] > MAONs62[0]) and MAONs10[0] > MAONs10[1]
    ma5xupb = (((EMA5e02[0] > EMA5e02[1] and SMA5s20[0] > SMA5s20[1]) and ma20100 > ma20101) and MAONs62[0] > MAONs62[1]) and SMA5s20[0] > MAONs10[0]
    ma5xdnn = ((EMA5e02[0] < EMA5e02[1] and SMA5s20[0] < SMA5s20[1]) and ma10620 <= ma10621) and (MAONs10[2] > MAONs62[2] and MAONs10[0] < MAONs62[0])
    ma5xdnc = (((EMA5e02[0] < EMA5e02[1] and SMA5s20[0] < SMA5s20[1]) and ma10620 <= ma10621) and MAONs10[0] < MAONs62[0]) and MAONs10[0] < MAONs10[1]
    ma5xdna = (((EMA5e02[0] < EMA5e02[1] and SMA5s20[0] < SMA5s20[1]) and ma20100 < ma20101) and MAONs62[0] < MAONs62[1]) and SMA5s20[0] < MAONs10[0]
    if (ma5xupn or ma5xupc) or ma5xupb:
        m5t = 1
    if (ma5xdnn or ma5xdnc) or ma5xdna:
        m5t = -1
    return m5t

def CreateSetLable(chartid, _name, _font_model, _font_size, _color, _obj_text, _corner, _xdist, _ydist, _hidden):
    if ObjectCreate(chart_id, _name, OBJ_LABEL, 0, 0, 0, 0, 0):
        ObjectSetString(chartid, _name, OBJPROP_TEXT, _obj_text)
        ObjectSetString(chartid, _name, OBJPROP_FONT, _font_model)
        ObjectSetInteger(chartid, _name, OBJPROP_FONTSIZE, _font_size)
        ObjectSetInteger(chartid, _name, OBJPROP_COLOR, _color)
        ObjectSetInteger(chartid, _name, OBJPROP_CORNER, _corner)
        ObjectSetInteger(chartid, _name, OBJPROP_XDISTANCE, _xdist)
        ObjectSetInteger(chartid, _name, OBJPROP_YDISTANCE, _ydist)
        ObjectSetInteger(chartid, _name, OBJPROP_HIDDEN, _hidden)
    else:
        return False
    return True

def FontsModel(mode):
    str_font = ""
    _sw2 = mode
    if _sw2 == 0:
        str_font = 'Arial Black'
    elif _sw2 == 1:
        str_font = 'Bodoni MT Black'
    return str_font

def Hours():
    return MqlReturnDateTime(TimeCurrent(), hour)

def Minutes():
    return MqlReturnDateTime(TimeCurrent(), min_)

def Seconds():
    return MqlReturnDateTime(TimeCurrent(), sec)

def MqlReturnDateTime(reqtime, mode):
    mqltm = MqlDateTime()
    TimeToStruct(reqtime, mqltm)
    valdate = 0
    _sw3 = mode
    if _sw3 == 0:
        valdate = mqltm.year
    elif _sw3 == 1:
        valdate = mqltm.mon
    elif _sw3 == 2:
        valdate = mqltm.day
    elif _sw3 == 3:
        valdate = mqltm.hour
    elif _sw3 == 4:
        valdate = mqltm.min
    elif _sw3 == 5:
        valdate = mqltm.sec
    elif _sw3 == 6:
        valdate = mqltm.day_of_week
    elif _sw3 == 7:
        valdate = mqltm.day_of_year
    return valdate

def TF(tf):
    _sw4 = tf
    if _sw4 == 0:
        return PERIOD_CURRENT
    elif _sw4 == 1:
        return PERIOD_M1
    elif _sw4 == 5:
        return PERIOD_M5
    elif _sw4 == 15:
        return PERIOD_M15
    elif _sw4 == 30:
        return PERIOD_M30
    elif _sw4 == 60:
        return PERIOD_H1
    elif _sw4 == 240:
        return PERIOD_H4
    elif _sw4 == 1440:
        return PERIOD_D1
    elif _sw4 == 10080:
        return PERIOD_W1
    elif _sw4 == 43200:
        return PERIOD_MN1
    else:
        return PERIOD_CURRENT

def doAlerts(msgText, eMailSub):
    Print(msgText)
    if MsgAlerts:
        Alert(msgText)
    if eMailAlerts == Yes:
        SendMail(eMailSub, msgText)
    if UseSendnotify == Yes:
        SendNotification(msgText)
    return

def strTF(tf):
    _sw5 = tf
    if _sw5 == PERIOD_M1:
        return 'M1'
    elif _sw5 == PERIOD_M5:
        return 'M5'
    elif _sw5 == PERIOD_M15:
        return 'M15'
    elif _sw5 == PERIOD_M30:
        return 'M30'
    elif _sw5 == PERIOD_H1:
        return 'H1'
    elif _sw5 == PERIOD_H4:
        return 'H4'
    elif _sw5 == PERIOD_D1:
        return 'D1'
    elif _sw5 == PERIOD_W1:
        return 'W1'
    elif _sw5 == PERIOD_MN1:
        return 'MN'
    return EnumToString(tf, 'ENUM_TIMEFRAMES')

def pos_alerts(alert):
    global alBase, alMsg, alSubj, crmnt, pral, prmnt
    crmnt = Minutes()
    if crmnt != prmnt:
        if cral != pral and alert == 2:
            alBase = short_name + ': ' + Symbol() + ', TF: ' + strTF(Period()) + ' @ ' + TimeToString(TimeLocal())
            alSubj = alBase + '. The Price Began to Down,'
            alMsg = alSubj + ' Action: Wait and See.!!'
            prmnt = crmnt
            pral = cral
            doAlerts(alMsg, alSubj)
        if cral != pral and alert == 1:
            alBase = short_name + ': ' + Symbol() + ', TF: ' + strTF(Period()) + ' @ ' + TimeToString(TimeLocal())
            alSubj = alBase + '. The Price Goes Up,'
            alMsg = alSubj + ' Action: Open BUY.!!'
            prmnt = crmnt
            pral = cral
            doAlerts(alMsg, alSubj)
        if cral != pral and alert == -2:
            alBase = short_name + ': ' + Symbol() + ', TF: ' + strTF(Period()) + ' @ ' + TimeToString(TimeLocal())
            alSubj = alBase + '. The Price Began to Up,'
            alMsg = alSubj + ' Action: Wait and See.!!'
            prmnt = crmnt
            pral = cral
            doAlerts(alMsg, alSubj)
        if cral != pral and alert == -1:
            alBase = short_name + ': ' + Symbol() + ', TF: ' + strTF(Period()) + ' @ ' + TimeToString(TimeLocal())
            alSubj = alBase + '. The Price Goes Down,'
            alMsg = alSubj + ' Action: Open SELL.!!'
            prmnt = crmnt
            pral = cral
            doAlerts(alMsg, alSubj)
    return

def NotZeroDiv(val1, val2):
    resval = 0.0
    if val1 == 0 or val2 == 0:
        resval = 0.0
    else:
        resval = _fdiv(val1, val2)
    return resval


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FiboPivotCandleBarMT5(_MQL5Indicator):
    name = 'FiboPivotCandleBarMT5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MsgAlerts': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Activate Alert (Yes) or (No)
        'eMailAlerts': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Send Email Alert (Yes) or (No)
        'UseSendnotify': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Send Notification (Yes) or (No)
        'Fonts_Model': _Choice({0: 'Arial_Black', 1: 'Bodoni_MT_Black'}, default=1),  # Choose Fonts Model
    }

