"""RainbowMMA — converted from MQL5: MQL5 Indicators/Rainbow Multiple Moving Average (RMMA) MT5/RainbowMMA.mq5

Rainbow Multiple Moving Average - 66 multi-colored MA lines.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 66, 'indicator_plots': 66}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1, 42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 1, 48: 1, 49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 1, 55: 1, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 1, 64: 1, 65: 1, 66: 1}, 'colors': {1: [13850042], 2: [13850042], 3: [13850042], 4: [13850042], 5: [13850042], 6: [13850042], 7: [13850042], 8: [13850042], 9: [13850042], 10: [13850042], 11: [13850042], 12: [13850042], 13: [13850042], 14: [13850042], 15: [13850042], 16: [13850042], 17: [13353215], 18: [13353215], 19: [13353215], 20: [13353215], 21: [13353215], 22: [13353215], 23: [13353215], 24: [13353215], 25: [13353215], 26: [13353215], 27: [13353215], 28: [13353215], 29: [65280], 30: [65280], 31: [65280], 32: [65280], 33: [65280], 34: [65280], 35: [65280], 36: [65280], 37: [65280], 38: [65280], 39: [65280], 40: [16760576], 41: [16760576], 42: [16760576], 43: [16760576], 44: [16760576], 45: [16760576], 46: [16760576], 47: [16760576], 48: [16760576], 49: [16760576], 50: [16760576], 51: [16760576], 52: [16760576], 53: [55295], 54: [55295], 55: [55295], 56: [55295], 57: [55295], 58: [55295], 59: [55295], 60: [55295], 61: [55295], 62: [55295], 63: [55295], 64: [55295], 65: [55295], 66: [55295]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Rainbow Multiple Moving Average - 66 multi-colored MA lines.'], 'name': 'RainbowMMA', 'source': 'MQL5 Indicators/Rainbow Multiple Moving Average (RMMA) MT5/RainbowMMA.mq5', 'folder': 'Rainbow Multiple Moving Average (RMMA) MT5', 'inputs': [{'mql': 'MA_Type', 'py': 'MA_Type', 'param': 'MA_Type', 'type': 'int', 'default': 1, 'label': 'MA Type', 'sinput': False}, {'mql': 'MA_Price', 'py': 'MA_Price', 'param': 'MA_Price', 'type': 'int', 'default': 1, 'label': 'MA Price', 'sinput': False}, {'mql': 'MA_Period_01', 'py': 'MA_Period_01', 'param': 'MA_Period_01', 'type': 'int', 'default': 200, 'label': 'MA 01 Period', 'sinput': False}, {'mql': 'MA_Period_02', 'py': 'MA_Period_02', 'param': 'MA_Period_02', 'type': 'int', 'default': 195, 'label': 'MA 02 Period', 'sinput': False}, {'mql': 'MA_Period_03', 'py': 'MA_Period_03', 'param': 'MA_Period_03', 'type': 'int', 'default': 190, 'label': 'MA 03 Period', 'sinput': False}, {'mql': 'MA_Period_04', 'py': 'MA_Period_04', 'param': 'MA_Period_04', 'type': 'int', 'default': 185, 'label': 'MA 04 Period', 'sinput': False}, {'mql': 'MA_Period_05', 'py': 'MA_Period_05', 'param': 'MA_Period_05', 'type': 'int', 'default': 180, 'label': 'MA 05 Period', 'sinput': False}, {'mql': 'MA_Period_06', 'py': 'MA_Period_06', 'param': 'MA_Period_06', 'type': 'int', 'default': 175, 'label': 'MA 06 Period', 'sinput': False}, {'mql': 'MA_Period_07', 'py': 'MA_Period_07', 'param': 'MA_Period_07', 'type': 'int', 'default': 170, 'label': 'MA 07 Period', 'sinput': False}, {'mql': 'MA_Period_08', 'py': 'MA_Period_08', 'param': 'MA_Period_08', 'type': 'int', 'default': 165, 'label': 'MA 08 Period', 'sinput': False}, {'mql': 'MA_Period_09', 'py': 'MA_Period_09', 'param': 'MA_Period_09', 'type': 'int', 'default': 160, 'label': 'MA 09 Period', 'sinput': False}, {'mql': 'MA_Period_10', 'py': 'MA_Period_10', 'param': 'MA_Period_10', 'type': 'int', 'default': 155, 'label': 'MA 10 Period', 'sinput': False}, {'mql': 'MA_Period_11', 'py': 'MA_Period_11', 'param': 'MA_Period_11', 'type': 'int', 'default': 150, 'label': 'MA 11 Period', 'sinput': False}, {'mql': 'MA_Period_12', 'py': 'MA_Period_12', 'param': 'MA_Period_12', 'type': 'int', 'default': 145, 'label': 'MA 12 Period', 'sinput': False}, {'mql': 'MA_Period_13', 'py': 'MA_Period_13', 'param': 'MA_Period_13', 'type': 'int', 'default': 140, 'label': 'MA 13 Period', 'sinput': False}, {'mql': 'MA_Period_14', 'py': 'MA_Period_14', 'param': 'MA_Period_14', 'type': 'int', 'default': 135, 'label': 'MA 14 Period', 'sinput': False}, {'mql': 'MA_Period_15', 'py': 'MA_Period_15', 'param': 'MA_Period_15', 'type': 'int', 'default': 130, 'label': 'MA 15 Period', 'sinput': False}, {'mql': 'MA_Period_16', 'py': 'MA_Period_16', 'param': 'MA_Period_16', 'type': 'int', 'default': 125, 'label': 'MA 16 Period', 'sinput': False}, {'mql': 'MA_Period_17', 'py': 'MA_Period_17', 'param': 'MA_Period_17', 'type': 'int', 'default': 122, 'label': 'MA 17 Period', 'sinput': False}, {'mql': 'MA_Period_18', 'py': 'MA_Period_18', 'param': 'MA_Period_18', 'type': 'int', 'default': 118, 'label': 'MA 18 Period', 'sinput': False}, {'mql': 'MA_Period_19', 'py': 'MA_Period_19', 'param': 'MA_Period_19', 'type': 'int', 'default': 114, 'label': 'MA 19 Period', 'sinput': False}, {'mql': 'MA_Period_20', 'py': 'MA_Period_20', 'param': 'MA_Period_20', 'type': 'int', 'default': 110, 'label': 'MA 20 Period', 'sinput': False}, {'mql': 'MA_Period_21', 'py': 'MA_Period_21', 'param': 'MA_Period_21', 'type': 'int', 'default': 106, 'label': 'MA 21 Period', 'sinput': False}, {'mql': 'MA_Period_22', 'py': 'MA_Period_22', 'param': 'MA_Period_22', 'type': 'int', 'default': 102, 'label': 'MA 22 Period', 'sinput': False}, {'mql': 'MA_Period_23', 'py': 'MA_Period_23', 'param': 'MA_Period_23', 'type': 'int', 'default': 98, 'label': 'MA 23 Period', 'sinput': False}, {'mql': 'MA_Period_24', 'py': 'MA_Period_24', 'param': 'MA_Period_24', 'type': 'int', 'default': 94, 'label': 'MA 24 Period', 'sinput': False}, {'mql': 'MA_Period_25', 'py': 'MA_Period_25', 'param': 'MA_Period_25', 'type': 'int', 'default': 90, 'label': 'MA 25 Period', 'sinput': False}, {'mql': 'MA_Period_26', 'py': 'MA_Period_26', 'param': 'MA_Period_26', 'type': 'int', 'default': 86, 'label': 'MA 26 Period', 'sinput': False}, {'mql': 'MA_Period_27', 'py': 'MA_Period_27', 'param': 'MA_Period_27', 'type': 'int', 'default': 82, 'label': 'MA 27 Period', 'sinput': False}, {'mql': 'MA_Period_28', 'py': 'MA_Period_28', 'param': 'MA_Period_28', 'type': 'int', 'default': 78, 'label': 'MA 28 Period', 'sinput': False}, {'mql': 'MA_Period_29', 'py': 'MA_Period_29', 'param': 'MA_Period_29', 'type': 'int', 'default': 74, 'label': 'MA 29 Period', 'sinput': False}, {'mql': 'MA_Period_30', 'py': 'MA_Period_30', 'param': 'MA_Period_30', 'type': 'int', 'default': 71, 'label': 'MA 30 Period', 'sinput': False}, {'mql': 'MA_Period_31', 'py': 'MA_Period_31', 'param': 'MA_Period_31', 'type': 'int', 'default': 68, 'label': 'MA 31 Period', 'sinput': False}, {'mql': 'MA_Period_32', 'py': 'MA_Period_32', 'param': 'MA_Period_32', 'type': 'int', 'default': 65, 'label': 'MA 32 Period', 'sinput': False}, {'mql': 'MA_Period_33', 'py': 'MA_Period_33', 'param': 'MA_Period_33', 'type': 'int', 'default': 62, 'label': 'MA 33 Period', 'sinput': False}, {'mql': 'MA_Period_34', 'py': 'MA_Period_34', 'param': 'MA_Period_34', 'type': 'int', 'default': 59, 'label': 'MA 34 Period', 'sinput': False}, {'mql': 'MA_Period_35', 'py': 'MA_Period_35', 'param': 'MA_Period_35', 'type': 'int', 'default': 56, 'label': 'MA 35 Period', 'sinput': False}, {'mql': 'MA_Period_36', 'py': 'MA_Period_36', 'param': 'MA_Period_36', 'type': 'int', 'default': 53, 'label': 'MA 36 Period', 'sinput': False}, {'mql': 'MA_Period_37', 'py': 'MA_Period_37', 'param': 'MA_Period_37', 'type': 'int', 'default': 50, 'label': 'MA 37 Period', 'sinput': False}, {'mql': 'MA_Period_38', 'py': 'MA_Period_38', 'param': 'MA_Period_38', 'type': 'int', 'default': 47, 'label': 'MA 38 Period', 'sinput': False}, {'mql': 'MA_Period_39', 'py': 'MA_Period_39', 'param': 'MA_Period_39', 'type': 'int', 'default': 44, 'label': 'MA 39 Period', 'sinput': False}, {'mql': 'MA_Period_40', 'py': 'MA_Period_40', 'param': 'MA_Period_40', 'type': 'int', 'default': 41, 'label': 'MA 40 Period', 'sinput': False}, {'mql': 'MA_Period_41', 'py': 'MA_Period_41', 'param': 'MA_Period_41', 'type': 'int', 'default': 39, 'label': 'MA 41 Period', 'sinput': False}, {'mql': 'MA_Period_42', 'py': 'MA_Period_42', 'param': 'MA_Period_42', 'type': 'int', 'default': 37, 'label': 'MA 42 Period', 'sinput': False}, {'mql': 'MA_Period_43', 'py': 'MA_Period_43', 'param': 'MA_Period_43', 'type': 'int', 'default': 35, 'label': 'MA 43 Period', 'sinput': False}, {'mql': 'MA_Period_44', 'py': 'MA_Period_44', 'param': 'MA_Period_44', 'type': 'int', 'default': 33, 'label': 'MA 44 Period', 'sinput': False}, {'mql': 'MA_Period_45', 'py': 'MA_Period_45', 'param': 'MA_Period_45', 'type': 'int', 'default': 31, 'label': 'MA 45 Period', 'sinput': False}, {'mql': 'MA_Period_46', 'py': 'MA_Period_46', 'param': 'MA_Period_46', 'type': 'int', 'default': 29, 'label': 'MA 46 Period', 'sinput': False}, {'mql': 'MA_Period_47', 'py': 'MA_Period_47', 'param': 'MA_Period_47', 'type': 'int', 'default': 27, 'label': 'MA 47 Period', 'sinput': False}, {'mql': 'MA_Period_48', 'py': 'MA_Period_48', 'param': 'MA_Period_48', 'type': 'int', 'default': 25, 'label': 'MA 48 Period', 'sinput': False}, {'mql': 'MA_Period_49', 'py': 'MA_Period_49', 'param': 'MA_Period_49', 'type': 'int', 'default': 23, 'label': 'MA 49 Period', 'sinput': False}, {'mql': 'MA_Period_50', 'py': 'MA_Period_50', 'param': 'MA_Period_50', 'type': 'int', 'default': 21, 'label': 'MA 50 Period', 'sinput': False}, {'mql': 'MA_Period_51', 'py': 'MA_Period_51', 'param': 'MA_Period_51', 'type': 'int', 'default': 19, 'label': 'MA 51 Period', 'sinput': False}, {'mql': 'MA_Period_52', 'py': 'MA_Period_52', 'param': 'MA_Period_52', 'type': 'int', 'default': 17, 'label': 'MA 52 Period', 'sinput': False}, {'mql': 'MA_Period_53', 'py': 'MA_Period_53', 'param': 'MA_Period_53', 'type': 'int', 'default': 15, 'label': 'MA 53 Period', 'sinput': False}, {'mql': 'MA_Period_54', 'py': 'MA_Period_54', 'param': 'MA_Period_54', 'type': 'int', 'default': 14, 'label': 'MA 54 Period', 'sinput': False}, {'mql': 'MA_Period_55', 'py': 'MA_Period_55', 'param': 'MA_Period_55', 'type': 'int', 'default': 13, 'label': 'MA 55 Period', 'sinput': False}, {'mql': 'MA_Period_56', 'py': 'MA_Period_56', 'param': 'MA_Period_56', 'type': 'int', 'default': 12, 'label': 'MA 56 Period', 'sinput': False}, {'mql': 'MA_Period_57', 'py': 'MA_Period_57', 'param': 'MA_Period_57', 'type': 'int', 'default': 11, 'label': 'MA 57 Period', 'sinput': False}, {'mql': 'MA_Period_58', 'py': 'MA_Period_58', 'param': 'MA_Period_58', 'type': 'int', 'default': 10, 'label': 'MA 58 Period', 'sinput': False}, {'mql': 'MA_Period_59', 'py': 'MA_Period_59', 'param': 'MA_Period_59', 'type': 'int', 'default': 9, 'label': 'MA 59 Period', 'sinput': False}, {'mql': 'MA_Period_60', 'py': 'MA_Period_60', 'param': 'MA_Period_60', 'type': 'int', 'default': 8, 'label': 'MA 60 Period', 'sinput': False}, {'mql': 'MA_Period_61', 'py': 'MA_Period_61', 'param': 'MA_Period_61', 'type': 'int', 'default': 7, 'label': 'MA 61 Period', 'sinput': False}, {'mql': 'MA_Period_62', 'py': 'MA_Period_62', 'param': 'MA_Period_62', 'type': 'int', 'default': 6, 'label': 'MA 62 Period', 'sinput': False}, {'mql': 'MA_Period_63', 'py': 'MA_Period_63', 'param': 'MA_Period_63', 'type': 'int', 'default': 5, 'label': 'MA 63 Period', 'sinput': False}, {'mql': 'MA_Period_64', 'py': 'MA_Period_64', 'param': 'MA_Period_64', 'type': 'int', 'default': 4, 'label': 'MA 64 Period', 'sinput': False}, {'mql': 'MA_Period_65', 'py': 'MA_Period_65', 'param': 'MA_Period_65', 'type': 'int', 'default': 3, 'label': 'MA 65 Period', 'sinput': False}, {'mql': 'MA_Period_66', 'py': 'MA_Period_66', 'param': 'MA_Period_66', 'type': 'int', 'default': 2, 'label': 'MA 66 Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Type = _input('MA_Type', MODE_EMA)  # MA Type
MA_Price = _input('MA_Price', PRICE_CLOSE)  # MA Price
MA_Period_01 = _input('MA_Period_01', 200)  # MA 01 Period
MA_Period_02 = _input('MA_Period_02', 195)  # MA 02 Period
MA_Period_03 = _input('MA_Period_03', 190)  # MA 03 Period
MA_Period_04 = _input('MA_Period_04', 185)  # MA 04 Period
MA_Period_05 = _input('MA_Period_05', 180)  # MA 05 Period
MA_Period_06 = _input('MA_Period_06', 175)  # MA 06 Period
MA_Period_07 = _input('MA_Period_07', 170)  # MA 07 Period
MA_Period_08 = _input('MA_Period_08', 165)  # MA 08 Period
MA_Period_09 = _input('MA_Period_09', 160)  # MA 09 Period
MA_Period_10 = _input('MA_Period_10', 155)  # MA 10 Period
MA_Period_11 = _input('MA_Period_11', 150)  # MA 11 Period
MA_Period_12 = _input('MA_Period_12', 145)  # MA 12 Period
MA_Period_13 = _input('MA_Period_13', 140)  # MA 13 Period
MA_Period_14 = _input('MA_Period_14', 135)  # MA 14 Period
MA_Period_15 = _input('MA_Period_15', 130)  # MA 15 Period
MA_Period_16 = _input('MA_Period_16', 125)  # MA 16 Period
MA_Period_17 = _input('MA_Period_17', 122)  # MA 17 Period
MA_Period_18 = _input('MA_Period_18', 118)  # MA 18 Period
MA_Period_19 = _input('MA_Period_19', 114)  # MA 19 Period
MA_Period_20 = _input('MA_Period_20', 110)  # MA 20 Period
MA_Period_21 = _input('MA_Period_21', 106)  # MA 21 Period
MA_Period_22 = _input('MA_Period_22', 102)  # MA 22 Period
MA_Period_23 = _input('MA_Period_23', 98)  # MA 23 Period
MA_Period_24 = _input('MA_Period_24', 94)  # MA 24 Period
MA_Period_25 = _input('MA_Period_25', 90)  # MA 25 Period
MA_Period_26 = _input('MA_Period_26', 86)  # MA 26 Period
MA_Period_27 = _input('MA_Period_27', 82)  # MA 27 Period
MA_Period_28 = _input('MA_Period_28', 78)  # MA 28 Period
MA_Period_29 = _input('MA_Period_29', 74)  # MA 29 Period
MA_Period_30 = _input('MA_Period_30', 71)  # MA 30 Period
MA_Period_31 = _input('MA_Period_31', 68)  # MA 31 Period
MA_Period_32 = _input('MA_Period_32', 65)  # MA 32 Period
MA_Period_33 = _input('MA_Period_33', 62)  # MA 33 Period
MA_Period_34 = _input('MA_Period_34', 59)  # MA 34 Period
MA_Period_35 = _input('MA_Period_35', 56)  # MA 35 Period
MA_Period_36 = _input('MA_Period_36', 53)  # MA 36 Period
MA_Period_37 = _input('MA_Period_37', 50)  # MA 37 Period
MA_Period_38 = _input('MA_Period_38', 47)  # MA 38 Period
MA_Period_39 = _input('MA_Period_39', 44)  # MA 39 Period
MA_Period_40 = _input('MA_Period_40', 41)  # MA 40 Period
MA_Period_41 = _input('MA_Period_41', 39)  # MA 41 Period
MA_Period_42 = _input('MA_Period_42', 37)  # MA 42 Period
MA_Period_43 = _input('MA_Period_43', 35)  # MA 43 Period
MA_Period_44 = _input('MA_Period_44', 33)  # MA 44 Period
MA_Period_45 = _input('MA_Period_45', 31)  # MA 45 Period
MA_Period_46 = _input('MA_Period_46', 29)  # MA 46 Period
MA_Period_47 = _input('MA_Period_47', 27)  # MA 47 Period
MA_Period_48 = _input('MA_Period_48', 25)  # MA 48 Period
MA_Period_49 = _input('MA_Period_49', 23)  # MA 49 Period
MA_Period_50 = _input('MA_Period_50', 21)  # MA 50 Period
MA_Period_51 = _input('MA_Period_51', 19)  # MA 51 Period
MA_Period_52 = _input('MA_Period_52', 17)  # MA 52 Period
MA_Period_53 = _input('MA_Period_53', 15)  # MA 53 Period
MA_Period_54 = _input('MA_Period_54', 14)  # MA 54 Period
MA_Period_55 = _input('MA_Period_55', 13)  # MA 55 Period
MA_Period_56 = _input('MA_Period_56', 12)  # MA 56 Period
MA_Period_57 = _input('MA_Period_57', 11)  # MA 57 Period
MA_Period_58 = _input('MA_Period_58', 10)  # MA 58 Period
MA_Period_59 = _input('MA_Period_59', 9)  # MA 59 Period
MA_Period_60 = _input('MA_Period_60', 8)  # MA 60 Period
MA_Period_61 = _input('MA_Period_61', 7)  # MA 61 Period
MA_Period_62 = _input('MA_Period_62', 6)  # MA 62 Period
MA_Period_63 = _input('MA_Period_63', 5)  # MA 63 Period
MA_Period_64 = _input('MA_Period_64', 4)  # MA 64 Period
MA_Period_65 = _input('MA_Period_65', 3)  # MA 65 Period
MA_Period_66 = _input('MA_Period_66', 2)  # MA 66 Period
ExtMapBuffer01 = Arr(0, 0.0)
ExtMapBuffer02 = Arr(0, 0.0)
ExtMapBuffer03 = Arr(0, 0.0)
ExtMapBuffer04 = Arr(0, 0.0)
ExtMapBuffer05 = Arr(0, 0.0)
ExtMapBuffer06 = Arr(0, 0.0)
ExtMapBuffer07 = Arr(0, 0.0)
ExtMapBuffer08 = Arr(0, 0.0)
ExtMapBuffer09 = Arr(0, 0.0)
ExtMapBuffer10 = Arr(0, 0.0)
ExtMapBuffer11 = Arr(0, 0.0)
ExtMapBuffer12 = Arr(0, 0.0)
ExtMapBuffer13 = Arr(0, 0.0)
ExtMapBuffer14 = Arr(0, 0.0)
ExtMapBuffer15 = Arr(0, 0.0)
ExtMapBuffer16 = Arr(0, 0.0)
ExtMapBuffer17 = Arr(0, 0.0)
ExtMapBuffer18 = Arr(0, 0.0)
ExtMapBuffer19 = Arr(0, 0.0)
ExtMapBuffer20 = Arr(0, 0.0)
ExtMapBuffer21 = Arr(0, 0.0)
ExtMapBuffer22 = Arr(0, 0.0)
ExtMapBuffer23 = Arr(0, 0.0)
ExtMapBuffer24 = Arr(0, 0.0)
ExtMapBuffer25 = Arr(0, 0.0)
ExtMapBuffer26 = Arr(0, 0.0)
ExtMapBuffer27 = Arr(0, 0.0)
ExtMapBuffer28 = Arr(0, 0.0)
ExtMapBuffer29 = Arr(0, 0.0)
ExtMapBuffer30 = Arr(0, 0.0)
ExtMapBuffer31 = Arr(0, 0.0)
ExtMapBuffer32 = Arr(0, 0.0)
ExtMapBuffer33 = Arr(0, 0.0)
ExtMapBuffer34 = Arr(0, 0.0)
ExtMapBuffer35 = Arr(0, 0.0)
ExtMapBuffer36 = Arr(0, 0.0)
ExtMapBuffer37 = Arr(0, 0.0)
ExtMapBuffer38 = Arr(0, 0.0)
ExtMapBuffer39 = Arr(0, 0.0)
ExtMapBuffer40 = Arr(0, 0.0)
ExtMapBuffer41 = Arr(0, 0.0)
ExtMapBuffer42 = Arr(0, 0.0)
ExtMapBuffer43 = Arr(0, 0.0)
ExtMapBuffer44 = Arr(0, 0.0)
ExtMapBuffer45 = Arr(0, 0.0)
ExtMapBuffer46 = Arr(0, 0.0)
ExtMapBuffer47 = Arr(0, 0.0)
ExtMapBuffer48 = Arr(0, 0.0)
ExtMapBuffer49 = Arr(0, 0.0)
ExtMapBuffer50 = Arr(0, 0.0)
ExtMapBuffer51 = Arr(0, 0.0)
ExtMapBuffer52 = Arr(0, 0.0)
ExtMapBuffer53 = Arr(0, 0.0)
ExtMapBuffer54 = Arr(0, 0.0)
ExtMapBuffer55 = Arr(0, 0.0)
ExtMapBuffer56 = Arr(0, 0.0)
ExtMapBuffer57 = Arr(0, 0.0)
ExtMapBuffer58 = Arr(0, 0.0)
ExtMapBuffer59 = Arr(0, 0.0)
ExtMapBuffer60 = Arr(0, 0.0)
ExtMapBuffer61 = Arr(0, 0.0)
ExtMapBuffer62 = Arr(0, 0.0)
ExtMapBuffer63 = Arr(0, 0.0)
ExtMapBuffer64 = Arr(0, 0.0)
ExtMapBuffer65 = Arr(0, 0.0)
ExtMapBuffer66 = Arr(0, 0.0)
MA_Handle_01 = 0
MA_Handle_02 = 0
MA_Handle_03 = 0
MA_Handle_04 = 0
MA_Handle_05 = 0
MA_Handle_06 = 0
MA_Handle_07 = 0
MA_Handle_08 = 0
MA_Handle_09 = 0
MA_Handle_10 = 0
MA_Handle_11 = 0
MA_Handle_12 = 0
MA_Handle_13 = 0
MA_Handle_14 = 0
MA_Handle_15 = 0
MA_Handle_16 = 0
MA_Handle_17 = 0
MA_Handle_18 = 0
MA_Handle_19 = 0
MA_Handle_20 = 0
MA_Handle_21 = 0
MA_Handle_22 = 0
MA_Handle_23 = 0
MA_Handle_24 = 0
MA_Handle_25 = 0
MA_Handle_26 = 0
MA_Handle_27 = 0
MA_Handle_28 = 0
MA_Handle_29 = 0
MA_Handle_30 = 0
MA_Handle_31 = 0
MA_Handle_32 = 0
MA_Handle_33 = 0
MA_Handle_34 = 0
MA_Handle_35 = 0
MA_Handle_36 = 0
MA_Handle_37 = 0
MA_Handle_38 = 0
MA_Handle_39 = 0
MA_Handle_40 = 0
MA_Handle_41 = 0
MA_Handle_42 = 0
MA_Handle_43 = 0
MA_Handle_44 = 0
MA_Handle_45 = 0
MA_Handle_46 = 0
MA_Handle_47 = 0
MA_Handle_48 = 0
MA_Handle_49 = 0
MA_Handle_50 = 0
MA_Handle_51 = 0
MA_Handle_52 = 0
MA_Handle_53 = 0
MA_Handle_54 = 0
MA_Handle_55 = 0
MA_Handle_56 = 0
MA_Handle_57 = 0
MA_Handle_58 = 0
MA_Handle_59 = 0
MA_Handle_60 = 0
MA_Handle_61 = 0
MA_Handle_62 = 0
MA_Handle_63 = 0
MA_Handle_64 = 0
MA_Handle_65 = 0
MA_Handle_66 = 0
MA_Buffer_01 = Arr(0, 0.0)
MA_Buffer_02 = Arr(0, 0.0)
MA_Buffer_03 = Arr(0, 0.0)
MA_Buffer_04 = Arr(0, 0.0)
MA_Buffer_05 = Arr(0, 0.0)
MA_Buffer_06 = Arr(0, 0.0)
MA_Buffer_07 = Arr(0, 0.0)
MA_Buffer_08 = Arr(0, 0.0)
MA_Buffer_09 = Arr(0, 0.0)
MA_Buffer_10 = Arr(0, 0.0)
MA_Buffer_11 = Arr(0, 0.0)
MA_Buffer_12 = Arr(0, 0.0)
MA_Buffer_13 = Arr(0, 0.0)
MA_Buffer_14 = Arr(0, 0.0)
MA_Buffer_15 = Arr(0, 0.0)
MA_Buffer_16 = Arr(0, 0.0)
MA_Buffer_17 = Arr(0, 0.0)
MA_Buffer_18 = Arr(0, 0.0)
MA_Buffer_19 = Arr(0, 0.0)
MA_Buffer_20 = Arr(0, 0.0)
MA_Buffer_21 = Arr(0, 0.0)
MA_Buffer_22 = Arr(0, 0.0)
MA_Buffer_23 = Arr(0, 0.0)
MA_Buffer_24 = Arr(0, 0.0)
MA_Buffer_25 = Arr(0, 0.0)
MA_Buffer_26 = Arr(0, 0.0)
MA_Buffer_27 = Arr(0, 0.0)
MA_Buffer_28 = Arr(0, 0.0)
MA_Buffer_29 = Arr(0, 0.0)
MA_Buffer_30 = Arr(0, 0.0)
MA_Buffer_31 = Arr(0, 0.0)
MA_Buffer_32 = Arr(0, 0.0)
MA_Buffer_33 = Arr(0, 0.0)
MA_Buffer_34 = Arr(0, 0.0)
MA_Buffer_35 = Arr(0, 0.0)
MA_Buffer_36 = Arr(0, 0.0)
MA_Buffer_37 = Arr(0, 0.0)
MA_Buffer_38 = Arr(0, 0.0)
MA_Buffer_39 = Arr(0, 0.0)
MA_Buffer_40 = Arr(0, 0.0)
MA_Buffer_41 = Arr(0, 0.0)
MA_Buffer_42 = Arr(0, 0.0)
MA_Buffer_43 = Arr(0, 0.0)
MA_Buffer_44 = Arr(0, 0.0)
MA_Buffer_45 = Arr(0, 0.0)
MA_Buffer_46 = Arr(0, 0.0)
MA_Buffer_47 = Arr(0, 0.0)
MA_Buffer_48 = Arr(0, 0.0)
MA_Buffer_49 = Arr(0, 0.0)
MA_Buffer_50 = Arr(0, 0.0)
MA_Buffer_51 = Arr(0, 0.0)
MA_Buffer_52 = Arr(0, 0.0)
MA_Buffer_53 = Arr(0, 0.0)
MA_Buffer_54 = Arr(0, 0.0)
MA_Buffer_55 = Arr(0, 0.0)
MA_Buffer_56 = Arr(0, 0.0)
MA_Buffer_57 = Arr(0, 0.0)
MA_Buffer_58 = Arr(0, 0.0)
MA_Buffer_59 = Arr(0, 0.0)
MA_Buffer_60 = Arr(0, 0.0)
MA_Buffer_61 = Arr(0, 0.0)
MA_Buffer_62 = Arr(0, 0.0)
MA_Buffer_63 = Arr(0, 0.0)
MA_Buffer_64 = Arr(0, 0.0)
MA_Buffer_65 = Arr(0, 0.0)
MA_Buffer_66 = Arr(0, 0.0)

def OnInit():
    global MA_Handle_01, MA_Handle_02, MA_Handle_03, MA_Handle_04, MA_Handle_05, MA_Handle_06, MA_Handle_07, MA_Handle_08, MA_Handle_09, MA_Handle_10, MA_Handle_11, MA_Handle_12, MA_Handle_13, MA_Handle_14, MA_Handle_15, MA_Handle_16, MA_Handle_17, MA_Handle_18, MA_Handle_19, MA_Handle_20, MA_Handle_21, MA_Handle_22, MA_Handle_23, MA_Handle_24, MA_Handle_25, MA_Handle_26, MA_Handle_27, MA_Handle_28, MA_Handle_29, MA_Handle_30, MA_Handle_31, MA_Handle_32, MA_Handle_33, MA_Handle_34, MA_Handle_35, MA_Handle_36, MA_Handle_37, MA_Handle_38, MA_Handle_39, MA_Handle_40, MA_Handle_41, MA_Handle_42, MA_Handle_43, MA_Handle_44, MA_Handle_45, MA_Handle_46, MA_Handle_47, MA_Handle_48, MA_Handle_49, MA_Handle_50, MA_Handle_51, MA_Handle_52, MA_Handle_53, MA_Handle_54, MA_Handle_55, MA_Handle_56, MA_Handle_57, MA_Handle_58, MA_Handle_59, MA_Handle_60, MA_Handle_61, MA_Handle_62, MA_Handle_63, MA_Handle_64, MA_Handle_65, MA_Handle_66
    SetIndexBuffer(0, ExtMapBuffer01, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMapBuffer02, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMapBuffer03, INDICATOR_DATA)
    SetIndexBuffer(3, ExtMapBuffer04, INDICATOR_DATA)
    SetIndexBuffer(4, ExtMapBuffer05, INDICATOR_DATA)
    SetIndexBuffer(5, ExtMapBuffer06, INDICATOR_DATA)
    SetIndexBuffer(6, ExtMapBuffer07, INDICATOR_DATA)
    SetIndexBuffer(7, ExtMapBuffer08, INDICATOR_DATA)
    SetIndexBuffer(8, ExtMapBuffer09, INDICATOR_DATA)
    SetIndexBuffer(9, ExtMapBuffer10, INDICATOR_DATA)
    SetIndexBuffer(10, ExtMapBuffer11, INDICATOR_DATA)
    SetIndexBuffer(11, ExtMapBuffer12, INDICATOR_DATA)
    SetIndexBuffer(12, ExtMapBuffer13, INDICATOR_DATA)
    SetIndexBuffer(13, ExtMapBuffer14, INDICATOR_DATA)
    SetIndexBuffer(14, ExtMapBuffer15, INDICATOR_DATA)
    SetIndexBuffer(15, ExtMapBuffer16, INDICATOR_DATA)
    SetIndexBuffer(16, ExtMapBuffer17, INDICATOR_DATA)
    SetIndexBuffer(17, ExtMapBuffer18, INDICATOR_DATA)
    SetIndexBuffer(18, ExtMapBuffer19, INDICATOR_DATA)
    SetIndexBuffer(19, ExtMapBuffer20, INDICATOR_DATA)
    SetIndexBuffer(20, ExtMapBuffer21, INDICATOR_DATA)
    SetIndexBuffer(21, ExtMapBuffer22, INDICATOR_DATA)
    SetIndexBuffer(22, ExtMapBuffer23, INDICATOR_DATA)
    SetIndexBuffer(23, ExtMapBuffer24, INDICATOR_DATA)
    SetIndexBuffer(24, ExtMapBuffer25, INDICATOR_DATA)
    SetIndexBuffer(25, ExtMapBuffer26, INDICATOR_DATA)
    SetIndexBuffer(26, ExtMapBuffer27, INDICATOR_DATA)
    SetIndexBuffer(27, ExtMapBuffer28, INDICATOR_DATA)
    SetIndexBuffer(28, ExtMapBuffer29, INDICATOR_DATA)
    SetIndexBuffer(29, ExtMapBuffer30, INDICATOR_DATA)
    SetIndexBuffer(30, ExtMapBuffer31, INDICATOR_DATA)
    SetIndexBuffer(31, ExtMapBuffer32, INDICATOR_DATA)
    SetIndexBuffer(32, ExtMapBuffer33, INDICATOR_DATA)
    SetIndexBuffer(33, ExtMapBuffer34, INDICATOR_DATA)
    SetIndexBuffer(34, ExtMapBuffer35, INDICATOR_DATA)
    SetIndexBuffer(35, ExtMapBuffer36, INDICATOR_DATA)
    SetIndexBuffer(36, ExtMapBuffer37, INDICATOR_DATA)
    SetIndexBuffer(37, ExtMapBuffer38, INDICATOR_DATA)
    SetIndexBuffer(38, ExtMapBuffer39, INDICATOR_DATA)
    SetIndexBuffer(39, ExtMapBuffer40, INDICATOR_DATA)
    SetIndexBuffer(40, ExtMapBuffer41, INDICATOR_DATA)
    SetIndexBuffer(41, ExtMapBuffer42, INDICATOR_DATA)
    SetIndexBuffer(42, ExtMapBuffer43, INDICATOR_DATA)
    SetIndexBuffer(43, ExtMapBuffer44, INDICATOR_DATA)
    SetIndexBuffer(44, ExtMapBuffer45, INDICATOR_DATA)
    SetIndexBuffer(45, ExtMapBuffer46, INDICATOR_DATA)
    SetIndexBuffer(46, ExtMapBuffer47, INDICATOR_DATA)
    SetIndexBuffer(47, ExtMapBuffer48, INDICATOR_DATA)
    SetIndexBuffer(48, ExtMapBuffer49, INDICATOR_DATA)
    SetIndexBuffer(49, ExtMapBuffer50, INDICATOR_DATA)
    SetIndexBuffer(50, ExtMapBuffer51, INDICATOR_DATA)
    SetIndexBuffer(51, ExtMapBuffer52, INDICATOR_DATA)
    SetIndexBuffer(52, ExtMapBuffer53, INDICATOR_DATA)
    SetIndexBuffer(53, ExtMapBuffer54, INDICATOR_DATA)
    SetIndexBuffer(54, ExtMapBuffer55, INDICATOR_DATA)
    SetIndexBuffer(55, ExtMapBuffer56, INDICATOR_DATA)
    SetIndexBuffer(56, ExtMapBuffer57, INDICATOR_DATA)
    SetIndexBuffer(57, ExtMapBuffer58, INDICATOR_DATA)
    SetIndexBuffer(58, ExtMapBuffer59, INDICATOR_DATA)
    SetIndexBuffer(59, ExtMapBuffer60, INDICATOR_DATA)
    SetIndexBuffer(60, ExtMapBuffer61, INDICATOR_DATA)
    SetIndexBuffer(61, ExtMapBuffer62, INDICATOR_DATA)
    SetIndexBuffer(62, ExtMapBuffer63, INDICATOR_DATA)
    SetIndexBuffer(63, ExtMapBuffer64, INDICATOR_DATA)
    SetIndexBuffer(64, ExtMapBuffer65, INDICATOR_DATA)
    SetIndexBuffer(65, ExtMapBuffer66, INDICATOR_DATA)
    MA_Handle_01 = iMA(Symbol(), Period(), MA_Period_01, 0, MA_Type, MA_Price)
    MA_Handle_02 = iMA(Symbol(), Period(), MA_Period_02, 0, MA_Type, MA_Price)
    MA_Handle_03 = iMA(Symbol(), Period(), MA_Period_03, 0, MA_Type, MA_Price)
    MA_Handle_04 = iMA(Symbol(), Period(), MA_Period_04, 0, MA_Type, MA_Price)
    MA_Handle_05 = iMA(Symbol(), Period(), MA_Period_05, 0, MA_Type, MA_Price)
    MA_Handle_06 = iMA(Symbol(), Period(), MA_Period_06, 0, MA_Type, MA_Price)
    MA_Handle_07 = iMA(Symbol(), Period(), MA_Period_07, 0, MA_Type, MA_Price)
    MA_Handle_08 = iMA(Symbol(), Period(), MA_Period_08, 0, MA_Type, MA_Price)
    MA_Handle_09 = iMA(Symbol(), Period(), MA_Period_09, 0, MA_Type, MA_Price)
    MA_Handle_10 = iMA(Symbol(), Period(), MA_Period_10, 0, MA_Type, MA_Price)
    MA_Handle_11 = iMA(Symbol(), Period(), MA_Period_11, 0, MA_Type, MA_Price)
    MA_Handle_12 = iMA(Symbol(), Period(), MA_Period_12, 0, MA_Type, MA_Price)
    MA_Handle_13 = iMA(Symbol(), Period(), MA_Period_13, 0, MA_Type, MA_Price)
    MA_Handle_14 = iMA(Symbol(), Period(), MA_Period_14, 0, MA_Type, MA_Price)
    MA_Handle_15 = iMA(Symbol(), Period(), MA_Period_15, 0, MA_Type, MA_Price)
    MA_Handle_16 = iMA(Symbol(), Period(), MA_Period_16, 0, MA_Type, MA_Price)
    MA_Handle_17 = iMA(Symbol(), Period(), MA_Period_17, 0, MA_Type, MA_Price)
    MA_Handle_18 = iMA(Symbol(), Period(), MA_Period_18, 0, MA_Type, MA_Price)
    MA_Handle_19 = iMA(Symbol(), Period(), MA_Period_19, 0, MA_Type, MA_Price)
    MA_Handle_20 = iMA(Symbol(), Period(), MA_Period_20, 0, MA_Type, MA_Price)
    MA_Handle_21 = iMA(Symbol(), Period(), MA_Period_21, 0, MA_Type, MA_Price)
    MA_Handle_22 = iMA(Symbol(), Period(), MA_Period_22, 0, MA_Type, MA_Price)
    MA_Handle_23 = iMA(Symbol(), Period(), MA_Period_23, 0, MA_Type, MA_Price)
    MA_Handle_24 = iMA(Symbol(), Period(), MA_Period_24, 0, MA_Type, MA_Price)
    MA_Handle_25 = iMA(Symbol(), Period(), MA_Period_25, 0, MA_Type, MA_Price)
    MA_Handle_26 = iMA(Symbol(), Period(), MA_Period_26, 0, MA_Type, MA_Price)
    MA_Handle_27 = iMA(Symbol(), Period(), MA_Period_27, 0, MA_Type, MA_Price)
    MA_Handle_28 = iMA(Symbol(), Period(), MA_Period_28, 0, MA_Type, MA_Price)
    MA_Handle_29 = iMA(Symbol(), Period(), MA_Period_29, 0, MA_Type, MA_Price)
    MA_Handle_30 = iMA(Symbol(), Period(), MA_Period_30, 0, MA_Type, MA_Price)
    MA_Handle_31 = iMA(Symbol(), Period(), MA_Period_31, 0, MA_Type, MA_Price)
    MA_Handle_32 = iMA(Symbol(), Period(), MA_Period_32, 0, MA_Type, MA_Price)
    MA_Handle_33 = iMA(Symbol(), Period(), MA_Period_33, 0, MA_Type, MA_Price)
    MA_Handle_34 = iMA(Symbol(), Period(), MA_Period_34, 0, MA_Type, MA_Price)
    MA_Handle_35 = iMA(Symbol(), Period(), MA_Period_35, 0, MA_Type, MA_Price)
    MA_Handle_36 = iMA(Symbol(), Period(), MA_Period_36, 0, MA_Type, MA_Price)
    MA_Handle_37 = iMA(Symbol(), Period(), MA_Period_37, 0, MA_Type, MA_Price)
    MA_Handle_38 = iMA(Symbol(), Period(), MA_Period_38, 0, MA_Type, MA_Price)
    MA_Handle_39 = iMA(Symbol(), Period(), MA_Period_39, 0, MA_Type, MA_Price)
    MA_Handle_40 = iMA(Symbol(), Period(), MA_Period_40, 0, MA_Type, MA_Price)
    MA_Handle_41 = iMA(Symbol(), Period(), MA_Period_41, 0, MA_Type, MA_Price)
    MA_Handle_42 = iMA(Symbol(), Period(), MA_Period_42, 0, MA_Type, MA_Price)
    MA_Handle_43 = iMA(Symbol(), Period(), MA_Period_43, 0, MA_Type, MA_Price)
    MA_Handle_44 = iMA(Symbol(), Period(), MA_Period_44, 0, MA_Type, MA_Price)
    MA_Handle_45 = iMA(Symbol(), Period(), MA_Period_45, 0, MA_Type, MA_Price)
    MA_Handle_46 = iMA(Symbol(), Period(), MA_Period_46, 0, MA_Type, MA_Price)
    MA_Handle_47 = iMA(Symbol(), Period(), MA_Period_47, 0, MA_Type, MA_Price)
    MA_Handle_48 = iMA(Symbol(), Period(), MA_Period_48, 0, MA_Type, MA_Price)
    MA_Handle_49 = iMA(Symbol(), Period(), MA_Period_49, 0, MA_Type, MA_Price)
    MA_Handle_50 = iMA(Symbol(), Period(), MA_Period_50, 0, MA_Type, MA_Price)
    MA_Handle_51 = iMA(Symbol(), Period(), MA_Period_51, 0, MA_Type, MA_Price)
    MA_Handle_52 = iMA(Symbol(), Period(), MA_Period_52, 0, MA_Type, MA_Price)
    MA_Handle_53 = iMA(Symbol(), Period(), MA_Period_53, 0, MA_Type, MA_Price)
    MA_Handle_54 = iMA(Symbol(), Period(), MA_Period_54, 0, MA_Type, MA_Price)
    MA_Handle_55 = iMA(Symbol(), Period(), MA_Period_55, 0, MA_Type, MA_Price)
    MA_Handle_56 = iMA(Symbol(), Period(), MA_Period_56, 0, MA_Type, MA_Price)
    MA_Handle_57 = iMA(Symbol(), Period(), MA_Period_57, 0, MA_Type, MA_Price)
    MA_Handle_58 = iMA(Symbol(), Period(), MA_Period_58, 0, MA_Type, MA_Price)
    MA_Handle_59 = iMA(Symbol(), Period(), MA_Period_59, 0, MA_Type, MA_Price)
    MA_Handle_60 = iMA(Symbol(), Period(), MA_Period_60, 0, MA_Type, MA_Price)
    MA_Handle_61 = iMA(Symbol(), Period(), MA_Period_61, 0, MA_Type, MA_Price)
    MA_Handle_62 = iMA(Symbol(), Period(), MA_Period_62, 0, MA_Type, MA_Price)
    MA_Handle_63 = iMA(Symbol(), Period(), MA_Period_63, 0, MA_Type, MA_Price)
    MA_Handle_64 = iMA(Symbol(), Period(), MA_Period_64, 0, MA_Type, MA_Price)
    MA_Handle_65 = iMA(Symbol(), Period(), MA_Period_65, 0, MA_Type, MA_Price)
    MA_Handle_66 = iMA(Symbol(), Period(), MA_Period_66, 0, MA_Type, MA_Price)
    ArraySetAsSeries(ExtMapBuffer01, True)
    ArraySetAsSeries(ExtMapBuffer02, True)
    ArraySetAsSeries(ExtMapBuffer03, True)
    ArraySetAsSeries(ExtMapBuffer04, True)
    ArraySetAsSeries(ExtMapBuffer05, True)
    ArraySetAsSeries(ExtMapBuffer06, True)
    ArraySetAsSeries(ExtMapBuffer07, True)
    ArraySetAsSeries(ExtMapBuffer08, True)
    ArraySetAsSeries(ExtMapBuffer09, True)
    ArraySetAsSeries(ExtMapBuffer10, True)
    ArraySetAsSeries(ExtMapBuffer11, True)
    ArraySetAsSeries(ExtMapBuffer12, True)
    ArraySetAsSeries(ExtMapBuffer13, True)
    ArraySetAsSeries(ExtMapBuffer14, True)
    ArraySetAsSeries(ExtMapBuffer15, True)
    ArraySetAsSeries(ExtMapBuffer16, True)
    ArraySetAsSeries(ExtMapBuffer17, True)
    ArraySetAsSeries(ExtMapBuffer18, True)
    ArraySetAsSeries(ExtMapBuffer19, True)
    ArraySetAsSeries(ExtMapBuffer20, True)
    ArraySetAsSeries(ExtMapBuffer21, True)
    ArraySetAsSeries(ExtMapBuffer22, True)
    ArraySetAsSeries(ExtMapBuffer23, True)
    ArraySetAsSeries(ExtMapBuffer24, True)
    ArraySetAsSeries(ExtMapBuffer25, True)
    ArraySetAsSeries(ExtMapBuffer26, True)
    ArraySetAsSeries(ExtMapBuffer27, True)
    ArraySetAsSeries(ExtMapBuffer28, True)
    ArraySetAsSeries(ExtMapBuffer29, True)
    ArraySetAsSeries(ExtMapBuffer30, True)
    ArraySetAsSeries(ExtMapBuffer31, True)
    ArraySetAsSeries(ExtMapBuffer32, True)
    ArraySetAsSeries(ExtMapBuffer33, True)
    ArraySetAsSeries(ExtMapBuffer34, True)
    ArraySetAsSeries(ExtMapBuffer35, True)
    ArraySetAsSeries(ExtMapBuffer36, True)
    ArraySetAsSeries(ExtMapBuffer37, True)
    ArraySetAsSeries(ExtMapBuffer38, True)
    ArraySetAsSeries(ExtMapBuffer39, True)
    ArraySetAsSeries(ExtMapBuffer40, True)
    ArraySetAsSeries(ExtMapBuffer41, True)
    ArraySetAsSeries(ExtMapBuffer42, True)
    ArraySetAsSeries(ExtMapBuffer43, True)
    ArraySetAsSeries(ExtMapBuffer44, True)
    ArraySetAsSeries(ExtMapBuffer45, True)
    ArraySetAsSeries(ExtMapBuffer46, True)
    ArraySetAsSeries(ExtMapBuffer47, True)
    ArraySetAsSeries(ExtMapBuffer48, True)
    ArraySetAsSeries(ExtMapBuffer49, True)
    ArraySetAsSeries(ExtMapBuffer50, True)
    ArraySetAsSeries(ExtMapBuffer51, True)
    ArraySetAsSeries(ExtMapBuffer52, True)
    ArraySetAsSeries(ExtMapBuffer53, True)
    ArraySetAsSeries(ExtMapBuffer54, True)
    ArraySetAsSeries(ExtMapBuffer55, True)
    ArraySetAsSeries(ExtMapBuffer56, True)
    ArraySetAsSeries(ExtMapBuffer57, True)
    ArraySetAsSeries(ExtMapBuffer58, True)
    ArraySetAsSeries(ExtMapBuffer59, True)
    ArraySetAsSeries(ExtMapBuffer60, True)
    ArraySetAsSeries(ExtMapBuffer61, True)
    ArraySetAsSeries(ExtMapBuffer62, True)
    ArraySetAsSeries(ExtMapBuffer63, True)
    ArraySetAsSeries(ExtMapBuffer64, True)
    ArraySetAsSeries(ExtMapBuffer65, True)
    ArraySetAsSeries(ExtMapBuffer66, True)
    ArraySetAsSeries(MA_Buffer_01, True)
    ArraySetAsSeries(MA_Buffer_02, True)
    ArraySetAsSeries(MA_Buffer_03, True)
    ArraySetAsSeries(MA_Buffer_04, True)
    ArraySetAsSeries(MA_Buffer_05, True)
    ArraySetAsSeries(MA_Buffer_06, True)
    ArraySetAsSeries(MA_Buffer_07, True)
    ArraySetAsSeries(MA_Buffer_08, True)
    ArraySetAsSeries(MA_Buffer_09, True)
    ArraySetAsSeries(MA_Buffer_10, True)
    ArraySetAsSeries(MA_Buffer_11, True)
    ArraySetAsSeries(MA_Buffer_12, True)
    ArraySetAsSeries(MA_Buffer_13, True)
    ArraySetAsSeries(MA_Buffer_14, True)
    ArraySetAsSeries(MA_Buffer_15, True)
    ArraySetAsSeries(MA_Buffer_16, True)
    ArraySetAsSeries(MA_Buffer_17, True)
    ArraySetAsSeries(MA_Buffer_18, True)
    ArraySetAsSeries(MA_Buffer_19, True)
    ArraySetAsSeries(MA_Buffer_20, True)
    ArraySetAsSeries(MA_Buffer_21, True)
    ArraySetAsSeries(MA_Buffer_22, True)
    ArraySetAsSeries(MA_Buffer_23, True)
    ArraySetAsSeries(MA_Buffer_24, True)
    ArraySetAsSeries(MA_Buffer_25, True)
    ArraySetAsSeries(MA_Buffer_26, True)
    ArraySetAsSeries(MA_Buffer_27, True)
    ArraySetAsSeries(MA_Buffer_28, True)
    ArraySetAsSeries(MA_Buffer_29, True)
    ArraySetAsSeries(MA_Buffer_30, True)
    ArraySetAsSeries(MA_Buffer_31, True)
    ArraySetAsSeries(MA_Buffer_32, True)
    ArraySetAsSeries(MA_Buffer_33, True)
    ArraySetAsSeries(MA_Buffer_34, True)
    ArraySetAsSeries(MA_Buffer_35, True)
    ArraySetAsSeries(MA_Buffer_36, True)
    ArraySetAsSeries(MA_Buffer_37, True)
    ArraySetAsSeries(MA_Buffer_38, True)
    ArraySetAsSeries(MA_Buffer_39, True)
    ArraySetAsSeries(MA_Buffer_40, True)
    ArraySetAsSeries(MA_Buffer_41, True)
    ArraySetAsSeries(MA_Buffer_42, True)
    ArraySetAsSeries(MA_Buffer_43, True)
    ArraySetAsSeries(MA_Buffer_44, True)
    ArraySetAsSeries(MA_Buffer_45, True)
    ArraySetAsSeries(MA_Buffer_46, True)
    ArraySetAsSeries(MA_Buffer_47, True)
    ArraySetAsSeries(MA_Buffer_48, True)
    ArraySetAsSeries(MA_Buffer_49, True)
    ArraySetAsSeries(MA_Buffer_50, True)
    ArraySetAsSeries(MA_Buffer_51, True)
    ArraySetAsSeries(MA_Buffer_52, True)
    ArraySetAsSeries(MA_Buffer_53, True)
    ArraySetAsSeries(MA_Buffer_54, True)
    ArraySetAsSeries(MA_Buffer_55, True)
    ArraySetAsSeries(MA_Buffer_56, True)
    ArraySetAsSeries(MA_Buffer_57, True)
    ArraySetAsSeries(MA_Buffer_58, True)
    ArraySetAsSeries(MA_Buffer_59, True)
    ArraySetAsSeries(MA_Buffer_60, True)
    ArraySetAsSeries(MA_Buffer_61, True)
    ArraySetAsSeries(MA_Buffer_62, True)
    ArraySetAsSeries(MA_Buffer_63, True)
    ArraySetAsSeries(MA_Buffer_64, True)
    ArraySetAsSeries(MA_Buffer_65, True)
    ArraySetAsSeries(MA_Buffer_66, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    counted_bars = prev_calculated
    if counted_bars > 0:
        counted_bars -= 1
    limit = rates_total - counted_bars
    if (rates_total - limit) < MA_Period_01:
        limit = rates_total - MA_Period_01
    if CopyBuffer(MA_Handle_01, 0, 0, limit, MA_Buffer_01) != limit:
        return 0
    if CopyBuffer(MA_Handle_02, 0, 0, limit, MA_Buffer_02) != limit:
        return 0
    if CopyBuffer(MA_Handle_03, 0, 0, limit, MA_Buffer_03) != limit:
        return 0
    if CopyBuffer(MA_Handle_04, 0, 0, limit, MA_Buffer_04) != limit:
        return 0
    if CopyBuffer(MA_Handle_05, 0, 0, limit, MA_Buffer_05) != limit:
        return 0
    if CopyBuffer(MA_Handle_06, 0, 0, limit, MA_Buffer_06) != limit:
        return 0
    if CopyBuffer(MA_Handle_07, 0, 0, limit, MA_Buffer_07) != limit:
        return 0
    if CopyBuffer(MA_Handle_08, 0, 0, limit, MA_Buffer_08) != limit:
        return 0
    if CopyBuffer(MA_Handle_09, 0, 0, limit, MA_Buffer_09) != limit:
        return 0
    if CopyBuffer(MA_Handle_10, 0, 0, limit, MA_Buffer_10) != limit:
        return 0
    if CopyBuffer(MA_Handle_11, 0, 0, limit, MA_Buffer_11) != limit:
        return 0
    if CopyBuffer(MA_Handle_12, 0, 0, limit, MA_Buffer_12) != limit:
        return 0
    if CopyBuffer(MA_Handle_13, 0, 0, limit, MA_Buffer_13) != limit:
        return 0
    if CopyBuffer(MA_Handle_14, 0, 0, limit, MA_Buffer_14) != limit:
        return 0
    if CopyBuffer(MA_Handle_15, 0, 0, limit, MA_Buffer_15) != limit:
        return 0
    if CopyBuffer(MA_Handle_16, 0, 0, limit, MA_Buffer_16) != limit:
        return 0
    if CopyBuffer(MA_Handle_17, 0, 0, limit, MA_Buffer_17) != limit:
        return 0
    if CopyBuffer(MA_Handle_18, 0, 0, limit, MA_Buffer_18) != limit:
        return 0
    if CopyBuffer(MA_Handle_19, 0, 0, limit, MA_Buffer_19) != limit:
        return 0
    if CopyBuffer(MA_Handle_20, 0, 0, limit, MA_Buffer_20) != limit:
        return 0
    if CopyBuffer(MA_Handle_21, 0, 0, limit, MA_Buffer_21) != limit:
        return 0
    if CopyBuffer(MA_Handle_22, 0, 0, limit, MA_Buffer_22) != limit:
        return 0
    if CopyBuffer(MA_Handle_23, 0, 0, limit, MA_Buffer_23) != limit:
        return 0
    if CopyBuffer(MA_Handle_24, 0, 0, limit, MA_Buffer_24) != limit:
        return 0
    if CopyBuffer(MA_Handle_25, 0, 0, limit, MA_Buffer_25) != limit:
        return 0
    if CopyBuffer(MA_Handle_26, 0, 0, limit, MA_Buffer_26) != limit:
        return 0
    if CopyBuffer(MA_Handle_27, 0, 0, limit, MA_Buffer_27) != limit:
        return 0
    if CopyBuffer(MA_Handle_28, 0, 0, limit, MA_Buffer_28) != limit:
        return 0
    if CopyBuffer(MA_Handle_29, 0, 0, limit, MA_Buffer_29) != limit:
        return 0
    if CopyBuffer(MA_Handle_30, 0, 0, limit, MA_Buffer_30) != limit:
        return 0
    if CopyBuffer(MA_Handle_31, 0, 0, limit, MA_Buffer_31) != limit:
        return 0
    if CopyBuffer(MA_Handle_32, 0, 0, limit, MA_Buffer_32) != limit:
        return 0
    if CopyBuffer(MA_Handle_33, 0, 0, limit, MA_Buffer_33) != limit:
        return 0
    if CopyBuffer(MA_Handle_34, 0, 0, limit, MA_Buffer_34) != limit:
        return 0
    if CopyBuffer(MA_Handle_35, 0, 0, limit, MA_Buffer_35) != limit:
        return 0
    if CopyBuffer(MA_Handle_36, 0, 0, limit, MA_Buffer_36) != limit:
        return 0
    if CopyBuffer(MA_Handle_37, 0, 0, limit, MA_Buffer_37) != limit:
        return 0
    if CopyBuffer(MA_Handle_38, 0, 0, limit, MA_Buffer_38) != limit:
        return 0
    if CopyBuffer(MA_Handle_39, 0, 0, limit, MA_Buffer_39) != limit:
        return 0
    if CopyBuffer(MA_Handle_40, 0, 0, limit, MA_Buffer_40) != limit:
        return 0
    if CopyBuffer(MA_Handle_41, 0, 0, limit, MA_Buffer_41) != limit:
        return 0
    if CopyBuffer(MA_Handle_42, 0, 0, limit, MA_Buffer_42) != limit:
        return 0
    if CopyBuffer(MA_Handle_43, 0, 0, limit, MA_Buffer_43) != limit:
        return 0
    if CopyBuffer(MA_Handle_44, 0, 0, limit, MA_Buffer_44) != limit:
        return 0
    if CopyBuffer(MA_Handle_45, 0, 0, limit, MA_Buffer_45) != limit:
        return 0
    if CopyBuffer(MA_Handle_46, 0, 0, limit, MA_Buffer_46) != limit:
        return 0
    if CopyBuffer(MA_Handle_47, 0, 0, limit, MA_Buffer_47) != limit:
        return 0
    if CopyBuffer(MA_Handle_48, 0, 0, limit, MA_Buffer_48) != limit:
        return 0
    if CopyBuffer(MA_Handle_49, 0, 0, limit, MA_Buffer_49) != limit:
        return 0
    if CopyBuffer(MA_Handle_50, 0, 0, limit, MA_Buffer_50) != limit:
        return 0
    if CopyBuffer(MA_Handle_51, 0, 0, limit, MA_Buffer_51) != limit:
        return 0
    if CopyBuffer(MA_Handle_52, 0, 0, limit, MA_Buffer_52) != limit:
        return 0
    if CopyBuffer(MA_Handle_53, 0, 0, limit, MA_Buffer_53) != limit:
        return 0
    if CopyBuffer(MA_Handle_54, 0, 0, limit, MA_Buffer_54) != limit:
        return 0
    if CopyBuffer(MA_Handle_55, 0, 0, limit, MA_Buffer_55) != limit:
        return 0
    if CopyBuffer(MA_Handle_56, 0, 0, limit, MA_Buffer_56) != limit:
        return 0
    if CopyBuffer(MA_Handle_57, 0, 0, limit, MA_Buffer_57) != limit:
        return 0
    if CopyBuffer(MA_Handle_58, 0, 0, limit, MA_Buffer_58) != limit:
        return 0
    if CopyBuffer(MA_Handle_59, 0, 0, limit, MA_Buffer_59) != limit:
        return 0
    if CopyBuffer(MA_Handle_60, 0, 0, limit, MA_Buffer_60) != limit:
        return 0
    if CopyBuffer(MA_Handle_61, 0, 0, limit, MA_Buffer_61) != limit:
        return 0
    if CopyBuffer(MA_Handle_62, 0, 0, limit, MA_Buffer_62) != limit:
        return 0
    if CopyBuffer(MA_Handle_63, 0, 0, limit, MA_Buffer_63) != limit:
        return 0
    if CopyBuffer(MA_Handle_64, 0, 0, limit, MA_Buffer_64) != limit:
        return 0
    if CopyBuffer(MA_Handle_65, 0, 0, limit, MA_Buffer_65) != limit:
        return 0
    if CopyBuffer(MA_Handle_66, 0, 0, limit, MA_Buffer_66) != limit:
        return 0
    for i in range(0, limit):
        ExtMapBuffer01[i] = MA_Buffer_01[i]
        ExtMapBuffer02[i] = MA_Buffer_02[i]
        ExtMapBuffer03[i] = MA_Buffer_03[i]
        ExtMapBuffer04[i] = MA_Buffer_04[i]
        ExtMapBuffer05[i] = MA_Buffer_05[i]
        ExtMapBuffer06[i] = MA_Buffer_06[i]
        ExtMapBuffer07[i] = MA_Buffer_07[i]
        ExtMapBuffer08[i] = MA_Buffer_08[i]
        ExtMapBuffer09[i] = MA_Buffer_09[i]
        ExtMapBuffer10[i] = MA_Buffer_10[i]
        ExtMapBuffer11[i] = MA_Buffer_11[i]
        ExtMapBuffer12[i] = MA_Buffer_12[i]
        ExtMapBuffer13[i] = MA_Buffer_13[i]
        ExtMapBuffer14[i] = MA_Buffer_14[i]
        ExtMapBuffer15[i] = MA_Buffer_15[i]
        ExtMapBuffer16[i] = MA_Buffer_16[i]
        ExtMapBuffer17[i] = MA_Buffer_17[i]
        ExtMapBuffer18[i] = MA_Buffer_18[i]
        ExtMapBuffer19[i] = MA_Buffer_19[i]
        ExtMapBuffer20[i] = MA_Buffer_20[i]
        ExtMapBuffer21[i] = MA_Buffer_21[i]
        ExtMapBuffer22[i] = MA_Buffer_22[i]
        ExtMapBuffer23[i] = MA_Buffer_23[i]
        ExtMapBuffer24[i] = MA_Buffer_24[i]
        ExtMapBuffer25[i] = MA_Buffer_25[i]
        ExtMapBuffer26[i] = MA_Buffer_26[i]
        ExtMapBuffer27[i] = MA_Buffer_27[i]
        ExtMapBuffer28[i] = MA_Buffer_28[i]
        ExtMapBuffer29[i] = MA_Buffer_29[i]
        ExtMapBuffer30[i] = MA_Buffer_30[i]
        ExtMapBuffer31[i] = MA_Buffer_31[i]
        ExtMapBuffer32[i] = MA_Buffer_32[i]
        ExtMapBuffer33[i] = MA_Buffer_33[i]
        ExtMapBuffer34[i] = MA_Buffer_34[i]
        ExtMapBuffer35[i] = MA_Buffer_35[i]
        ExtMapBuffer36[i] = MA_Buffer_36[i]
        ExtMapBuffer37[i] = MA_Buffer_37[i]
        ExtMapBuffer38[i] = MA_Buffer_38[i]
        ExtMapBuffer39[i] = MA_Buffer_39[i]
        ExtMapBuffer40[i] = MA_Buffer_40[i]
        ExtMapBuffer41[i] = MA_Buffer_41[i]
        ExtMapBuffer42[i] = MA_Buffer_42[i]
        ExtMapBuffer43[i] = MA_Buffer_43[i]
        ExtMapBuffer44[i] = MA_Buffer_44[i]
        ExtMapBuffer45[i] = MA_Buffer_45[i]
        ExtMapBuffer46[i] = MA_Buffer_46[i]
        ExtMapBuffer47[i] = MA_Buffer_47[i]
        ExtMapBuffer48[i] = MA_Buffer_48[i]
        ExtMapBuffer49[i] = MA_Buffer_49[i]
        ExtMapBuffer50[i] = MA_Buffer_50[i]
        ExtMapBuffer51[i] = MA_Buffer_51[i]
        ExtMapBuffer52[i] = MA_Buffer_52[i]
        ExtMapBuffer53[i] = MA_Buffer_53[i]
        ExtMapBuffer54[i] = MA_Buffer_54[i]
        ExtMapBuffer55[i] = MA_Buffer_55[i]
        ExtMapBuffer56[i] = MA_Buffer_56[i]
        ExtMapBuffer57[i] = MA_Buffer_57[i]
        ExtMapBuffer58[i] = MA_Buffer_58[i]
        ExtMapBuffer59[i] = MA_Buffer_59[i]
        ExtMapBuffer60[i] = MA_Buffer_60[i]
        ExtMapBuffer61[i] = MA_Buffer_61[i]
        ExtMapBuffer62[i] = MA_Buffer_62[i]
        ExtMapBuffer63[i] = MA_Buffer_63[i]
        ExtMapBuffer64[i] = MA_Buffer_64[i]
        ExtMapBuffer65[i] = MA_Buffer_65[i]
        ExtMapBuffer66[i] = MA_Buffer_66[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RainbowMMA(_MQL5Indicator):
    name = 'RainbowMMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Type': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA Type
        'MA_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Price
        'MA_Period_01': 200,  # MA 01 Period
        'MA_Period_02': 195,  # MA 02 Period
        'MA_Period_03': 190,  # MA 03 Period
        'MA_Period_04': 185,  # MA 04 Period
        'MA_Period_05': 180,  # MA 05 Period
        'MA_Period_06': 175,  # MA 06 Period
        'MA_Period_07': 170,  # MA 07 Period
        'MA_Period_08': 165,  # MA 08 Period
        'MA_Period_09': 160,  # MA 09 Period
        'MA_Period_10': 155,  # MA 10 Period
        'MA_Period_11': 150,  # MA 11 Period
        'MA_Period_12': 145,  # MA 12 Period
        'MA_Period_13': 140,  # MA 13 Period
        'MA_Period_14': 135,  # MA 14 Period
        'MA_Period_15': 130,  # MA 15 Period
        'MA_Period_16': 125,  # MA 16 Period
        'MA_Period_17': 122,  # MA 17 Period
        'MA_Period_18': 118,  # MA 18 Period
        'MA_Period_19': 114,  # MA 19 Period
        'MA_Period_20': 110,  # MA 20 Period
        'MA_Period_21': 106,  # MA 21 Period
        'MA_Period_22': 102,  # MA 22 Period
        'MA_Period_23': 98,  # MA 23 Period
        'MA_Period_24': 94,  # MA 24 Period
        'MA_Period_25': 90,  # MA 25 Period
        'MA_Period_26': 86,  # MA 26 Period
        'MA_Period_27': 82,  # MA 27 Period
        'MA_Period_28': 78,  # MA 28 Period
        'MA_Period_29': 74,  # MA 29 Period
        'MA_Period_30': 71,  # MA 30 Period
        'MA_Period_31': 68,  # MA 31 Period
        'MA_Period_32': 65,  # MA 32 Period
        'MA_Period_33': 62,  # MA 33 Period
        'MA_Period_34': 59,  # MA 34 Period
        'MA_Period_35': 56,  # MA 35 Period
        'MA_Period_36': 53,  # MA 36 Period
        'MA_Period_37': 50,  # MA 37 Period
        'MA_Period_38': 47,  # MA 38 Period
        'MA_Period_39': 44,  # MA 39 Period
        'MA_Period_40': 41,  # MA 40 Period
        'MA_Period_41': 39,  # MA 41 Period
        'MA_Period_42': 37,  # MA 42 Period
        'MA_Period_43': 35,  # MA 43 Period
        'MA_Period_44': 33,  # MA 44 Period
        'MA_Period_45': 31,  # MA 45 Period
        'MA_Period_46': 29,  # MA 46 Period
        'MA_Period_47': 27,  # MA 47 Period
        'MA_Period_48': 25,  # MA 48 Period
        'MA_Period_49': 23,  # MA 49 Period
        'MA_Period_50': 21,  # MA 50 Period
        'MA_Period_51': 19,  # MA 51 Period
        'MA_Period_52': 17,  # MA 52 Period
        'MA_Period_53': 15,  # MA 53 Period
        'MA_Period_54': 14,  # MA 54 Period
        'MA_Period_55': 13,  # MA 55 Period
        'MA_Period_56': 12,  # MA 56 Period
        'MA_Period_57': 11,  # MA 57 Period
        'MA_Period_58': 10,  # MA 58 Period
        'MA_Period_59': 9,  # MA 59 Period
        'MA_Period_60': 8,  # MA 60 Period
        'MA_Period_61': 7,  # MA 61 Period
        'MA_Period_62': 6,  # MA 62 Period
        'MA_Period_63': 5,  # MA 63 Period
        'MA_Period_64': 4,  # MA 64 Period
        'MA_Period_65': 3,  # MA 65 Period
        'MA_Period_66': 2,  # MA 66 Period
    }

