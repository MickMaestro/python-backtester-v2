"""Lot calculator — converted from MQL5: MQL5 Indicators/Lot calculator - risk management tool/Lot calculator.mq5

Tool used to calculate the correct lot size to trade, given a fixed risk and a number of pips.
Simply enter the number of pips of your desired stop loss order, and the indicator will show you 
the number of lots to trade based on your total account amount, your account currency and present chart currency pair.
Copyright: Copyleft 2018, by zebedeig; Link: https://www.mql5.com/en/users/zebedeig; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyleft 2018, by zebedeig', 'link': 'https://www.mql5.com/en/users/zebedeig', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Tool used to calculate the correct lot size to trade, given a fixed risk and a number of pips.', 'Simply enter the number of pips of your desired stop loss order, and the indicator will show you ', 'the number of lots to trade based on your total account amount, your account currency and present chart currency pair.'], 'name': 'Lot calculator', 'source': 'MQL5 Indicators/Lot calculator - risk management tool/Lot calculator.mq5', 'folder': 'Lot calculator - risk management tool', 'inputs': [{'mql': 'Pips', 'py': 'Pips', 'param': 'Pips', 'type': 'int', 'default': 165, 'label': 'Stop loss distance from open order', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'double', 'default': 0.02, 'label': 'Free margin fraction you want to risk for the trade', 'sinput': False}, {'mql': 'useAccountBalance', 'py': 'useAccountBalance', 'param': 'useAccountBalance', 'type': 'bool', 'default': True, 'label': 'Check to read the actual free margin of your balance, uncheck to specify it', 'sinput': False}, {'mql': 'AccountBalance', 'py': 'AccountBalance_v', 'param': 'AccountBalance_v', 'type': 'int', 'default': 2000, 'label': 'Specify here a simulated balance value', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

ACCOUNT_FREEMARGIN = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
Pips = _input('Pips', 165)  # Stop loss distance from open order
Risk = _input('Risk', 0.02)  # Free margin fraction you want to risk for the trade
useAccountBalance = _input('useAccountBalance', True)  # Check to read the actual free margin of your balance, uncheck to specify it
AccountBalance_v = _input('AccountBalance_v', 2000)  # Specify here a simulated balance value
point = 0.0

def OnInit():
    global point
    point = Point()
    Digits_ = Digits()
    if Digits() == 3 or Digits() == 5:
        point *= 10
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    Print('OnDeinit', '_UninitReason = ', getUninitReasonText(0))
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    CommentString = ''
    DepositCurrency = AccountInfoString(ACCOUNT_CURRENCY)
    freeMargin = 0.0
    if useAccountBalance:
        freeMargin = AccountInfoDouble(ACCOUNT_FREEMARGIN)
    else:
        freeMargin = AccountBalance_v
    PipValue = _fdiv(SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE) * point, SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_SIZE))
    lots = _fdiv(Risk * freeMargin, PipValue * Pips)
    lots = floor(lots * 100) / 100
    CommentString += '\n' + 'Your free margin: ' + DepositCurrency + ' ' + DoubleToString(freeMargin, 2) + '\n'
    CommentString += 'Risk selected: ' + DoubleToString(Risk * 100, 0) + '%\n'
    CommentString += 'Risk selected: ' + DepositCurrency + ' ' + DoubleToString(Risk * freeMargin, 2) + '\n'
    CommentString += '-----------------------------------------------------------------\n'
    CommentString += 'Value of one pip trading 1 lot of ' + Symbol() + ': ' + DepositCurrency + ' ' + DoubleToString(PipValue, 3) + '\n'
    CommentString += 'Max lots of ' + Symbol() + ' to trade while risking ' + _str(Pips) + ' pips: ' + DoubleToString(lots, 2) + '\n'
    CommentString += '-----------------------------------------------------------------\n'
    Comment(CommentString)
    return rates_total

def getUninitReasonText(reasonCode):
    text = ''
    _sw1 = reasonCode
    if _sw1 == REASON_ACCOUNT:
        text = 'Account was changed'
    elif _sw1 == REASON_CHARTCHANGE:
        text = 'Symbol or timeframe was changed'
    elif _sw1 == REASON_CHARTCLOSE:
        text = 'Chart was closed'
    elif _sw1 == REASON_PARAMETERS:
        text = 'Input-parameter was changed'
    elif _sw1 == REASON_RECOMPILE:
        text = 'Program ' + 'Lot calculator.mq5' + ' was recompiled'
    elif _sw1 == REASON_REMOVE:
        text = 'Program ' + 'Lot calculator.mq5' + ' was removed from chart'
    elif _sw1 == REASON_TEMPLATE:
        text = 'New template was applied to chart'
    else:
        text = 'Another reason'
    return text


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LotCalculator(_MQL5Indicator):
    name = 'Lot calculator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Pips': 165,  # Stop loss distance from open order
        'Risk': 0.02,  # Free margin fraction you want to risk for the trade
        'useAccountBalance': True,  # Check to read the actual free margin of your balance, uncheck to specify it
        'AccountBalance_v': 2000,  # Specify here a simulated balance value
    }

