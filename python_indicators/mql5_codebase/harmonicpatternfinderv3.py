"""HarmonicPatternFinderV3 — converted from MQL5: MQL5 Indicators/Harmonic Pattern Finder V3/HarmonicPatternFinderV3.mq5

Indicator to display existent and emerging harmonic chart patterns.
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.hpfmatchprocessor import *  # #include HPFMatchProcessor.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [4294967295]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Zig Zag'}, 'levels': [], 'description': ['Indicator to display existent and emerging harmonic chart patterns.'], 'name': 'HarmonicPatternFinderV3', 'source': 'MQL5 Indicators/Harmonic Pattern Finder V3/HarmonicPatternFinderV3.mq5', 'folder': 'Harmonic Pattern Finder V3', 'inputs': [{'mql': 'zigzagSettings', 'py': 'zigzagSettings', 'param': None, 'type': 'string', 'default': '-=ZigZag Settings=-', 'label': '-=ZigZag Settings=-', 'sinput': False}, {'mql': 'i_zzAtrMultiplier', 'py': 'i_zzAtrMultiplier', 'param': 'i_zzAtrMultiplier', 'type': 'double', 'default': 2.0, 'label': 'ATR ZZ atr multiplier', 'sinput': False}, {'mql': 'i_zzAtrPeriod', 'py': 'i_zzAtrPeriod', 'param': 'i_zzAtrPeriod', 'type': 'int', 'default': 50, 'label': 'ATR ZZ atr period', 'sinput': False}, {'mql': 'i_zzMaxPeriod', 'py': 'i_zzMaxPeriod', 'param': 'i_zzMaxPeriod', 'type': 'int', 'default': 10, 'label': 'ATR ZZ max period', 'sinput': False}, {'mql': 'i_zzMinPeriod', 'py': 'i_zzMinPeriod', 'param': 'i_zzMinPeriod', 'type': 'int', 'default': 3, 'label': 'ATR ZZ min period', 'sinput': False}, {'mql': 'i_zzRealtime', 'py': 'i_zzRealtime', 'param': 'i_zzRealtime', 'type': 'bool', 'default': True, 'label': 'ATR ZZ realtime', 'sinput': False}, {'mql': 'indicatorSettings', 'py': 'indicatorSettings', 'param': None, 'type': 'string', 'default': '-=Indicator Settings=-', 'label': '-=Indicator Settings=-', 'sinput': False}, {'mql': 'i_barsAnalyzed', 'py': 'i_barsAnalyzed', 'param': 'i_barsAnalyzed', 'type': 'int', 'default': 300, 'label': 'Max. bars per pattern', 'sinput': False}, {'mql': 'i_history', 'py': 'i_history', 'param': 'i_history', 'type': 'int', 'default': 1000, 'label': 'Max. history bars to process', 'sinput': False}, {'mql': 'i_maxSamePoints', 'py': 'i_maxSamePoints', 'param': 'i_maxSamePoints', 'type': 'int', 'default': 2, 'label': 'Max. shared points per pattern', 'sinput': False}, {'mql': 'i_slackRange', 'py': 'i_slackRange', 'param': 'i_slackRange', 'type': 'double', 'default': 0.05, 'label': 'Max. slack for fib ratios (range)', 'sinput': False}, {'mql': 'i_slackSingular', 'py': 'i_slackSingular', 'param': 'i_slackSingular', 'type': 'double', 'default': 0.1, 'label': 'Max. slack for fib ratios (unary)', 'sinput': False}, {'mql': 'i_tooEarly', 'py': 'i_tooEarly', 'param': 'i_tooEarly', 'type': 'double', 'default': 0.382, 'label': 'Too early timezone', 'sinput': False}, {'mql': 'i_ideal', 'py': 'i_ideal', 'param': 'i_ideal', 'type': 'double', 'default': 1.0, 'label': 'Ideal timezone', 'sinput': False}, {'mql': 'i_tooLate', 'py': 'i_tooLate', 'param': 'i_tooLate', 'type': 'double', 'default': 1.618, 'label': 'Too late timezone', 'sinput': False}, {'mql': 'i_puristPRZ', 'py': 'i_puristPRZ', 'param': 'i_puristPRZ', 'type': 'bool', 'default': False, 'label': 'Filter patterns without fib ratios in PRZ', 'sinput': False}, {'mql': 'i_timefilterEarly', 'py': 'i_timefilterEarly', 'param': 'i_timefilterEarly', 'type': 'bool', 'default': False, 'label': 'Filter too early patterns', 'sinput': False}, {'mql': 'i_timefilterLate', 'py': 'i_timefilterLate', 'param': 'i_timefilterLate', 'type': 'bool', 'default': False, 'label': 'Filter too late patterns', 'sinput': False}, {'mql': 'indicatorColors', 'py': 'indicatorColors', 'param': None, 'type': 'string', 'default': '-=Display Settings=-', 'label': '-=Display Settings=-', 'sinput': False}, {'mql': 'i_clrBull', 'py': 'i_clrBull', 'param': None, 'type': 'color', 'default': 16436871, 'label': 'Color for bullish patterns (5 points)', 'sinput': False}, {'mql': 'i_clrBear', 'py': 'i_clrBear', 'param': None, 'type': 'color', 'default': 12695295, 'label': 'Color for bearish patterns (5 points)', 'sinput': False}, {'mql': 'i_clrBull4P', 'py': 'i_clrBull4P', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Color for bullish patterns (4 points)', 'sinput': False}, {'mql': 'i_clrBear4P', 'py': 'i_clrBear4P', 'param': None, 'type': 'color', 'default': 9639167, 'label': 'Color for bearish patterns (4 points)', 'sinput': False}, {'mql': 'i_clrBullProjection', 'py': 'i_clrBullProjection', 'param': None, 'type': 'color', 'default': 5737262, 'label': 'Color for proj. bullish patterns (5P)', 'sinput': False}, {'mql': 'i_clrBearProjection', 'py': 'i_clrBearProjection', 'param': None, 'type': 'color', 'default': 36095, 'label': 'Color for proj. bearish patterns (5P)', 'sinput': False}, {'mql': 'i_clrBullProjection4P', 'py': 'i_clrBullProjection4P', 'param': None, 'type': 'color', 'default': 3329434, 'label': 'Color for proj. bullish patterns (4P)', 'sinput': False}, {'mql': 'i_clrBearProjection4P', 'py': 'i_clrBearProjection4P', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Color for proj. bearish patterns (4P)', 'sinput': False}, {'mql': 'i_clrFocus', 'py': 'i_clrFocus', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'Color for focused patterns', 'sinput': False}, {'mql': 'i_fillPatterns', 'py': 'i_fillPatterns', 'param': 'i_fillPatterns', 'type': 'bool', 'default': False, 'label': 'Fill 5 point patterns found', 'sinput': False}, {'mql': 'i_showDescriptions', 'py': 'i_showDescriptions', 'param': 'i_showDescriptions', 'type': 'bool', 'default': True, 'label': 'Show pattern descriptions', 'sinput': False}, {'mql': 'i_emergingPatterns', 'py': 'i_emergingPatterns', 'param': 'i_emergingPatterns', 'type': 'bool', 'default': True, 'label': 'Show emerging patterns', 'sinput': False}, {'mql': 'i_oldPatterns', 'py': 'i_oldPatterns', 'param': 'i_oldPatterns', 'type': 'bool', 'default': True, 'label': 'Show past patterns', 'sinput': False}, {'mql': 'i_oneAheadProjection', 'py': 'i_oneAheadProjection', 'param': 'i_oneAheadProjection', 'type': 'bool', 'default': False, 'label': 'Show "one-ahead" projections', 'sinput': False}, {'mql': 'i_showSoftProjections', 'py': 'i_showSoftProjections', 'param': 'i_showSoftProjections', 'type': 'bool', 'default': True, 'label': 'Draw projections bodies in soft color', 'sinput': False}, {'mql': 'showPatternNames', 'py': 'showPatternNames', 'param': 'showPatternNames', 'type': 'bool', 'default': True, 'label': 'Show comment box', 'sinput': False}, {'mql': 'i_lineWidth', 'py': 'i_lineWidth', 'param': 'i_lineWidth', 'type': 'int', 'default': 2, 'label': 'Pattern line width', 'sinput': False}, {'mql': 'i_lineWidthProj', 'py': 'i_lineWidthProj', 'param': 'i_lineWidthProj', 'type': 'int', 'default': 1, 'label': 'Emerging patterns line width', 'sinput': False}, {'mql': 'i_lineWidthFoc', 'py': 'i_lineWidthFoc', 'param': 'i_lineWidthFoc', 'type': 'int', 'default': 3, 'label': 'Focused patterns line width', 'sinput': False}, {'mql': 'i_fontSize', 'py': 'i_fontSize', 'param': 'i_fontSize', 'type': 'int', 'default': 8, 'label': 'Font size', 'sinput': False}, {'mql': 'i_style5P', 'py': 'i_style5P', 'param': 'i_style5P', 'type': 'int', 'default': 0, 'label': 'Style for 5 points patterns', 'sinput': False}, {'mql': 'i_style4P', 'py': 'i_style4P', 'param': 'i_style4P', 'type': 'int', 'default': 1, 'label': 'Style for 4 points patterns', 'sinput': False}, {'mql': 'i_styleProj', 'py': 'i_styleProj', 'param': 'i_styleProj', 'type': 'int', 'default': 4, 'label': 'Style for projections', 'sinput': False}, {'mql': 'i_styleRatio', 'py': 'i_styleRatio', 'param': 'i_styleRatio', 'type': 'int', 'default': 2, 'label': 'Style for ratio lines', 'sinput': False}, {'mql': 'i_stylePRZ', 'py': 'i_stylePRZ', 'param': 'i_stylePRZ', 'type': 'int', 'default': 3, 'label': 'Style for PRZ', 'sinput': False}, {'mql': 'indicatorPatternsQuick', 'py': 'indicatorPatternsQuick', 'param': None, 'type': 'string', 'default': '-=Patterns Quick=-', 'label': '-=Patterns Quick=-', 'sinput': False}, {'mql': 'i_show_abcd', 'py': 'i_show_abcd', 'param': 'i_show_abcd', 'type': 'bool', 'default': True, 'label': 'Display AB=CD patterns', 'sinput': False}, {'mql': 'i_show_alt127_abcd', 'py': 'i_show_alt127_abcd', 'param': 'i_show_alt127_abcd', 'type': 'bool', 'default': False, 'label': 'Display 1.27 AB=CD patterns', 'sinput': False}, {'mql': 'i_show_alt161_abcd', 'py': 'i_show_alt161_abcd', 'param': 'i_show_alt161_abcd', 'type': 'bool', 'default': False, 'label': 'Display 1.61 AB=CD patterns', 'sinput': False}, {'mql': 'i_show_rec_abcd', 'py': 'i_show_rec_abcd', 'param': 'i_show_rec_abcd', 'type': 'bool', 'default': False, 'label': 'Display Rec. AB=CD patterns', 'sinput': False}, {'mql': 'i_show_alt127_rec_abcd', 'py': 'i_show_alt127_rec_abcd', 'param': 'i_show_alt127_rec_abcd', 'type': 'bool', 'default': False, 'label': 'Display Rec. 1.27 AB=CD patterns', 'sinput': False}, {'mql': 'i_show_alt161_rec_abcd', 'py': 'i_show_alt161_rec_abcd', 'param': 'i_show_alt161_rec_abcd', 'type': 'bool', 'default': False, 'label': 'Display Rec. 1.61 AB=CD patterns', 'sinput': False}, {'mql': 'i_show_patterns', 'py': 'i_show_patterns', 'param': 'i_show_patterns', 'type': 'bool', 'default': True, 'label': 'Display normal 5-point patterns', 'sinput': False}, {'mql': 'i_show_antipatterns', 'py': 'i_show_antipatterns', 'param': 'i_show_antipatterns', 'type': 'bool', 'default': False, 'label': 'Display anti 5-point patterns', 'sinput': False}, {'mql': 'indicatorPatternsIndividual', 'py': 'indicatorPatternsIndividual', 'param': None, 'type': 'string', 'default': '-=Patterns Individual=-', 'label': '-=Patterns Individual=-', 'sinput': False}, {'mql': 'i_show_trendlike1_abcd', 'py': 'i_show_trendlike1_abcd', 'param': 'i_show_trendlike1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike AB=CD #1', 'sinput': False}, {'mql': 'i_show_trendlike2_abcd', 'py': 'i_show_trendlike2_abcd', 'param': 'i_show_trendlike2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike AB=CD #2', 'sinput': False}, {'mql': 'i_show_perfect_abcd', 'py': 'i_show_perfect_abcd', 'param': 'i_show_perfect_abcd', 'type': 'bool', 'default': True, 'label': 'Display Perfect AB=CD', 'sinput': False}, {'mql': 'i_show_ideal1_abcd', 'py': 'i_show_ideal1_abcd', 'param': 'i_show_ideal1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal AB=CD #1', 'sinput': False}, {'mql': 'i_show_ideal2_abcd', 'py': 'i_show_ideal2_abcd', 'param': 'i_show_ideal2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal AB=CD #2', 'sinput': False}, {'mql': 'i_show_rangelike_abcd', 'py': 'i_show_rangelike_abcd', 'param': 'i_show_rangelike_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rangelike AB=CD', 'sinput': False}, {'mql': 'i_show_alt127_trendlike1_abcd', 'py': 'i_show_alt127_trendlike1_abcd', 'param': 'i_show_alt127_trendlike1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike 1.27 AB=CD #1', 'sinput': False}, {'mql': 'i_show_alt127_trendlike2_abcd', 'py': 'i_show_alt127_trendlike2_abcd', 'param': 'i_show_alt127_trendlike2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike 1.27 AB=CD #2', 'sinput': False}, {'mql': 'i_show_alt127_perfect_abcd', 'py': 'i_show_alt127_perfect_abcd', 'param': 'i_show_alt127_perfect_abcd', 'type': 'bool', 'default': True, 'label': 'Display Perfect 1.27 AB=CD', 'sinput': False}, {'mql': 'i_show_alt127_ideal1_abcd', 'py': 'i_show_alt127_ideal1_abcd', 'param': 'i_show_alt127_ideal1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal 1.27 AB=CD #1', 'sinput': False}, {'mql': 'i_show_alt127_ideal2_abcd', 'py': 'i_show_alt127_ideal2_abcd', 'param': 'i_show_alt127_ideal2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal 1.27 AB=CD #2', 'sinput': False}, {'mql': 'i_show_alt127_rangelike_abcd', 'py': 'i_show_alt127_rangelike_abcd', 'param': 'i_show_alt127_rangelike_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rangelike 1.27 AB=CD', 'sinput': False}, {'mql': 'i_show_alt161_trendlike1_abcd', 'py': 'i_show_alt161_trendlike1_abcd', 'param': 'i_show_alt161_trendlike1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike 1.61 AB=CD #1', 'sinput': False}, {'mql': 'i_show_alt161_trendlike2_abcd', 'py': 'i_show_alt161_trendlike2_abcd', 'param': 'i_show_alt161_trendlike2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike 1.61 AB=CD #2', 'sinput': False}, {'mql': 'i_show_alt161_perfect_abcd', 'py': 'i_show_alt161_perfect_abcd', 'param': 'i_show_alt161_perfect_abcd', 'type': 'bool', 'default': True, 'label': 'Display Perfect 1.61 AB=CD', 'sinput': False}, {'mql': 'i_show_alt161_ideal1_abcd', 'py': 'i_show_alt161_ideal1_abcd', 'param': 'i_show_alt161_ideal1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal 1.61 AB=CD #1', 'sinput': False}, {'mql': 'i_show_alt161_ideal2_abcd', 'py': 'i_show_alt161_ideal2_abcd', 'param': 'i_show_alt161_ideal2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal 1.61 AB=CD #2', 'sinput': False}, {'mql': 'i_show_alt161_rangelike_abcd', 'py': 'i_show_alt161_rangelike_abcd', 'param': 'i_show_alt161_rangelike_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rangelike 1.61 AB=CD', 'sinput': False}, {'mql': 'i_show_rec_trendlike1_abcd', 'py': 'i_show_rec_trendlike1_abcd', 'param': 'i_show_rec_trendlike1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Trendlike AB=CD #1', 'sinput': False}, {'mql': 'i_show_rec_trendlike2_abcd', 'py': 'i_show_rec_trendlike2_abcd', 'param': 'i_show_rec_trendlike2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Trendlike AB=CD #2', 'sinput': False}, {'mql': 'i_show_rec_perfect_abcd', 'py': 'i_show_rec_perfect_abcd', 'param': 'i_show_rec_perfect_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Perfect AB=CD', 'sinput': False}, {'mql': 'i_show_rec_ideal1_abcd', 'py': 'i_show_rec_ideal1_abcd', 'param': 'i_show_rec_ideal1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Ideal AB=CD #1', 'sinput': False}, {'mql': 'i_show_rec_ideal2_abcd', 'py': 'i_show_rec_ideal2_abcd', 'param': 'i_show_rec_ideal2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Ideal AB=CD #2', 'sinput': False}, {'mql': 'i_show_rec_rangelike_abcd', 'py': 'i_show_rec_rangelike_abcd', 'param': 'i_show_rec_rangelike_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Rangelike AB=CD', 'sinput': False}, {'mql': 'i_show_alt127_rec_trendlike1_abcd', 'py': 'i_show_alt127_rec_trendlike1_abcd', 'param': 'i_show_alt127_rec_trendlike1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Trendlike 1.27 AB=CD #1', 'sinput': False}, {'mql': 'i_show_alt127_rec_trendlike2_abcd', 'py': 'i_show_alt127_rec_trendlike2_abcd', 'param': 'i_show_alt127_rec_trendlike2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Trendlike 1.27 AB=CD #2', 'sinput': False}, {'mql': 'i_show_alt127_rec_perfect_abcd', 'py': 'i_show_alt127_rec_perfect_abcd', 'param': 'i_show_alt127_rec_perfect_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Perfect 1.27 AB=CD', 'sinput': False}, {'mql': 'i_show_alt127_rec_ideal1_abcd', 'py': 'i_show_alt127_rec_ideal1_abcd', 'param': 'i_show_alt127_rec_ideal1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Ideal 1.27 AB=CD #1', 'sinput': False}, {'mql': 'i_show_alt127_rec_ideal2_abcd', 'py': 'i_show_alt127_rec_ideal2_abcd', 'param': 'i_show_alt127_rec_ideal2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Ideal 1.27 AB=CD #2', 'sinput': False}, {'mql': 'i_show_alt127_rec_rangelike_abcd', 'py': 'i_show_alt127_rec_rangelike_abcd', 'param': 'i_show_alt127_rec_rangelike_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Rangelike 1.27 AB=CD', 'sinput': False}, {'mql': 'i_show_alt161_rec_trendlike1_abcd', 'py': 'i_show_alt161_rec_trendlike1_abcd', 'param': 'i_show_alt161_rec_trendlike1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Trendlike 1.61 AB=CD #1', 'sinput': False}, {'mql': 'i_show_alt161_rec_trendlike2_abcd', 'py': 'i_show_alt161_rec_trendlike2_abcd', 'param': 'i_show_alt161_rec_trendlike2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Trendlike 1.61 AB=CD #2', 'sinput': False}, {'mql': 'i_show_alt161_rec_perfect_abcd', 'py': 'i_show_alt161_rec_perfect_abcd', 'param': 'i_show_alt161_rec_perfect_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Perfect 1.61 AB=CD', 'sinput': False}, {'mql': 'i_show_alt161_rec_ideal1_abcd', 'py': 'i_show_alt161_rec_ideal1_abcd', 'param': 'i_show_alt161_rec_ideal1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Ideal 1.61 AB=CD #1', 'sinput': False}, {'mql': 'i_show_alt161_rec_ideal2_abcd', 'py': 'i_show_alt161_rec_ideal2_abcd', 'param': 'i_show_alt161_rec_ideal2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Ideal 1.61 AB=CD #2', 'sinput': False}, {'mql': 'i_show_alt161_rec_rangelike_abcd', 'py': 'i_show_alt161_rec_rangelike_abcd', 'param': 'i_show_alt161_rec_rangelike_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Rangelike 1.61 AB=CD', 'sinput': False}, {'mql': 'i_show_gartley', 'py': 'i_show_gartley', 'param': 'i_show_gartley', 'type': 'bool', 'default': True, 'label': 'Display Gartley', 'sinput': False}, {'mql': 'i_show_perfect_gartley', 'py': 'i_show_perfect_gartley', 'param': 'i_show_perfect_gartley', 'type': 'bool', 'default': True, 'label': 'Display Perfect Gartley', 'sinput': False}, {'mql': 'i_show_gartley113', 'py': 'i_show_gartley113', 'param': 'i_show_gartley113', 'type': 'bool', 'default': True, 'label': 'Display Gartley 113', 'sinput': False}, {'mql': 'i_show_maxgartley', 'py': 'i_show_maxgartley', 'param': 'i_show_maxgartley', 'type': 'bool', 'default': True, 'label': 'Display Max. Gartley', 'sinput': False}, {'mql': 'i_show_bat', 'py': 'i_show_bat', 'param': 'i_show_bat', 'type': 'bool', 'default': True, 'label': 'Display Bat', 'sinput': False}, {'mql': 'i_show_perfect_bat', 'py': 'i_show_perfect_bat', 'param': 'i_show_perfect_bat', 'type': 'bool', 'default': True, 'label': 'Display Perfect Bat', 'sinput': False}, {'mql': 'i_show_altbat', 'py': 'i_show_altbat', 'param': 'i_show_altbat', 'type': 'bool', 'default': True, 'label': 'Display Alt. Bat', 'sinput': False}, {'mql': 'i_show_maxbat', 'py': 'i_show_maxbat', 'param': 'i_show_maxbat', 'type': 'bool', 'default': True, 'label': 'Display Max. Bat', 'sinput': False}, {'mql': 'i_show_crab', 'py': 'i_show_crab', 'param': 'i_show_crab', 'type': 'bool', 'default': True, 'label': 'Display Crab', 'sinput': False}, {'mql': 'i_show_perfect_crab', 'py': 'i_show_perfect_crab', 'param': 'i_show_perfect_crab', 'type': 'bool', 'default': True, 'label': 'Display Perfect Crab', 'sinput': False}, {'mql': 'i_show_deepcrab', 'py': 'i_show_deepcrab', 'param': 'i_show_deepcrab', 'type': 'bool', 'default': True, 'label': 'Display Deepcrab', 'sinput': False}, {'mql': 'i_show_butterfly', 'py': 'i_show_butterfly', 'param': 'i_show_butterfly', 'type': 'bool', 'default': True, 'label': 'Display Butterfly', 'sinput': False}, {'mql': 'i_show_perfect_butterfly', 'py': 'i_show_perfect_butterfly', 'param': 'i_show_perfect_butterfly', 'type': 'bool', 'default': True, 'label': 'Display Perfect Butterfly', 'sinput': False}, {'mql': 'i_show_maxbutterfly', 'py': 'i_show_maxbutterfly', 'param': 'i_show_maxbutterfly', 'type': 'bool', 'default': True, 'label': 'Display Max. Butterfly', 'sinput': False}, {'mql': 'i_show_butterfly113', 'py': 'i_show_butterfly113', 'param': 'i_show_butterfly113', 'type': 'bool', 'default': True, 'label': 'Display Butterfly 113', 'sinput': False}, {'mql': 'i_show_fiveo', 'py': 'i_show_fiveo', 'param': 'i_show_fiveo', 'type': 'bool', 'default': True, 'label': 'Display 5-0', 'sinput': False}, {'mql': 'i_show_threedrives', 'py': 'i_show_threedrives', 'param': 'i_show_threedrives', 'type': 'bool', 'default': True, 'label': 'Display Three Drives', 'sinput': False}, {'mql': 'i_show_cypher', 'py': 'i_show_cypher', 'param': 'i_show_cypher', 'type': 'bool', 'default': True, 'label': 'Display Cypher', 'sinput': False}, {'mql': 'i_show_shark', 'py': 'i_show_shark', 'param': 'i_show_shark', 'type': 'bool', 'default': True, 'label': 'Display Shark', 'sinput': False}, {'mql': 'i_show_nenstar', 'py': 'i_show_nenstar', 'param': 'i_show_nenstar', 'type': 'bool', 'default': True, 'label': 'Display Nen Star', 'sinput': False}, {'mql': 'i_show_blackswan', 'py': 'i_show_blackswan', 'param': 'i_show_blackswan', 'type': 'bool', 'default': True, 'label': 'Display Black Swan', 'sinput': False}, {'mql': 'i_show_whiteswan', 'py': 'i_show_whiteswan', 'param': 'i_show_whiteswan', 'type': 'bool', 'default': True, 'label': 'Display White Swan', 'sinput': False}, {'mql': 'i_show_one2one', 'py': 'i_show_one2one', 'param': 'i_show_one2one', 'type': 'bool', 'default': False, 'label': 'Display One2One', 'sinput': False}, {'mql': 'i_show_newCypher', 'py': 'i_show_newCypher', 'param': 'i_show_newCypher', 'type': 'bool', 'default': True, 'label': 'Display New Cypher', 'sinput': False}, {'mql': 'i_show_navarro200', 'py': 'i_show_navarro200', 'param': 'i_show_navarro200', 'type': 'bool', 'default': False, 'label': 'Display Navarro 200', 'sinput': False}, {'mql': 'i_show_leonardo', 'py': 'i_show_leonardo', 'param': 'i_show_leonardo', 'type': 'bool', 'default': True, 'label': 'Display Leonardo', 'sinput': False}, {'mql': 'i_show_kane', 'py': 'i_show_kane', 'param': 'i_show_kane', 'type': 'bool', 'default': True, 'label': 'Display Kane', 'sinput': False}, {'mql': 'i_show_garfly', 'py': 'i_show_garfly', 'param': 'i_show_garfly', 'type': 'bool', 'default': True, 'label': 'Display Garfly', 'sinput': False}, {'mql': 'i_show_antigartley', 'py': 'i_show_antigartley', 'param': 'i_show_antigartley', 'type': 'bool', 'default': True, 'label': 'Display Anti Gartley', 'sinput': False}, {'mql': 'i_show_antibat', 'py': 'i_show_antibat', 'param': 'i_show_antibat', 'type': 'bool', 'default': True, 'label': 'Display Anti Bat', 'sinput': False}, {'mql': 'i_show_antialtbat', 'py': 'i_show_antialtbat', 'param': 'i_show_antialtbat', 'type': 'bool', 'default': True, 'label': 'Display Anti Alt. Bat', 'sinput': False}, {'mql': 'i_show_antifiveo', 'py': 'i_show_antifiveo', 'param': 'i_show_antifiveo', 'type': 'bool', 'default': True, 'label': 'Display Anti 5-0', 'sinput': False}, {'mql': 'i_show_antibutterfly', 'py': 'i_show_antibutterfly', 'param': 'i_show_antibutterfly', 'type': 'bool', 'default': True, 'label': 'Display Anti Butterfly', 'sinput': False}, {'mql': 'i_show_anticrab', 'py': 'i_show_anticrab', 'param': 'i_show_anticrab', 'type': 'bool', 'default': True, 'label': 'Display Anti Crab', 'sinput': False}, {'mql': 'i_show_antideepcrab', 'py': 'i_show_antideepcrab', 'param': 'i_show_antideepcrab', 'type': 'bool', 'default': True, 'label': 'Display Anti Deepcrab', 'sinput': False}, {'mql': 'i_show_antithreedrives', 'py': 'i_show_antithreedrives', 'param': 'i_show_antithreedrives', 'type': 'bool', 'default': True, 'label': 'Display Anti Three Drives', 'sinput': False}, {'mql': 'i_show_anticypher', 'py': 'i_show_anticypher', 'param': 'i_show_anticypher', 'type': 'bool', 'default': True, 'label': 'Display Anti Cypher', 'sinput': False}, {'mql': 'i_show_antishark', 'py': 'i_show_antishark', 'param': 'i_show_antishark', 'type': 'bool', 'default': True, 'label': 'Display Anti Shark', 'sinput': False}, {'mql': 'i_show_antinenstar', 'py': 'i_show_antinenstar', 'param': 'i_show_antinenstar', 'type': 'bool', 'default': True, 'label': 'Display Anti Nen Star', 'sinput': False}, {'mql': 'i_show_antiblackswan', 'py': 'i_show_antiblackswan', 'param': 'i_show_antiblackswan', 'type': 'bool', 'default': True, 'label': 'Display Anti Black Swan', 'sinput': False}, {'mql': 'i_show_antiwhiteswan', 'py': 'i_show_antiwhiteswan', 'param': 'i_show_antiwhiteswan', 'type': 'bool', 'default': True, 'label': 'Display Anti White Swan', 'sinput': False}, {'mql': 'i_show_antione2one', 'py': 'i_show_antione2one', 'param': 'i_show_antione2one', 'type': 'bool', 'default': True, 'label': 'Display Anti One2One', 'sinput': False}, {'mql': 'i_show_antinewCypher', 'py': 'i_show_antinewCypher', 'param': 'i_show_antinewCypher', 'type': 'bool', 'default': True, 'label': 'Display Anti New Cypher', 'sinput': False}, {'mql': 'i_show_antinavarro200', 'py': 'i_show_antinavarro200', 'param': 'i_show_antinavarro200', 'type': 'bool', 'default': True, 'label': 'Display Anti Navarro 200', 'sinput': False}, {'mql': 'i_show_antileonardo', 'py': 'i_show_antileonardo', 'param': 'i_show_antileonardo', 'type': 'bool', 'default': True, 'label': 'Display Anti Leonardo', 'sinput': False}, {'mql': 'i_show_antikane', 'py': 'i_show_antikane', 'param': 'i_show_antikane', 'type': 'bool', 'default': True, 'label': 'Display Anti Kane', 'sinput': False}, {'mql': 'i_show_antigarfly', 'py': 'i_show_antigarfly', 'param': 'i_show_antigarfly', 'type': 'bool', 'default': True, 'label': 'Display Anti Garfly', 'sinput': False}, {'mql': 'i_show_antimaxbat', 'py': 'i_show_antimaxbat', 'param': 'i_show_antimaxbat', 'type': 'bool', 'default': True, 'label': 'Display Anti Max. Bat', 'sinput': False}, {'mql': 'i_show_antimaxgartley', 'py': 'i_show_antimaxgartley', 'param': 'i_show_antimaxgartley', 'type': 'bool', 'default': True, 'label': 'Display Anti Max. Gartley', 'sinput': False}, {'mql': 'i_show_antimaxbutterfly', 'py': 'i_show_antimaxbutterfly', 'param': 'i_show_antimaxbutterfly', 'type': 'bool', 'default': True, 'label': 'Display Anti Max. Butterfly', 'sinput': False}, {'mql': 'i_show_antigartley113', 'py': 'i_show_antigartley113', 'param': 'i_show_antigartley113', 'type': 'bool', 'default': True, 'label': 'Display Anti Gartley 113', 'sinput': False}, {'mql': 'i_show_antibutterfly113', 'py': 'i_show_antibutterfly113', 'param': 'i_show_antibutterfly113', 'type': 'bool', 'default': True, 'label': 'Display Anti Butterfly 113', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['HPFMatchProcessor.mqh']}

# enum HARMONIC_TIMELINESS
TOO_EARLY = 0
TIMELY = 1
TOO_LATE = 2
_enum('HARMONIC_TIMELINESS', {0: 'TOO_EARLY', 1: 'TIMELY', 2: 'TOO_LATE'})

# enum PATTERN_INDEX
TRENDLIKE1_ABCD = 0
TRENDLIKE2_ABCD = 1
PERFECT_ABCD = 2
IDEAL1_ABCD = 3
IDEAL2_ABCD = 4
RANGELIKE_ABCD = 5
ALT127_TRENDLIKE1_ABCD = 6
ALT127_TRENDLIKE2_ABCD = 7
ALT127_PERFECT_ABCD = 8
ALT127_IDEAL1_ABCD = 9
ALT127_IDEAL2_ABCD = 10
ALT127_RANGELIKE_ABCD = 11
ALT161_TRENDLIKE1_ABCD = 12
ALT161_TRENDLIKE2_ABCD = 13
ALT161_PERFECT_ABCD = 14
ALT161_IDEAL1_ABCD = 15
ALT161_IDEAL2_ABCD = 16
ALT161_RANGELIKE_ABCD = 17
REC_TRENDLIKE1_ABCD = 18
REC_TRENDLIKE2_ABCD = 19
REC_PERFECT_ABCD = 20
REC_IDEAL1_ABCD = 21
REC_IDEAL2_ABCD = 22
REC_RANGELIKE_ABCD = 23
ALT127_REC_TRENDLIKE1_ABCD = 24
ALT127_REC_TRENDLIKE2_ABCD = 25
ALT127_REC_PERFECT_ABCD = 26
ALT127_REC_IDEAL1_ABCD = 27
ALT127_REC_IDEAL2_ABCD = 28
ALT127_REC_RANGELIKE_ABCD = 29
ALT161_REC_TRENDLIKE1_ABCD = 30
ALT161_REC_TRENDLIKE2_ABCD = 31
ALT161_REC_PERFECT_ABCD = 32
ALT161_REC_IDEAL1_ABCD = 33
ALT161_REC_IDEAL2_ABCD = 34
ALT161_REC_RANGELIKE_ABCD = 35
GARTLEY = 36
PERFECT_GARTLEY = 37
MAXGARTLEY = 38
BAT = 39
PERFECT_BAT = 40
ALTBAT = 41
MAXBAT = 42
CRAB = 43
PERFECT_CRAB = 44
DEEPCRAB = 45
BUTTERFLY = 46
PERFECT_BUTTERFLY = 47
MAXBUTTERFLY = 48
BUTTERFLY113 = 49
FIVEO = 50
THREEDRIVES = 51
CYPHER = 52
SHARK = 53
NENSTAR = 54
BLACKSWAN = 55
WHITESWAN = 56
ONE2ONE = 57
NEWCYPHER = 58
NAVARRO200 = 59
LEONARDO = 60
KANE = 61
GARFLY = 62
GARTLEY113 = 63
ANTI_GARTLEY = 64
ANTI_BAT = 65
ANTI_ALTBAT = 66
ANTI_FIVEO = 67
ANTI_BUTTERFLY = 68
ANTI_CRAB = 69
ANTI_DEEPCRAB = 70
ANTI_THREEDRIVES = 71
ANTI_CYPHER = 72
ANTI_SHARK = 73
ANTI_NENSTAR = 74
ANTI_BLACKSWAN = 75
ANTI_WHITESWAN = 76
ANTI_ONE2ONE = 77
ANTI_NEWCYPHER = 78
ANTI_NAVARRO200 = 79
ANTI_LEONARDO = 80
ANTI_KANE = 81
ANTI_GARFLY = 82
ANTI_MAXBAT = 83
ANTI_MAXGARTLEY = 84
ANTI_MAXBUTTERFLY = 85
ANTI_GARTLEY113 = 86
ANTI_BUTTERFLY113 = 87
_enum('PATTERN_INDEX', {0: 'TRENDLIKE1_ABCD', 1: 'TRENDLIKE2_ABCD', 2: 'PERFECT_ABCD', 3: 'IDEAL1_ABCD', 4: 'IDEAL2_ABCD', 5: 'RANGELIKE_ABCD', 6: 'ALT127_TRENDLIKE1_ABCD', 7: 'ALT127_TRENDLIKE2_ABCD', 8: 'ALT127_PERFECT_ABCD', 9: 'ALT127_IDEAL1_ABCD', 10: 'ALT127_IDEAL2_ABCD', 11: 'ALT127_RANGELIKE_ABCD', 12: 'ALT161_TRENDLIKE1_ABCD', 13: 'ALT161_TRENDLIKE2_ABCD', 14: 'ALT161_PERFECT_ABCD', 15: 'ALT161_IDEAL1_ABCD', 16: 'ALT161_IDEAL2_ABCD', 17: 'ALT161_RANGELIKE_ABCD', 18: 'REC_TRENDLIKE1_ABCD', 19: 'REC_TRENDLIKE2_ABCD', 20: 'REC_PERFECT_ABCD', 21: 'REC_IDEAL1_ABCD', 22: 'REC_IDEAL2_ABCD', 23: 'REC_RANGELIKE_ABCD', 24: 'ALT127_REC_TRENDLIKE1_ABCD', 25: 'ALT127_REC_TRENDLIKE2_ABCD', 26: 'ALT127_REC_PERFECT_ABCD', 27: 'ALT127_REC_IDEAL1_ABCD', 28: 'ALT127_REC_IDEAL2_ABCD', 29: 'ALT127_REC_RANGELIKE_ABCD', 30: 'ALT161_REC_TRENDLIKE1_ABCD', 31: 'ALT161_REC_TRENDLIKE2_ABCD', 32: 'ALT161_REC_PERFECT_ABCD', 33: 'ALT161_REC_IDEAL1_ABCD', 34: 'ALT161_REC_IDEAL2_ABCD', 35: 'ALT161_REC_RANGELIKE_ABCD', 36: 'GARTLEY', 37: 'PERFECT_GARTLEY', 38: 'MAXGARTLEY', 39: 'BAT', 40: 'PERFECT_BAT', 41: 'ALTBAT', 42: 'MAXBAT', 43: 'CRAB', 44: 'PERFECT_CRAB', 45: 'DEEPCRAB', 46: 'BUTTERFLY', 47: 'PERFECT_BUTTERFLY', 48: 'MAXBUTTERFLY', 49: 'BUTTERFLY113', 50: 'FIVEO', 51: 'THREEDRIVES', 52: 'CYPHER', 53: 'SHARK', 54: 'NENSTAR', 55: 'BLACKSWAN', 56: 'WHITESWAN', 57: 'ONE2ONE', 58: 'NEWCYPHER', 59: 'NAVARRO200', 60: 'LEONARDO', 61: 'KANE', 62: 'GARFLY', 63: 'GARTLEY113', 64: 'ANTI_GARTLEY', 65: 'ANTI_BAT', 66: 'ANTI_ALTBAT', 67: 'ANTI_FIVEO', 68: 'ANTI_BUTTERFLY', 69: 'ANTI_CRAB', 70: 'ANTI_DEEPCRAB', 71: 'ANTI_THREEDRIVES', 72: 'ANTI_CYPHER', 73: 'ANTI_SHARK', 74: 'ANTI_NENSTAR', 75: 'ANTI_BLACKSWAN', 76: 'ANTI_WHITESWAN', 77: 'ANTI_ONE2ONE', 78: 'ANTI_NEWCYPHER', 79: 'ANTI_NAVARRO200', 80: 'ANTI_LEONARDO', 81: 'ANTI_KANE', 82: 'ANTI_GARFLY', 83: 'ANTI_MAXBAT', 84: 'ANTI_MAXGARTLEY', 85: 'ANTI_MAXBUTTERFLY', 86: 'ANTI_GARTLEY113', 87: 'ANTI_BUTTERFLY113'})

# ---- inputs and global variables
_identifier = 'HPE'
_secsDoubleClick = 1000
HARMONIC_NUMBERS = Arr.of([0.382, 0.5, 0.618, 0.707, 0.786, 0.886, 1.0, 1.13, 1.272, 1.414, 1.618, 2.0, 2.236, 2.618, 3.14, 3.618], fill=0.0)
zigzagSettings = _input('zigzagSettings', '-=ZigZag Settings=-')  # -=ZigZag Settings=-
i_zzAtrMultiplier = _input('i_zzAtrMultiplier', 2.0)  # ATR ZZ atr multiplier
i_zzAtrPeriod = _input('i_zzAtrPeriod', 50)  # ATR ZZ atr period
i_zzMaxPeriod = _input('i_zzMaxPeriod', 10)  # ATR ZZ max period
i_zzMinPeriod = _input('i_zzMinPeriod', 3)  # ATR ZZ min period
i_zzRealtime = _input('i_zzRealtime', True)  # ATR ZZ realtime
indicatorSettings = _input('indicatorSettings', '-=Indicator Settings=-')  # -=Indicator Settings=-
i_barsAnalyzed = _input('i_barsAnalyzed', 300)  # Max. bars per pattern
i_history = _input('i_history', 1000)  # Max. history bars to process
i_maxSamePoints = _input('i_maxSamePoints', 2)  # Max. shared points per pattern
i_slackRange = _input('i_slackRange', 0.05)  # Max. slack for fib ratios (range)
i_slackSingular = _input('i_slackSingular', 0.1)  # Max. slack for fib ratios (unary)
i_tooEarly = _input('i_tooEarly', 0.382)  # Too early timezone
i_ideal = _input('i_ideal', 1.0)  # Ideal timezone
i_tooLate = _input('i_tooLate', 1.618)  # Too late timezone
i_puristPRZ = _input('i_puristPRZ', False)  # Filter patterns without fib ratios in PRZ
i_timefilterEarly = _input('i_timefilterEarly', False)  # Filter too early patterns
i_timefilterLate = _input('i_timefilterLate', False)  # Filter too late patterns
indicatorColors = _input('indicatorColors', '-=Display Settings=-')  # -=Display Settings=-
i_clrBull = _input('i_clrBull', clrLightSkyBlue)  # Color for bullish patterns (5 points)
i_clrBear = _input('i_clrBear', clrLightPink)  # Color for bearish patterns (5 points)
i_clrBull4P = _input('i_clrBull4P', clrDeepSkyBlue)  # Color for bullish patterns (4 points)
i_clrBear4P = _input('i_clrBear4P', clrDeepPink)  # Color for bearish patterns (4 points)
i_clrBullProjection = _input('i_clrBullProjection', clrSeaGreen)  # Color for proj. bullish patterns (5P)
i_clrBearProjection = _input('i_clrBearProjection', clrDarkOrange)  # Color for proj. bearish patterns (5P)
i_clrBullProjection4P = _input('i_clrBullProjection4P', clrYellowGreen)  # Color for proj. bullish patterns (4P)
i_clrBearProjection4P = _input('i_clrBearProjection4P', clrYellow)  # Color for proj. bearish patterns (4P)
i_clrFocus = _input('i_clrFocus', clrWhite)  # Color for focused patterns
i_fillPatterns = _input('i_fillPatterns', False)  # Fill 5 point patterns found
i_showDescriptions = _input('i_showDescriptions', True)  # Show pattern descriptions
i_emergingPatterns = _input('i_emergingPatterns', True)  # Show emerging patterns
i_oldPatterns = _input('i_oldPatterns', True)  # Show past patterns
i_oneAheadProjection = _input('i_oneAheadProjection', False)  # Show "one-ahead" projections
i_showSoftProjections = _input('i_showSoftProjections', True)  # Draw projections bodies in soft color
showPatternNames = _input('showPatternNames', True)  # Show comment box
i_lineWidth = _input('i_lineWidth', 2)  # Pattern line width
i_lineWidthProj = _input('i_lineWidthProj', 1)  # Emerging patterns line width
i_lineWidthFoc = _input('i_lineWidthFoc', 3)  # Focused patterns line width
i_fontSize = _input('i_fontSize', 8)  # Font size
i_style5P = _input('i_style5P', STYLE_SOLID)  # Style for 5 points patterns
i_style4P = _input('i_style4P', STYLE_DASH)  # Style for 4 points patterns
i_styleProj = _input('i_styleProj', STYLE_DASHDOTDOT)  # Style for projections
i_styleRatio = _input('i_styleRatio', STYLE_DOT)  # Style for ratio lines
i_stylePRZ = _input('i_stylePRZ', STYLE_DASHDOT)  # Style for PRZ
indicatorPatternsQuick = _input('indicatorPatternsQuick', '-=Patterns Quick=-')  # -=Patterns Quick=-
i_show_abcd = _input('i_show_abcd', True)  # Display AB=CD patterns
i_show_alt127_abcd = _input('i_show_alt127_abcd', False)  # Display 1.27 AB=CD patterns
i_show_alt161_abcd = _input('i_show_alt161_abcd', False)  # Display 1.61 AB=CD patterns
i_show_rec_abcd = _input('i_show_rec_abcd', False)  # Display Rec. AB=CD patterns
i_show_alt127_rec_abcd = _input('i_show_alt127_rec_abcd', False)  # Display Rec. 1.27 AB=CD patterns
i_show_alt161_rec_abcd = _input('i_show_alt161_rec_abcd', False)  # Display Rec. 1.61 AB=CD patterns
i_show_patterns = _input('i_show_patterns', True)  # Display normal 5-point patterns
i_show_antipatterns = _input('i_show_antipatterns', False)  # Display anti 5-point patterns
indicatorPatternsIndividual = _input('indicatorPatternsIndividual', '-=Patterns Individual=-')  # -=Patterns Individual=-
i_show_trendlike1_abcd = _input('i_show_trendlike1_abcd', True)  # Display Trendlike AB=CD #1
i_show_trendlike2_abcd = _input('i_show_trendlike2_abcd', True)  # Display Trendlike AB=CD #2
i_show_perfect_abcd = _input('i_show_perfect_abcd', True)  # Display Perfect AB=CD
i_show_ideal1_abcd = _input('i_show_ideal1_abcd', True)  # Display Ideal AB=CD #1
i_show_ideal2_abcd = _input('i_show_ideal2_abcd', True)  # Display Ideal AB=CD #2
i_show_rangelike_abcd = _input('i_show_rangelike_abcd', True)  # Display Rangelike AB=CD
i_show_alt127_trendlike1_abcd = _input('i_show_alt127_trendlike1_abcd', True)  # Display Trendlike 1.27 AB=CD #1
i_show_alt127_trendlike2_abcd = _input('i_show_alt127_trendlike2_abcd', True)  # Display Trendlike 1.27 AB=CD #2
i_show_alt127_perfect_abcd = _input('i_show_alt127_perfect_abcd', True)  # Display Perfect 1.27 AB=CD
i_show_alt127_ideal1_abcd = _input('i_show_alt127_ideal1_abcd', True)  # Display Ideal 1.27 AB=CD #1
i_show_alt127_ideal2_abcd = _input('i_show_alt127_ideal2_abcd', True)  # Display Ideal 1.27 AB=CD #2
i_show_alt127_rangelike_abcd = _input('i_show_alt127_rangelike_abcd', True)  # Display Rangelike 1.27 AB=CD
i_show_alt161_trendlike1_abcd = _input('i_show_alt161_trendlike1_abcd', True)  # Display Trendlike 1.61 AB=CD #1
i_show_alt161_trendlike2_abcd = _input('i_show_alt161_trendlike2_abcd', True)  # Display Trendlike 1.61 AB=CD #2
i_show_alt161_perfect_abcd = _input('i_show_alt161_perfect_abcd', True)  # Display Perfect 1.61 AB=CD
i_show_alt161_ideal1_abcd = _input('i_show_alt161_ideal1_abcd', True)  # Display Ideal 1.61 AB=CD #1
i_show_alt161_ideal2_abcd = _input('i_show_alt161_ideal2_abcd', True)  # Display Ideal 1.61 AB=CD #2
i_show_alt161_rangelike_abcd = _input('i_show_alt161_rangelike_abcd', True)  # Display Rangelike 1.61 AB=CD
i_show_rec_trendlike1_abcd = _input('i_show_rec_trendlike1_abcd', True)  # Display Rec. Trendlike AB=CD #1
i_show_rec_trendlike2_abcd = _input('i_show_rec_trendlike2_abcd', True)  # Display Rec. Trendlike AB=CD #2
i_show_rec_perfect_abcd = _input('i_show_rec_perfect_abcd', True)  # Display Rec. Perfect AB=CD
i_show_rec_ideal1_abcd = _input('i_show_rec_ideal1_abcd', True)  # Display Rec. Ideal AB=CD #1
i_show_rec_ideal2_abcd = _input('i_show_rec_ideal2_abcd', True)  # Display Rec. Ideal AB=CD #2
i_show_rec_rangelike_abcd = _input('i_show_rec_rangelike_abcd', True)  # Display Rec. Rangelike AB=CD
i_show_alt127_rec_trendlike1_abcd = _input('i_show_alt127_rec_trendlike1_abcd', True)  # Display Rec. Trendlike 1.27 AB=CD #1
i_show_alt127_rec_trendlike2_abcd = _input('i_show_alt127_rec_trendlike2_abcd', True)  # Display Rec. Trendlike 1.27 AB=CD #2
i_show_alt127_rec_perfect_abcd = _input('i_show_alt127_rec_perfect_abcd', True)  # Display Rec. Perfect 1.27 AB=CD
i_show_alt127_rec_ideal1_abcd = _input('i_show_alt127_rec_ideal1_abcd', True)  # Display Rec. Ideal 1.27 AB=CD #1
i_show_alt127_rec_ideal2_abcd = _input('i_show_alt127_rec_ideal2_abcd', True)  # Display Rec. Ideal 1.27 AB=CD #2
i_show_alt127_rec_rangelike_abcd = _input('i_show_alt127_rec_rangelike_abcd', True)  # Display Rec. Rangelike 1.27 AB=CD
i_show_alt161_rec_trendlike1_abcd = _input('i_show_alt161_rec_trendlike1_abcd', True)  # Display Rec. Trendlike 1.61 AB=CD #1
i_show_alt161_rec_trendlike2_abcd = _input('i_show_alt161_rec_trendlike2_abcd', True)  # Display Rec. Trendlike 1.61 AB=CD #2
i_show_alt161_rec_perfect_abcd = _input('i_show_alt161_rec_perfect_abcd', True)  # Display Rec. Perfect 1.61 AB=CD
i_show_alt161_rec_ideal1_abcd = _input('i_show_alt161_rec_ideal1_abcd', True)  # Display Rec. Ideal 1.61 AB=CD #1
i_show_alt161_rec_ideal2_abcd = _input('i_show_alt161_rec_ideal2_abcd', True)  # Display Rec. Ideal 1.61 AB=CD #2
i_show_alt161_rec_rangelike_abcd = _input('i_show_alt161_rec_rangelike_abcd', True)  # Display Rec. Rangelike 1.61 AB=CD
i_show_gartley = _input('i_show_gartley', True)  # Display Gartley
i_show_perfect_gartley = _input('i_show_perfect_gartley', True)  # Display Perfect Gartley
i_show_gartley113 = _input('i_show_gartley113', True)  # Display Gartley 113
i_show_maxgartley = _input('i_show_maxgartley', True)  # Display Max. Gartley
i_show_bat = _input('i_show_bat', True)  # Display Bat
i_show_perfect_bat = _input('i_show_perfect_bat', True)  # Display Perfect Bat
i_show_altbat = _input('i_show_altbat', True)  # Display Alt. Bat
i_show_maxbat = _input('i_show_maxbat', True)  # Display Max. Bat
i_show_crab = _input('i_show_crab', True)  # Display Crab
i_show_perfect_crab = _input('i_show_perfect_crab', True)  # Display Perfect Crab
i_show_deepcrab = _input('i_show_deepcrab', True)  # Display Deepcrab
i_show_butterfly = _input('i_show_butterfly', True)  # Display Butterfly
i_show_perfect_butterfly = _input('i_show_perfect_butterfly', True)  # Display Perfect Butterfly
i_show_maxbutterfly = _input('i_show_maxbutterfly', True)  # Display Max. Butterfly
i_show_butterfly113 = _input('i_show_butterfly113', True)  # Display Butterfly 113
i_show_fiveo = _input('i_show_fiveo', True)  # Display 5-0
i_show_threedrives = _input('i_show_threedrives', True)  # Display Three Drives
i_show_cypher = _input('i_show_cypher', True)  # Display Cypher
i_show_shark = _input('i_show_shark', True)  # Display Shark
i_show_nenstar = _input('i_show_nenstar', True)  # Display Nen Star
i_show_blackswan = _input('i_show_blackswan', True)  # Display Black Swan
i_show_whiteswan = _input('i_show_whiteswan', True)  # Display White Swan
i_show_one2one = _input('i_show_one2one', False)  # Display One2One
i_show_newCypher = _input('i_show_newCypher', True)  # Display New Cypher
i_show_navarro200 = _input('i_show_navarro200', False)  # Display Navarro 200
i_show_leonardo = _input('i_show_leonardo', True)  # Display Leonardo
i_show_kane = _input('i_show_kane', True)  # Display Kane
i_show_garfly = _input('i_show_garfly', True)  # Display Garfly
i_show_antigartley = _input('i_show_antigartley', True)  # Display Anti Gartley
i_show_antibat = _input('i_show_antibat', True)  # Display Anti Bat
i_show_antialtbat = _input('i_show_antialtbat', True)  # Display Anti Alt. Bat
i_show_antifiveo = _input('i_show_antifiveo', True)  # Display Anti 5-0
i_show_antibutterfly = _input('i_show_antibutterfly', True)  # Display Anti Butterfly
i_show_anticrab = _input('i_show_anticrab', True)  # Display Anti Crab
i_show_antideepcrab = _input('i_show_antideepcrab', True)  # Display Anti Deepcrab
i_show_antithreedrives = _input('i_show_antithreedrives', True)  # Display Anti Three Drives
i_show_anticypher = _input('i_show_anticypher', True)  # Display Anti Cypher
i_show_antishark = _input('i_show_antishark', True)  # Display Anti Shark
i_show_antinenstar = _input('i_show_antinenstar', True)  # Display Anti Nen Star
i_show_antiblackswan = _input('i_show_antiblackswan', True)  # Display Anti Black Swan
i_show_antiwhiteswan = _input('i_show_antiwhiteswan', True)  # Display Anti White Swan
i_show_antione2one = _input('i_show_antione2one', True)  # Display Anti One2One
i_show_antinewCypher = _input('i_show_antinewCypher', True)  # Display Anti New Cypher
i_show_antinavarro200 = _input('i_show_antinavarro200', True)  # Display Anti Navarro 200
i_show_antileonardo = _input('i_show_antileonardo', True)  # Display Anti Leonardo
i_show_antikane = _input('i_show_antikane', True)  # Display Anti Kane
i_show_antigarfly = _input('i_show_antigarfly', True)  # Display Anti Garfly
i_show_antimaxbat = _input('i_show_antimaxbat', True)  # Display Anti Max. Bat
i_show_antimaxgartley = _input('i_show_antimaxgartley', True)  # Display Anti Max. Gartley
i_show_antimaxbutterfly = _input('i_show_antimaxbutterfly', True)  # Display Anti Max. Butterfly
i_show_antigartley113 = _input('i_show_antigartley113', True)  # Display Anti Gartley 113
i_show_antibutterfly113 = _input('i_show_antibutterfly113', True)  # Display Anti Butterfly 113
_peaks = Arr(0, 0.0)
_troughs = Arr(0, 0.0)
_zzLastDirection = False
_realtimeChange = False
_lastIndex = 0
_lastIndex2 = 0
_contraIndex = 0
_atr = 0.0
_time = Arr(0, 0)
_lastDirection = False
_lastPeakValue = 0.0
_lastTroughValue = 0.0
_lastPeak = 0
_lastTrough = 0
_patternNames = Arr(0, "")
_timeOfInit = 0
_prevClick = 0
_faintBGColor = 0
_clrbackground = 0
_clrRatio = 0

class PATTERN_DESCRIPTOR(MqlObject):
    _q_fields = ('ab2xa_min', 'ab2xa_max', 'bc2ab_min', 'bc2ab_max', 'cd2bc_min', 'cd2bc_max', 'ad2xa_min', 'ad2xa_max', 'cd2xc_min', 'cd2xc_max', 'xc2xa_min', 'xc2xa_max', 'cd2ab_min', 'cd2ab_max', 'bc2xa_min', 'bc2xa_max', 'cd2ad_min', 'cd2ad_max')
    def __init__(self, *args):
        self.ab2xa_min = 0.0
        self.ab2xa_max = 0.0
        self.bc2ab_min = 0.0
        self.bc2ab_max = 0.0
        self.cd2bc_min = 0.0
        self.cd2bc_max = 0.0
        self.ad2xa_min = 0.0
        self.ad2xa_max = 0.0
        self.cd2xc_min = 0.0
        self.cd2xc_max = 0.0
        self.xc2xa_min = 0.0
        self.xc2xa_max = 0.0
        self.cd2ab_min = 0.0
        self.cd2ab_max = 0.0
        self.bc2xa_min = 0.0
        self.bc2xa_max = 0.0
        self.cd2ad_min = 0.0
        self.cd2ad_max = 0.0

class CHPFMatcher(MqlObject):
    _q_fields = ('m_slackUnary', 'm_slackRange', 'm_matchProcessor')
    _q_ptrs = ('m_matchProcessor',)
    def __init__(self, *args):
        self.m_slackUnary = 0.0
        self.m_slackRange = 0.0
        self.m_matchProcessor = None
    def SetSlackUnary(self, slack):
        self.m_slackUnary = slack
    def SetSlackRange(self, slack):
        self.m_slackRange = slack
    def SetMatchProcessor(self, matchProcessor):
        self.m_matchProcessor = matchProcessor
    def FindPattern(self, pattern, startBar, endBar, lastPeak, lastTrough, peaks, troughs):
        ab2xaConstraint = pattern.ab2xa_max != 0 and pattern.ab2xa_min != 0
        ad2xaConstraint = pattern.ad2xa_max != 0 and pattern.ad2xa_min != 0
        bc2abConstraint = pattern.bc2ab_max != 0 and pattern.bc2ab_min != 0
        cd2bcConstraint = pattern.cd2bc_max != 0 and pattern.cd2bc_min != 0
        cd2xcConstraint = pattern.cd2xc_max != 0 and pattern.cd2xc_min != 0
        xc2xaConstraint = pattern.xc2xa_max != 0 and pattern.xc2xa_min != 0
        cd2abConstraint = pattern.cd2ab_max != 0 and pattern.cd2ab_min != 0
        bc2xaConstraint = pattern.bc2xa_max != 0 and pattern.bc2xa_min != 0
        ab2xaSlack = (self.m_slackUnary if (pattern.ab2xa_max == pattern.ab2xa_min) else self.m_slackRange)
        ad2xaSlack = (self.m_slackUnary if (pattern.ad2xa_max == pattern.ad2xa_min) else self.m_slackRange)
        bc2abSlack = (self.m_slackUnary if (pattern.bc2ab_max == pattern.bc2ab_min) else self.m_slackRange)
        cd2bcSlack = (self.m_slackUnary if (pattern.cd2bc_max == pattern.cd2bc_min) else self.m_slackRange)
        cd2xcSlack = (self.m_slackUnary if (pattern.cd2xc_max == pattern.cd2xc_min) else self.m_slackRange)
        xc2xaSlack = (self.m_slackUnary if (pattern.xc2xa_max == pattern.xc2xa_min) else self.m_slackRange)
        cd2abSlack = (self.m_slackUnary if (pattern.cd2ab_max == pattern.cd2ab_min) else self.m_slackRange)
        bc2xaSlack = (self.m_slackUnary if (pattern.bc2xa_max == pattern.bc2xa_min) else self.m_slackRange)
        xFirstRun = True
        XIndex = startBar
        while XIndex <= endBar:
            if XIndex <= 0:
                XIndex += 1
                continue
            isPeak = peaks[XIndex] != 0 and peaks[XIndex] != EMPTY_VALUE
            isTrough = troughs[XIndex] != 0 and troughs[XIndex] != EMPTY_VALUE
            if (not isPeak) and (not isTrough):
                XIndex += 1
                continue
            startsInTrough = isTrough
            xVerticalZZ = isPeak and isTrough
            xZZDirection = not startsInTrough
            if xVerticalZZ:
                if xFirstRun:
                    startsInTrough = not startsInTrough
                zzDirection = ZigZagDirection(XIndex, peaks, troughs)
                if zzDirection == 0:
                    XIndex += 1
                    continue
                elif zzDirection == -1:
                    xZZDirection = False
                elif zzDirection == 1:
                    xZZDirection = True
            X = (troughs[XIndex] if startsInTrough else peaks[XIndex])
            extremeA = (DBL_MIN if startsInTrough else DBL_MAX)
            aSkip = 0
            if xVerticalZZ and ((xZZDirection and (not startsInTrough)) or ((not xZZDirection) and startsInTrough)):
                aSkip = 1
            for AIndex in range(XIndex + aSkip, endBar + 1):
                if XIndex != AIndex:
                    notExtreme = (startsInTrough and (troughs[AIndex - 1] != 0 and troughs[AIndex - 1] != EMPTY_VALUE)) and troughs[AIndex - 1] < X
                    notExtreme |= ((not startsInTrough) and (peaks[AIndex - 1] != 0 and peaks[AIndex - 1] != EMPTY_VALUE)) and peaks[AIndex - 1] > X
                    if (troughs[AIndex] != 0 and troughs[AIndex] != EMPTY_VALUE) and (peaks[AIndex] != 0 and peaks[AIndex] != EMPTY_VALUE):
                        notExtreme |= (startsInTrough and ZigZagDirection(AIndex, peaks, troughs) == 1) and troughs[AIndex] < X
                        notExtreme |= ((not startsInTrough) and ZigZagDirection(AIndex, peaks, troughs) == -1) and peaks[AIndex] > X
                    if notExtreme:
                        break
                A = (peaks[AIndex] if startsInTrough else troughs[AIndex])
                if ((not (A != 0 and A != EMPTY_VALUE)) or (startsInTrough and A < extremeA)) or ((not startsInTrough) and A > extremeA):
                    continue
                extremeA = A
                XA = MathAbs(A - X)
                if XA == 0:
                    continue
                extremeB = (DBL_MAX if startsInTrough else DBL_MIN)
                bSkip = 0
                if XIndex == AIndex:
                    bSkip = 1
                for BIndex in range(AIndex + bSkip, endBar + 1):
                    extremeIndexAB = (BIndex if (AIndex == BIndex) else (BIndex - 1))
                    if (((not startsInTrough) and (troughs[extremeIndexAB] != 0 and troughs[extremeIndexAB] != EMPTY_VALUE)) and troughs[extremeIndexAB] < A) or ((startsInTrough and (peaks[extremeIndexAB] != 0 and peaks[extremeIndexAB] != EMPTY_VALUE)) and peaks[extremeIndexAB] > A):
                        break
                    if ((AIndex != BIndex and (troughs[BIndex] != 0 and troughs[BIndex] != EMPTY_VALUE)) and (peaks[BIndex] != 0 and peaks[BIndex] != EMPTY_VALUE)) and ((((not startsInTrough) and ZigZagDirection(BIndex, peaks, troughs) == 1) and troughs[BIndex] < A) or ((startsInTrough and ZigZagDirection(BIndex, peaks, troughs) == -1) and peaks[BIndex] > A)):
                        break
                    B = (troughs[BIndex] if startsInTrough else peaks[BIndex])
                    if ((not (B != 0 and B != EMPTY_VALUE)) or (startsInTrough and B > extremeB)) or ((not startsInTrough) and B < extremeB):
                        continue
                    extremeB = B
                    if AIndex == BIndex:
                        zzDirection = ZigZagDirection(AIndex, peaks, troughs)
                        if zzDirection == 0:
                            continue
                        elif zzDirection == -1 and (not startsInTrough):
                            continue
                        elif zzDirection == 1 and startsInTrough:
                            continue
                    AB = MathAbs(A - B)
                    if AB == 0:
                        continue
                    ab2xaRatio = _fdiv(AB, XA)
                    ab2xaContinue = ab2xaConstraint
                    ab2xaContinue &= ab2xaRatio < (pattern.ab2xa_min - ab2xaSlack)
                    if ab2xaContinue:
                        continue
                    ab2xaCutoff = ab2xaConstraint
                    ab2xaCutoff &= ab2xaRatio > (pattern.ab2xa_max + ab2xaSlack)
                    if ab2xaCutoff:
                        break
                    extremeC = (DBL_MIN if startsInTrough else DBL_MAX)
                    cSkip = 0
                    if AIndex == BIndex:
                        cSkip = 1
                    for CIndex in range(BIndex + cSkip, endBar + 1):
                        extremeIndexBC = (CIndex if (BIndex == CIndex) else (CIndex - 1))
                        if ((startsInTrough and (troughs[extremeIndexBC] != 0 and troughs[extremeIndexBC] != EMPTY_VALUE)) and troughs[extremeIndexBC] < B) or (((not startsInTrough) and (peaks[extremeIndexBC] != 0 and peaks[extremeIndexBC] != EMPTY_VALUE)) and peaks[extremeIndexBC] > B):
                            break
                        if ((BIndex != CIndex and (troughs[CIndex] != 0 and troughs[CIndex] != EMPTY_VALUE)) and (peaks[CIndex] != 0 and peaks[CIndex] != EMPTY_VALUE)) and (((startsInTrough and ZigZagDirection(CIndex, peaks, troughs) == 1) and troughs[CIndex] < B) or (((not startsInTrough) and ZigZagDirection(CIndex, peaks, troughs) == -1) and peaks[CIndex] > B)):
                            break
                        C = (peaks[CIndex] if startsInTrough else troughs[CIndex])
                        if ((not (C != 0 and C != EMPTY_VALUE)) or (startsInTrough and C < extremeC)) or ((not startsInTrough) and C > extremeC):
                            continue
                        extremeC = C
                        if BIndex == CIndex:
                            zzDirection = ZigZagDirection(BIndex, peaks, troughs)
                            if zzDirection == 0:
                                continue
                            elif zzDirection == -1 and startsInTrough:
                                continue
                            elif zzDirection == 1 and (not startsInTrough):
                                continue
                        BC = MathAbs(C - B)
                        XC = MathAbs(X - C)
                        if BC == 0:
                            continue
                        if XC == 0:
                            continue
                        bc2abRatio = _fdiv(BC, AB)
                        xc2xaRatio = _fdiv(XC, XA)
                        bc2xaRatio = _fdiv(BC, XA)
                        bc2abContinue = bc2abConstraint
                        xc2xaContinue = xc2xaConstraint
                        bc2xaContinue = bc2xaConstraint
                        bc2abContinue &= bc2abRatio < (pattern.bc2ab_min - bc2abSlack)
                        xc2xaContinue &= xc2xaRatio < (pattern.xc2xa_min - xc2xaSlack)
                        bc2xaContinue &= bc2xaRatio < (pattern.bc2xa_min - bc2xaSlack)
                        if (bc2abContinue or xc2xaContinue) or bc2xaContinue:
                            continue
                        bc2abCutoff = bc2abConstraint
                        xc2xaCutoff = xc2xaConstraint
                        bc2xaCutoff = bc2xaConstraint
                        bc2abCutoff &= bc2abRatio > (pattern.bc2ab_max + bc2abSlack)
                        xc2xaCutoff &= xc2xaRatio > (pattern.xc2xa_max + xc2xaSlack)
                        bc2xaCutoff &= bc2xaRatio > (pattern.bc2xa_max + bc2xaSlack)
                        if (bc2abCutoff or xc2xaCutoff) or bc2xaCutoff:
                            break
                        lastExtremeC = True
                        for i in range(CIndex + 1, endBar + 1):
                            if ((startsInTrough and (peaks[i] != 0 and peaks[i] != EMPTY_VALUE)) and peaks[i] > C) or (((not startsInTrough) and (troughs[i] != 0 and troughs[i] != EMPTY_VALUE)) and troughs[i] < C):
                                lastExtremeC = False
                                break
                        nearD = Box(0.0)
                        farD = Box(0.0)
                        HarmonicWindow(pattern, self.m_slackUnary, self.m_slackRange, startsInTrough, X, A, B, C, nearD, farD)
                        if (startsInTrough and farD.v > nearD.v) or ((not startsInTrough) and farD.v < nearD.v):
                            continue
                        extremeD = (DBL_MAX if startsInTrough else DBL_MIN)
                        dSkip = 0
                        if BIndex == CIndex:
                            dSkip = 1
                        for DIndex in range(CIndex + dSkip, endBar + 1):
                            extremeIndexCD = (DIndex if (CIndex == DIndex) else (DIndex - 1))
                            if (((not startsInTrough) and (troughs[extremeIndexCD] != 0 and troughs[extremeIndexCD] != EMPTY_VALUE)) and troughs[extremeIndexCD] < C) or ((startsInTrough and (peaks[extremeIndexCD] != 0 and peaks[extremeIndexCD] != EMPTY_VALUE)) and peaks[extremeIndexCD] > C):
                                break
                            if ((CIndex != DIndex and (troughs[DIndex] != 0 and troughs[DIndex] != EMPTY_VALUE)) and (peaks[DIndex] != 0 and peaks[DIndex] != EMPTY_VALUE)) and ((((not startsInTrough) and ZigZagDirection(DIndex, peaks, troughs) == 1) and troughs[DIndex] < C) or ((startsInTrough and ZigZagDirection(DIndex, peaks, troughs) == -1) and peaks[DIndex] > C)):
                                break
                            imaginaryD = ((startsInTrough and CIndex == lastPeak) and lastTrough <= lastPeak) or (((not startsInTrough) and CIndex == lastTrough) and lastPeak <= lastTrough)
                            if imaginaryD and lastPeak == lastTrough:
                                imaginaryD &= (startsInTrough and ZigZagDirection(lastPeak, peaks, troughs) == 1) or ((not startsInTrough) and ZigZagDirection(lastPeak, peaks, troughs) == -1)
                            D = (troughs[DIndex] if startsInTrough else peaks[DIndex])
                            if (not imaginaryD) and (((not (D != 0 and D != EMPTY_VALUE)) or (startsInTrough and D > extremeD)) or ((not startsInTrough) and D < extremeD)):
                                continue
                            extremeD = D
                            if (not imaginaryD) and CIndex == DIndex:
                                zzDirection = ZigZagDirection(CIndex, peaks, troughs)
                                if zzDirection == 0:
                                    continue
                                elif zzDirection == -1 and (not startsInTrough):
                                    continue
                                elif zzDirection == 1 and startsInTrough:
                                    continue
                            lastExtremeD = True
                            if not imaginaryD:
                                for i in range(DIndex + 1, endBar + 1):
                                    if (((not startsInTrough) and (peaks[i] != 0 and peaks[i] != EMPTY_VALUE)) and peaks[i] > D) or ((startsInTrough and (troughs[i] != 0 and troughs[i] != EMPTY_VALUE)) and troughs[i] < D):
                                        lastExtremeD = False
                                        break
                            match = PATTERN_MATCH()
                            match.bullish = startsInTrough
                            match.XIndex = XIndex
                            match.AIndex = AIndex
                            match.BIndex = BIndex
                            match.CIndex = CIndex
                            match.DIndex = DIndex
                            match.X = X
                            match.A = A
                            match.B = B
                            match.C = C
                            match.nearD = nearD.v
                            match.farD = farD.v
                            if (imaginaryD or (startsInTrough and D > nearD.v)) or ((not startsInTrough) and D < nearD.v):
                                if (not lastExtremeC) or (not lastExtremeD):
                                    continue
                                self.m_matchProcessor.PatternUndershot(match)
                                break
                            elif (startsInTrough and D < farD.v) or ((not startsInTrough) and D > farD.v):
                                self.m_matchProcessor.PatternOvershot(match)
                                break
                            else:
                                self.m_matchProcessor.PatternMatched(match)
            if xVerticalZZ:
                if xFirstRun:
                    XIndex -= 1
                    xFirstRun = False
                else:
                    xFirstRun = True
            XIndex += 1

class PRZLevels(MqlObject):
    _q_fields = ('cd2bc', 'ad2xa', 'cd2xc', 'cd2ab', 'cd2ad')
    def __init__(self, *args):
        self.cd2bc = 0.0
        self.ad2xa = 0.0
        self.cd2xc = 0.0
        self.cd2ab = 0.0
        self.cd2ad = 0.0

class CHPFRingbuffer(MqlObject):
    _q_fields = ('m_matches', 'm_head', 'm_tail', 'm_capacity', 'm_duration')
    def __init__(self):
        self.m_matches = Arr(0, 0, factory=PATTERN_MATCH)
        self.m_head = 0
        self.m_tail = 0
        self.m_capacity = 0
        self.m_duration = 0
        self.m_capacity = 2
        self.m_duration = INT_MAX
        self.Reset()
        if ArrayResize(self.m_matches, self.m_capacity) < self.m_capacity:
            printf('Error allocating array at ' + 'CHPFRingbuffer::CHPFRingbuffer' + ' code: ' + IntegerToString(GetLastError()))
    def _q_dtor(self):
        ArrayFree(self.m_matches)
    def GetHead(self):
        return self.m_head
    def GetTail(self):
        return self.m_tail
    def GetCapacity(self):
        return self.m_capacity
    def GetMatch(self, i):
        return _copy(self.m_matches[i])
    def SetDuration(self, duration):
        self.m_duration = duration
    def Reset(self):
        self.m_head = 0
        self.m_tail = self.m_head
    def Add(self, match):
        _assign(self.m_matches[self.m_head], match)
        self.m_head = _imod(self.m_head + 1, self.m_capacity)
        if self.m_head == self.m_tail:
            if MathAbs(match.DIndex - self.m_matches[self.m_tail].DIndex) > self.m_duration:
                self.m_tail = _imod(self.m_tail + 1, self.m_capacity)
            else:
                for rounds in range(0, self.m_tail):
                    tmp = _copy(self.m_matches[0])
                    for i in range(0, self.m_capacity - 1):
                        _assign(self.m_matches[i], self.m_matches[i + 1])
                    _assign(self.m_matches[self.m_capacity - 1], tmp)
                self.m_tail = 0
                self.m_head = self.m_capacity
                self.m_capacity *= 2
                if ArrayResize(self.m_matches, self.m_capacity) < self.m_capacity:
                    printf('Error allocating array at ' + 'CHPFRingbuffer::Add' + ' code: ' + IntegerToString(GetLastError()))
    def SortNearD(self):
        i = _imod(self.m_tail + 1, self.m_capacity)
        while i != self.m_head:
            j = i
            jminus1 = _imod(_imod(j - 1, self.m_capacity) + self.m_capacity, self.m_capacity)
            while j != self.m_tail and self.m_matches[jminus1].nearD > self.m_matches[j].nearD:
                tmp = _copy(self.m_matches[j])
                _assign(self.m_matches[j], self.m_matches[jminus1])
                _assign(self.m_matches[jminus1], tmp)
                j = jminus1
                jminus1 = _imod(_imod(j - 1, self.m_capacity) + self.m_capacity, self.m_capacity)
            i = _imod(i + 1, self.m_capacity)
    def SortDIndex(self):
        i = _imod(self.m_tail + 1, self.m_capacity)
        while i != self.m_head:
            j = i
            jminus1 = _imod(_imod(j - 1, self.m_capacity) + self.m_capacity, self.m_capacity)
            while j != self.m_tail and self.m_matches[jminus1].DIndex > self.m_matches[j].DIndex:
                tmp = _copy(self.m_matches[j])
                _assign(self.m_matches[j], self.m_matches[jminus1])
                _assign(self.m_matches[jminus1], tmp)
                j = jminus1
                jminus1 = _imod(_imod(j - 1, self.m_capacity) + self.m_capacity, self.m_capacity)
            i = _imod(i + 1, self.m_capacity)

class CHPFObserver(MqlObject):
    _q_fields = ()
    def __init__(self, *args):
        pass
    def Reset(self):
        pass
    def NotifyTransientMatch(self, patternIndex, match):
        pass
    def NotifyPersistentMatch(self, patternIndex, match):
        pass
    def NotifyStandardProjection(self, patternIndex, match):
        pass
    def NotifyOneAheadProjection(self, patternIndex, match):
        pass
    def NotifyOvershot(self, patternIndex, match):
        pass

class CHPFFilter(MqlObject):
    _q_fields = ()
    def __init__(self, *args):
        pass
    def IsValidUndershot(self, patternIndex, match):
        pass
    def IsValidMatched(self, patternIndex, match):
        pass
    def IsValidOvershot(self, patternIndex, match):
        pass

class CHPFIndicator(CHPFMatchProcessor):
    _q_fields = ('m_undershot', 'm_matched', 'm_overshot', 'm_matchedPersistent', 'm_matchedTransient', 'm_overshotPersistent', 'm_maxOverlap', 'm_num4PointPatterns', 'm_patternIndex', 'm_observer', 'm_filter')
    _q_ptrs = ('m_observer', 'm_filter',)
    def __init__(self, numPatterns, num4PointPatterns, duration):
        CHPFMatchProcessor.__init__(self)
        self.m_undershot = CHPFRingbuffer()
        self.m_matched = CHPFRingbuffer()
        self.m_overshot = CHPFRingbuffer()
        self.m_matchedPersistent = Arr(0, 0, factory=CHPFRingbuffer)
        self.m_matchedTransient = Arr(0, 0, factory=CHPFRingbuffer)
        self.m_overshotPersistent = Arr(0, 0, factory=CHPFRingbuffer)
        self.m_maxOverlap = 0
        self.m_num4PointPatterns = 0
        self.m_patternIndex = 0
        self.m_observer = None
        self.m_filter = None
        if ArrayResize(self.m_matchedPersistent, numPatterns) < numPatterns:
            printf('Error allocating array at ' + 'CHPFIndicator::CHPFIndicator' + ' code: ' + IntegerToString(GetLastError()))
        if ArrayResize(self.m_matchedTransient, numPatterns) < numPatterns:
            printf('Error allocating array at ' + 'CHPFIndicator::CHPFIndicator' + ' code: ' + IntegerToString(GetLastError()))
        if ArrayResize(self.m_overshotPersistent, numPatterns) < numPatterns:
            printf('Error allocating array at ' + 'CHPFIndicator::CHPFIndicator' + ' code: ' + IntegerToString(GetLastError()))
        for i in range(0, numPatterns):
            self.m_matchedPersistent[i].SetDuration(duration)
            self.m_overshotPersistent[i].SetDuration(duration)
        self.m_maxOverlap = 0
        self.m_num4PointPatterns = num4PointPatterns
        self.m_observer = None
    def _q_dtor(self):
        ArrayFree(self.m_matchedPersistent)
        ArrayFree(self.m_matchedTransient)
        ArrayFree(self.m_overshotPersistent)
    def SetMaxOverlap(self, maxOverlap):
        self.m_maxOverlap = maxOverlap
    def Is4PointPattern(self, index):
        return index < self.m_num4PointPatterns
    def GetMatchedPersistent(self, patternIndex):
        return self.m_matchedPersistent[patternIndex]
    def GetMatchedTransient(self, patternIndex):
        return self.m_matchedTransient[patternIndex]
    def SetObserver(self, observer):
        self.m_observer = observer
    def SetFilter(self, filter_):
        self.m_filter = filter_
    def ClearTransient(self):
        self.m_undershot.Reset()
        self.m_matched.Reset()
        self.m_overshot.Reset()
        i = 0
        while i < ArraySize(self.m_matchedTransient):
            self.m_matchedTransient[i].Reset()
            i += 1
    def Reset(self):
        self.m_observer.Reset()
        self.ClearTransient()
        i = 0
        while i < ArraySize(self.m_matchedPersistent):
            self.m_matchedPersistent[i].Reset()
            self.m_overshotPersistent[i].Reset()
            i += 1
    def PreFind(self, patternIndex):
        self.m_patternIndex = patternIndex
    def PostFind(self, patternIndex, lastPeak, lastTrough, endsInTrough):
        self.m_matched.SortDIndex()
        tail = self.m_matched.GetTail()
        head = self.m_matched.GetHead()
        capacity = self.m_matched.GetCapacity()
        i = tail
        while i != head:
            match = self.m_matched.GetMatch(i)
            if not self.Overlaps(patternIndex, match):
                bullish = match.bullish
                DIndex = match.DIndex
                activeSwing = (endsInTrough and bullish) and DIndex == lastTrough
                activeSwing |= ((not endsInTrough) and (not bullish)) and DIndex == lastPeak
                if activeSwing:
                    self.m_matchedTransient[patternIndex].Add(match)
                    self.m_observer.NotifyTransientMatch(patternIndex, match)
                else:
                    self.m_matchedPersistent[patternIndex].Add(match)
                    self.m_observer.NotifyPersistentMatch(patternIndex, match)
            i = _imod(i + 1, capacity)
        self.m_undershot.SortNearD()
        tail = self.m_undershot.GetTail()
        head = self.m_undershot.GetHead()
        capacity = self.m_undershot.GetCapacity()
        i = tail
        while i != head:
            match = self.m_undershot.GetMatch(i)
            bullish = match.bullish
            CIndex = match.CIndex
            DIndex = match.DIndex
            match.DIndex = -1
            if (not bullish) and (not self.Overlaps(patternIndex, match)):
                nonOverlapping = True
                if i != tail:
                    j = _imod(_imod(i - 1, capacity) + capacity, capacity)
                    while True:
                        match2 = self.m_undershot.GetMatch(j)
                        match2.DIndex = -1
                        if (not match2.bullish) and (not self.Overlaps(patternIndex, match2)):
                            numMatches = 0
                            if (not self.Is4PointPattern(patternIndex)) and match2.XIndex == match.XIndex:
                                numMatches += 1
                            if match2.AIndex == match.AIndex:
                                numMatches += 1
                            if match2.BIndex == match.BIndex:
                                numMatches += 1
                            if match2.CIndex == match.CIndex:
                                numMatches += 1
                            if numMatches > self.m_maxOverlap:
                                nonOverlapping = False
                                break
                        if j == tail:
                            break
                        j = _imod(_imod(j - 1, capacity) + capacity, capacity)
                if nonOverlapping:
                    match.DIndex = DIndex
                    imaginaryD = ((bullish and CIndex == lastPeak) and lastTrough <= lastPeak) or (((not bullish) and CIndex == lastTrough) and lastPeak <= lastTrough)
                    if imaginaryD and lastPeak == lastTrough:
                        imaginaryD &= (bullish and (not endsInTrough)) or ((not bullish) and endsInTrough)
                    if imaginaryD:
                        self.m_observer.NotifyOneAheadProjection(patternIndex, match)
                    else:
                        self.m_observer.NotifyStandardProjection(patternIndex, match)
            i = _imod(i + 1, capacity)
        if head != tail:
            i = _imod(_imod(head - 1, capacity) + capacity, capacity)
            while True:
                match = self.m_undershot.GetMatch(i)
                bullish = match.bullish
                CIndex = match.CIndex
                DIndex = match.DIndex
                match.DIndex = -1
                if bullish and (not self.Overlaps(patternIndex, match)):
                    nonOverlapping = True
                    if i != _imod(_imod(head - 1, capacity) + capacity, capacity):
                        j = _imod(i + 1, capacity)
                        while j != head:
                            match2 = self.m_undershot.GetMatch(j)
                            match2.DIndex = -1
                            if match2.bullish and (not self.Overlaps(patternIndex, match2)):
                                numMatches = 0
                                if (not self.Is4PointPattern(patternIndex)) and match2.XIndex == match.XIndex:
                                    numMatches += 1
                                if match2.AIndex == match.AIndex:
                                    numMatches += 1
                                if match2.BIndex == match.BIndex:
                                    numMatches += 1
                                if match2.CIndex == match.CIndex:
                                    numMatches += 1
                                if numMatches > self.m_maxOverlap:
                                    nonOverlapping = False
                                    break
                            j = _imod(j + 1, capacity)
                    if nonOverlapping:
                        match.DIndex = DIndex
                        imaginaryD = ((bullish and CIndex == lastPeak) and lastTrough <= lastPeak) or (((not bullish) and CIndex == lastTrough) and lastPeak <= lastTrough)
                        if imaginaryD and lastPeak == lastTrough:
                            imaginaryD &= (bullish and (not endsInTrough)) or ((not bullish) and endsInTrough)
                        if imaginaryD:
                            self.m_observer.NotifyOneAheadProjection(patternIndex, match)
                        else:
                            self.m_observer.NotifyStandardProjection(patternIndex, match)
                if i == tail:
                    break
                i = _imod(_imod(i - 1, capacity) + capacity, capacity)
        self.m_overshot.SortDIndex()
        tail = self.m_overshot.GetTail()
        head = self.m_overshot.GetHead()
        capacity = self.m_overshot.GetCapacity()
        i = tail
        while i != head:
            match = self.m_overshot.GetMatch(i)
            if (not self.Overlaps(patternIndex, match)) and (not self.OverlapsOvershot(patternIndex, match)):
                self.m_overshotPersistent[patternIndex].Add(match)
                self.m_observer.NotifyOvershot(patternIndex, match)
            i = _imod(i + 1, capacity)
        self.m_undershot.Reset()
        self.m_matched.Reset()
        self.m_overshot.Reset()
    def Overlaps(self, patternIndex, match):
        tail = self.m_matchedPersistent[patternIndex].GetTail()
        head = self.m_matchedPersistent[patternIndex].GetHead()
        capacity = self.m_matchedPersistent[patternIndex].GetCapacity()
        i = tail
        while i != head:
            numMatches = 0
            stored = self.m_matchedPersistent[patternIndex].GetMatch(i)
            if (not self.Is4PointPattern(patternIndex)) and stored.XIndex == match.XIndex:
                numMatches += 1
            if stored.AIndex == match.AIndex:
                numMatches += 1
            if stored.BIndex == match.BIndex:
                numMatches += 1
            if stored.CIndex == match.CIndex:
                numMatches += 1
            if numMatches >= (3 + (0 if self.Is4PointPattern(patternIndex) else 1)):
                return True
            if stored.DIndex == match.DIndex:
                numMatches += 1
            if numMatches > self.m_maxOverlap:
                return True
            i = _imod(i + 1, capacity)
        tail = self.m_matchedTransient[patternIndex].GetTail()
        head = self.m_matchedTransient[patternIndex].GetHead()
        capacity = self.m_matchedTransient[patternIndex].GetCapacity()
        i = tail
        while i != head:
            numMatches = 0
            stored = self.m_matchedTransient[patternIndex].GetMatch(i)
            if (not self.Is4PointPattern(patternIndex)) and stored.XIndex == match.XIndex:
                numMatches += 1
            if stored.AIndex == match.AIndex:
                numMatches += 1
            if stored.BIndex == match.BIndex:
                numMatches += 1
            if stored.CIndex == match.CIndex:
                numMatches += 1
            if numMatches >= (3 + (0 if self.Is4PointPattern(patternIndex) else 1)):
                return True
            if stored.DIndex == match.DIndex:
                numMatches += 1
            if numMatches > self.m_maxOverlap:
                return True
            i = _imod(i + 1, capacity)
        return False
    def OverlapsOvershot(self, patternIndex, match):
        tail = self.m_overshotPersistent[patternIndex].GetTail()
        head = self.m_overshotPersistent[patternIndex].GetHead()
        capacity = self.m_overshotPersistent[patternIndex].GetCapacity()
        i = tail
        while i != head:
            numMatches = 0
            stored = self.m_overshotPersistent[patternIndex].GetMatch(i)
            if (not self.Is4PointPattern(patternIndex)) and stored.XIndex == match.XIndex:
                numMatches += 1
            if stored.AIndex == match.AIndex:
                numMatches += 1
            if stored.BIndex == match.BIndex:
                numMatches += 1
            if stored.CIndex == match.CIndex:
                numMatches += 1
            if numMatches >= (3 + (0 if self.Is4PointPattern(patternIndex) else 1)):
                return True
            if stored.DIndex == match.DIndex:
                numMatches += 1
            if numMatches > self.m_maxOverlap:
                return True
            i = _imod(i + 1, capacity)
        return False
    def PersistTransient(self):
        k = 0
        while k < ArraySize(self.m_matchedPersistent):
            tail = self.m_matchedTransient[k].GetTail()
            head = self.m_matchedTransient[k].GetHead()
            capacity = self.m_matchedTransient[k].GetCapacity()
            j = tail
            while j != head:
                match = self.m_matchedTransient[k].GetMatch(j)
                self.m_matchedPersistent[k].Add(match)
                self.m_observer.NotifyPersistentMatch(k, match)
                j = _imod(j + 1, capacity)
            k += 1
    def PatternUndershot(self, match):
        if self.m_filter.IsValidUndershot(self.m_patternIndex, match):
            self.m_undershot.Add(match)
    def PatternMatched(self, match):
        if self.m_filter.IsValidMatched(self.m_patternIndex, match):
            self.m_matched.Add(match)
    def PatternOvershot(self, match):
        if self.m_filter.IsValidOvershot(self.m_patternIndex, match):
            self.m_overshot.Add(match)

class CHPFStatisticsObserver(CHPFObserver):
    _q_fields = ('m_failures', 'm_successes')
    def __init__(self, numPatterns):
        CHPFObserver.__init__(self)
        self.m_failures = Arr(0, 0)
        self.m_successes = Arr(0, 0)
        if ArrayResize(self.m_successes, numPatterns) < numPatterns:
            printf('Error allocating array at ' + 'CHPFStatisticsObserver::CHPFStatisticsObserver' + ' code: ' + IntegerToString(GetLastError()))
        if ArrayResize(self.m_failures, numPatterns) < numPatterns:
            printf('Error allocating array at ' + 'CHPFStatisticsObserver::CHPFStatisticsObserver' + ' code: ' + IntegerToString(GetLastError()))
        self.Reset()
    def _q_dtor(self):
        ArrayFree(self.m_successes)
        ArrayFree(self.m_failures)
    def GetSuccesses(self, patternIndex):
        return self.m_successes[patternIndex]
    def GetFailures(self, patternIndex):
        return self.m_failures[patternIndex]
    def Reset(self):
        for i in range(0, ArraySize(self.m_successes)):
            self.m_successes[i] = 0
            self.m_failures[i] = 0
    def GetSuccessRate(self, patternIndex):
        success = self.m_successes[patternIndex]
        total = success + self.m_failures[patternIndex]
        if total != 0:
            return _fdiv(success, total)
        else:
            return -1.0
    def NotifyTransientMatch(self, patternIndex, match):
        pass
    def NotifyPersistentMatch(self, patternIndex, match):
        self.m_successes[patternIndex] = self.m_successes[patternIndex] + 1
    def NotifyStandardProjection(self, patternIndex, match):
        pass
    def NotifyOneAheadProjection(self, patternIndex, match):
        pass
    def NotifyOvershot(self, patternIndex, match):
        self.m_failures[patternIndex] = self.m_failures[patternIndex] + 1

class CHPFObserverList(CHPFObserver):
    _q_fields = ('m_observers',)
    _q_ptrs = ('m_observers',)
    def __init__(self, size):
        CHPFObserver.__init__(self)
        self.m_observers = Arr(0, None)
        if ArrayResize(self.m_observers, size) < size:
            printf('Error allocating array at ' + 'CHPFObserverList::CHPFObserverList' + ' code: ' + IntegerToString(GetLastError()))
    def _q_dtor(self):
        ArrayFree(self.m_observers)
    def Set(self, index, observer):
        self.m_observers[index] = observer
    def Reset(self):
        i = 0
        while i < ArraySize(self.m_observers):
            self.m_observers[i].Reset()
            i += 1
    def NotifyTransientMatch(self, patternIndex, match):
        i = 0
        while i < ArraySize(self.m_observers):
            self.m_observers[i].NotifyTransientMatch(patternIndex, match)
            i += 1
    def NotifyPersistentMatch(self, patternIndex, match):
        i = 0
        while i < ArraySize(self.m_observers):
            self.m_observers[i].NotifyPersistentMatch(patternIndex, match)
            i += 1
    def NotifyStandardProjection(self, patternIndex, match):
        i = 0
        while i < ArraySize(self.m_observers):
            self.m_observers[i].NotifyStandardProjection(patternIndex, match)
            i += 1
    def NotifyOneAheadProjection(self, patternIndex, match):
        i = 0
        while i < ArraySize(self.m_observers):
            self.m_observers[i].NotifyOneAheadProjection(patternIndex, match)
            i += 1
    def NotifyOvershot(self, patternIndex, match):
        i = 0
        while i < ArraySize(self.m_observers):
            self.m_observers[i].NotifyOvershot(patternIndex, match)
            i += 1

class CHPFCommentObserver(CHPFObserver):
    _q_fields = ('m_buffer', 'm_statistics', 'm_com1', 'm_com2', 'm_com3', 'm_com4', 'm_com5', 'm_com6', 'm_com7', 'm_com8', 'm_com9', 'm_comment')
    _q_ptrs = ('m_statistics',)
    def __init__(self, numPatterns, duration, showComment):
        CHPFObserver.__init__(self)
        self.m_buffer = Arr(0, 0, factory=CHPFRingbuffer)
        self.m_statistics = None
        self.m_com1 = ""
        self.m_com2 = ""
        self.m_com3 = ""
        self.m_com4 = ""
        self.m_com5 = ""
        self.m_com6 = ""
        self.m_com7 = ""
        self.m_com8 = ""
        self.m_com9 = ""
        self.m_comment = False
        if ArrayResize(self.m_buffer, numPatterns) < numPatterns:
            printf('Error allocating array at ' + 'CHPFCommentObserver::CHPFCommentObserver' + ' code: ' + IntegerToString(GetLastError()))
        for i in range(0, numPatterns):
            self.m_buffer[i].SetDuration(duration)
        self.m_comment = showComment
    def _q_dtor(self):
        ArrayFree(self.m_buffer)
    def SetStatistics(self, observer):
        self.m_statistics = observer
    def ShowComment(self, sComment):
        if self.m_comment:
            if sComment != self.m_com1:
                self.m_com9 = self.m_com8
                self.m_com8 = self.m_com7
                self.m_com7 = self.m_com6
                self.m_com6 = self.m_com5
                self.m_com5 = self.m_com4
                self.m_com4 = self.m_com3
                self.m_com3 = self.m_com2
                self.m_com2 = self.m_com1
                self.m_com1 = sComment
            Comment('HarmonicPatternFinderV3 © 2018', '\n', '\n', self.m_com1, '\n', self.m_com2, '\n', self.m_com3, '\n', self.m_com4, '\n', self.m_com5, '\n', self.m_com6, '\n', self.m_com7, '\n', self.m_com8, '\n', self.m_com9, '\n')
    def Reset(self):
        i = 0
        while i < ArraySize(self.m_buffer):
            self.m_buffer[i].Reset()
            i += 1
    def NotifyTransientMatch(self, patternIndex, match):
        bullish = match.bullish
        DIndex = match.DIndex
        DDateTime = _time[DIndex]
        tail = self.m_buffer[patternIndex].GetTail()
        head = self.m_buffer[patternIndex].GetHead()
        capacity = self.m_buffer[patternIndex].GetCapacity()
        i = tail
        while i != head:
            numMatches = 0
            stored = self.m_buffer[patternIndex].GetMatch(i)
            if (not Is4PointPattern(patternIndex)) and stored.XIndex == match.XIndex:
                numMatches += 1
            if stored.AIndex == match.AIndex:
                numMatches += 1
            if stored.BIndex == match.BIndex:
                numMatches += 1
            if stored.CIndex == match.CIndex:
                numMatches += 1
            if numMatches >= (3 + (0 if Is4PointPattern(patternIndex) else 1)):
                return
            i = _imod(i + 1, capacity)
        self.m_buffer[patternIndex].Add(match)
        comment = ('T. Bull. ' if bullish else 'T. Bear. ')
        comment += _patternNames[patternIndex]
        comment += ' @ ' + TimeToString(DDateTime)
        comment += ' Prob. ' + DoubleToString(self.m_statistics.GetSuccessRate(patternIndex) * 100, 2)
        self.ShowComment(comment)
    def NotifyPersistentMatch(self, patternIndex, match):
        bullish = match.bullish
        DIndex = match.DIndex
        DDateTime = _time[DIndex]
        comment = ('P. Bull. ' if bullish else 'P. Bear. ')
        comment += _patternNames[patternIndex]
        comment += ' @ ' + TimeToString(DDateTime)
        comment += ' Prob. ' + DoubleToString(self.m_statistics.GetSuccessRate(patternIndex) * 100, 2)
        self.ShowComment(comment)
    def NotifyStandardProjection(self, patternIndex, match):
        pass
    def NotifyOneAheadProjection(self, patternIndex, match):
        pass
    def NotifyOvershot(self, patternIndex, match):
        bullish = match.bullish
        DIndex = match.DIndex
        DDateTime = _time[DIndex]
        comment = ('O. Bull. ' if bullish else 'O. Bear. ')
        comment += _patternNames[patternIndex]
        comment += ' @ ' + TimeToString(DDateTime)
        comment += ' Prob. ' + DoubleToString(self.m_statistics.GetSuccessRate(patternIndex) * 100, 2)
        self.ShowComment(comment)

class CHPFDrawingObserver(CHPFObserver):
    _q_fields = ('m_bar',)
    def __init__(self, *args):
        CHPFObserver.__init__(self)
        self.m_bar = 0
    def Reset(self):
        pass
    def SetBar(self, bar):
        self.m_bar = bar
    def NotifyTransientMatch(self, patternIndex, match):
        bullish = match.bullish
        XIndex = match.XIndex
        AIndex = match.AIndex
        BIndex = match.BIndex
        CIndex = match.CIndex
        DIndex = match.DIndex
        nearD = match.nearD
        farD = match.farD
        X = (_troughs[XIndex] if bullish else _peaks[XIndex])
        A = (_peaks[AIndex] if bullish else _troughs[AIndex])
        B = (_troughs[BIndex] if bullish else _peaks[BIndex])
        C = (_peaks[CIndex] if bullish else _troughs[CIndex])
        D = (_troughs[DIndex] if bullish else _peaks[DIndex])
        XDateTime = _time[XIndex]
        ADateTime = _time[AIndex]
        BDateTime = _time[BIndex]
        CDateTime = _time[CIndex]
        DDateTime = _time[DIndex]
        if _indicator.Is4PointPattern(patternIndex):
            self.DisplayPattern_11(patternIndex, bullish, AIndex, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D)
            self.DisplayPRZ_10(patternIndex, bullish, ADateTime, A, BDateTime, CDateTime, C, DDateTime, D, farD)
        else:
            self.DisplayPattern_13(patternIndex, bullish, XIndex, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D)
            self.DisplayPRZ_12(patternIndex, bullish, XDateTime, X, ADateTime, A, BDateTime, CDateTime, C, DDateTime, D, farD)
    def NotifyPersistentMatch(self, patternIndex, match):
        if not i_oldPatterns:
            return
        bullish = match.bullish
        XIndex = match.XIndex
        AIndex = match.AIndex
        BIndex = match.BIndex
        CIndex = match.CIndex
        DIndex = match.DIndex
        nearD = match.nearD
        farD = match.farD
        X = (_troughs[XIndex] if bullish else _peaks[XIndex])
        A = (_peaks[AIndex] if bullish else _troughs[AIndex])
        B = (_troughs[BIndex] if bullish else _peaks[BIndex])
        C = (_peaks[CIndex] if bullish else _troughs[CIndex])
        D = (_troughs[DIndex] if bullish else _peaks[DIndex])
        XDateTime = _time[XIndex]
        ADateTime = _time[AIndex]
        BDateTime = _time[BIndex]
        CDateTime = _time[CIndex]
        DDateTime = _time[DIndex]
        if _indicator.Is4PointPattern(patternIndex):
            self.DisplayPattern_11(patternIndex, bullish, AIndex, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D)
        else:
            self.DisplayPattern_13(patternIndex, bullish, XIndex, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D)
    def NotifyStandardProjection(self, patternIndex, match):
        if i_emergingPatterns:
            bullish = match.bullish
            XIndex = match.XIndex
            AIndex = match.AIndex
            BIndex = match.BIndex
            CIndex = match.CIndex
            DIndex = match.DIndex
            X = (_troughs[XIndex] if bullish else _peaks[XIndex])
            A = (_peaks[AIndex] if bullish else _troughs[AIndex])
            B = (_troughs[BIndex] if bullish else _peaks[BIndex])
            C = (_peaks[CIndex] if bullish else _troughs[CIndex])
            XDateTime = _time[XIndex]
            ADateTime = _time[AIndex]
            BDateTime = _time[BIndex]
            CDateTime = _time[CIndex]
            DDateTime = _time[DIndex]
            nearD = match.nearD
            if _indicator.Is4PointPattern(patternIndex):
                self.DisplayProjection_10(patternIndex, bullish, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, nearD)
            else:
                self.DisplayProjection_12(patternIndex, bullish, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, nearD)
    def NotifyOneAheadProjection(self, patternIndex, match):
        if i_oneAheadProjection:
            self.NotifyStandardProjection(patternIndex, match)
    def NotifyOvershot(self, patternIndex, match):
        pass
    def DisplayPRZ_10(self, k, bullish, ADateTime, A, BDateTime, CDateTime, C, DDateTime, D, farD):
        unique = UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime)
        prefix = ('Bullish ' if bullish else 'Bearish ')
        prefixName = (('U ' + _identifier) if bullish else ('D ' + _identifier))
        name = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PRZ' + unique
        ObjectCreate(0, name, OBJ_TREND, 0, DDateTime - 1, farD, DDateTime, farD)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, True)
        ObjectSetInteger(0, name, OBJPROP_COLOR, (i_clrBull4P if bullish else i_clrBear4P))
        ObjectSetInteger(0, name, OBJPROP_STYLE, i_stylePRZ)
        ObjectSetString(0, name, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PRZ stop ' + DoubleToString(NormalizeDouble(farD, Digits()), Digits()))
    def DisplayPRZ_12(self, k, bullish, XDateTime, X, ADateTime, A, BDateTime, CDateTime, C, DDateTime, D, farD):
        unique = UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime)
        prefix = ('Bullish ' if bullish else 'Bearish ')
        prefixName = (('U ' + _identifier) if bullish else ('D ' + _identifier))
        name = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PRZ' + unique
        ObjectCreate(0, name, OBJ_TREND, 0, DDateTime - 1, farD, DDateTime, farD)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, True)
        ObjectSetInteger(0, name, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
        ObjectSetInteger(0, name, OBJPROP_STYLE, i_stylePRZ)
        ObjectSetString(0, name, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PRZ stop ' + DoubleToString(NormalizeDouble(farD, Digits()), Digits()))
    def DisplayPattern_11(self, k, bullish, AIndex, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
        unique = UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime)
        prefix = ('Bullish ' if bullish else 'Bearish ')
        prefixName = (('U ' + _identifier) if bullish else ('D ' + _identifier))
        name0 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' AB' + unique
        name1 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BC' + unique
        name2 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' CD' + unique
        pointA = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PA' + unique
        pointB = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PB' + unique
        pointC = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PC' + unique
        pointD = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PD' + unique
        ObjectCreate(0, name0, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
        ObjectCreate(0, name1, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
        ObjectCreate(0, name2, OBJ_ARROWED_LINE, 0, CDateTime, C, DDateTime, D)
        ObjectSetInteger(0, name0, OBJPROP_COLOR, (i_clrBull4P if bullish else i_clrBear4P))
        ObjectSetInteger(0, name1, OBJPROP_COLOR, (i_clrBull4P if bullish else i_clrBear4P))
        ObjectSetInteger(0, name2, OBJPROP_COLOR, (i_clrBull4P if bullish else i_clrBear4P))
        ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name0, OBJPROP_WIDTH, i_lineWidth)
        ObjectSetInteger(0, name1, OBJPROP_WIDTH, i_lineWidth)
        ObjectSetInteger(0, name2, OBJPROP_WIDTH, i_lineWidth)
        ObjectSetInteger(0, name0, OBJPROP_STYLE, i_style4P)
        ObjectSetInteger(0, name1, OBJPROP_STYLE, i_style4P)
        ObjectSetInteger(0, name2, OBJPROP_STYLE, i_style4P)
        ObjectSetString(0, name0, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' AB')
        ObjectSetString(0, name1, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BC')
        ObjectSetString(0, name2, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' CD')
        if i_showDescriptions:
            numOverlapping = 0
            for i in range(0, 88):
                stored = _indicator.GetMatchedPersistent(i)
                tail = stored.GetTail()
                head = stored.GetHead()
                capacity = stored.GetCapacity()
                j = tail
                while j != head:
                    if (not _indicator.Is4PointPattern(i)) and AIndex == stored.GetMatch(j).XIndex:
                        numOverlapping += 1
                    if _indicator.Is4PointPattern(i) and AIndex == stored.GetMatch(j).AIndex:
                        numOverlapping += 1
                    j = _imod(j + 1, capacity)
                stored = _indicator.GetMatchedTransient(i)
                tail = stored.GetTail()
                head = stored.GetHead()
                capacity = stored.GetCapacity()
                j = tail
                while j != head:
                    if (not _indicator.Is4PointPattern(i)) and AIndex == stored.GetMatch(j).XIndex:
                        numOverlapping += 1
                    if _indicator.Is4PointPattern(i) and AIndex == stored.GetMatch(j).AIndex:
                        numOverlapping += 1
                    j = _imod(j + 1, capacity)
            x1 = Box(0)
            y1 = Box(0)
            x2 = Box(0)
            y2 = Box(0)
            ChartTimePriceToXY(0, 0, ADateTime, A, x1, y1)
            ChartTimePriceToXY(0, 0, ADateTime, A + 1, x2, y2)
            pixelsPerPrice = MathAbs(y1.v - y2.v)
            change = (_fdiv(numOverlapping * i_fontSize, pixelsPerPrice) if (pixelsPerPrice != 0) else 0)
            price = ((A + change) if bullish else (A - change))
            ObjectCreate(0, pointA, OBJ_TEXT, 0, ADateTime, price)
            ObjectSetInteger(0, pointA, OBJPROP_SELECTABLE, True)
            ObjectSetString(0, pointA, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PA')
            ObjectSetString(0, pointA, OBJPROP_TEXT, 'A ' + prefix + _patternNames[k])
            ObjectSetString(0, pointA, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointA, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointA, OBJPROP_COLOR, (i_clrBull4P if bullish else i_clrBear4P))
            ObjectCreate(0, pointB, OBJ_TEXT, 0, BDateTime, B)
            ObjectCreate(0, pointC, OBJ_TEXT, 0, CDateTime, C)
            ObjectCreate(0, pointD, OBJ_TEXT, 0, DDateTime, D)
            ObjectSetInteger(0, pointB, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointC, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointD, OBJPROP_SELECTABLE, True)
            ObjectSetString(0, pointB, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PB')
            ObjectSetString(0, pointC, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PC')
            ObjectSetString(0, pointD, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PD')
            ObjectSetString(0, pointB, OBJPROP_TEXT, 'B')
            ObjectSetString(0, pointB, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointB, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointB, OBJPROP_COLOR, (i_clrBull4P if bullish else i_clrBear4P))
            ObjectSetString(0, pointC, OBJPROP_TEXT, 'C')
            ObjectSetString(0, pointC, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointC, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointC, OBJPROP_COLOR, (i_clrBull4P if bullish else i_clrBear4P))
            ObjectSetString(0, pointD, OBJPROP_TEXT, 'D')
            ObjectSetString(0, pointD, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointD, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointD, OBJPROP_COLOR, (i_clrBull4P if bullish else i_clrBear4P))
    def DisplayPattern_13(self, k, bullish, XIndex, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
        unique = UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime)
        prefix = ('Bullish ' if bullish else 'Bearish ')
        prefixName = ('U ' if bullish else 'D ') + _identifier + StringFormat('%x', _timeOfInit) + IntegerToString(k)
        name0 = prefixName + ' XA' + unique
        name1 = prefixName + ' AB' + unique
        name2 = prefixName + ' BC' + unique
        name3 = prefixName + ' CD' + unique
        name4 = prefixName + ' XAB' + unique
        name5 = prefixName + ' XAD' + unique
        name6 = prefixName + ' ABC' + unique
        name7 = prefixName + ' BCD' + unique
        triangle_XB = prefixName + ' XB' + unique
        triangle_BD = prefixName + ' BD' + unique
        pointX = prefixName + ' PX' + unique
        pointA = prefixName + ' PA' + unique
        pointB = prefixName + ' PB' + unique
        pointC = prefixName + ' PC' + unique
        pointD = prefixName + ' PD' + unique
        xcd = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(D - C), MathAbs(X - C)))))
        xab = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(A - B), MathAbs(X - A)))))
        xad = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(D - A), MathAbs(X - A)))))
        abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - B), MathAbs(B - A)))))
        if (k == CYPHER or k == NENSTAR) or k == NEWCYPHER:
            abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(X - C), MathAbs(X - A)))))
        bcd = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - D), MathAbs(B - C)))))
        ObjectCreate(0, name0, OBJ_TREND, 0, XDateTime, X, ADateTime, A)
        ObjectCreate(0, name1, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
        ObjectCreate(0, name2, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
        ObjectCreate(0, name3, (OBJ_ARROWED_LINE if (((not i_fillPatterns) or k == THREEDRIVES) or k == FIVEO) else OBJ_TREND), 0, CDateTime, C, DDateTime, D)
        ObjectCreate(0, name4, OBJ_TREND, 0, XDateTime, X, BDateTime, B)
        if i_showDescriptions:
            numOverlapping = 0
            for i in range(0, 88):
                stored = _indicator.GetMatchedPersistent(i)
                tail = stored.GetTail()
                head = stored.GetHead()
                capacity = stored.GetCapacity()
                j = tail
                while j != head:
                    if (not _indicator.Is4PointPattern(i)) and XIndex == stored.GetMatch(j).XIndex:
                        numOverlapping += 1
                    if _indicator.Is4PointPattern(i) and XIndex == stored.GetMatch(j).AIndex:
                        numOverlapping += 1
                    j = _imod(j + 1, capacity)
                stored = _indicator.GetMatchedTransient(i)
                tail = stored.GetTail()
                head = stored.GetHead()
                capacity = stored.GetCapacity()
                j = tail
                while j != head:
                    if (not _indicator.Is4PointPattern(i)) and XIndex == stored.GetMatch(j).XIndex:
                        numOverlapping += 1
                    if _indicator.Is4PointPattern(i) and XIndex == stored.GetMatch(j).AIndex:
                        numOverlapping += 1
                    j = _imod(j + 1, capacity)
            x1 = Box(0)
            y1 = Box(0)
            x2 = Box(0)
            y2 = Box(0)
            ChartTimePriceToXY(0, 0, XDateTime, X, x1, y1)
            ChartTimePriceToXY(0, 0, XDateTime, X + 1, x2, y2)
            pixelsPerPrice = MathAbs(y1.v - y2.v)
            change = (_fdiv(numOverlapping * i_fontSize, pixelsPerPrice) if (pixelsPerPrice != 0) else 0)
            price = ((X - change) if bullish else (X + change))
            ObjectCreate(0, pointX, OBJ_TEXT, 0, XDateTime, price)
            ObjectCreate(0, pointA, OBJ_TEXT, 0, ADateTime, A)
            ObjectCreate(0, pointB, OBJ_TEXT, 0, BDateTime, B)
            ObjectCreate(0, pointC, OBJ_TEXT, 0, CDateTime, C)
            ObjectCreate(0, pointD, OBJ_TEXT, 0, DDateTime, D)
            ObjectSetInteger(0, pointX, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointA, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointB, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointC, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointD, OBJPROP_SELECTABLE, True)
            ObjectSetString(0, pointX, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PX')
            ObjectSetString(0, pointA, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PA')
            ObjectSetString(0, pointB, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PB')
            ObjectSetString(0, pointC, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PC')
            ObjectSetString(0, pointD, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PD')
            ObjectSetString(0, pointX, OBJPROP_TEXT, 'X ' + prefix + _patternNames[k])
            ObjectSetString(0, pointX, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointX, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointX, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
            ObjectSetString(0, pointA, OBJPROP_TEXT, 'A')
            ObjectSetString(0, pointA, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointA, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointA, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
            ObjectSetString(0, pointB, OBJPROP_TEXT, 'B')
            ObjectSetString(0, pointB, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointB, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointB, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
            ObjectSetString(0, pointC, OBJPROP_TEXT, 'C')
            ObjectSetString(0, pointC, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointC, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointC, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
            ObjectSetString(0, pointD, OBJPROP_TEXT, 'D')
            ObjectSetString(0, pointD, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointD, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointD, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
        if k != FIVEO:
            ObjectCreate(0, name5, OBJ_TREND, 0, XDateTime, X, DDateTime, D)
        ObjectCreate(0, name6, OBJ_TREND, 0, ADateTime, A, CDateTime, C)
        ObjectCreate(0, name7, OBJ_TREND, 0, BDateTime, B, DDateTime, D)
        ObjectSetInteger(0, name0, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
        ObjectSetInteger(0, name1, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
        ObjectSetInteger(0, name2, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
        ObjectSetInteger(0, name3, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
        ObjectSetInteger(0, name0, OBJPROP_STYLE, i_style5P)
        ObjectSetInteger(0, name1, OBJPROP_STYLE, i_style5P)
        ObjectSetInteger(0, name3, OBJPROP_STYLE, i_style5P)
        ObjectSetInteger(0, name4, OBJPROP_COLOR, _clrRatio)
        if k != FIVEO:
            ObjectSetInteger(0, name5, OBJPROP_COLOR, _clrRatio)
        ObjectSetInteger(0, name6, OBJPROP_COLOR, _clrRatio)
        ObjectSetInteger(0, name7, OBJPROP_COLOR, _clrRatio)
        ObjectSetInteger(0, name4, OBJPROP_STYLE, i_styleRatio)
        if k != FIVEO:
            ObjectSetInteger(0, name5, OBJPROP_STYLE, i_styleRatio)
        ObjectSetInteger(0, name6, OBJPROP_STYLE, i_styleRatio)
        ObjectSetInteger(0, name7, OBJPROP_STYLE, i_styleRatio)
        ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name3, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name4, OBJPROP_SELECTABLE, True)
        if k != FIVEO:
            ObjectSetInteger(0, name5, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name6, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name7, OBJPROP_SELECTABLE, True)
        ObjectSetString(0, name0, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XA')
        ObjectSetString(0, name1, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' AB')
        ObjectSetString(0, name2, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BC')
        ObjectSetString(0, name3, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' CD')
        ObjectSetString(0, name4, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XAB=' + xab)
        pattern = _copy(_patterns[k])
        ad2xaConstraint = pattern.ad2xa_max != 0 and pattern.ad2xa_min != 0
        cd2xcConstraint = pattern.cd2xc_max != 0 and pattern.cd2xc_min != 0
        xcdMostRelevant = cd2xcConstraint and (not ad2xaConstraint)
        if k != FIVEO and xcdMostRelevant:
            ObjectSetString(0, name5, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XCD=' + xcd)
        elif k != FIVEO:
            ObjectSetString(0, name5, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XAD=' + xad)
        ObjectSetString(0, name6, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' ABC=' + abc)
        ObjectSetString(0, name7, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BCD=' + bcd)
        ObjectSetInteger(0, name0, OBJPROP_WIDTH, i_lineWidth)
        ObjectSetInteger(0, name1, OBJPROP_WIDTH, i_lineWidth)
        ObjectSetInteger(0, name2, OBJPROP_WIDTH, i_lineWidth)
        ObjectSetInteger(0, name3, OBJPROP_WIDTH, i_lineWidth)
        if i_fillPatterns and (k != FIVEO and k != THREEDRIVES):
            ObjectCreate(0, triangle_XB, OBJ_TRIANGLE, 0, XDateTime, X, ADateTime, A, BDateTime, B)
            ObjectCreate(0, triangle_BD, OBJ_TRIANGLE, 0, BDateTime, B, CDateTime, C, DDateTime, D)
            ObjectSetInteger(0, triangle_XB, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
            ObjectSetInteger(0, triangle_XB, OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(0, triangle_XB, OBJPROP_FILL, True)
            ObjectSetInteger(0, triangle_XB, OBJPROP_BACK, True)
            ObjectSetInteger(0, triangle_XB, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, triangle_XB, OBJPROP_SELECTED, False)
            ObjectSetInteger(0, triangle_BD, OBJPROP_COLOR, (i_clrBull if bullish else i_clrBear))
            ObjectSetInteger(0, triangle_BD, OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(0, triangle_BD, OBJPROP_FILL, True)
            ObjectSetInteger(0, triangle_BD, OBJPROP_BACK, True)
            ObjectSetInteger(0, triangle_BD, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, triangle_BD, OBJPROP_SELECTED, False)
    def DisplayProjection_10(self, k, bullish, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
        unique = UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime)
        prefix = ('Proj. Bullish ' if bullish else 'Proj. Bearish ')
        prefixName = (('PU ' + _identifier) if bullish else ('PD ' + _identifier))
        name0 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' AB' + unique
        name1 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BC' + unique
        name2 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' CD' + unique
        pointA = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PA' + unique
        pointB = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PB' + unique
        pointC = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PC' + unique
        pointD = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PD' + unique
        prz = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PRS' + unique
        clr = (i_clrBullProjection4P if bullish else i_clrBearProjection4P)
        clrleg = (_faintBGColor if i_showSoftProjections else clr)
        ObjectCreate(0, name0, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
        ObjectCreate(0, name1, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
        ObjectCreate(0, name2, OBJ_TREND, 0, CDateTime, C, DDateTime, D)
        ObjectSetInteger(0, name0, OBJPROP_COLOR, clrleg)
        ObjectSetInteger(0, name1, OBJPROP_COLOR, clrleg)
        ObjectSetInteger(0, name2, OBJPROP_COLOR, clrleg)
        ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)
        ObjectSetString(0, name0, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' AB')
        ObjectSetString(0, name1, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BC')
        ObjectSetString(0, name2, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' CD')
        ObjectSetInteger(0, name0, OBJPROP_WIDTH, i_lineWidthProj)
        ObjectSetInteger(0, name1, OBJPROP_WIDTH, i_lineWidthProj)
        ObjectSetInteger(0, name2, OBJPROP_WIDTH, i_lineWidthProj)
        ObjectSetInteger(0, name0, OBJPROP_STYLE, i_styleProj)
        ObjectSetInteger(0, name1, OBJPROP_STYLE, i_styleProj)
        ObjectSetInteger(0, name2, OBJPROP_STYLE, i_styleProj)
        if i_showSoftProjections:
            ObjectSetInteger(0, name0, OBJPROP_BACK, True)
            ObjectSetInteger(0, name1, OBJPROP_BACK, True)
            ObjectSetInteger(0, name2, OBJPROP_BACK, True)
        if i_showDescriptions and (not i_showSoftProjections):
            ObjectCreate(0, pointA, OBJ_TEXT, 0, ADateTime, A)
            ObjectCreate(0, pointB, OBJ_TEXT, 0, BDateTime, B)
            ObjectCreate(0, pointC, OBJ_TEXT, 0, CDateTime, C)
            ObjectCreate(0, pointD, OBJ_TEXT, 0, DDateTime, D)
            ObjectSetInteger(0, pointA, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointB, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointC, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointD, OBJPROP_SELECTABLE, True)
            ObjectSetString(0, pointA, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PA')
            ObjectSetString(0, pointB, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PB')
            ObjectSetString(0, pointC, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PC')
            ObjectSetString(0, pointD, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PD')
            ObjectSetString(0, pointA, OBJPROP_TEXT, 'A')
            ObjectSetString(0, pointA, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointA, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointA, OBJPROP_COLOR, clrleg)
            ObjectSetString(0, pointB, OBJPROP_TEXT, 'B')
            ObjectSetString(0, pointB, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointB, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointB, OBJPROP_COLOR, clrleg)
            ObjectSetString(0, pointC, OBJPROP_TEXT, 'C')
            ObjectSetString(0, pointC, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointC, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointC, OBJPROP_COLOR, clrleg)
            ObjectSetString(0, pointD, OBJPROP_TEXT, ('' if i_showSoftProjections else ' D ') + prefix + _patternNames[k])
            ObjectSetString(0, pointD, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointD, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointD, OBJPROP_COLOR, clr)
        ObjectCreate(0, prz, OBJ_TREND, 0, DDateTime - 1, D, DDateTime + _deltaDT, D)
        ObjectSetInteger(0, prz, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, prz, OBJPROP_RAY_RIGHT, False)
        ObjectSetInteger(0, prz, OBJPROP_STYLE, i_stylePRZ)
        ObjectSetInteger(0, prz, OBJPROP_COLOR, clr)
        ObjectSetString(0, prz, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PRZ start ' + DoubleToString(D))
    def DisplayProjection_12(self, k, bullish, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
        unique = UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime)
        prefix = ('Proj. Bullish ' if bullish else 'Proj. Bearish ')
        prefixName = ('PU ' if bullish else 'PD ') + _identifier + StringFormat('%x', _timeOfInit) + IntegerToString(k)
        name0 = prefixName + ' XA' + unique
        name1 = prefixName + ' AB' + unique
        name2 = prefixName + ' BC' + unique
        name3 = prefixName + ' CD' + unique
        name4 = prefixName + ' XAB' + unique
        name5 = prefixName + ' XAD' + unique
        name6 = prefixName + ' ABC' + unique
        name7 = prefixName + ' BCD' + unique
        pointX = prefixName + ' PX' + unique
        pointA = prefixName + ' PA' + unique
        pointB = prefixName + ' PB' + unique
        pointC = prefixName + ' PC' + unique
        pointD = prefixName + ' PD' + unique
        prz = prefixName + ' PRS' + unique
        xcd = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(D - C), MathAbs(X - C)))))
        xab = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(A - B), MathAbs(X - A)))))
        xad = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(D - A), MathAbs(X - A)))))
        abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - B), MathAbs(B - A)))))
        if (k == CYPHER or k == NENSTAR) or k == NEWCYPHER:
            abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(X - C), MathAbs(X - A)))))
        bcd = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - D), MathAbs(B - C)))))
        clr = (i_clrBullProjection if bullish else i_clrBearProjection)
        clrleg = (_faintBGColor if i_showSoftProjections else clr)
        clrratio = (_faintBGColor if i_showSoftProjections else _clrRatio)
        ObjectCreate(0, name0, OBJ_TREND, 0, XDateTime, X, ADateTime, A)
        ObjectCreate(0, name1, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
        ObjectCreate(0, name2, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
        ObjectCreate(0, name3, OBJ_TREND, 0, CDateTime, C, DDateTime, D)
        ObjectCreate(0, name4, OBJ_TREND, 0, XDateTime, X, BDateTime, B)
        if k != FIVEO:
            ObjectCreate(0, name5, OBJ_TREND, 0, XDateTime, X, DDateTime, D)
        ObjectCreate(0, name6, OBJ_TREND, 0, ADateTime, A, CDateTime, C)
        ObjectCreate(0, name7, OBJ_TREND, 0, BDateTime, B, DDateTime, D)
        ObjectSetInteger(0, name0, OBJPROP_COLOR, clrleg)
        ObjectSetInteger(0, name1, OBJPROP_COLOR, clrleg)
        ObjectSetInteger(0, name2, OBJPROP_COLOR, clrleg)
        ObjectSetInteger(0, name3, OBJPROP_COLOR, clrleg)
        ObjectSetInteger(0, name4, OBJPROP_COLOR, clrratio)
        if k != FIVEO:
            ObjectSetInteger(0, name5, OBJPROP_COLOR, clrratio)
        ObjectSetInteger(0, name6, OBJPROP_COLOR, clrratio)
        ObjectSetInteger(0, name7, OBJPROP_COLOR, clrratio)
        ObjectSetInteger(0, name0, OBJPROP_STYLE, i_styleProj)
        ObjectSetInteger(0, name1, OBJPROP_STYLE, i_styleProj)
        ObjectSetInteger(0, name2, OBJPROP_STYLE, i_styleProj)
        ObjectSetInteger(0, name3, OBJPROP_STYLE, i_styleProj)
        ObjectSetInteger(0, name4, OBJPROP_STYLE, i_styleRatio)
        ObjectSetInteger(0, name5, OBJPROP_STYLE, i_styleRatio)
        ObjectSetInteger(0, name6, OBJPROP_STYLE, i_styleRatio)
        ObjectSetInteger(0, name7, OBJPROP_STYLE, i_styleRatio)
        ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name3, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name4, OBJPROP_SELECTABLE, True)
        if k != FIVEO:
            ObjectSetInteger(0, name5, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name6, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, name7, OBJPROP_SELECTABLE, True)
        ObjectSetString(0, name0, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XA')
        ObjectSetString(0, name1, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' AB')
        ObjectSetString(0, name2, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BC')
        ObjectSetString(0, name3, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' CD')
        ObjectSetString(0, name4, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XAB=' + xab)
        pattern = _copy(_patterns[k])
        ad2xaConstraint = pattern.ad2xa_max != 0 and pattern.ad2xa_min != 0
        cd2xcConstraint = pattern.cd2xc_max != 0 and pattern.cd2xc_min != 0
        xcdMostRelevant = cd2xcConstraint and (not ad2xaConstraint)
        if k != FIVEO and xcdMostRelevant:
            ObjectSetString(0, name5, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XCD=' + xcd)
        elif k != FIVEO:
            ObjectSetString(0, name5, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XAD=' + xad)
        ObjectSetString(0, name6, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' ABC=' + abc)
        ObjectSetString(0, name7, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BCD=' + bcd)
        if i_showSoftProjections:
            ObjectSetInteger(0, name0, OBJPROP_BACK, True)
            ObjectSetInteger(0, name1, OBJPROP_BACK, True)
            ObjectSetInteger(0, name2, OBJPROP_BACK, True)
            ObjectSetInteger(0, name3, OBJPROP_BACK, True)
            ObjectSetInteger(0, name4, OBJPROP_BACK, True)
            ObjectSetInteger(0, name5, OBJPROP_BACK, True)
            ObjectSetInteger(0, name6, OBJPROP_BACK, True)
            ObjectSetInteger(0, name7, OBJPROP_BACK, True)
        if i_showDescriptions and (not i_showSoftProjections):
            ObjectCreate(0, pointX, OBJ_TEXT, 0, XDateTime, X)
            ObjectCreate(0, pointA, OBJ_TEXT, 0, ADateTime, A)
            ObjectCreate(0, pointB, OBJ_TEXT, 0, BDateTime, B)
            ObjectCreate(0, pointC, OBJ_TEXT, 0, CDateTime, C)
            ObjectCreate(0, pointD, OBJ_TEXT, 0, DDateTime, D)
            ObjectSetInteger(0, pointX, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointA, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointB, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointC, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, pointD, OBJPROP_SELECTABLE, True)
            ObjectSetString(0, pointX, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PX')
            ObjectSetString(0, pointA, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PA')
            ObjectSetString(0, pointB, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PB')
            ObjectSetString(0, pointC, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PC')
            ObjectSetString(0, pointD, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PD')
            ObjectSetInteger(0, name0, OBJPROP_WIDTH, i_lineWidthProj)
            ObjectSetInteger(0, name1, OBJPROP_WIDTH, i_lineWidthProj)
            ObjectSetInteger(0, name2, OBJPROP_WIDTH, i_lineWidthProj)
            ObjectSetInteger(0, name3, OBJPROP_WIDTH, i_lineWidthProj)
            ObjectSetString(0, pointX, OBJPROP_TEXT, 'X')
            ObjectSetString(0, pointX, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointX, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointX, OBJPROP_COLOR, clrleg)
            ObjectSetString(0, pointA, OBJPROP_TEXT, 'A')
            ObjectSetString(0, pointA, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointA, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointA, OBJPROP_COLOR, clrleg)
            ObjectSetString(0, pointB, OBJPROP_TEXT, 'B')
            ObjectSetString(0, pointB, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointB, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointB, OBJPROP_COLOR, clrleg)
            ObjectSetString(0, pointC, OBJPROP_TEXT, 'C')
            ObjectSetString(0, pointC, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointC, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointC, OBJPROP_COLOR, clrleg)
            ObjectSetString(0, pointD, OBJPROP_TEXT, ('' if i_showSoftProjections else ' D ') + prefix + _patternNames[k])
            ObjectSetString(0, pointD, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, pointD, OBJPROP_FONTSIZE, i_fontSize)
            ObjectSetInteger(0, pointD, OBJPROP_COLOR, clr)
        ObjectCreate(0, prz, OBJ_TREND, 0, DDateTime - 1, D, DDateTime + _deltaDT, D)
        ObjectSetInteger(0, prz, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, prz, OBJPROP_RAY_RIGHT, False)
        ObjectSetInteger(0, prz, OBJPROP_STYLE, i_stylePRZ)
        ObjectSetInteger(0, prz, OBJPROP_COLOR, (i_clrBullProjection if bullish else i_clrBearProjection))
        ObjectSetString(0, prz, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PRZ start ' + DoubleToString(D))

class CHPFFilterList(CHPFFilter):
    _q_fields = ('m_filters',)
    _q_ptrs = ('m_filters',)
    def __init__(self, size):
        CHPFFilter.__init__(self)
        self.m_filters = Arr(0, None)
        if ArrayResize(self.m_filters, size) < size:
            printf('Error allocating array at ' + 'CHPFFilterList::CHPFFilterList' + ' code: ' + IntegerToString(GetLastError()))
    def _q_dtor(self):
        ArrayFree(self.m_filters)
    def Set(self, index, filter_):
        self.m_filters[index] = filter_
    def IsValidUndershot(self, patternIndex, match):
        i = 0
        while i < ArraySize(self.m_filters):
            if not self.m_filters[i].IsValidUndershot(patternIndex, match):
                return False
            i += 1
        return True
    def IsValidMatched(self, patternIndex, match):
        i = 0
        while i < ArraySize(self.m_filters):
            if not self.m_filters[i].IsValidMatched(patternIndex, match):
                return False
            i += 1
        return True
    def IsValidOvershot(self, patternIndex, match):
        i = 0
        while i < ArraySize(self.m_filters):
            if not self.m_filters[i].IsValidOvershot(patternIndex, match):
                return False
            i += 1
        return True

class CHPFPurityFilter(CHPFFilter):
    _q_fields = ('m_activated',)
    def __init__(self):
        CHPFFilter.__init__(self)
        self.m_activated = False
    def _q_dtor(self):
        pass
    def SetActivated(self, activated):
        self.m_activated = activated
    def IsValidUndershot(self, patternIndex, match):
        if self.m_activated:
            pattern = _copy(_patterns[patternIndex])
            return IsPuristPRZ(pattern, match.bullish, match.X, match.A, match.B, match.C, match.nearD, match.farD)
        return True
    def IsValidMatched(self, patternIndex, match):
        if self.m_activated:
            pattern = _copy(_patterns[patternIndex])
            return IsPuristPRZ(pattern, match.bullish, match.X, match.A, match.B, match.C, match.nearD, match.farD)
        return True
    def IsValidOvershot(self, patternIndex, match):
        if self.m_activated:
            pattern = _copy(_patterns[patternIndex])
            return IsPuristPRZ(pattern, match.bullish, match.X, match.A, match.B, match.C, match.nearD, match.farD)
        return True

class CHPFTimeFilter(CHPFFilter):
    _q_fields = ('m_tooEarly', 'm_tooLate', 'm_filterTooEarly', 'm_filterTooLate', 'm_num4PointPatterns', 'm_low', 'm_high', 'm_bar')
    def __init__(self, num4PointPatterns, tooEarly, tooLate):
        CHPFFilter.__init__(self)
        self.m_tooEarly = 0.0
        self.m_tooLate = 0.0
        self.m_filterTooEarly = False
        self.m_filterTooLate = False
        self.m_num4PointPatterns = 0
        self.m_low = Arr(0, 0.0)
        self.m_high = Arr(0, 0.0)
        self.m_bar = 0
        self.m_tooEarly = tooEarly
        self.m_tooLate = tooLate
        self.m_num4PointPatterns = num4PointPatterns
    def _q_dtor(self):
        pass
    def SetActivated(self, tooEarly, tooLate):
        self.m_filterTooEarly = tooEarly
        self.m_filterTooLate = tooLate
    def Is4PointPattern(self, index):
        return index < self.m_num4PointPatterns
    def SetBar(self, bar):
        self.m_bar = bar
    def IsValidUndershot(self, patternIndex, match):
        if self.m_filterTooLate:
            XIndex = match.XIndex
            AIndex = match.AIndex
            BIndex = match.BIndex
            CIndex = match.CIndex
            DIndex = self.m_bar
            timeliness = self.PatternTimeliness(XIndex, AIndex, BIndex, CIndex, DIndex, self.Is4PointPattern(patternIndex))
            return timeliness != TOO_LATE
        return True
    def IsValidMatched(self, patternIndex, match):
        if self.m_filterTooEarly or self.m_filterTooLate:
            XIndex = match.XIndex
            AIndex = match.AIndex
            BIndex = match.BIndex
            CIndex = match.CIndex
            DIndex = match.DIndex
            timeliness = self.PatternTimeliness(XIndex, AIndex, BIndex, CIndex, DIndex, self.Is4PointPattern(patternIndex))
            if self.m_filterTooEarly and timeliness == TOO_EARLY:
                return False
            if self.m_filterTooLate and timeliness == TOO_LATE:
                return False
        return True
    def IsValidOvershot(self, patternIndex, match):
        if self.m_filterTooEarly or self.m_filterTooLate:
            XIndex = match.XIndex
            AIndex = match.AIndex
            BIndex = match.BIndex
            CIndex = match.CIndex
            DIndex = self.PRZViolatingBar(match.bullish, CIndex, match.DIndex, match.farD)
            timeliness = self.PatternTimeliness(XIndex, AIndex, BIndex, CIndex, DIndex, self.Is4PointPattern(patternIndex))
            if self.m_filterTooEarly and timeliness == TOO_EARLY:
                return False
            if self.m_filterTooLate and timeliness == TOO_LATE:
                return False
        return True
    def PatternTimeliness(self, XIndex, AIndex, BIndex, CIndex, DIndex, is4P):
        baseBars = 0
        fixBar = 0
        if is4P:
            baseBars = BIndex - AIndex
            fixBar = CIndex
        else:
            baseBars = BIndex - XIndex
            fixBar = BIndex
        if DIndex < (fixBar + MathFloor(self.m_tooEarly * baseBars)):
            return TOO_EARLY
        elif DIndex < (fixBar + MathCeil(self.m_tooLate * baseBars)):
            return TIMELY
        else:
            return TOO_LATE
    def PRZViolatingBar(self, bullish, CIndex, DIndex, przEnd):
        for bar in range(CIndex, DIndex + 1):
            if bullish and self.m_low[bar] < przEnd:
                return bar
            if (not bullish) and self.m_high[bar] > przEnd:
                return bar
        return -1
    def SetPrices(self, lowArr, highArr):
        ArrayCopy(self.m_low, lowArr, 0, 0)
        ArrayCopy(self.m_high, highArr, 0, 0)

def ZigZagDirection(index, peaks, troughs):
    lastPeakBefore = FirstNonZeroFrom(index - 1, peaks)
    lastTroughBefore = FirstNonZeroFrom(index - 1, troughs)
    while lastPeakBefore == lastTroughBefore:
        lastPeakBefore = FirstNonZeroFrom(lastPeakBefore - 1, peaks)
        lastTroughBefore = FirstNonZeroFrom(lastTroughBefore - 1, troughs)
        if lastPeakBefore == -1 or lastTroughBefore == -1:
            return 0
    if lastPeakBefore == -1 or lastTroughBefore == -1:
        return 0
    elif lastPeakBefore < lastTroughBefore:
        return -1
    else:
        return 1

def FirstNonZeroFrom(start, array):
    for j in range(start, 0 - 1, -1):
        if array[j] != 0 and array[j] != EMPTY_VALUE:
            return j
    return -1

def HarmonicWindow(pattern, slackUnary, slackRange, startsInTrough, X, A, B, C, nearD, farD):
    ad2xaConstraint = pattern.ad2xa_max != 0 and pattern.ad2xa_min != 0
    cd2bcConstraint = pattern.cd2bc_max != 0 and pattern.cd2bc_min != 0
    cd2xcConstraint = pattern.cd2xc_max != 0 and pattern.cd2xc_min != 0
    cd2abConstraint = pattern.cd2ab_max != 0 and pattern.cd2ab_min != 0
    cd2adConstraint = pattern.cd2ad_max != 0 and pattern.cd2ad_min != 0
    ad2xaSlack = (slackUnary if (pattern.ad2xa_max == pattern.ad2xa_min) else slackRange)
    cd2bcSlack = (slackUnary if (pattern.cd2bc_max == pattern.cd2bc_min) else slackRange)
    cd2xcSlack = (slackUnary if (pattern.cd2xc_max == pattern.cd2xc_min) else slackRange)
    cd2abSlack = (slackUnary if (pattern.cd2ab_max == pattern.cd2ab_min) else slackRange)
    cd2adSlack = (slackUnary if (pattern.cd2ad_max == pattern.cd2ad_min) else slackRange)
    XA = MathAbs(A - X)
    XC = MathAbs(X - C)
    AB = MathAbs(A - B)
    BC = MathAbs(C - B)
    nearD_cd2bc = 0.0
    nearD_ad2xa = 0.0
    nearD_cd2xc = 0.0
    nearD_cd2ab = 0.0
    farD_cd2bc = 0.0
    farD_ad2xa = 0.0
    farD_cd2xc = 0.0
    farD_cd2ab = 0.0
    if startsInTrough:
        nearD_cd2bc = C - ((pattern.cd2bc_min - cd2bcSlack) * BC)
        nearD_ad2xa = A - ((pattern.ad2xa_min - ad2xaSlack) * XA)
        nearD_cd2xc = C - ((pattern.cd2xc_min - cd2xcSlack) * XC)
        nearD_cd2ab = C - ((pattern.cd2ab_min - cd2abSlack) * AB)
        farD_cd2bc = C - ((pattern.cd2bc_max + cd2bcSlack) * BC)
        farD_ad2xa = A - ((pattern.ad2xa_max + ad2xaSlack) * XA)
        farD_cd2xc = C - ((pattern.cd2xc_max + cd2xcSlack) * XC)
        farD_cd2ab = C - ((pattern.cd2ab_max + cd2abSlack) * AB)
    else:
        nearD_cd2bc = C + ((pattern.cd2bc_min - cd2bcSlack) * BC)
        nearD_ad2xa = A + ((pattern.ad2xa_min - ad2xaSlack) * XA)
        nearD_cd2xc = C + ((pattern.cd2xc_min - cd2xcSlack) * XC)
        nearD_cd2ab = C + ((pattern.cd2ab_min - cd2abSlack) * AB)
        farD_cd2bc = C + ((pattern.cd2bc_max + cd2bcSlack) * BC)
        farD_ad2xa = A + ((pattern.ad2xa_max + ad2xaSlack) * XA)
        farD_cd2xc = C + ((pattern.cd2xc_max + cd2xcSlack) * XC)
        farD_cd2ab = C + ((pattern.cd2ab_max + cd2abSlack) * AB)
    nearD.v = (DBL_MAX if startsInTrough else DBL_MIN)
    farD.v = (DBL_MIN if startsInTrough else DBL_MAX)
    if cd2bcConstraint:
        nearD.v = (MathMin(nearD.v, nearD_cd2bc) if startsInTrough else MathMax(nearD.v, nearD_cd2bc))
        farD.v = (MathMax(farD.v, farD_cd2bc) if startsInTrough else MathMin(farD.v, farD_cd2bc))
    if ad2xaConstraint:
        nearD.v = (MathMin(nearD.v, nearD_ad2xa) if startsInTrough else MathMax(nearD.v, nearD_ad2xa))
        farD.v = (MathMax(farD.v, farD_ad2xa) if startsInTrough else MathMin(farD.v, farD_ad2xa))
    if cd2xcConstraint:
        nearD.v = (MathMin(nearD.v, nearD_cd2xc) if startsInTrough else MathMax(nearD.v, nearD_cd2xc))
        farD.v = (MathMax(farD.v, farD_cd2xc) if startsInTrough else MathMin(farD.v, farD_cd2xc))
    if cd2abConstraint:
        nearD.v = (MathMin(nearD.v, nearD_cd2ab) if startsInTrough else MathMax(nearD.v, nearD_cd2ab))
        farD.v = (MathMax(farD.v, farD_cd2ab) if startsInTrough else MathMin(farD.v, farD_cd2ab))
    if (cd2adConstraint and (pattern.cd2ad_min - cd2adSlack) != 1.0) and (pattern.cd2ad_max + cd2adSlack) != 1:
        cd2ad_1 = MathAbs(_fdiv(C - ((pattern.cd2ad_min - cd2adSlack) * A), pattern.cd2ad_min - cd2adSlack - 1.0))
        cd2ad_2 = MathAbs(_fdiv(C - ((pattern.cd2ad_max + cd2adSlack) * A), pattern.cd2ad_max + cd2adSlack - 1.0))
        nearD.v = (MathMin(nearD.v, MathMax(cd2ad_1, cd2ad_2)) if startsInTrough else MathMax(nearD.v, MathMin(cd2ad_1, cd2ad_2)))
        farD.v = (MathMax(farD.v, MathMin(cd2ad_1, cd2ad_2)) if startsInTrough else MathMin(farD.v, MathMax(cd2ad_1, cd2ad_2)))

def HarmonicRatios(pattern, startsInTrough, X, A, B, C):
    ad2xaConstraint = pattern.ad2xa_max != 0 and pattern.ad2xa_min != 0
    cd2bcConstraint = pattern.cd2bc_max != 0 and pattern.cd2bc_min != 0
    cd2xcConstraint = pattern.cd2xc_max != 0 and pattern.cd2xc_min != 0
    cd2abConstraint = pattern.cd2ab_max != 0 and pattern.cd2ab_min != 0
    cd2adConstraint = pattern.cd2ad_max != 0 and pattern.cd2ad_min != 0
    ad2xaUnary = pattern.ad2xa_max == pattern.ad2xa_min
    cd2bcUnary = pattern.cd2bc_max == pattern.cd2bc_min
    cd2xcUnary = pattern.cd2xc_max == pattern.cd2xc_min
    cd2abUnary = pattern.cd2ab_max == pattern.cd2ab_min
    cd2adUnary = pattern.cd2ad_max == pattern.cd2ad_min
    XA = MathAbs(A - X)
    XC = MathAbs(X - C)
    AB = MathAbs(A - B)
    BC = MathAbs(C - B)
    cd2bc = 0.0
    ad2xa = 0.0
    cd2xc = 0.0
    cd2ab = 0.0
    cd2ad = 0.0
    if startsInTrough:
        if cd2bcConstraint and cd2bcUnary:
            cd2bc = C - (pattern.cd2bc_min * BC)
        if ad2xaConstraint and ad2xaUnary:
            ad2xa = A - (pattern.ad2xa_min * XA)
        if cd2xcConstraint and cd2xcUnary:
            cd2xc = C - (pattern.cd2xc_min * XC)
        if cd2abConstraint and cd2abUnary:
            cd2ab = C - (pattern.cd2ab_min * AB)
        if (cd2adConstraint and cd2adUnary) and pattern.cd2ad_min != 1.0:
            cd2ad = MathAbs(_fdiv(C - (pattern.cd2ad_min * A), pattern.cd2ad_min - 1.0))
    else:
        if cd2bcConstraint and cd2bcUnary:
            cd2bc = C + (pattern.cd2bc_min * BC)
        if ad2xaConstraint and ad2xaUnary:
            ad2xa = A + (pattern.ad2xa_min * XA)
        if cd2xcConstraint and cd2xcUnary:
            cd2xc = C + (pattern.cd2xc_min * XC)
        if cd2abConstraint and cd2abUnary:
            cd2ab = C + (pattern.cd2ab_min * AB)
        if (cd2adConstraint and cd2adUnary) and pattern.cd2ad_min != 1.0:
            cd2ad = MathAbs(_fdiv(C - (pattern.cd2ad_min * A), pattern.cd2ad_min - 1.0))
    levels = PRZLevels()
    levels.cd2bc = cd2bc
    levels.ad2xa = ad2xa
    levels.cd2xc = cd2xc
    levels.cd2ab = cd2ab
    levels.cd2ad = cd2ad
    return _copy(levels)

def HarmonicRatios2(pattern, startsInTrough, X, A, B, C):
    ad2xaConstraint = pattern.ad2xa_max != 0 and pattern.ad2xa_min != 0
    cd2bcConstraint = pattern.cd2bc_max != 0 and pattern.cd2bc_min != 0
    cd2xcConstraint = pattern.cd2xc_max != 0 and pattern.cd2xc_min != 0
    cd2abConstraint = pattern.cd2ab_max != 0 and pattern.cd2ab_min != 0
    cd2adConstraint = pattern.cd2ad_max != 0 and pattern.cd2ad_min != 0
    ad2xaUnary = pattern.ad2xa_max == pattern.ad2xa_min
    cd2bcUnary = pattern.cd2bc_max == pattern.cd2bc_min
    cd2xcUnary = pattern.cd2xc_max == pattern.cd2xc_min
    cd2abUnary = pattern.cd2ab_max == pattern.cd2ab_min
    cd2adUnary = pattern.cd2ad_max == pattern.cd2ad_min
    XA = MathAbs(A - X)
    XC = MathAbs(X - C)
    AB = MathAbs(A - B)
    BC = MathAbs(C - B)
    cd2bc = 0.0
    ad2xa = 0.0
    cd2xc = 0.0
    cd2ab = 0.0
    cd2ad = 0.0
    if startsInTrough:
        if cd2bcConstraint and cd2bcUnary:
            cd2bc = C - (pattern.cd2bc_min * BC)
        if ad2xaConstraint and ad2xaUnary:
            ad2xa = A - (pattern.ad2xa_min * XA)
        if cd2xcConstraint and cd2xcUnary:
            cd2xc = C - (pattern.cd2xc_min * XC)
        if cd2abConstraint and cd2abUnary:
            cd2ab = C - (pattern.cd2ab_min * AB)
        if (cd2adConstraint and cd2adUnary) and pattern.cd2ad_min != 1.0:
            cd2ad = MathAbs(_fdiv(C - (pattern.cd2ad_min * A), pattern.cd2ad_min - 1.0))
    else:
        if cd2bcConstraint and cd2bcUnary:
            cd2bc = C + (pattern.cd2bc_min * BC)
        if ad2xaConstraint and ad2xaUnary:
            ad2xa = A + (pattern.ad2xa_min * XA)
        if cd2xcConstraint and cd2xcUnary:
            cd2xc = C + (pattern.cd2xc_min * XC)
        if cd2abConstraint and cd2abUnary:
            cd2ab = C + (pattern.cd2ab_min * AB)
        if (cd2adConstraint and cd2adUnary) and pattern.cd2ad_min != 1.0:
            cd2ad = MathAbs(_fdiv(C - (pattern.cd2ad_min * A), pattern.cd2ad_min - 1.0))
    levels = PRZLevels()
    levels.cd2ab = cd2ab
    levels.ad2xa = ad2xa
    levels.cd2xc = cd2xc
    levels.cd2bc = cd2ab
    levels.cd2ad = cd2ad
    return _copy(levels)

def IsPuristPRZ(pattern, startsInTrough, X, A, B, C, nearD, farD):
    ad2xaConstraint = pattern.ad2xa_max != 0 and pattern.ad2xa_min != 0
    cd2bcConstraint = pattern.cd2bc_max != 0 and pattern.cd2bc_min != 0
    cd2xcConstraint = pattern.cd2xc_max != 0 and pattern.cd2xc_min != 0
    cd2abConstraint = pattern.cd2ab_max != 0 and pattern.cd2ab_min != 0
    cd2adConstraint = pattern.cd2ad_max != 0 and pattern.cd2ad_min != 0
    XA = MathAbs(A - X)
    XC = MathAbs(X - C)
    AB = MathAbs(A - B)
    BC = MathAbs(C - B)
    if cd2bcConstraint:
        contained = False
        if startsInTrough:
            nearRatio = C - (pattern.cd2bc_min * BC)
            farRatio = C - (pattern.cd2bc_max * BC)
            contained = nearD >= farRatio and nearRatio >= farD
        else:
            nearRatio = C + (pattern.cd2bc_min * BC)
            farRatio = C + (pattern.cd2bc_max * BC)
            contained = nearD <= farRatio and nearRatio <= farD
        if not contained:
            return False
    if ad2xaConstraint:
        contained = False
        if startsInTrough:
            nearRatio = A - (pattern.ad2xa_min * XA)
            farRatio = A - (pattern.ad2xa_max * XA)
            contained = nearD >= farRatio and nearRatio >= farD
        else:
            nearRatio = A + (pattern.ad2xa_min * XA)
            farRatio = A + (pattern.ad2xa_max * XA)
            contained = nearD <= farRatio and nearRatio <= farD
        if not contained:
            return False
    if cd2xcConstraint:
        contained = False
        if startsInTrough:
            nearRatio = C - (pattern.cd2xc_min * XC)
            farRatio = C - (pattern.cd2xc_max * XC)
            contained = nearD >= farRatio and nearRatio >= farD
        else:
            nearRatio = C + (pattern.cd2xc_min * XC)
            farRatio = C + (pattern.cd2xc_max * XC)
            contained = nearD <= farRatio and nearRatio <= farD
        if not contained:
            return False
    if cd2abConstraint:
        contained = False
        if startsInTrough:
            nearRatio = C - (pattern.cd2ab_min * AB)
            farRatio = C - (pattern.cd2ab_max * AB)
            contained = nearD >= farRatio and nearRatio >= farD
        else:
            nearRatio = C + (pattern.cd2ab_min * AB)
            farRatio = C + (pattern.cd2ab_max * AB)
            contained = nearD <= farRatio and nearRatio <= farD
        if not contained:
            return False
    if (cd2adConstraint and pattern.cd2ad_min != 1.0) and pattern.cd2ad_max != 1:
        contained = False
        cd2ad_1 = MathAbs(_fdiv(C - (pattern.cd2ad_min * A), pattern.cd2ad_min - 1.0))
        cd2ad_2 = MathAbs(_fdiv(C - (pattern.cd2ad_max * A), pattern.cd2ad_max - 1.0))
        if startsInTrough:
            nearRatio = MathMax(cd2ad_1, cd2ad_2)
            farRatio = MathMin(cd2ad_1, cd2ad_2)
            contained = nearD >= farRatio and nearRatio >= farD
        else:
            nearRatio = MathMin(cd2ad_1, cd2ad_2)
            farRatio = MathMax(cd2ad_1, cd2ad_2)
            contained = nearD <= farRatio and nearRatio <= farD
        if not contained:
            return False
    return True

def _matcher(*args):
    raise NotImplementedError('function _matcher has no body')

def UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime):
    return ' ' + StringFormat('%x', ADateTime) + StringFormat('%x', BDateTime) + StringFormat('%x', CDateTime) + StringFormat('%x', DDateTime)

def UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime):
    return ' ' + StringFormat('%x', XDateTime) + StringFormat('%x', ADateTime) + StringFormat('%x', BDateTime) + StringFormat('%x', CDateTime) + StringFormat('%x', DDateTime)

def Is4PointPattern(index):
    return index < 36

def OnInit():
    global _clrRatio, _faintBGColor, _timeOfInit
    SetIndexBuffer(0, _peaks, INDICATOR_DATA)
    SetIndexBuffer(1, _troughs, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    MathSrand(GetTickCount())
    _timeOfInit = MathRand()
    for i in range(ObjectsTotal(0, 0, -1) - 1, 0 - 1, -1):
        name = ObjectName(0, i, 0, -1)
        if StringFind(name, 'U ' + _identifier) != -1 or StringFind(name, 'D ' + _identifier) != -1:
            ObjectDelete(0, name)
    ret = PopulatePatterns()
    _purityFilter.SetActivated(i_puristPRZ)
    _timeFilter.SetActivated(i_timefilterEarly, i_timefilterLate)
    _commentator.SetStatistics(_statistics)
    _observers.Set(0, _statistics)
    _observers.Set(1, _drawer)
    _observers.Set(2, _commentator)
    _filters.Set(0, _purityFilter)
    _filters.Set(1, _timeFilter)
    _matcher.SetSlackRange(i_slackRange)
    _matcher.SetSlackUnary(i_slackSingular)
    _matcher.SetMatchProcessor(_indicator)
    _indicator.SetMaxOverlap(i_maxSamePoints)
    _indicator.SetObserver(_observers)
    _indicator.SetFilter(_filters)
    ChartGetInteger(0, CHART_COLOR_BACKGROUND, 0, _GlobRef(globals(), '_clrbackground'))
    _faintBGColor = ColorIntensity(_clrbackground, 40, True)
    _clrRatio = ColorIntensity(_clrbackground, 80, True)
    return ret

def OnDeinit(reason):
    OnReinit()
    Comment('')
    ArrayFree(_patterns)
    ArrayFree(_patternNames)

def OnReinit():
    global _lastPeak, _lastPeakValue, _lastTrough, _lastTroughValue
    _lastPeak = 0
    _lastTrough = 0
    _lastPeakValue = 0.0
    _lastTroughValue = 0.0
    ObjectsDeleteAll(0, 'U ' + _identifier + StringFormat('%x', _timeOfInit))
    ObjectsDeleteAll(0, 'D ' + _identifier + StringFormat('%x', _timeOfInit))
    ObjectsDeleteAll(0, 'PU ' + _identifier + StringFormat('%x', _timeOfInit))
    ObjectsDeleteAll(0, 'PD ' + _identifier + StringFormat('%x', _timeOfInit))
    _indicator.Reset()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _lastDirection, _lastPeak, _lastPeakValue, _lastTrough, _lastTroughValue
    ZZOnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread)
    start = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        OnReinit()
    else:
        start = prev_calculated - 1
    start = MathMax(1, start)
    ArrayCopy(_time, time, 0, 0)
    _drawer.SetBar(rates_total)
    _timeFilter.SetBar(rates_total)
    if i_timefilterEarly or i_timefilterLate:
        _timeFilter.SetPrices(low, high)
    for bar in range(start, rates_total):
        if bar < (rates_total - i_history):
            continue
        lastPeak = FirstNonZeroFrom(bar, _peaks)
        lastTrough = FirstNonZeroFrom(bar, _troughs)
        if lastPeak == -1 or lastTrough == -1:
            continue
        lastPeakValue = _peaks[lastPeak]
        lastTroughValue = _troughs[lastTrough]
        if lastPeakValue == _lastPeakValue and lastTroughValue == _lastTroughValue:
            continue
        endsInTrough = lastTrough > lastPeak
        if lastTrough == lastPeak:
            zzDirection = ZigZagDirection(lastPeak, _peaks, _troughs)
            if zzDirection == 0:
                continue
            elif zzDirection == -1:
                endsInTrough = True
            elif zzDirection == 1:
                endsInTrough = False
        UndisplayProjections()
        UndisplayPatterns(time)
        if not (_lastDirection == endsInTrough and (not (_lastPeak < lastPeak and _lastTrough < lastTrough))):
            _indicator.PersistTransient()
        _indicator.ClearTransient()
        _lastPeak = lastPeak
        _lastTrough = lastTrough
        _lastPeakValue = lastPeakValue
        _lastTroughValue = lastTroughValue
        _lastDirection = endsInTrough
        for patternIndex in range(0, 88):
            if not ShouldDisplay(patternIndex):
                continue
            pattern = _copy(_patterns[patternIndex])
            _indicator.PreFind(patternIndex)
            _matcher.FindPattern(pattern, bar - i_barsAnalyzed, bar, lastPeak, lastTrough, _peaks, _troughs)
            _indicator.PostFind(patternIndex, lastPeak, lastTrough, endsInTrough)
    return rates_total

def ZZOnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _atr, _contraIndex, _lastIndex, _lastIndex2, _realtimeChange, _zzLastDirection
    start = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        start = 1
        _lastIndex = 0
        _lastIndex2 = 0
        _contraIndex = 0
        _atr = 0.0
        _realtimeChange = False
    else:
        start = MathMax(1, prev_calculated - 1)
    atr = _atr
    bar = start
    while bar < (rates_total - (0 if i_zzRealtime else 1)):
        realtimeBar = bar == (rates_total - 1)
        if not realtimeBar:
            tr = MathMax(high[bar], close[bar - 1]) - MathMin(low[bar], close[bar - 1])
            atr += (tr - atr) * _fdiv(2.0, 1.0 + i_zzAtrPeriod)
            _atr = atr
            if _realtimeChange and i_zzRealtime:
                if _zzLastDirection:
                    _peaks[_lastIndex] = high[_lastIndex]
                else:
                    _troughs[_lastIndex] = low[_lastIndex]
                _peaks[rates_total - 1] = 0.0
                _troughs[rates_total - 1] = 0.0
                _realtimeChange = False
            _troughs[bar] = 0.0
            _peaks[bar] = 0.0
        shouldntChange = (bar - _lastIndex) < i_zzMinPeriod
        shallChange = (bar - _lastIndex) > i_zzMaxPeriod
        mustChange = False
        shouldChange = False
        canChange = False
        if _zzLastDirection:
            mustChange = low[bar] < low[_lastIndex2]
            shouldChange = (_peaks[_lastIndex] - low[bar]) > (atr * i_zzAtrMultiplier)
            canChange = low[bar] < low[_contraIndex]
        else:
            mustChange = high[bar] > high[_lastIndex2]
            shouldChange = (high[bar] - _troughs[_lastIndex]) > (atr * i_zzAtrMultiplier)
            canChange = high[bar] > high[_contraIndex]
        changeNow = mustChange or ((canChange and shouldChange) and (not shouldntChange))
        if realtimeBar and i_zzRealtime:
            if _zzLastDirection:
                if (not _realtimeChange) and high[bar] > _peaks[_lastIndex]:
                    _peaks[_lastIndex] = 0.0
                    _peaks[bar] = high[bar]
                    _realtimeChange = True
                elif _realtimeChange and high[bar] > _peaks[bar]:
                    _peaks[bar] = high[bar]
            else:
                if (not _realtimeChange) and low[bar] < _troughs[_lastIndex]:
                    _troughs[_lastIndex] = 0.0
                    _troughs[bar] = low[bar]
                    _realtimeChange = True
                elif _realtimeChange and low[bar] < _troughs[bar]:
                    _troughs[bar] = low[bar]
        else:
            if canChange:
                _contraIndex = bar
            if _zzLastDirection:
                if high[bar] > _peaks[_lastIndex]:
                    _peaks[_lastIndex] = 0.0
                    _peaks[bar] = high[bar]
                    if open[bar] > close[bar]:
                        shouldntChange = 0 < i_zzMinPeriod
                        shouldChange = (_peaks[bar] - low[bar]) > (atr * i_zzAtrMultiplier)
                        changeNow = mustChange or ((canChange and shouldChange) and (not shouldntChange))
                        if changeNow:
                            _troughs[bar] = low[bar]
                            _zzLastDirection = False
                            _lastIndex2 = bar
                    elif changeNow:
                        _peaks[_lastIndex] = high[_lastIndex]
                        _troughs[bar] = low[bar]
                        _lastIndex2 = bar
                    _lastIndex = bar
                    _contraIndex = bar
                elif changeNow:
                    _troughs[bar] = low[bar]
                    _zzLastDirection = False
                    _lastIndex2 = _lastIndex
                    _lastIndex = bar
                    _contraIndex = bar
                elif shallChange:
                    startSkip = (0 if (_troughs[_lastIndex] == 0) else 1)
                    if open[_lastIndex] < close[_lastIndex] and startSkip == 0:
                        startSkip += 1
                    bar = ArrayMinimum(low, _lastIndex + startSkip, bar - _lastIndex - startSkip + 1)
                    _troughs[bar] = low[bar]
                    _zzLastDirection = False
                    _lastIndex2 = _lastIndex
                    _lastIndex = bar
                    _contraIndex = bar
            else:
                if low[bar] < _troughs[_lastIndex]:
                    _troughs[_lastIndex] = 0.0
                    _troughs[bar] = low[bar]
                    if open[bar] < close[bar]:
                        shouldntChange = 0 < i_zzMinPeriod
                        shouldChange = (high[bar] - _troughs[bar]) > (atr * i_zzAtrMultiplier)
                        changeNow = mustChange or ((canChange and shouldChange) and (not shouldntChange))
                        if changeNow:
                            _peaks[bar] = high[bar]
                            _zzLastDirection = True
                            _lastIndex2 = bar
                    elif changeNow:
                        _troughs[_lastIndex] = low[_lastIndex]
                        _peaks[bar] = high[bar]
                        _lastIndex2 = bar
                    _lastIndex = bar
                    _contraIndex = bar
                elif changeNow:
                    _peaks[bar] = high[bar]
                    _zzLastDirection = True
                    _lastIndex2 = _lastIndex
                    _lastIndex = bar
                    _contraIndex = bar
                elif shallChange:
                    startSkip = (0 if (_peaks[_lastIndex] == 0) else 1)
                    if open[_lastIndex] > close[_lastIndex] and startSkip == 0:
                        startSkip += 1
                    bar = ArrayMaximum(high, _lastIndex + startSkip, bar - _lastIndex - startSkip + 1)
                    _peaks[bar] = high[bar]
                    _zzLastDirection = True
                    _lastIndex2 = _lastIndex
                    _lastIndex = bar
                    _contraIndex = bar
            _peaks[rates_total - 1] = 0.0
            _troughs[rates_total - 1] = 0.0
        bar += 1
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global _prevClick
    if id_ != CHARTEVENT_OBJECT_CLICK:
        return
    if not StringFind(_identifier + StringFormat('%x', _timeOfInit), sparam, 0):
        return
    doubleClicked = (GetTickCount() - _prevClick) < 1000
    _prevClick = GetTickCount()
    if not doubleClicked:
        return
    projection = StringFind(StringSubstr(sparam, 0, 1), 'P', 0) >= 0
    bullish = StringFind(StringSubstr(sparam, 0, 2), 'U', 0) >= 0
    splitString = Arr(0, "")
    StringSplit(sparam, 32, splitString)
    indx = StringSubstr(splitString[1], StringLen(_identifier + StringFormat('%x', _timeOfInit)))
    patternIndex = _int(StringToInteger(indx))
    if ArraySize(splitString) < 4:
        return
    unique = ' ' + splitString[3]
    is4PointPattern = _indicator.Is4PointPattern(patternIndex)
    prefixName = ('P' if projection else '') + ('U ' if bullish else 'D ') + _identifier + StringFormat('%x', _timeOfInit) + IntegerToString(patternIndex)
    name0 = prefixName + ' XA' + unique
    name1 = prefixName + ' AB' + unique
    name2 = prefixName + ' BC' + unique
    name3 = prefixName + ' CD' + unique
    name4 = prefixName + ' XAB' + unique
    name5 = prefixName + ' XAD' + unique
    name6 = prefixName + ' ABC' + unique
    name7 = prefixName + ' BCD' + unique
    pointX = prefixName + ' PX' + unique
    pointA = prefixName + ' PA' + unique
    pointB = prefixName + ' PB' + unique
    pointC = prefixName + ' PC' + unique
    pointD = prefixName + ' PD' + unique
    triangle_XB = prefixName + ' XB' + unique
    triangle_BD = prefixName + ' BD' + unique
    prz = prefixName + ' PRZ' + unique
    transient = False
    if ObjectFind(0, prz) >= 0:
        transient = True
    else:
        prz = prefixName + ' PRS' + unique
    X = ObjectGetDouble(0, name0, OBJPROP_PRICE, 0)
    A = ObjectGetDouble(0, name1, OBJPROP_PRICE, 0)
    B = ObjectGetDouble(0, name2, OBJPROP_PRICE, 0)
    C = ObjectGetDouble(0, name2, OBJPROP_PRICE, 1)
    XDateTime = ObjectGetInteger(0, name0, OBJPROP_TIME, 0)
    ADateTime = ObjectGetInteger(0, name1, OBJPROP_TIME, 0)
    BDateTime = ObjectGetInteger(0, name2, OBJPROP_TIME, 0)
    CDateTime = ObjectGetInteger(0, name2, OBJPROP_TIME, 1)
    DDateTime = ObjectGetInteger(0, name3, OBJPROP_TIME, 1)
    linePRZ = prefixName + ' PRH' + unique
    timeZones = prefixName + ' T' + unique
    lineXAD = prefixName + ' lv1' + unique
    lineXCD = prefixName + ' lv2' + unique
    lineBCD = prefixName + ' lv3' + unique
    lineACD = prefixName + ' lv4' + unique
    lineCD2AD = prefixName + ' lv5' + unique
    prefix = ""
    if projection:
        prefix = ('Proj. Bullish ' if bullish else 'Proj. Bearish ')
    else:
        prefix = ('Bullish ' if bullish else 'Bearish ')
    clr = _clrRatio
    clrRatio = _clrRatio
    clrLeg = clr
    width = i_lineWidth
    widthPRZ = 1
    selected = (ObjectGetInteger(0, sparam, OBJPROP_SELECTED) != 0)
    if selected:
        clrRatio = i_clrFocus
        clr = clrRatio
        clrLeg = clr
        width = i_lineWidthFoc
        widthPRZ = 2
        comment = ('F. Bull. ' if bullish else 'F. Bear. ')
        comment += _patternNames[patternIndex]
        comment += ' Prob. ' + DoubleToString(_statistics.GetSuccessRate(patternIndex) * 100, 2)
        comment += ' (' + _str(_statistics.GetSuccesses(patternIndex)) + ' S/ ' + _str(_statistics.GetFailures(patternIndex)) + ' F)'
        _commentator.ShowComment(comment)
        if not transient:
            nearD = Box(0.0)
            farD = Box(0.0)
            HarmonicWindow(_patterns[patternIndex], i_slackSingular, i_slackRange, bullish, X, A, B, C, nearD, farD)
            ObjectCreate(0, linePRZ, OBJ_TREND, 0, DDateTime - 1, farD.v, DDateTime + _deltaDT, farD.v)
            ObjectSetInteger(0, linePRZ, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, linePRZ, OBJPROP_COLOR, clr)
            ObjectSetInteger(0, linePRZ, OBJPROP_WIDTH, widthPRZ)
            ObjectSetString(0, linePRZ, OBJPROP_TOOLTIP, prefix + _patternNames[patternIndex] + ' PRZ stop ' + DoubleToString(NormalizeDouble(farD.v, Digits()), Digits()))
        levels = HarmonicRatios(_patterns[patternIndex], bullish, X, A, B, C)
        CreateLine(lineXAD, DDateTime, levels.ad2xa, clr, i_stylePRZ, 1, prefix, patternIndex, ' AD2XA level (', _patterns[patternIndex].ad2xa_min)
        CreateLine(lineXCD, DDateTime, levels.cd2xc, clr, i_stylePRZ, 1, prefix, patternIndex, ' CD2XC level (', _patterns[patternIndex].cd2xc_min)
        CreateLine(lineBCD, DDateTime, levels.cd2bc, clr, i_stylePRZ, 1, prefix, patternIndex, ' CD2BC level (', _patterns[patternIndex].cd2bc_min)
        CreateLine(lineACD, DDateTime, levels.cd2ab, clr, i_stylePRZ, 1, prefix, patternIndex, ' CD2AB level (', _patterns[patternIndex].cd2ab_min)
        CreateLine(lineCD2AD, DDateTime, levels.cd2ad, clr, i_stylePRZ, 1, prefix, patternIndex, ' CD2AD level (', _patterns[patternIndex].cd2ad_min)
        minVisiblePrice = ChartGetDouble(0, CHART_PRICE_MIN)
        if not is4PointPattern:
            ObjectCreate(0, timeZones, OBJ_FIBOTIMES, 0, XDateTime, 0, BDateTime, minVisiblePrice)
        else:
            numBars = Bars(Symbol(), Period())
            if numBars < 1:
                ObjectCreate(0, timeZones, OBJ_FIBOTIMES, 0, CDateTime, A, CDateTime + (BDateTime - ADateTime), B)
            else:
                time = Arr(0, 0)
                CopyTime(Symbol(), Period(), 0, numBars, time)
                ABar = -1
                BBar = -1
                CBar = -1
                for i in range(0, numBars):
                    if time[i] == ADateTime:
                        ABar = i
                    if time[i] == BDateTime:
                        BBar = i
                    if time[i] == CDateTime:
                        CBar = i
                        break
                legBars = BBar - ABar
                secondAnchor = 0
                if (numBars - CBar) > legBars and (CBar + legBars) >= 0:
                    secondAnchor = time[CBar + legBars]
                else:
                    futureBars = 1 + CBar + legBars - numBars
                    secondAnchor = time[numBars - 1] + (futureBars * PeriodSeconds())
                ObjectCreate(0, timeZones, OBJ_FIBOTIMES, 0, CDateTime, 0, secondAnchor, minVisiblePrice)
        ObjectSetInteger(0, timeZones, OBJPROP_COLOR, clrNONE)
        ObjectSetString(0, timeZones, OBJPROP_TOOLTIP, prefix + _patternNames[patternIndex] + ' Timezones ')
        fibColor = clrNONE
        if (projection and bullish) and is4PointPattern:
            fibColor = i_clrBullProjection4P
        elif (projection and bullish) and (not is4PointPattern):
            fibColor = i_clrBullProjection
        elif (projection and (not bullish)) and is4PointPattern:
            fibColor = i_clrBearProjection4P
        elif (projection and (not bullish)) and (not is4PointPattern):
            fibColor = i_clrBearProjection
        elif ((not projection) and bullish) and is4PointPattern:
            fibColor = i_clrBull4P
        elif ((not projection) and bullish) and (not is4PointPattern):
            fibColor = i_clrBull
        elif ((not projection) and (not bullish)) and is4PointPattern:
            fibColor = i_clrBear4P
        elif ((not projection) and (not bullish)) and (not is4PointPattern):
            fibColor = i_clrBear
        shift = (0 if is4PointPattern else 1)
        fibStyle = i_styleProj
        fibWidth = 1
        chart_ID = 0
        name = timeZones
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELS, 3)
        ObjectSetDouble(chart_ID, name, OBJPROP_LEVELVALUE, 0, i_tooEarly + shift)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELCOLOR, 0, fibColor)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELSTYLE, 0, fibStyle)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELWIDTH, 0, fibWidth)
        ObjectSetString(chart_ID, name, OBJPROP_LEVELTEXT, 0, DoubleToString(i_tooEarly + shift, 3))
        ObjectSetDouble(chart_ID, name, OBJPROP_LEVELVALUE, 1, i_ideal + shift)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELCOLOR, 1, fibColor)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELSTYLE, 1, fibStyle)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELWIDTH, 1, fibWidth)
        ObjectSetString(chart_ID, name, OBJPROP_LEVELTEXT, 1, DoubleToString(i_ideal + shift, 3))
        ObjectSetDouble(chart_ID, name, OBJPROP_LEVELVALUE, 2, i_tooLate + shift)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELCOLOR, 2, fibColor)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELSTYLE, 2, fibStyle)
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELWIDTH, 2, fibWidth)
        ObjectSetString(chart_ID, name, OBJPROP_LEVELTEXT, 2, DoubleToString(i_tooLate + shift, 3))
    else:
        ObjectDelete(0, linePRZ)
        ObjectDelete(0, lineXAD)
        ObjectDelete(0, lineXCD)
        ObjectDelete(0, lineBCD)
        ObjectDelete(0, lineACD)
        ObjectDelete(0, lineCD2AD)
        ObjectDelete(0, timeZones)
        if projection:
            if bullish:
                if is4PointPattern:
                    clr = i_clrBullProjection4P
                else:
                    clr = i_clrBullProjection
            else:
                if is4PointPattern:
                    clr = i_clrBearProjection4P
                else:
                    clr = i_clrBearProjection
            width = i_lineWidthProj
            clrLeg = (_faintBGColor if i_showSoftProjections else clr)
            clrRatio = (_faintBGColor if i_showSoftProjections else _clrRatio)
        else:
            if bullish and is4PointPattern:
                clr = i_clrBull4P
            if bullish and (not is4PointPattern):
                clr = i_clrBull
            if (not bullish) and is4PointPattern:
                clr = i_clrBear4P
            if (not bullish) and (not is4PointPattern):
                clr = i_clrBear
            width = i_lineWidth
            clrLeg = clr
            clrRatio = _clrRatio
    ObjectSetInteger(0, name0, OBJPROP_COLOR, clrLeg)
    ObjectSetInteger(0, name0, OBJPROP_WIDTH, width)
    ObjectSetInteger(0, name1, OBJPROP_COLOR, clrLeg)
    ObjectSetInteger(0, name1, OBJPROP_WIDTH, width)
    ObjectSetInteger(0, name2, OBJPROP_COLOR, clrLeg)
    ObjectSetInteger(0, name2, OBJPROP_WIDTH, width)
    ObjectSetInteger(0, name3, OBJPROP_COLOR, clrLeg)
    ObjectSetInteger(0, name3, OBJPROP_WIDTH, width)
    ObjectSetInteger(0, name4, OBJPROP_COLOR, clrRatio)
    ObjectSetInteger(0, name5, OBJPROP_COLOR, clrRatio)
    ObjectSetInteger(0, name6, OBJPROP_COLOR, clrRatio)
    ObjectSetInteger(0, name7, OBJPROP_COLOR, clrRatio)
    ObjectSetInteger(0, pointX, OBJPROP_COLOR, clrLeg)
    ObjectSetInteger(0, pointA, OBJPROP_COLOR, clrLeg)
    ObjectSetInteger(0, pointB, OBJPROP_COLOR, clrLeg)
    ObjectSetInteger(0, pointC, OBJPROP_COLOR, clrLeg)
    ObjectSetInteger(0, pointD, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, triangle_XB, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, triangle_BD, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, prz, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, prz, OBJPROP_WIDTH, widthPRZ)
    ChartRedraw()

def CreateLine(line, DDateTime, level, clr, style, width, prefix, patternIndex, levelName, levelDef):
    ObjectCreate(0, line, OBJ_TREND, 0, DDateTime - 1, level, DDateTime + _deltaDT, level)
    ObjectSetInteger(0, line, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, line, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, line, OBJPROP_STYLE, style)
    ObjectSetInteger(0, line, OBJPROP_WIDTH, width)
    ObjectSetString(0, line, OBJPROP_TOOLTIP, prefix + _patternNames[patternIndex] + levelName + DoubleToString(NormalizeDouble(levelDef, Digits()), 3) + ') ' + DoubleToString(NormalizeDouble(level, Digits()), Digits()))

def ColorIntensity(lcolor, ishift=30, dim=False):
    blue = _int(MathFloor(_idiv(lcolor, 65536)))
    green = _int(MathFloor(_idiv(lcolor - (blue * 65536), 256)))
    red = _int(lcolor) - (blue * 65536) - (green * 256)
    if dim:
        blue = ((blue + ishift + _idiv(blue * ishift, 100)) if (blue < 127) else (blue - ishift - _idiv(blue * ishift, 100)))
        green = ((green + ishift + _idiv(green * ishift, 100)) if (green < 127) else (green - ishift - _idiv(green * ishift, 100)))
        red = ((red + ishift + _idiv(red * ishift, 100)) if (red < 127) else (red - ishift - _idiv(red * ishift, 100)))
    else:
        red = red + _idiv(red * ishift, 100)
        green = green + _idiv(green * ishift, 100)
        blue = blue + _idiv(blue * ishift, 100)
    red = (255 if (red > 255) else red)
    red = (0 if (red < 0) else red)
    green = (255 if (green > 255) else green)
    green = (0 if (green < 0) else green)
    blue = (255 if (blue > 255) else blue)
    blue = (0 if (blue < 0) else blue)
    sred = IntegerToString(red)
    sgreen = IntegerToString(green)
    sblue = IntegerToString(blue)
    return StringToColor(sred + ',' + sgreen + ',' + sblue)

def UndisplayProjections():
    ObjectsDeleteAll(0, 'PU ' + _identifier)
    ObjectsDeleteAll(0, 'PD ' + _identifier)

def UndisplayPatterns(time):
    for k in range(0, 88):
        stored = _indicator.GetMatchedTransient(k)
        tail = stored.GetTail()
        head = stored.GetHead()
        capacity = stored.GetCapacity()
        j = tail
        while j != head:
            match = stored.GetMatch(j)
            bullish = match.bullish
            XDateTime = time[match.XIndex]
            ADateTime = time[match.AIndex]
            BDateTime = time[match.BIndex]
            CDateTime = time[match.CIndex]
            DDateTime = time[match.DIndex]
            unique = (UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime) if _indicator.Is4PointPattern(k) else UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime))
            prefix = (('U ' + _identifier) if bullish else ('D ' + _identifier))
            name0 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XA' + unique
            name1 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' AB' + unique
            name2 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BC' + unique
            name3 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' CD' + unique
            name4 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XAB' + unique
            name5 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XAD' + unique
            name6 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' ABC' + unique
            name7 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BCD' + unique
            triangle_XB = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XB' + unique
            triangle_BD = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BD' + unique
            pointX = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PX' + unique
            pointA = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PA' + unique
            pointB = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PB' + unique
            pointC = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PC' + unique
            pointD = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PD' + unique
            ObjectDelete(0, name0)
            ObjectDelete(0, name1)
            ObjectDelete(0, name2)
            ObjectDelete(0, name3)
            ObjectDelete(0, name4)
            ObjectDelete(0, name5)
            ObjectDelete(0, name6)
            ObjectDelete(0, name7)
            ObjectDelete(0, triangle_XB)
            ObjectDelete(0, triangle_BD)
            ObjectDelete(0, pointX)
            ObjectDelete(0, pointA)
            ObjectDelete(0, pointB)
            ObjectDelete(0, pointC)
            ObjectDelete(0, pointD)
            j = _imod(j + 1, capacity)
    for k in range(0, 88):
        stored = _indicator.GetMatchedTransient(k)
        tail = stored.GetTail()
        head = stored.GetHead()
        capacity = stored.GetCapacity()
        j = tail
        while j != head:
            match = stored.GetMatch(j)
            bullish = match.bullish
            XDateTime = time[match.XIndex]
            ADateTime = time[match.AIndex]
            BDateTime = time[match.BIndex]
            CDateTime = time[match.CIndex]
            DDateTime = time[match.DIndex]
            unique = (UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime) if _indicator.Is4PointPattern(k) else UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime))
            prefix = (('U ' + _identifier) if bullish else ('D ' + _identifier))
            linePRZ = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PRZ' + unique
            ObjectDelete(0, linePRZ)
            j = _imod(j + 1, capacity)

def PopulatePatterns():
    trendlike1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.382, 0.382, 2.618, 2.618, 0, 0, 0, 0, 0, 0, 1, 1])
    trendlike2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.5, 0.5, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 1, 1])
    perfect_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.618, 0.618, 1.618, 1.618, 0, 0, 0, 0, 0, 0, 1, 1])
    ideal1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.707, 0.707, 1.41, 1.41, 0, 0, 0, 0, 0, 0, 1, 1])
    ideal2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.786, 0.786, 1.27, 1.27, 0, 0, 0, 0, 0, 0, 1, 1])
    rangelike_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.886, 0.886, 1.13, 1.13, 0, 0, 0, 0, 0, 0, 1, 1])
    alt127_trendlike1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.382, 0.382, 2.618, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_trendlike2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.5, 0.5, 2.0, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_perfect_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.618, 0.618, 1.618, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_ideal1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.707, 0.707, 1.41, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_ideal2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.786, 0.786, 1.27, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_rangelike_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.886, 0.886, 1.13, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt161_trendlike1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.382, 0.382, 2.618, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_trendlike2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.5, 0.5, 2.0, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_perfect_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.618, 0.618, 1.618, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_ideal1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.707, 0.707, 1.41, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_ideal2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.786, 0.786, 1.27, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_rangelike_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.886, 0.886, 1.13, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    rec_trendlike1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 2.618, 2.618, 0.382, 0.382, 0, 0, 0, 0, 0, 0, 1, 1])
    rec_trendlike2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 2.0, 2.0, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 1, 1])
    rec_perfect_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.618, 1.618, 0.618, 0.618, 0, 0, 0, 0, 0, 0, 1, 1])
    rec_ideal1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.41, 1.41, 0.707, 0.707, 0, 0, 0, 0, 0, 0, 1, 1])
    rec_ideal2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.27, 1.27, 0.786, 0.786, 0, 0, 0, 0, 0, 0, 1, 1])
    rec_rangelike_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.13, 1.13, 0.886, 0.886, 0, 0, 0, 0, 0, 0, 1, 1])
    alt127_rec_trendlike1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 2.618, 2.618, 0.382, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_rec_trendlike2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 2.0, 2.0, 0.5, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_rec_perfect_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.618, 1.618, 0.618, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_rec_ideal1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.41, 1.41, 0.707, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_rec_ideal2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.27, 1.27, 0.786, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_rec_rangelike_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.13, 1.13, 0.886, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt161_rec_trendlike1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 2.618, 2.618, 0.382, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_rec_trendlike2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 2.0, 2.0, 0.5, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_rec_perfect_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.618, 1.618, 0.618, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_rec_ideal1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.41, 1.41, 0.707, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_rec_ideal2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.27, 1.27, 0.786, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    alt161_rec_rangelike_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.13, 1.13, 0.886, 3.618, 0, 0, 0, 0, 0, 0, 1.618, 1.618])
    perfect_gartley = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.618, 0.618, 0.618, 1.618, 1.618, 0.786, 0.786, 0, 0, 0, 0, 0, 0])
    perfect_bat = _struct_init(PATTERN_DESCRIPTOR(), [0.5, 0.5, 0.5, 0.618, 2, 2, 0.886, 0.886, 0, 0, 0, 0, 0, 0])
    gartley = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.618, 0.382, 0.886, 1.272, 1.618, 0.786, 0.786, 0, 0, 0, 0, 0, 0])
    gartley113 = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.618, 0.886, 0.886, 1.13, 1.13, 0.786, 0.786, 0, 0, 0, 0, 0, 0])
    maxgartley = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0.382, 0.886, 1.128, 2.236, 0.618, 0.786, 0, 0, 0, 0, 0, 0])
    bat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.5, 0.382, 0.886, 1.618, 2.618, 0.886, 0.886, 0, 0, 0, 0, 0, 0])
    altbat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.382, 0.382, 0.886, 2.0, 3.618, 1.13, 1.13, 0, 0, 0, 0, 0, 0])
    maxbat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0.382, 0.886, 1.272, 2.618, 0.886, 0.886, 0, 0, 0, 0, 0, 0])
    crab = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0.382, 0.886, 2.24, 3.618, 1.618, 1.618, 0, 0, 0, 0, 0, 0])
    perfect_crab = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.618, 0.5, 0.618, 3.14, 3.14, 1.618, 1.618, 0, 0, 0, 0, 1.618, 1.618])
    deepcrab = _struct_init(PATTERN_DESCRIPTOR(), [0.886, 0.886, 0.382, 0.886, 2.0, 3.618, 1.618, 1.618, 0, 0, 0, 0, 0, 0])
    butterfly = _struct_init(PATTERN_DESCRIPTOR(), [0.786, 0.786, 0.382, 0.886, 1.618, 2.618, 1.272, 1.272, 0, 0, 0, 0, 0, 0])
    perfect_butterfly = _struct_init(PATTERN_DESCRIPTOR(), [0.786, 0.786, 0.5, 0.886, 1.618, 1.618, 1.272, 1.272, 0, 0, 0, 0, 1.272, 1.272])
    maxbutterfly = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.886, 0.382, 0.886, 1.272, 2.618, 1.272, 1.618, 0, 0, 0, 0, 0, 0])
    butterfly113 = _struct_init(PATTERN_DESCRIPTOR(), [0.786, 1, 0.618, 1, 1.128, 1.618, 1.128, 1.128, 0, 0, 0, 0, 0, 0])
    fiveo = _struct_init(PATTERN_DESCRIPTOR(), [1.13, 1.618, 1.618, 2.24, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0])
    threedrives = _struct_init(PATTERN_DESCRIPTOR(), [1.272, 1.618, 0.618, 0.786, 1.272, 1.618, 0, 0, 0, 0, 0, 0, 0, 0])
    shark = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.13, 1.618, 1.618, 2.24, 0, 0, 0.886, 1.13, 0, 0, 0, 0])
    cypher = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0, 0, 0, 0, 0, 0, 0.786, 0.786, 1.13, 1.414, 0, 0])
    nenstar = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272, 1.13, 1.414, 0, 0])
    blackswan = _struct_init(PATTERN_DESCRIPTOR(), [1.382, 2.618, 0.236, 0.5, 1.128, 2, 1.128, 2.618, 0, 0, 0, 0, 0, 0])
    whiteswan = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.724, 2, 4.237, 0.5, 0.886, 0.382, 0.886, 0, 0, 0, 0, 0, 0])
    one2one = _struct_init(PATTERN_DESCRIPTOR(), [0.5, 0.786, 1.128, 3.618, 0.382, 0.786, 0.382, 0.786, 0, 0, 0, 0, 0, 0])
    newcypher = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0, 0, 0, 0, 0, 0, 0.786, 0.786, 1.414, 2.14, 0, 0])
    navarro200 = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.786, 0.886, 1.128, 0.886, 3.618, 0.886, 1.128, 0, 0, 0, 0, 0, 0])
    leonardo = _struct_init(PATTERN_DESCRIPTOR(), [0.5, 0.5, 0.382, 0.886, 1.128, 2.618, 0.786, 0.786, 0, 0, 0, 0, 0, 0])
    kane = _struct_init(PATTERN_DESCRIPTOR(), [0.685, 0.685, 0.382, 0.886, 0, 0, 1.46, 1.46, 0, 0, 0, 0, 0, 0])
    garfly = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.618, 0.382, 0.886, 1.618, 2.24, 1.272, 1.272, 0, 0, 0, 0, 0, 0])
    anti_gartley = Invert(gartley)
    anti_bat = Invert(bat)
    anti_altbat = Invert(altbat)
    anti_fiveo = Invert(fiveo)
    anti_butterfly = Invert(butterfly)
    anti_crab = Invert(crab)
    anti_deepcrab = Invert(deepcrab)
    anti_threedrives = Invert(threedrives)
    anti_shark = Invert(shark)
    anti_cypher = Invert(cypher)
    anti_nenstar = Invert(nenstar)
    anti_blackswan = Invert(blackswan)
    anti_whiteswan = Invert(whiteswan)
    anti_one2one = Invert(one2one)
    anti_newcypher = Invert(newcypher)
    anti_navarro200 = Invert(navarro200)
    anti_leonardo = Invert(leonardo)
    anti_kane = Invert(kane)
    anti_garfly = Invert(garfly)
    anti_maxbat = Invert(maxbat)
    anti_maxgartley = Invert(maxgartley)
    anti_maxbutterfly = Invert(maxbutterfly)
    anti_gartley113 = Invert(gartley113)
    anti_butterfly113 = Invert(butterfly113)
    if ArrayResize(_patterns, 88) < 88:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_patternNames, 88) < 88:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    fillPatternArrays(TRENDLIKE1_ABCD, trendlike1_abcd, 'Trendlike AB=CD #1')
    fillPatternArrays(TRENDLIKE2_ABCD, trendlike2_abcd, 'Trendlike AB=CD #2')
    fillPatternArrays(PERFECT_ABCD, perfect_abcd, 'Perfect AB=CD')
    fillPatternArrays(IDEAL1_ABCD, ideal1_abcd, 'Ideal AB=CD #1')
    fillPatternArrays(IDEAL2_ABCD, ideal2_abcd, 'Ideal AB=CD #2')
    fillPatternArrays(RANGELIKE_ABCD, rangelike_abcd, 'Rangelike AB=CD')
    fillPatternArrays(ALT127_TRENDLIKE1_ABCD, alt127_trendlike1_abcd, 'Trendlike 1.27 AB=CD #1')
    fillPatternArrays(ALT127_TRENDLIKE2_ABCD, alt127_trendlike2_abcd, 'Trendlike 1.27 AB=CD #2')
    fillPatternArrays(ALT127_PERFECT_ABCD, alt127_perfect_abcd, 'Perfect 1.27 AB=CD')
    fillPatternArrays(ALT127_IDEAL1_ABCD, alt127_ideal1_abcd, 'Ideal 1.27 AB=CD #1')
    fillPatternArrays(ALT127_IDEAL2_ABCD, alt127_ideal2_abcd, 'Ideal 1.27 AB=CD #2')
    fillPatternArrays(ALT127_RANGELIKE_ABCD, alt127_rangelike_abcd, 'Rangelike 1.27 AB=CD')
    fillPatternArrays(ALT161_TRENDLIKE1_ABCD, alt161_trendlike1_abcd, 'Trendlike 1.61 AB=CD #1')
    fillPatternArrays(ALT161_TRENDLIKE2_ABCD, alt161_trendlike2_abcd, 'Trendlike 1.61 AB=CD #2')
    fillPatternArrays(ALT161_PERFECT_ABCD, alt161_perfect_abcd, 'Perfect 1.61 AB=CD')
    fillPatternArrays(ALT161_IDEAL1_ABCD, alt161_ideal1_abcd, 'Ideal 1.61 AB=CD #1')
    fillPatternArrays(ALT161_IDEAL2_ABCD, alt161_ideal2_abcd, 'Ideal 1.61 AB=CD #2')
    fillPatternArrays(ALT161_RANGELIKE_ABCD, alt161_rangelike_abcd, 'Rangelike 1.61 AB=CD')
    fillPatternArrays(REC_TRENDLIKE1_ABCD, rec_trendlike1_abcd, 'Rec. Trendlike AB=CD #1')
    fillPatternArrays(REC_TRENDLIKE2_ABCD, rec_trendlike2_abcd, 'Rec. Trendlike AB=CD #2')
    fillPatternArrays(REC_PERFECT_ABCD, rec_perfect_abcd, 'Rec. Perfect AB=CD')
    fillPatternArrays(REC_IDEAL1_ABCD, rec_ideal1_abcd, 'Rec. Ideal AB=CD #1')
    fillPatternArrays(REC_IDEAL2_ABCD, rec_ideal2_abcd, 'Rec. Ideal AB=CD #2')
    fillPatternArrays(REC_RANGELIKE_ABCD, rec_rangelike_abcd, 'Rec. Rangelike AB=CD')
    fillPatternArrays(ALT127_REC_TRENDLIKE1_ABCD, alt127_rec_trendlike1_abcd, 'Rec. Trendlike 1.27 AB=CD #1')
    fillPatternArrays(ALT127_REC_TRENDLIKE2_ABCD, alt127_rec_trendlike2_abcd, 'Rec. Trendlike 1.27 AB=CD #2')
    fillPatternArrays(ALT127_REC_PERFECT_ABCD, alt127_rec_perfect_abcd, 'Rec. Perfect 1.27 AB=CD')
    fillPatternArrays(ALT127_REC_IDEAL1_ABCD, alt127_rec_ideal1_abcd, 'Rec. Ideal 1.27 AB=CD #1')
    fillPatternArrays(ALT127_REC_IDEAL2_ABCD, alt127_rec_ideal2_abcd, 'Rec. Ideal 1.27 AB=CD #2')
    fillPatternArrays(ALT127_REC_RANGELIKE_ABCD, alt127_rec_rangelike_abcd, 'Rec. Rangelike 1.27 AB=CD')
    fillPatternArrays(ALT161_REC_TRENDLIKE1_ABCD, alt161_rec_trendlike1_abcd, 'Rec. Trendlike 1.61 AB=CD #1')
    fillPatternArrays(ALT161_REC_TRENDLIKE2_ABCD, alt161_rec_trendlike2_abcd, 'Rec. Trendlike 1.61 AB=CD #2')
    fillPatternArrays(ALT161_REC_PERFECT_ABCD, alt161_rec_perfect_abcd, 'Rec. Perfect 1.61 AB=CD')
    fillPatternArrays(ALT161_REC_IDEAL1_ABCD, alt161_rec_ideal1_abcd, 'Rec. Ideal 1.61 AB=CD #1')
    fillPatternArrays(ALT161_REC_IDEAL2_ABCD, alt161_rec_ideal2_abcd, 'Rec. Ideal 1.61 AB=CD #2')
    fillPatternArrays(ALT161_REC_RANGELIKE_ABCD, alt161_rec_rangelike_abcd, 'Rec. Rangelike 1.61 AB=CD')
    fillPatternArrays(GARTLEY, gartley, 'Gartley')
    fillPatternArrays(PERFECT_GARTLEY, perfect_gartley, 'Perfect Gartley')
    fillPatternArrays(GARTLEY113, gartley113, 'Gartley 113')
    fillPatternArrays(MAXGARTLEY, maxgartley, 'Max. Gartley')
    fillPatternArrays(BAT, bat, 'Bat')
    fillPatternArrays(PERFECT_BAT, perfect_bat, 'Perfect Bat')
    fillPatternArrays(ALTBAT, altbat, 'Alt. Bat')
    fillPatternArrays(MAXBAT, maxbat, 'Max. Bat')
    fillPatternArrays(CRAB, crab, 'Crab')
    fillPatternArrays(PERFECT_CRAB, perfect_crab, 'Perfect Crab')
    fillPatternArrays(DEEPCRAB, deepcrab, 'Deep Crab')
    fillPatternArrays(BUTTERFLY, butterfly, 'Butterfly')
    fillPatternArrays(PERFECT_BUTTERFLY, perfect_butterfly, 'Perfect Butterfly')
    fillPatternArrays(MAXBUTTERFLY, maxbutterfly, 'Max. Butterfly')
    fillPatternArrays(BUTTERFLY113, butterfly113, 'Butterfly 113')
    fillPatternArrays(FIVEO, fiveo, '5-0')
    fillPatternArrays(THREEDRIVES, threedrives, 'Three Drives')
    fillPatternArrays(CYPHER, cypher, 'Cypher')
    fillPatternArrays(SHARK, shark, 'Shark')
    fillPatternArrays(NENSTAR, nenstar, 'Nen Star')
    fillPatternArrays(BLACKSWAN, blackswan, 'Black Swan')
    fillPatternArrays(WHITESWAN, whiteswan, 'White Swan')
    fillPatternArrays(ONE2ONE, one2one, 'One2One')
    fillPatternArrays(NEWCYPHER, newcypher, 'New Cypher')
    fillPatternArrays(NAVARRO200, navarro200, 'Navarro 200')
    fillPatternArrays(LEONARDO, leonardo, 'Leonardo')
    fillPatternArrays(KANE, kane, 'Kane')
    fillPatternArrays(GARFLY, garfly, 'Garfly')
    fillPatternArrays(ANTI_GARTLEY, anti_gartley, 'Anti Gartley')
    fillPatternArrays(ANTI_BAT, anti_bat, 'Anti Bat')
    fillPatternArrays(ANTI_ALTBAT, anti_altbat, 'Anti Alt. Bat')
    fillPatternArrays(ANTI_FIVEO, anti_fiveo, 'Anti 5-0')
    fillPatternArrays(ANTI_BUTTERFLY, anti_butterfly, 'Anti Butterfly')
    fillPatternArrays(ANTI_CRAB, anti_crab, 'Anti Crab')
    fillPatternArrays(ANTI_DEEPCRAB, anti_deepcrab, 'Anti Deep Crab')
    fillPatternArrays(ANTI_THREEDRIVES, anti_threedrives, 'Anti Three Drives')
    fillPatternArrays(ANTI_CYPHER, anti_cypher, 'Anti Cypher')
    fillPatternArrays(ANTI_SHARK, anti_shark, 'Anti Shark')
    fillPatternArrays(ANTI_NENSTAR, anti_nenstar, 'Anti Nen Star')
    fillPatternArrays(ANTI_BLACKSWAN, anti_blackswan, 'Anti Black Swan')
    fillPatternArrays(ANTI_WHITESWAN, anti_whiteswan, 'Anti White Swan')
    fillPatternArrays(ANTI_ONE2ONE, anti_one2one, 'Anti One2One')
    fillPatternArrays(ANTI_NEWCYPHER, anti_newcypher, 'Anti New Cypher')
    fillPatternArrays(ANTI_NAVARRO200, anti_navarro200, 'Anti Navarro 200')
    fillPatternArrays(ANTI_LEONARDO, anti_leonardo, 'Anti Leonardo')
    fillPatternArrays(ANTI_KANE, anti_kane, 'Anti Kane')
    fillPatternArrays(ANTI_GARFLY, anti_garfly, 'Anti Garfly')
    fillPatternArrays(ANTI_MAXBAT, anti_maxbat, 'Anti Max. Bat')
    fillPatternArrays(ANTI_MAXGARTLEY, anti_maxgartley, 'Anti Max. Gartley')
    fillPatternArrays(ANTI_MAXBUTTERFLY, anti_maxbutterfly, 'Anti Max. Butterfly')
    fillPatternArrays(ANTI_GARTLEY113, anti_gartley113, 'Anti Gartley 113')
    fillPatternArrays(ANTI_BUTTERFLY113, anti_butterfly113, 'Anti Butterfly 113')
    return INIT_SUCCEEDED

def fillPatternArrays(index, descriptor, name):
    _assign(_patterns[index], descriptor)
    _patternNames[index] = name

def ShouldDisplay(patternIndex):
    if patternIndex == TRENDLIKE1_ABCD and ((not i_show_trendlike1_abcd) or (not i_show_abcd)):
        return False
    if patternIndex == TRENDLIKE2_ABCD and ((not i_show_trendlike2_abcd) or (not i_show_abcd)):
        return False
    if patternIndex == PERFECT_ABCD and ((not i_show_perfect_abcd) or (not i_show_abcd)):
        return False
    if patternIndex == IDEAL1_ABCD and ((not i_show_ideal1_abcd) or (not i_show_abcd)):
        return False
    if patternIndex == IDEAL2_ABCD and ((not i_show_ideal2_abcd) or (not i_show_abcd)):
        return False
    if patternIndex == RANGELIKE_ABCD and ((not i_show_rangelike_abcd) or (not i_show_abcd)):
        return False
    if patternIndex == ALT127_TRENDLIKE1_ABCD and ((not i_show_alt127_trendlike1_abcd) or (not i_show_alt127_abcd)):
        return False
    if patternIndex == ALT127_TRENDLIKE2_ABCD and ((not i_show_alt127_trendlike2_abcd) or (not i_show_alt127_abcd)):
        return False
    if patternIndex == ALT127_PERFECT_ABCD and ((not i_show_alt127_perfect_abcd) or (not i_show_alt127_abcd)):
        return False
    if patternIndex == ALT127_IDEAL1_ABCD and ((not i_show_alt127_ideal1_abcd) or (not i_show_alt127_abcd)):
        return False
    if patternIndex == ALT127_IDEAL2_ABCD and ((not i_show_alt127_ideal2_abcd) or (not i_show_alt127_abcd)):
        return False
    if patternIndex == ALT127_RANGELIKE_ABCD and ((not i_show_alt127_rangelike_abcd) or (not i_show_alt127_abcd)):
        return False
    if patternIndex == ALT161_TRENDLIKE1_ABCD and ((not i_show_alt161_trendlike1_abcd) or (not i_show_alt161_abcd)):
        return False
    if patternIndex == ALT161_TRENDLIKE2_ABCD and ((not i_show_alt161_trendlike2_abcd) or (not i_show_alt161_abcd)):
        return False
    if patternIndex == ALT161_PERFECT_ABCD and ((not i_show_alt161_perfect_abcd) or (not i_show_alt161_abcd)):
        return False
    if patternIndex == ALT161_IDEAL1_ABCD and ((not i_show_alt161_ideal1_abcd) or (not i_show_alt161_abcd)):
        return False
    if patternIndex == ALT161_IDEAL2_ABCD and ((not i_show_alt161_ideal2_abcd) or (not i_show_alt161_abcd)):
        return False
    if patternIndex == ALT161_RANGELIKE_ABCD and ((not i_show_alt161_rangelike_abcd) or (not i_show_alt161_abcd)):
        return False
    if patternIndex == REC_TRENDLIKE1_ABCD and ((not i_show_rec_trendlike1_abcd) or (not i_show_rec_abcd)):
        return False
    if patternIndex == REC_TRENDLIKE2_ABCD and ((not i_show_rec_trendlike2_abcd) or (not i_show_rec_abcd)):
        return False
    if patternIndex == REC_PERFECT_ABCD and ((not i_show_rec_perfect_abcd) or (not i_show_rec_abcd)):
        return False
    if patternIndex == REC_IDEAL1_ABCD and ((not i_show_rec_ideal1_abcd) or (not i_show_rec_abcd)):
        return False
    if patternIndex == REC_IDEAL2_ABCD and ((not i_show_rec_ideal2_abcd) or (not i_show_rec_abcd)):
        return False
    if patternIndex == REC_RANGELIKE_ABCD and ((not i_show_rec_rangelike_abcd) or (not i_show_rec_abcd)):
        return False
    if patternIndex == ALT127_REC_TRENDLIKE1_ABCD and ((not i_show_alt127_rec_trendlike1_abcd) or (not i_show_alt127_rec_abcd)):
        return False
    if patternIndex == ALT127_REC_TRENDLIKE2_ABCD and ((not i_show_alt127_rec_trendlike2_abcd) or (not i_show_alt127_rec_abcd)):
        return False
    if patternIndex == ALT127_REC_PERFECT_ABCD and ((not i_show_alt127_rec_perfect_abcd) or (not i_show_alt127_rec_abcd)):
        return False
    if patternIndex == ALT127_REC_IDEAL1_ABCD and ((not i_show_alt127_rec_ideal1_abcd) or (not i_show_alt127_rec_abcd)):
        return False
    if patternIndex == ALT127_REC_IDEAL2_ABCD and ((not i_show_alt127_rec_ideal2_abcd) or (not i_show_alt127_rec_abcd)):
        return False
    if patternIndex == ALT127_REC_RANGELIKE_ABCD and ((not i_show_alt127_rec_rangelike_abcd) or (not i_show_alt127_rec_abcd)):
        return False
    if patternIndex == ALT161_REC_TRENDLIKE1_ABCD and ((not i_show_alt161_rec_trendlike1_abcd) or (not i_show_alt161_rec_abcd)):
        return False
    if patternIndex == ALT161_REC_TRENDLIKE2_ABCD and ((not i_show_alt161_rec_trendlike2_abcd) or (not i_show_alt161_rec_abcd)):
        return False
    if patternIndex == ALT161_REC_PERFECT_ABCD and ((not i_show_alt161_rec_perfect_abcd) or (not i_show_alt161_rec_abcd)):
        return False
    if patternIndex == ALT161_REC_IDEAL1_ABCD and ((not i_show_alt161_rec_ideal1_abcd) or (not i_show_alt161_rec_abcd)):
        return False
    if patternIndex == ALT161_REC_IDEAL2_ABCD and ((not i_show_alt161_rec_ideal2_abcd) or (not i_show_alt161_rec_abcd)):
        return False
    if patternIndex == ALT161_REC_RANGELIKE_ABCD and ((not i_show_alt161_rec_rangelike_abcd) or (not i_show_alt161_rec_abcd)):
        return False
    if patternIndex == GARTLEY and ((not i_show_gartley) or (not i_show_patterns)):
        return False
    if patternIndex == PERFECT_GARTLEY and ((not i_show_perfect_gartley) or (not i_show_patterns)):
        return False
    if patternIndex == GARTLEY113 and ((not i_show_gartley113) or (not i_show_patterns)):
        return False
    if patternIndex == MAXGARTLEY and ((not i_show_maxgartley) or (not i_show_patterns)):
        return False
    if patternIndex == BAT and ((not i_show_bat) or (not i_show_patterns)):
        return False
    if patternIndex == ALTBAT and ((not i_show_altbat) or (not i_show_patterns)):
        return False
    if patternIndex == PERFECT_BAT and ((not i_show_perfect_bat) or (not i_show_patterns)):
        return False
    if patternIndex == MAXBAT and ((not i_show_maxbat) or (not i_show_patterns)):
        return False
    if patternIndex == CRAB and ((not i_show_crab) or (not i_show_patterns)):
        return False
    if patternIndex == PERFECT_CRAB and ((not i_show_perfect_crab) or (not i_show_patterns)):
        return False
    if patternIndex == DEEPCRAB and ((not i_show_deepcrab) or (not i_show_patterns)):
        return False
    if patternIndex == BUTTERFLY and ((not i_show_butterfly) or (not i_show_patterns)):
        return False
    if patternIndex == PERFECT_BUTTERFLY and ((not i_show_perfect_butterfly) or (not i_show_patterns)):
        return False
    if patternIndex == MAXBUTTERFLY and ((not i_show_maxbutterfly) or (not i_show_patterns)):
        return False
    if patternIndex == BUTTERFLY113 and ((not i_show_butterfly113) or (not i_show_patterns)):
        return False
    if patternIndex == FIVEO and ((not i_show_fiveo) or (not i_show_patterns)):
        return False
    if patternIndex == THREEDRIVES and ((not i_show_threedrives) or (not i_show_patterns)):
        return False
    if patternIndex == CYPHER and ((not i_show_cypher) or (not i_show_patterns)):
        return False
    if patternIndex == SHARK and ((not i_show_shark) or (not i_show_patterns)):
        return False
    if patternIndex == NENSTAR and ((not i_show_nenstar) or (not i_show_patterns)):
        return False
    if patternIndex == BLACKSWAN and ((not i_show_blackswan) or (not i_show_patterns)):
        return False
    if patternIndex == WHITESWAN and ((not i_show_whiteswan) or (not i_show_patterns)):
        return False
    if patternIndex == ONE2ONE and ((not i_show_one2one) or (not i_show_patterns)):
        return False
    if patternIndex == NEWCYPHER and ((not i_show_newCypher) or (not i_show_patterns)):
        return False
    if patternIndex == NAVARRO200 and ((not i_show_navarro200) or (not i_show_patterns)):
        return False
    if patternIndex == LEONARDO and ((not i_show_leonardo) or (not i_show_patterns)):
        return False
    if patternIndex == KANE and ((not i_show_kane) or (not i_show_patterns)):
        return False
    if patternIndex == GARFLY and ((not i_show_garfly) or (not i_show_patterns)):
        return False
    if patternIndex == ANTI_GARTLEY and ((not i_show_antigartley) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_BAT and ((not i_show_antibat) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_ALTBAT and ((not i_show_antialtbat) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_FIVEO and ((not i_show_antifiveo) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_BUTTERFLY and ((not i_show_antibutterfly) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_CRAB and ((not i_show_anticrab) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_DEEPCRAB and ((not i_show_antideepcrab) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_THREEDRIVES and ((not i_show_antithreedrives) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_CYPHER and ((not i_show_anticypher) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_SHARK and ((not i_show_antishark) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_NENSTAR and ((not i_show_antinenstar) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_BLACKSWAN and ((not i_show_antiblackswan) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_WHITESWAN and ((not i_show_antiwhiteswan) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_ONE2ONE and ((not i_show_antione2one) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_NEWCYPHER and ((not i_show_antinewCypher) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_NAVARRO200 and ((not i_show_antinavarro200) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_LEONARDO and ((not i_show_antileonardo) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_KANE and ((not i_show_antikane) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_GARFLY and ((not i_show_antigarfly) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_MAXBAT and ((not i_show_antimaxbat) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_MAXGARTLEY and ((not i_show_antimaxgartley) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_MAXBUTTERFLY and ((not i_show_antimaxbutterfly) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_GARTLEY113 and ((not i_show_antigartley113) or (not i_show_antipatterns)):
        return False
    if patternIndex == ANTI_BUTTERFLY113 and ((not i_show_antibutterfly113) or (not i_show_antipatterns)):
        return False
    return True

def Invert(original):
    ret = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    if original.ab2xa_max != 0:
        ret.cd2bc_min = _fdiv(1.0, original.ab2xa_max)
    if original.ab2xa_min != 0:
        ret.cd2bc_max = _fdiv(1.0, original.ab2xa_min)
    if original.bc2ab_max != 0:
        ret.bc2ab_min = _fdiv(1.0, original.bc2ab_max)
    if original.bc2ab_min != 0:
        ret.bc2ab_max = _fdiv(1.0, original.bc2ab_min)
    if original.cd2bc_max != 0:
        ret.ab2xa_min = _fdiv(1.0, original.cd2bc_max)
    if original.cd2bc_min != 0:
        ret.ab2xa_max = _fdiv(1.0, original.cd2bc_min)
    if original.ad2xa_max != 0:
        ret.cd2xc_min = _fdiv(1.0, original.ad2xa_max)
    if original.ad2xa_min != 0:
        ret.cd2xc_max = _fdiv(1.0, original.ad2xa_min)
    if original.cd2xc_max != 0:
        ret.ad2xa_min = _fdiv(1.0, original.cd2xc_max)
    if original.cd2xc_min != 0:
        ret.ad2xa_max = _fdiv(1.0, original.cd2xc_min)
    if original.xc2xa_max != 0:
        ret.cd2ad_min = _fdiv(1.0, original.xc2xa_max)
    if original.xc2xa_min != 0:
        ret.cd2ad_max = _fdiv(1.0, original.xc2xa_min)
    if original.cd2ab_max != 0:
        ret.bc2xa_min = _fdiv(1.0, original.cd2ab_max)
    if original.cd2ab_min != 0:
        ret.bc2xa_max = _fdiv(1.0, original.cd2ab_min)
    return _copy(ret)

# ---- global variables initialised from expressions
_indicator = _alloc(CHPFIndicator)
_indicator.__init__(88, 36, i_barsAnalyzed * 2)
_statistics = _alloc(CHPFStatisticsObserver)
_statistics.__init__(88)
_observers = _alloc(CHPFObserverList)
_observers.__init__(3)
_timeFilter = _alloc(CHPFTimeFilter)
_timeFilter.__init__(36, i_tooEarly, i_tooLate)
_filters = _alloc(CHPFFilterList)
_filters.__init__(2)
_patterns = Arr(0, 0, factory=PATTERN_DESCRIPTOR)
_deltaDT = ((PeriodSeconds() * 180) if (Period() < 60) else (PeriodSeconds() * 180))
_drawer = _alloc(CHPFDrawingObserver)
_drawer.__init__()
_commentator = _alloc(CHPFCommentObserver)
_commentator.__init__(88, i_barsAnalyzed * 2, showPatternNames)
_purityFilter = _alloc(CHPFPurityFilter)
_purityFilter.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HarmonicPatternFinderV3(_MQL5Indicator):
    name = 'HarmonicPatternFinderV3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_zzAtrMultiplier': 2.0,  # ATR ZZ atr multiplier
        'i_zzAtrPeriod': 50,  # ATR ZZ atr period
        'i_zzMaxPeriod': 10,  # ATR ZZ max period
        'i_zzMinPeriod': 3,  # ATR ZZ min period
        'i_zzRealtime': True,  # ATR ZZ realtime
        'i_barsAnalyzed': 300,  # Max. bars per pattern
        'i_history': 1000,  # Max. history bars to process
        'i_maxSamePoints': 2,  # Max. shared points per pattern
        'i_slackRange': 0.05,  # Max. slack for fib ratios (range)
        'i_slackSingular': 0.1,  # Max. slack for fib ratios (unary)
        'i_tooEarly': 0.382,  # Too early timezone
        'i_ideal': 1.0,  # Ideal timezone
        'i_tooLate': 1.618,  # Too late timezone
        'i_puristPRZ': False,  # Filter patterns without fib ratios in PRZ
        'i_timefilterEarly': False,  # Filter too early patterns
        'i_timefilterLate': False,  # Filter too late patterns
        'i_fillPatterns': False,  # Fill 5 point patterns found
        'i_showDescriptions': True,  # Show pattern descriptions
        'i_emergingPatterns': True,  # Show emerging patterns
        'i_oldPatterns': True,  # Show past patterns
        'i_oneAheadProjection': False,  # Show "one-ahead" projections
        'i_showSoftProjections': True,  # Draw projections bodies in soft color
        'showPatternNames': True,  # Show comment box
        'i_lineWidth': 2,  # Pattern line width
        'i_lineWidthProj': 1,  # Emerging patterns line width
        'i_lineWidthFoc': 3,  # Focused patterns line width
        'i_fontSize': 8,  # Font size
        'i_style5P': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Style for 5 points patterns
        'i_style4P': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # Style for 4 points patterns
        'i_styleProj': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Style for projections
        'i_styleRatio': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Style for ratio lines
        'i_stylePRZ': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=3),  # Style for PRZ
        'i_show_abcd': True,  # Display AB=CD patterns
        'i_show_alt127_abcd': False,  # Display 1.27 AB=CD patterns
        'i_show_alt161_abcd': False,  # Display 1.61 AB=CD patterns
        'i_show_rec_abcd': False,  # Display Rec. AB=CD patterns
        'i_show_alt127_rec_abcd': False,  # Display Rec. 1.27 AB=CD patterns
        'i_show_alt161_rec_abcd': False,  # Display Rec. 1.61 AB=CD patterns
        'i_show_patterns': True,  # Display normal 5-point patterns
        'i_show_antipatterns': False,  # Display anti 5-point patterns
        'i_show_trendlike1_abcd': True,  # Display Trendlike AB=CD #1
        'i_show_trendlike2_abcd': True,  # Display Trendlike AB=CD #2
        'i_show_perfect_abcd': True,  # Display Perfect AB=CD
        'i_show_ideal1_abcd': True,  # Display Ideal AB=CD #1
        'i_show_ideal2_abcd': True,  # Display Ideal AB=CD #2
        'i_show_rangelike_abcd': True,  # Display Rangelike AB=CD
        'i_show_alt127_trendlike1_abcd': True,  # Display Trendlike 1.27 AB=CD #1
        'i_show_alt127_trendlike2_abcd': True,  # Display Trendlike 1.27 AB=CD #2
        'i_show_alt127_perfect_abcd': True,  # Display Perfect 1.27 AB=CD
        'i_show_alt127_ideal1_abcd': True,  # Display Ideal 1.27 AB=CD #1
        'i_show_alt127_ideal2_abcd': True,  # Display Ideal 1.27 AB=CD #2
        'i_show_alt127_rangelike_abcd': True,  # Display Rangelike 1.27 AB=CD
        'i_show_alt161_trendlike1_abcd': True,  # Display Trendlike 1.61 AB=CD #1
        'i_show_alt161_trendlike2_abcd': True,  # Display Trendlike 1.61 AB=CD #2
        'i_show_alt161_perfect_abcd': True,  # Display Perfect 1.61 AB=CD
        'i_show_alt161_ideal1_abcd': True,  # Display Ideal 1.61 AB=CD #1
        'i_show_alt161_ideal2_abcd': True,  # Display Ideal 1.61 AB=CD #2
        'i_show_alt161_rangelike_abcd': True,  # Display Rangelike 1.61 AB=CD
        'i_show_rec_trendlike1_abcd': True,  # Display Rec. Trendlike AB=CD #1
        'i_show_rec_trendlike2_abcd': True,  # Display Rec. Trendlike AB=CD #2
        'i_show_rec_perfect_abcd': True,  # Display Rec. Perfect AB=CD
        'i_show_rec_ideal1_abcd': True,  # Display Rec. Ideal AB=CD #1
        'i_show_rec_ideal2_abcd': True,  # Display Rec. Ideal AB=CD #2
        'i_show_rec_rangelike_abcd': True,  # Display Rec. Rangelike AB=CD
        'i_show_alt127_rec_trendlike1_abcd': True,  # Display Rec. Trendlike 1.27 AB=CD #1
        'i_show_alt127_rec_trendlike2_abcd': True,  # Display Rec. Trendlike 1.27 AB=CD #2
        'i_show_alt127_rec_perfect_abcd': True,  # Display Rec. Perfect 1.27 AB=CD
        'i_show_alt127_rec_ideal1_abcd': True,  # Display Rec. Ideal 1.27 AB=CD #1
        'i_show_alt127_rec_ideal2_abcd': True,  # Display Rec. Ideal 1.27 AB=CD #2
        'i_show_alt127_rec_rangelike_abcd': True,  # Display Rec. Rangelike 1.27 AB=CD
        'i_show_alt161_rec_trendlike1_abcd': True,  # Display Rec. Trendlike 1.61 AB=CD #1
        'i_show_alt161_rec_trendlike2_abcd': True,  # Display Rec. Trendlike 1.61 AB=CD #2
        'i_show_alt161_rec_perfect_abcd': True,  # Display Rec. Perfect 1.61 AB=CD
        'i_show_alt161_rec_ideal1_abcd': True,  # Display Rec. Ideal 1.61 AB=CD #1
        'i_show_alt161_rec_ideal2_abcd': True,  # Display Rec. Ideal 1.61 AB=CD #2
        'i_show_alt161_rec_rangelike_abcd': True,  # Display Rec. Rangelike 1.61 AB=CD
        'i_show_gartley': True,  # Display Gartley
        'i_show_perfect_gartley': True,  # Display Perfect Gartley
        'i_show_gartley113': True,  # Display Gartley 113
        'i_show_maxgartley': True,  # Display Max. Gartley
        'i_show_bat': True,  # Display Bat
        'i_show_perfect_bat': True,  # Display Perfect Bat
        'i_show_altbat': True,  # Display Alt. Bat
        'i_show_maxbat': True,  # Display Max. Bat
        'i_show_crab': True,  # Display Crab
        'i_show_perfect_crab': True,  # Display Perfect Crab
        'i_show_deepcrab': True,  # Display Deepcrab
        'i_show_butterfly': True,  # Display Butterfly
        'i_show_perfect_butterfly': True,  # Display Perfect Butterfly
        'i_show_maxbutterfly': True,  # Display Max. Butterfly
        'i_show_butterfly113': True,  # Display Butterfly 113
        'i_show_fiveo': True,  # Display 5-0
        'i_show_threedrives': True,  # Display Three Drives
        'i_show_cypher': True,  # Display Cypher
        'i_show_shark': True,  # Display Shark
        'i_show_nenstar': True,  # Display Nen Star
        'i_show_blackswan': True,  # Display Black Swan
        'i_show_whiteswan': True,  # Display White Swan
        'i_show_one2one': False,  # Display One2One
        'i_show_newCypher': True,  # Display New Cypher
        'i_show_navarro200': False,  # Display Navarro 200
        'i_show_leonardo': True,  # Display Leonardo
        'i_show_kane': True,  # Display Kane
        'i_show_garfly': True,  # Display Garfly
        'i_show_antigartley': True,  # Display Anti Gartley
        'i_show_antibat': True,  # Display Anti Bat
        'i_show_antialtbat': True,  # Display Anti Alt. Bat
        'i_show_antifiveo': True,  # Display Anti 5-0
        'i_show_antibutterfly': True,  # Display Anti Butterfly
        'i_show_anticrab': True,  # Display Anti Crab
        'i_show_antideepcrab': True,  # Display Anti Deepcrab
        'i_show_antithreedrives': True,  # Display Anti Three Drives
        'i_show_anticypher': True,  # Display Anti Cypher
        'i_show_antishark': True,  # Display Anti Shark
        'i_show_antinenstar': True,  # Display Anti Nen Star
        'i_show_antiblackswan': True,  # Display Anti Black Swan
        'i_show_antiwhiteswan': True,  # Display Anti White Swan
        'i_show_antione2one': True,  # Display Anti One2One
        'i_show_antinewCypher': True,  # Display Anti New Cypher
        'i_show_antinavarro200': True,  # Display Anti Navarro 200
        'i_show_antileonardo': True,  # Display Anti Leonardo
        'i_show_antikane': True,  # Display Anti Kane
        'i_show_antigarfly': True,  # Display Anti Garfly
        'i_show_antimaxbat': True,  # Display Anti Max. Bat
        'i_show_antimaxgartley': True,  # Display Anti Max. Gartley
        'i_show_antimaxbutterfly': True,  # Display Anti Max. Butterfly
        'i_show_antigartley113': True,  # Display Anti Gartley 113
        'i_show_antibutterfly113': True,  # Display Anti Butterfly 113
    }

