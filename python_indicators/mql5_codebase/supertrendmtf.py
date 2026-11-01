"""supertrendmtf — converted from MQL5: MQL5 Indicators/Multi-timeframe SuperTrend in the form of Pivot/supertrendmtf.mq5

Copyright: sanderz; Link: https://login.mql5.com/ru/users/sanderz/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'sanderz', 'link': 'https://login.mql5.com/ru/users/sanderz/seller', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'supertrendmtf', 'source': 'MQL5 Indicators/Multi-timeframe SuperTrend in the form of Pivot/supertrendmtf.mq5', 'folder': 'Multi-timeframe SuperTrend in the form of Pivot', 'inputs': [{'mql': 'sect1', 'py': 'sect1', 'param': None, 'type': 'string', 'default': '', 'label': 'SUPERTREND PARAMETERS', 'sinput': False}, {'mql': 'PeriodST', 'py': 'PeriodST', 'param': 'PeriodST', 'type': 'int', 'default': 10, 'label': 'Supertrend period', 'sinput': False}, {'mql': 'Multiplier', 'py': 'Multiplier', 'param': 'Multiplier', 'type': 'double', 'default': 3.0, 'label': 'Supertrend multiplier', 'sinput': False}, {'mql': 'sect2', 'py': 'sect2', 'param': None, 'type': 'string', 'default': '', 'label': 'TIMEFRAME PARAMETERS', 'sinput': False}, {'mql': 'swTF1', 'py': 'swTF1', 'param': 'swTF1', 'type': 'bool', 'default': False, 'label': 'Use TF 1 min', 'sinput': False}, {'mql': 'swTF2', 'py': 'swTF2', 'param': 'swTF2', 'type': 'bool', 'default': False, 'label': 'Use TF 2 min', 'sinput': False}, {'mql': 'swTF3', 'py': 'swTF3', 'param': 'swTF3', 'type': 'bool', 'default': False, 'label': 'Use TF 3 min', 'sinput': False}, {'mql': 'swTF4', 'py': 'swTF4', 'param': 'swTF4', 'type': 'bool', 'default': False, 'label': 'Use TF 4 min', 'sinput': False}, {'mql': 'swTF5', 'py': 'swTF5', 'param': 'swTF5', 'type': 'bool', 'default': False, 'label': 'Use TF 5 min', 'sinput': False}, {'mql': 'swTF6', 'py': 'swTF6', 'param': 'swTF6', 'type': 'bool', 'default': False, 'label': 'Use TF 6 min', 'sinput': False}, {'mql': 'swTF10', 'py': 'swTF10', 'param': 'swTF10', 'type': 'bool', 'default': False, 'label': 'Use TF 10 min', 'sinput': False}, {'mql': 'swTF12', 'py': 'swTF12', 'param': 'swTF12', 'type': 'bool', 'default': False, 'label': 'Use TF 12 min', 'sinput': False}, {'mql': 'swTF15', 'py': 'swTF15', 'param': 'swTF15', 'type': 'bool', 'default': True, 'label': 'Use TF 15 min', 'sinput': False}, {'mql': 'swTF20', 'py': 'swTF20', 'param': 'swTF20', 'type': 'bool', 'default': True, 'label': 'Use TF 20 min', 'sinput': False}, {'mql': 'swTF30', 'py': 'swTF30', 'param': 'swTF30', 'type': 'bool', 'default': True, 'label': 'Use TF 30 min', 'sinput': False}, {'mql': 'swTFH1', 'py': 'swTFH1', 'param': 'swTFH1', 'type': 'bool', 'default': True, 'label': 'Use TF 1 h', 'sinput': False}, {'mql': 'swTFH2', 'py': 'swTFH2', 'param': 'swTFH2', 'type': 'bool', 'default': False, 'label': 'Use TF 2 h', 'sinput': False}, {'mql': 'swTFH3', 'py': 'swTFH3', 'param': 'swTFH3', 'type': 'bool', 'default': False, 'label': 'Use TF 3 h', 'sinput': False}, {'mql': 'swTFH4', 'py': 'swTFH4', 'param': 'swTFH4', 'type': 'bool', 'default': False, 'label': 'Use TF 4 h', 'sinput': False}, {'mql': 'swTFH6', 'py': 'swTFH6', 'param': 'swTFH6', 'type': 'bool', 'default': False, 'label': 'Use TF 6 h', 'sinput': False}, {'mql': 'swTFH8', 'py': 'swTFH8', 'param': 'swTFH8', 'type': 'bool', 'default': False, 'label': 'Use TF 8 h', 'sinput': False}, {'mql': 'swTFH12', 'py': 'swTFH12', 'param': 'swTFH12', 'type': 'bool', 'default': False, 'label': 'Use TF 12 h', 'sinput': False}, {'mql': 'swTFD', 'py': 'swTFD', 'param': 'swTFD', 'type': 'bool', 'default': False, 'label': 'Use TF D', 'sinput': False}, {'mql': 'swTFW', 'py': 'swTFW', 'param': 'swTFW', 'type': 'bool', 'default': False, 'label': 'Use TF W', 'sinput': False}, {'mql': 'swTFM', 'py': 'swTFM', 'param': 'swTFM', 'type': 'bool', 'default': False, 'label': 'Use TF M', 'sinput': False}, {'mql': 'sect3', 'py': 'sect3', 'param': None, 'type': 'string', 'default': '', 'label': 'DESIGN PARAMETERS', 'sinput': False}, {'mql': 'sizeFont', 'py': 'sizeFont', 'param': 'sizeFont', 'type': 'int', 'default': 8, 'label': 'Text size', 'sinput': False}, {'mql': 'sizeP', 'py': 'sizeP', 'param': 'sizeP', 'type': 'int', 'default': 1, 'label': 'Price mark size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
sect1 = _input('sect1', '')  # SUPERTREND PARAMETERS
PeriodST = _input('PeriodST', 10)  # Supertrend period
Multiplier = _input('Multiplier', 3.0)  # Supertrend multiplier
sect2 = _input('sect2', '')  # TIMEFRAME PARAMETERS
swTF1 = _input('swTF1', False)  # Use TF 1 min
swTF2 = _input('swTF2', False)  # Use TF 2 min
swTF3 = _input('swTF3', False)  # Use TF 3 min
swTF4 = _input('swTF4', False)  # Use TF 4 min
swTF5 = _input('swTF5', False)  # Use TF 5 min
swTF6 = _input('swTF6', False)  # Use TF 6 min
swTF10 = _input('swTF10', False)  # Use TF 10 min
swTF12 = _input('swTF12', False)  # Use TF 12 min
swTF15 = _input('swTF15', True)  # Use TF 15 min
swTF20 = _input('swTF20', True)  # Use TF 20 min
swTF30 = _input('swTF30', True)  # Use TF 30 min
swTFH1 = _input('swTFH1', True)  # Use TF 1 h
swTFH2 = _input('swTFH2', False)  # Use TF 2 h
swTFH3 = _input('swTFH3', False)  # Use TF 3 h
swTFH4 = _input('swTFH4', False)  # Use TF 4 h
swTFH6 = _input('swTFH6', False)  # Use TF 6 h
swTFH8 = _input('swTFH8', False)  # Use TF 8 h
swTFH12 = _input('swTFH12', False)  # Use TF 12 h
swTFD = _input('swTFD', False)  # Use TF D
swTFW = _input('swTFW', False)  # Use TF W
swTFM = _input('swTFM', False)  # Use TF M
sect3 = _input('sect3', '')  # DESIGN PARAMETERS
sizeFont = _input('sizeFont', 8)  # Text size
sizeP = _input('sizeP', 1)  # Price mark size
handleSTr1 = INVALID_HANDLE
handleSTr2 = INVALID_HANDLE
handleSTr3 = INVALID_HANDLE
handleSTr4 = INVALID_HANDLE
handleSTr5 = INVALID_HANDLE
handleSTr6 = INVALID_HANDLE
handleSTr10 = INVALID_HANDLE
handleSTr12 = INVALID_HANDLE
handleSTr15 = INVALID_HANDLE
handleSTr20 = INVALID_HANDLE
handleSTr30 = INVALID_HANDLE
handleSTrH1 = INVALID_HANDLE
handleSTrH2 = INVALID_HANDLE
handleSTrH3 = INVALID_HANDLE
handleSTrH4 = INVALID_HANDLE
handleSTrH6 = INVALID_HANDLE
handleSTrH8 = INVALID_HANDLE
handleSTrH12 = INVALID_HANDLE
handleSTrD = INVALID_HANDLE
handleSTrW = INVALID_HANDLE
handleSTrM = INVALID_HANDLE
SuperTr1 = Arr(0, 0.0)
SuperTr2 = Arr(0, 0.0)
SuperTr3 = Arr(0, 0.0)
SuperTr4 = Arr(0, 0.0)
SuperTr5 = Arr(0, 0.0)
SuperTr6 = Arr(0, 0.0)
SuperTr10 = Arr(0, 0.0)
SuperTr12 = Arr(0, 0.0)
SuperTr15 = Arr(0, 0.0)
SuperTr20 = Arr(0, 0.0)
SuperTr30 = Arr(0, 0.0)
SuperTrH1 = Arr(0, 0.0)
SuperTrH2 = Arr(0, 0.0)
SuperTrH3 = Arr(0, 0.0)
SuperTrH4 = Arr(0, 0.0)
SuperTrH6 = Arr(0, 0.0)
SuperTrH8 = Arr(0, 0.0)
SuperTrH12 = Arr(0, 0.0)
SuperTrD = Arr(0, 0.0)
SuperTrW = Arr(0, 0.0)
SuperTrM = Arr(0, 0.0)

def OnInit():
    global handleSTr1, handleSTr10, handleSTr12, handleSTr15, handleSTr2, handleSTr20, handleSTr3, handleSTr30, handleSTr4, handleSTr5, handleSTr6, handleSTrD, handleSTrH1, handleSTrH12, handleSTrH2, handleSTrH3, handleSTrH4, handleSTrH6, handleSTrH8, handleSTrM, handleSTrW
    handleSTr1 = iCustom(Symbol(), PERIOD_M1, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr1 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr2 = iCustom(Symbol(), PERIOD_M2, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr2 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr3 = iCustom(Symbol(), PERIOD_M3, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr3 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr4 = iCustom(Symbol(), PERIOD_M4, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr4 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr5 = iCustom(Symbol(), PERIOD_M5, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr5 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr6 = iCustom(Symbol(), PERIOD_M6, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr6 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr10 = iCustom(Symbol(), PERIOD_M10, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr10 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr12 = iCustom(Symbol(), PERIOD_M12, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr12 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr15 = iCustom(Symbol(), PERIOD_M15, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr15 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr20 = iCustom(Symbol(), PERIOD_M20, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr20 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTr30 = iCustom(Symbol(), PERIOD_M30, 'SuperTrend', PeriodST, Multiplier)
    if handleSTr30 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrH1 = iCustom(Symbol(), PERIOD_H1, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrH1 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrH2 = iCustom(Symbol(), PERIOD_H2, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrH2 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrH3 = iCustom(Symbol(), PERIOD_H3, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrH3 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrH4 = iCustom(Symbol(), PERIOD_H4, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrH4 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrH6 = iCustom(Symbol(), PERIOD_H6, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrH6 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrH8 = iCustom(Symbol(), PERIOD_H8, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrH8 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrH12 = iCustom(Symbol(), PERIOD_H12, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrH12 == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrD = iCustom(Symbol(), PERIOD_D1, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrD == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrW = iCustom(Symbol(), PERIOD_W1, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrW == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    handleSTrM = iCustom(Symbol(), PERIOD_MN1, 'SuperTrend', PeriodST, Multiplier)
    if handleSTrM == INVALID_HANDLE:
        PrintFormat('Failed to create the handle of the Supertrend indicator. Error=', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(tick_volume, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(spread, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(volume, True)
    if swTF1:
        ArrayResize(SuperTr1, 2)
        ArrayInitialize(SuperTr1, 0.0)
        if CopyBufferAsSeries(handleSTr1, 2, 0, 2, True, SuperTr1):
            clr = clrBlack
            if close[0] < SuperTr1[0]:
                clr = clrRed
            if close[0] > SuperTr1[0]:
                clr = clrGreen
            if close[0] == SuperTr1[0] and close[1] > SuperTr1[1]:
                clr = clrGreen
            if close[0] == SuperTr1[0] and close[1] < SuperTr1[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB1')
            TextDelete(0, '2LPB1')
            TextCreate(0, '2LPB1', 0, time[0] + PeriodSeconds(Period()), SuperTr1[0], 'M1', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB1', 0, time[0] + PeriodSeconds(Period()), SuperTr1[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF2:
        ArrayResize(SuperTr2, 2)
        ArrayInitialize(SuperTr2, 0.0)
        if CopyBufferAsSeries(handleSTr2, 2, 0, 2, True, SuperTr2):
            clr = clrBlack
            if close[0] < SuperTr2[0]:
                clr = clrRed
            if close[0] > SuperTr2[0]:
                clr = clrGreen
            if close[0] == SuperTr2[0] and close[1] > SuperTr2[1]:
                clr = clrGreen
            if close[0] == SuperTr2[0] and close[1] < SuperTr2[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB2')
            TextDelete(0, '2LPB2')
            TextCreate(0, '2LPB2', 0, time[0] + PeriodSeconds(Period()), SuperTr2[0], 'M2', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB2', 0, time[0] + PeriodSeconds(Period()), SuperTr2[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF3:
        ArrayResize(SuperTr3, 2)
        ArrayInitialize(SuperTr3, 0.0)
        if CopyBufferAsSeries(handleSTr3, 2, 0, 2, True, SuperTr3):
            clr = clrBlack
            if close[0] < SuperTr3[0]:
                clr = clrRed
            if close[0] > SuperTr3[0]:
                clr = clrGreen
            if close[0] == SuperTr3[0] and close[1] > SuperTr3[1]:
                clr = clrGreen
            if close[0] == SuperTr3[0] and close[1] < SuperTr3[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB3')
            TextDelete(0, '2LPB3')
            TextCreate(0, '2LPB3', 0, time[0] + PeriodSeconds(Period()), SuperTr3[0], 'M3', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB3', 0, time[0] + PeriodSeconds(Period()), SuperTr3[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF4:
        ArrayResize(SuperTr4, 2)
        ArrayInitialize(SuperTr4, 0.0)
        if CopyBufferAsSeries(handleSTr4, 2, 0, 2, True, SuperTr4):
            clr = clrBlack
            if close[0] < SuperTr4[0]:
                clr = clrRed
            if close[0] > SuperTr4[0]:
                clr = clrGreen
            if close[0] == SuperTr4[0] and close[1] > SuperTr4[1]:
                clr = clrGreen
            if close[0] == SuperTr4[0] and close[1] < SuperTr4[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB4')
            TextDelete(0, '2LPB4')
            TextCreate(0, '2LPB4', 0, time[0] + PeriodSeconds(Period()), SuperTr4[0], 'M4', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB4', 0, time[0] + PeriodSeconds(Period()), SuperTr4[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF5:
        ArrayResize(SuperTr5, 2)
        ArrayInitialize(SuperTr5, 0.0)
        if CopyBufferAsSeries(handleSTr5, 2, 0, 2, True, SuperTr5):
            clr = clrBlack
            if close[0] < SuperTr5[0]:
                clr = clrRed
            if close[0] > SuperTr5[0]:
                clr = clrGreen
            if close[0] == SuperTr5[0] and close[1] > SuperTr5[1]:
                clr = clrGreen
            if close[0] == SuperTr5[0] and close[1] < SuperTr5[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB5')
            TextDelete(0, '2LPB5')
            TextCreate(0, '2LPB5', 0, time[0] + PeriodSeconds(Period()), SuperTr5[0], 'M5', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB5', 0, time[0] + PeriodSeconds(Period()), SuperTr5[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF6:
        ArrayResize(SuperTr6, 2)
        ArrayInitialize(SuperTr6, 0.0)
        if CopyBufferAsSeries(handleSTr6, 2, 0, 2, True, SuperTr6):
            clr = clrBlack
            if close[0] < SuperTr6[0]:
                clr = clrRed
            if close[0] > SuperTr6[0]:
                clr = clrGreen
            if close[0] == SuperTr6[0] and close[1] > SuperTr6[1]:
                clr = clrGreen
            if close[0] == SuperTr6[0] and close[1] < SuperTr6[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB6')
            TextDelete(0, '2LPB6')
            TextCreate(0, '2LPB6', 0, time[0] + PeriodSeconds(Period()), SuperTr6[0], 'M6', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB6', 0, time[0] + PeriodSeconds(Period()), SuperTr6[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF10:
        ArrayResize(SuperTr10, 2)
        ArrayInitialize(SuperTr10, 0.0)
        if CopyBufferAsSeries(handleSTr10, 2, 0, 2, True, SuperTr10):
            clr = clrBlack
            if close[0] < SuperTr10[0]:
                clr = clrRed
            if close[0] > SuperTr10[0]:
                clr = clrGreen
            if close[0] == SuperTr10[0] and close[1] > SuperTr10[1]:
                clr = clrGreen
            if close[0] == SuperTr10[0] and close[1] < SuperTr10[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB10')
            TextDelete(0, '2LPB10')
            TextCreate(0, '2LPB10', 0, time[0] + PeriodSeconds(Period()), SuperTr10[0], 'M10', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB10', 0, time[0] + PeriodSeconds(Period()), SuperTr10[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF12:
        ArrayResize(SuperTr12, 2)
        ArrayInitialize(SuperTr12, 0.0)
        if CopyBufferAsSeries(handleSTr12, 2, 0, 2, True, SuperTr12):
            clr = clrBlack
            if close[0] < SuperTr12[0]:
                clr = clrRed
            if close[0] > SuperTr12[0]:
                clr = clrGreen
            if close[0] == SuperTr12[0] and close[1] > SuperTr12[1]:
                clr = clrGreen
            if close[0] == SuperTr12[0] and close[1] < SuperTr12[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB12')
            TextDelete(0, '2LPB12')
            TextCreate(0, '2LPB12', 0, time[0] + PeriodSeconds(Period()), SuperTr12[0], 'M12', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB12', 0, time[0] + PeriodSeconds(Period()), SuperTr12[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF15:
        ArrayResize(SuperTr15, 2)
        ArrayInitialize(SuperTr15, 0.0)
        if CopyBufferAsSeries(handleSTr15, 2, 0, 2, True, SuperTr15):
            clr = clrBlack
            if close[0] < SuperTr15[0]:
                clr = clrRed
            if close[0] > SuperTr15[0]:
                clr = clrGreen
            if close[0] == SuperTr15[0] and close[1] > SuperTr15[1]:
                clr = clrGreen
            if close[0] == SuperTr15[0] and close[1] < SuperTr15[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB15')
            TextDelete(0, '2LPB15')
            TextCreate(0, '2LPB15', 0, time[0] + PeriodSeconds(Period()), SuperTr15[0], 'M15', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB15', 0, time[0] + PeriodSeconds(Period()), SuperTr15[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF20:
        ArrayResize(SuperTr20, 2)
        ArrayInitialize(SuperTr20, 0.0)
        if CopyBufferAsSeries(handleSTr20, 2, 0, 2, True, SuperTr20):
            clr = clrBlack
            if close[0] < SuperTr20[0]:
                clr = clrRed
            if close[0] > SuperTr20[0]:
                clr = clrGreen
            if close[0] == SuperTr20[0] and close[1] > SuperTr20[1]:
                clr = clrGreen
            if close[0] == SuperTr20[0] and close[1] < SuperTr20[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB20')
            TextDelete(0, '2LPB20')
            TextCreate(0, '2LPB20', 0, time[0] + PeriodSeconds(Period()), SuperTr20[0], 'M20', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB20', 0, time[0] + PeriodSeconds(Period()), SuperTr20[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTF30:
        ArrayResize(SuperTr30, 2)
        ArrayInitialize(SuperTr30, 0.0)
        if CopyBufferAsSeries(handleSTr30, 2, 0, 2, True, SuperTr30):
            clr = clrBlack
            if close[0] < SuperTr30[0]:
                clr = clrRed
            if close[0] > SuperTr30[0]:
                clr = clrGreen
            if close[0] == SuperTr30[0] and close[1] > SuperTr30[1]:
                clr = clrGreen
            if close[0] == SuperTr30[0] and close[1] < SuperTr30[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPB30')
            TextDelete(0, '2LPB30')
            TextCreate(0, '2LPB30', 0, time[0] + PeriodSeconds(Period()), SuperTr30[0], 'M30', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPB30', 0, time[0] + PeriodSeconds(Period()), SuperTr30[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFH1:
        ArrayResize(SuperTrH1, 2)
        ArrayInitialize(SuperTrH1, 0.0)
        if CopyBufferAsSeries(handleSTrH1, 2, 0, 2, True, SuperTrH1):
            clr = clrBlack
            if close[0] < SuperTrH1[0]:
                clr = clrRed
            if close[0] > SuperTrH1[0]:
                clr = clrGreen
            if close[0] == SuperTrH1[0] and close[1] > SuperTrH1[1]:
                clr = clrGreen
            if close[0] == SuperTrH1[0] and close[1] < SuperTrH1[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBH1')
            TextDelete(0, '2LPBH1')
            TextCreate(0, '2LPBH1', 0, time[0] + PeriodSeconds(Period()), SuperTrH1[0], 'H1', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBH1', 0, time[0] + PeriodSeconds(Period()), SuperTrH1[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFH2:
        ArrayResize(SuperTrH2, 2)
        ArrayInitialize(SuperTrH2, 0.0)
        if CopyBufferAsSeries(handleSTrH2, 2, 0, 2, True, SuperTrH2):
            clr = clrBlack
            if close[0] < SuperTrH2[0]:
                clr = clrRed
            if close[0] > SuperTrH2[0]:
                clr = clrGreen
            if close[0] == SuperTrH2[0] and close[1] > SuperTrH2[1]:
                clr = clrGreen
            if close[0] == SuperTrH2[0] and close[1] < SuperTrH2[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBH2')
            TextDelete(0, '2LPBH2')
            TextCreate(0, '2LPBH2', 0, time[0] + PeriodSeconds(Period()), SuperTrH2[0], 'H2', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBH2', 0, time[0] + PeriodSeconds(Period()), SuperTrH2[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFH3:
        ArrayResize(SuperTrH3, 2)
        ArrayInitialize(SuperTrH3, 0.0)
        if CopyBufferAsSeries(handleSTrH3, 2, 0, 2, True, SuperTrH3):
            clr = clrBlack
            if close[0] < SuperTrH3[0]:
                clr = clrRed
            if close[0] > SuperTrH3[0]:
                clr = clrGreen
            if close[0] == SuperTrH3[0] and close[1] > SuperTrH3[1]:
                clr = clrGreen
            if close[0] == SuperTrH3[0] and close[1] < SuperTrH3[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBH3')
            TextDelete(0, '2LPBH3')
            TextCreate(0, '2LPBH3', 0, time[0] + PeriodSeconds(Period()), SuperTrH3[0], 'H3', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBH3', 0, time[0] + PeriodSeconds(Period()), SuperTrH3[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFH4:
        ArrayResize(SuperTrH4, 2)
        ArrayInitialize(SuperTrH4, 0.0)
        if CopyBufferAsSeries(handleSTrH4, 2, 0, 2, True, SuperTrH4):
            clr = clrBlack
            if close[0] < SuperTrH4[0]:
                clr = clrRed
            if close[0] > SuperTrH4[0]:
                clr = clrGreen
            if close[0] == SuperTrH4[0] and close[1] > SuperTrH4[1]:
                clr = clrGreen
            if close[0] == SuperTrH4[0] and close[1] < SuperTrH4[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBH4')
            TextDelete(0, '2LPBH4')
            TextCreate(0, '2LPBH4', 0, time[0] + PeriodSeconds(Period()), SuperTrH4[0], 'H4', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBH4', 0, time[0] + PeriodSeconds(Period()), SuperTrH4[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFH6:
        ArrayResize(SuperTrH6, 2)
        ArrayInitialize(SuperTrH6, 0.0)
        if CopyBufferAsSeries(handleSTrH6, 2, 0, 2, True, SuperTrH6):
            clr = clrBlack
            if close[0] < SuperTrH6[0]:
                clr = clrRed
            if close[0] > SuperTrH6[0]:
                clr = clrGreen
            if close[0] == SuperTrH6[0] and close[1] > SuperTrH6[1]:
                clr = clrGreen
            if close[0] == SuperTrH6[0] and close[1] < SuperTrH6[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBH6')
            TextDelete(0, '2LPBH6')
            TextCreate(0, '2LPBH6', 0, time[0] + PeriodSeconds(Period()), SuperTrH6[0], 'H6', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBH6', 0, time[0] + PeriodSeconds(Period()), SuperTrH6[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFH8:
        ArrayResize(SuperTrH8, 2)
        ArrayInitialize(SuperTrH8, 0.0)
        if CopyBufferAsSeries(handleSTrH8, 2, 0, 2, True, SuperTrH8):
            clr = clrBlack
            if close[0] < SuperTrH8[0]:
                clr = clrRed
            if close[0] > SuperTrH8[0]:
                clr = clrGreen
            if close[0] == SuperTrH8[0] and close[1] > SuperTrH8[1]:
                clr = clrGreen
            if close[0] == SuperTrH8[0] and close[1] < SuperTrH8[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBH8')
            TextDelete(0, '2LPBH8')
            TextCreate(0, '2LPBH8', 0, time[0] + PeriodSeconds(Period()), SuperTrH8[0], 'H8', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBH8', 0, time[0] + PeriodSeconds(Period()), SuperTrH8[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFH12:
        ArrayResize(SuperTrH12, 2)
        ArrayInitialize(SuperTrH12, 0.0)
        if CopyBufferAsSeries(handleSTrH12, 2, 0, 2, True, SuperTrH12):
            clr = clrBlack
            if close[0] < SuperTrH12[0]:
                clr = clrRed
            if close[0] > SuperTrH12[0]:
                clr = clrGreen
            if close[0] == SuperTrH12[0] and close[1] > SuperTrH12[1]:
                clr = clrGreen
            if close[0] == SuperTrH12[0] and close[1] < SuperTrH12[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBH12')
            TextDelete(0, '2LPBH12')
            TextCreate(0, '2LPBH12', 0, time[0] + PeriodSeconds(Period()), SuperTrH12[0], 'H12', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBH12', 0, time[0] + PeriodSeconds(Period()), SuperTrH12[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFD:
        ArrayResize(SuperTrD, 2)
        ArrayInitialize(SuperTrD, 0.0)
        if CopyBufferAsSeries(handleSTrD, 2, 0, 2, True, SuperTrD):
            clr = clrBlack
            if close[0] < SuperTrD[0]:
                clr = clrRed
            if close[0] > SuperTrD[0]:
                clr = clrGreen
            if close[0] == SuperTrD[0] and close[1] > SuperTrD[1]:
                clr = clrGreen
            if close[0] == SuperTrD[0] and close[1] < SuperTrD[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBD')
            TextDelete(0, '2LPBD')
            TextCreate(0, '2LPBD', 0, time[0] + PeriodSeconds(Period()), SuperTrD[0], 'D1', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBD', 0, time[0] + PeriodSeconds(Period()), SuperTrD[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFW:
        ArrayResize(SuperTrW, 2)
        ArrayInitialize(SuperTrW, 0.0)
        if CopyBufferAsSeries(handleSTrW, 2, 0, 2, True, SuperTrW):
            clr = clrBlack
            if close[0] < SuperTrW[0]:
                clr = clrRed
            if close[0] > SuperTrW[0]:
                clr = clrGreen
            if close[0] == SuperTrW[0] and close[1] > SuperTrW[1]:
                clr = clrGreen
            if close[0] == SuperTrW[0] and close[1] < SuperTrW[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBW')
            TextDelete(0, '2LPBW')
            TextCreate(0, '2LPBW', 0, time[0] + PeriodSeconds(Period()), SuperTrW[0], 'W1', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBW', 0, time[0] + PeriodSeconds(Period()), SuperTrW[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    if swTFM:
        ArrayResize(SuperTrM, 2)
        ArrayInitialize(SuperTrM, 0.0)
        if CopyBufferAsSeries(handleSTrM, 2, 0, 2, True, SuperTrM):
            clr = clrBlack
            if close[0] < SuperTrM[0]:
                clr = clrRed
            if close[0] > SuperTrM[0]:
                clr = clrGreen
            if close[0] == SuperTrM[0] and close[1] > SuperTrM[1]:
                clr = clrGreen
            if close[0] == SuperTrM[0] and close[1] < SuperTrM[1]:
                clr = clrRed
            ArrowRightPriceDelete(0, 'LPBM')
            TextDelete(0, '2LPBM')
            TextCreate(0, '2LPBM', 0, time[0] + PeriodSeconds(Period()), SuperTrM[0], 'MN1', 'Arial', sizeFont, clr, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0)
            ArrowRightPriceCreate(0, 'LPBM', 0, time[0] + PeriodSeconds(Period()), SuperTrM[0], clr, STYLE_SOLID, sizeP, False, False, True, 0)
            ChartRedraw()
    return rates_total

def ArrowRightPriceCreate(chart_ID=0, name='RightPrice', sub_window=0, time=0, price=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, hidden=True, z_order=0):
    time = Box(time)
    price = Box(price)
    ChangeArrowEmptyPoint(time, price)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_ARROW_RIGHT_PRICE, sub_window, time.v, price.v):
        Print('ArrowRightPriceCreate', ': Failed to create the left price label! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def ArrowRightPriceDelete(chart_ID=0, name='RightPrice'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('ArrowRightPriceDelete', ': Failed to delete the left price label! Error code = ', GetLastError())
        return False
    return True

def CopyBufferAsSeries(_handle, bufer, start, number, asSeries, M):
    if CopyBuffer(_handle, bufer, start, number, M) <= 0:
        return False
    ArraySetAsSeries(M, asSeries)
    return True

def ChangeArrowEmptyPoint(time, price):
    if not time.v:
        time.v = TimeCurrent()
    if not price.v:
        price.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)

def TextCreate(chart_ID=0, name='Text', sub_window=0, time=0, price=0.0, text='Text', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    time = Box(time)
    price = Box(price)
    ChangeTextEmptyPoint(time, price)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time.v, price.v):
        Print('TextCreate', ': failed to create the "Text" object! Error code = ', GetLastError())
        return False
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def TextDelete(chart_ID=0, name='Text'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('TextDelete', ': failed to delete the "Text" object! Error code = ', GetLastError())
        return False
    return True

def ChangeTextEmptyPoint(time, price):
    if not time.v:
        time.v = TimeCurrent()
    if not price.v:
        price.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)

def OnDeinit(reason):
    ArrowRightPriceDelete(0, 'LPB1')
    ArrowRightPriceDelete(0, 'LPB2')
    ArrowRightPriceDelete(0, 'LPB3')
    ArrowRightPriceDelete(0, 'LPB4')
    ArrowRightPriceDelete(0, 'LPB5')
    ArrowRightPriceDelete(0, 'LPB6')
    ArrowRightPriceDelete(0, 'LPB10')
    ArrowRightPriceDelete(0, 'LPB12')
    ArrowRightPriceDelete(0, 'LPB15')
    ArrowRightPriceDelete(0, 'LPB20')
    ArrowRightPriceDelete(0, 'LPB30')
    ArrowRightPriceDelete(0, 'LPBH1')
    ArrowRightPriceDelete(0, 'LPBH2')
    ArrowRightPriceDelete(0, 'LPBH3')
    ArrowRightPriceDelete(0, 'LPBH4')
    ArrowRightPriceDelete(0, 'LPBH6')
    ArrowRightPriceDelete(0, 'LPBH8')
    ArrowRightPriceDelete(0, 'LPBH12')
    ArrowRightPriceDelete(0, 'LPBD')
    ArrowRightPriceDelete(0, 'LPBW')
    ArrowRightPriceDelete(0, 'LPBM')
    TextDelete(0, '2LPB1')
    TextDelete(0, '2LPB2')
    TextDelete(0, '2LPB3')
    TextDelete(0, '2LPB4')
    TextDelete(0, '2LPB5')
    TextDelete(0, '2LPB6')
    TextDelete(0, '2LPB10')
    TextDelete(0, '2LPB12')
    TextDelete(0, '2LPB15')
    TextDelete(0, '2LPB20')
    TextDelete(0, '2LPB30')
    TextDelete(0, '2LPBH1')
    TextDelete(0, '2LPBH2')
    TextDelete(0, '2LPBH3')
    TextDelete(0, '2LPBH4')
    TextDelete(0, '2LPBH6')
    TextDelete(0, '2LPBH8')
    TextDelete(0, '2LPBH12')
    TextDelete(0, '2LPBD')
    TextDelete(0, '2LPBW')
    TextDelete(0, '2LPBM')
    ChartRedraw()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Supertrendmtf(_MQL5Indicator):
    name = 'supertrendmtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodST': 10,  # Supertrend period
        'Multiplier': 3.0,  # Supertrend multiplier
        'swTF1': False,  # Use TF 1 min
        'swTF2': False,  # Use TF 2 min
        'swTF3': False,  # Use TF 3 min
        'swTF4': False,  # Use TF 4 min
        'swTF5': False,  # Use TF 5 min
        'swTF6': False,  # Use TF 6 min
        'swTF10': False,  # Use TF 10 min
        'swTF12': False,  # Use TF 12 min
        'swTF15': True,  # Use TF 15 min
        'swTF20': True,  # Use TF 20 min
        'swTF30': True,  # Use TF 30 min
        'swTFH1': True,  # Use TF 1 h
        'swTFH2': False,  # Use TF 2 h
        'swTFH3': False,  # Use TF 3 h
        'swTFH4': False,  # Use TF 4 h
        'swTFH6': False,  # Use TF 6 h
        'swTFH8': False,  # Use TF 8 h
        'swTFH12': False,  # Use TF 12 h
        'swTFD': False,  # Use TF D
        'swTFW': False,  # Use TF W
        'swTFM': False,  # Use TF M
        'sizeFont': 8,  # Text size
        'sizeP': 1,  # Price mark size
    }

