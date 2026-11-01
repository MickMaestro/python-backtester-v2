"""Multi_Pair_Pivot_Point_Scanner_Alerts_v2.8 — converted from MQL5: MQL5 Indicators/Multi Pair Pivot Point Scanner Alerts 2.8/Multi_Pair_Pivot_Point_Scanner_Alerts_v2.8.mq5

Indicator Scans Multiple Symbol Pairs Looking For When The Price Crosses A Pivot Point or xx points near or bounced off pivot Then It Alerts The Trader.
Copyright: NickBixy; Link: https://www.forexfactory.com/showthread.php?t=904734

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'NickBixy', 'link': 'https://www.forexfactory.com/showthread.php?t=904734', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Indicator Scans Multiple Symbol Pairs Looking For When The Price Crosses A Pivot Point or xx points near or bounced off pivot Then It Alerts The Trader.'], 'name': 'Multi_Pair_Pivot_Point_Scanner_Alerts_v2.8', 'source': 'MQL5 Indicators/Multi Pair Pivot Point Scanner Alerts 2.8/Multi_Pair_Pivot_Point_Scanner_Alerts_v2.8.mq5', 'folder': 'Multi Pair Pivot Point Scanner Alerts 2.8', 'inputs': [{'mql': 'info', 'py': 'info', 'param': None, 'type': 'string', 'default': 'Put Scanner On A Separate Chart Tab From Trading Strategy', 'label': 'Put Scanner On A Separate Chart Tab From Trading Stategy', 'sinput': False}, {'mql': 'indiLink', 'py': 'indiLink', 'param': None, 'type': 'string', 'default': 'https://www.forexfactory.com/showthread.php?t=904734', 'label': "Indicator's thread on Forex Factory", 'sinput': False}, {'mql': 'refreshTime', 'py': 'refreshTime', 'param': 'refreshTime', 'type': 'int', 'default': 5, 'label': 'Refresh check every x Seconds', 'sinput': False}, {'mql': 'pivotPointHeader', 'py': 'pivotPointHeader', 'param': None, 'type': 'string', 'default': '-----------------Pivot Point Settings------------------------------------------', 'label': '----- Pivot Point Settings', 'sinput': False}, {'mql': 'pivotSelection', 'py': 'pivotSelection', 'param': 'pivotSelection', 'type': 'int', 'default': 0, 'label': 'Pivot Point Formula', 'sinput': False}, {'mql': 'pivotTimeframe', 'py': 'pivotTimeframe', 'param': 'pivotTimeframe', 'type': 'int', 'default': 16408, 'label': 'Pivot Point Timeframe', 'sinput': False}, {'mql': 'alertModeSelection', 'py': 'alertModeSelection', 'param': 'alertModeSelection', 'type': 'int', 'default': 0, 'label': 'Alert Mode to use', 'sinput': False}, {'mql': 'xxPoints', 'py': 'xxPoints', 'param': 'xxPoints', 'type': 'int', 'default': 50, 'label': 'Points Near Pivot - For Alert Mode Near', 'sinput': False}, {'mql': 'symbolHeader', 'py': 'symbolHeader', 'param': None, 'type': 'string', 'default': '-----------------Symbol Settings------------------------------------------', 'label': '----- Symbol Settings', 'sinput': False}, {'mql': 'symTypeChoice', 'py': 'symTypeChoice', 'param': 'symTypeChoice', 'type': 'int', 'default': 0, 'label': 'Symbols To Scan- Market Watch/Symbol List Below', 'sinput': False}, {'mql': 'symbols', 'py': 'symbols', 'param': None, 'type': 'string', 'default': 'AUDCAD,AUDCHF,AUDJPY,AUDNZD,AUDUSD,CADCHF,CADJPY,CHFJPY,EURAUD,EURCAD,EURCHF,EURGBP,EURJPY,EURNZD,EURUSD,GBPAUD,GBPCAD,GBPCHF,GBPJPY,GBPNZD,GBPUSD,NZDCAD,NZDCHF,NZDJPY,NZDUSD,USDCAD,USDCHF,USDJPY', 'label': 'Symbols To Scan', 'sinput': False}, {'mql': 'symbolPrefix', 'py': 'symbolPrefix', 'param': None, 'type': 'string', 'default': '', 'label': 'Symbol Prefix', 'sinput': False}, {'mql': 'symbolSuffix', 'py': 'symbolSuffix', 'param': None, 'type': 'string', 'default': '', 'label': 'Symbol Suffix', 'sinput': False}, {'mql': 'printoutAndAlertHeader', 'py': 'printoutAndAlertHeader', 'param': None, 'type': 'string', 'default': '-----------------Alert/Printout Settings--------------------------------------', 'label': '----- Alert/Printout Settings', 'sinput': False}, {'mql': 'alertInternalMinutes', 'py': 'alertInternalMinutes', 'param': 'alertInternalMinutes', 'type': 'int', 'default': 30, 'label': 'Alert Wait Time In Min for same Pivot alert Msg', 'sinput': False}, {'mql': 'popupAlerts', 'py': 'popupAlerts', 'param': 'popupAlerts', 'type': 'int', 'default': 1, 'label': 'Use Popup Alerts?', 'sinput': False}, {'mql': 'notificationAlerts', 'py': 'notificationAlerts', 'param': 'notificationAlerts', 'type': 'int', 'default': 1, 'label': 'Use Notification Alerts?', 'sinput': False}, {'mql': 'emailAlerts', 'py': 'emailAlerts', 'param': 'emailAlerts', 'type': 'int', 'default': 0, 'label': 'Use Email Alerts?', 'sinput': False}, {'mql': 'showBidPriceOnAlert', 'py': 'showBidPriceOnAlert', 'param': 'showBidPriceOnAlert', 'type': 'int', 'default': 0, 'label': 'Show Bid Price in Alert Msg', 'sinput': False}, {'mql': 'printOutPivotPoints', 'py': 'printOutPivotPoints', 'param': 'printOutPivotPoints', 'type': 'int', 'default': 0, 'label': 'Print Out Pivot Values - For Testing Values', 'sinput': False}, {'mql': 'printOutPivotPointsSymbolIndex', 'py': 'printOutPivotPointsSymbolIndex', 'param': 'printOutPivotPointsSymbolIndex', 'type': 'int', 'default': 0, 'label': 'Index Value Of Symbol To Print Out', 'sinput': False}, {'mql': 'bouncedHeader', 'py': 'bouncedHeader', 'param': None, 'type': 'string', 'default': '-----------------Bounced Mode Alerts Settings------------------------------------------', 'label': '----- Bounce Settings', 'sinput': False}, {'mql': 'bouncedCandleTF', 'py': 'bouncedCandleTF', 'param': 'bouncedCandleTF', 'type': 'int', 'default': 15, 'label': 'Time Frame Candles For Bounced Alerts', 'sinput': False}, {'mql': 'candleColorFilter', 'py': 'candleColorFilter', 'param': 'candleColorFilter', 'type': 'int', 'default': 1, 'label': 'Use Candle Color Filter', 'sinput': False}, {'mql': 'bounceXBarsWait', 'py': 'bounceXBarsWait', 'param': 'bounceXBarsWait', 'type': 'int', 'default': 0, 'label': 'Alert Wait Time In Bars for same Pivot alert Msg', 'sinput': False}, {'mql': 'offResistanceBounceMSG', 'py': 'offResistanceBounceMSG', 'param': None, 'type': 'string', 'default': ' - Price Crossed Then Closed Below', 'label': 'Msg For Bounce Off Resistance', 'sinput': False}, {'mql': 'offSupportBounceMSG', 'py': 'offSupportBounceMSG', 'param': None, 'type': 'string', 'default': ' - Price Crossed Then Closed Above', 'label': 'Msg For Bounce Off Support', 'sinput': False}, {'mql': 'bbFilterHeader', 'py': 'bbFilterHeader', 'param': None, 'type': 'string', 'default': '-----------------Bollinger Bands Filter Settings------------------------------------------', 'label': '----- Bollinger Bands Filter', 'sinput': False}, {'mql': 'note', 'py': 'note', 'param': None, 'type': 'string', 'default': 'Near/Cross/Bounce Alerts only when price is above upper band or when price is below lower band', 'label': 'Filter note', 'sinput': False}, {'mql': 'useBollingerBands', 'py': 'useBollingerBands', 'param': 'useBollingerBands', 'type': 'int', 'default': 0, 'label': 'Use BollingerBands upper/lower Filter', 'sinput': False}, {'mql': 'BBtimeFrame', 'py': 'BBtimeFrame', 'param': 'BBtimeFrame', 'type': 'int', 'default': 30, 'label': 'Bollinger Bands: Timeframe', 'sinput': False}, {'mql': 'BBperiod', 'py': 'BBperiod', 'param': 'BBperiod', 'type': 'int', 'default': 20, 'label': 'Bollinger Bands: Period', 'sinput': False}, {'mql': 'BBdeviation', 'py': 'BBdeviation', 'param': 'BBdeviation', 'type': 'double', 'default': 2.0, 'label': 'Bollinger Bands: Deviations', 'sinput': False}, {'mql': 'BBShift', 'py': 'BBShift', 'param': 'BBShift', 'type': 'int', 'default': 0, 'label': 'Bollinger Bands: Shift', 'sinput': False}, {'mql': 'BBAppliedPrice', 'py': 'BBAppliedPrice', 'param': 'BBAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Bollinger Bands: Apply to', 'sinput': False}, {'mql': 'showAlertsHeader', 'py': 'showAlertsHeader', 'param': None, 'type': 'string', 'default': '-----------------Enable/Disable Alerts For Specified Pivot Point----------------------------------------------', 'label': '----- Will Affect All the Alert Modes', 'sinput': False}, {'mql': 'showAlertsStandardPivotHeader', 'py': 'showAlertsStandardPivotHeader', 'param': None, 'type': 'string', 'default': 'Standard Pivot Point--------------------------------------------', 'label': '----- Standard Pivot Point Settings', 'sinput': False}, {'mql': 'MidPointAlerts', 'py': 'MidPointAlerts', 'param': 'MidPointAlerts', 'type': 'int', 'default': 0, 'label': 'Mid Pivot Point Alerts', 'sinput': False}, {'mql': 'showStandardPivotR4', 'py': 'showStandardPivotR4', 'param': 'showStandardPivotR4', 'type': 'int', 'default': 1, 'label': 'Standard Pivot R4', 'sinput': False}, {'mql': 'showStandardPivotR3', 'py': 'showStandardPivotR3', 'param': 'showStandardPivotR3', 'type': 'int', 'default': 1, 'label': 'Standard Pivot R3', 'sinput': False}, {'mql': 'showStandardPivotR2', 'py': 'showStandardPivotR2', 'param': 'showStandardPivotR2', 'type': 'int', 'default': 1, 'label': 'Standard Pivot R2', 'sinput': False}, {'mql': 'showStandardPivotR1', 'py': 'showStandardPivotR1', 'param': 'showStandardPivotR1', 'type': 'int', 'default': 1, 'label': 'Standard Pivot R1', 'sinput': False}, {'mql': 'showStandardPivotPP', 'py': 'showStandardPivotPP', 'param': 'showStandardPivotPP', 'type': 'int', 'default': 1, 'label': 'Standard Pivot PP', 'sinput': False}, {'mql': 'showStandardPivotS1', 'py': 'showStandardPivotS1', 'param': 'showStandardPivotS1', 'type': 'int', 'default': 1, 'label': 'Standard Pivot S1', 'sinput': False}, {'mql': 'showStandardPivotS2', 'py': 'showStandardPivotS2', 'param': 'showStandardPivotS2', 'type': 'int', 'default': 1, 'label': 'Standard Pivot S2', 'sinput': False}, {'mql': 'showStandardPivotS3', 'py': 'showStandardPivotS3', 'param': 'showStandardPivotS3', 'type': 'int', 'default': 1, 'label': 'Standard Pivot S3', 'sinput': False}, {'mql': 'showStandardPivotS4', 'py': 'showStandardPivotS4', 'param': 'showStandardPivotS4', 'type': 'int', 'default': 1, 'label': 'Standard Pivot S4', 'sinput': False}, {'mql': 'StandardMidPivotHeader', 'py': 'StandardMidPivotHeader', 'param': None, 'type': 'string', 'default': '-----------------Standard Mid Pivot Points', 'label': '----- Standard Mid PP', 'sinput': False}, {'mql': 'showStandardPivotMR4', 'py': 'showStandardPivotMR4', 'param': 'showStandardPivotMR4', 'type': 'int', 'default': 1, 'label': 'Standard Pivot mR4', 'sinput': False}, {'mql': 'showStandardPivotMR3', 'py': 'showStandardPivotMR3', 'param': 'showStandardPivotMR3', 'type': 'int', 'default': 1, 'label': 'Standard Pivot mR3', 'sinput': False}, {'mql': 'showStandardPivotMR2', 'py': 'showStandardPivotMR2', 'param': 'showStandardPivotMR2', 'type': 'int', 'default': 1, 'label': 'Standard Pivot mR2', 'sinput': False}, {'mql': 'showStandardPivotMR1', 'py': 'showStandardPivotMR1', 'param': 'showStandardPivotMR1', 'type': 'int', 'default': 1, 'label': 'Standard Pivot mR1', 'sinput': False}, {'mql': 'showStandardPivotMS1', 'py': 'showStandardPivotMS1', 'param': 'showStandardPivotMS1', 'type': 'int', 'default': 1, 'label': 'Standard Pivot mS1', 'sinput': False}, {'mql': 'showStandardPivotMS2', 'py': 'showStandardPivotMS2', 'param': 'showStandardPivotMS2', 'type': 'int', 'default': 1, 'label': 'Standard Pivot mS2', 'sinput': False}, {'mql': 'showStandardPivotMS3', 'py': 'showStandardPivotMS3', 'param': 'showStandardPivotMS3', 'type': 'int', 'default': 1, 'label': 'Standard Pivot mS3', 'sinput': False}, {'mql': 'showStandardPivotMS4', 'py': 'showStandardPivotMS4', 'param': 'showStandardPivotMS4', 'type': 'int', 'default': 1, 'label': 'Standard Pivot mS4', 'sinput': False}, {'mql': 'showAlertsFibonacciPivotHeader', 'py': 'showAlertsFibonacciPivotHeader', 'param': None, 'type': 'string', 'default': 'Fibonacci Pivot Point--------------------------------------------', 'label': '----- Fibonacci Pivot Point Settings', 'sinput': False}, {'mql': 'showFibonacciPivotR200', 'py': 'showFibonacciPivotR200', 'param': 'showFibonacciPivotR200', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R200', 'sinput': False}, {'mql': 'showFibonacciPivotR161', 'py': 'showFibonacciPivotR161', 'param': 'showFibonacciPivotR161', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R161', 'sinput': False}, {'mql': 'showFibonacciPivotR138', 'py': 'showFibonacciPivotR138', 'param': 'showFibonacciPivotR138', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R138', 'sinput': False}, {'mql': 'showFibonacciPivotR100', 'py': 'showFibonacciPivotR100', 'param': 'showFibonacciPivotR100', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R100', 'sinput': False}, {'mql': 'showFibonacciPivotR78', 'py': 'showFibonacciPivotR78', 'param': 'showFibonacciPivotR78', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R78', 'sinput': False}, {'mql': 'showFibonacciPivotR61', 'py': 'showFibonacciPivotR61', 'param': 'showFibonacciPivotR61', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R61', 'sinput': False}, {'mql': 'showFibonacciPivotR38', 'py': 'showFibonacciPivotR38', 'param': 'showFibonacciPivotR38', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot R38', 'sinput': False}, {'mql': 'showFibonacciPivotPP', 'py': 'showFibonacciPivotPP', 'param': 'showFibonacciPivotPP', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot PP', 'sinput': False}, {'mql': 'showFibonacciPivotS38', 'py': 'showFibonacciPivotS38', 'param': 'showFibonacciPivotS38', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S38', 'sinput': False}, {'mql': 'showFibonacciPivotS61', 'py': 'showFibonacciPivotS61', 'param': 'showFibonacciPivotS61', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S61', 'sinput': False}, {'mql': 'showFibonacciPivotS78', 'py': 'showFibonacciPivotS78', 'param': 'showFibonacciPivotS78', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S78', 'sinput': False}, {'mql': 'showFibonacciPivotS100', 'py': 'showFibonacciPivotS100', 'param': 'showFibonacciPivotS100', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S100', 'sinput': False}, {'mql': 'showFibonacciPivotS138', 'py': 'showFibonacciPivotS138', 'param': 'showFibonacciPivotS138', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S138', 'sinput': False}, {'mql': 'showFibonacciPivotS161', 'py': 'showFibonacciPivotS161', 'param': 'showFibonacciPivotS161', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S161', 'sinput': False}, {'mql': 'showFibonacciPivotS200', 'py': 'showFibonacciPivotS200', 'param': 'showFibonacciPivotS200', 'type': 'int', 'default': 1, 'label': 'Fibonacci Pivot S200', 'sinput': False}, {'mql': 'showAlertsWoodiePivotHeader', 'py': 'showAlertsWoodiePivotHeader', 'param': None, 'type': 'string', 'default': 'Woodie Pivot Point--------------------------------------------', 'label': '----- Woodie Pivot Point Settings', 'sinput': False}, {'mql': 'showWoodieR1', 'py': 'showWoodieR1', 'param': 'showWoodieR1', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot R1', 'sinput': False}, {'mql': 'showWoodieR2', 'py': 'showWoodieR2', 'param': 'showWoodieR2', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot R2', 'sinput': False}, {'mql': 'showWoodiePP', 'py': 'showWoodiePP', 'param': 'showWoodiePP', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot PP', 'sinput': False}, {'mql': 'showWoodieS1', 'py': 'showWoodieS1', 'param': 'showWoodieS1', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot S1', 'sinput': False}, {'mql': 'showWoodieS2', 'py': 'showWoodieS2', 'param': 'showWoodieS2', 'type': 'int', 'default': 1, 'label': 'Woodie Pivot S2', 'sinput': False}, {'mql': 'showAlertsCamarillaPivotHeader', 'py': 'showAlertsCamarillaPivotHeader', 'param': None, 'type': 'string', 'default': 'Camarilla Pivot Point--------------------------------------------', 'label': '----- Camarilla Pivot Point Settings', 'sinput': False}, {'mql': 'showCamarillaR1', 'py': 'showCamarillaR1', 'param': 'showCamarillaR1', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot R1', 'sinput': False}, {'mql': 'showCamarillaR2', 'py': 'showCamarillaR2', 'param': 'showCamarillaR2', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot R2', 'sinput': False}, {'mql': 'showCamarillaR3', 'py': 'showCamarillaR3', 'param': 'showCamarillaR3', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot R3', 'sinput': False}, {'mql': 'showCamarillaR4', 'py': 'showCamarillaR4', 'param': 'showCamarillaR4', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot R4', 'sinput': False}, {'mql': 'showCamarillaR5', 'py': 'showCamarillaR5', 'param': 'showCamarillaR5', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot R5', 'sinput': False}, {'mql': 'showCamarillaPP', 'py': 'showCamarillaPP', 'param': 'showCamarillaPP', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot PP', 'sinput': False}, {'mql': 'showCamarillaS1', 'py': 'showCamarillaS1', 'param': 'showCamarillaS1', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot S1', 'sinput': False}, {'mql': 'showCamarillaS2', 'py': 'showCamarillaS2', 'param': 'showCamarillaS2', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot S2', 'sinput': False}, {'mql': 'showCamarillaS3', 'py': 'showCamarillaS3', 'param': 'showCamarillaS3', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot S3', 'sinput': False}, {'mql': 'showCamarillaS4', 'py': 'showCamarillaS4', 'param': 'showCamarillaS4', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot S4', 'sinput': False}, {'mql': 'showCamarillaS5', 'py': 'showCamarillaS5', 'param': 'showCamarillaS5', 'type': 'int', 'default': 1, 'label': 'Camarilla Pivot S5', 'sinput': False}, {'mql': 'dashBoardHeader', 'py': 'dashBoardHeader', 'param': None, 'type': 'string', 'default': '-----------------Dashboard Settings--------------------------------------', 'label': '----- Dashboard Settings', 'sinput': False}, {'mql': 'useDashboard', 'py': 'useDashboard', 'param': 'useDashboard', 'type': 'int', 'default': 1, 'label': 'Use DashBoard?', 'sinput': False}, {'mql': 'widthX', 'py': 'widthX', 'param': 'widthX', 'type': 'int', 'default': 28, 'label': 'X Dashboard +Moves right, -Moves left', 'sinput': False}, {'mql': 'widthY', 'py': 'widthY', 'param': 'widthY', 'type': 'int', 'default': 28, 'label': 'Y Dashboard +Moves down, -Moves up', 'sinput': False}, {'mql': 'symbolPivotXSpacing', 'py': 'symbolPivotXSpacing', 'param': 'symbolPivotXSpacing', 'type': 'int', 'default': 85, 'label': 'X  Between Columns Symbol-PP Nearest', 'sinput': False}, {'mql': 'pivotPivotAlertXSpacing', 'py': 'pivotPivotAlertXSpacing', 'param': 'pivotPivotAlertXSpacing', 'type': 'int', 'default': 50, 'label': 'X  Between Columns PP Nearest-PP Alert', 'sinput': False}, {'mql': 'pivotAlertTimeLastXSpacing', 'py': 'pivotAlertTimeLastXSpacing', 'param': 'pivotAlertTimeLastXSpacing', 'type': 'int', 'default': 35, 'label': 'X  Between Columns PP Alert-Time Last', 'sinput': False}, {'mql': 'FontHeader', 'py': 'FontHeader', 'param': None, 'type': 'string', 'default': 'Arial Bold', 'label': 'Font of the headers', 'sinput': False}, {'mql': 'Font', 'py': 'Font', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'font of the labels', 'sinput': False}, {'mql': 'fontText', 'py': 'fontText', 'param': 'fontText', 'type': 'int', 'default': 9, 'label': 'Font Size Labels', 'sinput': False}, {'mql': 'textH', 'py': 'textH', 'param': 'textH', 'type': 'int', 'default': 14, 'label': 'Y Spacing Between Rows', 'sinput': False}, {'mql': 'headerColors', 'py': 'headerColors', 'param': None, 'type': 'color', 'default': 15631086, 'label': 'Color of Header', 'sinput': False}, {'mql': 'symbolColor', 'py': 'symbolColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'Color of Symbol Rows', 'sinput': False}, {'mql': 'timeChoiceOption', 'py': 'timeChoiceOption', 'param': 'timeChoiceOption', 'type': 'int', 'default': 1, 'label': 'Local/Server Time For Time Last Alert', 'sinput': False}, {'mql': 'resistantColor', 'py': 'resistantColor', 'param': None, 'type': 'color', 'default': 17919, 'label': 'Resistant PP Color', 'sinput': False}, {'mql': 'supportColor', 'py': 'supportColor', 'param': None, 'type': 'color', 'default': 64636, 'label': 'Support PP Color', 'sinput': False}, {'mql': 'pivotColor', 'py': 'pivotColor', 'param': None, 'type': 'color', 'default': 55295, 'label': 'Pivot Color', 'sinput': False}, {'mql': 'listLabelSize', 'py': 'listLabelSize', 'param': 'listLabelSize', 'type': 'int', 'default': 40, 'label': 'Num Of Alert Msg In List Below', 'sinput': False}, {'mql': 'usePivotColor', 'py': 'usePivotColor', 'param': 'usePivotColor', 'type': 'bool', 'default': False, 'label': 'Label Color use res/sup/piv colors for alerts', 'sinput': False}, {'mql': 'listLabelColor', 'py': 'listLabelColor', 'param': None, 'type': 'color', 'default': 13959039, 'label': 'List Label Color', 'sinput': False}, {'mql': 'timeLastAlertColor', 'py': 'timeLastAlertColor', 'param': None, 'type': 'color', 'default': 13959039, 'label': 'Time Last Alert Label Color', 'sinput': False}, {'mql': 'openChartTimeFrame', 'py': 'openChartTimeFrame', 'param': 'openChartTimeFrame', 'type': 'int', 'default': 16385, 'label': 'Open Chart TimeFrame', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

ERR_CHART_CANNOT_CHANGE = 0  # MQL5 constant unknown to the converter

# enum pivotTypes
Standard = 0
Fibonacci = 1
Camarilla = 2
Woodie = 3
_enum('pivotTypes', {0: 'Standard', 1: 'Fibonacci', 2: 'Camarilla', 3: 'Woodie'})

# enum yesnoChoiceToggle
No = 0
Yes = 1
_enum('yesnoChoiceToggle', {0: 'No', 1: 'Yes'})

# enum timeChoice
Server = 0
Local = 1
_enum('timeChoice', {0: 'Server', 1: 'Local'})

# enum symbolTypeChoice
MarketWatch = 0
SymbolList = 1
_enum('symbolTypeChoice', {0: 'MarketWatch', 1: 'SymbolList'})

# enum alertMode
Cross_Alerts = 0
Near_Alerts = 1
Cross_And_Bounce_Alerts = 2
Near_And_Bounce_Alerts = 3
Bounce_Only_Alerts = 4
_enum('alertMode', {0: 'Cross_Alerts', 1: 'Near_Alerts', 2: 'Cross_And_Bounce_Alerts', 3: 'Near_And_Bounce_Alerts', 4: 'Bounce_Only_Alerts'})

# enum enabledisableChoiceToggle
Disable = 0
Enable = 1
_enum('enabledisableChoiceToggle', {0: 'Disable', 1: 'Enable'})

# ---- inputs and global variables
info = _input('info', 'Put Scanner On A Separate Chart Tab From Trading Strategy')  # Put Scanner On A Separate Chart Tab From Trading Stategy
indiLink = _input('indiLink', 'https://www.forexfactory.com/showthread.php?t=904734')  # Indicator's thread on Forex Factory
refreshTime = _input('refreshTime', 5)  # Refresh check every x Seconds
pivotPointHeader = _input('pivotPointHeader', '-----------------Pivot Point Settings------------------------------------------')  # ----- Pivot Point Settings
pivotSelection = _input('pivotSelection', Standard)  # Pivot Point Formula
pivotTimeframe = _input('pivotTimeframe', PERIOD_D1)  # Pivot Point Timeframe
alertModeSelection = _input('alertModeSelection', Cross_Alerts)  # Alert Mode to use
xxPoints = _input('xxPoints', 50)  # Points Near Pivot - For Alert Mode Near
pointsNearMessage = 'is Near'  # PointsNear Alert Msg
crossedMessage = 'Crossed'  # Cross Alert Msg
symbolHeader = _input('symbolHeader', '-----------------Symbol Settings------------------------------------------')  # ----- Symbol Settings
symTypeChoice = _input('symTypeChoice', MarketWatch)  # Symbols To Scan- Market Watch/Symbol List Below
symbols = _input('symbols', 'AUDCAD,AUDCHF,AUDJPY,AUDNZD,AUDUSD,CADCHF,CADJPY,CHFJPY,EURAUD,EURCAD,EURCHF,EURGBP,EURJPY,EURNZD,EURUSD,GBPAUD,GBPCAD,GBPCHF,GBPJPY,GBPNZD,GBPUSD,NZDCAD,NZDCHF,NZDJPY,NZDUSD,USDCAD,USDCHF,USDJPY')  # Symbols To Scan
symbolPrefix = _input('symbolPrefix', '')  # Symbol Prefix
symbolSuffix = _input('symbolSuffix', '')  # Symbol Suffix
printoutAndAlertHeader = _input('printoutAndAlertHeader', '-----------------Alert/Printout Settings--------------------------------------')  # ----- Alert/Printout Settings
alertInternalMinutes = _input('alertInternalMinutes', 30)  # Alert Wait Time In Min for same Pivot alert Msg
popupAlerts = _input('popupAlerts', Yes)  # Use Popup Alerts?
notificationAlerts = _input('notificationAlerts', Yes)  # Use Notification Alerts?
emailAlerts = _input('emailAlerts', No)  # Use Email Alerts?
showBidPriceOnAlert = _input('showBidPriceOnAlert', No)  # Show Bid Price in Alert Msg
printOutPivotPoints = _input('printOutPivotPoints', No)  # Print Out Pivot Values - For Testing Values
printOutPivotPointsSymbolIndex = _input('printOutPivotPointsSymbolIndex', 0)  # Index Value Of Symbol To Print Out
bouncedHeader = _input('bouncedHeader', '-----------------Bounced Mode Alerts Settings------------------------------------------')  # ----- Bounce Settings
bouncedCandleTF = _input('bouncedCandleTF', PERIOD_M15)  # Time Frame Candles For Bounced Alerts
candleColorFilter = _input('candleColorFilter', Yes)  # Use Candle Color Filter
bounceXBarsWait = _input('bounceXBarsWait', 0)  # Alert Wait Time In Bars for same Pivot alert Msg
offResistanceBounceMSG = _input('offResistanceBounceMSG', ' - Price Crossed Then Closed Below')  # Msg For Bounce Off Resistance
offSupportBounceMSG = _input('offSupportBounceMSG', ' - Price Crossed Then Closed Above')  # Msg For Bounce Off Support
bbFilterHeader = _input('bbFilterHeader', '-----------------Bollinger Bands Filter Settings------------------------------------------')  # ----- Bollinger Bands Filter
note = _input('note', 'Near/Cross/Bounce Alerts only when price is above upper band or when price is below lower band')  # Filter note
useBollingerBands = _input('useBollingerBands', No)  # Use BollingerBands upper/lower Filter
BBtimeFrame = _input('BBtimeFrame', PERIOD_M30)  # Bollinger Bands: Timeframe
BBperiod = _input('BBperiod', 20)  # Bollinger Bands: Period
BBdeviation = _input('BBdeviation', 2.0)  # Bollinger Bands: Deviations
BBShift = _input('BBShift', 0)  # Bollinger Bands: Shift
BBAppliedPrice = _input('BBAppliedPrice', PRICE_CLOSE)  # Bollinger Bands: Apply to
showAlertsHeader = _input('showAlertsHeader', '-----------------Enable/Disable Alerts For Specified Pivot Point----------------------------------------------')  # ----- Will Affect All the Alert Modes
showAlertsStandardPivotHeader = _input('showAlertsStandardPivotHeader', 'Standard Pivot Point--------------------------------------------')  # ----- Standard Pivot Point Settings
MidPointAlerts = _input('MidPointAlerts', Disable)  # Mid Pivot Point Alerts
showStandardPivotR4 = _input('showStandardPivotR4', Enable)  # Standard Pivot R4
showStandardPivotR3 = _input('showStandardPivotR3', Enable)  # Standard Pivot R3
showStandardPivotR2 = _input('showStandardPivotR2', Enable)  # Standard Pivot R2
showStandardPivotR1 = _input('showStandardPivotR1', Enable)  # Standard Pivot R1
showStandardPivotPP = _input('showStandardPivotPP', Enable)  # Standard Pivot PP
showStandardPivotS1 = _input('showStandardPivotS1', Enable)  # Standard Pivot S1
showStandardPivotS2 = _input('showStandardPivotS2', Enable)  # Standard Pivot S2
showStandardPivotS3 = _input('showStandardPivotS3', Enable)  # Standard Pivot S3
showStandardPivotS4 = _input('showStandardPivotS4', Enable)  # Standard Pivot S4
StandardMidPivotHeader = _input('StandardMidPivotHeader', '-----------------Standard Mid Pivot Points')  # ----- Standard Mid PP
showStandardPivotMR4 = _input('showStandardPivotMR4', Enable)  # Standard Pivot mR4
showStandardPivotMR3 = _input('showStandardPivotMR3', Enable)  # Standard Pivot mR3
showStandardPivotMR2 = _input('showStandardPivotMR2', Enable)  # Standard Pivot mR2
showStandardPivotMR1 = _input('showStandardPivotMR1', Enable)  # Standard Pivot mR1
showStandardPivotMS1 = _input('showStandardPivotMS1', Enable)  # Standard Pivot mS1
showStandardPivotMS2 = _input('showStandardPivotMS2', Enable)  # Standard Pivot mS2
showStandardPivotMS3 = _input('showStandardPivotMS3', Enable)  # Standard Pivot mS3
showStandardPivotMS4 = _input('showStandardPivotMS4', Enable)  # Standard Pivot mS4
showAlertsFibonacciPivotHeader = _input('showAlertsFibonacciPivotHeader', 'Fibonacci Pivot Point--------------------------------------------')  # ----- Fibonacci Pivot Point Settings
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
showAlertsWoodiePivotHeader = _input('showAlertsWoodiePivotHeader', 'Woodie Pivot Point--------------------------------------------')  # ----- Woodie Pivot Point Settings
showWoodieR1 = _input('showWoodieR1', Enable)  # Woodie Pivot R1
showWoodieR2 = _input('showWoodieR2', Enable)  # Woodie Pivot R2
showWoodiePP = _input('showWoodiePP', Enable)  # Woodie Pivot PP
showWoodieS1 = _input('showWoodieS1', Enable)  # Woodie Pivot S1
showWoodieS2 = _input('showWoodieS2', Enable)  # Woodie Pivot S2
showAlertsCamarillaPivotHeader = _input('showAlertsCamarillaPivotHeader', 'Camarilla Pivot Point--------------------------------------------')  # ----- Camarilla Pivot Point Settings
showCamarillaR1 = _input('showCamarillaR1', Enable)  # Camarilla Pivot R1
showCamarillaR2 = _input('showCamarillaR2', Enable)  # Camarilla Pivot R2
showCamarillaR3 = _input('showCamarillaR3', Enable)  # Camarilla Pivot R3
showCamarillaR4 = _input('showCamarillaR4', Enable)  # Camarilla Pivot R4
showCamarillaR5 = _input('showCamarillaR5', Enable)  # Camarilla Pivot R5
showCamarillaPP = _input('showCamarillaPP', Enable)  # Camarilla Pivot PP
showCamarillaS1 = _input('showCamarillaS1', Enable)  # Camarilla Pivot S1
showCamarillaS2 = _input('showCamarillaS2', Enable)  # Camarilla Pivot S2
showCamarillaS3 = _input('showCamarillaS3', Enable)  # Camarilla Pivot S3
showCamarillaS4 = _input('showCamarillaS4', Enable)  # Camarilla Pivot S4
showCamarillaS5 = _input('showCamarillaS5', Enable)  # Camarilla Pivot S5
numSymbols = 0  # the number of symbols to scan
alertIntervalTimeSeconds = 0  # wait time between same alert message for pivot point
symbolList = Arr(0, "")  # array of symbols
symbolListFinal = Arr(0, "")  # array of symbols after merging post and prefix
symbolTimeframeTimeP = Arr(0, 0)  # array of symbol dates today used for checking for new day for each symbol
Pivots = Arr(0, 0.0, dims=(20,))  # stores all the pivot points for each timeframe
PivotsCheck = Arr(0, 0.0, dims=(20,))  # stores all the pivot points for each timeframe
PivotsFlag = Arr(0, False, dims=(20,))
PivotsWaitTill = Arr(0, 0, dims=(20,))
PivotsZoneFlag = Arr(0, False, dims=(20,))
numPPStandard = 17
numPPCamarilla = 11
numPPWoodie = 5
numPPFibonacci = 15
showStandard = Arr(17, False, dyn=False)
standardPivotNames = Arr.of(['Pivot', 'S1', 'S2', 'S3', 'R1', 'R2', 'R3', 'R4', 'S4', 'mR4', 'mR3', 'mR2', 'mR1', 'mS1', 'mS2', 'mS3', 'mS4'], fill="")
showCamarilla = Arr(11, False, dyn=False)
camarillaPivotNames = Arr.of(['Pivot', 'S1', 'S2', 'S3', 'S4', 'R1', 'R2', 'R3', 'R4', 'R5', 'S5'], fill="")
showWoodie = Arr(5, False, dyn=False)
woodiePivotNames = Arr.of(['Pivot', 'S1', 'S2', 'R1', 'R2'], fill="")
showFibonacci = Arr(15, False, dyn=False)
fibonacciPivotNames = Arr.of(['Pivot', 'R38', 'R61', 'R78', 'R100', 'R138', 'R161', 'R200', 'S38', 'S61', 'S78', 'S100', 'S138', 'S161', 'S200'], fill="")
pivotTimeframeName = ""
symbolNewCandleCheck = Arr(0, 0, dims=(1,))  # keep track of current candle time so will know if new candle starts
bouncedWaitTill = Arr(0, 0, dims=(20,))
symbolPPIndex = Arr(0, 0, dims=(1,))  # keep track of the pivot point index that was crossed for all symbols in list, they start all set to -1
PivotState = Arr(0, 0, dims=(1,))
dashBoardHeader = _input('dashBoardHeader', '-----------------Dashboard Settings--------------------------------------')  # ----- Dashboard Settings
useDashboard = _input('useDashboard', Yes)  # Use DashBoard?
widthX = _input('widthX', 28)  # X Dashboard +Moves right, -Moves left
widthY = _input('widthY', 28)  # Y Dashboard +Moves down, -Moves up
symbolPivotXSpacing = _input('symbolPivotXSpacing', 85)  # X  Between Columns Symbol-PP Nearest
pivotPivotAlertXSpacing = _input('pivotPivotAlertXSpacing', 50)  # X  Between Columns PP Nearest-PP Alert
pivotAlertTimeLastXSpacing = _input('pivotAlertTimeLastXSpacing', 35)  # X  Between Columns PP Alert-Time Last
FontHeader = _input('FontHeader', 'Arial Bold')  # Font of the headers
Font = _input('Font', 'Arial')  # font of the labels
fontText = _input('fontText', 9)  # Font Size Labels
textH = _input('textH', 14)  # Y Spacing Between Rows
headerColors = _input('headerColors', clrViolet)  # Color of Header
symbolColor = _input('symbolColor', clrWhite)  # Color of Symbol Rows
textHEnd = 0
timeChoiceOption = _input('timeChoiceOption', Local)  # Local/Server Time For Time Last Alert
resistantColor = _input('resistantColor', clrOrangeRed)  # Resistant PP Color
supportColor = _input('supportColor', clrLawnGreen)  # Support PP Color
pivotColor = _input('pivotColor', clrGold)  # Pivot Color
listLabelSize = _input('listLabelSize', 40)  # Num Of Alert Msg In List Below
usePivotColor = _input('usePivotColor', False)  # Label Color use res/sup/piv colors for alerts
listLabelColor = _input('listLabelColor', clrAquamarine)  # List Label Color
timeLastAlertColor = _input('timeLastAlertColor', clrAquamarine)  # Time Last Alert Label Color
listLabelNames = Arr(0, "")
openChartTimeFrame = _input('openChartTimeFrame', PERIOD_H1)  # Open Chart TimeFrame

def TFMigrate(tf):
    _sw1 = tf
    if _sw1 == 0:
        return PERIOD_CURRENT
    elif _sw1 == 1:
        return PERIOD_M1
    elif _sw1 == 5:
        return PERIOD_M5
    elif _sw1 == 15:
        return PERIOD_M15
    elif _sw1 == 30:
        return PERIOD_M30
    elif _sw1 == 60:
        return PERIOD_H1
    elif _sw1 == 240:
        return PERIOD_H4
    elif _sw1 == 1440:
        return PERIOD_D1
    elif _sw1 == 10080:
        return PERIOD_W1
    elif _sw1 == 43200:
        return PERIOD_MN1
    elif _sw1 == 2:
        return PERIOD_M2
    elif _sw1 == 3:
        return PERIOD_M3
    elif _sw1 == 4:
        return PERIOD_M4
    elif _sw1 == 6:
        return PERIOD_M6
    elif _sw1 == 10:
        return PERIOD_M10
    elif _sw1 == 12:
        return PERIOD_M12
    elif _sw1 == 16385:
        return PERIOD_H1
    elif _sw1 == 16386:
        return PERIOD_H2
    elif _sw1 == 16387:
        return PERIOD_H3
    elif _sw1 == 16388:
        return PERIOD_H4
    elif _sw1 == 16390:
        return PERIOD_H6
    elif _sw1 == 16392:
        return PERIOD_H8
    elif _sw1 == 16396:
        return PERIOD_H12
    elif _sw1 == 16408:
        return PERIOD_D1
    elif _sw1 == 32769:
        return PERIOD_W1
    elif _sw1 == 49153:
        return PERIOD_MN1
    else:
        return PERIOD_CURRENT

def MethodMigrate(method):
    _sw2 = method
    if _sw2 == 0:
        return MODE_SMA
    elif _sw2 == 1:
        return MODE_EMA
    elif _sw2 == 2:
        return MODE_SMMA
    elif _sw2 == 3:
        return MODE_LWMA
    else:
        return MODE_SMA

def OnInit():
    global alertIntervalTimeSeconds, numSymbols, pivotTimeframeName
    if EventSetTimer(refreshTime) == False:
        Alert('ERROR CODE: ' + _str(GetLastError()))
    IndicatorSetString(INDICATOR_SHORTNAME, indiName)
    ObjectsDeleteAll(0, indiName, 0, OBJ_LABEL)
    alertIntervalTimeSeconds = alertInternalMinutes * 60
    updateSpecifiedPivotPointAlerts()
    if symTypeChoice == MarketWatch:
        numSymbolsMarketWatch = SymbolsTotal(True)
        numSymbols = numSymbolsMarketWatch
        ArrayResize(symbolListFinal, numSymbolsMarketWatch)
        for i in range(0, numSymbolsMarketWatch):
            symbolListFinal[i] = SymbolName(i, True)
    elif symTypeChoice == SymbolList:
        getSymbols()
    if testSymbols():
        if useDashboard == Yes:
            ArrayResize(listLabelNames, listLabelSize)
            for k in range(0, ArraySize(listLabelNames)):
                listLabelNames[k] = _str(k)
            CreateLabels()
        initializePivotPoints_1()
        _sw3 = pivotTimeframe
        if _sw3 == PERIOD_M1:
            pivotTimeframeName = 'M1 '
        elif _sw3 == PERIOD_M5:
            pivotTimeframeName = 'M5 '
        elif _sw3 == PERIOD_M15:
            pivotTimeframeName = 'M15 '
        elif _sw3 == PERIOD_M30:
            pivotTimeframeName = 'M30 '
        elif _sw3 == PERIOD_H1:
            pivotTimeframeName = 'H1 '
        elif _sw3 == PERIOD_H4:
            pivotTimeframeName = 'H4 '
        elif _sw3 == PERIOD_D1:
            pivotTimeframeName = 'D1 '
        elif _sw3 == PERIOD_W1:
            pivotTimeframeName = 'W1 '
        elif _sw3 == PERIOD_MN1:
            pivotTimeframeName = 'MN1 '
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, indiName, 0, OBJ_LABEL)
    Print('OnDeinit', ' Deinitialization reason code = ', reason)

def download_history(symbol, period=PERIOD_CURRENT):
    if period == PERIOD_CURRENT:
        period = Period()
    ResetLastError()
    other = iTime(symbol, period, 0)
    if GetLastError() == 0 and other != 0:
        return True
    if GetLastError() != ERR_HISTORY_NOT_FOUND:
        PrintFormat('iTime(%s,%i) Failed: %i', symbol, period, GetLastError())
    return False

def OnTimer():
    symbolIndex = 0
    while symbolIndex < numSymbols:
        if not download_history(symbolListFinal[symbolIndex], pivotTimeframe):
            symbolIndex += 1
            continue
        else:
            if symbolTimeframeTimeP[symbolIndex] == 0 or symbolTimeframeTimeP[symbolIndex] != iTime(symbolListFinal[symbolIndex], pivotTimeframe, 0):
                symbolTimeframeTimeP[symbolIndex] = 0
                _sw4 = pivotSelection
                if _sw4 == Standard:
                    initializePivotPoints_2(symbolIndex, numPPStandard)
                elif _sw4 == Camarilla:
                    initializePivotPoints_2(symbolIndex, numPPCamarilla)
                elif _sw4 == Woodie:
                    initializePivotPoints_2(symbolIndex, numPPWoodie)
                elif _sw4 == Fibonacci:
                    initializePivotPoints_2(symbolIndex, numPPFibonacci)
            else:
                _sw5 = pivotSelection
                if _sw5 == Standard:
                    checkValuesForValid(symbolIndex, numPPStandard)
                elif _sw5 == Camarilla:
                    checkValuesForValid(symbolIndex, numPPCamarilla)
                elif _sw5 == Woodie:
                    checkValuesForValid(symbolIndex, numPPWoodie)
                elif _sw5 == Fibonacci:
                    checkValuesForValid(symbolIndex, numPPFibonacci)
                _sw6 = pivotSelection
                if _sw6 == Standard:
                    PivotCheck(symbolIndex, numPPStandard, showStandard, standardPivotNames)
                elif _sw6 == Camarilla:
                    PivotCheck(symbolIndex, numPPCamarilla, showCamarilla, camarillaPivotNames)
                elif _sw6 == Woodie:
                    PivotCheck(symbolIndex, numPPWoodie, showWoodie, woodiePivotNames)
                elif _sw6 == Fibonacci:
                    PivotCheck(symbolIndex, numPPFibonacci, showFibonacci, fibonacciPivotNames)
                if useDashboard == Yes:
                    LabelPivot(symbolIndex)
        symbolIndex += 1

def start():
    return 0

def initializePivotPoints_1():
    global numPPStandard
    ArrayResize(symbolTimeframeTimeP, numSymbols)
    for i in range(0, numSymbols):
        symbolTimeframeTimeP[i] = 0
    if pivotSelection == Standard and MidPointAlerts == Enable:
        numPPStandard = 17
    else:
        numPPStandard = 9
    if (alertModeSelection == Cross_And_Bounce_Alerts or alertModeSelection == Near_And_Bounce_Alerts) or alertModeSelection == Bounce_Only_Alerts:
        ArrayResize(symbolNewCandleCheck, numSymbols)
        ArrayResize(symbolPPIndex, numSymbols)
        ArrayResize(PivotState, numSymbols)
        ArrayResize(bouncedWaitTill, numSymbols)
    ArrayResize(Pivots, numSymbols)
    ArrayResize(PivotsCheck, numSymbols)
    ArrayResize(PivotsFlag, numSymbols)
    ArrayResize(PivotsWaitTill, numSymbols)
    ArrayResize(PivotsZoneFlag, numSymbols)

def initializePivotPoints_2(symbolIndex, numOfPivotPoints):
    if symbolTimeframeTimeP[symbolIndex] == 0:
        resetVariables(symbolIndex)
        symbolTimeframeTimeP[symbolIndex] = iTime(symbolListFinal[symbolIndex], pivotTimeframe, 0)
        symbol = symbolListFinal[symbolIndex]
        bid = SymbolInfoDouble(symbol, SYMBOL_BID)
        if (alertModeSelection == Cross_And_Bounce_Alerts or alertModeSelection == Near_And_Bounce_Alerts) or alertModeSelection == Bounce_Only_Alerts:
            symbolNewCandleCheck[symbolIndex][0] = iTime(symbol, bouncedCandleTF, 0)
        points = SymbolInfoDouble(symbol, SYMBOL_POINT)
        pipPoints = xxPoints * points
        _sw7 = pivotSelection
        if _sw7 == Standard:
            standardPivotPoint(pivotTimeframe, Pivots, symbolIndex, symbol)
        elif _sw7 == Camarilla:
            camarillaPivotPoint(pivotTimeframe, Pivots, symbolIndex, symbol)
        elif _sw7 == Woodie:
            woodiePivotPoint(pivotTimeframe, Pivots, symbolIndex, symbol)
        elif _sw7 == Fibonacci:
            fibonacciPivotPoint(pivotTimeframe, Pivots, symbolIndex, symbol)
        for l in range(0, numOfPivotPoints):
            if (Pivots[symbolIndex][l] == 0 or iClose(symbolListFinal[symbolIndex], pivotTimeframe, 0) == 0) or iTime(symbolListFinal[symbolIndex], pivotTimeframe, 0) == 0:
                symbolTimeframeTimeP[symbolIndex] = 0
                Print(symbolListFinal[symbolIndex] + ' ' + 'History Still Downloading')
                return
        if alertModeSelection == Cross_Alerts or alertModeSelection == Cross_And_Bounce_Alerts:
            for i in range(0, numOfPivotPoints):
                if bid >= Pivots[symbolIndex][i]:
                    PivotsFlag[symbolIndex][i] = True
                else:
                    PivotsFlag[symbolIndex][i] = False
        elif alertModeSelection == Near_Alerts or alertModeSelection == Near_And_Bounce_Alerts:
            for i in range(0, numOfPivotPoints):
                pivotHigh = Pivots[symbolIndex][i] + pipPoints
                pivotLow = Pivots[symbolIndex][i] - pipPoints
                if bid <= pivotHigh and bid >= pivotLow:
                    PivotsZoneFlag[symbolIndex][i] = True
                else:
                    PivotsZoneFlag[symbolIndex][i] = False
        if printOutPivotPoints == Yes and printOutPivotPointsSymbolIndex == symbolIndex:
            printOutPivotPoint(printOutPivotPointsSymbolIndex)

def getSymbols():
    global numSymbols
    sep = ','
    u_sep = 0
    u_sep = StringGetCharacter(sep, 0)
    StringSplit(symbols, u_sep, symbolList)
    numSymbols = ArraySize(symbolList)
    ArrayResize(symbolListFinal, numSymbols)
    for i in range(0, numSymbols):
        symbolListFinal[i] = symbolPrefix + symbolList[i] + symbolSuffix

def testSymbols():
    result = True
    for i in range(0, numSymbols):
        bid = SymbolInfoDouble(symbolListFinal[i], SYMBOL_BID)
        if GetLastError() == ERR_CHART_CANNOT_CHANGE or GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
            result = False
            Alert("Can't find this symbol: " + symbolListFinal[i] + ',\nPut symbols in Market Watch,\nDouble Check Prefix Or Suffix Settings,\nREMOVING INDICATOR FROM CHART.')
            ChartIndicatorDelete(0, 0, indiName)
            break
    return result

def resetVariables(symbolIndex):
    if (alertModeSelection == Cross_And_Bounce_Alerts or alertModeSelection == Near_And_Bounce_Alerts) or alertModeSelection == Bounce_Only_Alerts:
        symbolNewCandleCheck[symbolIndex][0] = 0
        symbolPPIndex[symbolIndex][0] = 0
        PivotState[symbolIndex][0] = 0
        for k in range(0, 20):
            bouncedWaitTill[symbolIndex][k] = 0
    for k in range(0, 20):
        Pivots[symbolIndex][k] = 0.0
        PivotsFlag[symbolIndex][k] = False
        PivotsZoneFlag[symbolIndex][k] = False
        PivotsWaitTill[symbolIndex][k] = 0

def doAlert(symbol, timeFrameName, pivotLevelName):
    timeOfAlert = 0
    if useDashboard == Yes:
        if timeChoiceOption == Local:
            timeOfAlert = TimeLocal()
        elif timeChoiceOption == Server:
            timeOfAlert = TimeCurrent()
        TimeOfAlertLabelUpdate(symbol, timeOfAlert, pivotLevelName)
    if alertModeSelection == Cross_Alerts or alertModeSelection == Cross_And_Bounce_Alerts:
        if showBidPriceOnAlert == No:
            if useDashboard == Yes:
                message = symbol + ' ' + timeFrameName + pivotLevelName
                ListLabels(symbol, message, pivotLevelName)
            messageAlert = symbol + ' ' + timeFrameName + pivotLevelName + ' ' + crossedMessage + '\n' + EnumToString(pivotSelection, 'pivotTypes')
            if popupAlerts == Yes:
                Alert(messageAlert)
            if notificationAlerts == Yes:
                SendNotification(messageAlert)
            if emailAlerts == Yes:
                SendMail(messageAlert, messageAlert)
        else:
            if useDashboard == Yes:
                message = symbol + ' ' + timeFrameName + pivotLevelName + ' @ ' + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_BID), _int(SymbolInfoInteger(symbol, SYMBOL_DIGITS)))
                ListLabels(symbol, message, pivotLevelName)
            messageAlert = symbol + ' ' + timeFrameName + pivotLevelName + ' ' + crossedMessage + ' @ ' + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_BID), _int(SymbolInfoInteger(symbol, SYMBOL_DIGITS))) + '\n' + EnumToString(pivotSelection, 'pivotTypes')
            if popupAlerts == Yes:
                Alert(messageAlert)
            if notificationAlerts == Yes:
                SendNotification(messageAlert)
            if emailAlerts == Yes:
                SendMail(messageAlert, messageAlert)
    if alertModeSelection == Near_Alerts or alertModeSelection == Near_And_Bounce_Alerts:
        if showBidPriceOnAlert == No:
            if useDashboard == Yes:
                message = symbol + ' ' + timeFrameName + pivotLevelName
                ListLabels(symbol, message, pivotLevelName)
            messageAlert = symbol + ' ' + timeFrameName + pivotLevelName + ' ' + pointsNearMessage + '\n' + EnumToString(pivotSelection, 'pivotTypes')
            if popupAlerts == Yes:
                Alert(messageAlert)
            if notificationAlerts:
                SendNotification(messageAlert)
            if emailAlerts == Yes:
                SendMail(messageAlert, messageAlert)
        else:
            if useDashboard == Yes:
                message = symbol + ' ' + pivotLevelName + ' @ ' + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_BID), _int(SymbolInfoInteger(symbol, SYMBOL_DIGITS)))
                ListLabels(symbol, message, pivotLevelName)
            messageAlert = symbol + ' ' + pivotLevelName + pointsNearMessage + ' @ ' + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_BID), _int(SymbolInfoInteger(symbol, SYMBOL_DIGITS))) + '\n' + EnumToString(pivotSelection, 'pivotTypes')
            if popupAlerts == Yes:
                Alert(messageAlert)
            if notificationAlerts:
                SendNotification(messageAlert)
            if emailAlerts == Yes:
                SendMail(messageAlert, messageAlert)

def doAlertBounce(symbolName, ppTimeFrame, PivotName, rOrS):
    timeOfAlert = 0
    if useDashboard == Yes:
        if timeChoiceOption == Local:
            timeOfAlert = TimeLocal()
        elif timeChoiceOption == Server:
            timeOfAlert = TimeCurrent()
        TimeOfAlertLabelUpdate(symbolName, timeOfAlert, PivotName)
    if 82 == rOrS:
        if showBidPriceOnAlert == No:
            if useDashboard == Yes:
                message = symbolName + ' ' + ppTimeFrame + PivotName + ' ' + offResistanceBounceMSG
                ListLabels(symbolName, message, PivotName)
            messageAlert = symbolName + ' ' + ppTimeFrame + PivotName + ' ' + offResistanceBounceMSG + '\n' + EnumToString(pivotSelection, 'pivotTypes') + ' ' + EnumToString(bouncedCandleTF, 'ENUM_TIMEFRAMES')
            if popupAlerts == Yes:
                Alert(messageAlert)
            if notificationAlerts == Yes:
                SendNotification(messageAlert)
            if emailAlerts == Yes:
                SendMail(messageAlert, messageAlert)
        else:
            if useDashboard == Yes:
                message = symbolName + ' ' + ppTimeFrame + PivotName + ' ' + offResistanceBounceMSG + ' @ ' + DoubleToString(SymbolInfoDouble(symbolName, SYMBOL_BID), _int(SymbolInfoInteger(symbolName, SYMBOL_DIGITS)))
                ListLabels(symbolName, message, PivotName)
            messageAlert = symbolName + ' ' + ppTimeFrame + PivotName + ' ' + offResistanceBounceMSG + ' @ ' + DoubleToString(SymbolInfoDouble(symbolName, SYMBOL_BID), _int(SymbolInfoInteger(symbolName, SYMBOL_DIGITS))) + '\n' + EnumToString(pivotSelection, 'pivotTypes') + ' ' + EnumToString(bouncedCandleTF, 'ENUM_TIMEFRAMES')
            if popupAlerts == Yes:
                Alert(messageAlert)
            if notificationAlerts == Yes:
                SendNotification(messageAlert)
            if emailAlerts == Yes:
                SendMail(messageAlert, messageAlert)
    if 83 == rOrS:
        if showBidPriceOnAlert == No:
            if useDashboard == Yes:
                message = symbolName + ' ' + ppTimeFrame + PivotName + ' ' + offSupportBounceMSG
                ListLabels(symbolName, message, PivotName)
            messageAlert = symbolName + ' ' + ppTimeFrame + PivotName + ' ' + offSupportBounceMSG + '\n' + EnumToString(pivotSelection, 'pivotTypes') + ' ' + EnumToString(bouncedCandleTF, 'ENUM_TIMEFRAMES')
            if popupAlerts == Yes:
                Alert(messageAlert)
            if notificationAlerts == Yes:
                SendNotification(messageAlert)
            if emailAlerts == Yes:
                SendMail(messageAlert, messageAlert)
        else:
            if useDashboard == Yes:
                message = symbolName + ' ' + ppTimeFrame + PivotName + ' ' + offSupportBounceMSG + ' @ ' + DoubleToString(SymbolInfoDouble(symbolName, SYMBOL_BID), _int(SymbolInfoInteger(symbolName, SYMBOL_DIGITS)))
                ListLabels(symbolName, message, PivotName)
            messageAlert = symbolName + ' ' + ppTimeFrame + PivotName + ' ' + offSupportBounceMSG + ' @ ' + DoubleToString(SymbolInfoDouble(symbolName, SYMBOL_BID), _int(SymbolInfoInteger(symbolName, SYMBOL_DIGITS))) + '\n' + EnumToString(pivotSelection, 'pivotTypes') + ' ' + EnumToString(bouncedCandleTF, 'ENUM_TIMEFRAMES')
            if popupAlerts == Yes:
                Alert(messageAlert)
            if notificationAlerts == Yes:
                SendNotification(messageAlert)
            if emailAlerts == Yes:
                SendMail(messageAlert, messageAlert)

def standardPivotPoint(timeFrame, ppArrayRef, symbolIndex, symbolName):
    symbolDigits = _int(SymbolInfoInteger(symbolName, SYMBOL_DIGITS))
    prevRange = iHigh(symbolName, timeFrame, 1) - iLow(symbolName, timeFrame, 1)
    prevHigh = iHigh(symbolName, timeFrame, 1)
    prevLow = iLow(symbolName, timeFrame, 1)
    prevClose = iClose(symbolName, timeFrame, 1)
    PP = (prevHigh + prevLow + prevClose) / 3
    R1 = (PP * 2) - prevLow
    S1 = (PP * 2) - prevHigh
    R2 = PP + prevHigh - prevLow
    S2 = PP - prevHigh + prevLow
    R3 = R1 + (prevHigh - prevLow)
    S3 = prevLow - (2 * (prevHigh - PP))
    R4 = R3 + (R2 - R1)
    S4 = S3 - (S1 - S2)
    ppArrayRef[symbolIndex][0] = PP
    ppArrayRef[symbolIndex][1] = S1
    ppArrayRef[symbolIndex][2] = S2
    ppArrayRef[symbolIndex][3] = S3
    ppArrayRef[symbolIndex][4] = R1
    ppArrayRef[symbolIndex][5] = R2
    ppArrayRef[symbolIndex][6] = R3
    ppArrayRef[symbolIndex][7] = R4
    ppArrayRef[symbolIndex][8] = S4
    if MidPointAlerts == Enable:
        ppArrayRef[symbolIndex][9] = (R3 + R4) / 2
        ppArrayRef[symbolIndex][10] = (R2 + R3) / 2
        ppArrayRef[symbolIndex][11] = (R1 + R2) / 2
        ppArrayRef[symbolIndex][12] = (PP + R1) / 2
        ppArrayRef[symbolIndex][13] = (PP + S1) / 2
        ppArrayRef[symbolIndex][14] = (S1 + S2) / 2
        ppArrayRef[symbolIndex][15] = (S2 + S3) / 2
        ppArrayRef[symbolIndex][16] = (S3 + S4) / 2

def camarillaPivotPoint(timeFrame, ppArrayRef, symbolIndex, symbolName):
    camRange = iHigh(symbolName, timeFrame, 1) - iLow(symbolName, timeFrame, 1)
    prevHigh = iHigh(symbolName, timeFrame, 1)
    prevLow = iLow(symbolName, timeFrame, 1)
    prevClose = iClose(symbolName, timeFrame, 1)
    symbolDigits = _int(SymbolInfoInteger(symbolName, SYMBOL_DIGITS))
    R1 = ((1.1 / 12) * camRange) + prevClose
    R2 = ((1.1 / 6) * camRange) + prevClose
    R3 = ((1.1 / 4) * camRange) + prevClose
    R4 = ((1.1 / 2) * camRange) + prevClose
    S1 = prevClose - ((1.1 / 12) * camRange)
    S2 = prevClose - ((1.1 / 6) * camRange)
    S3 = prevClose - ((1.1 / 4) * camRange)
    S4 = prevClose - ((1.1 / 2) * camRange)
    PP = (R4 + S4) / 2
    R5 = _fdiv(prevHigh, prevLow) * prevClose
    S5 = prevClose - (R5 - prevClose)
    ppArrayRef[symbolIndex][0] = PP
    ppArrayRef[symbolIndex][1] = S1
    ppArrayRef[symbolIndex][2] = S2
    ppArrayRef[symbolIndex][3] = S3
    ppArrayRef[symbolIndex][4] = S4
    ppArrayRef[symbolIndex][5] = R1
    ppArrayRef[symbolIndex][6] = R2
    ppArrayRef[symbolIndex][7] = R3
    ppArrayRef[symbolIndex][8] = R4
    ppArrayRef[symbolIndex][9] = R5
    ppArrayRef[symbolIndex][10] = S5

def woodiePivotPoint(timeFrame, ppArrayRef, symbolIndex, symbolName):
    prevRange = iHigh(symbolName, timeFrame, 1) - iLow(symbolName, timeFrame, 1)
    prevHigh = iHigh(symbolName, timeFrame, 1)
    prevLow = iLow(symbolName, timeFrame, 1)
    prevClose = iClose(symbolName, timeFrame, 1)
    todayOpen = iOpen(symbolName, timeFrame, 0)
    symbolDigits = _int(SymbolInfoInteger(symbolName, SYMBOL_DIGITS))
    PP = (prevHigh + prevLow + (todayOpen * 2)) / 4
    R1 = (PP * 2) - prevLow
    R2 = PP + prevRange
    S1 = (PP * 2) - prevHigh
    S2 = PP - prevRange
    ppArrayRef[symbolIndex][0] = PP
    ppArrayRef[symbolIndex][1] = S1
    ppArrayRef[symbolIndex][2] = S2
    ppArrayRef[symbolIndex][3] = R1
    ppArrayRef[symbolIndex][4] = R2

def fibonacciPivotPoint(timeFrame, ppArrayRef, symbolIndex, symbolName):
    prevRange = iHigh(symbolName, timeFrame, 1) - iLow(symbolName, timeFrame, 1)
    prevHigh = iHigh(symbolName, timeFrame, 1)
    prevLow = iLow(symbolName, timeFrame, 1)
    prevClose = iClose(symbolName, timeFrame, 1)
    symbolDigits = _int(SymbolInfoInteger(symbolName, SYMBOL_DIGITS))
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
    ppArrayRef[symbolIndex][0] = Pivot
    ppArrayRef[symbolIndex][1] = R38
    ppArrayRef[symbolIndex][2] = R61
    ppArrayRef[symbolIndex][3] = R78
    ppArrayRef[symbolIndex][4] = R100
    ppArrayRef[symbolIndex][5] = R138
    ppArrayRef[symbolIndex][6] = R161
    ppArrayRef[symbolIndex][7] = R200
    ppArrayRef[symbolIndex][8] = S38
    ppArrayRef[symbolIndex][9] = S61
    ppArrayRef[symbolIndex][10] = S78
    ppArrayRef[symbolIndex][11] = S100
    ppArrayRef[symbolIndex][12] = S138
    ppArrayRef[symbolIndex][13] = S161
    ppArrayRef[symbolIndex][14] = S200

def PivotCheck(symbolIndex, numOfPivotPoints, showRef, pivotNamesRef):
    if symbolTimeframeTimeP[symbolIndex] != 0:
        result = False
        bid = 0.0
        points = 0.0
        pipPoints = 0.0
        digits = 0
        ppTimeFrame = ""
        symbolName = ""
        symbolName = symbolListFinal[symbolIndex]
        bid = SymbolInfoDouble(symbolName, SYMBOL_BID)
        points = SymbolInfoDouble(symbolName, SYMBOL_POINT)
        digits = _int(SymbolInfoInteger(symbolName, SYMBOL_DIGITS))
        pipPoints = xxPoints * points
        ppTimeFrame = pivotTimeframeName
        if alertModeSelection != Bounce_Only_Alerts:
            for j in range(0, numOfPivotPoints):
                if alertModeSelection == Cross_Alerts or alertModeSelection == Cross_And_Bounce_Alerts:
                    result = bid >= Pivots[symbolIndex][j]
                    if result != PivotsFlag[symbolIndex][j]:
                        PivotsFlag[symbolIndex][j] = result
                        if useBollingerBands == Yes:
                            if (isUpperLowerBollinger(symbolIndex) == True and TimeCurrent() >= PivotsWaitTill[symbolIndex][j]) and showRef[j] == True:
                                PivotsWaitTill[symbolIndex][j] = TimeCurrent() + alertIntervalTimeSeconds
                                doAlert(symbolName, ppTimeFrame, pivotNamesRef[j])
                        elif useBollingerBands == No:
                            if TimeCurrent() >= PivotsWaitTill[symbolIndex][j] and showRef[j] == True:
                                PivotsWaitTill[symbolIndex][j] = TimeCurrent() + alertIntervalTimeSeconds
                                doAlert(symbolName, ppTimeFrame, pivotNamesRef[j])
                elif alertModeSelection == Near_Alerts or alertModeSelection == Near_And_Bounce_Alerts:
                    pivotHigh = Pivots[symbolIndex][j] + pipPoints
                    pivotLow = Pivots[symbolIndex][j] - pipPoints
                    result = bid <= pivotHigh and bid >= pivotLow
                    if result != PivotsZoneFlag[symbolIndex][j]:
                        PivotsZoneFlag[symbolIndex][j] = result
                        if useBollingerBands == Yes:
                            if ((isUpperLowerBollinger(symbolIndex) == True and TimeCurrent() >= PivotsWaitTill[symbolIndex][j]) and showRef[j] == True) and PivotsZoneFlag[symbolIndex][j] == True:
                                PivotsWaitTill[symbolIndex][j] = TimeCurrent() + alertIntervalTimeSeconds
                                doAlert(symbolName, ppTimeFrame, pivotNamesRef[j])
                        elif useBollingerBands == No:
                            if (TimeCurrent() >= PivotsWaitTill[symbolIndex][j] and showRef[j] == True) and PivotsZoneFlag[symbolIndex][j] == True:
                                PivotsWaitTill[symbolIndex][j] = TimeCurrent() + alertIntervalTimeSeconds
                                doAlert(symbolName, ppTimeFrame, pivotNamesRef[j])
        if useBollingerBands == Yes and isUpperLowerBollinger(symbolIndex) == True:
            BouncedCheck(symbolIndex, numOfPivotPoints, symbolPPIndex, Pivots, PivotState, ppTimeFrame, pivotNamesRef, showRef)
        elif useBollingerBands == No:
            BouncedCheck(symbolIndex, numOfPivotPoints, symbolPPIndex, Pivots, PivotState, ppTimeFrame, pivotNamesRef, showRef)

def printOutPivotPoint(index):
    if index > (numSymbols - 1) or index < 0:
        Alert('printOutPivotPointsSymbolIndex invalid index number')
    else:
        printMessage = ''
        if pivotSelection == Standard:
            pivotLevelName = pivotTimeframeName
            digits = _int(SymbolInfoInteger(symbolListFinal[index], SYMBOL_DIGITS))
            for j in range(0, numPPStandard):
                printMessage += pivotLevelName + standardPivotNames[j] + ' ' + DoubleToString(Pivots[index][j], digits) + '\n'
            Alert('PRINT OUT TEST ' + symbolListFinal[index] + ' VALUES BELOW ' + EnumToString(pivotSelection, 'pivotTypes') + '\n' + printMessage)
        elif pivotSelection == Camarilla:
            pivotLevelName = pivotTimeframeName
            digits = _int(SymbolInfoInteger(symbolListFinal[index], SYMBOL_DIGITS))
            for j in range(0, numPPCamarilla):
                printMessage += pivotLevelName + camarillaPivotNames[j] + ' ' + DoubleToString(Pivots[index][j], digits) + '\n'
            Alert('PRINT OUT TEST ' + symbolListFinal[index] + ' VALUES BELOW ' + EnumToString(pivotSelection, 'pivotTypes') + '\n' + printMessage)
        elif pivotSelection == Woodie:
            pivotLevelName = pivotTimeframeName
            digits = _int(SymbolInfoInteger(symbolListFinal[index], SYMBOL_DIGITS))
            for j in range(0, numPPWoodie):
                printMessage += pivotLevelName + woodiePivotNames[j] + ' ' + DoubleToString(Pivots[index][j], digits) + '\n'
            Alert('PRINT OUT TEST ' + symbolListFinal[index] + ' VALUES BELOW ' + EnumToString(pivotSelection, 'pivotTypes') + '\n' + printMessage)
        elif pivotSelection == Fibonacci:
            pivotLevelName = pivotTimeframeName
            digits = _int(SymbolInfoInteger(symbolListFinal[index], SYMBOL_DIGITS))
            for j in range(0, numPPFibonacci):
                printMessage += pivotLevelName + fibonacciPivotNames[j] + ' ' + DoubleToString(Pivots[index][j], digits) + '\n'
            Alert('PRINT OUT TEST ' + symbolListFinal[index] + ' VALUES BELOW ' + EnumToString(pivotSelection, 'pivotTypes') + '\n' + printMessage)

def BouncedCheck(i, numPP, correctPivotIndexRef, ppArrayRef, pivotStateRef, ppTimeFrame, PivotNamesRef, showRef):
    if (alertModeSelection == Cross_And_Bounce_Alerts or alertModeSelection == Near_And_Bounce_Alerts) or alertModeSelection == Bounce_Only_Alerts:
        symbolName = symbolListFinal[i]
        if symbolNewCandleCheck[i][0] != iTime(symbolName, bouncedCandleTF, 0):
            symbolNewCandleCheck[i][0] = iTime(symbolName, bouncedCandleTF, 0)
            high = iHigh(symbolName, bouncedCandleTF, 1)
            open = iOpen(symbolName, bouncedCandleTF, 1)
            close = iClose(symbolName, bouncedCandleTF, 1)
            low = iLow(symbolName, bouncedCandleTF, 1)
            correctPivotIndex = -1
            PivotIndexCrossed = Arr(0, 0.0)
            ArrayResize(PivotIndexCrossed, numPP)
            for m in range(0, numPP):
                PivotIndexCrossed[m] = 0.0
            countFound = 0
            for k in range(0, numPP):
                if (open < ppArrayRef[i][k] and ppArrayRef[i][k] <= high) and ppArrayRef[i][k] >= low:
                    countFound += 1
                    PivotIndexCrossed[k] = 1.0
                    correctPivotIndex = k
                elif (open > ppArrayRef[i][k] and ppArrayRef[i][k] <= high) and ppArrayRef[i][k] >= low:
                    countFound += 1
                    PivotIndexCrossed[k] = 1.0
                    correctPivotIndex = k
            isBullishCandle = False
            if open < close:
                isBullishCandle = True
            isBearishCandle = False
            if open > close:
                isBearishCandle = True
            firstNumberGrabed = False
            highest = 0.0
            lowest = 0.0
            if countFound > 1:
                if isBullishCandle == True:
                    for n in range(0, numPP):
                        if PivotIndexCrossed[n] == 1:
                            if (firstNumberGrabed := False):
                                firstNumberGrabed = True
                                highest = ppArrayRef[i][n]
                                correctPivotIndex = n
                            else:
                                if ppArrayRef[i][n] > highest:
                                    highest = ppArrayRef[i][n]
                                    correctPivotIndex = n
                elif isBearishCandle == True:
                    for n in range(0, numPP):
                        if PivotIndexCrossed[n] == 1:
                            if (firstNumberGrabed := False):
                                firstNumberGrabed = True
                                lowest = ppArrayRef[i][n]
                                correctPivotIndex = n
                            else:
                                if ppArrayRef[i][n] < lowest:
                                    lowest = ppArrayRef[i][n]
                                    correctPivotIndex = n
            foundR = False
            foundP = False
            foundS = False
            if countFound >= 1:
                if 82 == StringGetCharacter(PivotNamesRef[correctPivotIndex], 0):
                    foundR = True
                elif 80 == StringGetCharacter(PivotNamesRef[correctPivotIndex], 0):
                    foundP = True
                elif 83 == StringGetCharacter(PivotNamesRef[correctPivotIndex], 0):
                    foundS = True
                elif 109 == StringGetCharacter(PivotNamesRef[correctPivotIndex], 0):
                    if 82 == StringGetCharacter(PivotNamesRef[correctPivotIndex], 1):
                        foundR = True
                    else:
                        foundS = True
            if (pivotStateRef[i][0] != 0 and countFound >= 1) and pivotStateRef[i][0] != correctPivotIndex:
                pivotStateRef[i][0] = 0
                correctPivotIndexRef[i][0] = -1
            if pivotStateRef[i][0] == 0 and countFound >= 1:
                if foundR == True and close < ppArrayRef[i][correctPivotIndex]:
                    if (candleColorFilter == Yes and isBullishCandle == False) and isBearishCandle == True:
                        if showRef[correctPivotIndex] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndex]:
                            bouncedWaitTill[i][correctPivotIndex] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndex], 82)
                    elif candleColorFilter == No:
                        if showRef[correctPivotIndex] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndex]:
                            bouncedWaitTill[i][correctPivotIndex] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndex], 82)
                elif foundS == True and close > ppArrayRef[i][correctPivotIndex]:
                    if (candleColorFilter == Yes and isBullishCandle == True) and isBearishCandle == False:
                        if showRef[correctPivotIndex] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndex]:
                            bouncedWaitTill[i][correctPivotIndex] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndex], 83)
                    elif candleColorFilter == No:
                        if showRef[correctPivotIndex] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndex]:
                            bouncedWaitTill[i][correctPivotIndex] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndex], 83)
                elif foundP == True and close > ppArrayRef[i][correctPivotIndex]:
                    if (candleColorFilter == Yes and isBullishCandle == True) and isBearishCandle == False:
                        if showRef[correctPivotIndex] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndex]:
                            bouncedWaitTill[i][correctPivotIndex] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndex], 83)
                    elif candleColorFilter == No:
                        if showRef[correctPivotIndex] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndex]:
                            bouncedWaitTill[i][correctPivotIndex] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndex], 83)
                elif foundP == True and close < ppArrayRef[i][correctPivotIndex]:
                    if (candleColorFilter == Yes and isBullishCandle == False) and isBearishCandle == True:
                        if showRef[correctPivotIndex] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndex]:
                            bouncedWaitTill[i][correctPivotIndex] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndex], 82)
                    elif candleColorFilter == No:
                        if showRef[correctPivotIndex] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndex]:
                            bouncedWaitTill[i][correctPivotIndex] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndex], 82)
            if pivotStateRef[i][0] == 0 and countFound >= 1:
                if foundR == True and close > ppArrayRef[i][correctPivotIndex]:
                    pivotStateRef[i][0] = 1
                    correctPivotIndexRef[i][0] = correctPivotIndex
                elif foundS == True and close < ppArrayRef[i][correctPivotIndex]:
                    pivotStateRef[i][0] = 2
                    correctPivotIndexRef[i][0] = correctPivotIndex
            if pivotStateRef[i][0] != 0:
                if 82 == StringGetCharacter(PivotNamesRef[correctPivotIndexRef[i][0]], 0):
                    foundR = True
                elif 80 == StringGetCharacter(PivotNamesRef[correctPivotIndexRef[i][0]], 0):
                    foundP = True
                elif 83 == StringGetCharacter(PivotNamesRef[correctPivotIndexRef[i][0]], 0):
                    foundS = True
                elif 109 == StringGetCharacter(PivotNamesRef[correctPivotIndex], 0):
                    if 82 == StringGetCharacter(PivotNamesRef[correctPivotIndex], 1):
                        foundR = True
                    else:
                        foundS = True
                if foundR == True and close < ppArrayRef[i][correctPivotIndexRef[i][0]]:
                    if (candleColorFilter == Yes and isBullishCandle == False) and isBearishCandle == True:
                        pivotStateRef[i][0] = 0
                        if showRef[correctPivotIndexRef[i][0]] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndexRef[i][0]]:
                            bouncedWaitTill[i][correctPivotIndexRef[i][0]] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndexRef[i][0]], 82)
                    elif candleColorFilter == No:
                        pivotStateRef[i][0] = 0
                        if showRef[correctPivotIndexRef[i][0]] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndexRef[i][0]]:
                            bouncedWaitTill[i][correctPivotIndexRef[i][0]] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndexRef[i][0]], 82)
                elif foundS == True and close > ppArrayRef[i][correctPivotIndexRef[i][0]]:
                    if (candleColorFilter == Yes and isBullishCandle == True) and isBearishCandle == False:
                        pivotStateRef[i][0] = 0
                        if showRef[correctPivotIndexRef[i][0]] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndexRef[i][0]]:
                            bouncedWaitTill[i][correctPivotIndexRef[i][0]] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndexRef[i][0]], 83)
                    elif candleColorFilter == No:
                        pivotStateRef[i][0] = 0
                        if showRef[correctPivotIndexRef[i][0]] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndexRef[i][0]]:
                            bouncedWaitTill[i][correctPivotIndexRef[i][0]] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndexRef[i][0]], 83)
                elif foundP == True and close > ppArrayRef[i][correctPivotIndexRef[i][0]]:
                    if (candleColorFilter == Yes and isBullishCandle == True) and isBearishCandle == False:
                        pivotStateRef[i][0] = 0
                        if showRef[correctPivotIndexRef[i][0]] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndexRef[i][0]]:
                            bouncedWaitTill[i][correctPivotIndexRef[i][0]] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndexRef[i][0]], 83)
                    elif candleColorFilter == No:
                        pivotStateRef[i][0] = 0
                        if showRef[correctPivotIndexRef[i][0]] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndexRef[i][0]]:
                            bouncedWaitTill[i][correctPivotIndexRef[i][0]] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndexRef[i][0]], 83)
                elif foundP == True and close < ppArrayRef[i][correctPivotIndexRef[i][0]]:
                    if (candleColorFilter == Yes and isBullishCandle == False) and isBearishCandle == True:
                        pivotStateRef[i][0] = 0
                        if showRef[correctPivotIndexRef[i][0]] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndexRef[i][0]]:
                            bouncedWaitTill[i][correctPivotIndexRef[i][0]] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndexRef[i][0]], 82)
                    elif candleColorFilter == No:
                        pivotStateRef[i][0] = 0
                        if showRef[correctPivotIndexRef[i][0]] and iTime(symbolName, bouncedCandleTF, bounceXBarsWait) >= bouncedWaitTill[i][correctPivotIndexRef[i][0]]:
                            bouncedWaitTill[i][correctPivotIndexRef[i][0]] = iTime(symbolName, bouncedCandleTF, 0)
                            doAlertBounce(symbolName, ppTimeFrame, PivotNamesRef[correctPivotIndexRef[i][0]], 82)

def updateSpecifiedPivotPointAlerts():
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
    if showCamarillaPP == Disable:
        showCamarilla[0] = False
    else:
        showCamarilla[0] = True
    if showCamarillaS1 == Disable:
        showCamarilla[1] = False
    else:
        showCamarilla[1] = True
    if showCamarillaS2 == Disable:
        showCamarilla[2] = False
    else:
        showCamarilla[2] = True
    if showCamarillaS3 == Disable:
        showCamarilla[3] = False
    else:
        showCamarilla[3] = True
    if showCamarillaS4 == Disable:
        showCamarilla[4] = False
    else:
        showCamarilla[4] = True
    if showCamarillaR1 == Disable:
        showCamarilla[5] = False
    else:
        showCamarilla[5] = True
    if showCamarillaR2 == Disable:
        showCamarilla[6] = False
    else:
        showCamarilla[6] = True
    if showCamarillaR3 == Disable:
        showCamarilla[7] = False
    else:
        showCamarilla[7] = True
    if showCamarillaR4 == Disable:
        showCamarilla[8] = False
    else:
        showCamarilla[8] = True
    if showCamarillaR5 == Disable:
        showCamarilla[9] = False
    else:
        showCamarilla[9] = True
    if showCamarillaS5 == Disable:
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

def checkValuesForValid(symbolIndex, numOfPivotPoints):
    symbol = symbolListFinal[symbolIndex]
    _sw8 = pivotSelection
    if _sw8 == Standard:
        standardPivotPoint(pivotTimeframe, PivotsCheck, symbolIndex, symbol)
    elif _sw8 == Camarilla:
        camarillaPivotPoint(pivotTimeframe, PivotsCheck, symbolIndex, symbol)
    elif _sw8 == Woodie:
        woodiePivotPoint(pivotTimeframe, PivotsCheck, symbolIndex, symbol)
    elif _sw8 == Fibonacci:
        fibonacciPivotPoint(pivotTimeframe, PivotsCheck, symbolIndex, symbol)
    for i in range(0, numOfPivotPoints):
        if PivotsCheck[symbolIndex][i] != Pivots[symbolIndex][i]:
            symbolTimeframeTimeP[symbolIndex] = 0
            Print(symbolListFinal[symbolIndex] + ' ' + 'checkValuesForValid found a outdated value reseting symbol and updating')

def isUpperLowerBollinger(symbolIndex):
    result = False
    symbolBidPrice = SymbolInfoDouble(symbolListFinal[symbolIndex], SYMBOL_BID)
    upperBand = iBandsMQL4(symbolListFinal[symbolIndex], BBtimeFrame, BBperiod, BBdeviation, BBShift, BBAppliedPrice, 1, 0)
    lowerBand = iBandsMQL4(symbolListFinal[symbolIndex], BBtimeFrame, BBperiod, BBdeviation, BBShift, BBAppliedPrice, 2, 0)
    if symbolBidPrice > upperBand or symbolBidPrice < lowerBand:
        result = True
    return result

def CreateLabels():
    global textHEnd
    timeOfAlertOption = ""
    if timeChoiceOption == Local:
        timeOfAlertOption = '(Local)'
    elif timeChoiceOption == Server:
        timeOfAlertOption = '(Server)'
    LabelCreate(0, indiName + ' pivottimeframeH ', 0, widthX, widthY - textH, CORNER_LEFT_UPPER, EnumToString(pivotSelection, 'pivotTypes') + ' - ' + EnumToString(pivotTimeframe, 'ENUM_TIMEFRAMES') + ' - ' + EnumToString(alertModeSelection, 'alertMode'), FontHeader, fontText, headerColors, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
    LabelCreate(0, indiName + ' symbolH ', 0, widthX, widthY, CORNER_LEFT_UPPER, 'Symbol', FontHeader, fontText, headerColors, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
    LabelCreate(0, indiName + ' pivotH ', 0, widthX + symbolPivotXSpacing, widthY, CORNER_LEFT_UPPER, 'Near', FontHeader, fontText, headerColors, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
    LabelCreate(0, indiName + ' pivotAlertH ', 0, widthX + symbolPivotXSpacing + pivotPivotAlertXSpacing, widthY, CORNER_LEFT_UPPER, 'PP', FontHeader, fontText, headerColors, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
    LabelCreate(0, indiName + ' timeAlertH ', 0, widthX + symbolPivotXSpacing + pivotPivotAlertXSpacing + pivotAlertTimeLastXSpacing, widthY, CORNER_LEFT_UPPER, 'Time Last Alert' + ' ' + timeOfAlertOption, FontHeader, fontText, headerColors, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
    textSpaceing = textH
    i = 0
    while i < ArraySize(symbolListFinal):
        LabelCreate(0, indiName + ' ' + symbolListFinal[i] + ' symbol ', 0, widthX, widthY + textSpaceing, CORNER_LEFT_UPPER, symbolListFinal[i], Font, fontText, symbolColor, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
        LabelCreate(0, indiName + ' ' + symbolListFinal[i] + ' pivot ', 0, widthX + symbolPivotXSpacing, widthY + textSpaceing, CORNER_LEFT_UPPER, '', Font, fontText, symbolColor, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
        LabelCreate(0, indiName + ' ' + symbolListFinal[i] + ' pivotAlert ', 0, widthX + symbolPivotXSpacing + pivotPivotAlertXSpacing, widthY + textSpaceing, CORNER_LEFT_UPPER, '', Font, fontText, symbolColor, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
        LabelCreate(0, indiName + ' ' + symbolListFinal[i] + ' timeAlert ', 0, widthX + symbolPivotXSpacing + pivotPivotAlertXSpacing + pivotAlertTimeLastXSpacing, widthY + textSpaceing, CORNER_LEFT_UPPER, '', Font, fontText, symbolColor, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
        textSpaceing += textH
        i += 1
    textHEnd = textSpaceing + textH
    LabelCreate(0, indiName + ' listAlertsH ', 0, widthX, widthY + textHEnd, CORNER_LEFT_UPPER, 'List Of Recent Alerts', FontHeader, fontText, headerColors, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
    textSpaceing = textH
    k = 0
    while k < ArraySize(listLabelNames):
        LabelCreate(0, indiName + ' ' + listLabelNames[k], 0, widthX, widthY + textHEnd + textSpaceing, CORNER_LEFT_UPPER, '', Font, fontText, clrWhite, 0.0, ANCHOR_LEFT_UPPER, False, False, True, 0)
        textSpaceing += textH
        k += 1

def LabelCreate(chart_ID=0, name='Label', sub_window=0, x=0, y=0, corner=CORNER_LEFT_UPPER, text='Label', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_LABEL, sub_window, 0, 0):
        Print('LabelCreate', ': failed to create text label! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
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

def LabelPivot(symbolIndex):
    bidPrice = SymbolInfoDouble(symbolListFinal[symbolIndex], SYMBOL_BID)
    otherCompares = 0.0
    pivotName = ''
    numPivotPoints = 0
    _sw9 = pivotSelection
    if _sw9 == Standard:
        numPivotPoints = 17
    elif _sw9 == Camarilla:
        numPivotPoints = 11
    elif _sw9 == Woodie:
        numPivotPoints = 5
    elif _sw9 == Fibonacci:
        numPivotPoints = 15
    pivotNearestIndex = 0
    currentSmallest = MathAbs(bidPrice - Pivots[symbolIndex][0])
    for i in range(1, numPivotPoints):
        otherCompares = MathAbs(bidPrice - Pivots[symbolIndex][i])
        if otherCompares < currentSmallest:
            currentSmallest = otherCompares
            pivotNearestIndex = i
    _sw10 = pivotSelection
    if _sw10 == Standard:
        pivotName = standardPivotNames[pivotNearestIndex]
    elif _sw10 == Camarilla:
        pivotName = camarillaPivotNames[pivotNearestIndex]
    elif _sw10 == Woodie:
        pivotName = woodiePivotNames[pivotNearestIndex]
    elif _sw10 == Fibonacci:
        pivotName = fibonacciPivotNames[pivotNearestIndex]
    if 82 == StringGetCharacter(pivotName, 0):
        ObjectSetTextMQL4(indiName + ' ' + symbolListFinal[symbolIndex] + ' pivot ', pivotName, fontText, Font, resistantColor)
    elif 80 == StringGetCharacter(pivotName, 0):
        ObjectSetTextMQL4(indiName + ' ' + symbolListFinal[symbolIndex] + ' pivot ', pivotName, fontText, Font, pivotColor)
    elif 83 == StringGetCharacter(pivotName, 0):
        ObjectSetTextMQL4(indiName + ' ' + symbolListFinal[symbolIndex] + ' pivot ', pivotName, fontText, Font, supportColor)
    ChartRedraw(0)

def TimeOfAlertLabelUpdate(symbol, timeCurrent, pivotName):
    if 82 == StringGetCharacter(pivotName, 0):
        if usePivotColor == False:
            ObjectSetTextMQL4(indiName + ' ' + symbol + ' timeAlert ', TimeToString(timeCurrent, TIME_DATE | TIME_SECONDS), fontText, Font, timeLastAlertColor)
        else:
            ObjectSetTextMQL4(indiName + ' ' + symbol + ' timeAlert ', TimeToString(timeCurrent, TIME_DATE | TIME_SECONDS), fontText, Font, resistantColor)
    elif 80 == StringGetCharacter(pivotName, 0):
        if usePivotColor == False:
            ObjectSetTextMQL4(indiName + ' ' + symbol + ' timeAlert ', TimeToString(timeCurrent, TIME_DATE | TIME_SECONDS), fontText, Font, timeLastAlertColor)
        else:
            ObjectSetTextMQL4(indiName + ' ' + symbol + ' timeAlert ', TimeToString(timeCurrent, TIME_DATE | TIME_SECONDS), fontText, Font, pivotColor)
    elif 83 == StringGetCharacter(pivotName, 0):
        if usePivotColor == False:
            ObjectSetTextMQL4(indiName + ' ' + symbol + ' timeAlert ', TimeToString(timeCurrent, TIME_DATE | TIME_SECONDS), fontText, Font, timeLastAlertColor)
        else:
            ObjectSetTextMQL4(indiName + ' ' + symbol + ' timeAlert ', TimeToString(timeCurrent, TIME_DATE | TIME_SECONDS), fontText, Font, supportColor)
    ChartRedraw(0)

def ListLabels(symbol, message, pivotLevelName):
    ppColor = clrNONE
    for k in range(listLabelSize - 1, 0 - 1, -1):
        if k >= 1:
            oldText = ObjectDescriptionMQL4(indiName + ' ' + listLabelNames[k - 1])
            oldColor = _uint(ObjectGetInteger(0, indiName + ' ' + listLabelNames[k - 1], OBJPROP_COLOR))
            ObjectSetTextMQL4(indiName + ' ' + listLabelNames[k], oldText, fontText, Font, oldColor)
    if 82 == StringGetCharacter(pivotLevelName, 0):
        ppColor = resistantColor
        if usePivotColor == False:
            ObjectSetTextMQL4(indiName + ' ' + listLabelNames[0], message, fontText, Font, listLabelColor)
        else:
            ObjectSetTextMQL4(indiName + ' ' + listLabelNames[0], message, fontText, Font, resistantColor)
    elif 80 == StringGetCharacter(pivotLevelName, 0):
        ppColor = pivotColor
        if usePivotColor == False:
            ObjectSetTextMQL4(indiName + ' ' + listLabelNames[0], message, fontText, Font, listLabelColor)
        else:
            ObjectSetTextMQL4(indiName + ' ' + listLabelNames[0], message, fontText, Font, pivotColor)
    elif 83 == StringGetCharacter(pivotLevelName, 0):
        ppColor = supportColor
        if usePivotColor == False:
            ObjectSetTextMQL4(indiName + ' ' + listLabelNames[0], message, fontText, Font, listLabelColor)
        else:
            ObjectSetTextMQL4(indiName + ' ' + listLabelNames[0], message, fontText, Font, supportColor)
    ObjectSetTextMQL4(indiName + ' ' + symbol + ' pivotAlert ', pivotLevelName, fontText, Font, ppColor)
    ChartRedraw(0)

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_OBJECT_CLICK:
        sep = ' '
        u_sep = 0
        result = Arr(0, "")
        resultRecentAlerts = Arr(0, "")
        u_sep = StringGetCharacter(sep, 0)
        k = StringSplit(sparam, u_sep, result)
        resultSize = ArraySize(result)
        if resultSize == 4:
            if result[2] == 'symbol' and indiName == result[0]:
                resultChartOpen = ChartOpen(result[1], openChartTimeFrame)
        if resultSize == 2:
            if indiName == result[0]:
                symbolName = ObjectGetString(0, result[0] + ' ' + result[1], OBJPROP_TEXT)
                j = StringSplit(symbolName, u_sep, resultRecentAlerts)
                resultRecentAlertsSize = ArraySize(resultRecentAlerts)
                if resultRecentAlertsSize == 3:
                    resultChartOpen = ChartOpen(resultRecentAlerts[0], openChartTimeFrame)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def iBandsMQL4(symbol, tf, period, deviation, bands_shift, method, mode, shift):
    timeframe = TFMigrate(tf)
    ma_method = MethodMigrate(method)
    handle = iBands(symbol, timeframe, period, bands_shift, deviation, ma_method)
    if handle < 0:
        Print('The iBands object is not created: Error', GetLastError())
        return -1.0
    else:
        return CopyBufferMQL4(handle, mode, shift)

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

def ObjectDescriptionMQL4(name):
    return ObjectGetString(0, name, OBJPROP_TEXT)

def CopyBufferMQL4(handle, index, shift):
    buf = Arr(0, 0.0)
    _sw11 = index
    if _sw11 == 0:
        if CopyBuffer(handle, 0, shift, 1, buf) > 0:
            return buf[0]
    elif _sw11 == 1:
        if CopyBuffer(handle, 1, shift, 1, buf) > 0:
            return buf[0]
    elif _sw11 == 2:
        if CopyBuffer(handle, 2, shift, 1, buf) > 0:
            return buf[0]
    elif _sw11 == 3:
        if CopyBuffer(handle, 3, shift, 1, buf) > 0:
            return buf[0]
    elif _sw11 == 4:
        if CopyBuffer(handle, 4, shift, 1, buf) > 0:
            return buf[0]
    else:
        pass
    return EMPTY_VALUE

# ---- global variables initialised from expressions
indiName = 'MPPPSA' + EnumToString(pivotTimeframe, 'ENUM_TIMEFRAMES') + EnumToString(pivotSelection, 'pivotTypes')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiPairPivotPointScannerAlertsV28(_MQL5Indicator):
    name = 'Multi_Pair_Pivot_Point_Scanner_Alerts_v2.8'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'refreshTime': 5,  # Refresh check every x Seconds
        'pivotSelection': _Choice({0: 'Standard(Floor) Pivot Formula', 1: 'Fibonacci Pivot Formula', 2: 'Camarilla Pivot Formula', 3: 'Woodie Pivot Formula'}, default=0),  # Pivot Point Formula
        'pivotTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Pivot Point Timeframe
        'alertModeSelection': _Choice({0: 'Crossed Pivot Alerts', 1: 'Near Pivot Alerts', 2: 'Crossed And Bounced Alerts', 3: 'Near And Bounced Alerts', 4: 'Bounced Only Alerts'}, default=0),  # Alert Mode to use
        'xxPoints': 50,  # Points Near Pivot - For Alert Mode Near
        'symTypeChoice': _Choice({0: 'Market Watch', 1: 'Symbols In List'}, default=0),  # Symbols To Scan- Market Watch/Symbol List Below
        'alertInternalMinutes': 30,  # Alert Wait Time In Min for same Pivot alert Msg
        'popupAlerts': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Use Popup Alerts?
        'notificationAlerts': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Use Notification Alerts?
        'emailAlerts': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Use Email Alerts?
        'showBidPriceOnAlert': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Show Bid Price in Alert Msg
        'printOutPivotPoints': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Print Out Pivot Values - For Testing Values
        'printOutPivotPointsSymbolIndex': 0,  # Index Value Of Symbol To Print Out
        'bouncedCandleTF': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=15),  # Time Frame Candles For Bounced Alerts
        'candleColorFilter': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Use Candle Color Filter
        'bounceXBarsWait': 0,  # Alert Wait Time In Bars for same Pivot alert Msg
        'useBollingerBands': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Use BollingerBands upper/lower Filter
        'BBtimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # Bollinger Bands: Timeframe
        'BBperiod': 20,  # Bollinger Bands: Period
        'BBdeviation': 2.0,  # Bollinger Bands: Deviations
        'BBShift': 0,  # Bollinger Bands: Shift
        'BBAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Bollinger Bands: Apply to
        'MidPointAlerts': _Choice({0: 'Disable', 1: 'Enable'}, default=0),  # Mid Pivot Point Alerts
        'showStandardPivotR4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot R4
        'showStandardPivotR3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot R3
        'showStandardPivotR2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot R2
        'showStandardPivotR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot R1
        'showStandardPivotPP': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot PP
        'showStandardPivotS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot S1
        'showStandardPivotS2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot S2
        'showStandardPivotS3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot S3
        'showStandardPivotS4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot S4
        'showStandardPivotMR4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot mR4
        'showStandardPivotMR3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot mR3
        'showStandardPivotMR2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot mR2
        'showStandardPivotMR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot mR1
        'showStandardPivotMS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot mS1
        'showStandardPivotMS2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot mS2
        'showStandardPivotMS3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot mS3
        'showStandardPivotMS4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Standard Pivot mS4
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
        'showWoodieR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot R1
        'showWoodieR2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot R2
        'showWoodiePP': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot PP
        'showWoodieS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot S1
        'showWoodieS2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Woodie Pivot S2
        'showCamarillaR1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot R1
        'showCamarillaR2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot R2
        'showCamarillaR3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot R3
        'showCamarillaR4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot R4
        'showCamarillaR5': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot R5
        'showCamarillaPP': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot PP
        'showCamarillaS1': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot S1
        'showCamarillaS2': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot S2
        'showCamarillaS3': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot S3
        'showCamarillaS4': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot S4
        'showCamarillaS5': _Choice({0: 'Disable', 1: 'Enable'}, default=1),  # Camarilla Pivot S5
        'useDashboard': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Use DashBoard?
        'widthX': 28,  # X Dashboard +Moves right, -Moves left
        'widthY': 28,  # Y Dashboard +Moves down, -Moves up
        'symbolPivotXSpacing': 85,  # X  Between Columns Symbol-PP Nearest
        'pivotPivotAlertXSpacing': 50,  # X  Between Columns PP Nearest-PP Alert
        'pivotAlertTimeLastXSpacing': 35,  # X  Between Columns PP Alert-Time Last
        'fontText': 9,  # Font Size Labels
        'textH': 14,  # Y Spacing Between Rows
        'timeChoiceOption': _Choice({0: 'Server', 1: 'Local'}, default=1),  # Local/Server Time For Time Last Alert
        'listLabelSize': 40,  # Num Of Alert Msg In List Below
        'usePivotColor': False,  # Label Color use res/sup/piv colors for alerts
        'openChartTimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Open Chart TimeFrame
    }

