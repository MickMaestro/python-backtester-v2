"""CamarillaFlatandClear — converted from MQL5: MQL5 Indicators/CamarillaFlatandClear/CamarillaFlatandClear.mq5

Copyright: Erdem Bozyel; Link: mailto:bozyel67@hotmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Erdem Bozyel', 'link': 'mailto:bozyel67@hotmail.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'CamarillaFlatandClear', 'source': 'MQL5 Indicators/CamarillaFlatandClear/CamarillaFlatandClear.mq5', 'folder': 'CamarillaFlatandClear', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    YuksekGun = iHigh(None, PERIOD_D1, 1)
    DusukGun = iLow(None, PERIOD_D1, 1)
    KapanisGun = iClose(None, PERIOD_D1, 1)
    PivotGun = (YuksekGun + DusukGun + KapanisGun) / 3
    H5 = _fdiv(YuksekGun, DusukGun) * KapanisGun
    H4 = ((1.1 * (YuksekGun - DusukGun)) / 2) + KapanisGun
    H3 = ((1.1 * (YuksekGun - DusukGun)) / 4) + KapanisGun
    H2 = ((1.1 * (YuksekGun - DusukGun)) / 6) + KapanisGun
    H1 = ((1.1 * (YuksekGun - DusukGun)) / 12) + KapanisGun
    L1 = KapanisGun - ((1.1 * (YuksekGun - DusukGun)) / 12)
    L2 = KapanisGun - ((1.1 * (YuksekGun - DusukGun)) / 6)
    L3 = KapanisGun - ((1.1 * (YuksekGun - DusukGun)) / 4)
    L4 = KapanisGun - ((1.1 * (YuksekGun - DusukGun)) / 2)
    L5 = KapanisGun - (H5 - KapanisGun)
    ObjectDelete(0, 'H5')
    ObjectCreate(0, 'H5', OBJ_HLINE, 0, 0, H5)
    ObjectSetInteger(0, 'H5', OBJPROP_COLOR, clrGreen)
    ObjectSetInteger(0, 'H5', OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, 'H5', OBJPROP_WIDTH, 2)
    ObjectSetInteger(0, 'H5', OBJPROP_BACK, False)
    ObjectSetString(0, 'H5', OBJPROP_TEXT, 'H5 LB Target')
    ObjectSetDouble(0, 'H5', OBJPROP_PRICE, H5)
    ObjectDelete(0, 'H4')
    ObjectCreate(0, 'H4', OBJ_HLINE, 0, 0, H4)
    ObjectSetInteger(0, 'H4', OBJPROP_COLOR, clrGreen)
    ObjectSetInteger(0, 'H4', OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, 'H4', OBJPROP_WIDTH, 2)
    ObjectSetInteger(0, 'H4', OBJPROP_BACK, False)
    ObjectSetString(0, 'H4', OBJPROP_TEXT, 'H4 Long BreakOut')
    ObjectSetDouble(0, 'H4', OBJPROP_PRICE, H4)
    ObjectDelete(0, 'H3')
    ObjectCreate(0, 'H3', OBJ_HLINE, 0, 0, H3)
    ObjectSetInteger(0, 'H3', OBJPROP_COLOR, clrRed)
    ObjectSetInteger(0, 'H3', OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, 'H3', OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, 'H3', OBJPROP_BACK, False)
    ObjectSetString(0, 'H3', OBJPROP_TEXT, 'H3 Short')
    ObjectSetDouble(0, 'H3', OBJPROP_PRICE, H3)
    ObjectDelete(0, 'PivotGun')
    ObjectCreate(0, 'PivotGun', OBJ_HLINE, 0, 0, PivotGun)
    ObjectSetInteger(0, 'PivotGun', OBJPROP_COLOR, clrMaroon)
    ObjectSetInteger(0, 'PivotGun', OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, 'PivotGun', OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, 'PivotGun', OBJPROP_BACK, False)
    ObjectSetString(0, 'PivotGun', OBJPROP_TEXT, 'Pivot')
    ObjectSetDouble(0, 'PivotGun', OBJPROP_PRICE, PivotGun)
    ObjectDelete(0, 'L3')
    ObjectCreate(0, 'L3', OBJ_HLINE, 0, 0, L3)
    ObjectSetInteger(0, 'L3', OBJPROP_COLOR, clrGreen)
    ObjectSetInteger(0, 'L3', OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, 'L3', OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, 'L3', OBJPROP_BACK, False)
    ObjectSetString(0, 'L3', OBJPROP_TEXT, 'L3 Long')
    ObjectSetDouble(0, 'L3', OBJPROP_PRICE, L3)
    ObjectDelete(0, 'L4')
    ObjectCreate(0, 'L4', OBJ_HLINE, 0, 0, L4)
    ObjectSetInteger(0, 'L4', OBJPROP_COLOR, clrRed)
    ObjectSetInteger(0, 'L4', OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, 'L4', OBJPROP_WIDTH, 2)
    ObjectSetInteger(0, 'L4', OBJPROP_BACK, False)
    ObjectSetString(0, 'L4', OBJPROP_TEXT, 'L4 Short BreakOut')
    ObjectSetDouble(0, 'L4', OBJPROP_PRICE, L4)
    ObjectDelete(0, 'L5')
    ObjectCreate(0, 'L5', OBJ_HLINE, 0, 0, L5)
    ObjectSetInteger(0, 'L5', OBJPROP_COLOR, clrRed)
    ObjectSetInteger(0, 'L5', OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, 'L5', OBJPROP_WIDTH, 2)
    ObjectSetInteger(0, 'L5', OBJPROP_BACK, False)
    ObjectSetString(0, 'L5', OBJPROP_TEXT, 'L5 SB Target')
    ObjectSetDouble(0, 'L5', OBJPROP_PRICE, L5)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CamarillaFlatandClear(_MQL5Indicator):
    name = 'CamarillaFlatandClear'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

