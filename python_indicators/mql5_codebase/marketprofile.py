"""MarketProfile — converted from MQL5: MQL5 Indicators/Market Profile MT5/MarketProfile.mq5

Displays the Market Profile indicator for intraday, daily, weekly, or monthly trading sessions.
Daily - should be attached to M5-M30 timeframes. M30 is recommended.
Weekly - should be attached to M30-H4 timeframes. H1 is recommended.
Weeks start on Sunday.
Monthly - should be attached to H1-D1 timeframes. H4 is recommended.
Intraday - should be attached to M1-M15 timeframes. M5 is recommended.\\r\\n
Designed for major currency pairs, but should work also with exotic pairs, CFDs, or commodities.
Link: https://t.me/ForexEaPremium; Version: 1.23

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'https://t.me/ForexEaPremium', 'version': '1.23', 'window': 'chart', 'indicator_plots': 6, 'indicator_buffers': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [32768], 2: [32768], 3: [2139610], 4: [2139610], 5: [7504122], 6: [7504122]}, 'widths': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Developing POC', 2: 'Developing POC', 3: 'Developing VAH', 4: 'Developing VAH', 5: 'Developing VAL', 6: 'Developing VAL'}, 'levels': [], 'description': ['Displays the Market Profile indicator for intraday, daily, weekly, or monthly trading sessions.', 'Daily - should be attached to M5-M30 timeframes. M30 is recommended.', 'Weekly - should be attached to M30-H4 timeframes. H1 is recommended.', 'Weeks start on Sunday.', 'Monthly - should be attached to H1-D1 timeframes. H4 is recommended.', 'Intraday - should be attached to M1-M15 timeframes. M5 is recommended.\\r\\n', 'Designed for major currency pairs, but should work also with exotic pairs, CFDs, or commodities.'], 'name': 'MarketProfile', 'source': 'MQL5 Indicators/Market Profile MT5/MarketProfile.mq5', 'folder': 'Market Profile MT5', 'inputs': [{'mql': 'Session', 'py': 'Session', 'param': 'Session', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'StartFromDate', 'py': 'StartFromDate', 'param': None, 'type': 'datetime', 'default': 1700000000, 'label': 'StartFromDate: lower priority.', 'sinput': False}, {'mql': 'StartFromCurrentSession', 'py': 'StartFromCurrentSession', 'param': 'StartFromCurrentSession', 'type': 'bool', 'default': True, 'label': 'StartFromCurrentSession: higher priority.', 'sinput': False}, {'mql': 'SessionsToCount', 'py': 'SessionsToCount', 'param': 'SessionsToCount', 'type': 'int', 'default': 2, 'label': 'SessionsToCount: Number of sessions to count Market Profile.', 'sinput': False}, {'mql': 'SeamlessScrollingMode', 'py': 'SeamlessScrollingMode', 'param': 'SeamlessScrollingMode', 'type': 'bool', 'default': False, 'label': 'SeamlessScrollingMode: Show sessions on current screen.', 'sinput': False}, {'mql': 'EnableDevelopingPOC', 'py': 'EnableDevelopingPOC', 'param': 'EnableDevelopingPOC', 'type': 'bool', 'default': False, 'label': 'Enable Developing POC', 'sinput': False}, {'mql': 'EnableDevelopingVAHVAL', 'py': 'EnableDevelopingVAHVAL', 'param': 'EnableDevelopingVAHVAL', 'type': 'bool', 'default': False, 'label': 'Enable Developing VAH/VAL', 'sinput': False}, {'mql': 'ValueAreaPercentage', 'py': 'ValueAreaPercentage', 'param': 'ValueAreaPercentage', 'type': 'int', 'default': 70, 'label': "ValueAreaPercentage: Percentage of TPO's inside Value Area.", 'sinput': False}, {'mql': 'ColorScheme', 'py': 'ColorScheme', 'param': 'ColorScheme', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SingleColor', 'py': 'SingleColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'SingleColor: if ColorScheme is set to Single Color.', 'sinput': False}, {'mql': 'ColorBullBear', 'py': 'ColorBullBear', 'param': 'ColorBullBear', 'type': 'bool', 'default': False, 'label': "ColorBullBear: If true, colors are from bars' direction.", 'sinput': False}, {'mql': 'MedianColor', 'py': 'MedianColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': '', 'sinput': False}, {'mql': 'ValueAreaSidesColor', 'py': 'ValueAreaSidesColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': '', 'sinput': False}, {'mql': 'ValueAreaHighLowColor', 'py': 'ValueAreaHighLowColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': '', 'sinput': False}, {'mql': 'MedianStyle', 'py': 'MedianStyle', 'param': 'MedianStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MedianRayStyle', 'py': 'MedianRayStyle', 'param': 'MedianRayStyle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ValueAreaSidesStyle', 'py': 'ValueAreaSidesStyle', 'param': 'ValueAreaSidesStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ValueAreaHighLowStyle', 'py': 'ValueAreaHighLowStyle', 'param': 'ValueAreaHighLowStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ValueAreaRayHighLowStyle', 'py': 'ValueAreaRayHighLowStyle', 'param': 'ValueAreaRayHighLowStyle', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'MedianWidth', 'py': 'MedianWidth', 'param': 'MedianWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MedianRayWidth', 'py': 'MedianRayWidth', 'param': 'MedianRayWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ValueAreaSidesWidth', 'py': 'ValueAreaSidesWidth', 'param': 'ValueAreaSidesWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ValueAreaHighLowWidth', 'py': 'ValueAreaHighLowWidth', 'param': 'ValueAreaHighLowWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ValueAreaRayHighLowWidth', 'py': 'ValueAreaRayHighLowWidth', 'param': 'ValueAreaRayHighLowWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ShowValueAreaRays', 'py': 'ShowValueAreaRays', 'param': 'ShowValueAreaRays', 'type': 'int', 'default': 0, 'label': 'ShowValueAreaRays: draw previous value area high/low rays.', 'sinput': False}, {'mql': 'ShowMedianRays', 'py': 'ShowMedianRays', 'param': 'ShowMedianRays', 'type': 'int', 'default': 0, 'label': 'ShowMedianRays: draw previous median rays.', 'sinput': False}, {'mql': 'RaysUntilIntersection', 'py': 'RaysUntilIntersection', 'param': 'RaysUntilIntersection', 'type': 'int', 'default': 0, 'label': 'RaysUntilIntersection: which rays stop when hit another MP.', 'sinput': False}, {'mql': 'HideRaysFromInvisibleSessions', 'py': 'HideRaysFromInvisibleSessions', 'param': 'HideRaysFromInvisibleSessions', 'type': 'bool', 'default': False, 'label': 'HideRaysFromInvisibleSessions: hide rays from behind the screen.', 'sinput': False}, {'mql': 'TimeShiftMinutes', 'py': 'TimeShiftMinutes', 'param': 'TimeShiftMinutes', 'type': 'int', 'default': 0, 'label': 'TimeShiftMinutes: shift session + to the left, - to the right.', 'sinput': False}, {'mql': 'ShowKeyValues', 'py': 'ShowKeyValues', 'param': 'ShowKeyValues', 'type': 'bool', 'default': True, 'label': 'ShowKeyValues: print out VAH, VAL, POC on chart.', 'sinput': False}, {'mql': 'KeyValuesColor', 'py': 'KeyValuesColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'KeyValuesColor: color for VAH, VAL, POC printout.', 'sinput': False}, {'mql': 'KeyValuesSize', 'py': 'KeyValuesSize', 'param': 'KeyValuesSize', 'type': 'int', 'default': 8, 'label': 'KeyValuesSize: font size for VAH, VAL, POC printout.', 'sinput': False}, {'mql': 'ShowSinglePrint', 'py': 'ShowSinglePrint', 'param': 'ShowSinglePrint', 'type': 'int', 'default': 0, 'label': 'ShowSinglePrint: mark Single Print profile levels.', 'sinput': False}, {'mql': 'SinglePrintRays', 'py': 'SinglePrintRays', 'param': 'SinglePrintRays', 'type': 'bool', 'default': False, 'label': 'SinglePrintRays: mark Single Print edges with rays.', 'sinput': False}, {'mql': 'SinglePrintColor', 'py': 'SinglePrintColor', 'param': None, 'type': 'color', 'default': 55295, 'label': '', 'sinput': False}, {'mql': 'SinglePrintRayStyle', 'py': 'SinglePrintRayStyle', 'param': 'SinglePrintRayStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SinglePrintRayWidth', 'py': 'SinglePrintRayWidth', 'param': 'SinglePrintRayWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ProminentMedianColor', 'py': 'ProminentMedianColor', 'param': None, 'type': 'color', 'default': 65535, 'label': '', 'sinput': False}, {'mql': 'ProminentMedianStyle', 'py': 'ProminentMedianStyle', 'param': 'ProminentMedianStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ProminentMedianWidth', 'py': 'ProminentMedianWidth', 'param': 'ProminentMedianWidth', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'RightToLeft', 'py': 'RightToLeft', 'param': 'RightToLeft', 'type': 'bool', 'default': False, 'label': 'RightToLeft: Draw histogram from right to left.', 'sinput': False}, {'mql': 'PointMultiplier', 'py': 'PointMultiplier', 'param': 'PointMultiplier', 'type': 'int', 'default': 0, 'label': 'PointMultiplier: higher value = fewer objects. 0 - adaptive.', 'sinput': False}, {'mql': 'ThrottleRedraw', 'py': 'ThrottleRedraw', 'param': 'ThrottleRedraw', 'type': 'int', 'default': 0, 'label': 'ThrottleRedraw: delay (in seconds) for updating Market Profile.', 'sinput': False}, {'mql': 'DisableHistogram', 'py': 'DisableHistogram', 'param': 'DisableHistogram', 'type': 'bool', 'default': False, 'label': 'DisableHistogram: do not draw profile, VAH, VAL, and POC still visible.', 'sinput': False}, {'mql': 'AlertNative', 'py': 'AlertNative', 'param': 'AlertNative', 'type': 'bool', 'default': False, 'label': 'AlertNative: issue native pop-up alerts.', 'sinput': False}, {'mql': 'AlertEmail', 'py': 'AlertEmail', 'param': 'AlertEmail', 'type': 'bool', 'default': False, 'label': 'AlertEmail: issue email alerts.', 'sinput': False}, {'mql': 'AlertPush', 'py': 'AlertPush', 'param': 'AlertPush', 'type': 'bool', 'default': False, 'label': 'AlertPush: issue push-notification alerts.', 'sinput': False}, {'mql': 'AlertArrows', 'py': 'AlertArrows', 'param': 'AlertArrows', 'type': 'bool', 'default': False, 'label': 'AlertArrows: draw chart arrows on alerts.', 'sinput': False}, {'mql': 'AlertCheckBar', 'py': 'AlertCheckBar', 'param': 'AlertCheckBar', 'type': 'int', 'default': 1, 'label': 'AlertCheckBar: which bar to check for alerts?', 'sinput': False}, {'mql': 'AlertForValueArea', 'py': 'AlertForValueArea', 'param': 'AlertForValueArea', 'type': 'bool', 'default': False, 'label': 'AlertForValueArea: alerts for Value Area (VAH, VAL) rays.', 'sinput': False}, {'mql': 'AlertForMedian', 'py': 'AlertForMedian', 'param': 'AlertForMedian', 'type': 'bool', 'default': False, 'label': "AlertForMedian: alerts for POC (Median) rays' crossing.", 'sinput': False}, {'mql': 'AlertForSinglePrint', 'py': 'AlertForSinglePrint', 'param': 'AlertForSinglePrint', 'type': 'bool', 'default': False, 'label': "AlertForSinglePrint: alerts for single print rays' crossing.", 'sinput': False}, {'mql': 'AlertOnPriceBreak', 'py': 'AlertOnPriceBreak', 'param': 'AlertOnPriceBreak', 'type': 'bool', 'default': False, 'label': 'AlertOnPriceBreak: price breaking above/below the ray.', 'sinput': False}, {'mql': 'AlertOnCandleClose', 'py': 'AlertOnCandleClose', 'param': 'AlertOnCandleClose', 'type': 'bool', 'default': False, 'label': 'AlertOnCandleClose: candle closing above/below the ray.', 'sinput': False}, {'mql': 'AlertOnGapCross', 'py': 'AlertOnGapCross', 'param': 'AlertOnGapCross', 'type': 'bool', 'default': False, 'label': 'AlertOnGapCross: bar gap above/below the ray.', 'sinput': False}, {'mql': 'AlertArrowCodePB', 'py': 'AlertArrowCodePB', 'param': 'AlertArrowCodePB', 'type': 'int', 'default': 108, 'label': 'AlertArrowCodePB: arrow code for price break alerts.', 'sinput': False}, {'mql': 'AlertArrowCodeCC', 'py': 'AlertArrowCodeCC', 'param': 'AlertArrowCodeCC', 'type': 'int', 'default': 110, 'label': 'AlertArrowCodeCC: arrow code for candle close alerts.', 'sinput': False}, {'mql': 'AlertArrowCodeGC', 'py': 'AlertArrowCodeGC', 'param': 'AlertArrowCodeGC', 'type': 'int', 'default': 117, 'label': 'AlertArrowCodeGC: arrow code for gap crossover alerts.', 'sinput': False}, {'mql': 'AlertArrowColorPB', 'py': 'AlertArrowColorPB', 'param': None, 'type': 'color', 'default': 255, 'label': 'AlertArrowColorPB: arrow color for price break alerts.', 'sinput': False}, {'mql': 'AlertArrowColorCC', 'py': 'AlertArrowColorCC', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'AlertArrowColorCC: arrow color for candle close alerts.', 'sinput': False}, {'mql': 'AlertArrowColorGC', 'py': 'AlertArrowColorGC', 'param': None, 'type': 'color', 'default': 65535, 'label': 'AlertArrowColorGC: arrow color for gap crossover alerts.', 'sinput': False}, {'mql': 'AlertArrowWidthPB', 'py': 'AlertArrowWidthPB', 'param': 'AlertArrowWidthPB', 'type': 'int', 'default': 1, 'label': 'AlertArrowWidthPB: arrow width for price break alerts.', 'sinput': False}, {'mql': 'AlertArrowWidthCC', 'py': 'AlertArrowWidthCC', 'param': 'AlertArrowWidthCC', 'type': 'int', 'default': 1, 'label': 'AlertArrowWidthCC: arrow width for candle close alerts.', 'sinput': False}, {'mql': 'AlertArrowWidthGC', 'py': 'AlertArrowWidthGC', 'param': 'AlertArrowWidthGC', 'type': 'int', 'default': 1, 'label': 'AlertArrowWidthGC: arrow width for gap crossover alerts.', 'sinput': False}, {'mql': 'EnableIntradaySession1', 'py': 'EnableIntradaySession1', 'param': 'EnableIntradaySession1', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'IntradaySession1StartTime', 'py': 'IntradaySession1StartTime', 'param': None, 'type': 'string', 'default': '00:00', 'label': '', 'sinput': False}, {'mql': 'IntradaySession1EndTime', 'py': 'IntradaySession1EndTime', 'param': None, 'type': 'string', 'default': '06:00', 'label': '', 'sinput': False}, {'mql': 'IntradaySession1ColorScheme', 'py': 'IntradaySession1ColorScheme', 'param': 'IntradaySession1ColorScheme', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'EnableIntradaySession2', 'py': 'EnableIntradaySession2', 'param': 'EnableIntradaySession2', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'IntradaySession2StartTime', 'py': 'IntradaySession2StartTime', 'param': None, 'type': 'string', 'default': '06:00', 'label': '', 'sinput': False}, {'mql': 'IntradaySession2EndTime', 'py': 'IntradaySession2EndTime', 'param': None, 'type': 'string', 'default': '12:00', 'label': '', 'sinput': False}, {'mql': 'IntradaySession2ColorScheme', 'py': 'IntradaySession2ColorScheme', 'param': 'IntradaySession2ColorScheme', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'EnableIntradaySession3', 'py': 'EnableIntradaySession3', 'param': 'EnableIntradaySession3', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'IntradaySession3StartTime', 'py': 'IntradaySession3StartTime', 'param': None, 'type': 'string', 'default': '12:00', 'label': '', 'sinput': False}, {'mql': 'IntradaySession3EndTime', 'py': 'IntradaySession3EndTime', 'param': None, 'type': 'string', 'default': '18:00', 'label': '', 'sinput': False}, {'mql': 'IntradaySession3ColorScheme', 'py': 'IntradaySession3ColorScheme', 'param': 'IntradaySession3ColorScheme', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'EnableIntradaySession4', 'py': 'EnableIntradaySession4', 'param': 'EnableIntradaySession4', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'IntradaySession4StartTime', 'py': 'IntradaySession4StartTime', 'param': None, 'type': 'string', 'default': '18:00', 'label': '', 'sinput': False}, {'mql': 'IntradaySession4EndTime', 'py': 'IntradaySession4EndTime', 'param': None, 'type': 'string', 'default': '00:00', 'label': '', 'sinput': False}, {'mql': 'IntradaySession4ColorScheme', 'py': 'IntradaySession4ColorScheme', 'param': 'IntradaySession4ColorScheme', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'SaturdaySunday', 'py': 'SaturdaySunday', 'param': 'SaturdaySunday', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'DisableAlertsOnWrongTimeframes', 'py': 'DisableAlertsOnWrongTimeframes', 'param': 'DisableAlertsOnWrongTimeframes', 'type': 'bool', 'default': False, 'label': 'Disable alerts on wrong timeframes.', 'sinput': False}, {'mql': 'ProminentMedianPercentage', 'py': 'ProminentMedianPercentage', 'param': 'ProminentMedianPercentage', 'type': 'int', 'default': 101, 'label': 'Percentage of Median TPOs out of total for a Prominent one.', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum color_scheme
Blue_to_Red = 0
Red_to_Green = 1
Green_to_Blue = 2
Yellow_to_Cyan = 3
Magenta_to_Yellow = 4
Cyan_to_Magenta = 5
Single_Color = 6
_enum('color_scheme', {0: 'Blue_to_Red', 1: 'Red_to_Green', 2: 'Green_to_Blue', 3: 'Yellow_to_Cyan', 4: 'Magenta_to_Yellow', 5: 'Cyan_to_Magenta', 6: 'Single_Color'})

# enum session_period
Daily = 0
Weekly = 1
Monthly = 2
Intraday = 3
Rectangle = 4
_enum('session_period', {0: 'Daily', 1: 'Weekly', 2: 'Monthly', 3: 'Intraday', 4: 'Rectangle'})

# enum sat_sun_solution
Saturday_Sunday_Normal_Days = 0
Ignore_Saturday_Sunday = 1
Append_Saturday_Sunday = 2
_enum('sat_sun_solution', {0: 'Saturday_Sunday_Normal_Days', 1: 'Ignore_Saturday_Sunday', 2: 'Append_Saturday_Sunday'})

# enum sessions_to_draw_rays
None_ = 0
Previous = 1
Current = 2
PreviousCurrent = 3
AllPrevious = 4
All = 5
_enum('sessions_to_draw_rays', {0: 'None', 1: 'Previous', 2: 'Current', 3: 'PreviousCurrent', 4: 'AllPrevious', 5: 'All'})

# enum ways_to_stop_rays
Stop_No_Rays = 0
Stop_All_Rays = 1
Stop_All_Rays_Except_Prev_Session = 2
Stop_Only_Previous_Session = 3
_enum('ways_to_stop_rays', {0: 'Stop_No_Rays', 1: 'Stop_All_Rays', 2: 'Stop_All_Rays_Except_Prev_Session', 3: 'Stop_Only_Previous_Session'})

# enum bar_direction
Bullish = 0
Bearish = 1
Neutral = 2
_enum('bar_direction', {0: 'Bullish', 1: 'Bearish', 2: 'Neutral'})

# enum single_print_type
No = 0
Leftside = 1
Rightside = 2
_enum('single_print_type', {0: 'No', 1: 'Leftside', 2: 'Rightside'})

# enum alert_check_bar
CheckCurrentBar = 0
CheckPreviousBar = 1
_enum('alert_check_bar', {0: 'CheckCurrentBar', 1: 'CheckPreviousBar'})

# enum alert_types
PriceBreak = 0
CandleCloseCrossover = 1
GapCrossover = 2
_enum('alert_types', {0: 'PriceBreak', 1: 'CandleCloseCrossover', 2: 'GapCrossover'})

# ---- inputs and global variables
Session = _input('Session', Daily)
StartFromDate = _input('StartFromDate', 1700000000)  # StartFromDate: lower priority.
StartFromCurrentSession = _input('StartFromCurrentSession', True)  # StartFromCurrentSession: higher priority.
SessionsToCount = _input('SessionsToCount', 2)  # SessionsToCount: Number of sessions to count Market Profile.
SeamlessScrollingMode = _input('SeamlessScrollingMode', False)  # SeamlessScrollingMode: Show sessions on current screen.
EnableDevelopingPOC = _input('EnableDevelopingPOC', False)  # Enable Developing POC
EnableDevelopingVAHVAL = _input('EnableDevelopingVAHVAL', False)  # Enable Developing VAH/VAL
ValueAreaPercentage = _input('ValueAreaPercentage', 70)  # ValueAreaPercentage: Percentage of TPO's inside Value Area.
ColorScheme = _input('ColorScheme', Blue_to_Red)
SingleColor = _input('SingleColor', clrBlue)  # SingleColor: if ColorScheme is set to Single Color.
ColorBullBear = _input('ColorBullBear', False)  # ColorBullBear: If true, colors are from bars' direction.
MedianColor = _input('MedianColor', clrWhite)
ValueAreaSidesColor = _input('ValueAreaSidesColor', clrWhite)
ValueAreaHighLowColor = _input('ValueAreaHighLowColor', clrWhite)
MedianStyle = _input('MedianStyle', STYLE_SOLID)
MedianRayStyle = _input('MedianRayStyle', STYLE_DASH)
ValueAreaSidesStyle = _input('ValueAreaSidesStyle', STYLE_SOLID)
ValueAreaHighLowStyle = _input('ValueAreaHighLowStyle', STYLE_SOLID)
ValueAreaRayHighLowStyle = _input('ValueAreaRayHighLowStyle', STYLE_DOT)
MedianWidth = _input('MedianWidth', 1)
MedianRayWidth = _input('MedianRayWidth', 1)
ValueAreaSidesWidth = _input('ValueAreaSidesWidth', 1)
ValueAreaHighLowWidth = _input('ValueAreaHighLowWidth', 1)
ValueAreaRayHighLowWidth = _input('ValueAreaRayHighLowWidth', 1)
ShowValueAreaRays = _input('ShowValueAreaRays', None_)  # ShowValueAreaRays: draw previous value area high/low rays.
ShowMedianRays = _input('ShowMedianRays', None_)  # ShowMedianRays: draw previous median rays.
RaysUntilIntersection = _input('RaysUntilIntersection', Stop_No_Rays)  # RaysUntilIntersection: which rays stop when hit another MP.
HideRaysFromInvisibleSessions = _input('HideRaysFromInvisibleSessions', False)  # HideRaysFromInvisibleSessions: hide rays from behind the screen.
TimeShiftMinutes = _input('TimeShiftMinutes', 0)  # TimeShiftMinutes: shift session + to the left, - to the right.
ShowKeyValues = _input('ShowKeyValues', True)  # ShowKeyValues: print out VAH, VAL, POC on chart.
KeyValuesColor = _input('KeyValuesColor', clrWhite)  # KeyValuesColor: color for VAH, VAL, POC printout.
KeyValuesSize = _input('KeyValuesSize', 8)  # KeyValuesSize: font size for VAH, VAL, POC printout.
ShowSinglePrint = _input('ShowSinglePrint', No)  # ShowSinglePrint: mark Single Print profile levels.
SinglePrintRays = _input('SinglePrintRays', False)  # SinglePrintRays: mark Single Print edges with rays.
SinglePrintColor = _input('SinglePrintColor', clrGold)
SinglePrintRayStyle = _input('SinglePrintRayStyle', STYLE_SOLID)
SinglePrintRayWidth = _input('SinglePrintRayWidth', 1)
ProminentMedianColor = _input('ProminentMedianColor', clrYellow)
ProminentMedianStyle = _input('ProminentMedianStyle', STYLE_SOLID)
ProminentMedianWidth = _input('ProminentMedianWidth', 4)
RightToLeft = _input('RightToLeft', False)  # RightToLeft: Draw histogram from right to left.
PointMultiplier = _input('PointMultiplier', 0)  # PointMultiplier: higher value = fewer objects. 0 - adaptive.
ThrottleRedraw = _input('ThrottleRedraw', 0)  # ThrottleRedraw: delay (in seconds) for updating Market Profile.
DisableHistogram = _input('DisableHistogram', False)  # DisableHistogram: do not draw profile, VAH, VAL, and POC still visible.
AlertNative = _input('AlertNative', False)  # AlertNative: issue native pop-up alerts.
AlertEmail = _input('AlertEmail', False)  # AlertEmail: issue email alerts.
AlertPush = _input('AlertPush', False)  # AlertPush: issue push-notification alerts.
AlertArrows = _input('AlertArrows', False)  # AlertArrows: draw chart arrows on alerts.
AlertCheckBar = _input('AlertCheckBar', CheckPreviousBar)  # AlertCheckBar: which bar to check for alerts?
AlertForValueArea = _input('AlertForValueArea', False)  # AlertForValueArea: alerts for Value Area (VAH, VAL) rays.
AlertForMedian = _input('AlertForMedian', False)  # AlertForMedian: alerts for POC (Median) rays' crossing.
AlertForSinglePrint = _input('AlertForSinglePrint', False)  # AlertForSinglePrint: alerts for single print rays' crossing.
AlertOnPriceBreak = _input('AlertOnPriceBreak', False)  # AlertOnPriceBreak: price breaking above/below the ray.
AlertOnCandleClose = _input('AlertOnCandleClose', False)  # AlertOnCandleClose: candle closing above/below the ray.
AlertOnGapCross = _input('AlertOnGapCross', False)  # AlertOnGapCross: bar gap above/below the ray.
AlertArrowCodePB = _input('AlertArrowCodePB', 108)  # AlertArrowCodePB: arrow code for price break alerts.
AlertArrowCodeCC = _input('AlertArrowCodeCC', 110)  # AlertArrowCodeCC: arrow code for candle close alerts.
AlertArrowCodeGC = _input('AlertArrowCodeGC', 117)  # AlertArrowCodeGC: arrow code for gap crossover alerts.
AlertArrowColorPB = _input('AlertArrowColorPB', clrRed)  # AlertArrowColorPB: arrow color for price break alerts.
AlertArrowColorCC = _input('AlertArrowColorCC', clrBlue)  # AlertArrowColorCC: arrow color for candle close alerts.
AlertArrowColorGC = _input('AlertArrowColorGC', clrYellow)  # AlertArrowColorGC: arrow color for gap crossover alerts.
AlertArrowWidthPB = _input('AlertArrowWidthPB', 1)  # AlertArrowWidthPB: arrow width for price break alerts.
AlertArrowWidthCC = _input('AlertArrowWidthCC', 1)  # AlertArrowWidthCC: arrow width for candle close alerts.
AlertArrowWidthGC = _input('AlertArrowWidthGC', 1)  # AlertArrowWidthGC: arrow width for gap crossover alerts.
EnableIntradaySession1 = _input('EnableIntradaySession1', True)
IntradaySession1StartTime = _input('IntradaySession1StartTime', '00:00')
IntradaySession1EndTime = _input('IntradaySession1EndTime', '06:00')
IntradaySession1ColorScheme = _input('IntradaySession1ColorScheme', Blue_to_Red)
EnableIntradaySession2 = _input('EnableIntradaySession2', True)
IntradaySession2StartTime = _input('IntradaySession2StartTime', '06:00')
IntradaySession2EndTime = _input('IntradaySession2EndTime', '12:00')
IntradaySession2ColorScheme = _input('IntradaySession2ColorScheme', Red_to_Green)
EnableIntradaySession3 = _input('EnableIntradaySession3', True)
IntradaySession3StartTime = _input('IntradaySession3StartTime', '12:00')
IntradaySession3EndTime = _input('IntradaySession3EndTime', '18:00')
IntradaySession3ColorScheme = _input('IntradaySession3ColorScheme', Green_to_Blue)
EnableIntradaySession4 = _input('EnableIntradaySession4', True)
IntradaySession4StartTime = _input('IntradaySession4StartTime', '18:00')
IntradaySession4EndTime = _input('IntradaySession4EndTime', '00:00')
IntradaySession4ColorScheme = _input('IntradaySession4ColorScheme', Yellow_to_Cyan)
SaturdaySunday = _input('SaturdaySunday', Saturday_Sunday_Normal_Days)
DisableAlertsOnWrongTimeframes = _input('DisableAlertsOnWrongTimeframes', False)  # Disable alerts on wrong timeframes.
ProminentMedianPercentage = _input('ProminentMedianPercentage', 101)  # Percentage of Median TPOs out of total for a Prominent one.
PointMultiplier_calculated = 0  # Will have to be calculated based number digits in a quote if PointMultiplier input is 0.
DigitsM = 0  # Number of digits normalized based on PointMultiplier_calculated.
InitFailed = False  # Used for soft INIT_FAILED. Hard INIT_FAILED resets input parameters.
StartDate = 0  # Will hold either StartFromDate or Time[0].
onetick = 0.0  # One normalized pip.
FirstRunDone = False  # If true - OnCalculate() was already executed once.
Suffix = '_'  # Will store object name suffix depending on timeframe.
CurrentColorScheme = 0  # Required due to intraday sessions.
Max_number_of_bars_in_a_session = 1
Timer = 0  # For throttling updates of market profiles in slow systems.
NeedToRestartDrawing = False  # Global flag for RightToLeft redrawing;
CleanedUpOn = 0  # To prevent cleaning up the buffers again and again when the platform just starts.
ValueAreaPercentage_double = 0.7  # Will be calculated based on the input parameter in OnInit().
CurrentBarDirection = Neutral
PreviousBarDirection = Neutral
NeedToReviewColors = False
IDStartHours = Arr(4, 0, dyn=False)
IDStartMinutes = Arr(4, 0, dyn=False)
IDStartTime = Arr(4, 0, dyn=False)  # Stores IDStartHours x 60 + IDStartMinutes for comparison purposes.
IDEndHours = Arr(4, 0, dyn=False)
IDEndMinutes = Arr(4, 0, dyn=False)
IDEndTime = Arr(4, 0, dyn=False)  # Stores IDEndHours x 60 + IDEndMinutes for comparison purposes.
IDColorScheme = Arr(4, 0, dyn=False)
IntradaySessionCount = 0
_SessionsToCount = 0
IntradayCrossSessionDefined = -1  # For special case used only with Ignore_Saturday_Sunday on Monday.
LastAlertTime_CandleCross = 0  # For CheckCurrentBar alerts.
LastAlertTime_GapCross = 0  # For CheckCurrentBar alerts.
LastAlertTime = 0  # For CheckPreviousBar alerts;
Close_prev = EMPTY_VALUE  # Previous price value for Price Break alerts.
ArrowsCounter = 0  # Counter for naming of alert arrows.
RememberSessionMax = Arr(0, 0.0)
RememberSessionMin = Arr(0, 0.0)
RememberSessionStart = Arr(0, 0)
RememberSessionEnd = Arr(0, 0)  # Used only for Arrows.
RememberSessionSuffix = Arr(0, "")
SessionsNumber = 0  # Different from _SessionsToCount when working with Intraday sessions and for RaysUntilIntersection != Stop_No_Rays.
MPR_Array = Arr(0, None)
mpr_total = 0
LastRecalculationTime = 0
DevelopingPOC_1 = Arr(0, 0.0)  # Indicator buffers for Developing POC and VAH/VAL.
DevelopingPOC_2 = Arr(0, 0.0)  # Indicator buffers for Developing POC and VAH/VAL.
DevelopingVAH_1 = Arr(0, 0.0)  # Indicator buffers for Developing POC and VAH/VAL.
DevelopingVAH_2 = Arr(0, 0.0)  # Indicator buffers for Developing POC and VAH/VAL.
DevelopingVAL_1 = Arr(0, 0.0)  # Indicator buffers for Developing POC and VAH/VAL.
DevelopingVAL_2 = Arr(0, 0.0)  # Indicator buffers for Developing POC and VAH/VAL.

class CRectangleMP(MqlObject):
    _q_fields = ('prev_Time0', 'prev_High', 'prev_Low', 'prev_RectanglePriceMax', 'prev_RectanglePriceMin', 'Number', 'RectanglePriceMax', 'RectanglePriceMin', 'RectangleTimeMax', 'RectangleTimeMin', 't1', 't2', 'name')
    def __init__(self, given_name='MPR'):
        self.prev_Time0 = 0
        self.prev_High = 0.0
        self.prev_Low = 0.0
        self.prev_RectanglePriceMax = 0.0
        self.prev_RectanglePriceMin = 0.0
        self.Number = 0
        self.RectanglePriceMax = 0.0
        self.RectanglePriceMin = 0.0
        self.RectangleTimeMax = 0
        self.RectangleTimeMin = 0
        self.t1 = 0
        self.t2 = 0
        self.name = ""
        self.name = given_name
        self.RectanglePriceMax = -DBL_MAX
        self.RectanglePriceMin = DBL_MAX
        self.prev_RectanglePriceMax = -DBL_MAX
        self.prev_RectanglePriceMin = DBL_MAX
        self.RectangleTimeMax = 0
        self.RectangleTimeMin = 32535129600
        self.prev_Time0 = 0
        self.prev_High = -DBL_MAX
        self.prev_Low = DBL_MAX
        self.Number = -1
        self.t1 = 0
        self.t2 = 0
    def _q_dtor(self):
        pass
    def Process(self, i, High, Low, Time, rates_total):
        global Max_number_of_bars_in_a_session
        p1 = ObjectGetDouble(0, self.name, OBJPROP_PRICE, 0)
        p2 = ObjectGetDouble(0, self.name, OBJPROP_PRICE, 1)
        if self.Number == -1:
            self.Number = i
        sessionstart = iBarShift(Symbol(), Period(), _int(MathMin(self.t1, self.t2)), True)
        sessionend = iBarShift(Symbol(), Period(), _int(MathMax(self.t1, self.t2)), True)
        if MathMin(self.t1, self.t2) <= Time[0]:
            if sessionend == -1 and sessionstart == -1:
                return
        rectangle_changed = False
        rectangle_time_changed = False
        rectangle_price_changed = False
        if self.RectangleTimeMax != MathMax(self.t1, self.t2) or self.RectangleTimeMin != MathMin(self.t1, self.t2):
            rectangle_changed = True
            rectangle_time_changed = True
        if self.RectanglePriceMax != MathMax(p1, p2) or self.RectanglePriceMin != MathMin(p1, p2):
            rectangle_changed = True
            rectangle_price_changed = True
        if ((EnableDevelopingPOC or EnableDevelopingVAHVAL) and rectangle_changed) and self.RectangleTimeMax != 0:
            local_sessionstart = iBarShift(Symbol(), Period(), self.RectangleTimeMin, True)
            local_sessionend = iBarShift(Symbol(), Period(), self.RectangleTimeMax, True)
            if local_sessionend < 0:
                local_sessionend = 0
            for j in range(local_sessionstart, local_sessionend - 1, -1):
                DevelopingPOC_1[j] = EMPTY_VALUE
                DevelopingPOC_2[j] = EMPTY_VALUE
                DevelopingVAH_1[j] = EMPTY_VALUE
                DevelopingVAH_2[j] = EMPTY_VALUE
                DevelopingVAL_1[j] = EMPTY_VALUE
                DevelopingVAL_2[j] = EMPTY_VALUE
            self.prev_Time0 = 0
        self.RectangleTimeMax = MathMax(self.t1, self.t2)
        self.RectangleTimeMin = MathMin(self.t1, self.t2)
        self.RectanglePriceMax = MathMax(p1, p2)
        self.RectanglePriceMin = MathMin(p1, p2)
        new_bars_are_not_within_rectangle = True
        current_bar_changed_within_boundaries = False
        if Time[0] != self.prev_Time0:
            new_bars_are_not_within_rectangle = False
            if (self.prev_Time0 < self.RectangleTimeMin and Time[0] < self.RectangleTimeMin) or (self.prev_Time0 > self.RectangleTimeMax and Time[0] > self.RectangleTimeMax):
                new_bars_are_not_within_rectangle = True
            if not new_bars_are_not_within_rectangle:
                max_index = iHighest(Symbol(), Period(), MODE_HIGH, iBarShift(Symbol(), Period(), self.prev_Time0, True), 0)
                min_index = iLowest(Symbol(), Period(), MODE_LOW, iBarShift(Symbol(), Period(), self.prev_Time0, True), 0)
                if High[max_index] < self.RectanglePriceMin or Low[min_index] > self.RectanglePriceMax:
                    new_bars_are_not_within_rectangle = True
            self.prev_Time0 = Time[0]
        else:
            if Time[0] >= self.RectangleTimeMin and Time[0] <= self.RectangleTimeMax:
                if self.prev_High != High[0]:
                    if High[0] <= self.RectanglePriceMax and High[0] >= self.RectanglePriceMin:
                        current_bar_changed_within_boundaries = True
                if self.prev_Low != Low[0]:
                    if Low[0] <= self.RectanglePriceMax and Low[0] >= self.RectanglePriceMin:
                        current_bar_changed_within_boundaries = True
        self.prev_High = High[0]
        self.prev_Low = Low[0]
        if sessionend < 0:
            sessionend = 0
        need_to_clean_up_dots = False
        rectangle_changed_and_recalc_is_due = False
        if rectangle_changed:
            if rectangle_price_changed:
                max_index = iHighest(Symbol(), Period(), MODE_HIGH, sessionstart - sessionend, sessionend)
                min_index = iLowest(Symbol(), Period(), MODE_LOW, sessionstart - sessionend, sessionend)
                if max_index != -1 and min_index != -1:
                    if ((self.RectanglePriceMax > High[max_index] and self.RectanglePriceMin < Low[min_index]) and self.prev_RectanglePriceMax > High[max_index]) and self.prev_RectanglePriceMin < Low[min_index]:
                        rectangle_changed_and_recalc_is_due = False
                    else:
                        need_to_clean_up_dots = True
                        rectangle_changed_and_recalc_is_due = True
            if rectangle_time_changed:
                need_to_clean_up_dots = True
                if sessionstart >= 0:
                    rectangle_changed_and_recalc_is_due = True
        self.prev_RectanglePriceMax = self.RectanglePriceMax
        self.prev_RectanglePriceMin = self.RectanglePriceMin
        if (sessionstart - sessionend + 1) != Max_number_of_bars_in_a_session:
            Max_number_of_bars_in_a_session = sessionstart - sessionend + 1
            if not new_bars_are_not_within_rectangle:
                need_to_clean_up_dots = True
        if need_to_clean_up_dots:
            ObjectCleanup(self.name + '_')
        if sessionstart < 0:
            return
        RememberSessionStart[i] = self.RectangleTimeMin
        if Time[0] < self.RectangleTimeMax:
            RememberSessionEnd[i] = Time[0]
        else:
            RememberSessionEnd[i] = self.RectangleTimeMax
        if (((not new_bars_are_not_within_rectangle) or current_bar_changed_within_boundaries) or rectangle_changed_and_recalc_is_due) or (self.Number != i and (RaysUntilIntersection != Stop_No_Rays and (ShowMedianRays != None_ or ShowValueAreaRays != None_))):
            ProcessSession(sessionstart, sessionend, i, High, Low, Time, rates_total, self)
        self.Number = i
    def ResetPrevTime0(self):
        self.prev_Time0 = 0

def OnInit():
    global CurrentColorScheme, DigitsM, InitFailed, IntradaySessionCount, PointMultiplier_calculated, Suffix, ValueAreaPercentage_double, _SessionsToCount, onetick
    InitFailed = False
    _SessionsToCount = SessionsToCount
    if Session == Daily:
        Suffix = '_D'
        if PeriodSeconds() < PeriodSeconds(PERIOD_M5) or PeriodSeconds() > PeriodSeconds(PERIOD_M30):
            alert_text = 'Timeframe should be between M5 and M30 for a Daily session.'
            if not DisableAlertsOnWrongTimeframes:
                Alert(alert_text)
            else:
                Print('Initialization failed: ' + alert_text)
            InitFailed = True
    elif Session == Weekly:
        Suffix = '_W'
        if PeriodSeconds() < PeriodSeconds(PERIOD_M30) or PeriodSeconds() > PeriodSeconds(PERIOD_H4):
            alert_text = 'Timeframe should be between M30 and H4 for a Weekly session.'
            if not DisableAlertsOnWrongTimeframes:
                Alert(alert_text)
            else:
                Print('Initialization failed: ' + alert_text)
            InitFailed = True
    elif Session == Monthly:
        Suffix = '_M'
        if PeriodSeconds() < PeriodSeconds(PERIOD_H1) or PeriodSeconds() > PeriodSeconds(PERIOD_D1):
            alert_text = 'Timeframe should be between H1 and D1 for a Monthly session.'
            if not DisableAlertsOnWrongTimeframes:
                Alert(alert_text)
            else:
                Print('Initialization failed: ' + alert_text)
            InitFailed = True
    elif Session == Intraday:
        if PeriodSeconds() > PeriodSeconds(PERIOD_M15):
            alert_text = 'Timeframe should not be higher than M15 for an Intraday sessions.'
            if not DisableAlertsOnWrongTimeframes:
                Alert(alert_text)
            else:
                Print('Initialization failed: ' + alert_text)
            InitFailed = True
        IntradaySessionCount = 0
        if not CheckIntradaySession(EnableIntradaySession1, IntradaySession1StartTime, IntradaySession1EndTime, IntradaySession1ColorScheme):
            return INIT_PARAMETERS_INCORRECT
        if not CheckIntradaySession(EnableIntradaySession2, IntradaySession2StartTime, IntradaySession2EndTime, IntradaySession2ColorScheme):
            return INIT_PARAMETERS_INCORRECT
        if not CheckIntradaySession(EnableIntradaySession3, IntradaySession3StartTime, IntradaySession3EndTime, IntradaySession3ColorScheme):
            return INIT_PARAMETERS_INCORRECT
        if not CheckIntradaySession(EnableIntradaySession4, IntradaySession4StartTime, IntradaySession4EndTime, IntradaySession4ColorScheme):
            return INIT_PARAMETERS_INCORRECT
        if IntradaySessionCount == 0:
            alert_text = 'Enable at least one intraday session if you want to use Intraday mode.'
            if not DisableAlertsOnWrongTimeframes:
                Alert(alert_text)
            else:
                Print('Initialization failed: ' + alert_text)
            InitFailed = True
    elif Session == Rectangle and SeamlessScrollingMode:
        alert_text = "Seamless scrolling mode doesn't work with Rectangle sessions."
        if not DisableAlertsOnWrongTimeframes:
            Alert(alert_text)
        else:
            Print('Initialization failed: ' + alert_text)
        InitFailed = True
    IndicatorSetString(INDICATOR_SHORTNAME, 'MarketProfile ' + EnumToString(Session, 'session_period'))
    if PointMultiplier == 0:
        quote = Box(0.0)
        success = (SymbolInfoDouble(Symbol(), SYMBOL_ASK, quote) != 0)
        if not success:
            Print('Failed to get price data. Error #', GetLastError(), '. Using PointMultiplier = 1.')
            PointMultiplier_calculated = 1
        else:
            s = Box(DoubleToString(quote.v, Digits()))
            StringReplace(s, '-', '')
            total_digits = StringLen(s.v)
            if StringFind(s.v, '.') != -1:
                total_digits -= 1
            if total_digits <= 5:
                PointMultiplier_calculated = 1
            else:
                PointMultiplier_calculated = _int(MathPow(10, total_digits - 5))
    else:
        PointMultiplier_calculated = PointMultiplier
    DigitsM = Digits() - (StringLen(IntegerToString(PointMultiplier_calculated)) - 1)
    onetick = NormalizeDouble(Point() * PointMultiplier_calculated, DigitsM)
    TickSize = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_SIZE)
    if onetick < TickSize:
        DigitsM = Digits() - (StringLen(IntegerToString(_int(MathRound(_fdiv(TickSize, Point()))))) - 1)
        onetick = NormalizeDouble(TickSize, DigitsM)
    CurrentColorScheme = ColorScheme
    ObjectCleanup()
    if ((Session == Rectangle or RightToLeft) or HideRaysFromInvisibleSessions) or SeamlessScrollingMode:
        EventSetMillisecondTimer(1000)
    if not EnableDevelopingPOC:
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, clrNONE)
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, clrNONE)
    SetIndexBuffer(0, DevelopingPOC_1, INDICATOR_DATA)
    ArraySetAsSeries(DevelopingPOC_1, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, DevelopingPOC_2, INDICATOR_DATA)
    ArraySetAsSeries(DevelopingPOC_2, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, DevelopingVAH_1, INDICATOR_DATA)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DevelopingVAH_1, True)
    SetIndexBuffer(3, DevelopingVAH_2, INDICATOR_DATA)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DevelopingVAH_2, True)
    SetIndexBuffer(4, DevelopingVAL_1, INDICATOR_DATA)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DevelopingVAL_1, True)
    SetIndexBuffer(5, DevelopingVAL_2, INDICATOR_DATA)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DevelopingVAL_2, True)
    ValueAreaPercentage_double = ValueAreaPercentage * 0.01
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if Session == Rectangle:
        i = 0
        while i < mpr_total:
            ObjectCleanup(MPR_Array[i].name + '_')
            _delete(MPR_Array[i])
            i += 1
    else:
        ObjectCleanup()

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global CleanedUpOn, FirstRunDone, Max_number_of_bars_in_a_session, NeedToRestartDrawing, StartDate, Timer
    if InitFailed:
        if not DisableAlertsOnWrongTimeframes:
            Print('Initialization failed. Please see the alert message for details.')
        return 0
    if ((EnableDevelopingPOC or EnableDevelopingVAHVAL) and (rates_total - prev_calculated) > 1) and CleanedUpOn != rates_total:
        for i in range(prev_calculated, rates_total):
            DevelopingPOC_1[i] = EMPTY_VALUE
            DevelopingPOC_2[i] = EMPTY_VALUE
            DevelopingVAH_1[i] = EMPTY_VALUE
            DevelopingVAH_2[i] = EMPTY_VALUE
            DevelopingVAL_1[i] = EMPTY_VALUE
            DevelopingVAL_2[i] = EMPTY_VALUE
        if prev_calculated == 0 and Session == Rectangle:
            for i in range(mpr_total - 1, 0 - 1, -1):
                MPR_Array[i].ResetPrevTime0()
        CleanedUpOn = rates_total
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Time, True)
    CheckAlerts(Open, High, Low, Close, Time)
    if SeamlessScrollingMode:
        last_visible_bar = _int(ChartGetInteger(ChartID(), CHART_FIRST_VISIBLE_BAR)) - _int(ChartGetInteger(ChartID(), CHART_WIDTH_IN_BARS)) + 1
        if last_visible_bar < 0:
            last_visible_bar = 0
        StartDate = Time[last_visible_bar]
    elif StartFromCurrentSession:
        StartDate = Time[0]
    else:
        StartDate = StartFromDate
    if SaturdaySunday == Ignore_Saturday_Sunday:
        if TimeDayOfWeek_u(StartDate) == 6:
            StartDate -= 86400
        elif TimeDayOfWeek_u(StartDate) == 0:
            StartDate -= 2 * 86400
    if FirstRunDone and StartDate != Time[0]:
        return rates_total
    if ThrottleRedraw > 0 and Timer > 0:
        if (_int(TimeLocal()) - Timer) < ThrottleRedraw:
            return rates_total
    if Session == Rectangle:
        CheckRectangles(High, Low, Time, rates_total)
        Timer = _int(TimeLocal())
        return rates_total
    if (rates_total - prev_calculated) > 1 or NeedToRestartDrawing:
        FirstRunDone = False
        ObjectCleanup()
        NeedToRestartDrawing = False
        if EnableDevelopingPOC:
            ArrayInitialize(DevelopingPOC_1, EMPTY_VALUE)
            ArrayInitialize(DevelopingPOC_2, EMPTY_VALUE)
    sessionend = FindSessionEndByDate(Time, StartDate, rates_total)
    sessionstart = FindSessionStart(Time, sessionend, rates_total)
    if sessionstart == -1:
        Print('Something went wrong! Waiting for data to load.')
        return prev_calculated
    SessionToStart = 0
    if FirstRunDone:
        SessionToStart = _SessionsToCount - 1
    else:
        i = 1
        while i < _SessionsToCount:
            sessionend = sessionstart + 1
            if sessionend >= rates_total:
                return prev_calculated
            if SaturdaySunday == Ignore_Saturday_Sunday:
                while TimeDayOfWeek_u(Time[sessionend]) == 0 or TimeDayOfWeek_u(Time[sessionend]) == 6:
                    sessionend += 1
                    if sessionend >= rates_total:
                        break
            sessionstart = FindSessionStart(Time, sessionend, rates_total)
            i += 1
    i = SessionToStart
    while i < _SessionsToCount:
        if Session == Intraday:
            if not ProcessIntradaySession(sessionstart, sessionend, i, High, Low, Time, rates_total):
                return 0
        else:
            if Session == Daily:
                Max_number_of_bars_in_a_session = _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds())
            elif Session == Weekly:
                Max_number_of_bars_in_a_session = _idiv(604800, PeriodSeconds())
            elif Session == Monthly:
                Max_number_of_bars_in_a_session = _idiv(2678400, PeriodSeconds())
            if SaturdaySunday == Append_Saturday_Sunday:
                if TimeDayOfWeek_u(Time[sessionstart]) == 0:
                    Max_number_of_bars_in_a_session += _idiv((24 * 3600) - ((TimeHour_u(Time[sessionstart]) * 3600) + (TimeMinute_u(Time[sessionstart]) * 60)), PeriodSeconds())
                if TimeDayOfWeek_u(Time[sessionend]) == 6:
                    Max_number_of_bars_in_a_session += _idiv((TimeHour_u(Time[sessionend]) * 3600) + (TimeMinute_u(Time[sessionend]) * 60), PeriodSeconds()) + 1
            if not ProcessSession(sessionstart, sessionend, i, High, Low, Time, rates_total):
                return 0
        if (_SessionsToCount - i) > 1:
            sessionstart = sessionend - 1
            if SaturdaySunday == Ignore_Saturday_Sunday:
                while TimeDayOfWeek_u(Time[sessionstart]) == 0 or TimeDayOfWeek_u(Time[sessionstart]) == 6:
                    sessionstart -= 1
                    if sessionstart == 0:
                        break
            sessionend = FindSessionEndByDate(Time, Time[sessionstart], rates_total)
        i += 1
    if (ShowValueAreaRays != None_ or ShowMedianRays != None_) or (HideRaysFromInvisibleSessions and SinglePrintRays):
        CheckRays()
    FirstRunDone = True
    Timer = _int(TimeLocal())
    return rates_total

def FindSessionStart(Time, n, rates_total):
    global _SessionsToCount
    if Session == Daily:
        return FindDayStart(Time, n, rates_total)
    elif Session == Weekly:
        return FindWeekStart(Time, n, rates_total)
    elif Session == Monthly:
        return FindMonthStart(Time, n, rates_total)
    elif Session == Intraday:
        if SaturdaySunday == Append_Saturday_Sunday and TimeDayOfWeek_u(Time[n] + (TimeShiftMinutes * 60)) == 1:
            intraday_i = 0
            while intraday_i < IntradaySessionCount:
                if IDStartTime[intraday_i] == 0 or IDStartTime[intraday_i] > IDEndTime[intraday_i]:
                    if ((TimeHour_u(Time[n]) * 60) + TimeMinute_u(Time[n])) >= IDEndTime[intraday_i] and IDStartTime[intraday_i] > IDEndTime[intraday_i]:
                        x = n
                        while x < rates_total and ((TimeHour_u(Time[x]) * 60) + TimeMinute_u(Time[x])) >= IDEndTime[intraday_i]:
                            x += 1
                            if TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60)) > 1:
                                return FindDayStart(Time, n, rates_total)
                        return x - 1
                    else:
                        x = n
                        while x < rates_total and (TimeDayOfYear_u(Time[n] + (TimeShiftMinutes * 60)) == TimeDayOfYear_u(Time[x] + (TimeShiftMinutes * 60)) or TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60)) == 0):
                            x += 1
                        _SessionsToCount += 1
                        return x - 1
                intraday_i += 1
        return FindDayStart(Time, n, rates_total)
    return -1

def FindDayStart(Time, n, rates_total):
    if n >= rates_total:
        return -1
    x = n
    time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    time_n_day_of_week = time_x_day_of_week
    while TimeDayOfYear_u(Time[n] + (TimeShiftMinutes * 60)) == TimeDayOfYear_u(Time[x] + (TimeShiftMinutes * 60)) or (SaturdaySunday == Append_Saturday_Sunday and (time_x_day_of_week == 0 or (time_x_day_of_week == 5 and time_n_day_of_week == 6))):
        x += 1
        if x >= rates_total:
            break
        time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    return x - 1

def FindWeekStart(Time, n, rates_total):
    if n >= rates_total:
        return -1
    x = n
    time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    while SameWeek(Time[n] + (TimeShiftMinutes * 60), Time[x] + (TimeShiftMinutes * 60)) or (SaturdaySunday == Append_Saturday_Sunday and time_x_day_of_week == 0):
        if SaturdaySunday == Ignore_Saturday_Sunday and time_x_day_of_week == 0:
            break
        x += 1
        if x >= rates_total:
            break
        time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    return x - 1

def FindMonthStart(Time, n, rates_total):
    if n >= rates_total:
        return -1
    x = n
    time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    time_n_day_of_week = TimeDayOfWeek_u(Time[n] + (TimeShiftMinutes * 60))
    time_n_day = TimeDay_u(Time[n] + (TimeShiftMinutes * 60))
    time_n_month = TimeMonth_u(Time[n] + (TimeShiftMinutes * 60))
    while time_n_month == TimeMonth_u(Time[x] + (TimeShiftMinutes * 60)) or (SaturdaySunday == Append_Saturday_Sunday and (time_x_day_of_week == 0 or (time_n_day_of_week == 6 and time_n_day == 1))):
        month_distance = time_n_month - TimeMonth_u(Time[x] + (TimeShiftMinutes * 60))
        if month_distance < 0:
            month_distance = 12 - month_distance
        if month_distance > 1:
            break
        if SaturdaySunday == Append_Saturday_Sunday:
            if (time_x_day_of_week == 6 and TimeDay_u(Time[x] + (TimeShiftMinutes * 60)) == 1) and time_n_day != TimeDay_u(Time[x] + (TimeShiftMinutes * 60)):
                break
        if SaturdaySunday == Ignore_Saturday_Sunday:
            if (time_x_day_of_week == 0 or time_x_day_of_week == 6) and (TimeDay_u(Time[x] + (TimeShiftMinutes * 60)) == 1 or TimeDay_u(Time[x] + (TimeShiftMinutes * 60)) == 2):
                break
        x += 1
        if x >= rates_total:
            break
        time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    return x - 1

def FindSessionEndByDate(Time, date, rates_total):
    if Session == Daily:
        return FindDayEndByDate(Time, date, rates_total)
    elif Session == Weekly:
        return FindWeekEndByDate(Time, date, rates_total)
    elif Session == Monthly:
        return FindMonthEndByDate(Time, date, rates_total)
    elif Session == Intraday:
        if SaturdaySunday == Append_Saturday_Sunday and TimeDayOfWeek_u(date + (TimeShiftMinutes * 60)) == 0:
            intraday_i = 0
            while intraday_i < IntradaySessionCount:
                if IDStartTime[intraday_i] == 0 or IDStartTime[intraday_i] > IDEndTime[intraday_i]:
                    x = 0
                    abs_day = TimeAbsoluteDay(date + (TimeShiftMinutes * 60))
                    while x < rates_total and abs_day < TimeAbsoluteDay(Time[x] + (TimeShiftMinutes * 60)):
                        if TimeAbsoluteDay(Time[x] + (TimeShiftMinutes * 60)) == (abs_day + 1):
                            if ((TimeHour_u(Time[x]) * 60) + TimeMinute_u(Time[x])) < IDEndTime[intraday_i]:
                                break
                            if IDStartTime[intraday_i] == 0:
                                break
                        x += 1
                    return x
                intraday_i += 1
        return FindDayEndByDate(Time, date, rates_total)
    return -1

def FindDayEndByDate(Time, date, rates_total):
    x = 0
    while x < rates_total and TimeAbsoluteDay(date + (TimeShiftMinutes * 60)) < TimeAbsoluteDay(Time[x] + (TimeShiftMinutes * 60)):
        if SaturdaySunday == Append_Saturday_Sunday:
            if (TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60)) == 6 or TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60)) == 1) and (TimeAbsoluteDay(Time[x] + (TimeShiftMinutes * 60)) - TimeAbsoluteDay(date + (TimeShiftMinutes * 60))) == 1:
                break
        x += 1
    return x

def FindWeekEndByDate(Time, date, rates_total):
    x = 0
    time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    while (SameWeek(date + (TimeShiftMinutes * 60), Time[x] + (TimeShiftMinutes * 60)) != True or (SaturdaySunday == Append_Saturday_Sunday and time_x_day_of_week == 0)) or (SaturdaySunday == Ignore_Saturday_Sunday and (time_x_day_of_week == 0 or time_x_day_of_week == 6)):
        x += 1
        if x >= rates_total:
            break
        time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    return x

def FindMonthEndByDate(Time, date, rates_total):
    x = 0
    time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    while (SameMonth(date + (TimeShiftMinutes * 60), Time[x] + (TimeShiftMinutes * 60)) != True or (SaturdaySunday == Append_Saturday_Sunday and time_x_day_of_week == 0)) or (SaturdaySunday == Ignore_Saturday_Sunday and (time_x_day_of_week == 0 or time_x_day_of_week == 6)):
        if SaturdaySunday == Append_Saturday_Sunday:
            if (time_x_day_of_week == 6 and TimeDay_u(Time[x] + (TimeShiftMinutes * 60)) == 1) and ((TimeYear_u(Time[x] + (TimeShiftMinutes * 60)) * 12) + TimeMonth_u(Time[x] + (TimeShiftMinutes * 60)) - (TimeYear_u(date + (TimeShiftMinutes * 60)) * 12) - TimeMonth_u(date + (TimeShiftMinutes * 60))) == 1:
                break
            if TimeDayOfWeek_u(date + (TimeShiftMinutes * 60)) == 0 and ((TimeYear_u(Time[x] + (TimeShiftMinutes * 60)) * 12) + TimeMonth_u(Time[x] + (TimeShiftMinutes * 60)) - (TimeYear_u(date + (TimeShiftMinutes * 60)) * 12) - TimeMonth_u(date + (TimeShiftMinutes * 60))) == 1:
                break
        x += 1
        if x >= rates_total:
            break
        time_x_day_of_week = TimeDayOfWeek_u(Time[x] + (TimeShiftMinutes * 60))
    return x

def SameWeek(date1, date2):
    dt1 = MqlDateTime()
    dt2 = MqlDateTime()
    TimeToStruct(date1, dt1)
    TimeToStruct(date2, dt2)
    seconds_from_start = (dt1.day_of_week * 24 * 3600) + (dt1.hour * 3600) + (dt1.min * 60) + dt1.sec
    if date1 == date2:
        return True
    elif date2 < date1:
        if (date1 - date2) <= seconds_from_start:
            return True
    elif (date2 - date1) < (604800 - seconds_from_start):
        return True
    return False

def SameMonth(date1, date2):
    dt1 = MqlDateTime()
    dt2 = MqlDateTime()
    TimeToStruct(date1, dt1)
    TimeToStruct(date2, dt2)
    if dt1.mon == dt2.mon and dt1.year == dt2.year:
        return True
    return False

def PutDot(price, start_bar, range_, bar, Time, rectangle_prefix='', converted_time=0):
    global NeedToRestartDrawing, _s_PutDot_prev_time_start_bar
    divisor = 0.0
    color_shift = 0.0
    colour = -1
    LastNameStart = ' ' + TimeToString(Time[bar + start_bar]) + ' '
    LastName = LastNameStart + DoubleToString(price, Digits())
    if ColorBullBear:
        colour = CalculateProperColor()
    if NeedToReviewColors:
        obj_total = ObjectsTotal(ChartID(), -1, OBJ_RECTANGLE)
        for i in range(obj_total - 1, 0 - 1, -1):
            obj = ObjectName(ChartID(), i, -1, OBJ_RECTANGLE)
            if StringSubstr(obj, 0, StringLen(rectangle_prefix + 'MP' + Suffix)) != (rectangle_prefix + 'MP' + Suffix):
                continue
            if StringSubstr(obj, 0, StringLen(rectangle_prefix + 'MP' + Suffix + LastNameStart)) != (rectangle_prefix + 'MP' + Suffix + LastNameStart):
                break
            ObjectSetInteger(0, obj, OBJPROP_COLOR, colour)
    if ObjectFind(0, rectangle_prefix + 'MP' + Suffix + LastName) >= 0:
        if (not RightToLeft) or converted_time == 0:
            return 0
    time_end = 0
    time_start = 0
    prev_time = converted_time
    if converted_time != 0:
        if Time[start_bar] != _s_PutDot_prev_time_start_bar and _s_PutDot_prev_time_start_bar != 0:
            NeedToRestartDrawing = True
        _s_PutDot_prev_time_start_bar = Time[start_bar]
        x = -1
        for i in range(range_ + 1, 0, -1):
            prev_time = converted_time
            if converted_time == Time[0]:
                x = i + 1
                converted_time = Time[1]
            elif converted_time < Time[0]:
                if x == -1:
                    x = iBarShift(Symbol(), Period(), converted_time) + i + 1
                converted_time = Time[x - i]
            else:
                converted_time -= PeriodSeconds()
        time_end = converted_time
        time_start = prev_time
    else:
        if (start_bar - (range_ + 1)) < 0:
            time_end = Time[0] + PeriodSeconds()
        else:
            time_end = Time[start_bar - (range_ + 1)]
        time_start = Time[start_bar - range_]
    if ObjectFind(0, rectangle_prefix + 'MP' + Suffix + LastName) >= 0:
        ObjectSetInteger(0, rectangle_prefix + 'MP' + Suffix + LastName, OBJPROP_TIME, 0, time_start)
        ObjectSetInteger(0, rectangle_prefix + 'MP' + Suffix + LastName, OBJPROP_TIME, 1, time_end)
    else:
        ObjectCreate(0, rectangle_prefix + 'MP' + Suffix + LastName, OBJ_RECTANGLE, 0, time_start, price, time_end, price - onetick)
    if not ColorBullBear:
        offset1 = 0
        offset2 = 0
        _sw1 = CurrentColorScheme
        if _sw1 == Blue_to_Red:
            colour = 0x00FF0000
            offset1 = 0x00010000
            offset2 = 0x00000001
        elif _sw1 == Red_to_Green:
            colour = 0x000000FF
            offset1 = 0x00000001
            offset2 = 0x00000100
        elif _sw1 == Green_to_Blue:
            colour = 0x0000FF00
            offset1 = 0x00000100
            offset2 = 0x00010000
        elif _sw1 == Yellow_to_Cyan:
            colour = 0x0000FFFF
            offset1 = 0x00000001
            offset2 = 0x00010000
        elif _sw1 == Magenta_to_Yellow:
            colour = 0x00FF00FF
            offset1 = 0x00010000
            offset2 = 0x00000100
        elif _sw1 == Cyan_to_Magenta:
            colour = 0x00FFFF00
            offset1 = 0x00000100
            offset2 = 0x00000001
        elif _sw1 == Single_Color:
            colour = SingleColor
            offset1 = 0
            offset2 = 0
        else:
            colour = SingleColor
            offset1 = 0
            offset2 = 0
        if CurrentColorScheme != Single_Color:
            divisor = (1.0 / 0xFF) * float(Max_number_of_bars_in_a_session)
            color_shift = MathFloor(_fdiv(float(bar), divisor))
            if _int(color_shift) < -255:
                color_shift = -255.0
            colour += _uint(_int(color_shift) * offset1)
            colour -= _uint(_int(color_shift) * offset2)
    ObjectSetInteger(0, rectangle_prefix + 'MP' + Suffix + LastName, OBJPROP_COLOR, colour)
    ObjectSetInteger(0, rectangle_prefix + 'MP' + Suffix + LastName, OBJPROP_FILL, True)
    ObjectSetInteger(0, rectangle_prefix + 'MP' + Suffix + LastName, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, rectangle_prefix + 'MP' + Suffix + LastName, OBJPROP_HIDDEN, True)
    return time_end

def ObjectCleanup(rectangle_prefix=''):
    ObjectsDeleteAll(0, rectangle_prefix + 'MP' + Suffix, 0, OBJ_RECTANGLE)
    ObjectsDeleteAll(0, rectangle_prefix + 'Median' + Suffix, 0, OBJ_TREND)
    ObjectsDeleteAll(0, rectangle_prefix + 'VA_LeftSide' + Suffix, 0, OBJ_TREND)
    ObjectsDeleteAll(0, rectangle_prefix + 'VA_RightSide' + Suffix, 0, OBJ_TREND)
    ObjectsDeleteAll(0, rectangle_prefix + 'VA_Top' + Suffix, 0, OBJ_TREND)
    ObjectsDeleteAll(0, rectangle_prefix + 'VA_Bottom' + Suffix, 0, OBJ_TREND)
    if ShowValueAreaRays != None_:
        ObjectsDeleteAll(0, rectangle_prefix + 'Value Area HighRay' + Suffix, 0, OBJ_TREND)
        ObjectsDeleteAll(0, rectangle_prefix + 'Value Area LowRay' + Suffix, 0, OBJ_TREND)
    if ShowMedianRays != None_:
        ObjectsDeleteAll(0, rectangle_prefix + 'Median Ray' + Suffix, 0, OBJ_TREND)
    if ShowKeyValues:
        ObjectsDeleteAll(0, rectangle_prefix + 'VAH' + Suffix, 0, OBJ_TEXT)
        ObjectsDeleteAll(0, rectangle_prefix + 'VAL' + Suffix, 0, OBJ_TEXT)
        ObjectsDeleteAll(0, rectangle_prefix + 'POC' + Suffix, 0, OBJ_TEXT)
    if ShowSinglePrint:
        ObjectsDeleteAll(0, rectangle_prefix + 'MPSP' + Suffix, 0, OBJ_RECTANGLE)
    if SinglePrintRays:
        ObjectsDeleteAll(0, rectangle_prefix + 'MPSPR' + Suffix, 0, OBJ_TREND)
    if AlertArrows:
        DeleteArrowsByPrefix(rectangle_prefix)

def GetHoursAndMinutes(time_string, hours, minutes, time):
    if StringLen(time_string) == 4:
        time_string = '0' + time_string
    if (((((StringLen(time_string) != 5 or StringGetCharacter(time_string, 2) != 58) or (StringGetCharacter(time_string, 0) < 48 or StringGetCharacter(time_string, 0) > 50)) or ((StringGetCharacter(time_string, 0) == 48 or StringGetCharacter(time_string, 0) == 49) and (StringGetCharacter(time_string, 1) < 48 or StringGetCharacter(time_string, 1) > 57))) or (StringGetCharacter(time_string, 0) == 50 and (StringGetCharacter(time_string, 1) < 48 or StringGetCharacter(time_string, 1) > 51))) or (StringGetCharacter(time_string, 3) < 48 or StringGetCharacter(time_string, 3) > 53)) or (StringGetCharacter(time_string, 4) < 48 or StringGetCharacter(time_string, 4) > 57):
        Print('Wrong time string: ', time_string, '. Please use HH:MM format.')
        return False
    result = Arr(0, "")
    number_of_substrings = StringSplit(time_string, 58, result)
    hours.v = _int(StringToInteger(result[0]))
    minutes.v = _int(StringToInteger(result[1]))
    time.v = (hours.v * 60) + minutes.v
    return True

def CheckIntradaySession(enable, start_time, end_time, cs):
    global IntradayCrossSessionDefined, IntradaySessionCount
    if enable:
        if not GetHoursAndMinutes(start_time, _ElemRef(IDStartHours, IntradaySessionCount), _ElemRef(IDStartMinutes, IntradaySessionCount), _ElemRef(IDStartTime, IntradaySessionCount)):
            Alert('Wrong time string format: ', start_time, '.')
            return False
        if not GetHoursAndMinutes(end_time, _ElemRef(IDEndHours, IntradaySessionCount), _ElemRef(IDEndMinutes, IntradaySessionCount), _ElemRef(IDEndTime, IntradaySessionCount)):
            Alert('Wrong time string format: ', end_time, '.')
            return False
        if IDEndTime[IntradaySessionCount] == 0:
            IDEndHours[IntradaySessionCount] = 24
            IDEndMinutes[IntradaySessionCount] = 0
            IDEndTime[IntradaySessionCount] = 24 * 60
        IDColorScheme[IntradaySessionCount] = cs
        if IDEndTime[IntradaySessionCount] < IDStartTime[IntradaySessionCount]:
            IntradayCrossSessionDefined = IntradaySessionCount
        IntradaySessionCount += 1
    return True

def ProcessSession(sessionstart, sessionend, i, High, Low, Time, rates_total, rectangle=None):
    global CurrentBarDirection, NeedToReviewColors, PreviousBarDirection, SessionsNumber, _s_ProcessSession_PreviousSessionMax, _s_ProcessSession_PreviousSessionStartTime
    rectangle_prefix = ''
    if sessionstart >= rates_total:
        return False
    SessionMax = DBL_MIN
    SessionMin = DBL_MAX
    for bar in range(sessionstart, sessionend - 1, -1):
        if High[bar] > SessionMax:
            SessionMax = High[bar]
        if Low[bar] < SessionMin:
            SessionMin = Low[bar]
    SessionMax = NormalizeDouble(SessionMax, DigitsM)
    SessionMin = NormalizeDouble(SessionMin, DigitsM)
    session_counter = i
    if Session == Rectangle:
        rectangle_prefix = rectangle.name + '_'
        if SessionMax > rectangle.RectanglePriceMax:
            SessionMax = NormalizeDouble(rectangle.RectanglePriceMax, DigitsM)
        if SessionMin < rectangle.RectanglePriceMin:
            SessionMin = NormalizeDouble(rectangle.RectanglePriceMin, DigitsM)
    else:
        need_to_increment = True
        for j in range(0, SessionsNumber):
            if RememberSessionStart[j] == Time[sessionstart]:
                need_to_increment = False
                session_counter = j
                break
        if need_to_increment:
            SessionsNumber += 1
            session_counter = SessionsNumber - 1
            ArrayResize(RememberSessionMax, SessionsNumber)
            ArrayResize(RememberSessionMin, SessionsNumber)
            ArrayResize(RememberSessionStart, SessionsNumber)
            ArrayResize(RememberSessionSuffix, SessionsNumber)
            ArrayResize(RememberSessionEnd, SessionsNumber)
    SessionMax = NormalizeDouble(MathRound(_fdiv(SessionMax, onetick)) * onetick, DigitsM)
    SessionMin = NormalizeDouble(MathRound(_fdiv(SessionMin, onetick)) * onetick, DigitsM)
    RememberSessionMax[session_counter] = SessionMax
    RememberSessionMin[session_counter] = SessionMin
    RememberSessionStart[session_counter] = Time[sessionstart]
    RememberSessionSuffix[session_counter] = Suffix
    RememberSessionEnd[session_counter] = Time[sessionend]
    if Time[sessionstart] > _s_ProcessSession_PreviousSessionStartTime:
        _s_ProcessSession_PreviousSessionMax = DBL_MIN
        _s_ProcessSession_PreviousSessionStartTime = Time[sessionstart]
    if (FirstRunDone and i == (_SessionsToCount - 1)) and PointMultiplier_calculated > 1:
        if (SessionMax - _s_ProcessSession_PreviousSessionMax) < onetick:
            SessionMax = _s_ProcessSession_PreviousSessionMax
        else:
            if _s_ProcessSession_PreviousSessionMax != DBL_MIN:
                nc = _fdiv(SessionMax - _s_ProcessSession_PreviousSessionMax, onetick)
                SessionMax = NormalizeDouble(_s_ProcessSession_PreviousSessionMax + (MathRound(nc) * onetick), DigitsM)
            _s_ProcessSession_PreviousSessionMax = SessionMax
    TPOperPrice = Arr(0, 0)
    max_ = _int(MathRound(_fdiv(SessionMax - SessionMin, onetick) + 2))
    ArrayResize(TPOperPrice, max_)
    ArrayInitialize(TPOperPrice, 0)
    SinglePrintTracking_array = Arr(0, False)
    if SinglePrintRays:
        ArrayResize(SinglePrintTracking_array, max_)
        ArrayInitialize(SinglePrintTracking_array, False)
    MaxRange = 0
    PriceOfMaxRange = 0.0
    DistanceToCenter = DBL_MAX
    converted_time = Box(0)
    converted_end_time = 0
    min_converted_end_time = UINT_MAX
    if RightToLeft and (sessionend == 0 or Session == Rectangle):
        dummy_subwindow = Box(0)
        dummy_price = Box(0.0)
        if Session == Rectangle:
            converted_time.v = rectangle.RectangleTimeMax
        else:
            ChartXYToTimePrice(0, _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)), 0, dummy_subwindow, converted_time, dummy_price)
    TotalTPO = 0
    price = SessionMax
    while price >= SessionMin:
        price = NormalizeDouble(price, DigitsM)
        range_ = 0
        for bar in range(sessionstart, sessionend - 1, -1):
            if price >= Low[bar] and price <= High[bar]:
                if MaxRange < range_ or (MaxRange == range_ and MathAbs(price - (SessionMin + ((SessionMax - SessionMin) / 2))) < DistanceToCenter):
                    MaxRange = range_
                    PriceOfMaxRange = price
                    DistanceToCenter = MathAbs(price - (SessionMin + ((SessionMax - SessionMin) / 2)))
                if not DisableHistogram:
                    if ColorBullBear:
                        close = iClose(None, PERIOD_CURRENT, bar)
                        open = iOpen(None, PERIOD_CURRENT, bar)
                        if close == open:
                            CurrentBarDirection = Neutral
                        elif close > open:
                            CurrentBarDirection = Bullish
                        elif close < open:
                            CurrentBarDirection = Bearish
                        if bar == 0:
                            if PreviousBarDirection == CurrentBarDirection:
                                NeedToReviewColors = False
                            else:
                                NeedToReviewColors = True
                                PreviousBarDirection = CurrentBarDirection
                    if not RightToLeft:
                        PutDot(price, sessionstart, range_, bar - sessionstart, Time, rectangle_prefix)
                    else:
                        converted_end_time = PutDot(price, sessionstart, range_, bar - sessionstart, Time, rectangle_prefix, converted_time.v)
                        if converted_end_time < min_converted_end_time:
                            min_converted_end_time = converted_end_time
                index = _int(MathRound(_fdiv(price - SessionMin, onetick)))
                TPOperPrice[index] += 1
                range_ += 1
                TotalTPO += 1
        if ShowSinglePrint:
            if range_ == 1:
                PutSinglePrintMark(price, sessionstart, rectangle_prefix, Time)
            elif range_ > 1:
                RemoveSinglePrintMark(price, sessionstart, rectangle_prefix, Time)
        if SinglePrintRays:
            index = _int(MathRound(_fdiv(price - SessionMin, onetick)))
            if range_ == 1:
                SinglePrintTracking_array[index] = True
            else:
                SinglePrintTracking_array[index] = False
        price -= onetick
    if SinglePrintRays:
        spr_color = SinglePrintColor
        if HideRaysFromInvisibleSessions and iTime(Symbol(), Period(), _int(ChartGetInteger(ChartID(), CHART_FIRST_VISIBLE_BAR))) >= Time[sessionstart]:
            spr_color = clrNONE
        price = SessionMax
        while price >= SessionMin:
            price = NormalizeDouble(price, DigitsM)
            index = _int(MathRound(_fdiv(price - SessionMin, onetick)))
            if SinglePrintTracking_array[index]:
                if price == SessionMax:
                    PutSinglePrintRay(price, sessionstart, rectangle_prefix, Time, spr_color)
                else:
                    if SinglePrintTracking_array[index + 1] == False:
                        PutSinglePrintRay(price, sessionstart, rectangle_prefix, Time, spr_color)
                    else:
                        RemoveSinglePrintRay(price, sessionstart, rectangle_prefix, Time)
                if price == SessionMin:
                    PutSinglePrintRay(price - onetick, sessionstart, rectangle_prefix, Time, spr_color)
                else:
                    if SinglePrintTracking_array[index - 1] == False:
                        PutSinglePrintRay(price - onetick, sessionstart, rectangle_prefix, Time, spr_color)
                    else:
                        RemoveSinglePrintRay(price - onetick, sessionstart, rectangle_prefix, Time)
            else:
                RemoveSinglePrintRay(price - onetick, sessionstart, rectangle_prefix, Time)
            price -= onetick
    if EnableDevelopingPOC or EnableDevelopingVAHVAL:
        CalculateDevelopingPOCVAHVAL(sessionstart, sessionend, High, Low, rectangle)
    ValueControlTPO = _int(float(TotalTPO) * ValueAreaPercentage_double)
    index = _int(_fdiv(PriceOfMaxRange - SessionMin, onetick))
    if index < 0:
        return False
    TPOcount = TPOperPrice[index]
    up_offset = 1
    down_offset = 1
    while TPOcount < ValueControlTPO:
        abovePrice = PriceOfMaxRange + (up_offset * onetick)
        belowPrice = PriceOfMaxRange - (down_offset * onetick)
        index = _int(MathRound(_fdiv(abovePrice - SessionMin, onetick)))
        index2 = _int(MathRound(_fdiv(belowPrice - SessionMin, onetick)))
        if (belowPrice < SessionMin or TPOperPrice[index] >= TPOperPrice[index2]) and abovePrice <= SessionMax:
            TPOcount += TPOperPrice[index]
            up_offset += 1
        elif belowPrice >= SessionMin:
            TPOcount += TPOperPrice[index2]
            down_offset += 1
        elif TPOcount < ValueControlTPO:
            break
    LastName = ' ' + TimeToString(Time[sessionstart])
    ObjectDelete(0, rectangle_prefix + 'Median' + Suffix + LastName)
    index = MathMax(sessionstart - MaxRange - 1, 0)
    time_start = 0
    time_end = 0
    if RightToLeft and (sessionend == 0 or Session == Rectangle):
        time_end = min_converted_end_time
        time_start = converted_time.v
    else:
        time_end = Time[index]
        time_start = Time[sessionstart]
    ObjectCreate(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJ_TREND, 0, time_start, PriceOfMaxRange, time_end, PriceOfMaxRange)
    mc = MedianColor
    if (_fdiv(float(sessionstart - index), float(Max_number_of_bars_in_a_session)) * 100) >= ProminentMedianPercentage:
        mc = ProminentMedianColor
        ObjectSetInteger(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJPROP_WIDTH, ProminentMedianWidth)
        ObjectSetInteger(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJPROP_STYLE, ProminentMedianStyle)
    else:
        ObjectSetInteger(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJPROP_WIDTH, MedianWidth)
        ObjectSetInteger(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJPROP_STYLE, MedianStyle)
    ObjectSetInteger(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJPROP_COLOR, mc)
    ObjectSetInteger(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJPROP_BACK, False)
    ObjectSetInteger(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, rectangle_prefix + 'Median' + Suffix + LastName, OBJPROP_RAY, False)
    ObjectDelete(0, rectangle_prefix + 'VA_LeftSide' + Suffix + LastName)
    ObjectCreate(0, rectangle_prefix + 'VA_LeftSide' + Suffix + LastName, OBJ_TREND, 0, time_start, PriceOfMaxRange + (up_offset * onetick), time_start, PriceOfMaxRange - (down_offset * onetick) + onetick)
    ObjectSetInteger(0, rectangle_prefix + 'VA_LeftSide' + Suffix + LastName, OBJPROP_COLOR, ValueAreaSidesColor)
    ObjectSetInteger(0, rectangle_prefix + 'VA_LeftSide' + Suffix + LastName, OBJPROP_STYLE, ValueAreaSidesStyle)
    ObjectSetInteger(0, rectangle_prefix + 'VA_LeftSide' + Suffix + LastName, OBJPROP_WIDTH, ValueAreaSidesWidth)
    ObjectSetInteger(0, rectangle_prefix + 'VA_LeftSide' + Suffix + LastName, OBJPROP_BACK, False)
    ObjectSetInteger(0, rectangle_prefix + 'VA_LeftSide' + Suffix + LastName, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, rectangle_prefix + 'VA_LeftSide' + Suffix + LastName, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, rectangle_prefix + 'VA_LeftSide' + Suffix + LastName, OBJPROP_RAY, False)
    ObjectDelete(0, rectangle_prefix + 'VA_RightSide' + Suffix + LastName)
    ObjectCreate(0, rectangle_prefix + 'VA_RightSide' + Suffix + LastName, OBJ_TREND, 0, time_end, PriceOfMaxRange + (up_offset * onetick), time_end, PriceOfMaxRange - (down_offset * onetick) + onetick)
    ObjectSetInteger(0, rectangle_prefix + 'VA_RightSide' + Suffix + LastName, OBJPROP_COLOR, ValueAreaSidesColor)
    ObjectSetInteger(0, rectangle_prefix + 'VA_RightSide' + Suffix + LastName, OBJPROP_STYLE, ValueAreaSidesStyle)
    ObjectSetInteger(0, rectangle_prefix + 'VA_RightSide' + Suffix + LastName, OBJPROP_WIDTH, ValueAreaSidesWidth)
    ObjectSetInteger(0, rectangle_prefix + 'VA_RightSide' + Suffix + LastName, OBJPROP_BACK, False)
    ObjectSetInteger(0, rectangle_prefix + 'VA_RightSide' + Suffix + LastName, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, rectangle_prefix + 'VA_RightSide' + Suffix + LastName, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, rectangle_prefix + 'VA_RightSide' + Suffix + LastName, OBJPROP_RAY, False)
    ObjectDelete(0, rectangle_prefix + 'VA_Top' + Suffix + LastName)
    ObjectCreate(0, rectangle_prefix + 'VA_Top' + Suffix + LastName, OBJ_TREND, 0, time_start, PriceOfMaxRange + (up_offset * onetick), time_end, PriceOfMaxRange + (up_offset * onetick))
    ObjectSetInteger(0, rectangle_prefix + 'VA_Top' + Suffix + LastName, OBJPROP_COLOR, ValueAreaHighLowColor)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Top' + Suffix + LastName, OBJPROP_STYLE, ValueAreaHighLowStyle)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Top' + Suffix + LastName, OBJPROP_WIDTH, ValueAreaHighLowWidth)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Top' + Suffix + LastName, OBJPROP_BACK, False)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Top' + Suffix + LastName, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Top' + Suffix + LastName, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Top' + Suffix + LastName, OBJPROP_RAY, False)
    ObjectDelete(0, rectangle_prefix + 'VA_Bottom' + Suffix + LastName)
    ObjectCreate(0, rectangle_prefix + 'VA_Bottom' + Suffix + LastName, OBJ_TREND, 0, time_start, PriceOfMaxRange - (down_offset * onetick) + onetick, time_end, PriceOfMaxRange - (down_offset * onetick) + onetick)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Bottom' + Suffix + LastName, OBJPROP_COLOR, ValueAreaHighLowColor)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Bottom' + Suffix + LastName, OBJPROP_STYLE, ValueAreaHighLowStyle)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Bottom' + Suffix + LastName, OBJPROP_WIDTH, ValueAreaHighLowWidth)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Bottom' + Suffix + LastName, OBJPROP_BACK, False)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Bottom' + Suffix + LastName, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Bottom' + Suffix + LastName, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, rectangle_prefix + 'VA_Bottom' + Suffix + LastName, OBJPROP_RAY, False)
    if ShowKeyValues:
        anchor_poc = ANCHOR_RIGHT
        anchor_va = ANCHOR_RIGHT
        if RightToLeft and (sessionend == 0 or Session == Rectangle):
            time_start = time_end
            if (Session != Rectangle and ((ShowValueAreaRays == All or ShowValueAreaRays == Current) or ShowValueAreaRays == PreviousCurrent)) or (Session == Rectangle and ((((ShowValueAreaRays == AllPrevious and (SessionsNumber - session_counter) >= 2) or ((ShowValueAreaRays == Previous or ShowValueAreaRays == PreviousCurrent) and (SessionsNumber - session_counter) == 2)) or ((ShowValueAreaRays == Current or ShowValueAreaRays == PreviousCurrent) and (SessionsNumber - session_counter) == 1)) or ShowValueAreaRays == All)):
                anchor_va = ANCHOR_RIGHT_LOWER
            if (Session != Rectangle and ((ShowMedianRays == All or ShowMedianRays == Current) or ShowMedianRays == PreviousCurrent)) or (Session == Rectangle and ((((ShowMedianRays == AllPrevious and (SessionsNumber - session_counter) >= 2) or ((ShowMedianRays == Previous or ShowMedianRays == PreviousCurrent) and (SessionsNumber - session_counter) == 2)) or ((ShowMedianRays == Current or ShowMedianRays == PreviousCurrent) and (SessionsNumber - session_counter) == 1)) or ShowMedianRays == All)):
                anchor_poc = ANCHOR_RIGHT_LOWER
        ValuePrintOut(rectangle_prefix + 'VAH' + Suffix + LastName, time_start, PriceOfMaxRange + (up_offset * onetick), anchor_va)
        ValuePrintOut(rectangle_prefix + 'VAL' + Suffix + LastName, time_start, PriceOfMaxRange - (down_offset * onetick), anchor_va)
        ValuePrintOut(rectangle_prefix + 'POC' + Suffix + LastName, time_start, PriceOfMaxRange, anchor_poc)
    return True

def ProcessIntradaySession(sessionstart, sessionend, i, High, Low, Time, rates_total):
    global CurrentColorScheme, Max_number_of_bars_in_a_session, Suffix
    remember_sessionstart = sessionstart
    remember_sessionend = sessionend
    if remember_sessionend >= rates_total:
        return False
    ContinuePreventionFlag = False
    IntradaySessionCount_tmp = IntradaySessionCount
    if (SaturdaySunday == Ignore_Saturday_Sunday and TimeDayOfWeek_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) == 1) and IntradayCrossSessionDefined > -1:
        IntradaySessionCount_tmp += 1
    intraday_i = 0
    while intraday_i < IntradaySessionCount_tmp:
        if ContinuePreventionFlag:
            break
        if intraday_i == IntradaySessionCount:
            intraday_i = IntradayCrossSessionDefined
            ContinuePreventionFlag = True
        Suffix = '_ID' + IntegerToString(intraday_i)
        CurrentColorScheme = IDColorScheme[intraday_i]
        Max_number_of_bars_in_a_session = IDEndTime[intraday_i] - IDStartTime[intraday_i]
        if Max_number_of_bars_in_a_session < 0:
            Max_number_of_bars_in_a_session = (24 * 60) + Max_number_of_bars_in_a_session
            if SaturdaySunday == Ignore_Saturday_Sunday:
                if TimeDayOfWeek_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) == 1 and (not ContinuePreventionFlag):
                    Max_number_of_bars_in_a_session -= (24 * 60) - IDStartTime[intraday_i]
                elif TimeDayOfWeek_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) == 5:
                    Max_number_of_bars_in_a_session -= IDEndTime[intraday_i]
        if SaturdaySunday == Append_Saturday_Sunday:
            if (IDStartTime[intraday_i] == 0 or IDStartTime[intraday_i] > IDEndTime[intraday_i]) and TimeDayOfWeek_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) == 0:
                Max_number_of_bars_in_a_session += (24 * 60) - ((TimeHour_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)))
                if IDStartTime[intraday_i] > IDEndTime[intraday_i]:
                    Max_number_of_bars_in_a_session -= (24 * 60) - IDStartTime[intraday_i]
            elif (IDEndTime[intraday_i] == (24 * 60) or IDStartTime[intraday_i] > IDEndTime[intraday_i]) and TimeDayOfWeek_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) == 5:
                Max_number_of_bars_in_a_session += 24 * 60
                if IDStartTime[intraday_i] > IDEndTime[intraday_i]:
                    Max_number_of_bars_in_a_session -= (24 * 60) - IDEndTime[intraday_i]
        Max_number_of_bars_in_a_session = _idiv(Max_number_of_bars_in_a_session, _idiv(PeriodSeconds(), 60))
        hour = 0
        minute = 0
        time = 0
        if FirstRunDone:
            hour = TimeHour_u(Time[0] + (TimeShiftMinutes * 60))
            minute = TimeMinute_u(Time[0] + (TimeShiftMinutes * 60))
            time = (hour * 60) + minute
            if IDStartTime[intraday_i] < IDEndTime[intraday_i]:
                if SaturdaySunday == Append_Saturday_Sunday:
                    if IDStartTime[intraday_i] != 0 and TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 0:
                        intraday_i += 1
                        continue
                    if IDEndTime[intraday_i] != (24 * 60) and TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 6:
                        intraday_i += 1
                        continue
                if (SaturdaySunday == Append_Saturday_Sunday and IDStartTime[intraday_i] == 0) and (TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 0 or (TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 1 and time < IDEndTime[intraday_i])):
                    sessionstart = remember_sessionstart
                elif (time < IDEndTime[intraday_i] and time >= IDStartTime[intraday_i]) or ((SaturdaySunday == Append_Saturday_Sunday and IDEndTime[intraday_i] == (24 * 60)) and TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 6):
                    sessionstart = 0
                    sessiontime = (TimeHour_u(Time[sessionstart] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[sessionstart] + (TimeShiftMinutes * 60))
                    while (sessiontime > IDStartTime[intraday_i] and (TimeDayOfYear_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == TimeDayOfYear_u(Time[0] + (TimeShiftMinutes * 60)) or ((SaturdaySunday == Append_Saturday_Sunday and IDEndTime[intraday_i] == (24 * 60)) and TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 6))) or ((SaturdaySunday == Append_Saturday_Sunday and IDEndTime[intraday_i] == (24 * 60)) and TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 6):
                        sessionstart += 1
                        sessiontime = (TimeHour_u(Time[sessionstart] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[sessionstart] + (TimeShiftMinutes * 60))
                    if sessionstart > remember_sessionstart:
                        sessionstart = remember_sessionstart
                else:
                    intraday_i += 1
                    continue
            elif IDStartTime[intraday_i] > IDEndTime[intraday_i]:
                if SaturdaySunday == Append_Saturday_Sunday and (TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 0 or (TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 1 and time < IDEndTime[intraday_i])):
                    sessionstart = remember_sessionstart
                elif (SaturdaySunday == Ignore_Saturday_Sunday and TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 1) and time < IDEndTime[intraday_i]:
                    sessionstart = remember_sessionstart
                elif (time < IDEndTime[intraday_i] or time >= IDStartTime[intraday_i]) or (SaturdaySunday == Append_Saturday_Sunday and TimeDayOfWeek_u(Time[0] + (TimeShiftMinutes * 60)) == 6):
                    sessionstart = 0
                    sessiontime = (TimeHour_u(Time[sessionstart] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[sessionstart] + (TimeShiftMinutes * 60))
                    while ((sessiontime > IDStartTime[intraday_i] and (Time[0] - Time[sessionstart]) <= (3600 * 24)) or (sessiontime < IDEndTime[intraday_i] and TimeDayOfYear_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == TimeDayOfYear_u(Time[0] + (TimeShiftMinutes * 60)))) or (SaturdaySunday == Append_Saturday_Sunday and TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 6):
                        sessionstart += 1
                        sessiontime = (TimeHour_u(Time[sessionstart] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[sessionstart] + (TimeShiftMinutes * 60))
                    if (Time[0] - Time[sessionstart]) > (3600 * 24):
                        sessionstart -= 1
                else:
                    intraday_i += 1
                    continue
            else:
                intraday_i += 1
                continue
            sessionend = 0
            if not ProcessSession(sessionstart, sessionend, i, High, Low, Time, rates_total):
                return False
        else:
            sessionend = remember_sessionend
            if IDStartTime[intraday_i] < IDEndTime[intraday_i]:
                if (SaturdaySunday == Append_Saturday_Sunday and TimeDayOfWeek_u(Time[remember_sessionend] + (TimeShiftMinutes * 60)) == 6) and TimeDayOfWeek_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) == 5:
                    pass
                elif ((TimeHour_u(Time[remember_sessionend] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[remember_sessionend] + (TimeShiftMinutes * 60))) < IDStartTime[intraday_i]:
                    intraday_i += 1
                    continue
                if SaturdaySunday == Append_Saturday_Sunday and ((IDStartTime[intraday_i] == 0 and TimeDayOfWeek_u(Time[remember_sessionend] + (TimeShiftMinutes * 60)) == 0) or (TimeDayOfWeek_u(Time[remember_sessionend] + (TimeShiftMinutes * 60)) == 1 and TimeDayOfWeek_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) == 0)):
                    pass
                elif ((TimeHour_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60))) >= IDEndTime[intraday_i]:
                    intraday_i += 1
                    continue
                if (SaturdaySunday == Append_Saturday_Sunday and IDEndTime[intraday_i] == (24 * 60)) and TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 5:
                    pass
                elif (SaturdaySunday == Append_Saturday_Sunday and IDStartTime[intraday_i] == 0) and TimeDayOfWeek_u(Time[sessionend] + (TimeShiftMinutes * 60)) == 0:
                    pass
                else:
                    while sessionend < rates_total and (((TimeHour_u(Time[sessionend] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[sessionend] + (TimeShiftMinutes * 60))) >= IDEndTime[intraday_i] or (TimeDayOfWeek_u(Time[sessionend] + (TimeShiftMinutes * 60)) == 6 and SaturdaySunday == Append_Saturday_Sunday)):
                        sessionend += 1
                if sessionend == rates_total:
                    sessionend -= 1
                if (SaturdaySunday == Append_Saturday_Sunday and IDStartTime[intraday_i] == 0) and TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 0:
                    sessionstart = remember_sessionstart
                else:
                    sessionstart = sessionend
                    while sessionstart < rates_total and ((((TimeHour_u(Time[sessionstart] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[sessionstart] + (TimeShiftMinutes * 60))) >= IDStartTime[intraday_i] and (TimeDayOfYear_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == TimeDayOfYear_u(Time[sessionend] + (TimeShiftMinutes * 60)) or ((SaturdaySunday == Append_Saturday_Sunday and IDEndTime[intraday_i] == (24 * 60)) and TimeDayOfWeek_u(Time[sessionend] + (TimeShiftMinutes * 60)) == 6))) or ((SaturdaySunday == Append_Saturday_Sunday and IDEndTime[intraday_i] == (24 * 60)) and TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 6)):
                        sessionstart += 1
                    sessionstart -= 1
            elif IDStartTime[intraday_i] > IDEndTime[intraday_i]:
                if SaturdaySunday == Append_Saturday_Sunday and ((TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 5 and TimeDayOfWeek_u(Time[remember_sessionend] + (TimeShiftMinutes * 60)) == 6) or (TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 0 and TimeDayOfWeek_u(Time[remember_sessionend] + (TimeShiftMinutes * 60)) == 1)):
                    pass
                elif ((TimeHour_u(Time[remember_sessionend] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[remember_sessionend] + (TimeShiftMinutes * 60))) < IDStartTime[intraday_i]:
                    intraday_i += 1
                    continue
                if SaturdaySunday == Append_Saturday_Sunday and TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 0:
                    sessionstart = remember_sessionstart
                elif (SaturdaySunday == Ignore_Saturday_Sunday and TimeDayOfWeek_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) == 1) and (not ContinuePreventionFlag):
                    sessionstart = remember_sessionstart
                    if ((TimeHour_u(Time[sessionstart] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[sessionstart] + (TimeShiftMinutes * 60))) >= IDEndTime[intraday_i]:
                        intraday_i += 1
                        continue
                else:
                    sessionstart = remember_sessionend
                    while sessionstart < rates_total and ((((TimeHour_u(Time[sessionstart] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[sessionstart] + (TimeShiftMinutes * 60))) >= IDStartTime[intraday_i] and (TimeDayOfYear_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == TimeDayOfYear_u(Time[remember_sessionend] + (TimeShiftMinutes * 60)) or TimeDayOfYear_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == TimeDayOfYear_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)))) or (SaturdaySunday == Append_Saturday_Sunday and TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 6)):
                        sessionstart += 1
                    sessionstart -= 1
                sessionlength = 0
                if SaturdaySunday == Append_Saturday_Sunday and TimeDayOfWeek_u(Time[sessionend] + (TimeShiftMinutes * 60)) == 6:
                    pass
                elif SaturdaySunday == Append_Saturday_Sunday and TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 0:
                    while (sessionend < rates_total and TimeDayOfWeek_u(Time[sessionend] + (TimeShiftMinutes * 60)) == 1) and ((TimeHour_u(Time[sessionend] + (TimeShiftMinutes * 60)) * 60) + TimeMinute_u(Time[sessionend] + (TimeShiftMinutes * 60))) >= IDEndTime[intraday_i]:
                        sessionend += 1
                elif SaturdaySunday == Ignore_Saturday_Sunday and TimeDayOfWeek_u(Time[remember_sessionstart] + (TimeShiftMinutes * 60)) == 5:
                    sessionend = remember_sessionend
                else:
                    sessionend = sessionstart
                    sessionlength = ((24 * 60) - IDStartTime[intraday_i] + IDEndTime[intraday_i]) * 60
                    if (SaturdaySunday == Ignore_Saturday_Sunday and TimeDayOfWeek_u(Time[sessionstart] + (TimeShiftMinutes * 60)) == 1) and (not ContinuePreventionFlag):
                        sessionlength -= ((24 * 60) - IDStartTime[intraday_i]) * 60
                    while sessionend >= 0 and (Time[sessionend] - Time[sessionstart]) < sessionlength:
                        sessionend -= 1
                    sessionend += 1
            else:
                intraday_i += 1
                continue
            if sessionend == sessionstart:
                intraday_i += 1
                continue
            if not ProcessSession(sessionstart, sessionend, i, High, Low, Time, rates_total):
                return False
        intraday_i += 1
    Suffix = '_ID'
    return True

def TimeHour_u(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    return dt.hour

def TimeMinute_u(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    return dt.min

def TimeDay_u(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    return dt.day

def TimeDayOfWeek_u(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    return dt.day_of_week

def TimeDayOfYear_u(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    return dt.day_of_year

def TimeMonth_u(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    return dt.mon

def TimeYear_u(time):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    return dt.year

def TimeAbsoluteDay(time):
    return _idiv(_int(time), 86400)

def CheckRays():
    i = 0
    while i < SessionsNumber:
        last_name = ' ' + TimeToString(RememberSessionStart[i])
        suffix = RememberSessionSuffix[i]
        rec_name = ''
        if Session == Rectangle:
            rec_name = MPR_Array[i].name + '_'
        if HideRaysFromInvisibleSessions and SinglePrintRays:
            obj_total = ObjectsTotal(ChartID(), 0, OBJ_TREND)
            for j in range(0, obj_total):
                obj_name = ObjectName(ChartID(), j, 0, OBJ_TREND)
                if StringSubstr(obj_name, 0, StringLen(rec_name + 'MPSPR' + suffix + last_name)) != (rec_name + 'MPSPR' + suffix + last_name):
                    continue
                if iTime(Symbol(), Period(), _int(ChartGetInteger(ChartID(), CHART_FIRST_VISIBLE_BAR))) >= RememberSessionStart[i]:
                    ObjectSetInteger(ChartID(), obj_name, OBJPROP_COLOR, clrNONE)
                else:
                    ObjectSetInteger(ChartID(), obj_name, OBJPROP_COLOR, SinglePrintColor)
        if (((ShowMedianRays == AllPrevious and (SessionsNumber - i) >= 2) or ((ShowMedianRays == Previous or ShowMedianRays == PreviousCurrent) and (SessionsNumber - i) == 2)) or ((ShowMedianRays == Current or ShowMedianRays == PreviousCurrent) and (SessionsNumber - i) == 1)) or ShowMedianRays == All:
            median_price = ObjectGetDouble(0, rec_name + 'Median' + suffix + last_name, OBJPROP_PRICE, 0)
            median_time = ObjectGetInteger(0, rec_name + 'Median' + suffix + last_name, OBJPROP_TIME, 1)
            if not (HideRaysFromInvisibleSessions and iTime(Symbol(), Period(), _int(ChartGetInteger(ChartID(), CHART_FIRST_VISIBLE_BAR))) >= median_time):
                if ObjectFind(ChartID(), rec_name + 'Median Ray' + suffix + last_name) < 0:
                    ObjectCreate(0, rec_name + 'Median Ray' + suffix + last_name, OBJ_TREND, 0, RememberSessionStart[i], median_price, median_time, median_price)
                    ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_COLOR, MedianColor)
                    ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_STYLE, MedianRayStyle)
                    ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_WIDTH, MedianRayWidth)
                    ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_BACK, False)
                    ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_SELECTABLE, False)
                    if (RightToLeft and i == (SessionsNumber - 1)) and Session != Rectangle:
                        ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_RAY_LEFT, True)
                        ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_RAY_RIGHT, False)
                    else:
                        ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_RAY_RIGHT, True)
                        ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_RAY_LEFT, False)
                    ObjectSetInteger(0, rec_name + 'Median Ray' + suffix + last_name, OBJPROP_HIDDEN, True)
                else:
                    ObjectMove(ChartID(), rec_name + 'Median Ray' + suffix + last_name, 0, RememberSessionStart[i], median_price)
                    ObjectMove(ChartID(), rec_name + 'Median Ray' + suffix + last_name, 1, median_time, median_price)
            else:
                ObjectDelete(0, rec_name + 'Median Ray' + suffix + last_name)
        if ((ShowMedianRays == Previous or ShowMedianRays == PreviousCurrent) and (SessionsNumber - i) > 2) or (ShowMedianRays == Current and (SessionsNumber - i) > 1):
            ObjectDelete(0, rec_name + 'Median Ray' + suffix + last_name)
        if (((ShowValueAreaRays == AllPrevious and (SessionsNumber - i) >= 2) or ((ShowValueAreaRays == Previous or ShowValueAreaRays == PreviousCurrent) and (SessionsNumber - i) == 2)) or ((ShowValueAreaRays == Current or ShowValueAreaRays == PreviousCurrent) and (SessionsNumber - i) == 1)) or ShowValueAreaRays == All:
            va_high_price = ObjectGetDouble(0, rec_name + 'VA_Top' + suffix + last_name, OBJPROP_PRICE, 0)
            va_low_price = ObjectGetDouble(0, rec_name + 'VA_Bottom' + suffix + last_name, OBJPROP_PRICE, 0)
            va_time = ObjectGetInteger(0, rec_name + 'VA_Top' + suffix + last_name, OBJPROP_TIME, 1)
            if not (HideRaysFromInvisibleSessions and iTime(Symbol(), Period(), _int(ChartGetInteger(ChartID(), CHART_FIRST_VISIBLE_BAR))) >= va_time):
                if ObjectFind(ChartID(), rec_name + 'Value Area HighRay' + suffix + last_name) < 0:
                    ObjectCreate(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJ_TREND, 0, RememberSessionStart[i], va_high_price, va_time, va_high_price)
                    ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_COLOR, ValueAreaHighLowColor)
                    ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_STYLE, ValueAreaRayHighLowStyle)
                    ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_WIDTH, ValueAreaRayHighLowWidth)
                    ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_BACK, False)
                    ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_SELECTABLE, False)
                    if (RightToLeft and i == (SessionsNumber - 1)) and Session != Rectangle:
                        ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_RAY_RIGHT, False)
                        ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_RAY_LEFT, True)
                    else:
                        ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_RAY_RIGHT, True)
                        ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_RAY_LEFT, False)
                    ObjectSetInteger(0, rec_name + 'Value Area HighRay' + suffix + last_name, OBJPROP_HIDDEN, True)
                else:
                    ObjectMove(ChartID(), rec_name + 'Value Area HighRay' + suffix + last_name, 0, RememberSessionStart[i], va_high_price)
                    ObjectMove(ChartID(), rec_name + 'Value Area HighRay' + suffix + last_name, 1, va_time, va_high_price)
                if ObjectFind(ChartID(), rec_name + 'Value Area LowRay' + suffix + last_name) < 0:
                    ObjectCreate(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJ_TREND, 0, RememberSessionStart[i], va_low_price, va_time, va_low_price)
                    ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_COLOR, ValueAreaHighLowColor)
                    ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_STYLE, ValueAreaRayHighLowStyle)
                    ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_WIDTH, ValueAreaRayHighLowWidth)
                    ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_BACK, False)
                    ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_SELECTABLE, False)
                    if (RightToLeft and i == (SessionsNumber - 1)) and Session != Rectangle:
                        ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_RAY_RIGHT, False)
                        ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_RAY_LEFT, True)
                    else:
                        ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_RAY_RIGHT, True)
                        ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_RAY_LEFT, False)
                    ObjectSetInteger(0, rec_name + 'Value Area LowRay' + suffix + last_name, OBJPROP_HIDDEN, True)
                else:
                    ObjectMove(ChartID(), rec_name + 'Value Area LowRay' + suffix + last_name, 0, RememberSessionStart[i], va_low_price)
                    ObjectMove(ChartID(), rec_name + 'Value Area LowRay' + suffix + last_name, 1, va_time, va_low_price)
            else:
                ObjectDelete(0, rec_name + 'Value Area HighRay' + suffix + last_name)
                ObjectDelete(0, rec_name + 'Value Area LowRay' + suffix + last_name)
        if ((ShowValueAreaRays == Previous or ShowValueAreaRays == PreviousCurrent) and (SessionsNumber - i) > 2) or (ShowValueAreaRays == Current and (SessionsNumber - i) > 1):
            ObjectDelete(0, rec_name + 'Value Area HighRay' + suffix + last_name)
            ObjectDelete(0, rec_name + 'Value Area LowRay' + suffix + last_name)
        if RaysUntilIntersection != Stop_No_Rays:
            if ((ShowMedianRays == Previous or ShowMedianRays == PreviousCurrent) and (SessionsNumber - i) == 2) or ((ShowMedianRays == AllPrevious or ShowMedianRays == All) and (SessionsNumber - i) >= 2):
                if (RaysUntilIntersection == Stop_All_Rays or (RaysUntilIntersection == Stop_All_Rays_Except_Prev_Session and (SessionsNumber - i) > 2)) or (RaysUntilIntersection == Stop_Only_Previous_Session and (SessionsNumber - i) == 2):
                    CheckRayIntersections(rec_name + 'Median Ray' + suffix + last_name, i + 1)
            if ((ShowValueAreaRays == Previous or ShowValueAreaRays == PreviousCurrent) and (SessionsNumber - i) == 2) or ((ShowValueAreaRays == AllPrevious or ShowValueAreaRays == All) and (SessionsNumber - i) >= 2):
                if (RaysUntilIntersection == Stop_All_Rays or (RaysUntilIntersection == Stop_All_Rays_Except_Prev_Session and (SessionsNumber - i) > 2)) or (RaysUntilIntersection == Stop_Only_Previous_Session and (SessionsNumber - i) == 2):
                    CheckRayIntersections(rec_name + 'Value Area HighRay' + suffix + last_name, i + 1)
                    CheckRayIntersections(rec_name + 'Value Area LowRay' + suffix + last_name, i + 1)
        if AlertArrows:
            bar_start = iBarShift(Symbol(), Period(), RememberSessionEnd[i]) - 1
            if AlertForSinglePrint:
                obj_total = ObjectsTotal(ChartID(), 0, OBJ_TREND)
                for j in range(0, obj_total):
                    obj_name = ObjectName(ChartID(), j, 0, OBJ_TREND)
                    obj_prefix = rec_name + 'MPSPR' + suffix + last_name
                    if StringSubstr(obj_name, 0, StringLen(obj_prefix)) != obj_prefix:
                        continue
                    if _uint(ObjectGetInteger(ChartID(), obj_name, OBJPROP_COLOR)) != clrNONE:
                        if not FindAtLeastOneArrowForRay(obj_prefix):
                            for k in range(bar_start, 0 - 1, -1):
                                CheckAndDrawArrow(k, ObjectGetDouble(ChartID(), obj_name, OBJPROP_PRICE, 0), obj_prefix)
                    else:
                        DeleteArrowsByPrefix(obj_prefix)
            if AlertForValueArea:
                obj_prefix = rec_name + 'Value Area HighRay' + suffix + last_name
                if ObjectFind(ChartID(), obj_prefix) >= 0:
                    if not FindAtLeastOneArrowForRay(obj_prefix):
                        CheckHistoricalArrowsForNonMPSPRRays(bar_start, obj_prefix)
                else:
                    DeleteArrowsByPrefix(obj_prefix)
                obj_prefix = rec_name + 'Value Area LowRay' + suffix + last_name
                if ObjectFind(ChartID(), obj_prefix) >= 0:
                    if not FindAtLeastOneArrowForRay(obj_prefix):
                        CheckHistoricalArrowsForNonMPSPRRays(bar_start, obj_prefix)
                else:
                    DeleteArrowsByPrefix(obj_prefix)
            if AlertForMedian:
                obj_prefix = rec_name + 'Median Ray' + suffix + last_name
                if ObjectFind(ChartID(), obj_prefix) >= 0:
                    if not FindAtLeastOneArrowForRay(obj_prefix):
                        CheckHistoricalArrowsForNonMPSPRRays(bar_start, obj_prefix)
                else:
                    DeleteArrowsByPrefix(obj_prefix)
        i += 1

def DeleteArrowsByPrefix(prefix):
    ObjectsDeleteAll(ChartID(), 'ArrCC' + prefix, 0, OBJ_ARROW)
    ObjectsDeleteAll(ChartID(), 'ArrGC' + prefix, 0, OBJ_ARROW)
    ObjectsDeleteAll(ChartID(), 'ArrPB' + prefix, 0, OBJ_ARROW)

def FindAtLeastOneArrowForRay(ray_name):
    objects_total = ObjectsTotal(ChartID(), 0, OBJ_ARROW)
    for i in range(0, objects_total):
        obj_name = ObjectName(ChartID(), i, 0, OBJ_ARROW)
        if StringFind(obj_name, ray_name) != -1:
            return True
    return False

def CheckHistoricalArrowsForNonMPSPRRays(bar_start, ray_name):
    end_bar = 0
    if ObjectGetInteger(ChartID(), ray_name, OBJPROP_RAY_RIGHT) != True:
        end_time = ObjectGetInteger(ChartID(), ray_name, OBJPROP_TIME, 1)
        end_bar = iBarShift(Symbol(), Period(), end_time) + 1
    for k in range(bar_start, end_bar - 1, -1):
        CheckAndDrawArrow(k, ObjectGetDouble(ChartID(), ray_name, OBJPROP_PRICE, 0), ray_name)

def CheckAndDrawArrow(n, level, ray_name):
    if AlertOnPriceBreak:
        if ((iHigh(Symbol(), Period(), n) >= level and iClose(Symbol(), Period(), n) < level) and iClose(Symbol(), Period(), n + 1) < level) or ((iLow(Symbol(), Period(), n) <= level and iClose(Symbol(), Period(), n) > level) and iClose(Symbol(), Period(), n + 1) > level):
            obj_name = 'ArrPB' + ray_name
            CreateArrowObject(obj_name, iTime(Symbol(), Period(), n), iClose(Symbol(), Period(), n), AlertArrowCodePB, AlertArrowColorPB, AlertArrowWidthPB, 'Price Break')
    if AlertOnCandleClose:
        if (iClose(Symbol(), Period(), n) >= level and iClose(Symbol(), Period(), n + 1) < level) or (iClose(Symbol(), Period(), n) <= level and iClose(Symbol(), Period(), n + 1) > level):
            obj_name = 'ArrCC' + ray_name
            CreateArrowObject(obj_name, iTime(Symbol(), Period(), n), iClose(Symbol(), Period(), n), AlertArrowCodeCC, AlertArrowColorCC, AlertArrowWidthCC, 'Candle Close')
    if AlertOnGapCross:
        if (iLow(Symbol(), Period(), n) > level and iHigh(Symbol(), Period(), n + 1) < level) or (iLow(Symbol(), Period(), n + 1) > level and iHigh(Symbol(), Period(), n) < level):
            obj_name = 'ArrGC' + ray_name
            CreateArrowObject(obj_name, iTime(Symbol(), Period(), n), level, AlertArrowCodeGC, AlertArrowColorGC, AlertArrowWidthGC, 'Gap Cross')

def CreateArrowObject(name, time, price, code, colour, width, tooltip):
    global ArrowsCounter
    obj_name = name + IntegerToString(ArrowsCounter)
    ArrowsCounter += 1
    ObjectCreate(ChartID(), obj_name, OBJ_ARROW, 0, time, price)
    ObjectSetInteger(ChartID(), obj_name, OBJPROP_ARROWCODE, code)
    ObjectSetInteger(ChartID(), obj_name, OBJPROP_COLOR, colour)
    ObjectSetInteger(ChartID(), obj_name, OBJPROP_ANCHOR, ANCHOR_CENTER)
    ObjectSetInteger(ChartID(), obj_name, OBJPROP_WIDTH, width)
    ObjectSetString(ChartID(), obj_name, OBJPROP_TOOLTIP, tooltip)

def CheckRayIntersections(object_, start_j):
    if ObjectFind(0, object_) < 0:
        return
    price = ObjectGetDouble(0, object_, OBJPROP_PRICE, 0)
    for j in range(start_j, SessionsNumber):
        if price <= RememberSessionMax[j] and price >= RememberSessionMin[j]:
            ObjectSetInteger(0, object_, OBJPROP_RAY_RIGHT, False)
            ObjectSetInteger(0, object_, OBJPROP_TIME, 1, RememberSessionStart[j])
            break

def ValuePrintOut(obj_name, time, price, anchor=ANCHOR_RIGHT):
    if ObjectFind(0, obj_name) >= 0:
        ObjectMove(0, obj_name, 0, time, price)
    else:
        ObjectCreate(0, obj_name, OBJ_TEXT, 0, time, price)
        ObjectSetInteger(0, obj_name, OBJPROP_COLOR, KeyValuesColor)
        ObjectSetInteger(0, obj_name, OBJPROP_FONTSIZE, KeyValuesSize)
        ObjectSetInteger(0, obj_name, OBJPROP_BACK, False)
        ObjectSetInteger(0, obj_name, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, obj_name, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, obj_name, OBJPROP_ANCHOR, anchor)
    ObjectSetString(0, obj_name, OBJPROP_TEXT, DoubleToString(price, Digits()))

def CalculateProperColor():
    colour = 0
    _sw2 = CurrentColorScheme
    if _sw2 == Blue_to_Red:
        if CurrentBarDirection == Bullish:
            colour = clrBlue
        elif CurrentBarDirection == Bearish:
            colour = clrDarkRed
        elif CurrentBarDirection == Neutral:
            colour = clrPink
    elif _sw2 == Red_to_Green:
        if CurrentBarDirection == Bullish:
            colour = clrDarkRed
        elif CurrentBarDirection == Bearish:
            colour = clrDarkGreen
        elif CurrentBarDirection == Neutral:
            colour = clrBrown
    elif _sw2 == Green_to_Blue:
        if CurrentBarDirection == Bullish:
            colour = clrDarkGreen
        elif CurrentBarDirection == Bearish:
            colour = clrBlue
        elif CurrentBarDirection == Neutral:
            colour = clrDarkGray
    elif _sw2 == Yellow_to_Cyan:
        if CurrentBarDirection == Bullish:
            colour = clrYellow
        elif CurrentBarDirection == Bearish:
            colour = clrCyan
        elif CurrentBarDirection == Neutral:
            colour = clrGreen
    elif _sw2 == Magenta_to_Yellow:
        if CurrentBarDirection == Bullish:
            colour = clrMagenta
        elif CurrentBarDirection == Bearish:
            colour = clrYellow
        elif CurrentBarDirection == Neutral:
            colour = clrGreen
    elif _sw2 == Cyan_to_Magenta:
        if CurrentBarDirection == Bullish:
            colour = clrCyan
        elif CurrentBarDirection == Bearish:
            colour = clrMagenta
        elif CurrentBarDirection == Neutral:
            colour = clrGreen
    elif _sw2 == Single_Color:
        if CurrentBarDirection == Bullish:
            colour = SingleColor
        elif CurrentBarDirection == Bearish:
            colour = _uint(0x00FFFFFF - SingleColor)
        elif CurrentBarDirection == Neutral:
            colour = _uint(_idiv(_int(MathMax(SingleColor, 0x00FFFFFF - SingleColor)), 2))
    else:
        if CurrentBarDirection == Bullish:
            colour = SingleColor
        elif CurrentBarDirection == Bearish:
            colour = _uint(0x00FFFFFF - SingleColor)
        elif CurrentBarDirection == Neutral:
            colour = _uint(_idiv(_int(MathMax(SingleColor, 0x00FFFFFF - SingleColor)), 2))
    return colour

def OnTimer():
    global FirstRunDone, LastRecalculationTime, _s_OnTimer_prev_converted_time
    if (GetTickCount() - LastRecalculationTime) < 500:
        return
    High = Arr(0, 0.0)
    Low = Arr(0, 0.0)
    Time = Arr(0, 0)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Time, True)
    rates_total = iBars(Symbol(), Period())
    h = CopyHigh(Symbol(), Period(), 0, rates_total, High)
    l = CopyLow(Symbol(), Period(), 0, rates_total, Low)
    t = CopyTime(Symbol(), Period(), 0, rates_total, Time)
    if (h <= 0 or l <= 0) or t <= 0:
        return
    if HideRaysFromInvisibleSessions:
        CheckRays()
    if Session == Rectangle:
        CheckRectangles(High, Low, Time, rates_total)
        return
    if (RightToLeft and (not SeamlessScrollingMode)) or (not FirstRunDone):
        return
    converted_time = Box(0)
    dummy_subwindow = Box(0)
    dummy_price = Box(0.0)
    ChartXYToTimePrice(0, _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)), 0, dummy_subwindow, converted_time, dummy_price)
    if converted_time.v == _s_OnTimer_prev_converted_time:
        return
    _s_OnTimer_prev_converted_time = converted_time.v
    if SeamlessScrollingMode:
        ObjectCleanup()
        if Session == Intraday:
            FirstRunDone = False
        if EnableDevelopingPOC or EnableDevelopingVAHVAL:
            i = 0
            while i < Bars(Symbol(), Period()):
                DevelopingPOC_1[i] = EMPTY_VALUE
                DevelopingPOC_2[i] = EMPTY_VALUE
                DevelopingVAH_1[i] = EMPTY_VALUE
                DevelopingVAH_2[i] = EMPTY_VALUE
                DevelopingVAL_1[i] = EMPTY_VALUE
                DevelopingVAL_2[i] = EMPTY_VALUE
                i += 1
    RedrawLastSession(High, Low, Time, rates_total)
    if SeamlessScrollingMode and Session == Intraday:
        FirstRunDone = True
    LastRecalculationTime = GetTickCount()
    ChartRedraw()

def CheckRectangles(High, Low, Time, rates_total):
    global LastRecalculationTime, SessionsNumber, mpr_total
    for i in range(mpr_total - 1, 0 - 1, -1):
        if ObjectFind(0, MPR_Array[i].name) < 0:
            ObjectCleanup(MPR_Array[i].name + '_')
            if EnableDevelopingPOC or EnableDevelopingVAHVAL:
                sessionstart = iBarShift(Symbol(), Period(), MPR_Array[i].RectangleTimeMin, True)
                sessionend = iBarShift(Symbol(), Period(), MPR_Array[i].RectangleTimeMax, True)
                if sessionend < 0:
                    sessionend = 0
                for j in range(sessionstart, sessionend - 1, -1):
                    DevelopingPOC_1[j] = EMPTY_VALUE
                    DevelopingPOC_2[j] = EMPTY_VALUE
                    DevelopingVAH_1[j] = EMPTY_VALUE
                    DevelopingVAH_2[j] = EMPTY_VALUE
                    DevelopingVAL_1[j] = EMPTY_VALUE
                    DevelopingVAL_2[j] = EMPTY_VALUE
            _delete(MPR_Array[i])
            for j in range(i, mpr_total - 1):
                MPR_Array[j] = MPR_Array[j + 1]
            mpr_total -= 1
            ArrayResize(MPR_Array, mpr_total)
    obj_total = ObjectsTotal(ChartID(), -1, OBJ_RECTANGLE)
    for i in range(0, obj_total):
        name = ObjectName(ChartID(), i, -1, OBJ_RECTANGLE)
        if StringSubstr(name, 0, 3) != 'MPR':
            continue
        if StringFind(name, '_') != -1:
            continue
        name_found = False
        for j in range(0, mpr_total):
            if MPR_Array[j].name == name:
                name_found = True
                t1 = ObjectGetInteger(0, name, OBJPROP_TIME, 0)
                t2 = ObjectGetInteger(0, name, OBJPROP_TIME, 1)
                MPR_Array[j].t1 = t1
                MPR_Array[j].t2 = t2
                if mpr_total == 1:
                    continue
                t1 = MathMin(t1, t2)
                if t1 == MPR_Array[j].RectangleTimeMin:
                    continue
                k = 0
                if k == j:
                    k += 1
                while k < mpr_total and MPR_Array[k].RectangleTimeMin < t1:
                    k += 1
                    if k == j:
                        k += 1
                if j == (k - 1):
                    continue
                tmp = MPR_Array[j]
                if t1 > MPR_Array[j].RectangleTimeMin:
                    for n in range(j, k - 1):
                        MPR_Array[n] = MPR_Array[n + 1]
                    MPR_Array[k - 1] = tmp
                else:
                    for n in range(j, k, -1):
                        MPR_Array[n] = MPR_Array[n - 1]
                    MPR_Array[k] = tmp
                break
        if not name_found:
            t1 = ObjectGetInteger(0, name, OBJPROP_TIME, 0)
            t2 = ObjectGetInteger(0, name, OBJPROP_TIME, 1)
            t = MathMin(t1, t2)
            k = 0
            while k < mpr_total and MPR_Array[k].RectangleTimeMin < t:
                k += 1
            mpr_total += 1
            ArrayResize(MPR_Array, mpr_total)
            for n in range(mpr_total - 1, k, -1):
                MPR_Array[n] = MPR_Array[n - 1]
            MPR_Array[k] = CRectangleMP(name)
            MPR_Array[k].RectangleTimeMin = t
            MPR_Array[k].t1 = t1
            MPR_Array[k].t2 = t2
    if SessionsNumber != mpr_total:
        SessionsNumber = mpr_total
        ArrayResize(RememberSessionMax, SessionsNumber)
        ArrayResize(RememberSessionMin, SessionsNumber)
        ArrayResize(RememberSessionStart, SessionsNumber)
        ArrayResize(RememberSessionSuffix, SessionsNumber)
        ArrayResize(RememberSessionEnd, SessionsNumber)
    i = 0
    while i < mpr_total:
        MPR_Array[i].Process(i, High, Low, Time, rates_total)
        i += 1
    if (ShowValueAreaRays != None_ or ShowMedianRays != None_) or (HideRaysFromInvisibleSessions and SinglePrintRays):
        CheckRays()
    LastRecalculationTime = GetTickCount()
    ChartRedraw()

def PutSinglePrintMark(price, sessionstart, rectangle_prefix, Time):
    t1 = sessionstart + 1
    t2 = sessionstart
    fill = True
    if ShowSinglePrint == Rightside:
        t1 = sessionstart
        t2 = sessionstart - 1
        fill = False
    LastNameStart = ' ' + TimeToString(Time[t1]) + ' '
    LastName = LastNameStart + DoubleToString(price, Digits())
    if ObjectFind(0, rectangle_prefix + 'MPSP' + Suffix + LastName) >= 0:
        return
    ObjectCreate(0, rectangle_prefix + 'MPSP' + Suffix + LastName, OBJ_RECTANGLE, 0, Time[t1], price, Time[t2], price - onetick)
    ObjectSetInteger(0, rectangle_prefix + 'MPSP' + Suffix + LastName, OBJPROP_COLOR, SinglePrintColor)
    ObjectSetInteger(0, rectangle_prefix + 'MPSP' + Suffix + LastName, OBJPROP_FILL, fill)
    ObjectSetInteger(0, rectangle_prefix + 'MPSP' + Suffix + LastName, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, rectangle_prefix + 'MPSP' + Suffix + LastName, OBJPROP_HIDDEN, True)

def RemoveSinglePrintMark(price, sessionstart, rectangle_prefix, Time):
    t = sessionstart + 1
    if ShowSinglePrint == Rightside:
        t = sessionstart
    LastNameStart = ' ' + TimeToString(Time[t]) + ' '
    LastName = LastNameStart + DoubleToString(price, Digits())
    ObjectDelete(0, rectangle_prefix + 'MPSP' + Suffix + LastName)

def PutSinglePrintRay(price, sessionstart, rectangle_prefix, Time, spr_color):
    t1 = Time[sessionstart]
    t2 = 0
    if (sessionstart - 1) >= 0:
        t2 = Time[sessionstart - 1]
    else:
        t2 = Time[sessionstart] + 1
    if ShowSinglePrint == Rightside:
        t1 = Time[sessionstart]
        t2 = Time[sessionstart + 1]
    LastNameStart = ' ' + TimeToString(t1) + ' '
    LastName = LastNameStart + DoubleToString(price, Digits())
    if ObjectFind(0, rectangle_prefix + 'MPSPR' + Suffix + LastName) >= 0:
        return
    ObjectCreate(0, rectangle_prefix + 'MPSPR' + Suffix + LastName, OBJ_TREND, 0, t1, price, t2, price)
    ObjectSetInteger(0, rectangle_prefix + 'MPSPR' + Suffix + LastName, OBJPROP_COLOR, spr_color)
    ObjectSetInteger(0, rectangle_prefix + 'MPSPR' + Suffix + LastName, OBJPROP_STYLE, SinglePrintRayStyle)
    ObjectSetInteger(0, rectangle_prefix + 'MPSPR' + Suffix + LastName, OBJPROP_WIDTH, SinglePrintRayWidth)
    ObjectSetInteger(0, rectangle_prefix + 'MPSPR' + Suffix + LastName, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(0, rectangle_prefix + 'MPSPR' + Suffix + LastName, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, rectangle_prefix + 'MPSPR' + Suffix + LastName, OBJPROP_HIDDEN, True)

def RemoveSinglePrintRay(price, sessionstart, rectangle_prefix, Time):
    t = Time[sessionstart]
    LastNameStart = ' ' + TimeToString(t) + ' '
    LastName = LastNameStart + DoubleToString(price, Digits())
    ObjectDelete(0, rectangle_prefix + 'MPSPR' + Suffix + LastName)

def RedrawLastSession(High, Low, Time, rates_total):
    global Max_number_of_bars_in_a_session, SessionsNumber, StartDate
    if SeamlessScrollingMode:
        last_visible_bar = _int(ChartGetInteger(ChartID(), CHART_FIRST_VISIBLE_BAR)) - _int(ChartGetInteger(ChartID(), CHART_WIDTH_IN_BARS)) + 1
        if last_visible_bar < 0:
            last_visible_bar = 0
        StartDate = Time[last_visible_bar]
    elif StartFromCurrentSession:
        StartDate = Time[0]
    else:
        StartDate = StartFromDate
    sessionend = FindSessionEndByDate(Time, StartDate, rates_total)
    sessionstart = FindSessionStart(Time, sessionend, rates_total)
    if sessionstart == -1:
        Print('Something went wrong! Waiting for data to load.')
        return
    SessionToStart = 0
    if not SeamlessScrollingMode:
        SessionToStart = _SessionsToCount - 1
    else:
        i = 1
        while i < _SessionsToCount:
            sessionend = sessionstart + 1
            if sessionend >= Bars(Symbol(), Period()):
                return
            if SaturdaySunday == Ignore_Saturday_Sunday:
                while TimeDayOfWeek_u(Time[sessionend]) == 0 or TimeDayOfWeek_u(Time[sessionend]) == 6:
                    sessionend += 1
                    if sessionend >= Bars(Symbol(), Period()):
                        break
            sessionstart = FindSessionStart(Time, sessionend, rates_total)
            i += 1
        SessionsNumber = 0
    i = SessionToStart
    while i < _SessionsToCount:
        if Session == Intraday:
            if not ProcessIntradaySession(sessionstart, sessionend, i, High, Low, Time, rates_total):
                return
        else:
            if Session == Daily:
                Max_number_of_bars_in_a_session = _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds())
            elif Session == Weekly:
                Max_number_of_bars_in_a_session = _idiv(604800, PeriodSeconds())
            elif Session == Monthly:
                Max_number_of_bars_in_a_session = _idiv(2678400, PeriodSeconds())
            if SaturdaySunday == Append_Saturday_Sunday:
                if TimeDayOfWeek_u(Time[sessionstart]) == 0:
                    Max_number_of_bars_in_a_session += _idiv((24 * 3600) - ((TimeHour_u(Time[sessionstart]) * 3600) + (TimeMinute_u(Time[sessionstart]) * 60)), PeriodSeconds())
                if TimeDayOfWeek_u(Time[sessionend]) == 6:
                    Max_number_of_bars_in_a_session += _idiv((TimeHour_u(Time[sessionend]) * 3600) + (TimeMinute_u(Time[sessionend]) * 60), PeriodSeconds()) + 1
            if not ProcessSession(sessionstart, sessionend, i, High, Low, Time, rates_total):
                return
        if (_SessionsToCount - i) > 1:
            sessionstart = sessionend - 1
            if SaturdaySunday == Ignore_Saturday_Sunday:
                while TimeDayOfWeek_u(Time[sessionstart]) == 0 or TimeDayOfWeek_u(Time[sessionstart]) == 6:
                    sessionstart -= 1
                    if sessionstart == 0:
                        break
            sessionend = FindSessionEndByDate(Time, Time[sessionstart], Bars(Symbol(), Period()))
        i += 1
    if (ShowValueAreaRays != None_ or ShowMedianRays != None_) or (HideRaysFromInvisibleSessions and SinglePrintRays):
        CheckRays()

def CalculateDevelopingPOCVAHVAL(sessionstart, sessionend, High, Low, rectangle=None):
    for max_bar in range(sessionstart, sessionend - 1, -1):
        if (DevelopingPOC_1[max_bar] != EMPTY_VALUE or DevelopingPOC_2[max_bar] != EMPTY_VALUE) and max_bar > 1:
            continue
        LocalMin = Low[iLowest(Symbol(), Period(), MODE_LOW, sessionstart - max_bar + 1, max_bar)]
        LocalMax = High[iHighest(Symbol(), Period(), MODE_HIGH, sessionstart - max_bar + 1, max_bar)]
        if Session == Rectangle:
            if LocalMax > rectangle.RectanglePriceMax:
                LocalMax = NormalizeDouble(rectangle.RectanglePriceMax, DigitsM)
            if LocalMin < rectangle.RectanglePriceMin:
                LocalMin = NormalizeDouble(rectangle.RectanglePriceMin, DigitsM)
        DistanceToCenter = DBL_MAX
        DevMaxRange = 0
        PriceOfMaxRange = EMPTY_VALUE
        TotalTPO = 0
        TPOperPrice = Arr(0, 0)
        max_ = _int(MathRound(_fdiv(LocalMax - LocalMin, onetick) + 2))
        ArrayResize(TPOperPrice, max_)
        ArrayInitialize(TPOperPrice, 0)
        price = LocalMax
        while price >= LocalMin:
            price = NormalizeDouble(price, DigitsM)
            range_ = 0
            for bar in range(sessionstart, max_bar - 1, -1):
                if price >= Low[bar] and price <= High[bar]:
                    if DevMaxRange < range_ or (DevMaxRange == range_ and MathAbs(price - (LocalMin + ((LocalMax - LocalMin) / 2))) < DistanceToCenter):
                        DevMaxRange = range_
                        PriceOfMaxRange = price
                        DistanceToCenter = MathAbs(price - (LocalMin + ((LocalMax - LocalMin) / 2)))
                    index = _int(MathRound(_fdiv(price - LocalMin, onetick)))
                    TPOperPrice[index] += 1
                    TotalTPO += 1
                    range_ += 1
            price -= onetick
        if EnableDevelopingVAHVAL:
            TotalTPOdouble = TotalTPO
            ValueControlTPO = _int(MathRound(TotalTPOdouble * ValueAreaPercentage_double))
            index = _int(_fdiv(PriceOfMaxRange - LocalMin, onetick))
            if index < 0:
                continue
            TPOcount = TPOperPrice[index]
            up_offset = 1
            down_offset = 1
            while TPOcount < ValueControlTPO:
                abovePrice = PriceOfMaxRange + (up_offset * onetick)
                belowPrice = PriceOfMaxRange - (down_offset * onetick)
                index = _int(MathRound(_fdiv(abovePrice - LocalMin, onetick)))
                index2 = _int(MathRound(_fdiv(belowPrice - LocalMin, onetick)))
                if (belowPrice < LocalMin or TPOperPrice[index] >= TPOperPrice[index2]) and abovePrice <= LocalMax:
                    TPOcount += TPOperPrice[index]
                    up_offset += 1
                elif belowPrice >= LocalMin:
                    TPOcount += TPOperPrice[index2]
                    down_offset += 1
                elif TPOcount < ValueControlTPO:
                    break
            DistributeBetweenTwoBuffers(DevelopingVAH_1, DevelopingVAH_2, max_bar, PriceOfMaxRange + (up_offset * onetick))
            DistributeBetweenTwoBuffers(DevelopingVAL_1, DevelopingVAL_2, max_bar, PriceOfMaxRange - (down_offset * onetick) + onetick)
        if EnableDevelopingPOC:
            DistributeBetweenTwoBuffers(DevelopingPOC_1, DevelopingPOC_2, max_bar, PriceOfMaxRange)

def DistributeBetweenTwoBuffers(buff1, buff2, bar, price):
    if buff1[bar + 1] == EMPTY_VALUE and buff2[bar + 1] == EMPTY_VALUE:
        buff1[bar] = price
        buff2[bar] = EMPTY_VALUE
    elif buff1[bar + 1] != EMPTY_VALUE:
        if buff1[bar + 1] != price:
            buff2[bar] = price
            buff1[bar] = EMPTY_VALUE
        else:
            buff1[bar] = price
            buff2[bar] = EMPTY_VALUE
    else:
        if buff2[bar + 1] != price:
            buff1[bar] = price
            buff2[bar] = EMPTY_VALUE
        else:
            buff2[bar] = price
            buff1[bar] = EMPTY_VALUE

def OnChartEvent(id_, lparam, dparam, sparam):
    if Session != Rectangle:
        return
    if id_ == CHARTEVENT_KEYDOWN:
        if lparam == 82:
            for i in range(0, 1000):
                name = 'MPR' + IntegerToString(i)
                if ObjectFind(0, name) >= 0:
                    continue
                pixel_width = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS))
                pixel_height = _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS))
                half_width = _idiv(pixel_width, 2)
                half_height = _idiv(pixel_height, 2)
                x1 = _idiv(half_width, 2)
                x2 = _int(half_width * 1.5)
                y1 = _idiv(half_height, 2)
                y2 = _int(half_height * 1.5)
                dummy_subwindow = Box(0)
                time1 = Box(0)
                time2 = Box(0)
                price1 = Box(0.0)
                price2 = Box(0.0)
                ChartXYToTimePrice(0, x1, y1, dummy_subwindow, time1, price1)
                ChartXYToTimePrice(0, x2, y2, dummy_subwindow, time2, price2)
                ObjectCreate(0, name, OBJ_RECTANGLE, 0, time1.v, price1.v, time2.v, price2.v)
                ObjectSetInteger(0, name, OBJPROP_SELECTABLE, True)
                ObjectSetInteger(0, name, OBJPROP_HIDDEN, False)
                ObjectSetInteger(0, name, OBJPROP_SELECTED, True)
                ObjectSetInteger(0, name, OBJPROP_FILL, False)
                break

def CheckAlerts(Open, High, Low, Close, Time):
    global Close_prev, LastAlertTime
    if (((not AlertNative) and (not AlertEmail)) and (not AlertPush)) and (not AlertArrows):
        return
    if ((not AlertForMedian) and (not AlertForValueArea)) and (not AlertForSinglePrint):
        return
    if ((not AlertOnPriceBreak) and (not AlertOnCandleClose)) and (not AlertOnGapCross):
        return
    if AlertCheckBar == CheckPreviousBar and LastAlertTime == Time[0]:
        return
    obj_total = ObjectsTotal(ChartID(), -1, OBJ_TREND)
    for i in range(0, obj_total):
        object_name = ObjectName(ChartID(), i, -1, OBJ_TREND)
        if not (((AlertForMedian and StringFind(object_name, 'Median Ray') > -1) or (AlertForValueArea and (StringFind(object_name, 'Value Area HighRay') > -1 or StringFind(object_name, 'Value Area LowRay') > -1))) or ((AlertForSinglePrint and StringFind(object_name, 'MPSPR') > -1) and _uint(ObjectGetInteger(ChartID(), object_name, OBJPROP_COLOR)) != clrNONE)):
            continue
        level = NormalizeDouble(ObjectGetDouble(ChartID(), object_name, OBJPROP_PRICE, 0), Digits())
        if AlertCheckBar == CheckCurrentBar:
            if AlertOnPriceBreak:
                if Close_prev != EMPTY_VALUE and ((Close[0] >= level and Close_prev < level) or (Close[0] <= level and Close_prev > level)):
                    DoAlerts(PriceBreak, object_name)
                    if AlertArrows:
                        CreateArrowObject('ArrPB' + object_name, Time[0], Close[0], AlertArrowCodePB, AlertArrowColorPB, AlertArrowWidthPB, 'Price Break')
                Close_prev = Close[0]
            if AlertOnCandleClose:
                if (Close[0] >= level and Close[1] < level) or (Close[0] <= level and Close[1] > level):
                    DoAlerts(CandleCloseCrossover, object_name)
                    if AlertArrows:
                        CreateArrowObject('ArrCC' + object_name, Time[0], Close[0], AlertArrowCodeCC, AlertArrowColorCC, AlertArrowWidthCC, 'Candle Close')
            if AlertOnGapCross:
                if (Open[0] > level and High[1] < level) or (Open[0] < level and Low[1] > level):
                    DoAlerts(GapCrossover, object_name)
                    if AlertArrows:
                        CreateArrowObject('ArrGC' + object_name, Time[0], level, AlertArrowCodeGC, AlertArrowColorGC, AlertArrowWidthGC, 'Gap Cross')
        elif AlertCheckBar == CheckPreviousBar:
            if AlertOnPriceBreak:
                if ((High[1] >= level and Close[1] < level) and Close[2] < level) or ((Low[1] <= level and Close[1] > level) and Close[2] > level):
                    DoAlerts(PriceBreak, object_name)
                    if AlertArrows:
                        CreateArrowObject('ArrPB' + object_name, Time[1], Close[1], AlertArrowCodePB, AlertArrowColorPB, AlertArrowWidthPB, 'Price Break')
            if AlertOnCandleClose:
                if (Close[1] >= level and Close[2] < level) or (Close[1] <= level and Close[2] > level):
                    DoAlerts(CandleCloseCrossover, object_name)
                    if AlertArrows:
                        CreateArrowObject('ArrCC' + object_name, Time[1], Close[1], AlertArrowCodeCC, AlertArrowColorCC, AlertArrowWidthCC, 'Candle Close')
            if AlertOnGapCross:
                if (Low[1] > level and High[2] < level) or (Low[2] > level and High[1] < level):
                    DoAlerts(GapCrossover, object_name)
                    if AlertArrows:
                        CreateArrowObject('ArrGC' + object_name, Time[1], level, AlertArrowCodeGC, AlertArrowColorGC, AlertArrowWidthGC, 'Gap Cross')
            LastAlertTime = Time[0]

def DoAlerts(alert_type, object_name):
    global LastAlertTime_CandleCross, LastAlertTime_GapCross
    if (alert_type == CandleCloseCrossover and AlertCheckBar == CheckCurrentBar) and TimeCurrent() <= LastAlertTime_CandleCross:
        return
    if (alert_type == GapCrossover and AlertCheckBar == CheckCurrentBar) and TimeCurrent() <= LastAlertTime_GapCross:
        return
    Subject = 'Market Profile: ' + Symbol() + ' ' + EnumToString(alert_type, 'alert_types') + ' on ' + object_name
    if AlertNative:
        AlertText = Subject
        Alert(AlertText)
    if AlertEmail:
        EmailSubject = Subject
        EmailBody = AccountInfoString(ACCOUNT_COMPANY) + ' - ' + AccountInfoString(ACCOUNT_NAME) + ' - ' + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + '\r\n\r\n' + Subject
        if not SendMail(EmailSubject, EmailBody):
            Print('Error sending email: ' + IntegerToString(GetLastError()) + '.')
    if AlertPush:
        AppText = Subject
        if not SendNotification(AppText):
            Print('Error sending notification: ' + IntegerToString(GetLastError()) + '.')
    if alert_type == CandleCloseCrossover and AlertCheckBar == CheckCurrentBar:
        LastAlertTime_CandleCross = TimeCurrent()
    elif alert_type == GapCrossover and AlertCheckBar == CheckCurrentBar:
        LastAlertTime_GapCross = TimeCurrent()

# ---- static local variables
_s_PutDot_prev_time_start_bar = 0
_s_ProcessSession_PreviousSessionMax = DBL_MIN
_s_ProcessSession_PreviousSessionStartTime = 0
_s_OnTimer_prev_converted_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MarketProfile(_MQL5Indicator):
    name = 'MarketProfile'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Session': _Choice({0: 'Daily', 1: 'Weekly', 2: 'Monthly', 3: 'Intraday', 4: 'Rectangle'}, default=0),
        'StartFromCurrentSession': True,  # StartFromCurrentSession: higher priority.
        'SessionsToCount': 2,  # SessionsToCount: Number of sessions to count Market Profile.
        'SeamlessScrollingMode': False,  # SeamlessScrollingMode: Show sessions on current screen.
        'EnableDevelopingPOC': False,  # Enable Developing POC
        'EnableDevelopingVAHVAL': False,  # Enable Developing VAH/VAL
        'ValueAreaPercentage': 70,  # ValueAreaPercentage: Percentage of TPO's inside Value Area.
        'ColorScheme': _Choice({0: 'Blue to Red', 1: 'Red to Green', 2: 'Green to Blue', 3: 'Yellow to Cyan', 4: 'Magenta to Yellow', 5: 'Cyan to Magenta', 6: 'Single Color'}, default=0),
        'ColorBullBear': False,  # ColorBullBear: If true, colors are from bars' direction.
        'MedianStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'MedianRayStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),
        'ValueAreaSidesStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'ValueAreaHighLowStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'ValueAreaRayHighLowStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),
        'MedianWidth': 1,
        'MedianRayWidth': 1,
        'ValueAreaSidesWidth': 1,
        'ValueAreaHighLowWidth': 1,
        'ValueAreaRayHighLowWidth': 1,
        'ShowValueAreaRays': _Choice({0: 'None', 1: 'Previous', 2: 'Current', 3: 'Previous & Current', 4: 'All Previous', 5: 'All'}, default=0),  # ShowValueAreaRays: draw previous value area high/low rays.
        'ShowMedianRays': _Choice({0: 'None', 1: 'Previous', 2: 'Current', 3: 'Previous & Current', 4: 'All Previous', 5: 'All'}, default=0),  # ShowMedianRays: draw previous median rays.
        'RaysUntilIntersection': _Choice({0: 'Stop no rays', 1: 'Stop all rays', 2: 'Stop all rays except previous session', 3: "Stop only previous session's rays"}, default=0),  # RaysUntilIntersection: which rays stop when hit another MP.
        'HideRaysFromInvisibleSessions': False,  # HideRaysFromInvisibleSessions: hide rays from behind the screen.
        'TimeShiftMinutes': 0,  # TimeShiftMinutes: shift session + to the left, - to the right.
        'ShowKeyValues': True,  # ShowKeyValues: print out VAH, VAL, POC on chart.
        'KeyValuesSize': 8,  # KeyValuesSize: font size for VAH, VAL, POC printout.
        'ShowSinglePrint': _Choice({0: 'No', 1: 'Leftside', 2: 'Rightside'}, default=0),  # ShowSinglePrint: mark Single Print profile levels.
        'SinglePrintRays': False,  # SinglePrintRays: mark Single Print edges with rays.
        'SinglePrintRayStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'SinglePrintRayWidth': 1,
        'ProminentMedianStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'ProminentMedianWidth': 4,
        'RightToLeft': False,  # RightToLeft: Draw histogram from right to left.
        'PointMultiplier': 0,  # PointMultiplier: higher value = fewer objects. 0 - adaptive.
        'ThrottleRedraw': 0,  # ThrottleRedraw: delay (in seconds) for updating Market Profile.
        'DisableHistogram': False,  # DisableHistogram: do not draw profile, VAH, VAL, and POC still visible.
        'AlertNative': False,  # AlertNative: issue native pop-up alerts.
        'AlertEmail': False,  # AlertEmail: issue email alerts.
        'AlertPush': False,  # AlertPush: issue push-notification alerts.
        'AlertArrows': False,  # AlertArrows: draw chart arrows on alerts.
        'AlertCheckBar': _Choice({0: 'Current', 1: 'Previous'}, default=1),  # AlertCheckBar: which bar to check for alerts?
        'AlertForValueArea': False,  # AlertForValueArea: alerts for Value Area (VAH, VAL) rays.
        'AlertForMedian': False,  # AlertForMedian: alerts for POC (Median) rays' crossing.
        'AlertForSinglePrint': False,  # AlertForSinglePrint: alerts for single print rays' crossing.
        'AlertOnPriceBreak': False,  # AlertOnPriceBreak: price breaking above/below the ray.
        'AlertOnCandleClose': False,  # AlertOnCandleClose: candle closing above/below the ray.
        'AlertOnGapCross': False,  # AlertOnGapCross: bar gap above/below the ray.
        'AlertArrowCodePB': 108,  # AlertArrowCodePB: arrow code for price break alerts.
        'AlertArrowCodeCC': 110,  # AlertArrowCodeCC: arrow code for candle close alerts.
        'AlertArrowCodeGC': 117,  # AlertArrowCodeGC: arrow code for gap crossover alerts.
        'AlertArrowWidthPB': 1,  # AlertArrowWidthPB: arrow width for price break alerts.
        'AlertArrowWidthCC': 1,  # AlertArrowWidthCC: arrow width for candle close alerts.
        'AlertArrowWidthGC': 1,  # AlertArrowWidthGC: arrow width for gap crossover alerts.
        'EnableIntradaySession1': True,
        'IntradaySession1ColorScheme': _Choice({0: 'Blue to Red', 1: 'Red to Green', 2: 'Green to Blue', 3: 'Yellow to Cyan', 4: 'Magenta to Yellow', 5: 'Cyan to Magenta', 6: 'Single Color'}, default=0),
        'EnableIntradaySession2': True,
        'IntradaySession2ColorScheme': _Choice({0: 'Blue to Red', 1: 'Red to Green', 2: 'Green to Blue', 3: 'Yellow to Cyan', 4: 'Magenta to Yellow', 5: 'Cyan to Magenta', 6: 'Single Color'}, default=1),
        'EnableIntradaySession3': True,
        'IntradaySession3ColorScheme': _Choice({0: 'Blue to Red', 1: 'Red to Green', 2: 'Green to Blue', 3: 'Yellow to Cyan', 4: 'Magenta to Yellow', 5: 'Cyan to Magenta', 6: 'Single Color'}, default=2),
        'EnableIntradaySession4': True,
        'IntradaySession4ColorScheme': _Choice({0: 'Blue to Red', 1: 'Red to Green', 2: 'Green to Blue', 3: 'Yellow to Cyan', 4: 'Magenta to Yellow', 5: 'Cyan to Magenta', 6: 'Single Color'}, default=3),
        'SaturdaySunday': _Choice({0: 'Normal sessions', 1: 'Ignore Saturday and Sunday', 2: 'Append Saturday and Sunday'}, default=0),
        'DisableAlertsOnWrongTimeframes': False,  # Disable alerts on wrong timeframes.
        'ProminentMedianPercentage': 101,  # Percentage of Median TPOs out of total for a Prominent one.
    }

