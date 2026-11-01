"""All Pivot Points — converted from MQL5: MQL5 Indicators/All Pivot Points MT5/All Pivot Points.mq5

Donation (BTC): 1B8523u9AuZ69j98nDrLJ7TMDEM27erXLx
 
All important Pivot Points including:
Classic1, Classic2, Camarilla, Woodie, Floor, Fibonacci, Fibonacci_Retracement
Fully Coded By Hossein Nouri
Email : hsn.nouri@gmail.com
Skype : hsn.nouri
Telegram : @hypernova1990
Website : http://www.dlikedeveloper.com
MQL5 Profile : https://www.mql5.com/en/users/hsnnouri
 
Feel free to contact me for MQL4/MQL5/Pine coding.
Copyright: Copyright 2022, Hossein Nouri; Link: https://www.mql5.com/en/users/hsnnouri; Version: 1.14

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, Hossein Nouri', 'link': 'https://www.mql5.com/en/users/hsnnouri', 'version': '1.14', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 9}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {1: 'Pivot', 2: 'S1', 3: 'S2', 4: 'S3', 5: 'S4', 6: 'R1', 7: 'R2', 8: 'R3', 9: 'R4'}, 'levels': [], 'description': ['Donation (BTC): 1B8523u9AuZ69j98nDrLJ7TMDEM27erXLx', ' ', 'All important Pivot Points including:', 'Classic1, Classic2, Camarilla, Woodie, Floor, Fibonacci, Fibonacci_Retracement', 'Fully Coded By Hossein Nouri', 'Email : hsn.nouri@gmail.com', 'Skype : hsn.nouri', 'Telegram : @hypernova1990', 'Website : http://www.dlikedeveloper.com', 'MQL5 Profile : https://www.mql5.com/en/users/hsnnouri', ' ', 'Feel free to contact me for MQL4/MQL5/Pine coding.'], 'name': 'All Pivot Points', 'source': 'MQL5 Indicators/All Pivot Points MT5/All Pivot Points.mq5', 'folder': 'All Pivot Points MT5', 'inputs': [{'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 16408, 'label': 'Timeframe', 'sinput': False}, {'mql': 'CalculationMode', 'py': 'CalculationMode', 'param': 'CalculationMode', 'type': 'int', 'default': 0, 'label': 'Calculation Mode', 'sinput': False}, {'mql': 'InpShowMode', 'py': 'InpShowMode', 'param': 'InpShowMode', 'type': 'int', 'default': 1, 'label': 'Displaying Mode', 'sinput': False}, {'mql': 'InpHistoricalBars', 'py': 'InpHistoricalBars', 'param': 'InpHistoricalBars', 'type': 'int', 'default': 0, 'label': 'Historical Bars (0=All)', 'sinput': False}, {'mql': 'InpShowLabels', 'py': 'InpShowLabels', 'param': 'InpShowLabels', 'type': 'bool', 'default': True, 'label': 'Show Labels', 'sinput': False}, {'mql': 'InpShowPriceTags', 'py': 'InpShowPriceTags', 'param': 'InpShowPriceTags', 'type': 'bool', 'default': True, 'label': 'Show Price Tags', 'sinput': False}, {'mql': 'InpIncludeSundays', 'py': 'InpIncludeSundays', 'param': 'InpIncludeSundays', 'type': 'bool', 'default': True, 'label': 'Include Sundays', 'sinput': False}, {'mql': 'InpDesc1', 'py': 'InpDesc1', 'param': None, 'type': 'string', 'default': '********* Fibonacci Levels *********', 'label': 'Description', 'sinput': False}, {'mql': 'InpFibR1S1', 'py': 'InpFibR1S1', 'param': 'InpFibR1S1', 'type': 'double', 'default': 38.2, 'label': 'R1/S1', 'sinput': False}, {'mql': 'InpFibR2S2', 'py': 'InpFibR2S2', 'param': 'InpFibR2S2', 'type': 'double', 'default': 61.8, 'label': 'R2/S2', 'sinput': False}, {'mql': 'InpFibR3S3', 'py': 'InpFibR3S3', 'param': 'InpFibR3S3', 'type': 'double', 'default': 100.0, 'label': 'R3/S3', 'sinput': False}, {'mql': 'InpFibR4S4', 'py': 'InpFibR4S4', 'param': 'InpFibR4S4', 'type': 'double', 'default': 161.8, 'label': 'R4/S4', 'sinput': False}, {'mql': 'InpDesc2', 'py': 'InpDesc2', 'param': None, 'type': 'string', 'default': '*********** Active Lines ***********', 'label': 'Description', 'sinput': False}, {'mql': 'InpShowPivot', 'py': 'InpShowPivot', 'param': 'InpShowPivot', 'type': 'bool', 'default': True, 'label': 'Pivot', 'sinput': False}, {'mql': 'InpShowS1', 'py': 'InpShowS1', 'param': 'InpShowS1', 'type': 'bool', 'default': True, 'label': 'S1', 'sinput': False}, {'mql': 'InpShowS2', 'py': 'InpShowS2', 'param': 'InpShowS2', 'type': 'bool', 'default': True, 'label': 'S2', 'sinput': False}, {'mql': 'InpShowS3', 'py': 'InpShowS3', 'param': 'InpShowS3', 'type': 'bool', 'default': True, 'label': 'S3', 'sinput': False}, {'mql': 'InpShowS4', 'py': 'InpShowS4', 'param': 'InpShowS4', 'type': 'bool', 'default': True, 'label': 'S4', 'sinput': False}, {'mql': 'InpShowR1', 'py': 'InpShowR1', 'param': 'InpShowR1', 'type': 'bool', 'default': True, 'label': 'R1', 'sinput': False}, {'mql': 'InpShowR2', 'py': 'InpShowR2', 'param': 'InpShowR2', 'type': 'bool', 'default': True, 'label': 'R2', 'sinput': False}, {'mql': 'InpShowR3', 'py': 'InpShowR3', 'param': 'InpShowR3', 'type': 'bool', 'default': True, 'label': 'R3', 'sinput': False}, {'mql': 'InpShowR4', 'py': 'InpShowR4', 'param': 'InpShowR4', 'type': 'bool', 'default': True, 'label': 'R4', 'sinput': False}, {'mql': 'InpDesc3', 'py': 'InpDesc3', 'param': None, 'type': 'string', 'default': '*********** Line Color ***********', 'label': 'Description', 'sinput': False}, {'mql': 'InpPivotColor', 'py': 'InpPivotColor', 'param': None, 'type': 'color', 'default': 13882323, 'label': 'Pivot', 'sinput': False}, {'mql': 'InpS1Color', 'py': 'InpS1Color', 'param': None, 'type': 'color', 'default': 255, 'label': 'S1', 'sinput': False}, {'mql': 'InpS2Color', 'py': 'InpS2Color', 'param': None, 'type': 'color', 'default': 3937500, 'label': 'S2', 'sinput': False}, {'mql': 'InpS3Color', 'py': 'InpS3Color', 'param': None, 'type': 'color', 'default': 2237106, 'label': 'S3', 'sinput': False}, {'mql': 'InpS4Color', 'py': 'InpS4Color', 'param': None, 'type': 'color', 'default': 128, 'label': 'S4', 'sinput': False}, {'mql': 'InpR1Color', 'py': 'InpR1Color', 'param': None, 'type': 'color', 'default': 65280, 'label': 'R1', 'sinput': False}, {'mql': 'InpR2Color', 'py': 'InpR2Color', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'R2', 'sinput': False}, {'mql': 'InpR3Color', 'py': 'InpR3Color', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'R3', 'sinput': False}, {'mql': 'InpR4Color', 'py': 'InpR4Color', 'param': None, 'type': 'color', 'default': 5737262, 'label': 'R4', 'sinput': False}, {'mql': 'InpDesc4', 'py': 'InpDesc4', 'param': None, 'type': 'string', 'default': '*********** Line Style ***********', 'label': 'Description', 'sinput': False}, {'mql': 'InpPivotStyle', 'py': 'InpPivotStyle', 'param': 'InpPivotStyle', 'type': 'int', 'default': 0, 'label': 'Pivot', 'sinput': False}, {'mql': 'InpS1Style', 'py': 'InpS1Style', 'param': 'InpS1Style', 'type': 'int', 'default': 0, 'label': 'S1', 'sinput': False}, {'mql': 'InpS2Style', 'py': 'InpS2Style', 'param': 'InpS2Style', 'type': 'int', 'default': 0, 'label': 'S2', 'sinput': False}, {'mql': 'InpS3Style', 'py': 'InpS3Style', 'param': 'InpS3Style', 'type': 'int', 'default': 0, 'label': 'S3', 'sinput': False}, {'mql': 'InpS4Style', 'py': 'InpS4Style', 'param': 'InpS4Style', 'type': 'int', 'default': 0, 'label': 'S4', 'sinput': False}, {'mql': 'InpR1Style', 'py': 'InpR1Style', 'param': 'InpR1Style', 'type': 'int', 'default': 0, 'label': 'R1', 'sinput': False}, {'mql': 'InpR2Style', 'py': 'InpR2Style', 'param': 'InpR2Style', 'type': 'int', 'default': 0, 'label': 'R2', 'sinput': False}, {'mql': 'InpR3Style', 'py': 'InpR3Style', 'param': 'InpR3Style', 'type': 'int', 'default': 0, 'label': 'R3', 'sinput': False}, {'mql': 'InpR4Style', 'py': 'InpR4Style', 'param': 'InpR4Style', 'type': 'int', 'default': 0, 'label': 'R4', 'sinput': False}, {'mql': 'InpDesc5', 'py': 'InpDesc5', 'param': None, 'type': 'string', 'default': '*********** Line Width ***********', 'label': 'Description', 'sinput': False}, {'mql': 'InpPivotWidth', 'py': 'InpPivotWidth', 'param': 'InpPivotWidth', 'type': 'int', 'default': 1, 'label': 'Pivot', 'sinput': False}, {'mql': 'InpS1Width', 'py': 'InpS1Width', 'param': 'InpS1Width', 'type': 'int', 'default': 1, 'label': 'S1', 'sinput': False}, {'mql': 'InpS2Width', 'py': 'InpS2Width', 'param': 'InpS2Width', 'type': 'int', 'default': 1, 'label': 'S2', 'sinput': False}, {'mql': 'InpS3Width', 'py': 'InpS3Width', 'param': 'InpS3Width', 'type': 'int', 'default': 1, 'label': 'S3', 'sinput': False}, {'mql': 'InpS4Width', 'py': 'InpS4Width', 'param': 'InpS4Width', 'type': 'int', 'default': 1, 'label': 'S4', 'sinput': False}, {'mql': 'InpR1Width', 'py': 'InpR1Width', 'param': 'InpR1Width', 'type': 'int', 'default': 1, 'label': 'R1', 'sinput': False}, {'mql': 'InpR2Width', 'py': 'InpR2Width', 'param': 'InpR2Width', 'type': 'int', 'default': 1, 'label': 'R2', 'sinput': False}, {'mql': 'InpR3Width', 'py': 'InpR3Width', 'param': 'InpR3Width', 'type': 'int', 'default': 1, 'label': 'R3', 'sinput': False}, {'mql': 'InpR4Width', 'py': 'InpR4Width', 'param': 'InpR4Width', 'type': 'int', 'default': 1, 'label': 'R4', 'sinput': False}, {'mql': 'DescAlertLines', 'py': 'DescAlertLines', 'param': None, 'type': 'string', 'default': '*********** Alert Lines ***********', 'label': 'Description', 'sinput': False}, {'mql': 'InpPivotAlert', 'py': 'InpPivotAlert', 'param': 'InpPivotAlert', 'type': 'bool', 'default': True, 'label': 'Pivot', 'sinput': False}, {'mql': 'InpS1Alert', 'py': 'InpS1Alert', 'param': 'InpS1Alert', 'type': 'bool', 'default': True, 'label': 'S1', 'sinput': False}, {'mql': 'InpS2Alert', 'py': 'InpS2Alert', 'param': 'InpS2Alert', 'type': 'bool', 'default': True, 'label': 'S2', 'sinput': False}, {'mql': 'InpS3Alert', 'py': 'InpS3Alert', 'param': 'InpS3Alert', 'type': 'bool', 'default': True, 'label': 'S3', 'sinput': False}, {'mql': 'InpS4Alert', 'py': 'InpS4Alert', 'param': 'InpS4Alert', 'type': 'bool', 'default': True, 'label': 'S4', 'sinput': False}, {'mql': 'InpR1Alert', 'py': 'InpR1Alert', 'param': 'InpR1Alert', 'type': 'bool', 'default': True, 'label': 'R1', 'sinput': False}, {'mql': 'InpR2Alert', 'py': 'InpR2Alert', 'param': 'InpR2Alert', 'type': 'bool', 'default': True, 'label': 'R2', 'sinput': False}, {'mql': 'InpR3Alert', 'py': 'InpR3Alert', 'param': 'InpR3Alert', 'type': 'bool', 'default': True, 'label': 'R3', 'sinput': False}, {'mql': 'InpR4Alert', 'py': 'InpR4Alert', 'param': 'InpR4Alert', 'type': 'bool', 'default': True, 'label': 'R4', 'sinput': False}, {'mql': 'DescAlertSettings', 'py': 'DescAlertSettings', 'param': None, 'type': 'string', 'default': '********** Alert Settings **********', 'label': 'Description', 'sinput': False}, {'mql': 'InpAlertShowPopup', 'py': 'InpAlertShowPopup', 'param': 'InpAlertShowPopup', 'type': 'bool', 'default': True, 'label': 'Show Pop-up', 'sinput': False}, {'mql': 'InpAlertSendEmail', 'py': 'InpAlertSendEmail', 'param': 'InpAlertSendEmail', 'type': 'bool', 'default': False, 'label': 'Send Email', 'sinput': False}, {'mql': 'InpAlertSendNotification', 'py': 'InpAlertSendNotification', 'param': 'InpAlertSendNotification', 'type': 'bool', 'default': False, 'label': 'Send Notification', 'sinput': False}, {'mql': 'InpAlertPlaySound', 'py': 'InpAlertPlaySound', 'param': 'InpAlertPlaySound', 'type': 'bool', 'default': False, 'label': 'Play Sound', 'sinput': False}, {'mql': 'InpAlertSoundFile', 'py': 'InpAlertSoundFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound File', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CALC_MODE
CALC_MODE_CLASSIC1 = 0
CALC_MODE_CLASSIC2 = 1
CALC_MODE_CAMARILLA = 2
CALC_MODE_WOODIE = 3
CALC_MODE_FIBONACCI = 4
CALC_MODE_FLOOR = 5
CALC_MODE_FIBONACCI_RETRACEMENT = 6
_enum('ENUM_CALC_MODE', {0: 'CALC_MODE_CLASSIC1', 1: 'CALC_MODE_CLASSIC2', 2: 'CALC_MODE_CAMARILLA', 3: 'CALC_MODE_WOODIE', 4: 'CALC_MODE_FIBONACCI', 5: 'CALC_MODE_FLOOR', 6: 'CALC_MODE_FIBONACCI_RETRACEMENT'})

# enum ENUM_SHOW_MODE
SHOW_MODE_TODAY = 0
SHOW_MODE_HISTORICAL = 1
_enum('ENUM_SHOW_MODE', {0: 'SHOW_MODE_TODAY', 1: 'SHOW_MODE_HISTORICAL'})

# ---- inputs and global variables
PivotBuffer = Arr(0, 0.0)
S1Buffer = Arr(0, 0.0)
S2Buffer = Arr(0, 0.0)
S3Buffer = Arr(0, 0.0)
S4Buffer = Arr(0, 0.0)
R1Buffer = Arr(0, 0.0)
R2Buffer = Arr(0, 0.0)
R3Buffer = Arr(0, 0.0)
R4Buffer = Arr(0, 0.0)
InpTimeframe = _input('InpTimeframe', PERIOD_D1)  # Timeframe
CalculationMode = _input('CalculationMode', CALC_MODE_CLASSIC1)  # Calculation Mode
InpShowMode = _input('InpShowMode', SHOW_MODE_HISTORICAL)  # Displaying Mode
InpHistoricalBars = _input('InpHistoricalBars', 0)  # Historical Bars (0=All)
InpShowLabels = _input('InpShowLabels', True)  # Show Labels
InpShowPriceTags = _input('InpShowPriceTags', True)  # Show Price Tags
InpIncludeSundays = _input('InpIncludeSundays', True)  # Include Sundays
InpDesc1 = _input('InpDesc1', '********* Fibonacci Levels *********')  # Description
InpFibR1S1 = _input('InpFibR1S1', 38.2)  # R1/S1
InpFibR2S2 = _input('InpFibR2S2', 61.8)  # R2/S2
InpFibR3S3 = _input('InpFibR3S3', 100.0)  # R3/S3
InpFibR4S4 = _input('InpFibR4S4', 161.8)  # R4/S4
InpDesc2 = _input('InpDesc2', '*********** Active Lines ***********')  # Description
InpShowPivot = _input('InpShowPivot', True)  # Pivot
InpShowS1 = _input('InpShowS1', True)  # S1
InpShowS2 = _input('InpShowS2', True)  # S2
InpShowS3 = _input('InpShowS3', True)  # S3
InpShowS4 = _input('InpShowS4', True)  # S4
InpShowR1 = _input('InpShowR1', True)  # R1
InpShowR2 = _input('InpShowR2', True)  # R2
InpShowR3 = _input('InpShowR3', True)  # R3
InpShowR4 = _input('InpShowR4', True)  # R4
InpDesc3 = _input('InpDesc3', '*********** Line Color ***********')  # Description
InpPivotColor = _input('InpPivotColor', clrLightGray)  # Pivot
InpS1Color = _input('InpS1Color', clrRed)  # S1
InpS2Color = _input('InpS2Color', clrCrimson)  # S2
InpS3Color = _input('InpS3Color', clrFireBrick)  # S3
InpS4Color = _input('InpS4Color', clrMaroon)  # S4
InpR1Color = _input('InpR1Color', clrLime)  # R1
InpR2Color = _input('InpR2Color', clrLimeGreen)  # R2
InpR3Color = _input('InpR3Color', clrMediumSeaGreen)  # R3
InpR4Color = _input('InpR4Color', clrSeaGreen)  # R4
InpDesc4 = _input('InpDesc4', '*********** Line Style ***********')  # Description
InpPivotStyle = _input('InpPivotStyle', STYLE_SOLID)  # Pivot
InpS1Style = _input('InpS1Style', STYLE_SOLID)  # S1
InpS2Style = _input('InpS2Style', STYLE_SOLID)  # S2
InpS3Style = _input('InpS3Style', STYLE_SOLID)  # S3
InpS4Style = _input('InpS4Style', STYLE_SOLID)  # S4
InpR1Style = _input('InpR1Style', STYLE_SOLID)  # R1
InpR2Style = _input('InpR2Style', STYLE_SOLID)  # R2
InpR3Style = _input('InpR3Style', STYLE_SOLID)  # R3
InpR4Style = _input('InpR4Style', STYLE_SOLID)  # R4
InpDesc5 = _input('InpDesc5', '*********** Line Width ***********')  # Description
InpPivotWidth = _input('InpPivotWidth', 1)  # Pivot
InpS1Width = _input('InpS1Width', 1)  # S1
InpS2Width = _input('InpS2Width', 1)  # S2
InpS3Width = _input('InpS3Width', 1)  # S3
InpS4Width = _input('InpS4Width', 1)  # S4
InpR1Width = _input('InpR1Width', 1)  # R1
InpR2Width = _input('InpR2Width', 1)  # R2
InpR3Width = _input('InpR3Width', 1)  # R3
InpR4Width = _input('InpR4Width', 1)  # R4
DescAlertLines = _input('DescAlertLines', '*********** Alert Lines ***********')  # Description
InpPivotAlert = _input('InpPivotAlert', True)  # Pivot
InpS1Alert = _input('InpS1Alert', True)  # S1
InpS2Alert = _input('InpS2Alert', True)  # S2
InpS3Alert = _input('InpS3Alert', True)  # S3
InpS4Alert = _input('InpS4Alert', True)  # S4
InpR1Alert = _input('InpR1Alert', True)  # R1
InpR2Alert = _input('InpR2Alert', True)  # R2
InpR3Alert = _input('InpR3Alert', True)  # R3
InpR4Alert = _input('InpR4Alert', True)  # R4
DescAlertSettings = _input('DescAlertSettings', '********** Alert Settings **********')  # Description
InpAlertShowPopup = _input('InpAlertShowPopup', True)  # Show Pop-up
InpAlertSendEmail = _input('InpAlertSendEmail', False)  # Send Email
InpAlertSendNotification = _input('InpAlertSendNotification', False)  # Send Notification
InpAlertPlaySound = _input('InpAlertPlaySound', False)  # Play Sound
InpAlertSoundFile = _input('InpAlertSoundFile', 'alert.wav')  # Sound File
StartTime = 0
StopTime = 0
OneCandleGap = 0
OneCandle = 0
R1 = 0.0
R2 = 0.0
R3 = 0.0
R4 = 0.0
S1 = 0.0
S2 = 0.0
S3 = 0.0
S4 = 0.0
PP = 0.0
NextDayR1 = 0.0
NextDayR2 = 0.0
NextDayR3 = 0.0
NextDayR4 = 0.0
NextDayS1 = 0.0
NextDayS2 = 0.0
NextDayS3 = 0.0
NextDayS4 = 0.0
NextDayPP = 0.0
prefix = ""
CalcTypeAbb = ""
Status = True
CurrentCandleIndex = 0
PrevCandleIndex = 1
LastTouchedLine = ''
LastTickClose = 0.0

def OnInit():
    global OneCandle, OneCandleGap, Status
    SetIndexBuffer(0, PivotBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, S1Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, S2Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, S3Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, S4Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, R1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, R2Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, R3Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, R4Buffer, INDICATOR_DATA)
    if InpShowMode == SHOW_MODE_TODAY:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(5, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(6, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(7, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(8, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(0, PLOT_LINE_STYLE, InpPivotStyle)
    PlotIndexSetInteger(1, PLOT_LINE_STYLE, InpS1Style)
    PlotIndexSetInteger(2, PLOT_LINE_STYLE, InpS2Style)
    PlotIndexSetInteger(3, PLOT_LINE_STYLE, InpS3Style)
    PlotIndexSetInteger(4, PLOT_LINE_STYLE, InpS4Style)
    PlotIndexSetInteger(5, PLOT_LINE_STYLE, InpR1Style)
    PlotIndexSetInteger(6, PLOT_LINE_STYLE, InpR2Style)
    PlotIndexSetInteger(7, PLOT_LINE_STYLE, InpR3Style)
    PlotIndexSetInteger(8, PLOT_LINE_STYLE, InpR4Style)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, InpPivotWidth)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, InpS1Width)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, InpS2Width)
    PlotIndexSetInteger(3, PLOT_LINE_WIDTH, InpS3Width)
    PlotIndexSetInteger(4, PLOT_LINE_WIDTH, InpS4Width)
    PlotIndexSetInteger(5, PLOT_LINE_WIDTH, InpR1Width)
    PlotIndexSetInteger(6, PLOT_LINE_WIDTH, InpR2Width)
    PlotIndexSetInteger(7, PLOT_LINE_WIDTH, InpR3Width)
    PlotIndexSetInteger(8, PLOT_LINE_WIDTH, InpR4Width)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, InpPivotColor)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, InpS1Color)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, InpS2Color)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, InpS3Color)
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, InpS4Color)
    PlotIndexSetInteger(5, PLOT_LINE_COLOR, InpR1Color)
    PlotIndexSetInteger(6, PLOT_LINE_COLOR, InpR2Color)
    PlotIndexSetInteger(7, PLOT_LINE_COLOR, InpR3Color)
    PlotIndexSetInteger(8, PLOT_LINE_COLOR, InpR4Color)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(S1Buffer, True)
    ArraySetAsSeries(S2Buffer, True)
    ArraySetAsSeries(S3Buffer, True)
    ArraySetAsSeries(S4Buffer, True)
    ArraySetAsSeries(R1Buffer, True)
    ArraySetAsSeries(R2Buffer, True)
    ArraySetAsSeries(R3Buffer, True)
    ArraySetAsSeries(R4Buffer, True)
    ArraySetAsSeries(PivotBuffer, True)
    StringConcatenate(_GlobRef(globals(), 'prefix'), EnumToString(CalculationMode, 'ENUM_CALC_MODE'), '_', EnumToString(InpTimeframe, 'ENUM_TIMEFRAMES'), '_')
    Status = True
    if Period() > InpTimeframe:
        Alert('Loading failed, please set a higher timeframe.')
        Status = False
    ExtractCalculationType()
    PlotIndexSetString(0, PLOT_LABEL, 'Pivot (' + CalcTypeAbb + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'S1 (' + CalcTypeAbb + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'S2 (' + CalcTypeAbb + ')')
    PlotIndexSetString(3, PLOT_LABEL, 'S3 (' + CalcTypeAbb + ')')
    PlotIndexSetString(4, PLOT_LABEL, 'S4 (' + CalcTypeAbb + ')')
    PlotIndexSetString(5, PLOT_LABEL, 'R1 (' + CalcTypeAbb + ')')
    PlotIndexSetString(6, PLOT_LABEL, 'R2 (' + CalcTypeAbb + ')')
    PlotIndexSetString(7, PLOT_LABEL, 'R3 (' + CalcTypeAbb + ')')
    PlotIndexSetString(8, PLOT_LABEL, 'R4 (' + CalcTypeAbb + ')')
    OneCandleGap = PeriodSeconds(InpTimeframe)
    OneCandle = PeriodSeconds(PERIOD_CURRENT)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    if not Status:
        return 0
    limit = 0
    limit = ((rates_total - 1) if (prev_calculated == 0) else (rates_total - prev_calculated + 1))
    if rates_total > prev_calculated:
        if not IsChartLoaded():
            return prev_calculated
        UpdateCandlesIndex()
        if InpShowMode == SHOW_MODE_HISTORICAL:
            if CalculationMode == CALC_MODE_CAMARILLA:
                j = 0
                for i in range(0, limit):
                    if InpHistoricalBars != 0 and i > InpHistoricalBars:
                        PivotBuffer[i] = 0.0
                        S1Buffer[i] = 0.0
                        S2Buffer[i] = 0.0
                        S3Buffer[i] = 0.0
                        S4Buffer[i] = 0.0
                        R1Buffer[i] = 0.0
                        R2Buffer[i] = 0.0
                        R3Buffer[i] = 0.0
                        R4Buffer[i] = 0.0
                        continue
                    if time[i] >= iTime(Symbol(), InpTimeframe, j):
                        calculateHistCamarilla(i, j + 1)
                    else:
                        j += 1
                        calculateHistCamarilla(i, j + 1)
                calculateCamarilla()
            elif CalculationMode == CALC_MODE_CLASSIC1:
                j = 0
                for i in range(0, limit):
                    if InpHistoricalBars != 0 and i > InpHistoricalBars:
                        PivotBuffer[i] = 0.0
                        S1Buffer[i] = 0.0
                        S2Buffer[i] = 0.0
                        S3Buffer[i] = 0.0
                        S4Buffer[i] = 0.0
                        R1Buffer[i] = 0.0
                        R2Buffer[i] = 0.0
                        R3Buffer[i] = 0.0
                        R4Buffer[i] = 0.0
                        continue
                    if time[i] >= iTime(Symbol(), InpTimeframe, j):
                        calculateHistClassic1(i, j + 1)
                    else:
                        j += 1
                        calculateHistClassic1(i, j + 1)
                calculateClassic1()
            elif CalculationMode == CALC_MODE_CLASSIC2:
                j = 0
                for i in range(0, limit):
                    if InpHistoricalBars != 0 and i > InpHistoricalBars:
                        PivotBuffer[i] = 0.0
                        S1Buffer[i] = 0.0
                        S2Buffer[i] = 0.0
                        S3Buffer[i] = 0.0
                        S4Buffer[i] = 0.0
                        R1Buffer[i] = 0.0
                        R2Buffer[i] = 0.0
                        R3Buffer[i] = 0.0
                        R4Buffer[i] = 0.0
                        continue
                    if time[i] >= iTime(Symbol(), InpTimeframe, j):
                        calculateHistClassic2(i, j + 1)
                    else:
                        j += 1
                        calculateHistClassic2(i, j + 1)
                calculateClassic2()
            elif CalculationMode == CALC_MODE_WOODIE:
                j = 0
                for i in range(0, limit):
                    if InpHistoricalBars != 0 and i > InpHistoricalBars:
                        PivotBuffer[i] = 0.0
                        S1Buffer[i] = 0.0
                        S2Buffer[i] = 0.0
                        S3Buffer[i] = 0.0
                        S4Buffer[i] = 0.0
                        R1Buffer[i] = 0.0
                        R2Buffer[i] = 0.0
                        R3Buffer[i] = 0.0
                        R4Buffer[i] = 0.0
                        continue
                    if time[i] >= iTime(Symbol(), InpTimeframe, j):
                        calculateHistWoodie(i, j + 1)
                    else:
                        j += 1
                        calculateHistWoodie(i, j + 1)
                calculateWoodie()
            elif CalculationMode == CALC_MODE_FIBONACCI:
                j = 0
                for i in range(0, limit):
                    if InpHistoricalBars != 0 and i > InpHistoricalBars:
                        PivotBuffer[i] = 0.0
                        S1Buffer[i] = 0.0
                        S2Buffer[i] = 0.0
                        S3Buffer[i] = 0.0
                        S4Buffer[i] = 0.0
                        R1Buffer[i] = 0.0
                        R2Buffer[i] = 0.0
                        R3Buffer[i] = 0.0
                        R4Buffer[i] = 0.0
                        continue
                    if time[i] >= iTime(Symbol(), InpTimeframe, j):
                        calculateHistFibonacci(i, j + 1)
                    else:
                        j += 1
                        calculateHistFibonacci(i, j + 1)
                calculateFibonacci()
            elif CalculationMode == CALC_MODE_FLOOR:
                j = 0
                for i in range(0, limit):
                    if InpHistoricalBars != 0 and i > InpHistoricalBars:
                        PivotBuffer[i] = 0.0
                        S1Buffer[i] = 0.0
                        S2Buffer[i] = 0.0
                        S3Buffer[i] = 0.0
                        S4Buffer[i] = 0.0
                        R1Buffer[i] = 0.0
                        R2Buffer[i] = 0.0
                        R3Buffer[i] = 0.0
                        R4Buffer[i] = 0.0
                        continue
                    if time[i] >= iTime(Symbol(), InpTimeframe, j):
                        calculateHistFloor(i, j + 1)
                    else:
                        j += 1
                        calculateHistFloor(i, j + 1)
                calculateFloor()
            elif CalculationMode == CALC_MODE_FIBONACCI_RETRACEMENT:
                j = 0
                for i in range(0, limit):
                    if InpHistoricalBars != 0 and i > InpHistoricalBars:
                        PivotBuffer[i] = 0.0
                        S1Buffer[i] = 0.0
                        S2Buffer[i] = 0.0
                        S3Buffer[i] = 0.0
                        S4Buffer[i] = 0.0
                        R1Buffer[i] = 0.0
                        R2Buffer[i] = 0.0
                        R3Buffer[i] = 0.0
                        R4Buffer[i] = 0.0
                        continue
                    if time[i] >= iTime(Symbol(), InpTimeframe, j):
                        calculateHistFibonacciRet(i, j + 1)
                    else:
                        j += 1
                        calculateHistFibonacciRet(i, j + 1)
                calculateFibonacciRet()
        if InpShowMode == SHOW_MODE_TODAY:
            if CalculationMode == CALC_MODE_CLASSIC1:
                calculateClassic1()
            if CalculationMode == CALC_MODE_CLASSIC2:
                calculateClassic2()
            if CalculationMode == CALC_MODE_CAMARILLA:
                calculateCamarilla()
            if CalculationMode == CALC_MODE_WOODIE:
                calculateWoodie()
            if CalculationMode == CALC_MODE_FIBONACCI:
                calculateFibonacci()
            if CalculationMode == CALC_MODE_FLOOR:
                calculateFloor()
            if CalculationMode == CALC_MODE_FIBONACCI_RETRACEMENT:
                calculateFibonacciRet()
    RefreshAlerts()
    return rates_total

def calculateHistFibonacciRet(index, barIndex):
    barIndex = Box(barIndex)
    CorrectBarIndex(barIndex)
    prevRange = iHigh(Symbol(), InpTimeframe, barIndex.v) - iLow(Symbol(), InpTimeframe, barIndex.v)
    prevHigh = iHigh(Symbol(), InpTimeframe, barIndex.v)
    prevLow = iLow(Symbol(), InpTimeframe, barIndex.v)
    prevClose = iClose(Symbol(), InpTimeframe, barIndex.v)
    PivotBuffer[index] = NormalizeDouble(prevLow + (0.5 * prevRange), Digits())
    R1Buffer[index] = NormalizeDouble(prevLow + (0.618 * prevRange), Digits())
    R2Buffer[index] = NormalizeDouble(prevLow + (0.786 * prevRange), Digits())
    R3Buffer[index] = NormalizeDouble(prevHigh, Digits())
    R4Buffer[index] = NormalizeDouble(prevLow + (1.382 * prevRange), Digits())
    S1Buffer[index] = NormalizeDouble(prevLow + (0.382 * prevRange), Digits())
    S2Buffer[index] = NormalizeDouble(prevLow + (0.236 * prevRange), Digits())
    S3Buffer[index] = NormalizeDouble(prevLow, Digits())
    S4Buffer[index] = NormalizeDouble(prevLow - (0.382 * prevRange), Digits())
    checkVisiblity(index)

def calculateFibonacciRet():
    global PP, R1, R2, R3, R4, S1, S2, S3, S4
    prevRange = iHigh(Symbol(), InpTimeframe, 1) - iLow(Symbol(), InpTimeframe, 1)
    prevHigh = iHigh(Symbol(), InpTimeframe, 1)
    prevLow = iLow(Symbol(), InpTimeframe, 1)
    prevClose = iClose(Symbol(), InpTimeframe, 1)
    PP = NormalizeDouble(prevLow + (0.5 * prevRange), Digits())
    R1 = NormalizeDouble(prevLow + (0.618 * prevRange), Digits())
    R2 = NormalizeDouble(prevLow + (0.786 * prevRange), Digits())
    R3 = NormalizeDouble(prevHigh, Digits())
    R4 = NormalizeDouble(prevLow + (1.382 * prevRange), Digits())
    S1 = NormalizeDouble(prevLow + (0.382 * prevRange), Digits())
    S2 = NormalizeDouble(prevLow + (0.236 * prevRange), Digits())
    S3 = NormalizeDouble(prevLow, Digits())
    S4 = NormalizeDouble(prevLow - (0.382 * prevRange), Digits())
    DrawOnChart()

def calculateHistFloor(index, barIndex):
    barIndex = Box(barIndex)
    CorrectBarIndex(barIndex)
    prevRange = iHigh(Symbol(), InpTimeframe, barIndex.v) - iLow(Symbol(), InpTimeframe, barIndex.v)
    prevHigh = iHigh(Symbol(), InpTimeframe, barIndex.v)
    prevLow = iLow(Symbol(), InpTimeframe, barIndex.v)
    prevClose = iClose(Symbol(), InpTimeframe, barIndex.v)
    PivotBuffer[index] = NormalizeDouble((prevHigh + prevLow + prevClose) / 3, Digits())
    R1Buffer[index] = NormalizeDouble((PivotBuffer[index] * 2) - prevLow, Digits())
    S1Buffer[index] = NormalizeDouble((PivotBuffer[index] * 2) - prevHigh, Digits())
    R2Buffer[index] = NormalizeDouble(PivotBuffer[index] + prevHigh - prevLow, Digits())
    S2Buffer[index] = NormalizeDouble(PivotBuffer[index] - prevHigh + prevLow, Digits())
    R3Buffer[index] = NormalizeDouble(R1Buffer[index] + (prevHigh - prevLow), Digits())
    S3Buffer[index] = NormalizeDouble(prevLow - (2 * (prevHigh - PivotBuffer[index])), Digits())
    checkVisiblity(index)

def calculateFloor():
    global PP, R1, R2, R3, S1, S2, S3
    prevRange = iHigh(Symbol(), InpTimeframe, PrevCandleIndex) - iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevHigh = iHigh(Symbol(), InpTimeframe, PrevCandleIndex)
    prevLow = iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevClose = iClose(Symbol(), InpTimeframe, PrevCandleIndex)
    PP = NormalizeDouble((prevHigh + prevLow + prevClose) / 3, Digits())
    R1 = NormalizeDouble((PP * 2) - prevLow, Digits())
    S1 = NormalizeDouble((PP * 2) - prevHigh, Digits())
    R2 = NormalizeDouble(PP + prevHigh - prevLow, Digits())
    S2 = NormalizeDouble(PP - prevHigh + prevLow, Digits())
    R3 = NormalizeDouble(R1 + (prevHigh - prevLow), Digits())
    S3 = NormalizeDouble(prevLow - (2 * (prevHigh - PP)), Digits())
    DrawOnChart()

def calculateHistFibonacci(index, barIndex):
    barIndex = Box(barIndex)
    CorrectBarIndex(barIndex)
    prevRange = iHigh(Symbol(), InpTimeframe, barIndex.v) - iLow(Symbol(), InpTimeframe, barIndex.v)
    prevHigh = iHigh(Symbol(), InpTimeframe, barIndex.v)
    prevLow = iLow(Symbol(), InpTimeframe, barIndex.v)
    prevClose = iClose(Symbol(), InpTimeframe, barIndex.v)
    PivotBuffer[index] = NormalizeDouble((prevHigh + prevLow + prevClose) / 3, Digits())
    R1Buffer[index] = NormalizeDouble(PivotBuffer[index] + ((InpFibR1S1 / 100) * (prevHigh - prevLow)), Digits())
    R2Buffer[index] = NormalizeDouble(PivotBuffer[index] + ((InpFibR2S2 / 100) * (prevHigh - prevLow)), Digits())
    R3Buffer[index] = NormalizeDouble(PivotBuffer[index] + ((InpFibR3S3 / 100) * (prevHigh - prevLow)), Digits())
    R4Buffer[index] = NormalizeDouble(PivotBuffer[index] + ((InpFibR4S4 / 100) * (prevHigh - prevLow)), Digits())
    S1Buffer[index] = NormalizeDouble(PivotBuffer[index] - ((InpFibR1S1 / 100) * (prevHigh - prevLow)), Digits())
    S2Buffer[index] = NormalizeDouble(PivotBuffer[index] - ((InpFibR2S2 / 100) * (prevHigh - prevLow)), Digits())
    S3Buffer[index] = NormalizeDouble(PivotBuffer[index] - ((InpFibR3S3 / 100) * (prevHigh - prevLow)), Digits())
    S4Buffer[index] = NormalizeDouble(PivotBuffer[index] - ((InpFibR4S4 / 100) * (prevHigh - prevLow)), Digits())
    checkVisiblity(index)

def calculateFibonacci():
    global PP, R1, R2, R3, R4, S1, S2, S3, S4
    prevRange = iHigh(Symbol(), InpTimeframe, PrevCandleIndex) - iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevHigh = iHigh(Symbol(), InpTimeframe, PrevCandleIndex)
    prevLow = iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevClose = iClose(Symbol(), InpTimeframe, PrevCandleIndex)
    PP = NormalizeDouble((prevHigh + prevLow + prevClose) / 3, Digits())
    R1 = NormalizeDouble(PP + ((InpFibR1S1 / 100) * (prevHigh - prevLow)), Digits())
    R2 = NormalizeDouble(PP + ((InpFibR2S2 / 100) * (prevHigh - prevLow)), Digits())
    R3 = NormalizeDouble(PP + ((InpFibR3S3 / 100) * (prevHigh - prevLow)), Digits())
    R4 = NormalizeDouble(PP + ((InpFibR4S4 / 100) * (prevHigh - prevLow)), Digits())
    S1 = NormalizeDouble(PP - ((InpFibR1S1 / 100) * (prevHigh - prevLow)), Digits())
    S2 = NormalizeDouble(PP - ((InpFibR2S2 / 100) * (prevHigh - prevLow)), Digits())
    S3 = NormalizeDouble(PP - ((InpFibR3S3 / 100) * (prevHigh - prevLow)), Digits())
    S4 = NormalizeDouble(PP - ((InpFibR4S4 / 100) * (prevHigh - prevLow)), Digits())
    DrawOnChart()

def calculateHistCamarilla(index, barIndex):
    barIndex = Box(barIndex)
    CorrectBarIndex(barIndex)
    camRange = iHigh(Symbol(), InpTimeframe, barIndex.v) - iLow(Symbol(), InpTimeframe, barIndex.v)
    prevHigh = iHigh(Symbol(), InpTimeframe, barIndex.v)
    prevLow = iLow(Symbol(), InpTimeframe, barIndex.v)
    prevClose = iClose(Symbol(), InpTimeframe, barIndex.v)
    R1Buffer[index] = NormalizeDouble(((1.1 / 12) * camRange) + prevClose, Digits())
    R2Buffer[index] = NormalizeDouble(((1.1 / 6) * camRange) + prevClose, Digits())
    R3Buffer[index] = NormalizeDouble(((1.1 / 4) * camRange) + prevClose, Digits())
    R4Buffer[index] = NormalizeDouble(((1.1 / 2) * camRange) + prevClose, Digits())
    S1Buffer[index] = NormalizeDouble(prevClose - ((1.1 / 12) * camRange), Digits())
    S2Buffer[index] = NormalizeDouble(prevClose - ((1.1 / 6) * camRange), Digits())
    S3Buffer[index] = NormalizeDouble(prevClose - ((1.1 / 4) * camRange), Digits())
    S4Buffer[index] = NormalizeDouble(prevClose - ((1.1 / 2) * camRange), Digits())
    PivotBuffer[index] = NormalizeDouble((R1Buffer[index] + S1Buffer[index]) / 2, Digits())
    checkVisiblity(index)

def calculateHistClassic1(index, barIndex):
    barIndex = Box(barIndex)
    CorrectBarIndex(barIndex)
    prevRange = iHigh(Symbol(), InpTimeframe, barIndex.v) - iLow(Symbol(), InpTimeframe, barIndex.v)
    prevHigh = iHigh(Symbol(), InpTimeframe, barIndex.v)
    prevLow = iLow(Symbol(), InpTimeframe, barIndex.v)
    prevClose = iClose(Symbol(), InpTimeframe, barIndex.v)
    PivotBuffer[index] = NormalizeDouble((prevHigh + prevLow + prevClose) / 3, Digits())
    R1Buffer[index] = NormalizeDouble((PivotBuffer[index] * 2) - prevLow, Digits())
    R2Buffer[index] = NormalizeDouble(PivotBuffer[index] + prevRange, Digits())
    R3Buffer[index] = NormalizeDouble(R2Buffer[index] + prevRange, Digits())
    R4Buffer[index] = NormalizeDouble(R3Buffer[index] + prevRange, Digits())
    S1Buffer[index] = NormalizeDouble((PivotBuffer[index] * 2) - prevHigh, Digits())
    S2Buffer[index] = NormalizeDouble(PivotBuffer[index] - prevRange, Digits())
    S3Buffer[index] = NormalizeDouble(S2Buffer[index] - prevRange, Digits())
    S4Buffer[index] = NormalizeDouble(S3Buffer[index] - prevRange, Digits())
    checkVisiblity(index)

def calculateHistClassic2(index, barIndex):
    barIndex = Box(barIndex)
    CorrectBarIndex(barIndex)
    prevRange = iHigh(Symbol(), InpTimeframe, barIndex.v) - iLow(Symbol(), InpTimeframe, barIndex.v)
    prevHigh = iHigh(Symbol(), InpTimeframe, barIndex.v)
    prevLow = iLow(Symbol(), InpTimeframe, barIndex.v)
    prevClose = iClose(Symbol(), InpTimeframe, barIndex.v)
    prevOpen = iOpen(Symbol(), InpTimeframe, barIndex.v)
    PivotBuffer[index] = NormalizeDouble((prevHigh + prevLow + prevClose + prevOpen) / 4, Digits())
    R1Buffer[index] = NormalizeDouble((PivotBuffer[index] * 2) - prevLow, Digits())
    R2Buffer[index] = NormalizeDouble(PivotBuffer[index] + prevRange, Digits())
    R3Buffer[index] = NormalizeDouble(PivotBuffer[index] + (prevRange * 2), Digits())
    R4Buffer[index] = NormalizeDouble(PivotBuffer[index] + (prevRange * 3), Digits())
    S1Buffer[index] = NormalizeDouble((PivotBuffer[index] * 2) - prevHigh, Digits())
    S2Buffer[index] = NormalizeDouble(PivotBuffer[index] - prevRange, Digits())
    S3Buffer[index] = NormalizeDouble(PivotBuffer[index] - (prevRange * 2), Digits())
    S4Buffer[index] = NormalizeDouble(PivotBuffer[index] - (prevRange * 3), Digits())
    checkVisiblity(index)

def calculateHistWoodie(index, barIndex):
    barIndex = Box(barIndex)
    CorrectBarIndex(barIndex)
    prevRange = iHigh(Symbol(), InpTimeframe, barIndex.v) - iLow(Symbol(), InpTimeframe, barIndex.v)
    prevHigh = iHigh(Symbol(), InpTimeframe, barIndex.v)
    prevLow = iLow(Symbol(), InpTimeframe, barIndex.v)
    prevClose = iClose(Symbol(), InpTimeframe, barIndex.v)
    todayOpen = iOpen(Symbol(), InpTimeframe, barIndex.v - 1)
    PivotBuffer[index] = NormalizeDouble((prevHigh + prevLow + (todayOpen * 2)) / 4, Digits())
    R1Buffer[index] = NormalizeDouble((PivotBuffer[index] * 2) - prevLow, Digits())
    R2Buffer[index] = NormalizeDouble(PivotBuffer[index] + prevRange, Digits())
    R3Buffer[index] = NormalizeDouble(prevHigh + (2 * (PivotBuffer[index] - prevLow)), Digits())
    R4Buffer[index] = NormalizeDouble(R3Buffer[index] + prevRange, Digits())
    S1Buffer[index] = NormalizeDouble((PivotBuffer[index] * 2) - prevHigh, Digits())
    S2Buffer[index] = NormalizeDouble(PivotBuffer[index] - prevRange, Digits())
    S3Buffer[index] = NormalizeDouble(prevLow - (2 * (prevHigh - PivotBuffer[index])), Digits())
    S4Buffer[index] = NormalizeDouble(S3Buffer[index] - prevRange, Digits())
    checkVisiblity(index)

def calculateWoodie():
    global PP, R1, R2, R3, R4, S1, S2, S3, S4
    prevRange = iHigh(Symbol(), InpTimeframe, PrevCandleIndex) - iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevHigh = iHigh(Symbol(), InpTimeframe, PrevCandleIndex)
    prevLow = iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevClose = iClose(Symbol(), InpTimeframe, PrevCandleIndex)
    todayOpen = iOpen(Symbol(), InpTimeframe, CurrentCandleIndex)
    PP = NormalizeDouble((prevHigh + prevLow + (todayOpen * 2)) / 4, Digits())
    R1 = NormalizeDouble((PP * 2) - prevLow, Digits())
    R2 = NormalizeDouble(PP + prevRange, Digits())
    R3 = NormalizeDouble(prevHigh + (2 * (PP - prevLow)), Digits())
    R4 = NormalizeDouble(R3 + prevRange, Digits())
    S1 = NormalizeDouble((PP * 2) - prevHigh, Digits())
    S2 = NormalizeDouble(PP - prevRange, Digits())
    S3 = NormalizeDouble(prevLow - (2 * (prevHigh - PP)), Digits())
    S4 = NormalizeDouble(S3 - prevRange, Digits())
    DrawOnChart()

def calculateClassic1():
    global PP, R1, R2, R3, R4, S1, S2, S3, S4
    prevRange = iHigh(Symbol(), InpTimeframe, PrevCandleIndex) - iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevHigh = iHigh(Symbol(), InpTimeframe, PrevCandleIndex)
    prevLow = iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevClose = iClose(Symbol(), InpTimeframe, PrevCandleIndex)
    PP = NormalizeDouble((prevHigh + prevLow + prevClose) / 3, Digits())
    R1 = NormalizeDouble((PP * 2) - prevLow, Digits())
    R2 = NormalizeDouble(PP + prevRange, Digits())
    R3 = NormalizeDouble(R2 + prevRange, Digits())
    R4 = NormalizeDouble(R3 + prevRange, Digits())
    S1 = NormalizeDouble((PP * 2) - prevHigh, Digits())
    S2 = NormalizeDouble(PP - prevRange, Digits())
    S3 = NormalizeDouble(S2 - prevRange, Digits())
    S4 = NormalizeDouble(S3 - prevRange, Digits())
    DrawOnChart()

def calculateClassic2():
    global PP, R1, R2, R3, R4, S1, S2, S3, S4
    prevRange = iHigh(Symbol(), InpTimeframe, PrevCandleIndex) - iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevHigh = iHigh(Symbol(), InpTimeframe, PrevCandleIndex)
    prevLow = iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevClose = iClose(Symbol(), InpTimeframe, PrevCandleIndex)
    prevOpen = iOpen(Symbol(), InpTimeframe, PrevCandleIndex)
    PP = NormalizeDouble((prevHigh + prevLow + prevClose + prevOpen) / 4, Digits())
    R1 = NormalizeDouble((PP * 2) - prevLow, Digits())
    R2 = NormalizeDouble(PP + prevRange, Digits())
    R3 = NormalizeDouble(PP + (prevRange * 2), Digits())
    R4 = NormalizeDouble(PP + (prevRange * 3), Digits())
    S1 = NormalizeDouble((PP * 2) - prevHigh, Digits())
    S2 = NormalizeDouble(PP - prevRange, Digits())
    S3 = NormalizeDouble(PP - (prevRange * 2), Digits())
    S4 = NormalizeDouble(PP - (prevRange * 3), Digits())
    DrawOnChart()

def calculateCamarilla():
    global PP, R1, R2, R3, R4, S1, S2, S3, S4
    camRange = iHigh(Symbol(), InpTimeframe, PrevCandleIndex) - iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevHigh = iHigh(Symbol(), InpTimeframe, PrevCandleIndex)
    prevLow = iLow(Symbol(), InpTimeframe, PrevCandleIndex)
    prevClose = iClose(Symbol(), InpTimeframe, PrevCandleIndex)
    R1 = NormalizeDouble(((1.1 / 12) * camRange) + prevClose, Digits())
    R2 = NormalizeDouble(((1.1 / 6) * camRange) + prevClose, Digits())
    R3 = NormalizeDouble(((1.1 / 4) * camRange) + prevClose, Digits())
    R4 = NormalizeDouble(((1.1 / 2) * camRange) + prevClose, Digits())
    S1 = NormalizeDouble(prevClose - ((1.1 / 12) * camRange), Digits())
    S2 = NormalizeDouble(prevClose - ((1.1 / 6) * camRange), Digits())
    S3 = NormalizeDouble(prevClose - ((1.1 / 4) * camRange), Digits())
    S4 = NormalizeDouble(prevClose - ((1.1 / 2) * camRange), Digits())
    PP = NormalizeDouble((R4 + S4) / 2, Digits())
    DrawOnChart()

def DrawOnChart():
    global StartTime, StopTime
    while (TimeDayOfWeek_u(StartTime) == SUNDAY or TimeDayOfWeek_u(StartTime) == SATURDAY) or ((not InpIncludeSundays) and TimeDayOfWeek_u(StartTime) == SUNDAY):
        StartTime = StartTime + (24 * 60 * 60)
    TimeStruct = MqlDateTime()
    TimeToStruct(StartTime, TimeStruct)
    if InpTimeframe == PERIOD_M1:
        StopTime = StartTime + (1 * 60)
        StopTime = StopTime - OneCandle
    if InpTimeframe == PERIOD_M5:
        StopTime = StartTime + (5 * 60)
        StopTime = StopTime - OneCandle
    if InpTimeframe == PERIOD_M15:
        StopTime = StartTime + (15 * 60)
        StopTime = StopTime - OneCandle
    if InpTimeframe == PERIOD_M30:
        StopTime = StartTime + (30 * 60)
        StopTime = StopTime - OneCandle
    if InpTimeframe == PERIOD_H1:
        StopTime = StartTime + (60 * 60)
        StopTime = StopTime - OneCandle
    if InpTimeframe == PERIOD_H4:
        StopTime = StartTime + (4 * 60 * 60)
        StopTime = StopTime - OneCandle
    if InpTimeframe == PERIOD_D1:
        StopTime = StartTime + (24 * 60 * 60)
        StopTime = StopTime - OneCandle
    if InpTimeframe == PERIOD_W1:
        StopTime = StartTime + (7 * 24 * 60 * 60)
        StopTime = StopTime - OneCandle
    if InpTimeframe == PERIOD_MN1:
        if TimeStruct.mon < 12:
            TimeStruct.mon += 1
        else:
            TimeStruct.mon = 1
            TimeStruct.year += 1
        StopTime = StructToTime(TimeStruct)
        StopTime = StopTime - OneCandle
    if InpShowR1 == True:
        DrawTrendLine(0, 'R1', InpR1Color, InpR1Style, InpR1Width, StartTime, StopTime, R1, R1, 'R1 (' + CalcTypeAbb + '): ' + DoubleToString(R1, Digits()))
        if InpShowMode == SHOW_MODE_TODAY:
            R1Buffer[2] = 0.0
            R1Buffer[1] = R1
    if InpShowR2 == True:
        DrawTrendLine(0, 'R2', InpR2Color, InpR2Style, InpR2Width, StartTime, StopTime, R2, R2, 'R2 (' + CalcTypeAbb + '): ' + DoubleToString(R2, Digits()))
        if InpShowMode == SHOW_MODE_TODAY:
            R2Buffer[2] = 0.0
            R2Buffer[1] = R2
    if InpShowR3 == True:
        DrawTrendLine(0, 'R3', InpR3Color, InpR3Style, InpR3Width, StartTime, StopTime, R3, R3, 'R3 (' + CalcTypeAbb + '): ' + DoubleToString(R3, Digits()))
        if InpShowMode == SHOW_MODE_TODAY:
            R3Buffer[2] = 0.0
            R3Buffer[1] = R3
    if InpShowR4 == True:
        DrawTrendLine(0, 'R4', InpR4Color, InpR4Style, InpR4Width, StartTime, StopTime, R4, R4, 'R4 (' + CalcTypeAbb + '): ' + DoubleToString(R4, Digits()))
        if InpShowMode == SHOW_MODE_TODAY:
            R4Buffer[2] = 0.0
            R4Buffer[1] = R4
    if InpShowS1 == True:
        DrawTrendLine(0, 'S1', InpS1Color, InpS1Style, InpS1Width, StartTime, StopTime, S1, S1, 'S1 (' + CalcTypeAbb + '): ' + DoubleToString(S1, Digits()))
        if InpShowMode == SHOW_MODE_TODAY:
            S1Buffer[2] = 0.0
            S1Buffer[1] = S1
    if InpShowS2 == True:
        DrawTrendLine(0, 'S2', InpS2Color, InpS2Style, InpS2Width, StartTime, StopTime, S2, S2, 'S2 (' + CalcTypeAbb + '): ' + DoubleToString(S2, Digits()))
        if InpShowMode == SHOW_MODE_TODAY:
            S2Buffer[2] = 0.0
            S2Buffer[1] = S2
    if InpShowS3 == True:
        DrawTrendLine(0, 'S3', InpS3Color, InpS3Style, InpS3Width, StartTime, StopTime, S3, S3, 'S3 (' + CalcTypeAbb + '): ' + DoubleToString(S3, Digits()))
        if InpShowMode == SHOW_MODE_TODAY:
            S3Buffer[2] = 0.0
            S3Buffer[1] = S3
    if InpShowS4 == True:
        DrawTrendLine(0, 'S4', InpS4Color, InpS4Style, InpS4Width, StartTime, StopTime, S4, S4, 'S4 (' + CalcTypeAbb + '): ' + DoubleToString(S4, Digits()))
        if InpShowMode == SHOW_MODE_TODAY:
            S4Buffer[2] = 0.0
            S4Buffer[1] = S4
    if InpShowPivot == True:
        DrawTrendLine(0, 'Pivot', InpPivotColor, InpPivotStyle, InpPivotWidth, StartTime, StopTime, PP, PP, 'P (' + CalcTypeAbb + '): ' + DoubleToString(PP, Digits()))
        if InpShowMode == SHOW_MODE_TODAY:
            PivotBuffer[2] = 0.0
            PivotBuffer[1] = PP
    if InpShowLabels:
        if InpShowR1:
            DrawLabel(0, 'LR1', 'R1', clrGray, R1, StartTime, 'R1 (' + CalcTypeAbb + ')')
        if InpShowR2:
            DrawLabel(0, 'LR2', 'R2', clrGray, R2, StartTime, 'R2 (' + CalcTypeAbb + ')')
        if InpShowR3:
            DrawLabel(0, 'LR3', 'R3', clrGray, R3, StartTime, 'R3 (' + CalcTypeAbb + ')')
        if InpShowR4:
            DrawLabel(0, 'LR4', 'R4', clrGray, R4, StartTime, 'R4 (' + CalcTypeAbb + ')')
        if InpShowS1:
            DrawLabel(0, 'LS1', 'S1', clrGray, S1, StartTime, 'S1 (' + CalcTypeAbb + ')')
        if InpShowS2:
            DrawLabel(0, 'LS2', 'S2', clrGray, S2, StartTime, 'S2 (' + CalcTypeAbb + ')')
        if InpShowS3:
            DrawLabel(0, 'LS3', 'S3', clrGray, S3, StartTime, 'S3 (' + CalcTypeAbb + ')')
        if InpShowS4:
            DrawLabel(0, 'LS4', 'S4', clrGray, S4, StartTime, 'S4 (' + CalcTypeAbb + ')')
        if InpShowPivot:
            DrawLabel(0, 'LPivot', 'P', clrGray, PP, StartTime, 'P (' + CalcTypeAbb + ')')
    if InpShowPriceTags:
        PriceTagTime = StopTime
        if InpShowR1:
            DrawPriceTag('R1', PriceTagTime, R1, InpR1Color, InpR1Style, InpR1Width)
        if InpShowR2:
            DrawPriceTag('R2', PriceTagTime, R2, InpR2Color, InpR2Style, InpR2Width)
        if InpShowR3:
            DrawPriceTag('R3', PriceTagTime, R3, InpR3Color, InpR3Style, InpR3Width)
        if InpShowR4:
            DrawPriceTag('R4', PriceTagTime, R4, InpR4Color, InpR4Style, InpR4Width)
        if InpShowS1:
            DrawPriceTag('S1', PriceTagTime, S1, InpS1Color, InpS1Style, InpS1Width)
        if InpShowS2:
            DrawPriceTag('S2', PriceTagTime, S2, InpS2Color, InpS2Style, InpS2Width)
        if InpShowS3:
            DrawPriceTag('S3', PriceTagTime, S3, InpS3Color, InpS3Style, InpS3Width)
        if InpShowS4:
            DrawPriceTag('S4', PriceTagTime, S4, InpS4Color, InpS4Style, InpS4Width)
        if InpShowPivot:
            DrawPriceTag('Pivot', PriceTagTime, PP, InpPivotColor, InpPivotStyle, InpPivotWidth)
    ChartRedraw()

def checkVisiblity(index):
    if InpShowR1 == False:
        R1Buffer[index] = 0.0
    if InpShowR2 == False:
        R2Buffer[index] = 0.0
    if InpShowR3 == False:
        R3Buffer[index] = 0.0
    if InpShowR4 == False:
        R4Buffer[index] = 0.0
    if InpShowS1 == False:
        S1Buffer[index] = 0.0
    if InpShowS2 == False:
        S2Buffer[index] = 0.0
    if InpShowS3 == False:
        S3Buffer[index] = 0.0
    if InpShowS4 == False:
        S4Buffer[index] = 0.0
    if InpShowPivot == False:
        PivotBuffer[index] = 0.0

def DrawTrendLine(chart_ID, name, trendColor, lineStyle, lineWidth, timeStart, timeEnd, StartPrice, StopPrice, tooltip=''):
    name = prefix + name
    if ObjectFind(0, name) < 0:
        ObjectCreate(chart_ID, name, OBJ_TREND, 0, timeStart, StartPrice, timeEnd, StopPrice)
    else:
        ObjectSetDouble(chart_ID, name, OBJPROP_PRICE, 0, StartPrice)
        ObjectSetDouble(chart_ID, name, OBJPROP_PRICE, 1, StopPrice)
        ObjectSetInteger(chart_ID, name, OBJPROP_TIME, 0, timeStart)
        ObjectSetInteger(chart_ID, name, OBJPROP_TIME, 1, timeEnd)
        return
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, trendColor)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, lineStyle)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, lineWidth)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, True)
    ObjectSetString(chart_ID, name, OBJPROP_TOOLTIP, tooltip)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, 0)

def DrawLabel(chart_ID, name, text, labelColor, price, time, tooltip=''):
    name = prefix + name
    if ObjectFind(0, name) < 0:
        ObjectCreate(chart_ID, name, OBJ_TEXT, 0, time, price)
    else:
        ObjectSetDouble(chart_ID, name, OBJPROP_PRICE, 0, price)
        ObjectSetInteger(chart_ID, name, OBJPROP_TIME, 0, time)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, 'Arial')
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, 10)
    ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, 0.0)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, labelColor)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, True)
    ObjectSetString(chart_ID, name, OBJPROP_TOOLTIP, tooltip)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, 0)

def ExtractCalculationType():
    global CalcTypeAbb
    _sw1 = CalculationMode
    if _sw1 == CALC_MODE_CLASSIC1:
        CalcTypeAbb = 'Classic1'
    elif _sw1 == CALC_MODE_CLASSIC2:
        CalcTypeAbb = 'Classic2'
    elif _sw1 == CALC_MODE_CAMARILLA:
        CalcTypeAbb = 'Cam'
    elif _sw1 == CALC_MODE_FIBONACCI:
        CalcTypeAbb = 'Fib'
    elif _sw1 == CALC_MODE_FIBONACCI_RETRACEMENT:
        CalcTypeAbb = 'FibR'
    elif _sw1 == CALC_MODE_FLOOR:
        CalcTypeAbb = 'Floor'
    elif _sw1 == CALC_MODE_WOODIE:
        CalcTypeAbb = 'Woodie'
    else:
        CalcTypeAbb = ''
    CalcTypeAbb += ' ' + FriendlyTimeframeName(InpTimeframe)

def FriendlyTimeframeName(_period):
    if _period == PERIOD_M1:
        return '1Minute'
    if _period == PERIOD_M5:
        return '5Minutes'
    if _period == PERIOD_M5:
        return '15Minutes'
    if _period == PERIOD_M30:
        return '30Minutes'
    if _period == PERIOD_H1:
        return '1Hour'
    if _period == PERIOD_H4:
        return '4Hour'
    if _period == PERIOD_D1:
        return 'Daily'
    if _period == PERIOD_W1:
        return 'Weekly'
    if _period == PERIOD_MN1:
        return 'Monthly'
    return ''

def DrawPriceTag(name, time, price, clr, style, width):
    name = prefix + 'PriceTag_' + name
    chart_ID = 0
    if not ObjectCreate(chart_ID, name, OBJ_ARROW_RIGHT_PRICE, 0, time, price):
        ObjectSetInteger(chart_ID, name, OBJPROP_TIME, time)
        ObjectSetDouble(chart_ID, name, OBJPROP_PRICE, price)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, 0)

def IsChartLoaded():
    global StartTime
    testArray = Arr(0, 0.0)
    if CopyClose(Symbol(), InpTimeframe, _DT(TimeCurrent()), 2, testArray) < 2:
        Print('Loading ', Symbol(), ' chart failed...')
        return False
    StartTime = iTime(Symbol(), InpTimeframe, 0)
    if StartTime == 0:
        Print('Loading ', Symbol(), ' chart failed...')
        return False
    if not PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0):
        return False
    if not PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0):
        return False
    if not PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0):
        return False
    if not PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0):
        return False
    if not PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0):
        return False
    if not PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0):
        return False
    if not PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0):
        return False
    if not PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0):
        return False
    if not PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, 0):
        return False
    Print(Symbol(), ' chart loaded successfully!')
    return True

def UpdateCandlesIndex():
    global CurrentCandleIndex, PrevCandleIndex
    if (InpTimeframe == PERIOD_W1 or InpTimeframe == PERIOD_MN1) or (InpTimeframe == PERIOD_CURRENT and (Period() == PERIOD_W1 or Period() == PERIOD_MN1)):
        CurrentCandleIndex = 0
        PrevCandleIndex = 1
        return
    i = 0
    CurrentCandleIndex = i
    while TimeDayOfWeek_u(iTime(Symbol(), InpTimeframe, i)) == SATURDAY or ((not InpIncludeSundays) and TimeDayOfWeek_u(iTime(Symbol(), InpTimeframe, i)) == SUNDAY):
        i += 1
        CurrentCandleIndex = i
    i = CurrentCandleIndex + 1
    PrevCandleIndex = i
    while TimeDayOfWeek_u(iTime(Symbol(), InpTimeframe, i)) == SATURDAY or ((not InpIncludeSundays) and TimeDayOfWeek_u(iTime(Symbol(), InpTimeframe, i)) == SUNDAY):
        i += 1
        PrevCandleIndex = i

def CorrectBarIndex(barIndex):
    if InpTimeframe == PERIOD_MN1:
        return
    i = barIndex.v
    while TimeDayOfWeek_u(iTime(Symbol(), InpTimeframe, i)) == SATURDAY or ((not InpIncludeSundays) and TimeDayOfWeek_u(iTime(Symbol(), InpTimeframe, i)) == SUNDAY):
        i += 1
        barIndex.v = i

def TimeDayOfWeek_u(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day_of_week

def GetTFName():
    Result = Arr(0, "")
    if StringSplit(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 95, Result) > 0:
        return Result[1]
    else:
        return ''

def SendAlert(_OP):
    message = Box('')
    StringConcatenate(message, Symbol(), '(', CalcTypeToString(), ' ', APPTFtoString(), ') - ', _OP, ' touched')
    if InpAlertShowPopup:
        Alert(message.v)
    if InpAlertSendEmail:
        if not SendMail('APP', message.v):
            Print('Send email failed with error #', GetLastError())
    if InpAlertPlaySound:
        PlaySound(InpAlertSoundFile)
    if InpAlertSendNotification:
        if not SendNotification(message.v):
            Print('Send notification failed with error #', GetLastError())

def RefreshAlerts():
    global LastTickClose, LastTouchedLine
    if not TerminalInfoInteger(TERMINAL_CONNECTED):
        return
    if LastTickClose == 0:
        LastTickClose = SymbolInfoDouble(Symbol(), SYMBOL_BID)
        return
    if InpShowR4:
        if (LastTickClose < R4 and iClose(Symbol(), Period(), 0) >= R4) or (LastTickClose > R4 and iClose(Symbol(), Period(), 0) <= R4):
            if LastTouchedLine != 'R4':
                if InpR4Alert:
                    SendAlert(StringFormat('R4 (%s)', DoubleToString(R4, Digits())))
                    LastTouchedLine = 'R4'
    if InpShowR3:
        if (LastTickClose < R3 and iClose(Symbol(), Period(), 0) >= R3) or (LastTickClose > R3 and iClose(Symbol(), Period(), 0) <= R3):
            if LastTouchedLine != 'R3':
                if InpR3Alert:
                    SendAlert(StringFormat('R3 (%s)', DoubleToString(R3, Digits())))
                    LastTouchedLine = 'R3'
    if InpShowR2:
        if (LastTickClose < R2 and iClose(Symbol(), Period(), 0) >= R2) or (LastTickClose > R2 and iClose(Symbol(), Period(), 0) <= R2):
            if LastTouchedLine != 'R2':
                if InpR2Alert:
                    SendAlert(StringFormat('R2 (%s)', DoubleToString(R2, Digits())))
                    LastTouchedLine = 'R2'
    if InpShowR1:
        if (LastTickClose < R1 and iClose(Symbol(), Period(), 0) >= R1) or (LastTickClose > R1 and iClose(Symbol(), Period(), 0) <= R1):
            if LastTouchedLine != 'R1':
                if InpR1Alert:
                    SendAlert(StringFormat('R1 (%s)', DoubleToString(R1, Digits())))
                    LastTouchedLine = 'R1'
    if InpShowPivot:
        if (LastTickClose < PP and iClose(Symbol(), Period(), 0) >= PP) or (LastTickClose > PP and iClose(Symbol(), Period(), 0) <= PP):
            if LastTouchedLine != 'PP':
                if InpPivotAlert:
                    SendAlert(StringFormat('PP (%s)', DoubleToString(PP, Digits())))
                    LastTouchedLine = 'PP'
    if InpShowS1:
        if (LastTickClose < S1 and iClose(Symbol(), Period(), 0) >= S1) or (LastTickClose > S1 and iClose(Symbol(), Period(), 0) <= S1):
            if LastTouchedLine != 'S1':
                if InpS1Alert:
                    SendAlert(StringFormat('S1 (%s)', DoubleToString(S1, Digits())))
                    LastTouchedLine = 'S1'
    if InpShowS2:
        if (LastTickClose < S2 and iClose(Symbol(), Period(), 0) >= S2) or (LastTickClose > S2 and iClose(Symbol(), Period(), 0) <= S2):
            if LastTouchedLine != 'S2':
                if InpS2Alert:
                    SendAlert(StringFormat('S2 (%s)', DoubleToString(S2, Digits())))
                    LastTouchedLine = 'S2'
    if InpShowS3:
        if (LastTickClose < S3 and iClose(Symbol(), Period(), 0) >= S3) or (LastTickClose > S3 and iClose(Symbol(), Period(), 0) <= S3):
            if LastTouchedLine != 'S3':
                if InpS3Alert:
                    SendAlert(StringFormat('S3 (%s)', DoubleToString(S3, Digits())))
                    LastTouchedLine = 'S3'
    if InpShowS4:
        if (LastTickClose < S4 and iClose(Symbol(), Period(), 0) >= S4) or (LastTickClose > S4 and iClose(Symbol(), Period(), 0) <= S4):
            if LastTouchedLine != 'S4':
                if InpS4Alert:
                    SendAlert(StringFormat('S4 (%s)', DoubleToString(S4, Digits())))
                    LastTouchedLine = 'S4'
    LastTickClose = SymbolInfoDouble(Symbol(), SYMBOL_BID)

def APPTFtoString():
    Result = Arr(0, "")
    if StringSplit(EnumToString(InpTimeframe, 'ENUM_TIMEFRAMES'), 95, Result) > 0:
        return Result[1]
    else:
        return ''

def CalcTypeToString():
    Result = ''
    _sw2 = CalculationMode
    if _sw2 == CALC_MODE_CLASSIC1:
        Result = 'Classic1'
    elif _sw2 == CALC_MODE_CLASSIC2:
        Result = 'Classic2'
    elif _sw2 == CALC_MODE_CAMARILLA:
        Result = 'Cam'
    elif _sw2 == CALC_MODE_FIBONACCI:
        Result = 'Fib'
    elif _sw2 == CALC_MODE_FIBONACCI_RETRACEMENT:
        Result = 'FibR'
    elif _sw2 == CALC_MODE_FLOOR:
        Result = 'Floor'
    elif _sw2 == CALC_MODE_WOODIE:
        Result = 'Woodie'
    else:
        Result = ''
    return Result


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AllPivotPoints(_MQL5Indicator):
    name = 'All Pivot Points'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Timeframe
        'CalculationMode': _Choice({0: 'Classic 1', 1: 'Classic 2', 2: 'Camarilla', 3: 'Woodie', 4: 'Fibonacci', 5: 'Floor', 6: 'Fibonacci Retracement'}, default=0),  # Calculation Mode
        'InpShowMode': _Choice({0: 'Today', 1: 'Historical'}, default=1),  # Displaying Mode
        'InpHistoricalBars': 0,  # Historical Bars (0=All)
        'InpShowLabels': True,  # Show Labels
        'InpShowPriceTags': True,  # Show Price Tags
        'InpIncludeSundays': True,  # Include Sundays
        'InpFibR1S1': 38.2,  # R1/S1
        'InpFibR2S2': 61.8,  # R2/S2
        'InpFibR3S3': 100.0,  # R3/S3
        'InpFibR4S4': 161.8,  # R4/S4
        'InpShowPivot': True,  # Pivot
        'InpShowS1': True,  # S1
        'InpShowS2': True,  # S2
        'InpShowS3': True,  # S3
        'InpShowS4': True,  # S4
        'InpShowR1': True,  # R1
        'InpShowR2': True,  # R2
        'InpShowR3': True,  # R3
        'InpShowR4': True,  # R4
        'InpPivotStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Pivot
        'InpS1Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # S1
        'InpS2Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # S2
        'InpS3Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # S3
        'InpS4Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # S4
        'InpR1Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # R1
        'InpR2Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # R2
        'InpR3Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # R3
        'InpR4Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # R4
        'InpPivotWidth': 1,  # Pivot
        'InpS1Width': 1,  # S1
        'InpS2Width': 1,  # S2
        'InpS3Width': 1,  # S3
        'InpS4Width': 1,  # S4
        'InpR1Width': 1,  # R1
        'InpR2Width': 1,  # R2
        'InpR3Width': 1,  # R3
        'InpR4Width': 1,  # R4
        'InpPivotAlert': True,  # Pivot
        'InpS1Alert': True,  # S1
        'InpS2Alert': True,  # S2
        'InpS3Alert': True,  # S3
        'InpS4Alert': True,  # S4
        'InpR1Alert': True,  # R1
        'InpR2Alert': True,  # R2
        'InpR3Alert': True,  # R3
        'InpR4Alert': True,  # R4
        'InpAlertShowPopup': True,  # Show Pop-up
        'InpAlertSendEmail': False,  # Send Email
        'InpAlertSendNotification': False,  # Send Notification
        'InpAlertPlaySound': False,  # Play Sound
    }

