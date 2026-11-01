"""Pivot_Points_Lines_v1.3 — converted from MQL5: MQL5 Indicators/Pivot_Points_Lines_v1.3 MT5/Pivot_Points_Lines_v1.3.mq5

Copyright: Copyright 2021, NickBixy; Link: https://www.forexfactory.com/showthread.php?t=904734

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, NickBixy', 'link': 'https://www.forexfactory.com/showthread.php?t=904734', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Pivot_Points_Lines_v1.3', 'source': 'MQL5 Indicators/Pivot_Points_Lines_v1.3 MT5/Pivot_Points_Lines_v1.3.mq5', 'folder': 'Pivot_Points_Lines_v1.3 MT5', 'inputs': [{'mql': 'indiLink', 'py': 'indiLink', 'param': None, 'type': 'string', 'default': 'https://www.forexfactory.com/showthread.php?t=904734', 'label': "Indicator's Support Thread On Forex Factory", 'sinput': False}, {'mql': 'UniqueID', 'py': 'UniqueID', 'param': 'UniqueID', 'type': 'int', 'default': 1, 'label': 'Unique ID', 'sinput': False}, {'mql': 'historicalPP', 'py': 'historicalPP', 'param': 'historicalPP', 'type': 'int', 'default': 0, 'label': 'Historical Pivot Points,Set 0 for NONE', 'sinput': False}, {'mql': 'Header', 'py': 'Header', 'param': None, 'type': 'string', 'default': '----------------- Pivot Point Settings------------------------------------------', 'label': '----- Pivot Point Settings', 'sinput': False}, {'mql': 'pivotSelection', 'py': 'pivotSelection', 'param': 'pivotSelection', 'type': 'int', 'default': 0, 'label': 'Formula', 'sinput': False}, {'mql': 'timeFrame', 'py': 'timeFrame', 'param': 'timeFrame', 'type': 'int', 'default': 16408, 'label': 'TimeFrame', 'sinput': False}, {'mql': 'drawFuturePlot', 'py': 'drawFuturePlot', 'param': 'drawFuturePlot', 'type': 'int', 'default': 0, 'label': 'Draw Future Plot?', 'sinput': False}, {'mql': 'showPriceLabel', 'py': 'showPriceLabel', 'param': 'showPriceLabel', 'type': 'int', 'default': 0, 'label': 'Show Price In Label?', 'sinput': False}, {'mql': 'useShortLines', 'py': 'useShortLines', 'param': 'useShortLines', 'type': 'int', 'default': 0, 'label': 'Draw Short Lines For Current Period?', 'sinput': False}, {'mql': 'ShiftLabel', 'py': 'ShiftLabel', 'param': 'ShiftLabel', 'type': 'int', 'default': 3, 'label': 'Label Follow Price Shift -Move Left, +Move Right', 'sinput': False}, {'mql': 'Line_Length', 'py': 'Line_Length', 'param': 'Line_Length', 'type': 'int', 'default': 15, 'label': 'Length Of Short Line', 'sinput': False}, {'mql': 'HeaderStandardAdditionalSettings', 'py': 'HeaderStandardAdditionalSettings', 'param': None, 'type': 'string', 'default': '----------------- Standard(Floor) Additional Settings------------------------------------------', 'label': '----- Standard(Floor) Additional Settings', 'sinput': False}, {'mql': 'drawFloorMidPP', 'py': 'drawFloorMidPP', 'param': 'drawFloorMidPP', 'type': 'int', 'default': 0, 'label': 'Show Mid Pivot Points?', 'sinput': False}, {'mql': 'floorCPR', 'py': 'floorCPR', 'param': 'floorCPR', 'type': 'int', 'default': 1, 'label': 'Show Central Pivot Range?', 'sinput': False}, {'mql': 'Header2', 'py': 'Header2', 'param': None, 'type': 'string', 'default': '----------------- Line/Label Customize Settings------------------------------------------', 'label': '----- Line/Label Customize Settings', 'sinput': False}, {'mql': 'customMSG', 'py': 'customMSG', 'param': None, 'type': 'string', 'default': '', 'label': 'MSG Before Pivot Point Name', 'sinput': False}, {'mql': 'lineStyle', 'py': 'lineStyle', 'param': 'lineStyle', 'type': 'int', 'default': 0, 'label': 'Line Style', 'sinput': False}, {'mql': 'lineWidth', 'py': 'lineWidth', 'param': 'lineWidth', 'type': 'int', 'default': 1, 'label': 'Line Width', 'sinput': False}, {'mql': 'Font', 'py': 'Font', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Label Font', 'sinput': False}, {'mql': 'labelFontSize', 'py': 'labelFontSize', 'param': 'labelFontSize', 'type': 'int', 'default': 8, 'label': 'Label Text Size', 'sinput': False}, {'mql': 'historicalLabelLocation', 'py': 'historicalLabelLocation', 'param': 'historicalLabelLocation', 'type': 'int', 'default': 0, 'label': 'Historical Label Location?', 'sinput': False}, {'mql': 'currentLabelLocation', 'py': 'currentLabelLocation', 'param': 'currentLabelLocation', 'type': 'int', 'default': 0, 'label': 'Current Label Location?', 'sinput': False}, {'mql': 'futureLabelLocation', 'py': 'futureLabelLocation', 'param': 'futureLabelLocation', 'type': 'int', 'default': 2, 'label': 'Future Label Location?', 'sinput': False}, {'mql': 'hideHistoricalLabels', 'py': 'hideHistoricalLabels', 'param': 'hideHistoricalLabels', 'type': 'int', 'default': 0, 'label': 'Hide Historical Pivot Points Labels?', 'sinput': False}, {'mql': 'hideCurrentLabels', 'py': 'hideCurrentLabels', 'param': 'hideCurrentLabels', 'type': 'int', 'default': 0, 'label': 'Hide Current Pivot Points Labels?', 'sinput': False}, {'mql': 'hideFutureLabels', 'py': 'hideFutureLabels', 'param': 'hideFutureLabels', 'type': 'int', 'default': 0, 'label': 'Hide Future Pivot Points Labels?', 'sinput': False}, {'mql': 'useSameColorLabelChoice', 'py': 'useSameColorLabelChoice', 'param': 'useSameColorLabelChoice', 'type': 'int', 'default': 1, 'label': 'Label Use Same Color?', 'sinput': False}, {'mql': 'useSameColorLabelColor', 'py': 'useSameColorLabelColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'Label Color For Label Use Same Color', 'sinput': False}, {'mql': 'resistantColor', 'py': 'resistantColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Resistant Line/Label Color', 'sinput': False}, {'mql': 'pivotColor', 'py': 'pivotColor', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Pivot Line/Label Color', 'sinput': False}, {'mql': 'supportColor', 'py': 'supportColor', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Support Line/Label Color', 'sinput': False}, {'mql': 'midColor', 'py': 'midColor', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Standard(Floor)Mid PP Line/Label Color', 'sinput': False}, {'mql': 'CPRColor', 'py': 'CPRColor', 'param': None, 'type': 'color', 'default': 15631086, 'label': 'Standard(Floor)CPR PP Line/Label Color', 'sinput': False}, {'mql': 'showHeader', 'py': 'showHeader', 'param': None, 'type': 'string', 'default': '-----------------Enable/Disable Specified Pivot Point----------------------------------------------', 'label': '----- Enable/Disable Specified Pivot Point', 'sinput': False}, {'mql': 'showStandardPivotHeader', 'py': 'showStandardPivotHeader', 'param': None, 'type': 'string', 'default': 'Standard(Floor) Pivot Point--------------------------------------------', 'label': '----- Standard(Floor) Pivot Point Settings', 'sinput': False}, {'mql': 'showStandardPivotR4', 'py': 'showStandardPivotR4', 'param': 'showStandardPivotR4', 'type': 'int', 'default': 1, 'label': 'Standard Pivot R4', 'sinput': False}, {'mql': 'showStandardPivotR3', 'py': 'showStandardPivotR3', 'param': 'showStandardPivotR3', 'type': 'int', 'default': 1, 'label': 'Standard Pivot R3', 'sinput': False}, {'mql': 'showStandardPivotR2', 'py': 'showStandardPivotR2', 'param': 'showStandardPivotR2', 'type': 'int', 'default': 1, 'label': 'Standard Pivot R2', 'sinput': False}, {'mql': 'showStandardPivotR1', 'py': 'showStandardPivotR1', 'param': 'showStandardPivotR1', 'type': 'int', 'default': 1, 'label': 'Standard Pivot R1', 'sinput': False}, {'mql': 'showStandardPivotPP', 'py': 'showStandardPivotPP', 'param': 'showStandardPivotPP', 'type': 'int', 'default': 1, 'label': 'Standard Pivot PP', 'sinput': False}, {'mql': 'showStandardPivotS1', 'py': 'showStandardPivotS1', 'param': 'showStandardPivotS1', 'type': 'int', 'default': 1, 'label': 'Standard Pivot S1', 'sinput': False}, {'mql': 'showStandardPivotS2', 'py': 'showStandardPivotS2', 'param': 'showStandardPivotS2', 'type': 'int', 'default': 1, 'label': 'Standard Pivot S2', 'sinput': False}, {'mql': 'showStandardPivotS3', 'py': 'showStandardPivotS3', 'param': 'showStandardPivotS3', 'type': 'int', 'default': 1, 'label': 'Standard Pivot S3', 'sinput': False}, {'mql': 'showStandardPivotS4', 'py': 'showStandardPivotS4', 'param': 'showStandardPivotS4', 'type': 'int', 'default': 1, 'label': 'Standard Pivot S4', 'sinput': False}, {'mql': 'StandardMidPivotHeader', 'py': 'StandardMidPivotHeader', 'param': None, 'type': 'string', 'default': '-----------------Standard(Floor) Mid Pivot Points', 'label': '----- Standard(Floor) Mid PP', 'sinput': False}, {'mql': 'showStandardPivotMR4', 'py': 'showStandardPivotMR4', 'param': 'showStandardPivotMR4', 'type': 'int', 'default': 1, 'label': 'Standard Pivot MR4', 'sinput': False}, {'mql': 'showStandardPivotMR3', 'py': 'showStandardPivotMR3', 'param': 'showStandardPivotMR3', 'type': 'int', 'default': 1, 'label': 'Standard Pivot MR3', 'sinput': False}, {'mql': 'showStandardPivotMR2', 'py': 'showStandardPivotMR2', 'param': 'showStandardPivotMR2', 'type': 'int', 'default': 1, 'label': 'Standard Pivot MR2', 'sinput': False}, {'mql': 'showStandardPivotMR1', 'py': 'showStandardPivotMR1', 'param': 'showStandardPivotMR1', 'type': 'int', 'default': 1, 'label': 'Standard Pivot MR1', 'sinput': False}, {'mql': 'showStandardPivotMS1', 'py': 'showStandardPivotMS1', 'param': 'showStandardPivotMS1', 'type': 'int', 'default': 1, 'label': 'Standard Pivot MS1', 'sinput': False}, {'mql': 'showStandardPivotMS2', 'py': 'showStandardPivotMS2', 'param': 'showStandardPivotMS2', 'type': 'int', 'default': 1, 'label': 'Standard Pivot MS2', 'sinput': False}, {'mql': 'showStandardPivotMS3', 'py': 'showStandardPivotMS3', 'param': 'showStandardPivotMS3', 'type': 'int', 'default': 1, 'label': 'Standard Pivot MS3', 'sinput': False}, {'mql': 'showStandardPivotMS4', 'py': 'showStandardPivotMS4', 'param': 'showStandardPivotMS4', 'type': 'int', 'default': 1, 'label': 'Standard Pivot MS4', 'sinput': False}, {'mql': 'showCPRPivotHeader', 'py': 'showCPRPivotHeader', 'param': None, 'type': 'string', 'default': 'Standard(Floor) CPR Pivot Point--------------------------------------------', 'label': '----- Standard(Floor) CPR Pivot Point', 'sinput': False}, {'mql': 'showCPRTC', 'py': 'showCPRTC', 'param': 'showCPRTC', 'type': 'int', 'default': 1, 'label': 'Standard CPR Pivot TC', 'sinput': False}, {'mql': 'showCPRBC', 'py': 'showCPRBC', 'param': 'showCPRBC', 'type': 'int', 'default': 1, 'label': 'Standard CPR Pivot BC', 'sinput': False}, {'mql': 'showFibonacciPivotHeader', 'py': 'showFibonacciPivotHeader', 'param': None, 'type': 'string', 'default': 'Fibonacci Pivot Point--------------------------------------------', 'label': '----- Fibonacci Pivot Point Settings', 'sinput': False}, {'mql': 'showFibonacciPivotR200', 'py': 'showFibonacciPivotR200', 'param': 'showFibonacciPivotR200', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R200', 'sinput': False}, {'mql': 'showFibonacciPivotR161', 'py': 'showFibonacciPivotR161', 'param': 'showFibonacciPivotR161', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R161', 'sinput': False}, {'mql': 'showFibonacciPivotR138', 'py': 'showFibonacciPivotR138', 'param': 'showFibonacciPivotR138', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R138', 'sinput': False}, {'mql': 'showFibonacciPivotR100', 'py': 'showFibonacciPivotR100', 'param': 'showFibonacciPivotR100', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R100', 'sinput': False}, {'mql': 'showFibonacciPivotR78', 'py': 'showFibonacciPivotR78', 'param': 'showFibonacciPivotR78', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R78', 'sinput': False}, {'mql': 'showFibonacciPivotR61', 'py': 'showFibonacciPivotR61', 'param': 'showFibonacciPivotR61', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R61', 'sinput': False}, {'mql': 'showFibonacciPivotR38', 'py': 'showFibonacciPivotR38', 'param': 'showFibonacciPivotR38', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R38', 'sinput': False}, {'mql': 'showFibonacciPivotPP', 'py': 'showFibonacciPivotPP', 'param': 'showFibonacciPivotPP', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot PP', 'sinput': False}, {'mql': 'showFibonacciPivotS38', 'py': 'showFibonacciPivotS38', 'param': 'showFibonacciPivotS38', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S38', 'sinput': False}, {'mql': 'showFibonacciPivotS61', 'py': 'showFibonacciPivotS61', 'param': 'showFibonacciPivotS61', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S61', 'sinput': False}, {'mql': 'showFibonacciPivotS78', 'py': 'showFibonacciPivotS78', 'param': 'showFibonacciPivotS78', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S78', 'sinput': False}, {'mql': 'showFibonacciPivotS100', 'py': 'showFibonacciPivotS100', 'param': 'showFibonacciPivotS100', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S100', 'sinput': False}, {'mql': 'showFibonacciPivotS138', 'py': 'showFibonacciPivotS138', 'param': 'showFibonacciPivotS138', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S138', 'sinput': False}, {'mql': 'showFibonacciPivotS161', 'py': 'showFibonacciPivotS161', 'param': 'showFibonacciPivotS161', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S161', 'sinput': False}, {'mql': 'showFibonacciPivotS200', 'py': 'showFibonacciPivotS200', 'param': 'showFibonacciPivotS200', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S200', 'sinput': False}, {'mql': 'showWoodiePivotHeader', 'py': 'showWoodiePivotHeader', 'param': None, 'type': 'string', 'default': 'Woodie Pivot Point--------------------------------------------', 'label': '----- Woodie Pivot Point Settings', 'sinput': False}, {'mql': 'showWoodieR4', 'py': 'showWoodieR4', 'param': 'showWoodieR4', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot R4', 'sinput': False}, {'mql': 'showWoodieR3', 'py': 'showWoodieR3', 'param': 'showWoodieR3', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot R3', 'sinput': False}, {'mql': 'showWoodieR2', 'py': 'showWoodieR2', 'param': 'showWoodieR2', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot R2', 'sinput': False}, {'mql': 'showWoodieR1', 'py': 'showWoodieR1', 'param': 'showWoodieR1', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot R1', 'sinput': False}, {'mql': 'showWoodiePP', 'py': 'showWoodiePP', 'param': 'showWoodiePP', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot PP', 'sinput': False}, {'mql': 'showWoodieS1', 'py': 'showWoodieS1', 'param': 'showWoodieS1', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot S1', 'sinput': False}, {'mql': 'showWoodieS2', 'py': 'showWoodieS2', 'param': 'showWoodieS2', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot S2', 'sinput': False}, {'mql': 'showWoodieS3', 'py': 'showWoodieS3', 'param': 'showWoodieS3', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot S3', 'sinput': False}, {'mql': 'showWoodieS4', 'py': 'showWoodieS4', 'param': 'showWoodieS4', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot S4', 'sinput': False}, {'mql': 'showCamarillaPivotHeader', 'py': 'showCamarillaPivotHeader', 'param': None, 'type': 'string', 'default': 'Camarilla Pivot Point--------------------------------------------', 'label': '----- Camarilla Pivot Point Settings', 'sinput': False}, {'mql': 'showCamarillaH5', 'py': 'showCamarillaH5', 'param': 'showCamarillaH5', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot H5', 'sinput': False}, {'mql': 'showCamarillaH4', 'py': 'showCamarillaH4', 'param': 'showCamarillaH4', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot H4', 'sinput': False}, {'mql': 'showCamarillaH3', 'py': 'showCamarillaH3', 'param': 'showCamarillaH3', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot H3', 'sinput': False}, {'mql': 'showCamarillaH2', 'py': 'showCamarillaH2', 'param': 'showCamarillaH2', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot H2', 'sinput': False}, {'mql': 'showCamarillaH1', 'py': 'showCamarillaH1', 'param': 'showCamarillaH1', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot H1', 'sinput': False}, {'mql': 'showCamarillaPP', 'py': 'showCamarillaPP', 'param': 'showCamarillaPP', 'type': 'int', 'default': 0, 'label': 'Camarilla Pivot PP', 'sinput': False}, {'mql': 'showCamarillaL1', 'py': 'showCamarillaL1', 'param': 'showCamarillaL1', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot L1', 'sinput': False}, {'mql': 'showCamarillaL2', 'py': 'showCamarillaL2', 'param': 'showCamarillaL2', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot L2', 'sinput': False}, {'mql': 'showCamarillaL3', 'py': 'showCamarillaL3', 'param': 'showCamarillaL3', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot L3', 'sinput': False}, {'mql': 'showCamarillaL4', 'py': 'showCamarillaL4', 'param': 'showCamarillaL4', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot L4', 'sinput': False}, {'mql': 'showCamarillaL5', 'py': 'showCamarillaL5', 'param': 'showCamarillaL5', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot L5', 'sinput': False}, {'mql': 'showTraditionalPivotHeader', 'py': 'showTraditionalPivotHeader', 'param': None, 'type': 'string', 'default': 'Traditional Pivot Point--------------------------------------------', 'label': '----- Traditional Pivot Point Settings', 'sinput': False}, {'mql': 'showTraditionalR5', 'py': 'showTraditionalR5', 'param': 'showTraditionalR5', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot R5', 'sinput': False}, {'mql': 'showTraditionalR4', 'py': 'showTraditionalR4', 'param': 'showTraditionalR4', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot R4', 'sinput': False}, {'mql': 'showTraditionalR3', 'py': 'showTraditionalR3', 'param': 'showTraditionalR3', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot R3', 'sinput': False}, {'mql': 'showTraditionalR2', 'py': 'showTraditionalR2', 'param': 'showTraditionalR2', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot R2', 'sinput': False}, {'mql': 'showTraditionalR1', 'py': 'showTraditionalR1', 'param': 'showTraditionalR1', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot R1', 'sinput': False}, {'mql': 'showTraditionalPP', 'py': 'showTraditionalPP', 'param': 'showTraditionalPP', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot PP', 'sinput': False}, {'mql': 'showTraditionalS1', 'py': 'showTraditionalS1', 'param': 'showTraditionalS1', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot S1', 'sinput': False}, {'mql': 'showTraditionalS2', 'py': 'showTraditionalS2', 'param': 'showTraditionalS2', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot S2', 'sinput': False}, {'mql': 'showTraditionalS3', 'py': 'showTraditionalS3', 'param': 'showTraditionalS3', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot S3', 'sinput': False}, {'mql': 'showTraditionalS4', 'py': 'showTraditionalS4', 'param': 'showTraditionalS4', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot S4', 'sinput': False}, {'mql': 'showTraditionalS5', 'py': 'showTraditionalS5', 'param': 'showTraditionalS5', 'type': 'int', 'default': 1, 'label': 'Traditional Pivot S5', 'sinput': False}, {'mql': 'showDemarkPivotHeader', 'py': 'showDemarkPivotHeader', 'param': None, 'type': 'string', 'default': 'Demark Pivot Point--------------------------------------------', 'label': '----- Demark Pivot Point Settings', 'sinput': False}, {'mql': 'showDemarkR1', 'py': 'showDemarkR1', 'param': 'showDemarkR1', 'type': 'int', 'default': 1, 'label': 'Demark Pivot R1', 'sinput': False}, {'mql': 'showDemarkPP', 'py': 'showDemarkPP', 'param': 'showDemarkPP', 'type': 'int', 'default': 1, 'label': 'Demark Pivot PP', 'sinput': False}, {'mql': 'showDemarkS1', 'py': 'showDemarkS1', 'param': 'showDemarkS1', 'type': 'int', 'default': 1, 'label': 'Demark Pivot S1', 'sinput': False}, {'mql': 'showClassicPivotHeader', 'py': 'showClassicPivotHeader', 'param': None, 'type': 'string', 'default': 'Classic Pivot Point--------------------------------------------', 'label': '----- Classic Pivot Point Settings', 'sinput': False}, {'mql': 'showClassicR4', 'py': 'showClassicR4', 'param': 'showClassicR4', 'type': 'int', 'default': 1, 'label': 'Classic Pivot R4', 'sinput': False}, {'mql': 'showClassicR3', 'py': 'showClassicR3', 'param': 'showClassicR3', 'type': 'int', 'default': 1, 'label': 'Classic Pivot R3', 'sinput': False}, {'mql': 'showClassicR2', 'py': 'showClassicR2', 'param': 'showClassicR2', 'type': 'int', 'default': 1, 'label': 'Classic Pivot R2', 'sinput': False}, {'mql': 'showClassicR1', 'py': 'showClassicR1', 'param': 'showClassicR1', 'type': 'int', 'default': 1, 'label': 'Classic Pivot R1', 'sinput': False}, {'mql': 'showClassicPP', 'py': 'showClassicPP', 'param': 'showClassicPP', 'type': 'int', 'default': 1, 'label': 'Classic Pivot PP', 'sinput': False}, {'mql': 'showClassicS1', 'py': 'showClassicS1', 'param': 'showClassicS1', 'type': 'int', 'default': 1, 'label': 'Classic Pivot S1', 'sinput': False}, {'mql': 'showClassicS2', 'py': 'showClassicS2', 'param': 'showClassicS2', 'type': 'int', 'default': 1, 'label': 'Classic Pivot S2', 'sinput': False}, {'mql': 'showClassicS3', 'py': 'showClassicS3', 'param': 'showClassicS3', 'type': 'int', 'default': 1, 'label': 'Classic Pivot S3', 'sinput': False}, {'mql': 'showClassicS4', 'py': 'showClassicS4', 'param': 'showClassicS4', 'type': 'int', 'default': 1, 'label': 'Classic Pivot S4', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum pivotTypes
Standard = 0
Fibonacci = 1
Camarilla = 2
Woodie = 3
Traditional = 4
Demark = 5
Classic = 6
_enum('pivotTypes', {0: 'Standard', 1: 'Fibonacci', 2: 'Camarilla', 3: 'Woodie', 4: 'Traditional', 5: 'Demark', 6: 'Classic'})

# enum yesnoChoiceToggle
No = 0
Yes = 1
_enum('yesnoChoiceToggle', {0: 'No', 1: 'Yes'})

# enum enabledisableChoiceToggle
Disable = 0
Enable = 1
_enum('enabledisableChoiceToggle', {0: 'Disable', 1: 'Enable'})

# enum labelLocation1
Left_1 = 0
Middle_1 = 1
Right_1 = 2
_enum('labelLocation1', {0: 'Left_1', 1: 'Middle_1', 2: 'Right_1'})

# enum labelLocation2
Follow_Price_2 = 0
Left_2 = 1
Middle_2 = 2
Right_2 = 3
_enum('labelLocation2', {0: 'Follow_Price_2', 1: 'Left_2', 2: 'Middle_2', 3: 'Right_2'})

# ---- inputs and global variables
indiLink = _input('indiLink', 'https://www.forexfactory.com/showthread.php?t=904734')  # Indicator's Support Thread On Forex Factory
UniqueID = _input('UniqueID', 1)  # Unique ID
historicalPP = _input('historicalPP', 0)  # Historical Pivot Points,Set 0 for NONE
Header = _input('Header', '----------------- Pivot Point Settings------------------------------------------')  # ----- Pivot Point Settings
pivotSelection = _input('pivotSelection', Standard)  # Formula
timeFrame = _input('timeFrame', PERIOD_D1)  # TimeFrame
drawFuturePlot = _input('drawFuturePlot', No)  # Draw Future Plot?
showPriceLabel = _input('showPriceLabel', No)  # Show Price In Label?
useShortLines = _input('useShortLines', No)  # Draw Short Lines For Current Period?
ShiftLabel = _input('ShiftLabel', 3)  # Label Follow Price Shift -Move Left, +Move Right
Line_Length = _input('Line_Length', 15)  # Length Of Short Line
HeaderStandardAdditionalSettings = _input('HeaderStandardAdditionalSettings', '----------------- Standard(Floor) Additional Settings------------------------------------------')  # ----- Standard(Floor) Additional Settings
drawFloorMidPP = _input('drawFloorMidPP', No)  # Show Mid Pivot Points?
floorCPR = _input('floorCPR', Yes)  # Show Central Pivot Range?
Header2 = _input('Header2', '----------------- Line/Label Customize Settings------------------------------------------')  # ----- Line/Label Customize Settings
customMSG = _input('customMSG', '')  # MSG Before Pivot Point Name
lineStyle = _input('lineStyle', STYLE_SOLID)  # Line Style
lineWidth = _input('lineWidth', 1)  # Line Width
Font = _input('Font', 'Arial')  # Label Font
labelFontSize = _input('labelFontSize', 8)  # Label Text Size
historicalLabelLocation = _input('historicalLabelLocation', Left_1)  # Historical Label Location?
currentLabelLocation = _input('currentLabelLocation', Follow_Price_2)  # Current Label Location?
futureLabelLocation = _input('futureLabelLocation', Right_1)  # Future Label Location?
hideHistoricalLabels = _input('hideHistoricalLabels', No)  # Hide Historical Pivot Points Labels?
hideCurrentLabels = _input('hideCurrentLabels', No)  # Hide Current Pivot Points Labels?
hideFutureLabels = _input('hideFutureLabels', No)  # Hide Future Pivot Points Labels?
useSameColorLabelChoice = _input('useSameColorLabelChoice', Yes)  # Label Use Same Color?
useSameColorLabelColor = _input('useSameColorLabelColor', clrWhite)  # Label Color For Label Use Same Color
resistantColor = _input('resistantColor', clrRed)  # Resistant Line/Label Color
pivotColor = _input('pivotColor', clrYellow)  # Pivot Line/Label Color
supportColor = _input('supportColor', clrLime)  # Support Line/Label Color
midColor = _input('midColor', clrGreen)  # Standard(Floor)Mid PP Line/Label Color
CPRColor = _input('CPRColor', clrViolet)  # Standard(Floor)CPR PP Line/Label Color
camarillaPivotNames = Arr.of(['PP', 'L1', 'L2', 'L3', 'L4', 'H1', 'H2', 'H3', 'H4', 'H5', 'L5'], fill="")
camarillaValueArray = Arr(11, 0.0, dyn=False)
showCamarilla = Arr(11, False, dyn=False)
standardPivotNames = Arr.of(['PP', 'S1', 'S2', 'S3', 'R1', 'R2', 'R3', 'R4', 'S4', 'MR4', 'MR3', 'MR2', 'MR1', 'MS1', 'MS2', 'MS3', 'MS4'], fill="")
standardValueArray = Arr(17, 0.0, dyn=False)
showStandard = Arr(17, False, dyn=False)
traditionalPivotNames = Arr.of(['PP', 'S1', 'S2', 'S3', 'R1', 'R2', 'R3', 'R4', 'S4', 'S5', 'R5'], fill="")
traditionalValueArray = Arr(11, 0.0, dyn=False)
showTraditional = Arr(11, False, dyn=False)
demarkPivotNames = Arr.of(['PP', 'R1', 'S1'], fill="")
demarkValueArray = Arr(3, 0.0, dyn=False)
showDemark = Arr(3, False, dyn=False)
woodiePivotNames = Arr.of(['PP', 'S1', 'S2', 'R1', 'R2', 'S3', 'S4', 'R3', 'R4'], fill="")
woodieValueArray = Arr(9, 0.0, dyn=False)
showWoodie = Arr(9, False, dyn=False)
fibonacciPivotNames = Arr.of(['PP', 'R38', 'R61', 'R78', 'R100', 'R138', 'R161', 'R200', 'S38', 'S61', 'S78', 'S100', 'S138', 'S161', 'S200'], fill="")
fibonacciValueArray = Arr(15, 0.0, dyn=False)
showFibonacci = Arr(15, False, dyn=False)
classicPivotNames = Arr.of(['PP', 'S1', 'S2', 'S3', 'S4', 'R1', 'R2', 'R3', 'R4'], fill="")
classicValueArray = Arr(9, 0.0, dyn=False)
showClassic = Arr(9, False, dyn=False)
floorCPRPivotNames = Arr.of(['BC', 'TC'], fill="")
floorCPRValueArray = Arr(2, 0.0, dyn=False)
showFloorCPR = Arr(2, False, dyn=False)
showHeader = _input('showHeader', '-----------------Enable/Disable Specified Pivot Point----------------------------------------------')  # ----- Enable/Disable Specified Pivot Point
showStandardPivotHeader = _input('showStandardPivotHeader', 'Standard(Floor) Pivot Point--------------------------------------------')  # ----- Standard(Floor) Pivot Point Settings
showStandardPivotR4 = _input('showStandardPivotR4', Enable)  # Standard Pivot R4
showStandardPivotR3 = _input('showStandardPivotR3', Enable)  # Standard Pivot R3
showStandardPivotR2 = _input('showStandardPivotR2', Enable)  # Standard Pivot R2
showStandardPivotR1 = _input('showStandardPivotR1', Enable)  # Standard Pivot R1
showStandardPivotPP = _input('showStandardPivotPP', Enable)  # Standard Pivot PP
showStandardPivotS1 = _input('showStandardPivotS1', Enable)  # Standard Pivot S1
showStandardPivotS2 = _input('showStandardPivotS2', Enable)  # Standard Pivot S2
showStandardPivotS3 = _input('showStandardPivotS3', Enable)  # Standard Pivot S3
showStandardPivotS4 = _input('showStandardPivotS4', Enable)  # Standard Pivot S4
StandardMidPivotHeader = _input('StandardMidPivotHeader', '-----------------Standard(Floor) Mid Pivot Points')  # ----- Standard(Floor) Mid PP
showStandardPivotMR4 = _input('showStandardPivotMR4', Enable)  # Standard Pivot MR4
showStandardPivotMR3 = _input('showStandardPivotMR3', Enable)  # Standard Pivot MR3
showStandardPivotMR2 = _input('showStandardPivotMR2', Enable)  # Standard Pivot MR2
showStandardPivotMR1 = _input('showStandardPivotMR1', Enable)  # Standard Pivot MR1
showStandardPivotMS1 = _input('showStandardPivotMS1', Enable)  # Standard Pivot MS1
showStandardPivotMS2 = _input('showStandardPivotMS2', Enable)  # Standard Pivot MS2
showStandardPivotMS3 = _input('showStandardPivotMS3', Enable)  # Standard Pivot MS3
showStandardPivotMS4 = _input('showStandardPivotMS4', Enable)  # Standard Pivot MS4
showCPRPivotHeader = _input('showCPRPivotHeader', 'Standard(Floor) CPR Pivot Point--------------------------------------------')  # ----- Standard(Floor) CPR Pivot Point
showCPRTC = _input('showCPRTC', Enable)  # Standard CPR Pivot TC
showCPRBC = _input('showCPRBC', Enable)  # Standard CPR Pivot BC
showFibonacciPivotHeader = _input('showFibonacciPivotHeader', 'Fibonacci Pivot Point--------------------------------------------')  # ----- Fibonacci Pivot Point Settings
showFibonacciPivotR200 = _input('showFibonacciPivotR200', Enable)  # Fibonacci Pivot R200
showFibonacciPivotR161 = _input('showFibonacciPivotR161', Enable)  # Fibonacci Pivot R161
showFibonacciPivotR138 = _input('showFibonacciPivotR138', Enable)  # Fibonacci Pivot R138
showFibonacciPivotR100 = _input('showFibonacciPivotR100', Enable)  # Fibonacci Pivot R100
showFibonacciPivotR78 = _input('showFibonacciPivotR78', Enable)  # Fibonacci Pivot R78
showFibonacciPivotR61 = _input('showFibonacciPivotR61', Enable)  # Fibonacci Pivot R61
showFibonacciPivotR38 = _input('showFibonacciPivotR38', Enable)  # Fibonacci Pivot R38
showFibonacciPivotPP = _input('showFibonacciPivotPP', Enable)  # Fibonacci Pivot PP
showFibonacciPivotS38 = _input('showFibonacciPivotS38', Enable)  # Fibonacci Pivot S38
showFibonacciPivotS61 = _input('showFibonacciPivotS61', Enable)  # Fibonacci Pivot S61
showFibonacciPivotS78 = _input('showFibonacciPivotS78', Enable)  # Fibonacci Pivot S78
showFibonacciPivotS100 = _input('showFibonacciPivotS100', Enable)  # Fibonacci Pivot S100
showFibonacciPivotS138 = _input('showFibonacciPivotS138', Enable)  # Fibonacci Pivot S138
showFibonacciPivotS161 = _input('showFibonacciPivotS161', Enable)  # Fibonacci Pivot S161
showFibonacciPivotS200 = _input('showFibonacciPivotS200', Enable)  # Fibonacci Pivot S200
showWoodiePivotHeader = _input('showWoodiePivotHeader', 'Woodie Pivot Point--------------------------------------------')  # ----- Woodie Pivot Point Settings
showWoodieR4 = _input('showWoodieR4', Enable)  # Woodie Pivot R4
showWoodieR3 = _input('showWoodieR3', Enable)  # Woodie Pivot R3
showWoodieR2 = _input('showWoodieR2', Enable)  # Woodie Pivot R2
showWoodieR1 = _input('showWoodieR1', Enable)  # Woodie Pivot R1
showWoodiePP = _input('showWoodiePP', Enable)  # Woodie Pivot PP
showWoodieS1 = _input('showWoodieS1', Enable)  # Woodie Pivot S1
showWoodieS2 = _input('showWoodieS2', Enable)  # Woodie Pivot S2
showWoodieS3 = _input('showWoodieS3', Enable)  # Woodie Pivot S3
showWoodieS4 = _input('showWoodieS4', Enable)  # Woodie Pivot S4
showCamarillaPivotHeader = _input('showCamarillaPivotHeader', 'Camarilla Pivot Point--------------------------------------------')  # ----- Camarilla Pivot Point Settings
showCamarillaH5 = _input('showCamarillaH5', Enable)  # Camarilla Pivot H5
showCamarillaH4 = _input('showCamarillaH4', Enable)  # Camarilla Pivot H4
showCamarillaH3 = _input('showCamarillaH3', Enable)  # Camarilla Pivot H3
showCamarillaH2 = _input('showCamarillaH2', Enable)  # Camarilla Pivot H2
showCamarillaH1 = _input('showCamarillaH1', Enable)  # Camarilla Pivot H1
showCamarillaPP = _input('showCamarillaPP', Disable)  # Camarilla Pivot PP
showCamarillaL1 = _input('showCamarillaL1', Enable)  # Camarilla Pivot L1
showCamarillaL2 = _input('showCamarillaL2', Enable)  # Camarilla Pivot L2
showCamarillaL3 = _input('showCamarillaL3', Enable)  # Camarilla Pivot L3
showCamarillaL4 = _input('showCamarillaL4', Enable)  # Camarilla Pivot L4
showCamarillaL5 = _input('showCamarillaL5', Enable)  # Camarilla Pivot L5
showTraditionalPivotHeader = _input('showTraditionalPivotHeader', 'Traditional Pivot Point--------------------------------------------')  # ----- Traditional Pivot Point Settings
showTraditionalR5 = _input('showTraditionalR5', Enable)  # Traditional Pivot R5
showTraditionalR4 = _input('showTraditionalR4', Enable)  # Traditional Pivot R4
showTraditionalR3 = _input('showTraditionalR3', Enable)  # Traditional Pivot R3
showTraditionalR2 = _input('showTraditionalR2', Enable)  # Traditional Pivot R2
showTraditionalR1 = _input('showTraditionalR1', Enable)  # Traditional Pivot R1
showTraditionalPP = _input('showTraditionalPP', Enable)  # Traditional Pivot PP
showTraditionalS1 = _input('showTraditionalS1', Enable)  # Traditional Pivot S1
showTraditionalS2 = _input('showTraditionalS2', Enable)  # Traditional Pivot S2
showTraditionalS3 = _input('showTraditionalS3', Enable)  # Traditional Pivot S3
showTraditionalS4 = _input('showTraditionalS4', Enable)  # Traditional Pivot S4
showTraditionalS5 = _input('showTraditionalS5', Enable)  # Traditional Pivot S5
showDemarkPivotHeader = _input('showDemarkPivotHeader', 'Demark Pivot Point--------------------------------------------')  # ----- Demark Pivot Point Settings
showDemarkR1 = _input('showDemarkR1', Enable)  # Demark Pivot R1
showDemarkPP = _input('showDemarkPP', Enable)  # Demark Pivot PP
showDemarkS1 = _input('showDemarkS1', Enable)  # Demark Pivot S1
showClassicPivotHeader = _input('showClassicPivotHeader', 'Classic Pivot Point--------------------------------------------')  # ----- Classic Pivot Point Settings
showClassicR4 = _input('showClassicR4', Enable)  # Classic Pivot R4
showClassicR3 = _input('showClassicR3', Enable)  # Classic Pivot R3
showClassicR2 = _input('showClassicR2', Enable)  # Classic Pivot R2
showClassicR1 = _input('showClassicR1', Enable)  # Classic Pivot R1
showClassicPP = _input('showClassicPP', Enable)  # Classic Pivot PP
showClassicS1 = _input('showClassicS1', Enable)  # Classic Pivot S1
showClassicS2 = _input('showClassicS2', Enable)  # Classic Pivot S2
showClassicS3 = _input('showClassicS3', Enable)  # Classic Pivot S3
showClassicS4 = _input('showClassicS4', Enable)  # Classic Pivot S4

def OnInit():
    EnableDisablePivotPoint()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if (((((reason == 1 or reason == 2) or reason == 3) or reason == 4) or reason == 5) or reason == 7) or reason == 9:
        ObjectsDeleteAll(0, 'PPL' + _str(UniqueID), 0, OBJ_TREND)
        ObjectsDeleteAll(0, 'PPL' + _str(UniqueID), 0, OBJ_TEXT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if pivotSelection == Camarilla:
        camarillaPivotPoint(camarillaValueArray, 0, False)
        i = 0
        while i < ArraySize(camarillaValueArray):
            if showCamarilla[i]:
                DrawPivotLines(camarillaValueArray[i], camarillaPivotNames[i])
            i += 1
        numHistoricalPP = historicalPP
        if numHistoricalPP > 0:
            j = 1
            while j <= numHistoricalPP:
                if timeFrame == PERIOD_D1:
                    if foundWeekend(j):
                        numHistoricalPP += 1
                        j += 1
                        continue
                camarillaPivotPoint(camarillaValueArray, j, False)
                k = 0
                while k < ArraySize(camarillaValueArray):
                    if showCamarilla[k]:
                        DrawHistoricalLines(camarillaValueArray[k], camarillaPivotNames[k], j)
                    k += 1
                j += 1
        if drawFuturePlot == Yes:
            camarillaPivotPoint(camarillaValueArray, 0, True)
            k = 0
            while k < ArraySize(camarillaValueArray):
                if showCamarilla[k]:
                    DrawFuturePlot(camarillaValueArray[k], camarillaPivotNames[k])
                k += 1
    if pivotSelection == Standard:
        if drawFloorMidPP == Yes:
            standardPivotPoint(standardValueArray, 0, False)
            for i in range(0, 17):
                if showStandard[i]:
                    DrawPivotLines(standardValueArray[i], standardPivotNames[i])
            if floorCPR == Yes:
                standardPivotPointCPR(floorCPRValueArray, 0, False)
                k = 0
                while k < ArraySize(floorCPRValueArray):
                    if showFloorCPR[k]:
                        DrawCPRPivotLines(floorCPRValueArray[k], floorCPRPivotNames[k])
                    k += 1
            numHistoricalPP = historicalPP
            if numHistoricalPP > 0:
                j = 1
                while j <= numHistoricalPP:
                    if timeFrame == PERIOD_D1:
                        if foundWeekend(j):
                            numHistoricalPP += 1
                            j += 1
                            continue
                    standardPivotPoint(standardValueArray, j, False)
                    for k in range(0, 17):
                        if showStandard[k]:
                            DrawHistoricalLines(standardValueArray[k], standardPivotNames[k], j)
                    if floorCPR == Yes:
                        standardPivotPointCPR(floorCPRValueArray, j, False)
                        k = 0
                        while k < ArraySize(floorCPRValueArray):
                            if showFloorCPR[k]:
                                DrawCPRHistoricalLines(floorCPRValueArray[k], floorCPRPivotNames[k], j)
                            k += 1
                    j += 1
            if drawFuturePlot == Yes:
                standardPivotPoint(standardValueArray, 0, True)
                for k in range(0, 17):
                    if showStandard[k]:
                        DrawFuturePlot(standardValueArray[k], standardPivotNames[k])
                if floorCPR == Yes:
                    standardPivotPointCPR(floorCPRValueArray, 0, True)
                    k = 0
                    while k < ArraySize(floorCPRValueArray):
                        if showFloorCPR[k]:
                            DrawCPRFuturePlot(floorCPRValueArray[k], floorCPRPivotNames[k])
                        k += 1
        else:
            standardPivotPoint(standardValueArray, 0, False)
            for i in range(0, 9):
                if showStandard[i]:
                    DrawPivotLines(standardValueArray[i], standardPivotNames[i])
                if floorCPR == Yes:
                    standardPivotPointCPR(floorCPRValueArray, 0, False)
                    k = 0
                    while k < ArraySize(floorCPRValueArray):
                        if showFloorCPR[k]:
                            DrawCPRPivotLines(floorCPRValueArray[k], floorCPRPivotNames[k])
                        k += 1
            numHistoricalPP = historicalPP
            if numHistoricalPP > 0:
                j = 1
                while j <= numHistoricalPP:
                    if timeFrame == PERIOD_D1:
                        if foundWeekend(j):
                            numHistoricalPP += 1
                            j += 1
                            continue
                    standardPivotPoint(standardValueArray, j, False)
                    for k in range(0, 9):
                        if showStandard[k]:
                            DrawHistoricalLines(standardValueArray[k], standardPivotNames[k], j)
                    if floorCPR == Yes:
                        standardPivotPointCPR(floorCPRValueArray, j, False)
                        k = 0
                        while k < ArraySize(floorCPRValueArray):
                            if showFloorCPR[k]:
                                DrawCPRHistoricalLines(floorCPRValueArray[k], floorCPRPivotNames[k], j)
                            k += 1
                    j += 1
            if drawFuturePlot == Yes:
                standardPivotPoint(standardValueArray, 0, True)
                for k in range(0, 9):
                    if showStandard[k]:
                        DrawFuturePlot(standardValueArray[k], standardPivotNames[k])
                if floorCPR == Yes:
                    standardPivotPointCPR(floorCPRValueArray, 0, True)
                    k = 0
                    while k < ArraySize(floorCPRValueArray):
                        if showFloorCPR[k]:
                            DrawCPRFuturePlot(floorCPRValueArray[k], floorCPRPivotNames[k])
                        k += 1
    if pivotSelection == Fibonacci:
        fibonacciPivotPoint(fibonacciValueArray, 0, False)
        i = 0
        while i < ArraySize(fibonacciValueArray):
            if showFibonacci[i]:
                DrawPivotLines(fibonacciValueArray[i], fibonacciPivotNames[i])
            i += 1
        numHistoricalPP = historicalPP
        if numHistoricalPP > 0:
            j = 1
            while j <= numHistoricalPP:
                if timeFrame == PERIOD_D1:
                    if foundWeekend(j):
                        numHistoricalPP += 1
                        j += 1
                        continue
                fibonacciPivotPoint(fibonacciValueArray, j, False)
                k = 0
                while k < ArraySize(fibonacciValueArray):
                    if showFibonacci[k]:
                        DrawHistoricalLines(fibonacciValueArray[k], fibonacciPivotNames[k], j)
                    k += 1
                j += 1
        if drawFuturePlot == Yes:
            fibonacciPivotPoint(fibonacciValueArray, 0, True)
            k = 0
            while k < ArraySize(fibonacciValueArray):
                if showFibonacci[k]:
                    DrawFuturePlot(fibonacciValueArray[k], fibonacciPivotNames[k])
                k += 1
    if pivotSelection == Woodie:
        woodiePivotPoint(woodieValueArray, 0, False)
        i = 0
        while i < ArraySize(woodieValueArray):
            if showWoodie[i]:
                DrawPivotLines(woodieValueArray[i], woodiePivotNames[i])
            i += 1
        numHistoricalPP = historicalPP
        if numHistoricalPP > 0:
            j = 1
            while j <= numHistoricalPP:
                if timeFrame == PERIOD_D1:
                    if foundWeekend(j):
                        numHistoricalPP += 1
                        j += 1
                        continue
                woodiePivotPoint(woodieValueArray, j, False)
                k = 0
                while k < ArraySize(woodieValueArray):
                    if showWoodie[k]:
                        DrawHistoricalLines(woodieValueArray[k], woodiePivotNames[k], j)
                    k += 1
                j += 1
        if drawFuturePlot == Yes:
            woodiePivotPoint(woodieValueArray, 0, True)
            k = 0
            while k < ArraySize(woodieValueArray):
                if showWoodie[k]:
                    DrawFuturePlot(woodieValueArray[k], woodiePivotNames[k])
                k += 1
    if pivotSelection == Traditional:
        traditionalPivotPoint(traditionalValueArray, 0, False)
        i = 0
        while i < ArraySize(traditionalValueArray):
            if showTraditional[i]:
                DrawPivotLines(traditionalValueArray[i], traditionalPivotNames[i])
            i += 1
        numHistoricalPP = historicalPP
        if numHistoricalPP > 0:
            j = 1
            while j <= numHistoricalPP:
                if timeFrame == PERIOD_D1:
                    if foundWeekend(j):
                        numHistoricalPP += 1
                        j += 1
                        continue
                traditionalPivotPoint(traditionalValueArray, j, False)
                k = 0
                while k < ArraySize(traditionalValueArray):
                    if showTraditional[k]:
                        DrawHistoricalLines(traditionalValueArray[k], traditionalPivotNames[k], j)
                    k += 1
                j += 1
        if drawFuturePlot == Yes:
            traditionalPivotPoint(traditionalValueArray, 0, True)
            k = 0
            while k < ArraySize(traditionalValueArray):
                if showTraditional[k]:
                    DrawFuturePlot(traditionalValueArray[k], traditionalPivotNames[k])
                k += 1
    if pivotSelection == Demark:
        demarkPivotPoint(demarkValueArray, 0, False)
        i = 0
        while i < ArraySize(demarkValueArray):
            if showDemark[i]:
                DrawPivotLines(demarkValueArray[i], demarkPivotNames[i])
            i += 1
        numHistoricalPP = historicalPP
        if numHistoricalPP > 0:
            j = 1
            while j <= numHistoricalPP:
                if timeFrame == PERIOD_D1:
                    if foundWeekend(j):
                        numHistoricalPP += 1
                        j += 1
                        continue
                demarkPivotPoint(demarkValueArray, j, False)
                k = 0
                while k < ArraySize(demarkValueArray):
                    if showDemark[k]:
                        DrawHistoricalLines(demarkValueArray[k], demarkPivotNames[k], j)
                    k += 1
                j += 1
        if drawFuturePlot == Yes:
            demarkPivotPoint(demarkValueArray, 0, True)
            k = 0
            while k < ArraySize(demarkValueArray):
                if showDemark[k]:
                    DrawFuturePlot(demarkValueArray[k], demarkPivotNames[k])
                k += 1
    if pivotSelection == Classic:
        classicPivotPoint(classicValueArray, 0, False)
        i = 0
        while i < ArraySize(classicValueArray):
            if showClassic[i]:
                DrawPivotLines(classicValueArray[i], classicPivotNames[i])
            i += 1
        numHistoricalPP = historicalPP
        if numHistoricalPP > 0:
            j = 1
            while j <= numHistoricalPP:
                if timeFrame == PERIOD_D1:
                    if foundWeekend(j):
                        numHistoricalPP += 1
                        j += 1
                        continue
                classicPivotPoint(classicValueArray, j, False)
                k = 0
                while k < ArraySize(classicValueArray):
                    if showClassic[k]:
                        DrawHistoricalLines(classicValueArray[k], classicPivotNames[k], j)
                    k += 1
                j += 1
        if drawFuturePlot == Yes:
            classicPivotPoint(classicValueArray, 0, True)
            k = 0
            while k < ArraySize(classicValueArray):
                if showClassic[k]:
                    DrawFuturePlot(classicValueArray[k], classicPivotNames[k])
                k += 1
    return 0

def DrawPivotLines(value, pivotName):
    timeframeValueLabel = 0
    timeframeValueLine = 0
    if currentLabelLocation == Follow_Price_2 or useShortLines == Yes:
        _sw1 = Period()
        if _sw1 == PERIOD_M1:
            timeframeValueLabel = 1
        elif _sw1 == PERIOD_M2:
            timeframeValueLabel = 2
        elif _sw1 == PERIOD_M3:
            timeframeValueLabel = 3
        elif _sw1 == PERIOD_M4:
            timeframeValueLabel = 4
        elif _sw1 == PERIOD_M5:
            timeframeValueLabel = 5
        elif _sw1 == PERIOD_M6:
            timeframeValueLabel = 6
        elif _sw1 == PERIOD_M10:
            timeframeValueLabel = 10
        elif _sw1 == PERIOD_M12:
            timeframeValueLabel = 12
        elif _sw1 == PERIOD_M15:
            timeframeValueLabel = 15
        elif _sw1 == PERIOD_M20:
            timeframeValueLabel = 20
        elif _sw1 == PERIOD_M30:
            timeframeValueLabel = 30
        elif _sw1 == PERIOD_H1:
            timeframeValueLabel = 60
        elif _sw1 == PERIOD_H2:
            timeframeValueLabel = 240
        elif _sw1 == PERIOD_H3:
            timeframeValueLabel = 180
        elif _sw1 == PERIOD_H4:
            timeframeValueLabel = 240
        elif _sw1 == PERIOD_H6:
            timeframeValueLabel = 360
        elif _sw1 == PERIOD_H8:
            timeframeValueLabel = 480
        elif _sw1 == PERIOD_H12:
            timeframeValueLabel = 720
        elif _sw1 == PERIOD_D1:
            timeframeValueLabel = 1440
        elif _sw1 == PERIOD_W1:
            timeframeValueLabel = 10080
        elif _sw1 == PERIOD_MN1:
            timeframeValueLabel = 43200
    _sw2 = timeFrame
    if _sw2 == PERIOD_M1:
        timeframeValueLine = 1
    elif _sw2 == PERIOD_M2:
        timeframeValueLine = 2
    elif _sw2 == PERIOD_M3:
        timeframeValueLine = 3
    elif _sw2 == PERIOD_M4:
        timeframeValueLine = 4
    elif _sw2 == PERIOD_M5:
        timeframeValueLine = 5
    elif _sw2 == PERIOD_M6:
        timeframeValueLine = 6
    elif _sw2 == PERIOD_M10:
        timeframeValueLine = 10
    elif _sw2 == PERIOD_M12:
        timeframeValueLine = 12
    elif _sw2 == PERIOD_M15:
        timeframeValueLine = 15
    elif _sw2 == PERIOD_M20:
        timeframeValueLine = 20
    elif _sw2 == PERIOD_M30:
        timeframeValueLine = 30
    elif _sw2 == PERIOD_H1:
        timeframeValueLine = 60
    elif _sw2 == PERIOD_H2:
        timeframeValueLine = 240
    elif _sw2 == PERIOD_H3:
        timeframeValueLine = 180
    elif _sw2 == PERIOD_H4:
        timeframeValueLine = 240
    elif _sw2 == PERIOD_H6:
        timeframeValueLine = 360
    elif _sw2 == PERIOD_H8:
        timeframeValueLine = 480
    elif _sw2 == PERIOD_H12:
        timeframeValueLine = 720
    elif _sw2 == PERIOD_D1:
        timeframeValueLine = 1440
    elif _sw2 == PERIOD_W1:
        timeframeValueLine = 10080
    elif _sw2 == PERIOD_MN1:
        timeframeValueLine = 43200
    Time = Arr(0, 0)
    count = 2
    ArraySetAsSeries(Time, True)
    CopyTime(Symbol(), Period(), 0, count, Time)
    lineLabelColor = clrNONE
    message = ''
    if showPriceLabel == Yes:
        message = customMSG + pivotName + ': ' + DoubleToString(value, Digits())
    else:
        message = customMSG + pivotName
    if 82 == StringGetCharacter(pivotName, 0):
        lineLabelColor = resistantColor
    if 80 == StringGetCharacter(pivotName, 0):
        lineLabelColor = pivotColor
    if 83 == StringGetCharacter(pivotName, 0):
        lineLabelColor = supportColor
    if 77 == StringGetCharacter(pivotName, 0):
        lineLabelColor = midColor
    if 72 == StringGetCharacter(pivotName, 0):
        lineLabelColor = resistantColor
    if 76 == StringGetCharacter(pivotName, 0):
        lineLabelColor = supportColor
    nameLine = indiName + pivotName + ' Line'
    nameLabel = indiName + pivotName + ' Label'
    if ObjectFindMQL4(nameLine) != 0:
        if useShortLines == Yes:
            ObjectCreate(0, nameLine, OBJ_TREND, 0, Time[1] + (timeframeValueLabel * 60), value, Time[0] + (timeframeValueLabel * 60 * Line_Length), value)
        else:
            ObjectCreateMQL4(nameLine, OBJ_TREND, 0, iTime(None, timeFrame, 0), value, iTime(None, timeFrame, 0) + (timeframeValueLine * 60), value)
        ObjectSetMQL4(nameLine, 310, False)
        ObjectSetMQL4(nameLine, OBJPROP_COLOR, lineLabelColor)
        ObjectSetMQL4(nameLine, OBJPROP_STYLE, lineStyle)
        ObjectSetMQL4(nameLine, OBJPROP_WIDTH, lineWidth)
        ObjectSetMQL4(nameLine, OBJPROP_BACK, True)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTED, False)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTABLE, False)
        ChartRedraw(0)
    else:
        if useShortLines == Yes:
            ObjectMoveMQL4(nameLine, 0, Time[1] + (timeframeValueLabel * 60), value)
            ObjectMoveMQL4(nameLine, 1, Time[0] + (timeframeValueLabel * 60 * Line_Length), value)
        else:
            ObjectMoveMQL4(nameLine, 0, iTime(None, timeFrame, 0), value)
            ObjectMoveMQL4(nameLine, 1, iTime(None, timeFrame, 0) + (timeframeValueLine * 60), value)
    if hideCurrentLabels == No:
        if ObjectFindMQL4(nameLabel) != 0:
            if useShortLines == Yes:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, Time[0] + (timeframeValueLabel * 60 * ShiftLabel), value)
                if useSameColorLabelChoice == Yes:
                    ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
                else:
                    ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
                ObjectSetMQL4(nameLabel, OBJPROP_BACK, True)
                ObjectSetMQL4(nameLabel, OBJPROP_SELECTED, False)
                ObjectSetMQL4(nameLabel, OBJPROP_SELECTABLE, False)
            else:
                if currentLabelLocation == Follow_Price_2:
                    ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, Time[0] + (timeframeValueLabel * 60 * ShiftLabel), value)
                    ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
                if currentLabelLocation == Left_2:
                    ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0), value)
                    ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
                if currentLabelLocation == Middle_2:
                    ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValueLine * 30), value)
                    ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_UPPER)
                if currentLabelLocation == Right_2:
                    ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValueLine * 60), value)
                    ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
                if useSameColorLabelChoice == Yes:
                    ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
                else:
                    ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
                ObjectSetMQL4(nameLabel, OBJPROP_BACK, True)
                ObjectSetMQL4(nameLabel, OBJPROP_SELECTED, False)
                ObjectSetMQL4(nameLabel, OBJPROP_SELECTABLE, False)
            ChartRedraw(0)
        else:
            if currentLabelLocation == Follow_Price_2:
                ObjectMoveMQL4(nameLabel, 0, Time[0] + (timeframeValueLabel * 60 * ShiftLabel), value)
            if currentLabelLocation == Left_2:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0), value)
            if currentLabelLocation == Middle_2:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValueLine * 30), value)
            if currentLabelLocation == Right_2:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValueLine * 60), value)

def camarillaPivotPoint(ppArrayRef, timeframeShift, futurePlot):
    shift = 0
    if futurePlot:
        shift = 0
    else:
        shift = 1 + timeframeShift
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    camRange = iHigh(None, timeFrame, shift) - iLow(None, timeFrame, shift)
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    if futurePlot:
        prevClose = SymbolInfoDouble(None, SYMBOL_BID)
    H5 = _fdiv(prevHigh, prevLow) * prevClose
    H4 = prevClose + ((camRange * 1.1) / 2)
    H3 = ((1.1 / 4) * camRange) + prevClose
    H2 = prevClose + ((camRange * 1.1) / 6)
    H1 = prevClose + ((camRange * 1.1) / 12)
    L1 = prevClose - ((camRange * 1.1) / 12)
    L2 = prevClose - ((camRange * 1.1) / 6)
    L3 = prevClose - ((camRange * 1.1) / 4)
    L4 = prevClose - ((camRange * 1.1) / 2)
    L5 = prevClose - (H5 - prevClose)
    PP = (prevHigh + prevLow + prevClose) / 3
    ppArrayRef[0] = PP
    ppArrayRef[1] = L1
    ppArrayRef[2] = L2
    ppArrayRef[3] = L3
    ppArrayRef[4] = L4
    ppArrayRef[5] = H1
    ppArrayRef[6] = H2
    ppArrayRef[7] = H3
    ppArrayRef[8] = H4
    ppArrayRef[9] = H5
    ppArrayRef[10] = L5

def standardPivotPoint(ppArrayRef, timeframeShift, futurePlot):
    shift = 0
    if futurePlot:
        shift = 0
    else:
        shift = 1 + timeframeShift
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    if futurePlot:
        prevClose = SymbolInfoDouble(None, SYMBOL_BID)
    PP = (prevHigh + prevLow + prevClose) / 3
    R1 = (PP * 2) - prevLow
    S1 = (PP * 2) - prevHigh
    R2 = PP + prevHigh - prevLow
    S2 = PP - prevHigh + prevLow
    R3 = R1 + (prevHigh - prevLow)
    S3 = prevLow - (2 * (prevHigh - PP))
    R4 = R3 + (R2 - R1)
    S4 = S3 - (S1 - S2)
    ppArrayRef[0] = PP
    ppArrayRef[1] = S1
    ppArrayRef[2] = S2
    ppArrayRef[3] = S3
    ppArrayRef[4] = R1
    ppArrayRef[5] = R2
    ppArrayRef[6] = R3
    ppArrayRef[7] = R4
    ppArrayRef[8] = S4
    if drawFloorMidPP == Yes:
        ppArrayRef[9] = (R3 + R4) / 2
        ppArrayRef[10] = (R2 + R3) / 2
        ppArrayRef[11] = (R1 + R2) / 2
        ppArrayRef[12] = (PP + R1) / 2
        ppArrayRef[13] = (PP + S1) / 2
        ppArrayRef[14] = (S1 + S2) / 2
        ppArrayRef[15] = (S2 + S3) / 2
        ppArrayRef[16] = (S3 + S4) / 2

def woodiePivotPoint(ppArrayRef, timeframeShift, futurePlot):
    shift = 0
    if futurePlot:
        shift = 0
    else:
        shift = 1 + timeframeShift
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevRange = iHigh(None, timeFrame, shift) - iLow(None, timeFrame, shift)
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    if futurePlot:
        prevClose = SymbolInfoDouble(None, SYMBOL_BID)
    todayOpen = iOpen(None, timeFrame, shift - 1)
    PP = (prevHigh + prevLow + (todayOpen * 2)) / 4
    R1 = (PP * 2) - prevLow
    R2 = PP + prevRange
    S1 = (PP * 2) - prevHigh
    S2 = PP - prevRange
    S3 = prevLow - (2 * (prevHigh - PP))
    S4 = S3 - prevRange
    R3 = prevHigh + (2 * (PP - prevLow))
    R4 = R3 + prevRange
    ppArrayRef[0] = PP
    ppArrayRef[1] = S1
    ppArrayRef[2] = S2
    ppArrayRef[3] = R1
    ppArrayRef[4] = R2
    ppArrayRef[5] = S3
    ppArrayRef[6] = S4
    ppArrayRef[7] = R3
    ppArrayRef[8] = R4

def fibonacciPivotPoint(ppArrayRef, timeframeShift, futurePlot):
    shift = 0
    if futurePlot:
        shift = 0
    else:
        shift = 1 + timeframeShift
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevRange = iHigh(None, timeFrame, shift) - iLow(None, timeFrame, shift)
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    if futurePlot:
        prevClose = SymbolInfoDouble(None, SYMBOL_BID)
    Pivot = (prevHigh + prevLow + prevClose) / 3
    R38 = Pivot + (prevRange * 0.382)
    R61 = Pivot + (prevRange * 0.618)
    R78 = Pivot + (prevRange * 0.786)
    R100 = Pivot + (prevRange * 1.0)
    R138 = Pivot + (prevRange * 1.382)
    R161 = Pivot + (prevRange * 1.618)
    R200 = Pivot + (prevRange * 2.0)
    S38 = Pivot - (prevRange * 0.382)
    S61 = Pivot - (prevRange * 0.618)
    S78 = Pivot - (prevRange * 0.786)
    S100 = Pivot - (prevRange * 1.0)
    S138 = Pivot - (prevRange * 1.382)
    S161 = Pivot - (prevRange * 1.618)
    S200 = Pivot - (prevRange * 2.0)
    ppArrayRef[0] = Pivot
    ppArrayRef[1] = R38
    ppArrayRef[2] = R61
    ppArrayRef[3] = R78
    ppArrayRef[4] = R100
    ppArrayRef[5] = R138
    ppArrayRef[6] = R161
    ppArrayRef[7] = R200
    ppArrayRef[8] = S38
    ppArrayRef[9] = S61
    ppArrayRef[10] = S78
    ppArrayRef[11] = S100
    ppArrayRef[12] = S138
    ppArrayRef[13] = S161
    ppArrayRef[14] = S200

def traditionalPivotPoint(ppArrayRef, timeframeShift, futurePlot):
    shift = 0
    if futurePlot:
        shift = 0
    else:
        shift = 1 + timeframeShift
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    if futurePlot:
        prevClose = SymbolInfoDouble(None, SYMBOL_BID)
    PP = (prevHigh + prevLow + prevClose) / 3
    R1 = (PP * 2) - prevLow
    S1 = (PP * 2) - prevHigh
    R2 = PP + prevHigh - prevLow
    S2 = PP - prevHigh + prevLow
    R3 = (PP * 2) + (prevHigh - (2 * prevLow))
    S3 = (PP * 2) - ((2 * prevHigh) - prevLow)
    R4 = (PP * 3) + (prevHigh - (3 * prevLow))
    S4 = (PP * 3) - ((3 * prevHigh) - prevLow)
    R5 = (PP * 4) + (prevHigh - (4 * prevLow))
    S5 = (PP * 4) - ((4 * prevHigh) - prevLow)
    ppArrayRef[0] = PP
    ppArrayRef[1] = S1
    ppArrayRef[2] = S2
    ppArrayRef[3] = S3
    ppArrayRef[4] = R1
    ppArrayRef[5] = R2
    ppArrayRef[6] = R3
    ppArrayRef[7] = R4
    ppArrayRef[8] = S4
    ppArrayRef[9] = S5
    ppArrayRef[10] = R5

def demarkPivotPoint(ppArrayRef, timeframeShift, futurePlot):
    shift = 0
    if futurePlot:
        shift = 0
    else:
        shift = 1 + timeframeShift
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    if futurePlot:
        prevClose = SymbolInfoDouble(None, SYMBOL_BID)
    prevOpen = iOpen(None, timeFrame, shift)
    X = 1.0
    if prevOpen == prevClose:
        X = prevHigh + prevLow + (2 * prevClose)
    if prevClose > prevOpen:
        X = (2 * prevHigh) + prevLow + prevClose
    if prevClose < prevOpen:
        X = prevHigh + (prevLow * 2) + prevClose
    PP = X / 4
    R1 = (X / 2) - prevLow
    S1 = (X / 2) - prevHigh
    ppArrayRef[0] = PP
    ppArrayRef[1] = R1
    ppArrayRef[2] = S1

def classicPivotPoint(ppArrayRef, timeframeShift, futurePlot):
    shift = 0
    if futurePlot:
        shift = 0
    else:
        shift = 1 + timeframeShift
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    if futurePlot:
        prevClose = SymbolInfoDouble(None, SYMBOL_BID)
    PP = (prevHigh + prevLow + prevClose) / 3
    R1 = (2 * PP) - prevLow
    S1 = (2 * PP) - prevHigh
    R2 = PP + (prevHigh - prevLow)
    S2 = PP - (prevHigh - prevLow)
    R3 = PP + (2 * (prevHigh - prevLow))
    S3 = PP - (2 * (prevHigh - prevLow))
    R4 = PP + (3 * (prevHigh - prevLow))
    S4 = PP - (3 * (prevHigh - prevLow))
    ppArrayRef[0] = PP
    ppArrayRef[1] = S1
    ppArrayRef[2] = S2
    ppArrayRef[3] = S3
    ppArrayRef[4] = S4
    ppArrayRef[5] = R1
    ppArrayRef[6] = R2
    ppArrayRef[7] = R3
    ppArrayRef[8] = R4

def EnableDisablePivotPoint():
    if showStandardPivotPP == Disable:
        showStandard[0] = False
    else:
        showStandard[0] = True
    if showStandardPivotS1 == Disable:
        showStandard[1] = False
    else:
        showStandard[1] = True
    if showStandardPivotS2 == Disable:
        showStandard[2] = False
    else:
        showStandard[2] = True
    if showStandardPivotS3 == Disable:
        showStandard[3] = False
    else:
        showStandard[3] = True
    if showStandardPivotR1 == Disable:
        showStandard[4] = False
    else:
        showStandard[4] = True
    if showStandardPivotR2 == Disable:
        showStandard[5] = False
    else:
        showStandard[5] = True
    if showStandardPivotR3 == Disable:
        showStandard[6] = False
    else:
        showStandard[6] = True
    if showStandardPivotR4 == Disable:
        showStandard[7] = False
    else:
        showStandard[7] = True
    if showStandardPivotS4 == Disable:
        showStandard[8] = False
    else:
        showStandard[8] = True
    if showStandardPivotMR4 == Disable:
        showStandard[9] = False
    else:
        showStandard[9] = True
    if showStandardPivotMR3 == Disable:
        showStandard[10] = False
    else:
        showStandard[10] = True
    if showStandardPivotMR2 == Disable:
        showStandard[11] = False
    else:
        showStandard[11] = True
    if showStandardPivotMR1 == Disable:
        showStandard[12] = False
    else:
        showStandard[12] = True
    if showStandardPivotMS1 == Disable:
        showStandard[13] = False
    else:
        showStandard[13] = True
    if showStandardPivotMS2 == Disable:
        showStandard[14] = False
    else:
        showStandard[14] = True
    if showStandardPivotMS3 == Disable:
        showStandard[15] = False
    else:
        showStandard[15] = True
    if showStandardPivotMS4 == Disable:
        showStandard[16] = False
    else:
        showStandard[16] = True
    if showCamarillaPP == Disable:
        showCamarilla[0] = False
    else:
        showCamarilla[0] = True
    if showCamarillaL1 == Disable:
        showCamarilla[1] = False
    else:
        showCamarilla[1] = True
    if showCamarillaL2 == Disable:
        showCamarilla[2] = False
    else:
        showCamarilla[2] = True
    if showCamarillaL3 == Disable:
        showCamarilla[3] = False
    else:
        showCamarilla[3] = True
    if showCamarillaL4 == Disable:
        showCamarilla[4] = False
    else:
        showCamarilla[4] = True
    if showCamarillaH1 == Disable:
        showCamarilla[5] = False
    else:
        showCamarilla[5] = True
    if showCamarillaH2 == Disable:
        showCamarilla[6] = False
    else:
        showCamarilla[6] = True
    if showCamarillaH3 == Disable:
        showCamarilla[7] = False
    else:
        showCamarilla[7] = True
    if showCamarillaH4 == Disable:
        showCamarilla[8] = False
    else:
        showCamarilla[8] = True
    if showCamarillaH5 == Disable:
        showCamarilla[9] = False
    else:
        showCamarilla[9] = True
    if showCamarillaL5 == Disable:
        showCamarilla[10] = False
    else:
        showCamarilla[10] = True
    if showWoodiePP == Disable:
        showWoodie[0] = False
    else:
        showWoodie[0] = True
    if showWoodieS1 == Disable:
        showWoodie[1] = False
    else:
        showWoodie[1] = True
    if showWoodieS2 == Disable:
        showWoodie[2] = False
    else:
        showWoodie[2] = True
    if showWoodieR1 == Disable:
        showWoodie[3] = False
    else:
        showWoodie[3] = True
    if showWoodieR2 == Disable:
        showWoodie[4] = False
    else:
        showWoodie[4] = True
    if showWoodieS3 == Disable:
        showWoodie[5] = False
    else:
        showWoodie[5] = True
    if showWoodieS4 == Disable:
        showWoodie[6] = False
    else:
        showWoodie[6] = True
    if showWoodieR3 == Disable:
        showWoodie[7] = False
    else:
        showWoodie[7] = True
    if showWoodieR4 == Disable:
        showWoodie[8] = False
    else:
        showWoodie[8] = True
    if showFibonacciPivotPP == Disable:
        showFibonacci[0] = False
    else:
        showFibonacci[0] = True
    if showFibonacciPivotR38 == Disable:
        showFibonacci[1] = False
    else:
        showFibonacci[1] = True
    if showFibonacciPivotR61 == Disable:
        showFibonacci[2] = False
    else:
        showFibonacci[2] = True
    if showFibonacciPivotR78 == Disable:
        showFibonacci[3] = False
    else:
        showFibonacci[3] = True
    if showFibonacciPivotR100 == Disable:
        showFibonacci[4] = False
    else:
        showFibonacci[4] = True
    if showFibonacciPivotR138 == Disable:
        showFibonacci[5] = False
    else:
        showFibonacci[5] = True
    if showFibonacciPivotR161 == Disable:
        showFibonacci[6] = False
    else:
        showFibonacci[6] = True
    if showFibonacciPivotR200 == Disable:
        showFibonacci[7] = False
    else:
        showFibonacci[7] = True
    if showFibonacciPivotS38 == Disable:
        showFibonacci[8] = False
    else:
        showFibonacci[8] = True
    if showFibonacciPivotS61 == Disable:
        showFibonacci[9] = False
    else:
        showFibonacci[9] = True
    if showFibonacciPivotS78 == Disable:
        showFibonacci[10] = False
    else:
        showFibonacci[10] = True
    if showFibonacciPivotS100 == Disable:
        showFibonacci[11] = False
    else:
        showFibonacci[11] = True
    if showFibonacciPivotS138 == Disable:
        showFibonacci[12] = False
    else:
        showFibonacci[12] = True
    if showFibonacciPivotS161 == Disable:
        showFibonacci[13] = False
    else:
        showFibonacci[13] = True
    if showFibonacciPivotS200 == Disable:
        showFibonacci[14] = False
    else:
        showFibonacci[14] = True
    if showTraditionalPP == Disable:
        showTraditional[0] = False
    else:
        showTraditional[0] = True
    if showTraditionalS1 == Disable:
        showTraditional[1] = False
    else:
        showTraditional[1] = True
    if showTraditionalS2 == Disable:
        showTraditional[2] = False
    else:
        showTraditional[2] = True
    if showTraditionalS3 == Disable:
        showTraditional[3] = False
    else:
        showTraditional[3] = True
    if showTraditionalR1 == Disable:
        showTraditional[4] = False
    else:
        showTraditional[4] = True
    if showTraditionalR2 == Disable:
        showTraditional[5] = False
    else:
        showTraditional[5] = True
    if showTraditionalR3 == Disable:
        showTraditional[6] = False
    else:
        showTraditional[6] = True
    if showTraditionalR4 == Disable:
        showTraditional[7] = False
    else:
        showTraditional[7] = True
    if showTraditionalS4 == Disable:
        showTraditional[8] = False
    else:
        showTraditional[8] = True
    if showTraditionalS5 == Disable:
        showTraditional[9] = False
    else:
        showTraditional[9] = True
    if showTraditionalR5 == Disable:
        showTraditional[10] = False
    else:
        showTraditional[10] = True
    if showDemarkPP == Disable:
        showDemark[0] = False
    else:
        showDemark[0] = True
    if showDemarkR1 == Disable:
        showDemark[1] = False
    else:
        showDemark[1] = True
    if showDemarkS1 == Disable:
        showDemark[2] = False
    else:
        showDemark[2] = True
    if showClassicPP == Disable:
        showClassic[0] = False
    else:
        showClassic[0] = True
    if showClassicS1 == Disable:
        showClassic[1] = False
    else:
        showClassic[1] = True
    if showClassicS2 == Disable:
        showClassic[2] = False
    else:
        showClassic[2] = True
    if showClassicS3 == Disable:
        showClassic[3] = False
    else:
        showClassic[3] = True
    if showClassicS4 == Disable:
        showClassic[4] = False
    else:
        showClassic[4] = True
    if showClassicR1 == Disable:
        showClassic[5] = False
    else:
        showClassic[5] = True
    if showClassicR2 == Disable:
        showClassic[6] = False
    else:
        showClassic[6] = True
    if showClassicR3 == Disable:
        showClassic[7] = False
    else:
        showClassic[7] = True
    if showClassicR4 == Disable:
        showClassic[8] = False
    else:
        showClassic[8] = True
    if showCPRBC == Disable:
        showFloorCPR[0] = False
    else:
        showFloorCPR[0] = True
    if showCPRTC == Disable:
        showFloorCPR[1] = False
    else:
        showFloorCPR[1] = True

def DrawHistoricalLines(value, pivotName, index):
    timeframeValue = 0
    _sw3 = timeFrame
    if _sw3 == PERIOD_M1:
        timeframeValue = 1
    elif _sw3 == PERIOD_M2:
        timeframeValue = 2
    elif _sw3 == PERIOD_M3:
        timeframeValue = 3
    elif _sw3 == PERIOD_M4:
        timeframeValue = 4
    elif _sw3 == PERIOD_M5:
        timeframeValue = 5
    elif _sw3 == PERIOD_M6:
        timeframeValue = 6
    elif _sw3 == PERIOD_M10:
        timeframeValue = 10
    elif _sw3 == PERIOD_M12:
        timeframeValue = 12
    elif _sw3 == PERIOD_M15:
        timeframeValue = 15
    elif _sw3 == PERIOD_M20:
        timeframeValue = 20
    elif _sw3 == PERIOD_M30:
        timeframeValue = 30
    elif _sw3 == PERIOD_H1:
        timeframeValue = 60
    elif _sw3 == PERIOD_H2:
        timeframeValue = 240
    elif _sw3 == PERIOD_H3:
        timeframeValue = 180
    elif _sw3 == PERIOD_H4:
        timeframeValue = 240
    elif _sw3 == PERIOD_H6:
        timeframeValue = 360
    elif _sw3 == PERIOD_H8:
        timeframeValue = 480
    elif _sw3 == PERIOD_H12:
        timeframeValue = 720
    elif _sw3 == PERIOD_D1:
        timeframeValue = 1440
    elif _sw3 == PERIOD_W1:
        timeframeValue = 10080
    elif _sw3 == PERIOD_MN1:
        timeframeValue = 43200
    lineLabelColor = clrNONE
    message = ''
    if showPriceLabel == Yes:
        message = customMSG + pivotName + ': ' + DoubleToString(value, Digits())
    else:
        message = customMSG + pivotName
    if 82 == StringGetCharacter(pivotName, 0):
        lineLabelColor = resistantColor
    if 80 == StringGetCharacter(pivotName, 0):
        lineLabelColor = pivotColor
    if 83 == StringGetCharacter(pivotName, 0):
        lineLabelColor = supportColor
    if 77 == StringGetCharacter(pivotName, 0):
        lineLabelColor = midColor
    if 72 == StringGetCharacter(pivotName, 0):
        lineLabelColor = resistantColor
    if 76 == StringGetCharacter(pivotName, 0):
        lineLabelColor = supportColor
    nameLine = indiName + pivotName + ' Line' + ' ' + _str(index)
    nameLabel = indiName + pivotName + ' Label' + ' ' + _str(index)
    if ObjectFindMQL4(nameLine) != 0:
        ObjectCreateMQL4(nameLine, OBJ_TREND, 0, iTime(None, timeFrame, index), value, iTime(None, timeFrame, index) + (timeframeValue * 60), value)
        ObjectSetMQL4(nameLine, 310, False)
        ObjectSetMQL4(nameLine, OBJPROP_COLOR, lineLabelColor)
        ObjectSetMQL4(nameLine, OBJPROP_STYLE, lineStyle)
        ObjectSetMQL4(nameLine, OBJPROP_WIDTH, lineWidth)
        ObjectSetMQL4(nameLine, OBJPROP_BACK, True)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTED, False)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTABLE, False)
        ChartRedraw(0)
    else:
        ObjectMoveMQL4(nameLine, 0, iTime(None, timeFrame, index), value)
        ObjectMoveMQL4(nameLine, 1, iTime(None, timeFrame, index) + (timeframeValue * 60), value)
    if hideHistoricalLabels == No:
        if ObjectFindMQL4(nameLabel) != 0:
            if historicalLabelLocation == Left_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, index), value)
                ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
            if historicalLabelLocation == Middle_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, index) + (timeframeValue * 30), value)
                ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_UPPER)
            if historicalLabelLocation == Right_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, index) + (timeframeValue * 60), value)
                ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
            if useSameColorLabelChoice == Yes:
                ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
            else:
                ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
            ObjectSetMQL4(nameLabel, OBJPROP_BACK, True)
            ObjectSetMQL4(nameLabel, OBJPROP_SELECTED, False)
            ObjectSetMQL4(nameLabel, OBJPROP_SELECTABLE, False)
            ChartRedraw(0)
        else:
            if historicalLabelLocation == Left_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, index), value)
            if historicalLabelLocation == Middle_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, index) + (timeframeValue * 30), value)
            if historicalLabelLocation == Right_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, index) + (timeframeValue * 60), value)

def foundWeekend(index):
    result = False
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, index)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            result = True
        dayCheck2 = iTime(None, PERIOD_D1, index)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            result = True
    return result

def DrawFuturePlot(value, pivotName):
    timeframeValue = 0
    _sw4 = timeFrame
    if _sw4 == PERIOD_M1:
        timeframeValue = 1
    elif _sw4 == PERIOD_M2:
        timeframeValue = 2
    elif _sw4 == PERIOD_M3:
        timeframeValue = 3
    elif _sw4 == PERIOD_M4:
        timeframeValue = 4
    elif _sw4 == PERIOD_M5:
        timeframeValue = 5
    elif _sw4 == PERIOD_M6:
        timeframeValue = 6
    elif _sw4 == PERIOD_M10:
        timeframeValue = 10
    elif _sw4 == PERIOD_M12:
        timeframeValue = 12
    elif _sw4 == PERIOD_M15:
        timeframeValue = 15
    elif _sw4 == PERIOD_M20:
        timeframeValue = 20
    elif _sw4 == PERIOD_M30:
        timeframeValue = 30
    elif _sw4 == PERIOD_H1:
        timeframeValue = 60
    elif _sw4 == PERIOD_H2:
        timeframeValue = 240
    elif _sw4 == PERIOD_H3:
        timeframeValue = 180
    elif _sw4 == PERIOD_H4:
        timeframeValue = 240
    elif _sw4 == PERIOD_H6:
        timeframeValue = 360
    elif _sw4 == PERIOD_H8:
        timeframeValue = 480
    elif _sw4 == PERIOD_H12:
        timeframeValue = 720
    elif _sw4 == PERIOD_D1:
        timeframeValue = 1440
    elif _sw4 == PERIOD_W1:
        timeframeValue = 10080
    elif _sw4 == PERIOD_MN1:
        timeframeValue = 43200
    lineLabelColor = clrNONE
    message = ''
    if showPriceLabel == Yes:
        message = customMSG + pivotName + ': ' + DoubleToString(value, Digits())
    else:
        message = customMSG + pivotName
    if 82 == StringGetCharacter(pivotName, 0):
        lineLabelColor = resistantColor
    if 80 == StringGetCharacter(pivotName, 0):
        lineLabelColor = pivotColor
    if 83 == StringGetCharacter(pivotName, 0):
        lineLabelColor = supportColor
    if 77 == StringGetCharacter(pivotName, 0):
        lineLabelColor = midColor
    if 72 == StringGetCharacter(pivotName, 0):
        lineLabelColor = resistantColor
    if 76 == StringGetCharacter(pivotName, 0):
        lineLabelColor = supportColor
    nameLine = indiName + pivotName + ' Line' + ' Future'
    nameLabel = indiName + pivotName + ' Label' + ' Future'
    if ObjectFindMQL4(nameLine) != 0:
        ObjectCreateMQL4(nameLine, OBJ_TREND, 0, iTime(None, timeFrame, 0) + (timeFrame * 60), value, iTime(None, timeFrame, 0) + (timeframeValue * 120), value)
        ObjectSetMQL4(nameLine, 310, False)
        ObjectSetMQL4(nameLine, OBJPROP_COLOR, lineLabelColor)
        ObjectSetMQL4(nameLine, OBJPROP_STYLE, lineStyle)
        ObjectSetMQL4(nameLine, OBJPROP_WIDTH, lineWidth)
        ObjectSetMQL4(nameLine, OBJPROP_BACK, True)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTED, False)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTABLE, False)
        ChartRedraw(0)
    else:
        ObjectMoveMQL4(nameLine, 0, iTime(None, timeFrame, 0) + (timeframeValue * 60), value)
        ObjectMoveMQL4(nameLine, 1, iTime(None, timeFrame, 0) + (timeframeValue * 120), value)
    if hideFutureLabels == No:
        if ObjectFindMQL4(nameLabel) != 0:
            if futureLabelLocation == Left_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValue * 60), value)
                ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
            if futureLabelLocation == Middle_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValue * 90), value)
                ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_UPPER)
            if futureLabelLocation == Right_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValue * 120), value)
                ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
            if useSameColorLabelChoice == Yes:
                ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
            else:
                ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
            ObjectSetMQL4(nameLabel, OBJPROP_BACK, True)
            ObjectSetMQL4(nameLabel, OBJPROP_SELECTED, False)
            ObjectSetMQL4(nameLabel, OBJPROP_SELECTABLE, False)
            ChartRedraw(0)
        else:
            if futureLabelLocation == Left_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValue * 60), value)
            if futureLabelLocation == Middle_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValue * 90), value)
            if futureLabelLocation == Right_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValue * 120), value)

def standardPivotPointCPR(ppArrayRef, timeframeShift, futurePlot):
    shift = 0
    if futurePlot:
        shift = 0
    else:
        shift = 1
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, timeframeShift + shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, timeframeShift + shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevHigh = iHigh(None, timeFrame, timeframeShift + shift)
    prevLow = iLow(None, timeFrame, timeframeShift + shift)
    prevClose = iClose(None, timeFrame, timeframeShift + shift)
    if futurePlot:
        prevClose = SymbolInfoDouble(None, SYMBOL_BID)
    PP = (prevHigh + prevLow + prevClose) / 3
    BC = (prevHigh + prevLow) / 2
    TC = PP - BC + PP
    ppArrayRef[0] = BC
    ppArrayRef[1] = TC

def DrawCPRPivotLines(value, pivotName):
    timeframeValueLabel = 0
    timeframeValueLine = 0
    if currentLabelLocation == Follow_Price_2 or useShortLines == Yes:
        _sw5 = Period()
        if _sw5 == PERIOD_M1:
            timeframeValueLabel = 1
        elif _sw5 == PERIOD_M2:
            timeframeValueLabel = 2
        elif _sw5 == PERIOD_M3:
            timeframeValueLabel = 3
        elif _sw5 == PERIOD_M4:
            timeframeValueLabel = 4
        elif _sw5 == PERIOD_M5:
            timeframeValueLabel = 5
        elif _sw5 == PERIOD_M6:
            timeframeValueLabel = 6
        elif _sw5 == PERIOD_M10:
            timeframeValueLabel = 10
        elif _sw5 == PERIOD_M12:
            timeframeValueLabel = 12
        elif _sw5 == PERIOD_M15:
            timeframeValueLabel = 15
        elif _sw5 == PERIOD_M20:
            timeframeValueLabel = 20
        elif _sw5 == PERIOD_M30:
            timeframeValueLabel = 30
        elif _sw5 == PERIOD_H1:
            timeframeValueLabel = 60
        elif _sw5 == PERIOD_H2:
            timeframeValueLabel = 240
        elif _sw5 == PERIOD_H3:
            timeframeValueLabel = 180
        elif _sw5 == PERIOD_H4:
            timeframeValueLabel = 240
        elif _sw5 == PERIOD_H6:
            timeframeValueLabel = 360
        elif _sw5 == PERIOD_H8:
            timeframeValueLabel = 480
        elif _sw5 == PERIOD_H12:
            timeframeValueLabel = 720
        elif _sw5 == PERIOD_D1:
            timeframeValueLabel = 1440
        elif _sw5 == PERIOD_W1:
            timeframeValueLabel = 10080
        elif _sw5 == PERIOD_MN1:
            timeframeValueLabel = 43200
    _sw6 = timeFrame
    if _sw6 == PERIOD_M1:
        timeframeValueLine = 1
    elif _sw6 == PERIOD_M2:
        timeframeValueLine = 2
    elif _sw6 == PERIOD_M3:
        timeframeValueLine = 3
    elif _sw6 == PERIOD_M4:
        timeframeValueLine = 4
    elif _sw6 == PERIOD_M5:
        timeframeValueLine = 5
    elif _sw6 == PERIOD_M6:
        timeframeValueLine = 6
    elif _sw6 == PERIOD_M10:
        timeframeValueLine = 10
    elif _sw6 == PERIOD_M12:
        timeframeValueLine = 12
    elif _sw6 == PERIOD_M15:
        timeframeValueLine = 15
    elif _sw6 == PERIOD_M20:
        timeframeValueLine = 20
    elif _sw6 == PERIOD_M30:
        timeframeValueLine = 30
    elif _sw6 == PERIOD_H1:
        timeframeValueLine = 60
    elif _sw6 == PERIOD_H2:
        timeframeValueLine = 240
    elif _sw6 == PERIOD_H3:
        timeframeValueLine = 180
    elif _sw6 == PERIOD_H4:
        timeframeValueLine = 240
    elif _sw6 == PERIOD_H6:
        timeframeValueLine = 360
    elif _sw6 == PERIOD_H8:
        timeframeValueLine = 480
    elif _sw6 == PERIOD_H12:
        timeframeValueLine = 720
    elif _sw6 == PERIOD_D1:
        timeframeValueLine = 1440
    elif _sw6 == PERIOD_W1:
        timeframeValueLine = 10080
    elif _sw6 == PERIOD_MN1:
        timeframeValueLine = 43200
    Time = Arr(0, 0)
    count = 2
    ArraySetAsSeries(Time, True)
    CopyTime(Symbol(), Period(), 0, count, Time)
    lineLabelColor = clrNONE
    message = 'Poop'
    if showPriceLabel == Yes:
        message = customMSG + pivotName + ': ' + DoubleToString(value, Digits())
    else:
        message = customMSG + pivotName
    if 66 == StringGetCharacter(pivotName, 0):
        lineLabelColor = CPRColor
    elif 84 == StringGetCharacter(pivotName, 0):
        lineLabelColor = CPRColor
    nameLine = indiName + pivotName + ' Line'
    nameLabel = indiName + pivotName + ' Label'
    if ObjectFindMQL4(nameLine) != 0:
        if useShortLines == Yes:
            ObjectCreateMQL4(nameLine, OBJ_TREND, 0, Time[1] + (timeframeValueLabel * 60), value, Time[0] + (timeframeValueLabel * 60 * Line_Length), value)
        else:
            ObjectCreateMQL4(nameLine, OBJ_TREND, 0, iTime(None, timeFrame, 0), value, iTime(None, timeFrame, 0) + (timeframeValueLine * 120), value)
        ObjectSetMQL4(nameLine, 310, False)
        ObjectSetMQL4(nameLine, OBJPROP_COLOR, lineLabelColor)
        ObjectSetMQL4(nameLine, OBJPROP_STYLE, lineStyle)
        ObjectSetMQL4(nameLine, OBJPROP_WIDTH, lineWidth)
        ObjectSetMQL4(nameLine, OBJPROP_BACK, True)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTED, False)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTABLE, False)
        ChartRedraw(0)
    else:
        if useShortLines == Yes:
            ObjectMoveMQL4(nameLine, 0, Time[1] + (timeframeValueLabel * 60), value)
            ObjectMoveMQL4(nameLine, 1, Time[0] + (timeframeValueLabel * 60 * Line_Length), value)
        else:
            ObjectMoveMQL4(nameLine, 0, iTime(None, timeFrame, 0), value)
            ObjectMoveMQL4(nameLine, 1, iTime(None, timeFrame, 0) + (timeframeValueLine * 60), value)
    if hideCurrentLabels == No:
        if ObjectFindMQL4(nameLabel) != 0:
            if useShortLines == Yes:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, Time[0] + (timeframeValueLabel * 60 * ShiftLabel), value)
                if useSameColorLabelChoice == Yes:
                    ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
                else:
                    ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
                ObjectSetMQL4(nameLabel, OBJPROP_BACK, True)
                ObjectSetMQL4(nameLabel, OBJPROP_SELECTED, False)
                ObjectSetMQL4(nameLabel, OBJPROP_SELECTABLE, False)
            else:
                if currentLabelLocation == Follow_Price_2:
                    ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, Time[0] + (timeframeValueLabel * 60 * ShiftLabel), value)
                    ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
                if currentLabelLocation == Left_2:
                    ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0), value)
                    ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
                if currentLabelLocation == Middle_2:
                    ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValueLine * 30), value)
                    ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_UPPER)
                if currentLabelLocation == Right_2:
                    ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValueLine * 60), value)
                    ObjectSetInteger(0, nameLabel, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
                if useSameColorLabelChoice == Yes:
                    ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
                else:
                    ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
                ObjectSetMQL4(nameLabel, OBJPROP_BACK, True)
                ObjectSetMQL4(nameLabel, OBJPROP_SELECTED, False)
                ObjectSetMQL4(nameLabel, OBJPROP_SELECTABLE, False)
            ChartRedraw(0)
        else:
            if currentLabelLocation == Follow_Price_2:
                ObjectMoveMQL4(nameLabel, 0, Time[0] + (timeframeValueLabel * 60 * ShiftLabel), value)
            if currentLabelLocation == Left_2:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0), value)
            if currentLabelLocation == Middle_2:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValueLine * 30), value)
            if currentLabelLocation == Right_2:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValueLine * 60), value)

def DrawCPRHistoricalLines(value, pivotName, index):
    timeframeValue = 0
    _sw7 = timeFrame
    if _sw7 == PERIOD_M1:
        timeframeValue = 1
    elif _sw7 == PERIOD_M2:
        timeframeValue = 2
    elif _sw7 == PERIOD_M3:
        timeframeValue = 3
    elif _sw7 == PERIOD_M4:
        timeframeValue = 4
    elif _sw7 == PERIOD_M5:
        timeframeValue = 5
    elif _sw7 == PERIOD_M6:
        timeframeValue = 6
    elif _sw7 == PERIOD_M10:
        timeframeValue = 10
    elif _sw7 == PERIOD_M12:
        timeframeValue = 12
    elif _sw7 == PERIOD_M15:
        timeframeValue = 15
    elif _sw7 == PERIOD_M20:
        timeframeValue = 20
    elif _sw7 == PERIOD_M30:
        timeframeValue = 30
    elif _sw7 == PERIOD_H1:
        timeframeValue = 60
    elif _sw7 == PERIOD_H2:
        timeframeValue = 240
    elif _sw7 == PERIOD_H3:
        timeframeValue = 180
    elif _sw7 == PERIOD_H4:
        timeframeValue = 240
    elif _sw7 == PERIOD_H6:
        timeframeValue = 360
    elif _sw7 == PERIOD_H8:
        timeframeValue = 480
    elif _sw7 == PERIOD_H12:
        timeframeValue = 720
    elif _sw7 == PERIOD_D1:
        timeframeValue = 1440
    elif _sw7 == PERIOD_W1:
        timeframeValue = 10080
    elif _sw7 == PERIOD_MN1:
        timeframeValue = 43200
    lineLabelColor = clrNONE
    message = ''
    if showPriceLabel == Yes:
        message = customMSG + pivotName + ': ' + DoubleToString(value, Digits())
    else:
        message = customMSG + pivotName
    if 66 == StringGetCharacter(pivotName, 0):
        lineLabelColor = CPRColor
    if 84 == StringGetCharacter(pivotName, 0):
        lineLabelColor = CPRColor
    nameLine = indiName + pivotName + ' Line' + ' ' + _str(index)
    nameLabel = indiName + pivotName + ' Label' + ' ' + _str(index)
    if ObjectFindMQL4(nameLine) != 0:
        ObjectCreateMQL4(nameLine, OBJ_TREND, 0, iTime(None, timeFrame, index), value, iTime(None, timeFrame, index) + (timeframeValue * 60), value)
        ObjectSetMQL4(nameLine, 310, False)
        ObjectSetMQL4(nameLine, OBJPROP_COLOR, lineLabelColor)
        ObjectSetMQL4(nameLine, OBJPROP_STYLE, lineStyle)
        ObjectSetMQL4(nameLine, OBJPROP_WIDTH, lineWidth)
        ObjectSetMQL4(nameLine, OBJPROP_BACK, True)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTED, False)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTABLE, False)
        ChartRedraw(0)
    else:
        ObjectMoveMQL4(nameLine, 0, iTime(None, timeFrame, index), value)
        ObjectMoveMQL4(nameLine, 1, iTime(None, timeFrame, index) + (timeframeValue * 60), value)
    if hideHistoricalLabels == No:
        if ObjectFindMQL4(nameLabel) != 0:
            if historicalLabelLocation == Left_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, index), value)
                ObjectSetMQL4(nameLabel, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
            if historicalLabelLocation == Middle_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, index) + (timeframeValue * 30), value)
                ObjectSetMQL4(nameLabel, OBJPROP_ANCHOR, ANCHOR_UPPER)
            if historicalLabelLocation == Right_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, index) + (timeframeValue * 60), value)
                ObjectSetMQL4(nameLabel, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
            if useSameColorLabelChoice == Yes:
                ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
            else:
                ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
            ObjectSetMQL4(nameLabel, OBJPROP_BACK, True)
            ObjectSetMQL4(nameLabel, OBJPROP_SELECTED, False)
            ObjectSetMQL4(nameLabel, OBJPROP_SELECTABLE, False)
            ChartRedraw(0)
        else:
            if historicalLabelLocation == Left_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, index), value)
            if historicalLabelLocation == Middle_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, index) + (timeframeValue * 30), value)
            if historicalLabelLocation == Right_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, index) + (timeframeValue * 60), value)

def DrawCPRFuturePlot(value, pivotName):
    timeframeValue = 0
    _sw8 = timeFrame
    if _sw8 == PERIOD_M1:
        timeframeValue = 1
    elif _sw8 == PERIOD_M2:
        timeframeValue = 2
    elif _sw8 == PERIOD_M3:
        timeframeValue = 3
    elif _sw8 == PERIOD_M4:
        timeframeValue = 4
    elif _sw8 == PERIOD_M5:
        timeframeValue = 5
    elif _sw8 == PERIOD_M6:
        timeframeValue = 6
    elif _sw8 == PERIOD_M10:
        timeframeValue = 10
    elif _sw8 == PERIOD_M12:
        timeframeValue = 12
    elif _sw8 == PERIOD_M15:
        timeframeValue = 15
    elif _sw8 == PERIOD_M20:
        timeframeValue = 20
    elif _sw8 == PERIOD_M30:
        timeframeValue = 30
    elif _sw8 == PERIOD_H1:
        timeframeValue = 60
    elif _sw8 == PERIOD_H2:
        timeframeValue = 240
    elif _sw8 == PERIOD_H3:
        timeframeValue = 180
    elif _sw8 == PERIOD_H4:
        timeframeValue = 240
    elif _sw8 == PERIOD_H6:
        timeframeValue = 360
    elif _sw8 == PERIOD_H8:
        timeframeValue = 480
    elif _sw8 == PERIOD_H12:
        timeframeValue = 720
    elif _sw8 == PERIOD_D1:
        timeframeValue = 1440
    elif _sw8 == PERIOD_W1:
        timeframeValue = 10080
    elif _sw8 == PERIOD_MN1:
        timeframeValue = 43200
    lineLabelColor = clrNONE
    message = ''
    if showPriceLabel == Yes:
        message = customMSG + pivotName + ': ' + DoubleToString(value, Digits())
    else:
        message = customMSG + pivotName
    if 66 == StringGetCharacter(pivotName, 0):
        lineLabelColor = CPRColor
    if 84 == StringGetCharacter(pivotName, 0):
        lineLabelColor = CPRColor
    nameLine = indiName + pivotName + ' Line' + ' Future'
    nameLabel = indiName + pivotName + ' Label' + ' Future'
    if ObjectFindMQL4(nameLine) != 0:
        ObjectCreateMQL4(nameLine, OBJ_TREND, 0, iTime(None, timeFrame, 0) + (timeFrame * 60), value, iTime(None, timeFrame, 0) + (timeframeValue * 120), value)
        ObjectSetMQL4(nameLine, 310, False)
        ObjectSetMQL4(nameLine, OBJPROP_COLOR, lineLabelColor)
        ObjectSetMQL4(nameLine, OBJPROP_STYLE, lineStyle)
        ObjectSetMQL4(nameLine, OBJPROP_WIDTH, lineWidth)
        ObjectSetMQL4(nameLine, OBJPROP_BACK, True)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTED, False)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTABLE, False)
        ChartRedraw(0)
    else:
        ObjectMoveMQL4(nameLine, 0, iTime(None, timeFrame, 0) + (timeframeValue * 60), value)
        ObjectMoveMQL4(nameLine, 1, iTime(None, timeFrame, 0) + (timeframeValue * 120), value)
    if hideFutureLabels == No:
        if ObjectFindMQL4(nameLabel) != 0:
            if futureLabelLocation == Left_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValue * 60), value)
                ObjectSetMQL4(nameLabel, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
            if futureLabelLocation == Middle_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValue * 90), value)
                ObjectSetMQL4(nameLabel, OBJPROP_ANCHOR, ANCHOR_UPPER)
            if futureLabelLocation == Right_1:
                ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, iTime(None, timeFrame, 0) + (timeframeValue * 120), value)
                ObjectSetMQL4(nameLabel, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
            if useSameColorLabelChoice == Yes:
                ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
            else:
                ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
            ObjectSetMQL4(nameLabel, OBJPROP_BACK, True)
            ObjectSetMQL4(nameLabel, OBJPROP_SELECTED, False)
            ObjectSetMQL4(nameLabel, OBJPROP_SELECTABLE, False)
            ChartRedraw(0)
        else:
            if futureLabelLocation == Left_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValue * 60), value)
            if futureLabelLocation == Middle_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValue * 90), value)
            if futureLabelLocation == Right_1:
                ObjectMoveMQL4(nameLabel, 0, iTime(None, timeFrame, 0) + (timeframeValue * 120), value)

def ObjectFindMQL4(name):
    return ObjectFind(0, name)

def ObjectSetMQL4(name, index, value):
    _sw9 = index
    if _sw9 == 300:
        ObjectSetInteger(0, name, OBJPROP_TIME, _int(value))
        return True
    elif _sw9 == 301:
        ObjectSetDouble(0, name, OBJPROP_PRICE, value)
        return True
    elif _sw9 == 302:
        ObjectSetInteger(0, name, OBJPROP_TIME, 1, _int(value))
        return True
    elif _sw9 == 303:
        ObjectSetDouble(0, name, OBJPROP_PRICE, 1, value)
        return True
    elif _sw9 == 304:
        ObjectSetInteger(0, name, OBJPROP_TIME, 2, _int(value))
        return True
    elif _sw9 == 305:
        ObjectSetDouble(0, name, OBJPROP_PRICE, 2, value)
        return True
    elif _sw9 == OBJPROP_COLOR:
        ObjectSetInteger(0, name, OBJPROP_COLOR, _int(value))
        return True
    elif _sw9 == OBJPROP_STYLE:
        ObjectSetInteger(0, name, OBJPROP_STYLE, _int(value))
        return True
    elif _sw9 == OBJPROP_WIDTH:
        ObjectSetInteger(0, name, OBJPROP_WIDTH, _int(value))
        return True
    elif _sw9 == OBJPROP_BACK:
        ObjectSetInteger(0, name, OBJPROP_BACK, _int(value))
        return True
    elif _sw9 == 310:
        ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, _int(value))
        return True
    elif _sw9 == OBJPROP_ELLIPSE:
        ObjectSetInteger(0, name, OBJPROP_ELLIPSE, _int(value))
        return True
    elif _sw9 == OBJPROP_SCALE:
        ObjectSetDouble(0, name, OBJPROP_SCALE, value)
        return True
    elif _sw9 == OBJPROP_ANGLE:
        ObjectSetDouble(0, name, OBJPROP_ANGLE, value)
        return True
    elif _sw9 == OBJPROP_ARROWCODE:
        ObjectSetInteger(0, name, OBJPROP_ARROWCODE, _int(value))
        return True
    elif _sw9 == OBJPROP_TIMEFRAMES:
        ObjectSetInteger(0, name, OBJPROP_TIMEFRAMES, _int(value))
        return True
    elif _sw9 == OBJPROP_DEVIATION:
        ObjectSetDouble(0, name, OBJPROP_DEVIATION, value)
        return True
    elif _sw9 == OBJPROP_FONTSIZE:
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, _int(value))
        return True
    elif _sw9 == OBJPROP_CORNER:
        ObjectSetInteger(0, name, OBJPROP_CORNER, _int(value))
        return True
    elif _sw9 == OBJPROP_XDISTANCE:
        ObjectSetInteger(0, name, OBJPROP_XDISTANCE, _int(value))
        return True
    elif _sw9 == OBJPROP_YDISTANCE:
        ObjectSetInteger(0, name, OBJPROP_YDISTANCE, _int(value))
        return True
    elif _sw9 == 200:
        ObjectSetInteger(0, name, OBJPROP_LEVELS, _int(value))
        return True
    elif _sw9 == OBJPROP_LEVELCOLOR:
        ObjectSetInteger(0, name, OBJPROP_LEVELCOLOR, _int(value))
        return True
    elif _sw9 == OBJPROP_LEVELSTYLE:
        ObjectSetInteger(0, name, OBJPROP_LEVELSTYLE, _int(value))
        return True
    elif _sw9 == OBJPROP_LEVELWIDTH:
        ObjectSetInteger(0, name, OBJPROP_LEVELWIDTH, _int(value))
        return True
    else:
        return False
    return False

def ObjectMoveMQL4(name, point, time1, price1):
    return ObjectMove(0, name, point, time1, price1)

def ObjectCreateMQL4(name, type_, window, time1, price1, time2=0, price2=0.0, time3=0, price3=0.0):
    return ObjectCreate(0, name, type_, window, time1, price1, time2, price2, time3, price3)

def ObjectSetTextMQL4(name, text, font_size, font='', text_color=CLR_NONE):
    tmpObjType = _int(ObjectGetInteger(0, name, OBJPROP_TYPE))
    if tmpObjType != OBJ_LABEL and tmpObjType != OBJ_TEXT:
        return False
    if StringLen(text) > 0 and font_size > 0:
        if ObjectSetString(0, name, OBJPROP_TEXT, text) == True and ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size) == True:
            if StringLen(font) > 0 and ObjectSetString(0, name, OBJPROP_FONT, font) == False:
                return False
            if text_color > -1 and ObjectSetInteger(0, name, OBJPROP_COLOR, text_color) == False:
                return False
            return True
        return False
    return False

def TimeDayOfWeekMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day_of_week

# ---- global variables initialised from expressions
indiName = 'PPL' + _str(UniqueID) + ' ' + EnumToString(pivotSelection, 'pivotTypes') + ' ' + EnumToString(timeFrame, 'ENUM_TIMEFRAMES') + ' '


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PivotPointsLinesV13(_MQL5Indicator):
    name = 'Pivot_Points_Lines_v1.3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'UniqueID': 1,  # Unique ID
        'historicalPP': 0,  # Historical Pivot Points,Set 0 for NONE
        'pivotSelection': _Choice({0: 'Standard(Floor)', 1: 'Fibonacci', 2: 'Camarilla', 3: 'Woodie', 4: 'Traditional', 5: 'Demark', 6: 'Classic'}, default=0),  # Formula
        'timeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # TimeFrame
        'drawFuturePlot': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Draw Future Plot?
        'showPriceLabel': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Show Price In Label?
        'useShortLines': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Draw Short Lines For Current Period?
        'ShiftLabel': 3,  # Label Follow Price Shift -Move Left, +Move Right
        'Line_Length': 15,  # Length Of Short Line
        'drawFloorMidPP': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Show Mid Pivot Points?
        'floorCPR': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Show Central Pivot Range?
        'lineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Line Style
        'lineWidth': 1,  # Line Width
        'labelFontSize': 8,  # Label Text Size
        'historicalLabelLocation': _Choice({0: 'Left', 1: 'Middle', 2: 'Right'}, default=0),  # Historical Label Location?
        'currentLabelLocation': _Choice({0: 'Follow Price', 1: 'Left', 2: 'Middle', 3: 'Right'}, default=0),  # Current Label Location?
        'futureLabelLocation': _Choice({0: 'Left', 1: 'Middle', 2: 'Right'}, default=2),  # Future Label Location?
        'hideHistoricalLabels': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Hide Historical Pivot Points Labels?
        'hideCurrentLabels': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Hide Current Pivot Points Labels?
        'hideFutureLabels': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Hide Future Pivot Points Labels?
        'useSameColorLabelChoice': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Label Use Same Color?
        'showStandardPivotR4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot R4
        'showStandardPivotR3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot R3
        'showStandardPivotR2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot R2
        'showStandardPivotR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot R1
        'showStandardPivotPP': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot PP
        'showStandardPivotS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot S1
        'showStandardPivotS2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot S2
        'showStandardPivotS3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot S3
        'showStandardPivotS4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot S4
        'showStandardPivotMR4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot MR4
        'showStandardPivotMR3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot MR3
        'showStandardPivotMR2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot MR2
        'showStandardPivotMR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot MR1
        'showStandardPivotMS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot MS1
        'showStandardPivotMS2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot MS2
        'showStandardPivotMS3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot MS3
        'showStandardPivotMS4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot MS4
        'showCPRTC': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard CPR Pivot TC
        'showCPRBC': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard CPR Pivot BC
        'showFibonacciPivotR200': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot R200
        'showFibonacciPivotR161': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot R161
        'showFibonacciPivotR138': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot R138
        'showFibonacciPivotR100': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot R100
        'showFibonacciPivotR78': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot R78
        'showFibonacciPivotR61': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot R61
        'showFibonacciPivotR38': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot R38
        'showFibonacciPivotPP': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot PP
        'showFibonacciPivotS38': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot S38
        'showFibonacciPivotS61': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot S61
        'showFibonacciPivotS78': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot S78
        'showFibonacciPivotS100': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot S100
        'showFibonacciPivotS138': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot S138
        'showFibonacciPivotS161': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot S161
        'showFibonacciPivotS200': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Fibonacci Pivot S200
        'showWoodieR4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot R4
        'showWoodieR3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot R3
        'showWoodieR2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot R2
        'showWoodieR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot R1
        'showWoodiePP': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot PP
        'showWoodieS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot S1
        'showWoodieS2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot S2
        'showWoodieS3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot S3
        'showWoodieS4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot S4
        'showCamarillaH5': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot H5
        'showCamarillaH4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot H4
        'showCamarillaH3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot H3
        'showCamarillaH2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot H2
        'showCamarillaH1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot H1
        'showCamarillaPP': _Choice({0: 'Disable', 1: 'Enable'}, default=0),  # Camarilla Pivot PP
        'showCamarillaL1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot L1
        'showCamarillaL2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot L2
        'showCamarillaL3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot L3
        'showCamarillaL4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot L4
        'showCamarillaL5': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot L5
        'showTraditionalR5': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot R5
        'showTraditionalR4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot R4
        'showTraditionalR3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot R3
        'showTraditionalR2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot R2
        'showTraditionalR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot R1
        'showTraditionalPP': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot PP
        'showTraditionalS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot S1
        'showTraditionalS2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot S2
        'showTraditionalS3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot S3
        'showTraditionalS4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot S4
        'showTraditionalS5': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Traditional Pivot S5
        'showDemarkR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Demark Pivot R1
        'showDemarkPP': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Demark Pivot PP
        'showDemarkS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Demark Pivot S1
        'showClassicR4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Classic Pivot R4
        'showClassicR3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Classic Pivot R3
        'showClassicR2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Classic Pivot R2
        'showClassicR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Classic Pivot R1
        'showClassicPP': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Classic Pivot PP
        'showClassicS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Classic Pivot S1
        'showClassicS2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Classic Pivot S2
        'showClassicS3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Classic Pivot S3
        'showClassicS4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Classic Pivot S4
    }

