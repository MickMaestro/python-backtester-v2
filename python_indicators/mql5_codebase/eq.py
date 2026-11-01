"""EQ — converted from MQL5: MQL5 Indicators/EQ/EQ.mq5

Historical virtual equity indicator
Purpose:
- Modeling (simulate) portfolio behavior with selected symbols
- Visualizing combined instrument movements
Applications:
- Identifying volatility-flat patterns for spread/equity trading
- Visual analysis of 'channel boundary' flat strategy effectiveness

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Virtual Equity'}, 'levels': [], 'description': ['Historical virtual equity indicator', '', 'Purpose:', '- Modeling (simulate) portfolio behavior with selected symbols', '- Visualizing combined instrument movements', '', 'Applications:', '- Identifying volatility-flat patterns for spread/equity trading', "- Visual analysis of 'channel boundary' flat strategy effectiveness"], 'name': 'EQ', 'source': 'MQL5 Indicators/EQ/EQ.mq5', 'folder': 'EQ', 'inputs': [{'mql': 'Lot_EURUSD', 'py': 'Lot_EURUSD', 'param': 'Lot_EURUSD', 'type': 'double', 'default': 1.0, 'label': 'EURUSD', 'sinput': False}, {'mql': 'Lot_GBPUSD', 'py': 'Lot_GBPUSD', 'param': 'Lot_GBPUSD', 'type': 'double', 'default': 1.0, 'label': 'GBPUSD', 'sinput': False}, {'mql': 'Lot_USDJPY', 'py': 'Lot_USDJPY', 'param': 'Lot_USDJPY', 'type': 'double', 'default': 1.0, 'label': 'USDJPY', 'sinput': False}, {'mql': 'Lot_USDCHF', 'py': 'Lot_USDCHF', 'param': 'Lot_USDCHF', 'type': 'double', 'default': 1.0, 'label': 'USDCHF', 'sinput': False}, {'mql': 'Lot_AUDUSD', 'py': 'Lot_AUDUSD', 'param': 'Lot_AUDUSD', 'type': 'double', 'default': 1.0, 'label': 'AUDUSD', 'sinput': False}, {'mql': 'Lot_USDCAD', 'py': 'Lot_USDCAD', 'param': 'Lot_USDCAD', 'type': 'double', 'default': 1.0, 'label': 'USDCAD', 'sinput': False}, {'mql': 'Lot_NZDUSD', 'py': 'Lot_NZDUSD', 'param': 'Lot_NZDUSD', 'type': 'double', 'default': 1.0, 'label': 'NZDUSD', 'sinput': False}, {'mql': 'Lot_EURGBP', 'py': 'Lot_EURGBP', 'param': 'Lot_EURGBP', 'type': 'double', 'default': 1.0, 'label': 'EURGBP', 'sinput': False}, {'mql': 'Lot_EURJPY', 'py': 'Lot_EURJPY', 'param': 'Lot_EURJPY', 'type': 'double', 'default': 1.0, 'label': 'EURJPY', 'sinput': False}, {'mql': 'Lot_EURCHF', 'py': 'Lot_EURCHF', 'param': 'Lot_EURCHF', 'type': 'double', 'default': 1.0, 'label': 'EURCHF', 'sinput': False}, {'mql': 'Lot_EURAUD', 'py': 'Lot_EURAUD', 'param': 'Lot_EURAUD', 'type': 'double', 'default': 1.0, 'label': 'EURAUD', 'sinput': False}, {'mql': 'Lot_EURCAD', 'py': 'Lot_EURCAD', 'param': 'Lot_EURCAD', 'type': 'double', 'default': 1.0, 'label': 'EURCAD', 'sinput': False}, {'mql': 'Lot_EURNZD', 'py': 'Lot_EURNZD', 'param': 'Lot_EURNZD', 'type': 'double', 'default': 1.0, 'label': 'EURNZD', 'sinput': False}, {'mql': 'Lot_GBPJPY', 'py': 'Lot_GBPJPY', 'param': 'Lot_GBPJPY', 'type': 'double', 'default': 1.0, 'label': 'GBPJPY', 'sinput': False}, {'mql': 'Lot_GBPCHF', 'py': 'Lot_GBPCHF', 'param': 'Lot_GBPCHF', 'type': 'double', 'default': 1.0, 'label': 'GBPCHF', 'sinput': False}, {'mql': 'Lot_GBPAUD', 'py': 'Lot_GBPAUD', 'param': 'Lot_GBPAUD', 'type': 'double', 'default': 1.0, 'label': 'GBPAUD', 'sinput': False}, {'mql': 'Lot_GBPCAD', 'py': 'Lot_GBPCAD', 'param': 'Lot_GBPCAD', 'type': 'double', 'default': 1.0, 'label': 'GBPCAD', 'sinput': False}, {'mql': 'Lot_GBPNZD', 'py': 'Lot_GBPNZD', 'param': 'Lot_GBPNZD', 'type': 'double', 'default': 1.0, 'label': 'GBPNZD', 'sinput': False}, {'mql': 'Lot_CHFJPY', 'py': 'Lot_CHFJPY', 'param': 'Lot_CHFJPY', 'type': 'double', 'default': 1.0, 'label': 'CHFJPY', 'sinput': False}, {'mql': 'Lot_AUDJPY', 'py': 'Lot_AUDJPY', 'param': 'Lot_AUDJPY', 'type': 'double', 'default': 1.0, 'label': 'AUDJPY', 'sinput': False}, {'mql': 'Lot_CADJPY', 'py': 'Lot_CADJPY', 'param': 'Lot_CADJPY', 'type': 'double', 'default': 1.0, 'label': 'CADJPY', 'sinput': False}, {'mql': 'Lot_NZDJPY', 'py': 'Lot_NZDJPY', 'param': 'Lot_NZDJPY', 'type': 'double', 'default': 1.0, 'label': 'NZDJPY', 'sinput': False}, {'mql': 'Lot_AUDCHF', 'py': 'Lot_AUDCHF', 'param': 'Lot_AUDCHF', 'type': 'double', 'default': 1.0, 'label': 'AUDCHF', 'sinput': False}, {'mql': 'Lot_AUDCAD', 'py': 'Lot_AUDCAD', 'param': 'Lot_AUDCAD', 'type': 'double', 'default': 1.0, 'label': 'AUDCAD', 'sinput': False}, {'mql': 'Lot_AUDNZD', 'py': 'Lot_AUDNZD', 'param': 'Lot_AUDNZD', 'type': 'double', 'default': 1.0, 'label': 'AUDNZD', 'sinput': False}, {'mql': 'Lot_CADCHF', 'py': 'Lot_CADCHF', 'param': 'Lot_CADCHF', 'type': 'double', 'default': 1.0, 'label': 'CADCHF', 'sinput': False}, {'mql': 'Lot_NZDCHF', 'py': 'Lot_NZDCHF', 'param': 'Lot_NZDCHF', 'type': 'double', 'default': 1.0, 'label': 'NZDCHF', 'sinput': False}, {'mql': 'Lot_NZDCAD', 'py': 'Lot_NZDCAD', 'param': 'Lot_NZDCAD', 'type': 'double', 'default': 1.0, 'label': 'NZDCAD', 'sinput': False}, {'mql': 'Dir_EURUSD', 'py': 'Dir_EURUSD', 'param': 'Dir_EURUSD', 'type': 'int', 'default': 0, 'label': 'EURUSD', 'sinput': False}, {'mql': 'Dir_GBPUSD', 'py': 'Dir_GBPUSD', 'param': 'Dir_GBPUSD', 'type': 'int', 'default': 1, 'label': 'GBPUSD', 'sinput': False}, {'mql': 'Dir_USDJPY', 'py': 'Dir_USDJPY', 'param': 'Dir_USDJPY', 'type': 'int', 'default': 0, 'label': 'USDJPY', 'sinput': False}, {'mql': 'Dir_USDCHF', 'py': 'Dir_USDCHF', 'param': 'Dir_USDCHF', 'type': 'int', 'default': 1, 'label': 'USDCHF', 'sinput': False}, {'mql': 'Dir_AUDUSD', 'py': 'Dir_AUDUSD', 'param': 'Dir_AUDUSD', 'type': 'int', 'default': 1, 'label': 'AUDUSD', 'sinput': False}, {'mql': 'Dir_USDCAD', 'py': 'Dir_USDCAD', 'param': 'Dir_USDCAD', 'type': 'int', 'default': 0, 'label': 'USDCAD', 'sinput': False}, {'mql': 'Dir_NZDUSD', 'py': 'Dir_NZDUSD', 'param': 'Dir_NZDUSD', 'type': 'int', 'default': 0, 'label': 'NZDUSD', 'sinput': False}, {'mql': 'Dir_EURGBP', 'py': 'Dir_EURGBP', 'param': 'Dir_EURGBP', 'type': 'int', 'default': 1, 'label': 'EURGBP', 'sinput': False}, {'mql': 'Dir_EURJPY', 'py': 'Dir_EURJPY', 'param': 'Dir_EURJPY', 'type': 'int', 'default': 0, 'label': 'EURJPY', 'sinput': False}, {'mql': 'Dir_EURCHF', 'py': 'Dir_EURCHF', 'param': 'Dir_EURCHF', 'type': 'int', 'default': 1, 'label': 'EURCHF', 'sinput': False}, {'mql': 'Dir_EURAUD', 'py': 'Dir_EURAUD', 'param': 'Dir_EURAUD', 'type': 'int', 'default': 0, 'label': 'EURAUD', 'sinput': False}, {'mql': 'Dir_EURCAD', 'py': 'Dir_EURCAD', 'param': 'Dir_EURCAD', 'type': 'int', 'default': 1, 'label': 'EURCAD', 'sinput': False}, {'mql': 'Dir_EURNZD', 'py': 'Dir_EURNZD', 'param': 'Dir_EURNZD', 'type': 'int', 'default': 1, 'label': 'EURNZD', 'sinput': False}, {'mql': 'Dir_GBPJPY', 'py': 'Dir_GBPJPY', 'param': 'Dir_GBPJPY', 'type': 'int', 'default': 1, 'label': 'GBPJPY', 'sinput': False}, {'mql': 'Dir_GBPCHF', 'py': 'Dir_GBPCHF', 'param': 'Dir_GBPCHF', 'type': 'int', 'default': 0, 'label': 'GBPCHF', 'sinput': False}, {'mql': 'Dir_GBPAUD', 'py': 'Dir_GBPAUD', 'param': 'Dir_GBPAUD', 'type': 'int', 'default': 0, 'label': 'GBPAUD', 'sinput': False}, {'mql': 'Dir_GBPCAD', 'py': 'Dir_GBPCAD', 'param': 'Dir_GBPCAD', 'type': 'int', 'default': 1, 'label': 'GBPCAD', 'sinput': False}, {'mql': 'Dir_GBPNZD', 'py': 'Dir_GBPNZD', 'param': 'Dir_GBPNZD', 'type': 'int', 'default': 0, 'label': 'GBPNZD', 'sinput': False}, {'mql': 'Dir_CHFJPY', 'py': 'Dir_CHFJPY', 'param': 'Dir_CHFJPY', 'type': 'int', 'default': 0, 'label': 'CHFJPY', 'sinput': False}, {'mql': 'Dir_AUDJPY', 'py': 'Dir_AUDJPY', 'param': 'Dir_AUDJPY', 'type': 'int', 'default': 1, 'label': 'AUDJPY', 'sinput': False}, {'mql': 'Dir_CADJPY', 'py': 'Dir_CADJPY', 'param': 'Dir_CADJPY', 'type': 'int', 'default': 0, 'label': 'CADJPY', 'sinput': False}, {'mql': 'Dir_NZDJPY', 'py': 'Dir_NZDJPY', 'param': 'Dir_NZDJPY', 'type': 'int', 'default': 1, 'label': 'NZDJPY', 'sinput': False}, {'mql': 'Dir_AUDCHF', 'py': 'Dir_AUDCHF', 'param': 'Dir_AUDCHF', 'type': 'int', 'default': 0, 'label': 'AUDCHF', 'sinput': False}, {'mql': 'Dir_AUDCAD', 'py': 'Dir_AUDCAD', 'param': 'Dir_AUDCAD', 'type': 'int', 'default': 1, 'label': 'AUDCAD', 'sinput': False}, {'mql': 'Dir_AUDNZD', 'py': 'Dir_AUDNZD', 'param': 'Dir_AUDNZD', 'type': 'int', 'default': 0, 'label': 'AUDNZD', 'sinput': False}, {'mql': 'Dir_CADCHF', 'py': 'Dir_CADCHF', 'param': 'Dir_CADCHF', 'type': 'int', 'default': 0, 'label': 'CADCHF', 'sinput': False}, {'mql': 'Dir_NZDCHF', 'py': 'Dir_NZDCHF', 'param': 'Dir_NZDCHF', 'type': 'int', 'default': 1, 'label': 'NZDCHF', 'sinput': False}, {'mql': 'Dir_NZDCAD', 'py': 'Dir_NZDCAD', 'param': 'Dir_NZDCAD', 'type': 'int', 'default': 0, 'label': 'NZDCAD', 'sinput': False}, {'mql': 'Enable_EURUSD', 'py': 'Enable_EURUSD', 'param': 'Enable_EURUSD', 'type': 'bool', 'default': True, 'label': 'EURUSD', 'sinput': False}, {'mql': 'Enable_GBPUSD', 'py': 'Enable_GBPUSD', 'param': 'Enable_GBPUSD', 'type': 'bool', 'default': False, 'label': 'GBPUSD', 'sinput': False}, {'mql': 'Enable_USDJPY', 'py': 'Enable_USDJPY', 'param': 'Enable_USDJPY', 'type': 'bool', 'default': False, 'label': 'USDJPY', 'sinput': False}, {'mql': 'Enable_USDCHF', 'py': 'Enable_USDCHF', 'param': 'Enable_USDCHF', 'type': 'bool', 'default': False, 'label': 'USDCHF', 'sinput': False}, {'mql': 'Enable_AUDUSD', 'py': 'Enable_AUDUSD', 'param': 'Enable_AUDUSD', 'type': 'bool', 'default': False, 'label': 'AUDUSD', 'sinput': False}, {'mql': 'Enable_USDCAD', 'py': 'Enable_USDCAD', 'param': 'Enable_USDCAD', 'type': 'bool', 'default': False, 'label': 'USDCAD', 'sinput': False}, {'mql': 'Enable_NZDUSD', 'py': 'Enable_NZDUSD', 'param': 'Enable_NZDUSD', 'type': 'bool', 'default': False, 'label': 'NZDUSD', 'sinput': False}, {'mql': 'Enable_EURGBP', 'py': 'Enable_EURGBP', 'param': 'Enable_EURGBP', 'type': 'bool', 'default': False, 'label': 'EURGBP', 'sinput': False}, {'mql': 'Enable_EURJPY', 'py': 'Enable_EURJPY', 'param': 'Enable_EURJPY', 'type': 'bool', 'default': False, 'label': 'EURJPY', 'sinput': False}, {'mql': 'Enable_EURCHF', 'py': 'Enable_EURCHF', 'param': 'Enable_EURCHF', 'type': 'bool', 'default': False, 'label': 'EURCHF', 'sinput': False}, {'mql': 'Enable_EURAUD', 'py': 'Enable_EURAUD', 'param': 'Enable_EURAUD', 'type': 'bool', 'default': False, 'label': 'EURAUD', 'sinput': False}, {'mql': 'Enable_EURCAD', 'py': 'Enable_EURCAD', 'param': 'Enable_EURCAD', 'type': 'bool', 'default': False, 'label': 'EURCAD', 'sinput': False}, {'mql': 'Enable_EURNZD', 'py': 'Enable_EURNZD', 'param': 'Enable_EURNZD', 'type': 'bool', 'default': False, 'label': 'EURNZD', 'sinput': False}, {'mql': 'Enable_GBPJPY', 'py': 'Enable_GBPJPY', 'param': 'Enable_GBPJPY', 'type': 'bool', 'default': False, 'label': 'GBPJPY', 'sinput': False}, {'mql': 'Enable_GBPCHF', 'py': 'Enable_GBPCHF', 'param': 'Enable_GBPCHF', 'type': 'bool', 'default': False, 'label': 'GBPCHF', 'sinput': False}, {'mql': 'Enable_GBPAUD', 'py': 'Enable_GBPAUD', 'param': 'Enable_GBPAUD', 'type': 'bool', 'default': False, 'label': 'GBPAUD', 'sinput': False}, {'mql': 'Enable_GBPCAD', 'py': 'Enable_GBPCAD', 'param': 'Enable_GBPCAD', 'type': 'bool', 'default': False, 'label': 'GBPCAD', 'sinput': False}, {'mql': 'Enable_GBPNZD', 'py': 'Enable_GBPNZD', 'param': 'Enable_GBPNZD', 'type': 'bool', 'default': False, 'label': 'GBPNZD', 'sinput': False}, {'mql': 'Enable_CHFJPY', 'py': 'Enable_CHFJPY', 'param': 'Enable_CHFJPY', 'type': 'bool', 'default': False, 'label': 'CHFJPY', 'sinput': False}, {'mql': 'Enable_AUDJPY', 'py': 'Enable_AUDJPY', 'param': 'Enable_AUDJPY', 'type': 'bool', 'default': False, 'label': 'AUDJPY', 'sinput': False}, {'mql': 'Enable_CADJPY', 'py': 'Enable_CADJPY', 'param': 'Enable_CADJPY', 'type': 'bool', 'default': False, 'label': 'CADJPY', 'sinput': False}, {'mql': 'Enable_NZDJPY', 'py': 'Enable_NZDJPY', 'param': 'Enable_NZDJPY', 'type': 'bool', 'default': False, 'label': 'NZDJPY', 'sinput': False}, {'mql': 'Enable_AUDCHF', 'py': 'Enable_AUDCHF', 'param': 'Enable_AUDCHF', 'type': 'bool', 'default': False, 'label': 'AUDCHF', 'sinput': False}, {'mql': 'Enable_AUDCAD', 'py': 'Enable_AUDCAD', 'param': 'Enable_AUDCAD', 'type': 'bool', 'default': False, 'label': 'AUDCAD', 'sinput': False}, {'mql': 'Enable_AUDNZD', 'py': 'Enable_AUDNZD', 'param': 'Enable_AUDNZD', 'type': 'bool', 'default': False, 'label': 'AUDNZD', 'sinput': False}, {'mql': 'Enable_CADCHF', 'py': 'Enable_CADCHF', 'param': 'Enable_CADCHF', 'type': 'bool', 'default': False, 'label': 'CADCHF', 'sinput': False}, {'mql': 'Enable_NZDCHF', 'py': 'Enable_NZDCHF', 'param': 'Enable_NZDCHF', 'type': 'bool', 'default': False, 'label': 'NZDCHF', 'sinput': False}, {'mql': 'Enable_NZDCAD', 'py': 'Enable_NZDCAD', 'param': 'Enable_NZDCAD', 'type': 'bool', 'default': False, 'label': 'NZDCAD', 'sinput': False}, {'mql': 'Symbo_suffix', 'py': 'Symbo_suffix', 'param': None, 'type': 'string', 'default': '', 'label': 'Symbol suffix', 'sinput': False}, {'mql': 'Bars_to_calculate', 'py': 'Bars_to_calculate', 'param': 'Bars_to_calculate', 'type': 'int', 'default': 1000, 'label': 'Drawing depth in bars (should be < available symbol history)', 'sinput': False}, {'mql': 'Initial_balance', 'py': 'Initial_balance', 'param': 'Initial_balance', 'type': 'double', 'default': 0.0, 'label': 'Initial virtual balance (optional)', 'sinput': False}, {'mql': 'InfoOutput', 'py': 'InfoOutput', 'param': 'InfoOutput', 'type': 'int', 'default': 3, 'label': 'Information output mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_TRADE_DIRECTION
DIR_BUY = 0
DIR_SELL = 1
_enum('ENUM_TRADE_DIRECTION', {0: 'DIR_BUY', 1: 'DIR_SELL'})

# enum ENUM_OUTPUT_MODE
OUTPUT_NONE = 0
OUTPUT_PRINT = 1
OUTPUT_COMMENT = 2
OUTPUT_BOTH = 3
_enum('ENUM_OUTPUT_MODE', {0: 'OUTPUT_NONE', 1: 'OUTPUT_PRINT', 2: 'OUTPUT_COMMENT', 3: 'OUTPUT_BOTH'})

# ---- inputs and global variables
Lot_EURUSD = _input('Lot_EURUSD', 1.0)  # EURUSD
Lot_GBPUSD = _input('Lot_GBPUSD', 1.0)  # GBPUSD
Lot_USDJPY = _input('Lot_USDJPY', 1.0)  # USDJPY
Lot_USDCHF = _input('Lot_USDCHF', 1.0)  # USDCHF
Lot_AUDUSD = _input('Lot_AUDUSD', 1.0)  # AUDUSD
Lot_USDCAD = _input('Lot_USDCAD', 1.0)  # USDCAD
Lot_NZDUSD = _input('Lot_NZDUSD', 1.0)  # NZDUSD
Lot_EURGBP = _input('Lot_EURGBP', 1.0)  # EURGBP
Lot_EURJPY = _input('Lot_EURJPY', 1.0)  # EURJPY
Lot_EURCHF = _input('Lot_EURCHF', 1.0)  # EURCHF
Lot_EURAUD = _input('Lot_EURAUD', 1.0)  # EURAUD
Lot_EURCAD = _input('Lot_EURCAD', 1.0)  # EURCAD
Lot_EURNZD = _input('Lot_EURNZD', 1.0)  # EURNZD
Lot_GBPJPY = _input('Lot_GBPJPY', 1.0)  # GBPJPY
Lot_GBPCHF = _input('Lot_GBPCHF', 1.0)  # GBPCHF
Lot_GBPAUD = _input('Lot_GBPAUD', 1.0)  # GBPAUD
Lot_GBPCAD = _input('Lot_GBPCAD', 1.0)  # GBPCAD
Lot_GBPNZD = _input('Lot_GBPNZD', 1.0)  # GBPNZD
Lot_CHFJPY = _input('Lot_CHFJPY', 1.0)  # CHFJPY
Lot_AUDJPY = _input('Lot_AUDJPY', 1.0)  # AUDJPY
Lot_CADJPY = _input('Lot_CADJPY', 1.0)  # CADJPY
Lot_NZDJPY = _input('Lot_NZDJPY', 1.0)  # NZDJPY
Lot_AUDCHF = _input('Lot_AUDCHF', 1.0)  # AUDCHF
Lot_AUDCAD = _input('Lot_AUDCAD', 1.0)  # AUDCAD
Lot_AUDNZD = _input('Lot_AUDNZD', 1.0)  # AUDNZD
Lot_CADCHF = _input('Lot_CADCHF', 1.0)  # CADCHF
Lot_NZDCHF = _input('Lot_NZDCHF', 1.0)  # NZDCHF
Lot_NZDCAD = _input('Lot_NZDCAD', 1.0)  # NZDCAD
Dir_EURUSD = _input('Dir_EURUSD', DIR_BUY)  # EURUSD
Dir_GBPUSD = _input('Dir_GBPUSD', DIR_SELL)  # GBPUSD
Dir_USDJPY = _input('Dir_USDJPY', DIR_BUY)  # USDJPY
Dir_USDCHF = _input('Dir_USDCHF', DIR_SELL)  # USDCHF
Dir_AUDUSD = _input('Dir_AUDUSD', DIR_SELL)  # AUDUSD
Dir_USDCAD = _input('Dir_USDCAD', DIR_BUY)  # USDCAD
Dir_NZDUSD = _input('Dir_NZDUSD', DIR_BUY)  # NZDUSD
Dir_EURGBP = _input('Dir_EURGBP', DIR_SELL)  # EURGBP
Dir_EURJPY = _input('Dir_EURJPY', DIR_BUY)  # EURJPY
Dir_EURCHF = _input('Dir_EURCHF', DIR_SELL)  # EURCHF
Dir_EURAUD = _input('Dir_EURAUD', DIR_BUY)  # EURAUD
Dir_EURCAD = _input('Dir_EURCAD', DIR_SELL)  # EURCAD
Dir_EURNZD = _input('Dir_EURNZD', DIR_SELL)  # EURNZD
Dir_GBPJPY = _input('Dir_GBPJPY', DIR_SELL)  # GBPJPY
Dir_GBPCHF = _input('Dir_GBPCHF', DIR_BUY)  # GBPCHF
Dir_GBPAUD = _input('Dir_GBPAUD', DIR_BUY)  # GBPAUD
Dir_GBPCAD = _input('Dir_GBPCAD', DIR_SELL)  # GBPCAD
Dir_GBPNZD = _input('Dir_GBPNZD', DIR_BUY)  # GBPNZD
Dir_CHFJPY = _input('Dir_CHFJPY', DIR_BUY)  # CHFJPY
Dir_AUDJPY = _input('Dir_AUDJPY', DIR_SELL)  # AUDJPY
Dir_CADJPY = _input('Dir_CADJPY', DIR_BUY)  # CADJPY
Dir_NZDJPY = _input('Dir_NZDJPY', DIR_SELL)  # NZDJPY
Dir_AUDCHF = _input('Dir_AUDCHF', DIR_BUY)  # AUDCHF
Dir_AUDCAD = _input('Dir_AUDCAD', DIR_SELL)  # AUDCAD
Dir_AUDNZD = _input('Dir_AUDNZD', DIR_BUY)  # AUDNZD
Dir_CADCHF = _input('Dir_CADCHF', DIR_BUY)  # CADCHF
Dir_NZDCHF = _input('Dir_NZDCHF', DIR_SELL)  # NZDCHF
Dir_NZDCAD = _input('Dir_NZDCAD', DIR_BUY)  # NZDCAD
Enable_EURUSD = _input('Enable_EURUSD', True)  # EURUSD
Enable_GBPUSD = _input('Enable_GBPUSD', False)  # GBPUSD
Enable_USDJPY = _input('Enable_USDJPY', False)  # USDJPY
Enable_USDCHF = _input('Enable_USDCHF', False)  # USDCHF
Enable_AUDUSD = _input('Enable_AUDUSD', False)  # AUDUSD
Enable_USDCAD = _input('Enable_USDCAD', False)  # USDCAD
Enable_NZDUSD = _input('Enable_NZDUSD', False)  # NZDUSD
Enable_EURGBP = _input('Enable_EURGBP', False)  # EURGBP
Enable_EURJPY = _input('Enable_EURJPY', False)  # EURJPY
Enable_EURCHF = _input('Enable_EURCHF', False)  # EURCHF
Enable_EURAUD = _input('Enable_EURAUD', False)  # EURAUD
Enable_EURCAD = _input('Enable_EURCAD', False)  # EURCAD
Enable_EURNZD = _input('Enable_EURNZD', False)  # EURNZD
Enable_GBPJPY = _input('Enable_GBPJPY', False)  # GBPJPY
Enable_GBPCHF = _input('Enable_GBPCHF', False)  # GBPCHF
Enable_GBPAUD = _input('Enable_GBPAUD', False)  # GBPAUD
Enable_GBPCAD = _input('Enable_GBPCAD', False)  # GBPCAD
Enable_GBPNZD = _input('Enable_GBPNZD', False)  # GBPNZD
Enable_CHFJPY = _input('Enable_CHFJPY', False)  # CHFJPY
Enable_AUDJPY = _input('Enable_AUDJPY', False)  # AUDJPY
Enable_CADJPY = _input('Enable_CADJPY', False)  # CADJPY
Enable_NZDJPY = _input('Enable_NZDJPY', False)  # NZDJPY
Enable_AUDCHF = _input('Enable_AUDCHF', False)  # AUDCHF
Enable_AUDCAD = _input('Enable_AUDCAD', False)  # AUDCAD
Enable_AUDNZD = _input('Enable_AUDNZD', False)  # AUDNZD
Enable_CADCHF = _input('Enable_CADCHF', False)  # CADCHF
Enable_NZDCHF = _input('Enable_NZDCHF', False)  # NZDCHF
Enable_NZDCAD = _input('Enable_NZDCAD', False)  # NZDCAD
Symbo_suffix = _input('Symbo_suffix', '')  # Symbol suffix
Bars_to_calculate = _input('Bars_to_calculate', 1000)  # Drawing depth in bars (should be < available symbol history)
Initial_balance = _input('Initial_balance', 0.0)  # Initial virtual balance (optional)
InfoOutput = _input('InfoOutput', OUTPUT_BOTH)  # Information output mode
currency_symbol = Arr.of(['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'USDCAD', 'NZDUSD', 'EURGBP', 'EURJPY', 'EURCHF', 'EURAUD', 'EURCAD', 'EURNZD', 'GBPJPY', 'GBPCHF', 'GBPAUD', 'GBPCAD', 'GBPNZD', 'CHFJPY', 'AUDJPY', 'CADJPY', 'NZDJPY', 'AUDCHF', 'AUDCAD', 'AUDNZD', 'CADCHF', 'NZDCHF', 'NZDCAD'], fill="")
Equity_buffer = Arr(0, 0.0)  # main buffer for equity values
initial_prices = Arr(0, 0.0)  # prices on starting bar for change calculation
directions = Arr(0, 0)  # converted directions (1/-1)
bars_count = Arr(0, 0)  # available history for each symbol
settings_info = ''  # storage for settings information
total_symbols = 0  # symbol count
start_flag = True
start_chart_flag = True

def OnInit():
    global total_symbols
    total_symbols = ArraySize(currency_symbol)
    ArrayResize(initial_prices, total_symbols)
    ArrayResize(directions, total_symbols)
    ArrayResize(bars_count, total_symbols)
    SetIndexBuffer(0, Equity_buffer, INDICATOR_DATA)
    ArraySetAsSeries(Equity_buffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    EventSetTimer(1)
    return INIT_SUCCEEDED

def OnTimer():
    Main()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    Main()
    return rates_total

def Main():
    global start_chart_flag, start_flag
    start = 0
    if start_flag:
        ArrayInitialize(Equity_buffer, EMPTY_VALUE)
        start_time = iTime(Symbol(), Period(), Bars_to_calculate)
        i = 0
        while i < total_symbols:
            pair = currency_symbol[i]
            if not Is_Pair_Enabled(pair):
                i += 1
                continue
            symbol = Get_Full_Symbol_Name(pair)
            symbol_check = Check_symbols(symbol)
            if not symbol_check:
                return
            directions[i] = Get_Direction_By_Pair(pair)
            i += 1
        i = 0
        while i < total_symbols:
            if not Is_Pair_Enabled(currency_symbol[i]):
                i += 1
                continue
            symbol = Get_Full_Symbol_Name(currency_symbol[i])
            initial_prices[i] = iOpen(symbol, Period(), Bars_to_calculate)
            i += 1
        Print_Settings()
        start = Bars_to_calculate
        start_flag = False
    else:
        start = 0
        if start_chart_flag:
            ChartRedraw()
        start_chart_flag = False
    for i in range(start, 0 - 1, -1):
        EQ = Initial_balance
        j = 0
        while j < total_symbols:
            pair = currency_symbol[j]
            if not Is_Pair_Enabled(pair):
                j += 1
                continue
            symbol = Get_Full_Symbol_Name(pair)
            current_close = iClose(symbol, Period(), i)
            if current_close == 0:
                j += 1
                continue
            initial_price = initial_prices[j]
            price_change_in_points = _fdiv(current_close - initial_price, SymbolInfoDouble(symbol, SYMBOL_POINT))
            point_value = Calculate_point_value(symbol)
            lot = Get_Lot_By_Symbol(pair)
            direction = directions[j]
            eq = price_change_in_points * direction * lot * point_value
            EQ += eq
            j += 1
        Equity_buffer[i] = EQ

def Get_Full_Symbol_Name(baseSymbol):
    return baseSymbol + Symbo_suffix

def Check_symbols(sym):
    if not SymbolSelect(sym, True):
        Print(sym + ' - error: symbol not found in Market Watch!')
        return False
    if iClose(sym, PERIOD_CURRENT, Bars_to_calculate) <= 0:
        Comment('LOADING HISTORY: ' + sym)
        return False
    return True

def Calculate_point_value(symbol):
    tick_value = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
    tick_size = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
    point = SymbolInfoDouble(symbol, SYMBOL_POINT)
    return tick_value * _fdiv(point, tick_size)

def Get_Lot_By_Symbol(pair):
    if pair == 'EURUSD':
        return Lot_EURUSD
    if pair == 'GBPUSD':
        return Lot_GBPUSD
    if pair == 'USDJPY':
        return Lot_USDJPY
    if pair == 'USDCHF':
        return Lot_USDCHF
    if pair == 'AUDUSD':
        return Lot_AUDUSD
    if pair == 'USDCAD':
        return Lot_USDCAD
    if pair == 'NZDUSD':
        return Lot_NZDUSD
    if pair == 'EURGBP':
        return Lot_EURGBP
    if pair == 'EURJPY':
        return Lot_EURJPY
    if pair == 'EURCHF':
        return Lot_EURCHF
    if pair == 'EURAUD':
        return Lot_EURAUD
    if pair == 'EURCAD':
        return Lot_EURCAD
    if pair == 'EURNZD':
        return Lot_EURNZD
    if pair == 'GBPJPY':
        return Lot_GBPJPY
    if pair == 'GBPCHF':
        return Lot_GBPCHF
    if pair == 'GBPAUD':
        return Lot_GBPAUD
    if pair == 'GBPCAD':
        return Lot_GBPCAD
    if pair == 'GBPNZD':
        return Lot_GBPNZD
    if pair == 'CHFJPY':
        return Lot_CHFJPY
    if pair == 'AUDJPY':
        return Lot_AUDJPY
    if pair == 'CADJPY':
        return Lot_CADJPY
    if pair == 'NZDJPY':
        return Lot_NZDJPY
    if pair == 'AUDCHF':
        return Lot_AUDCHF
    if pair == 'AUDCAD':
        return Lot_AUDCAD
    if pair == 'AUDNZD':
        return Lot_AUDNZD
    if pair == 'CADCHF':
        return Lot_CADCHF
    if pair == 'NZDCHF':
        return Lot_NZDCHF
    if pair == 'NZDCAD':
        return Lot_NZDCAD
    return 0.0

def Get_Direction_By_Pair(pair):
    if pair == 'EURUSD':
        return (1 if (Dir_EURUSD == DIR_BUY) else -1)
    if pair == 'GBPUSD':
        return (1 if (Dir_GBPUSD == DIR_BUY) else -1)
    if pair == 'USDJPY':
        return (1 if (Dir_USDJPY == DIR_BUY) else -1)
    if pair == 'USDCHF':
        return (1 if (Dir_USDCHF == DIR_BUY) else -1)
    if pair == 'AUDUSD':
        return (1 if (Dir_AUDUSD == DIR_BUY) else -1)
    if pair == 'USDCAD':
        return (1 if (Dir_USDCAD == DIR_BUY) else -1)
    if pair == 'NZDUSD':
        return (1 if (Dir_NZDUSD == DIR_BUY) else -1)
    if pair == 'EURGBP':
        return (1 if (Dir_EURGBP == DIR_BUY) else -1)
    if pair == 'EURJPY':
        return (1 if (Dir_EURJPY == DIR_BUY) else -1)
    if pair == 'EURCHF':
        return (1 if (Dir_EURCHF == DIR_BUY) else -1)
    if pair == 'EURAUD':
        return (1 if (Dir_EURAUD == DIR_BUY) else -1)
    if pair == 'EURCAD':
        return (1 if (Dir_EURCAD == DIR_BUY) else -1)
    if pair == 'EURNZD':
        return (1 if (Dir_EURNZD == DIR_BUY) else -1)
    if pair == 'GBPJPY':
        return (1 if (Dir_GBPJPY == DIR_BUY) else -1)
    if pair == 'GBPCHF':
        return (1 if (Dir_GBPCHF == DIR_BUY) else -1)
    if pair == 'GBPAUD':
        return (1 if (Dir_GBPAUD == DIR_BUY) else -1)
    if pair == 'GBPCAD':
        return (1 if (Dir_GBPCAD == DIR_BUY) else -1)
    if pair == 'GBPNZD':
        return (1 if (Dir_GBPNZD == DIR_BUY) else -1)
    if pair == 'CHFJPY':
        return (1 if (Dir_CHFJPY == DIR_BUY) else -1)
    if pair == 'AUDJPY':
        return (1 if (Dir_AUDJPY == DIR_BUY) else -1)
    if pair == 'CADJPY':
        return (1 if (Dir_CADJPY == DIR_BUY) else -1)
    if pair == 'NZDJPY':
        return (1 if (Dir_NZDJPY == DIR_BUY) else -1)
    if pair == 'AUDCHF':
        return (1 if (Dir_AUDCHF == DIR_BUY) else -1)
    if pair == 'AUDCAD':
        return (1 if (Dir_AUDCAD == DIR_BUY) else -1)
    if pair == 'AUDNZD':
        return (1 if (Dir_AUDNZD == DIR_BUY) else -1)
    if pair == 'CADCHF':
        return (1 if (Dir_CADCHF == DIR_BUY) else -1)
    if pair == 'NZDCHF':
        return (1 if (Dir_NZDCHF == DIR_BUY) else -1)
    if pair == 'NZDCAD':
        return (1 if (Dir_NZDCAD == DIR_BUY) else -1)
    return 0

def Is_Pair_Enabled(pair):
    if pair == 'EURUSD':
        return Enable_EURUSD
    if pair == 'GBPUSD':
        return Enable_GBPUSD
    if pair == 'USDJPY':
        return Enable_USDJPY
    if pair == 'USDCHF':
        return Enable_USDCHF
    if pair == 'AUDUSD':
        return Enable_AUDUSD
    if pair == 'USDCAD':
        return Enable_USDCAD
    if pair == 'NZDUSD':
        return Enable_NZDUSD
    if pair == 'EURGBP':
        return Enable_EURGBP
    if pair == 'EURJPY':
        return Enable_EURJPY
    if pair == 'EURCHF':
        return Enable_EURCHF
    if pair == 'EURAUD':
        return Enable_EURAUD
    if pair == 'EURCAD':
        return Enable_EURCAD
    if pair == 'EURNZD':
        return Enable_EURNZD
    if pair == 'GBPJPY':
        return Enable_GBPJPY
    if pair == 'GBPCHF':
        return Enable_GBPCHF
    if pair == 'GBPAUD':
        return Enable_GBPAUD
    if pair == 'GBPCAD':
        return Enable_GBPCAD
    if pair == 'GBPNZD':
        return Enable_GBPNZD
    if pair == 'CHFJPY':
        return Enable_CHFJPY
    if pair == 'AUDJPY':
        return Enable_AUDJPY
    if pair == 'CADJPY':
        return Enable_CADJPY
    if pair == 'NZDJPY':
        return Enable_NZDJPY
    if pair == 'AUDCHF':
        return Enable_AUDCHF
    if pair == 'AUDCAD':
        return Enable_AUDCAD
    if pair == 'AUDNZD':
        return Enable_AUDNZD
    if pair == 'CADCHF':
        return Enable_CADCHF
    if pair == 'NZDCHF':
        return Enable_NZDCHF
    if pair == 'NZDCAD':
        return Enable_NZDCAD
    return False

def Print_Settings():
    global settings_info
    Print('')
    settings_info = ''
    print_info = ''
    comment_info = ''
    new_line = '\n'
    active_count = 0
    i = 0
    while i < total_symbols:
        if Is_Pair_Enabled(currency_symbol[i]):
            active_count += 1
        i += 1
    header = '=== VIRTUAL EQUITY SETTINGS ==='
    print_info += new_line
    print_info += header + new_line
    max_symbol_len = 0
    i = 0
    while i < total_symbols:
        if not Is_Pair_Enabled(currency_symbol[i]):
            i += 1
            continue
        len_ = StringLen(currency_symbol[i])
        if len_ > max_symbol_len:
            max_symbol_len = len_
        i += 1
    field_width = max_symbol_len
    common_info = new_line + 'Active symbols:' + new_line
    i = 0
    while i < total_symbols:
        if not Is_Pair_Enabled(currency_symbol[i]):
            i += 1
            continue
        dir_str = ('BUY' if (Get_Direction_By_Pair(currency_symbol[i]) == 1) else 'SELL')
        arrow = ('▲' if (dir_str == 'BUY') else '▼')
        symbol_field = StringFormat('%-' + IntegerToString(field_width) + 's', currency_symbol[i])
        entry = StringFormat('%s %s %-4s %.2f', symbol_field, arrow, dir_str, Get_Lot_By_Symbol(currency_symbol[i]))
        common_info += entry + new_line
        i += 1
    print_info += common_info + new_line
    print_info += 'General parameters:' + new_line
    print_info += 'Symbol suffix: ' + ('not specified' if (Symbo_suffix == '') else Symbo_suffix) + new_line
    print_info += 'Bars to calculate: ' + IntegerToString(Bars_to_calculate) + new_line
    print_info += 'Initial balance: ' + DoubleToString(Initial_balance, 2) + new_line
    warning = False
    warn_text = new_line + 'WARNINGS:'
    if active_count == 0:
        warn_text += new_line + "• No active instruments! Indicator won't work"
        warning = True
    if warning:
        print_info += warn_text + new_line
        print_info += 'Recommendation: Check activation settings and data availability' + new_line
    comment_info = 'Active symbols:' + new_line
    i = 0
    while i < total_symbols:
        if not Is_Pair_Enabled(currency_symbol[i]):
            i += 1
            continue
        dir_str = ('BUY' if (Get_Direction_By_Pair(currency_symbol[i]) == 1) else 'SELL')
        arrow = ('▲' if (dir_str == 'BUY') else '▼')
        comment_info += StringFormat('%s %s %.1f', currency_symbol[i], arrow, Get_Lot_By_Symbol(currency_symbol[i])) + new_line
        i += 1
    if active_count == 0:
        comment_info = 'WARNING!\nNo active\ninstruments'
    _sw1 = InfoOutput
    if _sw1 == OUTPUT_PRINT:
        Print(print_info)
    elif _sw1 == OUTPUT_COMMENT:
        Comment(comment_info)
    elif _sw1 == OUTPUT_BOTH:
        Print(print_info)
        Comment(comment_info)
    else:
        pass

def OnDeinit(reason):
    if InfoOutput == OUTPUT_COMMENT or InfoOutput == OUTPUT_BOTH:
        Comment('')
    EventKillTimer()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EQ(_MQL5Indicator):
    name = 'EQ'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Lot_EURUSD': 1.0,  # EURUSD
        'Lot_GBPUSD': 1.0,  # GBPUSD
        'Lot_USDJPY': 1.0,  # USDJPY
        'Lot_USDCHF': 1.0,  # USDCHF
        'Lot_AUDUSD': 1.0,  # AUDUSD
        'Lot_USDCAD': 1.0,  # USDCAD
        'Lot_NZDUSD': 1.0,  # NZDUSD
        'Lot_EURGBP': 1.0,  # EURGBP
        'Lot_EURJPY': 1.0,  # EURJPY
        'Lot_EURCHF': 1.0,  # EURCHF
        'Lot_EURAUD': 1.0,  # EURAUD
        'Lot_EURCAD': 1.0,  # EURCAD
        'Lot_EURNZD': 1.0,  # EURNZD
        'Lot_GBPJPY': 1.0,  # GBPJPY
        'Lot_GBPCHF': 1.0,  # GBPCHF
        'Lot_GBPAUD': 1.0,  # GBPAUD
        'Lot_GBPCAD': 1.0,  # GBPCAD
        'Lot_GBPNZD': 1.0,  # GBPNZD
        'Lot_CHFJPY': 1.0,  # CHFJPY
        'Lot_AUDJPY': 1.0,  # AUDJPY
        'Lot_CADJPY': 1.0,  # CADJPY
        'Lot_NZDJPY': 1.0,  # NZDJPY
        'Lot_AUDCHF': 1.0,  # AUDCHF
        'Lot_AUDCAD': 1.0,  # AUDCAD
        'Lot_AUDNZD': 1.0,  # AUDNZD
        'Lot_CADCHF': 1.0,  # CADCHF
        'Lot_NZDCHF': 1.0,  # NZDCHF
        'Lot_NZDCAD': 1.0,  # NZDCAD
        'Dir_EURUSD': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # EURUSD
        'Dir_GBPUSD': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # GBPUSD
        'Dir_USDJPY': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # USDJPY
        'Dir_USDCHF': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # USDCHF
        'Dir_AUDUSD': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # AUDUSD
        'Dir_USDCAD': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # USDCAD
        'Dir_NZDUSD': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # NZDUSD
        'Dir_EURGBP': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # EURGBP
        'Dir_EURJPY': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # EURJPY
        'Dir_EURCHF': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # EURCHF
        'Dir_EURAUD': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # EURAUD
        'Dir_EURCAD': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # EURCAD
        'Dir_EURNZD': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # EURNZD
        'Dir_GBPJPY': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # GBPJPY
        'Dir_GBPCHF': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # GBPCHF
        'Dir_GBPAUD': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # GBPAUD
        'Dir_GBPCAD': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # GBPCAD
        'Dir_GBPNZD': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # GBPNZD
        'Dir_CHFJPY': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # CHFJPY
        'Dir_AUDJPY': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # AUDJPY
        'Dir_CADJPY': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # CADJPY
        'Dir_NZDJPY': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # NZDJPY
        'Dir_AUDCHF': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # AUDCHF
        'Dir_AUDCAD': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # AUDCAD
        'Dir_AUDNZD': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # AUDNZD
        'Dir_CADCHF': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # CADCHF
        'Dir_NZDCHF': _Choice({0: 'BUY', 1: 'SELL'}, default=1),  # NZDCHF
        'Dir_NZDCAD': _Choice({0: 'BUY', 1: 'SELL'}, default=0),  # NZDCAD
        'Enable_EURUSD': True,  # EURUSD
        'Enable_GBPUSD': False,  # GBPUSD
        'Enable_USDJPY': False,  # USDJPY
        'Enable_USDCHF': False,  # USDCHF
        'Enable_AUDUSD': False,  # AUDUSD
        'Enable_USDCAD': False,  # USDCAD
        'Enable_NZDUSD': False,  # NZDUSD
        'Enable_EURGBP': False,  # EURGBP
        'Enable_EURJPY': False,  # EURJPY
        'Enable_EURCHF': False,  # EURCHF
        'Enable_EURAUD': False,  # EURAUD
        'Enable_EURCAD': False,  # EURCAD
        'Enable_EURNZD': False,  # EURNZD
        'Enable_GBPJPY': False,  # GBPJPY
        'Enable_GBPCHF': False,  # GBPCHF
        'Enable_GBPAUD': False,  # GBPAUD
        'Enable_GBPCAD': False,  # GBPCAD
        'Enable_GBPNZD': False,  # GBPNZD
        'Enable_CHFJPY': False,  # CHFJPY
        'Enable_AUDJPY': False,  # AUDJPY
        'Enable_CADJPY': False,  # CADJPY
        'Enable_NZDJPY': False,  # NZDJPY
        'Enable_AUDCHF': False,  # AUDCHF
        'Enable_AUDCAD': False,  # AUDCAD
        'Enable_AUDNZD': False,  # AUDNZD
        'Enable_CADCHF': False,  # CADCHF
        'Enable_NZDCHF': False,  # NZDCHF
        'Enable_NZDCAD': False,  # NZDCAD
        'Bars_to_calculate': 1000,  # Drawing depth in bars (should be < available symbol history)
        'Initial_balance': 0.0,  # Initial virtual balance (optional)
        'InfoOutput': _Choice({0: 'Do not output', 1: 'Only to journal', 2: 'Only on chart', 3: 'To journal and chart'}, default=3),  # Information output mode
    }

