"""Binary_Options_Simulated_Trading — converted from MQL5: MQL5 Indicators/Binary Options Simulated Trading Indicator for MT5/Binary_Options_Simulated_Trading.mq5

Binary Options Simulated Trading
Copyright: Coded by Leon Lam (QQ: 82756); Link: http://wpa.qq.com/msgrd?v=3&uin=82756&site=qq&menu=yes; Version: 17.429

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Leon Lam (QQ: 82756)', 'link': 'http://wpa.qq.com/msgrd?v=3&uin=82756&site=qq&menu=yes', 'version': '17.429', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Binary Options Simulated Trading'], 'name': 'Binary_Options_Simulated_Trading', 'source': 'MQL5 Indicators/Binary Options Simulated Trading Indicator for MT5/Binary_Options_Simulated_Trading.mq5', 'folder': 'Binary Options Simulated Trading Indicator for MT5', 'inputs': [{'mql': 'BALANCE', 'py': 'BALANCE', 'param': 'BALANCE', 'type': 'double', 'default': 10000.0, 'label': 'Account Balance', 'sinput': False}, {'mql': 'AMOUNT', 'py': 'AMOUNT', 'param': 'AMOUNT', 'type': 'double', 'default': 10.0, 'label': 'Investment Amount (Lots)', 'sinput': False}, {'mql': 'MARGIN', 'py': 'MARGIN', 'param': 'MARGIN', 'type': 'double', 'default': 0.75, 'label': 'Profit Margin', 'sinput': False}, {'mql': 'EXPIRED', 'py': 'EXPIRED', 'param': 'EXPIRED', 'type': 'int', 'default': 3, 'label': 'Expiry Time (Minutes)', 'sinput': False}, {'mql': 'LANGUAGE', 'py': 'LANGUAGE', 'param': 'LANGUAGE', 'type': 'int', 'default': 1, 'label': 'Display Language', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_LANGUAGE
English = 0
Chinese = 1
_enum('ENUM_LANGUAGE', {0: 'English', 1: 'Chinese'})

# ---- inputs and global variables
BALANCE = _input('BALANCE', 10000.0)  # Account Balance
AMOUNT = _input('AMOUNT', 10.0)  # Investment Amount (Lots)
MARGIN = _input('MARGIN', 0.75)  # Profit Margin
EXPIRED = _input('EXPIRED', 3)  # Expiry Time (Minutes)
LANGUAGE = _input('LANGUAGE', Chinese)  # Display Language
OS_BALANCE = BALANCE  # Variable for account balance / investment amount / profit margin
OS_LOTS = AMOUNT  # Variable for account balance / investment amount / profit margin
OS_MARGIN = MARGIN  # Variable for account balance / investment amount / profit margin
OS_EXPIRED = EXPIRED  # Variable for expiry time / buy order / sell order
OP_BUY_v = 0  # Variable for expiry time / buy order / sell order
OP_SELL_v = 1  # Variable for expiry time / buy order / sell order
OS_ORDER = Arr.of([0.0, 0.0, -1.0], fill=0.0)  # Variables for time & price & buy/sell
OS_COUNT = Arr.of([0.0, 0.0, 0.0], fill=0.0)  # Variable for total & win & flat

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    CHART_ID = 0
    OBJ_NAME = 'ORDER LINE'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelRectangle'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelTitle'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelBalance'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelProfit'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelExpired'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelBtnExpMinus'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelBtnExpPlus'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelCount'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelBtnCall'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)
    OBJ_NAME = 'PanelBtnPut'
    if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
        ObjectDelete(CHART_ID, OBJ_NAME)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    PanelCreate()
    ORDER_CLOSE()
    return INIT_SUCCEEDED

def OnChartEvent(id_, lparam, dparam, sparam):
    global OS_EXPIRED
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if OS_ORDER[0] != 0 or OS_ORDER[1] != 0:
            return
        if sparam == 'PanelBtnCall':
            ORDER_OPEN(OP_BUY_v)
        if sparam == 'PanelBtnPut':
            ORDER_OPEN(OP_SELL_v)
        if sparam == 'PanelBtnExpMinus':
            if OS_EXPIRED <= 1:
                return
            OS_EXPIRED -= 1
        if sparam == 'PanelBtnExpPlus':
            if OS_EXPIRED >= 60:
                return
            OS_EXPIRED += 1

def ORDER_OPEN(OP):
    global OS_BALANCE
    if OS_ORDER[0] != 0 or OS_ORDER[1] != 0:
        return False
    if OS_BALANCE < OS_LOTS:
        return False
    if OP == OP_BUY_v:
        OS_ORDER[0] = _int(TimeCurrent())
        OS_ORDER[1] = Close()
        OS_ORDER[2] = OP_BUY_v
        OS_BALANCE -= OS_LOTS
        ORDER_LINE(OP)
        return True
    if OP == OP_SELL_v:
        OS_ORDER[0] = _int(TimeCurrent())
        OS_ORDER[1] = Close()
        OS_ORDER[2] = OP_SELL_v
        OS_BALANCE -= OS_LOTS
        ORDER_LINE(OP)
        return True
    return False

def ORDER_CLOSE():
    global OS_BALANCE
    if OS_ORDER[0] != 0 and OS_ORDER[1] != 0:
        if TimeCurrent() >= (OS_ORDER[0] + (OS_EXPIRED * 60)):
            if OS_ORDER[2] == OP_BUY_v:
                if Close() == OS_ORDER[1]:
                    OS_BALANCE += OS_LOTS
                    OS_COUNT[2] += 1
                if Close() > OS_ORDER[1]:
                    OS_BALANCE += OS_LOTS + (OS_LOTS * OS_MARGIN)
                    OS_COUNT[1] += 1
            if OS_ORDER[2] == OP_SELL_v:
                if Close() == OS_ORDER[1]:
                    OS_BALANCE += OS_LOTS
                    OS_COUNT[2] += 1
                if Close() < OS_ORDER[1]:
                    OS_BALANCE += OS_LOTS + (OS_LOTS * OS_MARGIN)
                    OS_COUNT[1] += 1
            OS_COUNT[0] += 1
            OS_ORDER[0] = 0.0
            OS_ORDER[1] = 0.0
            OS_ORDER[2] = -1.0
            CHART_ID = 0
            OBJ_NAME = 'ORDER LINE'
            if ObjectFind(CHART_ID, OBJ_NAME) >= 0:
                ObjectDelete(CHART_ID, OBJ_NAME)

def ORDER_LINE(OP):
    CHART_ID = 0
    OBJ_NAME = 'ORDER LINE'
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_HLINE, 0, 0, Close())
        ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
        ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
        ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
        ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, (clrRed if (OP == OP_BUY_v) else clrLime))
        ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_STYLE, STYLE_DASHDOT)
        if LANGUAGE == Chinese:
            ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, ('买涨' if (OP == OP_BUY_v) else '买跌') + _str(OS_EXPIRED) + '分钟 (' + TimeToString(TimeCurrent(), TIME_DATE) + ' ' + TimeToString(TimeCurrent(), TIME_SECONDS) + ')')
        else:
            ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, ('Buy' if (OP == OP_BUY_v) else 'Sell') + ' ' + _str(OS_EXPIRED) + ' Minutes (' + TimeToString(TimeCurrent(), TIME_DATE) + ' ' + TimeToString(TimeCurrent(), TIME_SECONDS) + ')')

def PanelCreate():
    CHART_ID = 0
    OBJ_NAME = 'PanelRectangle'
    OBJ_CLOCK = ""
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_RECTANGLE_LABEL, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FILL, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BGCOLOR, 0x0A0A0A)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BORDER_TYPE, BORDER_FLAT)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_WIDTH, 1)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 115)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 5)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XSIZE, 110)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YSIZE, 120)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    OBJ_NAME = 'PanelTitle'
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 110)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 10)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FONTSIZE, 9)
    if LANGUAGE == Chinese:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Microsoft Yahei')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, '二元期权模拟交易')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, '二元期权模拟交易')
    else:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Arial Black')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, 'Binary Options')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, 'Binary Options Simulated Trading')
    OBJ_NAME = 'PanelBalance'
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 110)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 30)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FONTSIZE, 8)
    if LANGUAGE == Chinese:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Microsoft Yahei')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, '余额 ' + _str(OS_BALANCE))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, '余额 ' + _str(OS_BALANCE))
    else:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Arial')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, 'BAL: ' + _str(OS_BALANCE))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, 'Balance: ' + _str(OS_BALANCE))
    OBJ_NAME = 'PanelProfit'
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 110)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 45)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FONTSIZE, 8)
    if LANGUAGE == Chinese:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Microsoft Yahei')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, '收益 ' + _str(OS_LOTS) + '*' + _str(OS_MARGIN) + '=' + _str(OS_LOTS * OS_MARGIN))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, '收益 ' + _str(OS_LOTS) + '*' + _str(OS_MARGIN) + '=' + _str(OS_LOTS * OS_MARGIN))
    else:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Arial')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, 'PRO: ' + _str(OS_LOTS) + '*' + _str(OS_MARGIN) + '=' + _str(OS_LOTS * OS_MARGIN))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, 'Profit: ' + _str(OS_LOTS) + '*' + _str(OS_MARGIN) + '=' + _str(OS_LOTS * OS_MARGIN))
    OBJ_NAME = 'PanelExpired'
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 110)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 60)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FONTSIZE, 8)
    if LANGUAGE == Chinese:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Microsoft Yahei')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, '到期 ' + _str(OS_EXPIRED) + ' 分钟')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, '到期 ' + _str(OS_EXPIRED) + ' 分钟')
    else:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Arial')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, 'EXP: ' + _str(OS_EXPIRED) + ' Minutes')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, 'Expired: ' + _str(OS_EXPIRED) + ' Minutes')
    OBJ_NAME = 'PanelBtnExpMinus'
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_BUTTON, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 36)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 62)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XSIZE, 12)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YSIZE, 12)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_ALIGN, ALIGN_CENTER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BGCOLOR, clrLime)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BORDER_COLOR, clrLime)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FONTSIZE, 9)
    if LANGUAGE == Chinese:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Microsoft Yahei')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, '－')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, '减小1分钟')
    else:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Arial Black')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, '-')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, 'Subtract 1 minute')
    OBJ_NAME = 'PanelBtnExpPlus'
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_BUTTON, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 22)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 62)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XSIZE, 12)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YSIZE, 12)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_ALIGN, ALIGN_CENTER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BGCOLOR, clrRed)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BORDER_COLOR, clrRed)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FONTSIZE, 9)
    if LANGUAGE == Chinese:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Microsoft Yahei')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, '＋')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, '增加1分钟')
    else:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Arial Black')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, '+')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, 'Add 1 minute')
    OBJ_NAME = 'PanelCount'
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 110)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 75)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FONTSIZE, 8)
    if LANGUAGE == Chinese:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Microsoft Yahei')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, '胜率 ' + ('0%' if (OS_COUNT[0] == 0) else (DoubleToString(_fdiv(OS_COUNT[1], OS_COUNT[0]) * 100, 1) + '% (' + _str(OS_COUNT[1]) + '/' + _str(OS_COUNT[0]) + ')')))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, '胜率 ' + ('0%' if (OS_COUNT[0] == 0) else (DoubleToString(_fdiv(OS_COUNT[1], OS_COUNT[0]) * 100, 1) + '% (胜 ' + _str(OS_COUNT[1]) + ', 平 ' + _str(OS_COUNT[2]) + ', 共 ' + _str(OS_COUNT[0]) + ')')))
    else:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Arial')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, 'WIN: ' + ('0%' if (OS_COUNT[0] == 0) else (DoubleToString(_fdiv(OS_COUNT[1], OS_COUNT[0]) * 100, 1) + '% (' + _str(OS_COUNT[1]) + '/' + _str(OS_COUNT[0]) + ')')))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, 'Win rate: ' + ('0%' if (OS_COUNT[0] == 0) else (DoubleToString(_fdiv(OS_COUNT[1], OS_COUNT[0]) * 100, 1) + '% (Win ' + _str(OS_COUNT[1]) + ', Flat ' + _str(OS_COUNT[2]) + ', Total ' + _str(OS_COUNT[0]) + ')')))
    OBJ_NAME = 'PanelBtnCall'
    OBJ_CLOCK = ''
    if OS_ORDER[2] == OP_BUY_v and OS_ORDER[0] != 0:
        OBJ_CLOCK = DoubleToString(OS_ORDER[0] + (OS_EXPIRED * 60) - _int(TimeCurrent()), 0) + (' :)' if (OS_ORDER[1] < Close()) else ' :(' if (OS_ORDER[1] > Close()) else ' :|')
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_BUTTON, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 110)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 99)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XSIZE, 45)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YSIZE, 20)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_ALIGN, ALIGN_CENTER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BGCOLOR, clrRed)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BORDER_COLOR, clrRed)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FONTSIZE, 9)
    if LANGUAGE == Chinese:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Microsoft Yahei')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, ('买涨▲' if (OBJ_CLOCK == '') else OBJ_CLOCK))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, '买涨' + _str(OS_EXPIRED) + '分钟')
    else:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Arial')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, ('Buy▲' if (OBJ_CLOCK == '') else OBJ_CLOCK))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, 'Buy ' + _str(OS_EXPIRED) + ' Minutes')
    OBJ_NAME = 'PanelBtnPut'
    OBJ_CLOCK = ''
    if OS_ORDER[2] == OP_SELL_v and OS_ORDER[0] != 0:
        OBJ_CLOCK = DoubleToString(OS_ORDER[0] + (OS_EXPIRED * 60) - _int(TimeCurrent()), 0) + (' :)' if (OS_ORDER[1] > Close()) else ' :(' if (OS_ORDER[1] < Close()) else ' :|')
    if ObjectFind(CHART_ID, OBJ_NAME) < 0:
        ObjectCreate(CHART_ID, OBJ_NAME, OBJ_BUTTON, 0, 0, 0)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XDISTANCE, 55)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YDISTANCE, 99)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, True)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_XSIZE, 45)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_YSIZE, 20)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_ALIGN, ALIGN_CENTER)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BGCOLOR, clrLime)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BORDER_COLOR, clrLime)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_FONTSIZE, 9)
    if LANGUAGE == Chinese:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Microsoft Yahei')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, ('买跌▼' if (OBJ_CLOCK == '') else OBJ_CLOCK))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, '买跌' + _str(OS_EXPIRED) + '分钟')
    else:
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_FONT, 'Arial')
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TEXT, ('Sell▼' if (OBJ_CLOCK == '') else OBJ_CLOCK))
        ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, 'Sell ' + _str(OS_EXPIRED) + ' Minutes')

def Close():
    return SymbolInfoDouble(Symbol(), SYMBOL_BID)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BinaryOptionsSimulatedTrading(_MQL5Indicator):
    name = 'Binary_Options_Simulated_Trading'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BALANCE': 10000.0,  # Account Balance
        'AMOUNT': 10.0,  # Investment Amount (Lots)
        'MARGIN': 0.75,  # Profit Margin
        'EXPIRED': 3,  # Expiry Time (Minutes)
        'LANGUAGE': _Choice({0: 'Define Language', 1: 'Define Language'}, default=1),  # Display Language
    }

