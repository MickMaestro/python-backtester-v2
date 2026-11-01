"""HarmonicPatternFinderV2 — converted from MQL5: MQL5 Indicators/Harmonic Pattern Finder V2/HarmonicPatternFinderV2.mq5

Indicator to display existent and emerging harmonic chart patterns.
Copyright: Copyright 2016, Andre S. Enger.; Link: andre_enger@hotmail.com; Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Andre S. Enger.', 'link': 'andre_enger@hotmail.com', 'version': '2.0', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [4294967295]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Zig Zag'}, 'levels': [], 'description': ['Indicator to display existent and emerging harmonic chart patterns.'], 'name': 'HarmonicPatternFinderV2', 'source': 'MQL5 Indicators/Harmonic Pattern Finder V2/HarmonicPatternFinderV2.mq5', 'folder': 'Harmonic Pattern Finder V2', 'inputs': [{'mql': 'indicatorSettings', 'py': 'indicatorSettings', 'param': None, 'type': 'string', 'default': '-=Indicator Settings=-', 'label': '-=Indicator Settings=-', 'sinput': False}, {'mql': 'zztype', 'py': 'zztype', 'param': 'zztype', 'type': 'int', 'default': 1, 'label': 'ZigZag type', 'sinput': False}, {'mql': 'zzperiod', 'py': 'zzperiod', 'param': 'zzperiod', 'type': 'int', 'default': 12, 'label': 'AlexStal ZZ period', 'sinput': False}, {'mql': 'zzamplitude', 'py': 'zzamplitude', 'param': 'zzamplitude', 'type': 'int', 'default': 10, 'label': 'AlexStal ZZ amplitude', 'sinput': False}, {'mql': 'zzminmotion', 'py': 'zzminmotion', 'param': 'zzminmotion', 'type': 'int', 'default': 0, 'label': 'AlexStal ZZ minimum motion', 'sinput': False}, {'mql': 'SwingSize', 'py': 'SwingSize', 'param': 'SwingSize', 'type': 'int', 'default': 200, 'label': 'Fast ZZ sensitivity in points', 'sinput': False}, {'mql': 'BarsAnalyzed', 'py': 'BarsAnalyzed', 'param': 'BarsAnalyzed', 'type': 'int', 'default': 200, 'label': 'Max. bars per pattern', 'sinput': False}, {'mql': 'History', 'py': 'History', 'param': 'History', 'type': 'int', 'default': 1000, 'label': 'Max. history bars to process', 'sinput': False}, {'mql': 'MaxSamePoints', 'py': 'MaxSamePoints', 'param': 'MaxSamePoints', 'type': 'int', 'default': 2, 'label': 'Max. shared points per pattern', 'sinput': False}, {'mql': 'SlackRange', 'py': 'SlackRange', 'param': 'SlackRange', 'type': 'double', 'default': 0.01, 'label': 'Max. slack for fib ratios (range)', 'sinput': False}, {'mql': 'SlackUnary', 'py': 'SlackUnary', 'param': 'SlackUnary', 'type': 'double', 'default': 0.1, 'label': 'Max. slack for fib ratios (unary)', 'sinput': False}, {'mql': 'indicatorColors', 'py': 'indicatorColors', 'param': None, 'type': 'string', 'default': '-=Display Settings=-', 'label': '-=Display Settings=-', 'sinput': False}, {'mql': 'ClrBull', 'py': 'ClrBull', 'param': None, 'type': 'color', 'default': 16436871, 'label': 'Color for bullish patterns (5 points)', 'sinput': False}, {'mql': 'ClrBear', 'py': 'ClrBear', 'param': None, 'type': 'color', 'default': 7504122, 'label': 'Color for bearish patterns (5 points)', 'sinput': False}, {'mql': 'ClrBull4P', 'py': 'ClrBull4P', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color for bullish patterns (4 points)', 'sinput': False}, {'mql': 'ClrBear4P', 'py': 'ClrBear4P', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color for bearish patterns (4 points)', 'sinput': False}, {'mql': 'ClrBullProjection', 'py': 'ClrBullProjection', 'param': None, 'type': 'color', 'default': 5737262, 'label': 'Color for projected bullish patterns', 'sinput': False}, {'mql': 'ClrBearProjection', 'py': 'ClrBearProjection', 'param': None, 'type': 'color', 'default': 36095, 'label': 'Color for projected bearish patterns', 'sinput': False}, {'mql': 'ClrRatio', 'py': 'ClrRatio', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Color for patterns ratios', 'sinput': False}, {'mql': 'Fill_Patterns', 'py': 'Fill_Patterns', 'param': 'Fill_Patterns', 'type': 'bool', 'default': False, 'label': 'Fill 5 point patterns found', 'sinput': False}, {'mql': 'Show_descriptions', 'py': 'Show_descriptions', 'param': 'Show_descriptions', 'type': 'bool', 'default': True, 'label': 'Show pattern descriptions', 'sinput': False}, {'mql': 'Show_PRZ', 'py': 'Show_PRZ', 'param': 'Show_PRZ', 'type': 'bool', 'default': True, 'label': 'Show potential reversal zone (PRZ)', 'sinput': False}, {'mql': 'EmergingPatterns', 'py': 'EmergingPatterns', 'param': 'EmergingPatterns', 'type': 'bool', 'default': True, 'label': 'Show emerging patterns', 'sinput': False}, {'mql': 'OneAheadProjection', 'py': 'OneAheadProjection', 'param': 'OneAheadProjection', 'type': 'bool', 'default': False, 'label': 'Show "one-ahead" projections', 'sinput': False}, {'mql': 'showPatternNames', 'py': 'showPatternNames', 'param': 'showPatternNames', 'type': 'bool', 'default': False, 'label': 'Show comment box', 'sinput': False}, {'mql': 'l_width', 'py': 'l_width', 'param': 'l_width', 'type': 'int', 'default': 2, 'label': 'Pattern line width (5 points)', 'sinput': False}, {'mql': 'l_width4p', 'py': 'l_width4p', 'param': 'l_width4p', 'type': 'int', 'default': 2, 'label': 'Patterns line width (4 points)', 'sinput': False}, {'mql': 'l_width_proj', 'py': 'l_width_proj', 'param': 'l_width_proj', 'type': 'int', 'default': 2, 'label': 'Emerging patterns line width', 'sinput': False}, {'mql': 'Font_size', 'py': 'Font_size', 'param': 'Font_size', 'type': 'int', 'default': 8, 'label': 'Font size', 'sinput': False}, {'mql': 'Style_5P', 'py': 'Style_5P', 'param': 'Style_5P', 'type': 'int', 'default': 0, 'label': 'Style for 5 points patterns', 'sinput': False}, {'mql': 'Style_4P', 'py': 'Style_4P', 'param': 'Style_4P', 'type': 'int', 'default': 1, 'label': 'Style for 4 points patterns', 'sinput': False}, {'mql': 'Style_Proj', 'py': 'Style_Proj', 'param': 'Style_Proj', 'type': 'int', 'default': 4, 'label': 'Style for projections', 'sinput': False}, {'mql': 'Style_Ratio', 'py': 'Style_Ratio', 'param': 'Style_Ratio', 'type': 'int', 'default': 2, 'label': 'Style for ratio lines', 'sinput': False}, {'mql': 'Style_PRZ', 'py': 'Style_PRZ', 'param': 'Style_PRZ', 'type': 'int', 'default': 3, 'label': 'Style for PRZ', 'sinput': False}, {'mql': 'indicatorPatternsQuick', 'py': 'indicatorPatternsQuick', 'param': None, 'type': 'string', 'default': '-=Patterns Quick=-', 'label': '-=Patterns Quick=-', 'sinput': False}, {'mql': 'Show_abcd', 'py': 'Show_abcd', 'param': 'Show_abcd', 'type': 'bool', 'default': True, 'label': 'Display AB=CD patterns', 'sinput': False}, {'mql': 'Show_alt127_abcd', 'py': 'Show_alt127_abcd', 'param': 'Show_alt127_abcd', 'type': 'bool', 'default': True, 'label': 'Display 1.27 AB=CD patterns', 'sinput': False}, {'mql': 'Show_rec_abcd', 'py': 'Show_rec_abcd', 'param': 'Show_rec_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. AB=CD patterns', 'sinput': False}, {'mql': 'Show_patterns', 'py': 'Show_patterns', 'param': 'Show_patterns', 'type': 'bool', 'default': True, 'label': 'Display normal 5-point patterns', 'sinput': False}, {'mql': 'Show_antipatterns', 'py': 'Show_antipatterns', 'param': 'Show_antipatterns', 'type': 'bool', 'default': False, 'label': 'Display anti 5-point patterns', 'sinput': False}, {'mql': 'indicatorPatternsIndividual', 'py': 'indicatorPatternsIndividual', 'param': None, 'type': 'string', 'default': '-=Patterns Individual=-', 'label': '-=Patterns Individual=-', 'sinput': False}, {'mql': 'Show_trendlike1_abcd', 'py': 'Show_trendlike1_abcd', 'param': 'Show_trendlike1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike AB=CD #1', 'sinput': False}, {'mql': 'Show_trendlike2_abcd', 'py': 'Show_trendlike2_abcd', 'param': 'Show_trendlike2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike AB=CD #2', 'sinput': False}, {'mql': 'Show_perfect_abcd', 'py': 'Show_perfect_abcd', 'param': 'Show_perfect_abcd', 'type': 'bool', 'default': True, 'label': 'Display Perfect AB=CD', 'sinput': False}, {'mql': 'Show_ideal1_abcd', 'py': 'Show_ideal1_abcd', 'param': 'Show_ideal1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal AB=CD #1', 'sinput': False}, {'mql': 'Show_ideal2_abcd', 'py': 'Show_ideal2_abcd', 'param': 'Show_ideal2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal AB=CD #2', 'sinput': False}, {'mql': 'Show_rangelike_abcd', 'py': 'Show_rangelike_abcd', 'param': 'Show_rangelike_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rangelike AB=CD', 'sinput': False}, {'mql': 'Show_alt127_trendlike1_abcd', 'py': 'Show_alt127_trendlike1_abcd', 'param': 'Show_alt127_trendlike1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike 1.27 AB=CD #1', 'sinput': False}, {'mql': 'Show_alt127_trendlike2_abcd', 'py': 'Show_alt127_trendlike2_abcd', 'param': 'Show_alt127_trendlike2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Trendlike 1.27 AB=CD #2', 'sinput': False}, {'mql': 'Show_alt127_perfect_abcd', 'py': 'Show_alt127_perfect_abcd', 'param': 'Show_alt127_perfect_abcd', 'type': 'bool', 'default': True, 'label': 'Display Perfect 1.27 AB=CD', 'sinput': False}, {'mql': 'Show_alt127_ideal1_abcd', 'py': 'Show_alt127_ideal1_abcd', 'param': 'Show_alt127_ideal1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal 1.27 AB=CD #1', 'sinput': False}, {'mql': 'Show_alt127_ideal2_abcd', 'py': 'Show_alt127_ideal2_abcd', 'param': 'Show_alt127_ideal2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Ideal 1.27 AB=CD #2', 'sinput': False}, {'mql': 'Show_alt127_rangelike_abcd', 'py': 'Show_alt127_rangelike_abcd', 'param': 'Show_alt127_rangelike_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rangelike 1.27 AB=CD', 'sinput': False}, {'mql': 'Show_rec_trendlike1_abcd', 'py': 'Show_rec_trendlike1_abcd', 'param': 'Show_rec_trendlike1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Trendlike AB=CD #1', 'sinput': False}, {'mql': 'Show_rec_trendlike2_abcd', 'py': 'Show_rec_trendlike2_abcd', 'param': 'Show_rec_trendlike2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Trendlike AB=CD #2', 'sinput': False}, {'mql': 'Show_rec_perfect_abcd', 'py': 'Show_rec_perfect_abcd', 'param': 'Show_rec_perfect_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Perfect AB=CD', 'sinput': False}, {'mql': 'Show_rec_ideal1_abcd', 'py': 'Show_rec_ideal1_abcd', 'param': 'Show_rec_ideal1_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Ideal AB=CD #1', 'sinput': False}, {'mql': 'Show_rec_ideal2_abcd', 'py': 'Show_rec_ideal2_abcd', 'param': 'Show_rec_ideal2_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Ideal AB=CD #2', 'sinput': False}, {'mql': 'Show_rec_rangelike_abcd', 'py': 'Show_rec_rangelike_abcd', 'param': 'Show_rec_rangelike_abcd', 'type': 'bool', 'default': True, 'label': 'Display Rec. Rangelike AB=CD', 'sinput': False}, {'mql': 'Show_gartley', 'py': 'Show_gartley', 'param': 'Show_gartley', 'type': 'bool', 'default': True, 'label': 'Display Gartley', 'sinput': False}, {'mql': 'Show_bat', 'py': 'Show_bat', 'param': 'Show_bat', 'type': 'bool', 'default': True, 'label': 'Display Bat', 'sinput': False}, {'mql': 'Show_altbat', 'py': 'Show_altbat', 'param': 'Show_altbat', 'type': 'bool', 'default': True, 'label': 'Display Alt. Bat', 'sinput': False}, {'mql': 'Show_fiveo', 'py': 'Show_fiveo', 'param': 'Show_fiveo', 'type': 'bool', 'default': True, 'label': 'Display 5-0', 'sinput': False}, {'mql': 'Show_butterfly', 'py': 'Show_butterfly', 'param': 'Show_butterfly', 'type': 'bool', 'default': True, 'label': 'Display Butterfly', 'sinput': False}, {'mql': 'Show_crab', 'py': 'Show_crab', 'param': 'Show_crab', 'type': 'bool', 'default': True, 'label': 'Display Crab', 'sinput': False}, {'mql': 'Show_deepcrab', 'py': 'Show_deepcrab', 'param': 'Show_deepcrab', 'type': 'bool', 'default': True, 'label': 'Display Deepcrab', 'sinput': False}, {'mql': 'Show_threedrives', 'py': 'Show_threedrives', 'param': 'Show_threedrives', 'type': 'bool', 'default': True, 'label': 'Display Three Drives', 'sinput': False}, {'mql': 'Show_cypher', 'py': 'Show_cypher', 'param': 'Show_cypher', 'type': 'bool', 'default': True, 'label': 'Display Cypher', 'sinput': False}, {'mql': 'Show_shark', 'py': 'Show_shark', 'param': 'Show_shark', 'type': 'bool', 'default': True, 'label': 'Display Shark', 'sinput': False}, {'mql': 'Show_nenstar', 'py': 'Show_nenstar', 'param': 'Show_nenstar', 'type': 'bool', 'default': True, 'label': 'Display Nen Star', 'sinput': False}, {'mql': 'Show_blackswan', 'py': 'Show_blackswan', 'param': 'Show_blackswan', 'type': 'bool', 'default': True, 'label': 'Display Black Swan', 'sinput': False}, {'mql': 'Show_whiteswan', 'py': 'Show_whiteswan', 'param': 'Show_whiteswan', 'type': 'bool', 'default': True, 'label': 'Display White Swan', 'sinput': False}, {'mql': 'Show_one2one', 'py': 'Show_one2one', 'param': 'Show_one2one', 'type': 'bool', 'default': True, 'label': 'Display One2One', 'sinput': False}, {'mql': 'Show_newCypher', 'py': 'Show_newCypher', 'param': 'Show_newCypher', 'type': 'bool', 'default': True, 'label': 'Display New Cypher', 'sinput': False}, {'mql': 'Show_navarro200', 'py': 'Show_navarro200', 'param': 'Show_navarro200', 'type': 'bool', 'default': True, 'label': 'Display Navarro 200', 'sinput': False}, {'mql': 'Show_leonardo', 'py': 'Show_leonardo', 'param': 'Show_leonardo', 'type': 'bool', 'default': True, 'label': 'Display Leonardo', 'sinput': False}, {'mql': 'Show_kane', 'py': 'Show_kane', 'param': 'Show_kane', 'type': 'bool', 'default': True, 'label': 'Display Kane', 'sinput': False}, {'mql': 'Show_garfly', 'py': 'Show_garfly', 'param': 'Show_garfly', 'type': 'bool', 'default': True, 'label': 'Display Garfly', 'sinput': False}, {'mql': 'Show_maxbat', 'py': 'Show_maxbat', 'param': 'Show_maxbat', 'type': 'bool', 'default': True, 'label': 'Display Max. Bat', 'sinput': False}, {'mql': 'Show_maxgartley', 'py': 'Show_maxgartley', 'param': 'Show_maxgartley', 'type': 'bool', 'default': True, 'label': 'Display Max. Gartley', 'sinput': False}, {'mql': 'Show_maxbutterfly', 'py': 'Show_maxbutterfly', 'param': 'Show_maxbutterfly', 'type': 'bool', 'default': True, 'label': 'Display Max. Butterfly', 'sinput': False}, {'mql': 'Show_gartley113', 'py': 'Show_gartley113', 'param': 'Show_gartley113', 'type': 'bool', 'default': True, 'label': 'Display Gartley 113', 'sinput': False}, {'mql': 'Show_butterfly113', 'py': 'Show_butterfly113', 'param': 'Show_butterfly113', 'type': 'bool', 'default': True, 'label': 'Display Butterfly 113', 'sinput': False}, {'mql': 'Show_antigartley', 'py': 'Show_antigartley', 'param': 'Show_antigartley', 'type': 'bool', 'default': True, 'label': 'Display Anti Gartley', 'sinput': False}, {'mql': 'Show_antibat', 'py': 'Show_antibat', 'param': 'Show_antibat', 'type': 'bool', 'default': True, 'label': 'Display Anti Bat', 'sinput': False}, {'mql': 'Show_antialtbat', 'py': 'Show_antialtbat', 'param': 'Show_antialtbat', 'type': 'bool', 'default': True, 'label': 'Display Anti Alt. Bat', 'sinput': False}, {'mql': 'Show_antifiveo', 'py': 'Show_antifiveo', 'param': 'Show_antifiveo', 'type': 'bool', 'default': True, 'label': 'Display Anti 5-0', 'sinput': False}, {'mql': 'Show_antibutterfly', 'py': 'Show_antibutterfly', 'param': 'Show_antibutterfly', 'type': 'bool', 'default': True, 'label': 'Display Anti Butterfly', 'sinput': False}, {'mql': 'Show_anticrab', 'py': 'Show_anticrab', 'param': 'Show_anticrab', 'type': 'bool', 'default': True, 'label': 'Display Anti Crab', 'sinput': False}, {'mql': 'Show_antideepcrab', 'py': 'Show_antideepcrab', 'param': 'Show_antideepcrab', 'type': 'bool', 'default': True, 'label': 'Display Anti Deepcrab', 'sinput': False}, {'mql': 'Show_antithreedrives', 'py': 'Show_antithreedrives', 'param': 'Show_antithreedrives', 'type': 'bool', 'default': True, 'label': 'Display Anti Three Drives', 'sinput': False}, {'mql': 'Show_anticypher', 'py': 'Show_anticypher', 'param': 'Show_anticypher', 'type': 'bool', 'default': True, 'label': 'Display Anti Cypher', 'sinput': False}, {'mql': 'Show_antishark', 'py': 'Show_antishark', 'param': 'Show_antishark', 'type': 'bool', 'default': True, 'label': 'Display Anti Shark', 'sinput': False}, {'mql': 'Show_antinenstar', 'py': 'Show_antinenstar', 'param': 'Show_antinenstar', 'type': 'bool', 'default': True, 'label': 'Display Anti Nen Star', 'sinput': False}, {'mql': 'Show_antiblackswan', 'py': 'Show_antiblackswan', 'param': 'Show_antiblackswan', 'type': 'bool', 'default': True, 'label': 'Display Anti Black Swan', 'sinput': False}, {'mql': 'Show_antiwhiteswan', 'py': 'Show_antiwhiteswan', 'param': 'Show_antiwhiteswan', 'type': 'bool', 'default': True, 'label': 'Display Anti White Swan', 'sinput': False}, {'mql': 'Show_antione2one', 'py': 'Show_antione2one', 'param': 'Show_antione2one', 'type': 'bool', 'default': True, 'label': 'Display Anti One2One', 'sinput': False}, {'mql': 'Show_antinewCypher', 'py': 'Show_antinewCypher', 'param': 'Show_antinewCypher', 'type': 'bool', 'default': True, 'label': 'Display Anti New Cypher', 'sinput': False}, {'mql': 'Show_antinavarro200', 'py': 'Show_antinavarro200', 'param': 'Show_antinavarro200', 'type': 'bool', 'default': True, 'label': 'Display Anti Navarro 200', 'sinput': False}, {'mql': 'Show_antileonardo', 'py': 'Show_antileonardo', 'param': 'Show_antileonardo', 'type': 'bool', 'default': True, 'label': 'Display Anti Leonardo', 'sinput': False}, {'mql': 'Show_antikane', 'py': 'Show_antikane', 'param': 'Show_antikane', 'type': 'bool', 'default': True, 'label': 'Display Anti Kane', 'sinput': False}, {'mql': 'Show_antigarfly', 'py': 'Show_antigarfly', 'param': 'Show_antigarfly', 'type': 'bool', 'default': True, 'label': 'Display Anti Garfly', 'sinput': False}, {'mql': 'Show_antimaxbat', 'py': 'Show_antimaxbat', 'param': 'Show_antimaxbat', 'type': 'bool', 'default': True, 'label': 'Display Anti Max. Bat', 'sinput': False}, {'mql': 'Show_antimaxgartley', 'py': 'Show_antimaxgartley', 'param': 'Show_antimaxgartley', 'type': 'bool', 'default': True, 'label': 'Display Anti Max. Gartley', 'sinput': False}, {'mql': 'Show_antimaxbutterfly', 'py': 'Show_antimaxbutterfly', 'param': 'Show_antimaxbutterfly', 'type': 'bool', 'default': True, 'label': 'Display Anti Max. Butterfly', 'sinput': False}, {'mql': 'Show_antigartley113', 'py': 'Show_antigartley113', 'param': 'Show_antigartley113', 'type': 'bool', 'default': True, 'label': 'Display Anti Gartley 113', 'sinput': False}, {'mql': 'Show_antibutterfly113', 'py': 'Show_antibutterfly113', 'param': 'Show_antibutterfly113', 'type': 'bool', 'default': True, 'label': 'Display Anti Butterfly 113', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
REC_TRENDLIKE1_ABCD = 12
REC_TRENDLIKE2_ABCD = 13
REC_PERFECT_ABCD = 14
REC_IDEAL1_ABCD = 15
REC_IDEAL2_ABCD = 16
REC_RANGELIKE_ABCD = 17
GARTLEY = 18
BAT = 19
ALTBAT = 20
FIVEO = 21
BUTTERFLY = 22
CRAB = 23
DEEPCRAB = 24
THREEDRIVES = 25
CYPHER = 26
SHARK = 27
NENSTAR = 28
BLACKSWAN = 29
WHITESWAN = 30
ONE2ONE = 31
NEWCYPHER = 32
NAVARRO200 = 33
LEONARDO = 34
KANE = 35
GARFLY = 36
MAXBAT = 37
MAXGARTLEY = 38
MAXBUTTERFLY = 39
GARTLEY113 = 40
BUTTERFLY113 = 41
ANTI_GARTLEY = 42
ANTI_BAT = 43
ANTI_ALTBAT = 44
ANTI_FIVEO = 45
ANTI_BUTTERFLY = 46
ANTI_CRAB = 47
ANTI_DEEPCRAB = 48
ANTI_THREEDRIVES = 49
ANTI_CYPHER = 50
ANTI_SHARK = 51
ANTI_NENSTAR = 52
ANTI_BLACKSWAN = 53
ANTI_WHITESWAN = 54
ANTI_ONE2ONE = 55
ANTI_NEWCYPHER = 56
ANTI_NAVARRO200 = 57
ANTI_LEONARDO = 58
ANTI_KANE = 59
ANTI_GARFLY = 60
ANTI_MAXBAT = 61
ANTI_MAXGARTLEY = 62
ANTI_MAXBUTTERFLY = 63
ANTI_GARTLEY113 = 64
ANTI_BUTTERFLY113 = 65
_enum('PATTERN_INDEX', {0: 'TRENDLIKE1_ABCD', 1: 'TRENDLIKE2_ABCD', 2: 'PERFECT_ABCD', 3: 'IDEAL1_ABCD', 4: 'IDEAL2_ABCD', 5: 'RANGELIKE_ABCD', 6: 'ALT127_TRENDLIKE1_ABCD', 7: 'ALT127_TRENDLIKE2_ABCD', 8: 'ALT127_PERFECT_ABCD', 9: 'ALT127_IDEAL1_ABCD', 10: 'ALT127_IDEAL2_ABCD', 11: 'ALT127_RANGELIKE_ABCD', 12: 'REC_TRENDLIKE1_ABCD', 13: 'REC_TRENDLIKE2_ABCD', 14: 'REC_PERFECT_ABCD', 15: 'REC_IDEAL1_ABCD', 16: 'REC_IDEAL2_ABCD', 17: 'REC_RANGELIKE_ABCD', 18: 'GARTLEY', 19: 'BAT', 20: 'ALTBAT', 21: 'FIVEO', 22: 'BUTTERFLY', 23: 'CRAB', 24: 'DEEPCRAB', 25: 'THREEDRIVES', 26: 'CYPHER', 27: 'SHARK', 28: 'NENSTAR', 29: 'BLACKSWAN', 30: 'WHITESWAN', 31: 'ONE2ONE', 32: 'NEWCYPHER', 33: 'NAVARRO200', 34: 'LEONARDO', 35: 'KANE', 36: 'GARFLY', 37: 'MAXBAT', 38: 'MAXGARTLEY', 39: 'MAXBUTTERFLY', 40: 'GARTLEY113', 41: 'BUTTERFLY113', 42: 'ANTI_GARTLEY', 43: 'ANTI_BAT', 44: 'ANTI_ALTBAT', 45: 'ANTI_FIVEO', 46: 'ANTI_BUTTERFLY', 47: 'ANTI_CRAB', 48: 'ANTI_DEEPCRAB', 49: 'ANTI_THREEDRIVES', 50: 'ANTI_CYPHER', 51: 'ANTI_SHARK', 52: 'ANTI_NENSTAR', 53: 'ANTI_BLACKSWAN', 54: 'ANTI_WHITESWAN', 55: 'ANTI_ONE2ONE', 56: 'ANTI_NEWCYPHER', 57: 'ANTI_NAVARRO200', 58: 'ANTI_LEONARDO', 59: 'ANTI_KANE', 60: 'ANTI_GARFLY', 61: 'ANTI_MAXBAT', 62: 'ANTI_MAXGARTLEY', 63: 'ANTI_MAXBUTTERFLY', 64: 'ANTI_GARTLEY113', 65: 'ANTI_BUTTERFLY113'})

# enum ZIGZAGTYPE
FASTZZ = 0
ALEXSTAL = 1
SWINGCHART = 2
_enum('ZIGZAGTYPE', {0: 'FASTZZ', 1: 'ALEXSTAL', 2: 'SWINGCHART'})

# ---- inputs and global variables
_identifier = 'HPF'
indicatorSettings = _input('indicatorSettings', '-=Indicator Settings=-')  # -=Indicator Settings=-
zztype = _input('zztype', ALEXSTAL)  # ZigZag type
zzperiod = _input('zzperiod', 12)  # AlexStal ZZ period
zzamplitude = _input('zzamplitude', 10)  # AlexStal ZZ amplitude
zzminmotion = _input('zzminmotion', 0)  # AlexStal ZZ minimum motion
SwingSize = _input('SwingSize', 200)  # Fast ZZ sensitivity in points
BarsAnalyzed = _input('BarsAnalyzed', 200)  # Max. bars per pattern
History = _input('History', 1000)  # Max. history bars to process
MaxSamePoints = _input('MaxSamePoints', 2)  # Max. shared points per pattern
SlackRange = _input('SlackRange', 0.01)  # Max. slack for fib ratios (range)
SlackUnary = _input('SlackUnary', 0.1)  # Max. slack for fib ratios (unary)
indicatorColors = _input('indicatorColors', '-=Display Settings=-')  # -=Display Settings=-
ClrBull = _input('ClrBull', clrLightSkyBlue)  # Color for bullish patterns (5 points)
ClrBear = _input('ClrBear', clrSalmon)  # Color for bearish patterns (5 points)
ClrBull4P = _input('ClrBull4P', clrBlue)  # Color for bullish patterns (4 points)
ClrBear4P = _input('ClrBear4P', clrRed)  # Color for bearish patterns (4 points)
ClrBullProjection = _input('ClrBullProjection', clrSeaGreen)  # Color for projected bullish patterns
ClrBearProjection = _input('ClrBearProjection', clrDarkOrange)  # Color for projected bearish patterns
ClrRatio = _input('ClrRatio', clrGray)  # Color for patterns ratios
Fill_Patterns = _input('Fill_Patterns', False)  # Fill 5 point patterns found
Show_descriptions = _input('Show_descriptions', True)  # Show pattern descriptions
Show_PRZ = _input('Show_PRZ', True)  # Show potential reversal zone (PRZ)
EmergingPatterns = _input('EmergingPatterns', True)  # Show emerging patterns
OneAheadProjection = _input('OneAheadProjection', False)  # Show "one-ahead" projections
showPatternNames = _input('showPatternNames', False)  # Show comment box
l_width = _input('l_width', 2)  # Pattern line width (5 points)
l_width4p = _input('l_width4p', 2)  # Patterns line width (4 points)
l_width_proj = _input('l_width_proj', 2)  # Emerging patterns line width
Font_size = _input('Font_size', 8)  # Font size
Style_5P = _input('Style_5P', STYLE_SOLID)  # Style for 5 points patterns
Style_4P = _input('Style_4P', STYLE_DASH)  # Style for 4 points patterns
Style_Proj = _input('Style_Proj', STYLE_DASHDOTDOT)  # Style for projections
Style_Ratio = _input('Style_Ratio', STYLE_DOT)  # Style for ratio lines
Style_PRZ = _input('Style_PRZ', STYLE_DASHDOT)  # Style for PRZ
indicatorPatternsQuick = _input('indicatorPatternsQuick', '-=Patterns Quick=-')  # -=Patterns Quick=-
Show_abcd = _input('Show_abcd', True)  # Display AB=CD patterns
Show_alt127_abcd = _input('Show_alt127_abcd', True)  # Display 1.27 AB=CD patterns
Show_rec_abcd = _input('Show_rec_abcd', True)  # Display Rec. AB=CD patterns
Show_patterns = _input('Show_patterns', True)  # Display normal 5-point patterns
Show_antipatterns = _input('Show_antipatterns', False)  # Display anti 5-point patterns
indicatorPatternsIndividual = _input('indicatorPatternsIndividual', '-=Patterns Individual=-')  # -=Patterns Individual=-
Show_trendlike1_abcd = _input('Show_trendlike1_abcd', True)  # Display Trendlike AB=CD #1
Show_trendlike2_abcd = _input('Show_trendlike2_abcd', True)  # Display Trendlike AB=CD #2
Show_perfect_abcd = _input('Show_perfect_abcd', True)  # Display Perfect AB=CD
Show_ideal1_abcd = _input('Show_ideal1_abcd', True)  # Display Ideal AB=CD #1
Show_ideal2_abcd = _input('Show_ideal2_abcd', True)  # Display Ideal AB=CD #2
Show_rangelike_abcd = _input('Show_rangelike_abcd', True)  # Display Rangelike AB=CD
Show_alt127_trendlike1_abcd = _input('Show_alt127_trendlike1_abcd', True)  # Display Trendlike 1.27 AB=CD #1
Show_alt127_trendlike2_abcd = _input('Show_alt127_trendlike2_abcd', True)  # Display Trendlike 1.27 AB=CD #2
Show_alt127_perfect_abcd = _input('Show_alt127_perfect_abcd', True)  # Display Perfect 1.27 AB=CD
Show_alt127_ideal1_abcd = _input('Show_alt127_ideal1_abcd', True)  # Display Ideal 1.27 AB=CD #1
Show_alt127_ideal2_abcd = _input('Show_alt127_ideal2_abcd', True)  # Display Ideal 1.27 AB=CD #2
Show_alt127_rangelike_abcd = _input('Show_alt127_rangelike_abcd', True)  # Display Rangelike 1.27 AB=CD
Show_rec_trendlike1_abcd = _input('Show_rec_trendlike1_abcd', True)  # Display Rec. Trendlike AB=CD #1
Show_rec_trendlike2_abcd = _input('Show_rec_trendlike2_abcd', True)  # Display Rec. Trendlike AB=CD #2
Show_rec_perfect_abcd = _input('Show_rec_perfect_abcd', True)  # Display Rec. Perfect AB=CD
Show_rec_ideal1_abcd = _input('Show_rec_ideal1_abcd', True)  # Display Rec. Ideal AB=CD #1
Show_rec_ideal2_abcd = _input('Show_rec_ideal2_abcd', True)  # Display Rec. Ideal AB=CD #2
Show_rec_rangelike_abcd = _input('Show_rec_rangelike_abcd', True)  # Display Rec. Rangelike AB=CD
Show_gartley = _input('Show_gartley', True)  # Display Gartley
Show_bat = _input('Show_bat', True)  # Display Bat
Show_altbat = _input('Show_altbat', True)  # Display Alt. Bat
Show_fiveo = _input('Show_fiveo', True)  # Display 5-0
Show_butterfly = _input('Show_butterfly', True)  # Display Butterfly
Show_crab = _input('Show_crab', True)  # Display Crab
Show_deepcrab = _input('Show_deepcrab', True)  # Display Deepcrab
Show_threedrives = _input('Show_threedrives', True)  # Display Three Drives
Show_cypher = _input('Show_cypher', True)  # Display Cypher
Show_shark = _input('Show_shark', True)  # Display Shark
Show_nenstar = _input('Show_nenstar', True)  # Display Nen Star
Show_blackswan = _input('Show_blackswan', True)  # Display Black Swan
Show_whiteswan = _input('Show_whiteswan', True)  # Display White Swan
Show_one2one = _input('Show_one2one', True)  # Display One2One
Show_newCypher = _input('Show_newCypher', True)  # Display New Cypher
Show_navarro200 = _input('Show_navarro200', True)  # Display Navarro 200
Show_leonardo = _input('Show_leonardo', True)  # Display Leonardo
Show_kane = _input('Show_kane', True)  # Display Kane
Show_garfly = _input('Show_garfly', True)  # Display Garfly
Show_maxbat = _input('Show_maxbat', True)  # Display Max. Bat
Show_maxgartley = _input('Show_maxgartley', True)  # Display Max. Gartley
Show_maxbutterfly = _input('Show_maxbutterfly', True)  # Display Max. Butterfly
Show_gartley113 = _input('Show_gartley113', True)  # Display Gartley 113
Show_butterfly113 = _input('Show_butterfly113', True)  # Display Butterfly 113
Show_antigartley = _input('Show_antigartley', True)  # Display Anti Gartley
Show_antibat = _input('Show_antibat', True)  # Display Anti Bat
Show_antialtbat = _input('Show_antialtbat', True)  # Display Anti Alt. Bat
Show_antifiveo = _input('Show_antifiveo', True)  # Display Anti 5-0
Show_antibutterfly = _input('Show_antibutterfly', True)  # Display Anti Butterfly
Show_anticrab = _input('Show_anticrab', True)  # Display Anti Crab
Show_antideepcrab = _input('Show_antideepcrab', True)  # Display Anti Deepcrab
Show_antithreedrives = _input('Show_antithreedrives', True)  # Display Anti Three Drives
Show_anticypher = _input('Show_anticypher', True)  # Display Anti Cypher
Show_antishark = _input('Show_antishark', True)  # Display Anti Shark
Show_antinenstar = _input('Show_antinenstar', True)  # Display Anti Nen Star
Show_antiblackswan = _input('Show_antiblackswan', True)  # Display Anti Black Swan
Show_antiwhiteswan = _input('Show_antiwhiteswan', True)  # Display Anti White Swan
Show_antione2one = _input('Show_antione2one', True)  # Display Anti One2One
Show_antinewCypher = _input('Show_antinewCypher', True)  # Display Anti New Cypher
Show_antinavarro200 = _input('Show_antinavarro200', True)  # Display Anti Navarro 200
Show_antileonardo = _input('Show_antileonardo', True)  # Display Anti Leonardo
Show_antikane = _input('Show_antikane', True)  # Display Anti Kane
Show_antigarfly = _input('Show_antigarfly', True)  # Display Anti Garfly
Show_antimaxbat = _input('Show_antimaxbat', True)  # Display Anti Max. Bat
Show_antimaxgartley = _input('Show_antimaxgartley', True)  # Display Anti Max. Gartley
Show_antimaxbutterfly = _input('Show_antimaxbutterfly', True)  # Display Anti Max. Butterfly
Show_antigartley113 = _input('Show_antigartley113', True)  # Display Anti Gartley 113
Show_antibutterfly113 = _input('Show_antibutterfly113', True)  # Display Anti Butterfly 113
peaks = Arr(0, 0.0)
troughs = Arr(0, 0.0)
_lastDirection = False
_lastPeakValue = 0.0
_lastTroughValue = 0.0
_lastPeak = 0
_lastTrough = 0
_patternInstanceCounter = 0
_maxPatternInstances = 0
_projectionInstanceCounter = 0
_maxProjectionInstances = 0
_drawnProjectionInstanceCounter = 0
_maxDrawnProjectionInstances = 0
_zzHandle = 0
_patternNames = Arr(0, "")
_patternCounter = Arr(0, 0)
_patternX = Arr(0, 0, dims=(10,))
_patternA = Arr(0, 0, dims=(10,))
_patternB = Arr(0, 0, dims=(10,))
_patternC = Arr(0, 0, dims=(10,))
_patternD = Arr(0, 0, dims=(10,))
com1 = ''
com2 = ''
com3 = ''
com4 = ''
com5 = ''
com6 = ''
com7 = ''
com8 = ''
com9 = ''
_timeOfInit = 0

class PATTERN_DESCRIPTOR(MqlObject):
    _q_fields = ('ab2xa_min', 'ab2xa_max', 'bc2ab_min', 'bc2ab_max', 'cd2bc_min', 'cd2bc_max', 'ad2xa_min', 'ad2xa_max', 'cd2xc_min', 'cd2xc_max', 'xc2xa_min', 'xc2xa_max', 'cd2ab_min', 'cd2ab_max')
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

class PATTERN_INSTANCE(MqlObject):
    _q_fields = ('patternIndex', 'patternBufferIndex', 'bullish', 'overlapping', 'XDateTime', 'ADateTime', 'BDateTime', 'CDateTime', 'DDateTime', 'X', 'A', 'B', 'C', 'D', 'PRZ')
    def __init__(self, *args):
        self.patternIndex = 0
        self.patternBufferIndex = 0
        self.bullish = False
        self.overlapping = False
        self.XDateTime = 0
        self.ADateTime = 0
        self.BDateTime = 0
        self.CDateTime = 0
        self.DDateTime = 0
        self.X = 0.0
        self.A = 0.0
        self.B = 0.0
        self.C = 0.0
        self.D = 0.0
        self.PRZ = 0.0

def OnInit():
    global _timeOfInit, _zzHandle
    SetIndexBuffer(0, peaks, INDICATOR_DATA)
    SetIndexBuffer(1, troughs, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    _sw1 = zztype
    if _sw1 == FASTZZ:
        _zzHandle = iCustom(None, 0, 'Downloads\\fastzz', SwingSize)
    elif _sw1 == ALEXSTAL:
        _zzHandle = iCustom(None, 0, 'Downloads\\alexstal_zigzagprof', zzperiod, zzamplitude, zzminmotion, True)
    else:
        _zzHandle = iCustom(None, 0, 'Downloads\\swingchart')
    if _zzHandle == INVALID_HANDLE:
        printf('Error obtaining handle')
        return INIT_FAILED
    MathSrand(GetTickCount())
    _timeOfInit = MathRand()
    for i in range(ObjectsTotal(0, 0, -1) - 1, 0 - 1, -1):
        name = ObjectName(0, i, 0, -1)
        if StringFind(name, 'U ' + _identifier) != -1 or StringFind(name, 'D ' + _identifier) != -1:
            ObjectDelete(0, name)
    return PopulatePatterns()

def OnDeinit(reason):
    OnReinit()
    Comment('')
    ArrayFree(_patterns)
    ArrayFree(_patternInstances)
    ArrayFree(_projectionInstances)
    ArrayFree(_drawnProjectionInstances)
    ArrayFree(_patternNames)
    ArrayFree(_patternCounter)
    ArrayFree(_patternX)
    ArrayFree(_patternA)
    ArrayFree(_patternB)
    ArrayFree(_patternC)
    ArrayFree(_patternD)

def OnReinit():
    global _drawnProjectionInstanceCounter, _lastPeak, _lastPeakValue, _lastTrough, _lastTroughValue, _patternInstanceCounter
    _lastPeak = 0
    _lastTrough = 0
    _lastPeakValue = 0.0
    _lastTroughValue = 0.0
    _patternInstanceCounter = 0
    _drawnProjectionInstanceCounter = 0
    ArrayFill(_patternCounter, 0, 66, 0)
    for i in range(0, 66):
        for j in range(0, 10):
            _patternX[i][j] = 0
            _patternA[i][j] = 0
            _patternB[i][j] = 0
            _patternC[i][j] = 0
            _patternD[i][j] = 0
    for i in range(ObjectsTotal(0, 0, -1) - 1, 0 - 1, -1):
        name = ObjectName(0, i, 0, -1)
        if StringFind(name, 'U ' + _identifier + StringFormat('%x', _timeOfInit)) != -1 or StringFind(name, 'D ' + _identifier + StringFormat('%x', _timeOfInit)) != -1:
            ObjectDelete(0, name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _drawnProjectionInstanceCounter, _lastDirection, _lastPeak, _lastPeakValue, _lastTrough, _lastTroughValue, _maxDrawnProjectionInstances, _patternInstanceCounter, _projectionInstanceCounter
    start = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        OnReinit()
    else:
        start = prev_calculated - 1
    start = MathMax(1, start)
    if BarsCalculated(_zzHandle) < rates_total:
        printf('ZigZag not calculated: ' + IntegerToString(GetLastError()))
        return 0
    if CopyBuffer(_zzHandle, 0, 0, rates_total, peaks) <= 0:
        printf('ZigZag peaks not copied: ' + IntegerToString(GetLastError()))
        return 0
    if CopyBuffer(_zzHandle, 1, 0, rates_total, troughs) <= 0:
        printf('ZigZag troughs not copied: ' + IntegerToString(GetLastError()))
        return 0
    for bar in range(start, rates_total):
        if bar < (rates_total - History):
            continue
        lastPeak = FirstNonZeroFrom(bar, peaks)
        lastTrough = FirstNonZeroFrom(bar, troughs)
        if lastPeak == -1 or lastTrough == -1:
            continue
        lastPeakValue = peaks[lastPeak]
        lastTroughValue = troughs[lastTrough]
        if lastPeakValue == _lastPeakValue and lastTroughValue == _lastTroughValue:
            continue
        endsInTrough = lastTrough > lastPeak
        if lastTrough == lastPeak:
            zzDirection = ZigZagDirection(lastPeak)
            if zzDirection == 0:
                continue
            elif zzDirection == -1:
                endsInTrough = True
            elif zzDirection == 1:
                endsInTrough = False
        UndisplayProjections()
        if _lastDirection == endsInTrough and (not (_lastPeak < lastPeak and _lastTrough < lastTrough)):
            UndisplayPatterns()
        else:
            i = 0
            while i < _patternInstanceCounter:
                instance = _copy(_patternInstances[i])
                k = instance.patternIndex
                bullish = instance.bullish
                XDateTime = instance.XDateTime
                ADateTime = instance.ADateTime
                BDateTime = instance.BDateTime
                CDateTime = instance.CDateTime
                DDateTime = instance.DDateTime
                StoreOverlaps(k, XDateTime, ADateTime, BDateTime, CDateTime, DDateTime)
                i += 1
        if Show_PRZ:
            UndisplayPRZs()
        _patternInstanceCounter = 0
        _lastPeak = lastPeak
        _lastTrough = lastTrough
        _lastPeakValue = lastPeakValue
        _lastTroughValue = lastTroughValue
        _lastDirection = endsInTrough
        for patternIndex in range(0, 66):
            if patternIndex == TRENDLIKE1_ABCD and ((not Show_trendlike1_abcd) or (not Show_abcd)):
                continue
            if patternIndex == TRENDLIKE2_ABCD and ((not Show_trendlike2_abcd) or (not Show_abcd)):
                continue
            if patternIndex == PERFECT_ABCD and ((not Show_perfect_abcd) or (not Show_abcd)):
                continue
            if patternIndex == IDEAL1_ABCD and ((not Show_ideal1_abcd) or (not Show_abcd)):
                continue
            if patternIndex == IDEAL2_ABCD and ((not Show_ideal2_abcd) or (not Show_abcd)):
                continue
            if patternIndex == RANGELIKE_ABCD and ((not Show_rangelike_abcd) or (not Show_abcd)):
                continue
            if patternIndex == ALT127_TRENDLIKE1_ABCD and ((not Show_alt127_trendlike1_abcd) or (not Show_alt127_abcd)):
                continue
            if patternIndex == ALT127_TRENDLIKE2_ABCD and ((not Show_alt127_trendlike2_abcd) or (not Show_alt127_abcd)):
                continue
            if patternIndex == ALT127_PERFECT_ABCD and ((not Show_alt127_perfect_abcd) or (not Show_alt127_abcd)):
                continue
            if patternIndex == ALT127_IDEAL1_ABCD and ((not Show_alt127_ideal1_abcd) or (not Show_alt127_abcd)):
                continue
            if patternIndex == ALT127_IDEAL2_ABCD and ((not Show_alt127_ideal2_abcd) or (not Show_alt127_abcd)):
                continue
            if patternIndex == ALT127_RANGELIKE_ABCD and ((not Show_alt127_rangelike_abcd) or (not Show_alt127_abcd)):
                continue
            if patternIndex == REC_TRENDLIKE1_ABCD and ((not Show_rec_trendlike1_abcd) or (not Show_rec_abcd)):
                continue
            if patternIndex == REC_TRENDLIKE2_ABCD and ((not Show_rec_trendlike2_abcd) or (not Show_rec_abcd)):
                continue
            if patternIndex == REC_PERFECT_ABCD and ((not Show_rec_perfect_abcd) or (not Show_rec_abcd)):
                continue
            if patternIndex == REC_IDEAL1_ABCD and ((not Show_rec_ideal1_abcd) or (not Show_rec_abcd)):
                continue
            if patternIndex == REC_IDEAL2_ABCD and ((not Show_rec_ideal2_abcd) or (not Show_rec_abcd)):
                continue
            if patternIndex == REC_RANGELIKE_ABCD and ((not Show_rec_rangelike_abcd) or (not Show_rec_abcd)):
                continue
            if patternIndex == GARTLEY and ((not Show_gartley) or (not Show_patterns)):
                continue
            if patternIndex == BAT and ((not Show_bat) or (not Show_patterns)):
                continue
            if patternIndex == ALTBAT and ((not Show_altbat) or (not Show_patterns)):
                continue
            if patternIndex == FIVEO and ((not Show_fiveo) or (not Show_patterns)):
                continue
            if patternIndex == BUTTERFLY and ((not Show_butterfly) or (not Show_patterns)):
                continue
            if patternIndex == CRAB and ((not Show_crab) or (not Show_patterns)):
                continue
            if patternIndex == DEEPCRAB and ((not Show_deepcrab) or (not Show_patterns)):
                continue
            if patternIndex == THREEDRIVES and ((not Show_threedrives) or (not Show_patterns)):
                continue
            if patternIndex == CYPHER and ((not Show_cypher) or (not Show_patterns)):
                continue
            if patternIndex == SHARK and ((not Show_shark) or (not Show_patterns)):
                continue
            if patternIndex == NENSTAR and ((not Show_nenstar) or (not Show_patterns)):
                continue
            if patternIndex == BLACKSWAN and ((not Show_blackswan) or (not Show_patterns)):
                continue
            if patternIndex == WHITESWAN and ((not Show_whiteswan) or (not Show_patterns)):
                continue
            if patternIndex == ONE2ONE and ((not Show_one2one) or (not Show_patterns)):
                continue
            if patternIndex == NEWCYPHER and ((not Show_newCypher) or (not Show_patterns)):
                continue
            if patternIndex == NAVARRO200 and ((not Show_navarro200) or (not Show_patterns)):
                continue
            if patternIndex == LEONARDO and ((not Show_leonardo) or (not Show_patterns)):
                continue
            if patternIndex == KANE and ((not Show_kane) or (not Show_patterns)):
                continue
            if patternIndex == GARFLY and ((not Show_garfly) or (not Show_patterns)):
                continue
            if patternIndex == MAXBAT and ((not Show_maxbat) or (not Show_patterns)):
                continue
            if patternIndex == MAXGARTLEY and ((not Show_maxgartley) or (not Show_patterns)):
                continue
            if patternIndex == MAXBUTTERFLY and ((not Show_maxbutterfly) or (not Show_patterns)):
                continue
            if patternIndex == GARTLEY113 and ((not Show_gartley113) or (not Show_patterns)):
                continue
            if patternIndex == BUTTERFLY113 and ((not Show_butterfly113) or (not Show_patterns)):
                continue
            if patternIndex == ANTI_GARTLEY and ((not Show_antigartley) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_BAT and ((not Show_antibat) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_ALTBAT and ((not Show_antialtbat) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_FIVEO and ((not Show_antifiveo) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_BUTTERFLY and ((not Show_antibutterfly) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_CRAB and ((not Show_anticrab) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_DEEPCRAB and ((not Show_antideepcrab) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_THREEDRIVES and ((not Show_antithreedrives) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_CYPHER and ((not Show_anticypher) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_SHARK and ((not Show_antishark) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_NENSTAR and ((not Show_antinenstar) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_BLACKSWAN and ((not Show_antiblackswan) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_WHITESWAN and ((not Show_antiwhiteswan) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_ONE2ONE and ((not Show_antione2one) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_NEWCYPHER and ((not Show_antinewCypher) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_NAVARRO200 and ((not Show_antinavarro200) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_LEONARDO and ((not Show_antileonardo) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_KANE and ((not Show_antikane) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_GARFLY and ((not Show_antigarfly) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_MAXBAT and ((not Show_antimaxbat) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_MAXGARTLEY and ((not Show_antimaxgartley) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_MAXBUTTERFLY and ((not Show_antimaxbutterfly) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_GARTLEY113 and ((not Show_antigartley113) or (not Show_antipatterns)):
                continue
            if patternIndex == ANTI_BUTTERFLY113 and ((not Show_antibutterfly113) or (not Show_antipatterns)):
                continue
            pattern = _copy(_patterns[patternIndex])
            ab2xaConstraint = pattern.ab2xa_max != 0 and pattern.ab2xa_min != 0
            ad2xaConstraint = pattern.ad2xa_max != 0 and pattern.ad2xa_min != 0
            bc2abConstraint = pattern.bc2ab_max != 0 and pattern.bc2ab_min != 0
            cd2bcConstraint = pattern.cd2bc_max != 0 and pattern.cd2bc_min != 0
            cd2xcConstraint = pattern.cd2xc_max != 0 and pattern.cd2xc_min != 0
            xc2xaConstraint = pattern.xc2xa_max != 0 and pattern.xc2xa_min != 0
            cd2abConstraint = pattern.cd2ab_max != 0 and pattern.cd2ab_min != 0
            ab2xaSlack = (SlackUnary if (pattern.ab2xa_max == pattern.ab2xa_min) else SlackRange)
            ad2xaSlack = (SlackUnary if (pattern.ad2xa_max == pattern.ad2xa_min) else SlackRange)
            bc2abSlack = (SlackUnary if (pattern.bc2ab_max == pattern.bc2ab_min) else SlackRange)
            cd2bcSlack = (SlackUnary if (pattern.cd2bc_max == pattern.cd2bc_min) else SlackRange)
            cd2xcSlack = (SlackUnary if (pattern.cd2xc_max == pattern.cd2xc_min) else SlackRange)
            xc2xaSlack = (SlackUnary if (pattern.xc2xa_max == pattern.xc2xa_min) else SlackRange)
            cd2abSlack = (SlackUnary if (pattern.cd2ab_max == pattern.cd2ab_min) else SlackRange)
            _projectionInstanceCounter = 0
            xFirstRun = True
            XIndex = bar - BarsAnalyzed
            while XIndex <= bar:
                if XIndex <= 0:
                    XIndex += 1
                    continue
                isPeak = IsProperValue(peaks[XIndex])
                isTrough = IsProperValue(troughs[XIndex])
                if (not isPeak) and (not isTrough):
                    XIndex += 1
                    continue
                startsInTrough = isTrough
                xVerticalZZ = isPeak and isTrough
                xZZDirection = not startsInTrough
                if xVerticalZZ:
                    if xFirstRun:
                        startsInTrough = not startsInTrough
                    zzDirection = ZigZagDirection(XIndex)
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
                for AIndex in range(XIndex + aSkip, bar + 1):
                    extremeIndexXA = (AIndex if (XIndex == AIndex) else (AIndex - 1))
                    if ((startsInTrough and IsProperValue(troughs[extremeIndexXA])) and troughs[extremeIndexXA] < X) or (((not startsInTrough) and IsProperValue(peaks[extremeIndexXA])) and peaks[extremeIndexXA] > X):
                        break
                    if ((XIndex != AIndex and IsProperValue(troughs[AIndex])) and IsProperValue(peaks[AIndex])) and (((startsInTrough and ZigZagDirection(AIndex) == 1) and troughs[AIndex] < X) or (((not startsInTrough) and ZigZagDirection(AIndex) == -1) and peaks[AIndex] > X)):
                        break
                    A = (peaks[AIndex] if startsInTrough else troughs[AIndex])
                    if ((not IsProperValue(A)) or (startsInTrough and A < extremeA)) or ((not startsInTrough) and A > extremeA):
                        continue
                    extremeA = A
                    XA = MathAbs(A - X)
                    if XA == 0:
                        continue
                    extremeB = (DBL_MAX if startsInTrough else DBL_MIN)
                    bSkip = 0
                    if XIndex == AIndex:
                        bSkip = 1
                    for BIndex in range(AIndex + bSkip, bar + 1):
                        extremeIndexAB = (BIndex if (AIndex == BIndex) else (BIndex - 1))
                        if (((not startsInTrough) and IsProperValue(troughs[extremeIndexAB])) and troughs[extremeIndexAB] < A) or ((startsInTrough and IsProperValue(peaks[extremeIndexAB])) and peaks[extremeIndexAB] > A):
                            break
                        if ((AIndex != BIndex and IsProperValue(troughs[BIndex])) and IsProperValue(peaks[BIndex])) and ((((not startsInTrough) and ZigZagDirection(BIndex) == 1) and troughs[BIndex] < A) or ((startsInTrough and ZigZagDirection(BIndex) == -1) and peaks[BIndex] > A)):
                            break
                        B = (troughs[BIndex] if startsInTrough else peaks[BIndex])
                        if ((not IsProperValue(B)) or (startsInTrough and B > extremeB)) or ((not startsInTrough) and B < extremeB):
                            continue
                        extremeB = B
                        if AIndex == BIndex:
                            zzDirection = ZigZagDirection(AIndex)
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
                        for CIndex in range(BIndex + cSkip, bar + 1):
                            extremeIndexBC = (CIndex if (BIndex == CIndex) else (CIndex - 1))
                            if ((startsInTrough and IsProperValue(troughs[extremeIndexBC])) and troughs[extremeIndexBC] < B) or (((not startsInTrough) and IsProperValue(peaks[extremeIndexBC])) and peaks[extremeIndexBC] > B):
                                break
                            if ((BIndex != CIndex and IsProperValue(troughs[CIndex])) and IsProperValue(peaks[CIndex])) and (((startsInTrough and ZigZagDirection(CIndex) == 1) and troughs[CIndex] < B) or (((not startsInTrough) and ZigZagDirection(CIndex) == -1) and peaks[CIndex] > B)):
                                break
                            C = (peaks[CIndex] if startsInTrough else troughs[CIndex])
                            if not IsProperValue(C):
                                continue
                            if (startsInTrough and C < extremeC) or ((not startsInTrough) and C > extremeC):
                                continue
                            extremeC = C
                            if BIndex == CIndex:
                                zzDirection = ZigZagDirection(BIndex)
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
                            bc2abContinue = bc2abConstraint
                            xc2xaContinue = xc2xaConstraint
                            bc2abContinue &= bc2abRatio < (pattern.bc2ab_min - bc2abSlack)
                            xc2xaContinue &= xc2xaRatio < (pattern.xc2xa_min - xc2xaSlack)
                            if bc2abContinue or xc2xaContinue:
                                continue
                            bc2abCutoff = bc2abConstraint
                            xc2xaCutoff = xc2xaConstraint
                            bc2abCutoff &= bc2abRatio > (pattern.bc2ab_max + bc2abSlack)
                            xc2xaCutoff &= xc2xaRatio > (pattern.xc2xa_max + xc2xaSlack)
                            if bc2abCutoff or xc2xaCutoff:
                                break
                            lastExtremeC = True
                            for i in range(CIndex + 1, bar + 1):
                                if ((startsInTrough and IsProperValue(peaks[i])) and peaks[i] > C) or (((not startsInTrough) and IsProperValue(troughs[i])) and troughs[i] < C):
                                    lastExtremeC = False
                                    break
                            extremeD = (DBL_MAX if startsInTrough else DBL_MIN)
                            dSkip = 0
                            if BIndex == CIndex:
                                dSkip = 1
                            for DIndex in range(CIndex + dSkip, bar + 1):
                                extremeIndexCD = (DIndex if (CIndex == DIndex) else (DIndex - 1))
                                if (((not startsInTrough) and IsProperValue(troughs[extremeIndexCD])) and troughs[extremeIndexCD] < C) or ((startsInTrough and IsProperValue(peaks[extremeIndexCD])) and peaks[extremeIndexCD] > C):
                                    break
                                if ((CIndex != DIndex and IsProperValue(troughs[DIndex])) and IsProperValue(peaks[DIndex])) and ((((not startsInTrough) and ZigZagDirection(DIndex) == 1) and troughs[DIndex] < C) or ((startsInTrough and ZigZagDirection(DIndex) == -1) and peaks[DIndex] > C)):
                                    break
                                imaginaryD = ((startsInTrough and CIndex == lastPeak) and lastTrough <= lastPeak) or (((not startsInTrough) and CIndex == lastTrough) and lastPeak <= lastTrough)
                                if imaginaryD and lastPeak == lastTrough:
                                    imaginaryD &= (startsInTrough and ZigZagDirection(lastPeak) == 1) or ((not startsInTrough) and ZigZagDirection(lastPeak) == -1)
                                D = (troughs[DIndex] if startsInTrough else peaks[DIndex])
                                if (not imaginaryD) and (((not IsProperValue(D)) or (startsInTrough and D > extremeD)) or ((not startsInTrough) and D < extremeD)):
                                    continue
                                extremeD = D
                                if (not imaginaryD) and CIndex == DIndex:
                                    zzDirection = ZigZagDirection(CIndex)
                                    if zzDirection == 0:
                                        continue
                                    elif zzDirection == -1 and (not startsInTrough):
                                        continue
                                    elif zzDirection == 1 and startsInTrough:
                                        continue
                                lastExtremeD = True
                                if not imaginaryD:
                                    for i in range(DIndex + 1, bar + 1):
                                        if (((not startsInTrough) and IsProperValue(peaks[i])) and peaks[i] > D) or ((startsInTrough and IsProperValue(troughs[i])) and troughs[i] < D):
                                            lastExtremeD = False
                                            break
                                activeSwing = ((endsInTrough and startsInTrough) and DIndex == lastTrough) or (((not endsInTrough) and (not startsInTrough)) and DIndex == lastPeak)
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
                                nearD = (DBL_MAX if startsInTrough else DBL_MIN)
                                farD = (DBL_MIN if startsInTrough else DBL_MAX)
                                if cd2bcConstraint:
                                    nearD = (MathMin(nearD, nearD_cd2bc) if startsInTrough else MathMax(nearD, nearD_cd2bc))
                                    farD = (MathMax(farD, farD_cd2bc) if startsInTrough else MathMin(farD, farD_cd2bc))
                                if ad2xaConstraint:
                                    nearD = (MathMin(nearD, nearD_ad2xa) if startsInTrough else MathMax(nearD, nearD_ad2xa))
                                    farD = (MathMax(farD, farD_ad2xa) if startsInTrough else MathMin(farD, farD_ad2xa))
                                if cd2xcConstraint:
                                    nearD = (MathMin(nearD, nearD_cd2xc) if startsInTrough else MathMax(nearD, nearD_cd2xc))
                                    farD = (MathMax(farD, farD_cd2xc) if startsInTrough else MathMin(farD, farD_cd2xc))
                                if cd2abConstraint:
                                    nearD = (MathMin(nearD, nearD_cd2ab) if startsInTrough else MathMax(nearD, nearD_cd2ab))
                                    farD = (MathMax(farD, farD_cd2ab) if startsInTrough else MathMin(farD, farD_cd2ab))
                                if imaginaryD and (not OneAheadProjection):
                                    break
                                elif (imaginaryD or (startsInTrough and D > nearD)) or ((not startsInTrough) and D < nearD):
                                    if (startsInTrough and farD > nearD) or ((not startsInTrough) and farD < nearD):
                                        break
                                    if (not lastExtremeC) or (not lastExtremeD):
                                        continue
                                    if not EmergingPatterns:
                                        break
                                    if Is4PointPattern(patternIndex):
                                        StoreProjection(patternIndex, startsInTrough, 0, 0.0, time[AIndex], A, time[BIndex], B, time[CIndex], C, time[bar], nearD, farD)
                                    else:
                                        StoreProjection(patternIndex, startsInTrough, time[XIndex], X, time[AIndex], A, time[BIndex], B, time[CIndex], C, time[bar], nearD, farD)
                                    break
                                elif (startsInTrough and D < farD) or ((not startsInTrough) and D > farD):
                                    break
                                else:
                                    if Overlaps(patternIndex, time[XIndex], time[AIndex], time[BIndex], time[CIndex], time[DIndex]):
                                        continue
                                    if Is4PointPattern(patternIndex):
                                        DisplayPattern_1(patternIndex, startsInTrough, time[AIndex], A, time[BIndex], B, time[CIndex], C, time[DIndex], D)
                                        if activeSwing:
                                            StorePattern(patternIndex, startsInTrough, 0, time[AIndex], time[BIndex], time[CIndex], time[DIndex])
                                            if Show_PRZ:
                                                DisplayPRZ_1(patternIndex, startsInTrough, time[AIndex], A, time[BIndex], time[CIndex], C, time[DIndex], D, farD)
                                        else:
                                            StoreOverlaps(patternIndex, 0, time[AIndex], time[BIndex], time[CIndex], time[DIndex])
                                    else:
                                        DisplayPattern_2(patternIndex, startsInTrough, time[XIndex], X, time[AIndex], A, time[BIndex], B, time[CIndex], C, time[DIndex], D)
                                        if activeSwing:
                                            StorePattern(patternIndex, startsInTrough, time[XIndex], time[AIndex], time[BIndex], time[CIndex], time[DIndex])
                                            if Show_PRZ:
                                                DisplayPRZ_2(patternIndex, startsInTrough, time[XIndex], X, time[AIndex], A, time[BIndex], time[CIndex], C, time[DIndex], D, farD)
                                        else:
                                            StoreOverlaps(patternIndex, time[XIndex], time[AIndex], time[BIndex], time[CIndex], time[DIndex])
                if xVerticalZZ:
                    if xFirstRun:
                        XIndex -= 1
                        xFirstRun = False
                    else:
                        xFirstRun = True
                XIndex += 1
            for i in range(1, _projectionInstanceCounter):
                _projectionInstances[i].overlapping = False
                j = i
                while j > 0 and _projectionInstances[j - 1].D > _projectionInstances[j].D:
                    tmp = _copy(_projectionInstances[j])
                    _assign(_projectionInstances[j], _projectionInstances[j - 1])
                    _assign(_projectionInstances[j - 1], tmp)
                    j -= 1
            _projectionInstances[0].overlapping = False
            forward = True
            i = 0
            while _projectionInstanceCounter != 0:
                bullish = _projectionInstances[i].bullish
                if (forward and (not bullish)) or ((not forward) and bullish):
                    XDateTime = _projectionInstances[i].XDateTime
                    ADateTime = _projectionInstances[i].ADateTime
                    BDateTime = _projectionInstances[i].BDateTime
                    CDateTime = _projectionInstances[i].CDateTime
                    DDateTime = _projectionInstances[i].DDateTime
                    X = _projectionInstances[i].X
                    A = _projectionInstances[i].A
                    B = _projectionInstances[i].B
                    C = _projectionInstances[i].C
                    D = _projectionInstances[i].D
                    farD = _projectionInstances[i].PRZ
                    if Overlaps(patternIndex, XDateTime, ADateTime, BDateTime, CDateTime, 332812800):
                        _projectionInstances[i].overlapping = True
                    j = i
                    while True:
                        if forward:
                            if j == 0:
                                break
                            else:
                                j -= 1
                        else:
                            if j == (_projectionInstanceCounter - 1):
                                break
                            else:
                                j += 1
                        if (not _projectionInstances[j].overlapping) and _projectionInstances[j].bullish == bullish:
                            XDateTimeActive = _projectionInstances[j].XDateTime
                            ADateTimeActive = _projectionInstances[j].ADateTime
                            BDateTimeActive = _projectionInstances[j].BDateTime
                            CDateTimeActive = _projectionInstances[j].CDateTime
                            DDateTimeActive = _projectionInstances[j].DDateTime
                            numMatches = 0
                            if (not Is4PointPattern(patternIndex)) and XDateTime == XDateTimeActive:
                                numMatches += 1
                            if ADateTime == ADateTimeActive:
                                numMatches += 1
                            if BDateTime == BDateTimeActive:
                                numMatches += 1
                            if CDateTime == CDateTimeActive:
                                numMatches += 1
                            if numMatches > MaxSamePoints:
                                _projectionInstances[i].overlapping = True
                                break
                    if not _projectionInstances[i].overlapping:
                        if Is4PointPattern(patternIndex):
                            DisplayProjection_1(patternIndex, bullish, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D)
                        else:
                            DisplayProjection_2(patternIndex, bullish, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D)
                        _assign(_drawnProjectionInstances[_drawnProjectionInstanceCounter], _projectionInstances[i])
                        _drawnProjectionInstanceCounter += 1
                        if _drawnProjectionInstanceCounter >= _maxDrawnProjectionInstances:
                            _maxDrawnProjectionInstances *= 2
                            if ArrayResize(_drawnProjectionInstances, _maxDrawnProjectionInstances) < _maxDrawnProjectionInstances:
                                printf('Error allocating array')
                if forward:
                    if i == (_projectionInstanceCounter - 1):
                        forward = False
                    else:
                        i += 1
                else:
                    if i == 0:
                        break
                    else:
                        i -= 1
    return rates_total

def Is4PointPattern(patternIndex):
    if patternIndex == TRENDLIKE1_ABCD:
        return True
    if patternIndex == TRENDLIKE2_ABCD:
        return True
    if patternIndex == PERFECT_ABCD:
        return True
    if patternIndex == IDEAL1_ABCD:
        return True
    if patternIndex == IDEAL2_ABCD:
        return True
    if patternIndex == RANGELIKE_ABCD:
        return True
    if patternIndex == ALT127_TRENDLIKE1_ABCD:
        return True
    if patternIndex == ALT127_TRENDLIKE2_ABCD:
        return True
    if patternIndex == ALT127_PERFECT_ABCD:
        return True
    if patternIndex == ALT127_IDEAL1_ABCD:
        return True
    if patternIndex == ALT127_IDEAL2_ABCD:
        return True
    if patternIndex == ALT127_RANGELIKE_ABCD:
        return True
    if patternIndex == REC_TRENDLIKE1_ABCD:
        return True
    if patternIndex == REC_TRENDLIKE2_ABCD:
        return True
    if patternIndex == REC_PERFECT_ABCD:
        return True
    if patternIndex == REC_IDEAL1_ABCD:
        return True
    if patternIndex == REC_IDEAL2_ABCD:
        return True
    if patternIndex == REC_RANGELIKE_ABCD:
        return True
    return False

def ZigZagDirection(index):
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
        if IsProperValue(array[j]):
            return j
    return -1

def IsProperValue(value):
    return value != 0 and value != EMPTY_VALUE

def ShowComment(sComment):
    global com1, com2, com3, com4, com5, com6, com7, com8, com9
    if sComment != '':
        com9 = com8
        com8 = com7
        com7 = com6
        com6 = com5
        com5 = com4
        com4 = com3
        com3 = com2
        com2 = com1
        com1 = sComment
    Comment('HarmonicPatternFinderV2 © 2016', '\n', '\n', com1, '\n', com2, '\n', com3, '\n', com4, '\n', com5, '\n', com6, '\n', com7, '\n', com8, '\n', com9, '\n')

def Overlaps(k, XDateTime, ADateTime, BDateTime, CDateTime, DDateTime):
    overlaps = False
    for i in range(0, 10):
        numMatches = 0
        if (not Is4PointPattern(k)) and XDateTime == _patternX[k][i]:
            numMatches += 1
        if ADateTime == _patternA[k][i]:
            numMatches += 1
        if BDateTime == _patternB[k][i]:
            numMatches += 1
        if CDateTime == _patternC[k][i]:
            numMatches += 1
        if DDateTime == _patternD[k][i]:
            numMatches += 1
        if numMatches > MaxSamePoints:
            return True
    i = 0
    while i < _patternInstanceCounter:
        instance = _copy(_patternInstances[i])
        patternIndexActive = _patternInstances[i].patternIndex
        if patternIndexActive != k:
            i += 1
            continue
        bullish = instance.bullish
        XDateTimeActive = instance.XDateTime
        ADateTimeActive = instance.ADateTime
        BDateTimeActive = instance.BDateTime
        CDateTimeActive = instance.CDateTime
        DDateTimeActive = instance.DDateTime
        numMatches = 0
        if (not Is4PointPattern(k)) and XDateTime == XDateTimeActive:
            numMatches += 1
        if ADateTime == ADateTimeActive:
            numMatches += 1
        if BDateTime == BDateTimeActive:
            numMatches += 1
        if CDateTime == CDateTimeActive:
            numMatches += 1
        if DDateTime == DDateTimeActive:
            numMatches += 1
        if numMatches > MaxSamePoints:
            return True
        i += 1
    return False

def StoreOverlaps(k, XDateTime, ADateTime, BDateTime, CDateTime, DDateTime):
    index = _patternCounter[k]
    _patternCounter[k] = _imod(index + 1, 10)
    _patternX[k][index] = XDateTime
    _patternA[k][index] = ADateTime
    _patternB[k][index] = BDateTime
    _patternC[k][index] = CDateTime
    _patternD[k][index] = DDateTime

def StorePattern(k, bullish, XDateTime, ADateTime, BDateTime, CDateTime, DDateTime):
    global _maxPatternInstances, _patternInstanceCounter
    _patternInstances[_patternInstanceCounter].patternIndex = k
    _patternInstances[_patternInstanceCounter].bullish = bullish
    _patternInstances[_patternInstanceCounter].XDateTime = XDateTime
    _patternInstances[_patternInstanceCounter].ADateTime = ADateTime
    _patternInstances[_patternInstanceCounter].BDateTime = BDateTime
    _patternInstances[_patternInstanceCounter].CDateTime = CDateTime
    _patternInstances[_patternInstanceCounter].DDateTime = DDateTime
    _patternInstanceCounter += 1
    if _patternInstanceCounter >= _maxPatternInstances:
        _maxPatternInstances *= 2
        if ArrayResize(_patternInstances, _maxPatternInstances) < _maxPatternInstances:
            printf('Error allocating array')

def StoreProjection(k, bullish, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D, farD):
    global _maxProjectionInstances, _projectionInstanceCounter
    _projectionInstances[_projectionInstanceCounter].patternIndex = k
    _projectionInstances[_projectionInstanceCounter].bullish = bullish
    _projectionInstances[_projectionInstanceCounter].XDateTime = XDateTime
    _projectionInstances[_projectionInstanceCounter].ADateTime = ADateTime
    _projectionInstances[_projectionInstanceCounter].BDateTime = BDateTime
    _projectionInstances[_projectionInstanceCounter].CDateTime = CDateTime
    _projectionInstances[_projectionInstanceCounter].DDateTime = DDateTime
    _projectionInstances[_projectionInstanceCounter].X = X
    _projectionInstances[_projectionInstanceCounter].A = A
    _projectionInstances[_projectionInstanceCounter].B = B
    _projectionInstances[_projectionInstanceCounter].C = C
    _projectionInstances[_projectionInstanceCounter].D = D
    _projectionInstances[_projectionInstanceCounter].PRZ = farD
    _projectionInstanceCounter += 1
    if _projectionInstanceCounter >= _maxProjectionInstances:
        _maxProjectionInstances *= 2
        if ArrayResize(_projectionInstances, _maxProjectionInstances) < _maxProjectionInstances:
            printf('Error allocating array')

def DisplayPRZ_1(k, bullish, ADateTime, A, BDateTime, CDateTime, C, DDateTime, D, farD):
    unique = UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime)
    prefix = ('Bullish ' if bullish else 'Bearish ')
    prefixName = (('U ' + _identifier) if bullish else ('D ' + _identifier))
    name = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PRZ' + unique
    ObjectCreate(0, name, OBJ_TREND, 0, DDateTime - 1, farD, DDateTime, farD)
    ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(0, name, OBJPROP_COLOR, (ClrBull4P if bullish else ClrBear4P))
    ObjectSetInteger(0, name, OBJPROP_STYLE, Style_PRZ)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PRZ stop ' + DoubleToString(farD))

def DisplayPRZ_2(k, bullish, XDateTime, X, ADateTime, A, BDateTime, CDateTime, C, DDateTime, D, farD):
    unique = UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime)
    prefix = ('Bullish ' if bullish else 'Bearish ')
    prefixName = (('U ' + _identifier) if bullish else ('D ' + _identifier))
    name = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PRZ' + unique
    ObjectCreate(0, name, OBJ_TREND, 0, DDateTime - 1, farD, DDateTime, farD)
    ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(0, name, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name, OBJPROP_STYLE, Style_PRZ)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PRZ stop ' + DoubleToString(farD))

def DisplayPattern_1(k, bullish, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
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
    ObjectSetInteger(0, name0, OBJPROP_COLOR, (ClrBull4P if bullish else ClrBear4P))
    ObjectSetInteger(0, name1, OBJPROP_COLOR, (ClrBull4P if bullish else ClrBear4P))
    ObjectSetInteger(0, name2, OBJPROP_COLOR, (ClrBull4P if bullish else ClrBear4P))
    ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name0, OBJPROP_WIDTH, l_width4p)
    ObjectSetInteger(0, name1, OBJPROP_WIDTH, l_width4p)
    ObjectSetInteger(0, name2, OBJPROP_WIDTH, l_width4p)
    ObjectSetInteger(0, name0, OBJPROP_STYLE, Style_4P)
    ObjectSetInteger(0, name1, OBJPROP_STYLE, Style_4P)
    ObjectSetInteger(0, name2, OBJPROP_STYLE, Style_4P)
    ObjectSetString(0, name0, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' AB')
    ObjectSetString(0, name1, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BC')
    ObjectSetString(0, name2, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' CD')
    if Show_descriptions:
        numOverlapping = 0
        for i in range(0, 66):
            for j in range(0, 10):
                if ADateTime == _patternX[i][j]:
                    numOverlapping += 1
                if Is4PointPattern(i) and ADateTime == _patternA[i][j]:
                    numOverlapping += 1
        i = 0
        while i < _patternInstanceCounter:
            instance = _copy(_patternInstances[i])
            patternIndexActive = _patternInstances[i].patternIndex
            XDateTimeActive = instance.XDateTime
            ADateTimeActive = instance.ADateTime
            if ADateTime == XDateTimeActive:
                numOverlapping += 1
            if Is4PointPattern(patternIndexActive) and ADateTime == ADateTimeActive:
                numOverlapping += 1
            i += 1
        x1 = Box(0)
        y1 = Box(0)
        x2 = Box(0)
        y2 = Box(0)
        ChartTimePriceToXY(0, 0, ADateTime, A, x1, y1)
        ChartTimePriceToXY(0, 0, ADateTime, A + 1, x2, y2)
        pixelsPerPrice = MathAbs(y1.v - y2.v)
        change = (_fdiv(numOverlapping * Font_size, pixelsPerPrice) if (pixelsPerPrice != 0) else 0)
        price = ((A + change) if bullish else (A - change))
        ObjectCreate(0, pointA, OBJ_TEXT, 0, ADateTime, price)
        ObjectCreate(0, pointB, OBJ_TEXT, 0, BDateTime, B)
        ObjectCreate(0, pointC, OBJ_TEXT, 0, CDateTime, C)
        ObjectCreate(0, pointD, OBJ_TEXT, 0, DDateTime, D)
        ObjectSetString(0, pointA, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PA')
        ObjectSetString(0, pointB, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PB')
        ObjectSetString(0, pointC, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PC')
        ObjectSetString(0, pointD, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PD')
        ObjectSetString(0, pointA, OBJPROP_TEXT, 'A ' + prefix + _patternNames[k])
        ObjectSetString(0, pointA, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointA, OBJPROP_FONTSIZE, 8)
        ObjectSetInteger(0, pointA, OBJPROP_COLOR, (ClrBull4P if bullish else ClrBear4P))
        ObjectSetString(0, pointB, OBJPROP_TEXT, 'B')
        ObjectSetString(0, pointB, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointB, OBJPROP_FONTSIZE, 8)
        ObjectSetInteger(0, pointB, OBJPROP_COLOR, (ClrBull4P if bullish else ClrBear4P))
        ObjectSetString(0, pointC, OBJPROP_TEXT, 'C')
        ObjectSetString(0, pointC, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointC, OBJPROP_FONTSIZE, 8)
        ObjectSetInteger(0, pointC, OBJPROP_COLOR, (ClrBull4P if bullish else ClrBear4P))
        ObjectSetString(0, pointD, OBJPROP_TEXT, 'D')
        ObjectSetString(0, pointD, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointD, OBJPROP_FONTSIZE, 8)
        ObjectSetInteger(0, pointD, OBJPROP_COLOR, (ClrBull4P if bullish else ClrBear4P))
    if showPatternNames:
        ShowComment(prefix + _patternNames[k] + ' @ ' + TimeToString(DDateTime))

def DisplayPattern_2(k, bullish, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
    unique = UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime)
    prefix = ('Bullish ' if bullish else 'Bearish ')
    prefixName = (('U ' + _identifier) if bullish else ('D ' + _identifier))
    name0 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XA' + unique
    name1 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' AB' + unique
    name2 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BC' + unique
    name3 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' CD' + unique
    name4 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XAB' + unique
    name5 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XAD' + unique
    name6 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' ABC' + unique
    name7 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BCD' + unique
    triangle_XB = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XB' + unique
    triangle_BD = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BD' + unique
    pointX = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PX' + unique
    pointA = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PA' + unique
    pointB = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PB' + unique
    pointC = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PC' + unique
    pointD = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PD' + unique
    xab = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(A - B), MathAbs(X - A)))))
    xad = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(D - A), MathAbs(X - A)))))
    abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - B), MathAbs(B - A)))))
    if (k == CYPHER or k == NENSTAR) or k == NEWCYPHER:
        abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(X - C), MathAbs(X - A)))))
    bcd = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - D), MathAbs(B - C)))))
    ObjectCreate(0, name0, OBJ_TREND, 0, XDateTime, X, ADateTime, A)
    ObjectCreate(0, name1, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
    ObjectCreate(0, name2, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
    ObjectCreate(0, name3, (OBJ_ARROWED_LINE if (((not Fill_Patterns) or k == THREEDRIVES) or k == FIVEO) else OBJ_TREND), 0, CDateTime, C, DDateTime, D)
    ObjectCreate(0, name4, OBJ_TREND, 0, XDateTime, X, BDateTime, B)
    if Show_descriptions:
        numOverlapping = 0
        for i in range(0, 66):
            for j in range(0, 10):
                if XDateTime == _patternX[i][j]:
                    numOverlapping += 1
                if Is4PointPattern(i) and XDateTime == _patternA[i][j]:
                    numOverlapping += 1
        i = 0
        while i < _patternInstanceCounter:
            instance = _copy(_patternInstances[i])
            patternIndexActive = _patternInstances[i].patternIndex
            XDateTimeActive = instance.XDateTime
            ADateTimeActive = instance.ADateTime
            if XDateTime == XDateTimeActive:
                numOverlapping += 1
            if Is4PointPattern(patternIndexActive) and XDateTime == ADateTimeActive:
                numOverlapping += 1
            i += 1
        x1 = Box(0)
        y1 = Box(0)
        x2 = Box(0)
        y2 = Box(0)
        ChartTimePriceToXY(0, 0, XDateTime, X, x1, y1)
        ChartTimePriceToXY(0, 0, XDateTime, X + 1, x2, y2)
        pixelsPerPrice = MathAbs(y1.v - y2.v)
        change = (_fdiv(numOverlapping * Font_size, pixelsPerPrice) if (pixelsPerPrice != 0) else 0)
        price = ((X - change) if bullish else (X + change))
        ObjectCreate(0, pointX, OBJ_TEXT, 0, XDateTime, price)
        ObjectCreate(0, pointA, OBJ_TEXT, 0, ADateTime, A)
        ObjectCreate(0, pointB, OBJ_TEXT, 0, BDateTime, B)
        ObjectCreate(0, pointC, OBJ_TEXT, 0, CDateTime, C)
        ObjectCreate(0, pointD, OBJ_TEXT, 0, DDateTime, D)
        ObjectSetString(0, pointX, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PX')
        ObjectSetString(0, pointA, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PA')
        ObjectSetString(0, pointB, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PB')
        ObjectSetString(0, pointC, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PC')
        ObjectSetString(0, pointD, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PD')
        ObjectSetString(0, pointX, OBJPROP_TEXT, 'X ' + prefix + _patternNames[k])
        ObjectSetString(0, pointX, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointX, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointX, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
        ObjectSetString(0, pointA, OBJPROP_TEXT, 'A')
        ObjectSetString(0, pointA, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointA, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointA, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
        ObjectSetString(0, pointB, OBJPROP_TEXT, 'B')
        ObjectSetString(0, pointB, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointB, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointB, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
        ObjectSetString(0, pointC, OBJPROP_TEXT, 'C')
        ObjectSetString(0, pointC, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointC, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointC, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
        ObjectSetString(0, pointD, OBJPROP_TEXT, 'D')
        ObjectSetString(0, pointD, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointD, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointD, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    if k != FIVEO:
        ObjectCreate(0, name5, OBJ_TREND, 0, XDateTime, X, DDateTime, D)
    ObjectCreate(0, name6, OBJ_TREND, 0, ADateTime, A, CDateTime, C)
    ObjectCreate(0, name7, OBJ_TREND, 0, BDateTime, B, DDateTime, D)
    ObjectSetInteger(0, name0, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name1, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name2, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name3, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name0, OBJPROP_STYLE, Style_5P)
    ObjectSetInteger(0, name1, OBJPROP_STYLE, Style_5P)
    ObjectSetInteger(0, name3, OBJPROP_STYLE, Style_5P)
    ObjectSetInteger(0, name4, OBJPROP_COLOR, ClrRatio)
    if k != FIVEO:
        ObjectSetInteger(0, name5, OBJPROP_COLOR, ClrRatio)
    ObjectSetInteger(0, name6, OBJPROP_COLOR, ClrRatio)
    ObjectSetInteger(0, name7, OBJPROP_COLOR, ClrRatio)
    ObjectSetInteger(0, name4, OBJPROP_STYLE, Style_Ratio)
    if k != FIVEO:
        ObjectSetInteger(0, name5, OBJPROP_STYLE, Style_Ratio)
    ObjectSetInteger(0, name6, OBJPROP_STYLE, Style_Ratio)
    ObjectSetInteger(0, name7, OBJPROP_STYLE, Style_Ratio)
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
    if k != FIVEO:
        ObjectSetString(0, name5, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XAD=' + xad)
    ObjectSetString(0, name6, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' ABC=' + abc)
    ObjectSetString(0, name7, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BCD=' + bcd)
    ObjectSetInteger(0, name0, OBJPROP_WIDTH, l_width)
    ObjectSetInteger(0, name1, OBJPROP_WIDTH, l_width)
    ObjectSetInteger(0, name2, OBJPROP_WIDTH, l_width)
    ObjectSetInteger(0, name3, OBJPROP_WIDTH, l_width)
    if Fill_Patterns and (k != FIVEO and k != THREEDRIVES):
        ObjectCreate(0, triangle_XB, OBJ_TRIANGLE, 0, XDateTime, X, ADateTime, A, BDateTime, B)
        ObjectCreate(0, triangle_BD, OBJ_TRIANGLE, 0, BDateTime, B, CDateTime, C, DDateTime, D)
        ObjectSetInteger(0, triangle_XB, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
        ObjectSetInteger(0, triangle_XB, OBJPROP_STYLE, STYLE_SOLID)
        ObjectSetInteger(0, triangle_XB, OBJPROP_FILL, True)
        ObjectSetInteger(0, triangle_XB, OBJPROP_BACK, True)
        ObjectSetInteger(0, triangle_XB, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, triangle_XB, OBJPROP_SELECTED, False)
        ObjectSetInteger(0, triangle_BD, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
        ObjectSetInteger(0, triangle_BD, OBJPROP_STYLE, STYLE_SOLID)
        ObjectSetInteger(0, triangle_BD, OBJPROP_FILL, True)
        ObjectSetInteger(0, triangle_BD, OBJPROP_BACK, True)
        ObjectSetInteger(0, triangle_BD, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, triangle_BD, OBJPROP_SELECTED, False)
    if showPatternNames:
        ShowComment(prefix + _patternNames[k] + ' @ ' + TimeToString(DDateTime))

def DisplayProjection_1(k, bullish, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
    unique = UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime)
    prefix = ('Projected Bullish ' if bullish else 'Projected Bearish ')
    prefixName = (('PU ' + _identifier) if bullish else ('PD ' + _identifier))
    name0 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' AB' + unique
    name1 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BC' + unique
    name2 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' CD' + unique
    pointA = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PA' + unique
    pointB = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PB' + unique
    pointC = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PC' + unique
    pointD = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PD' + unique
    ObjectCreate(0, name0, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
    ObjectCreate(0, name1, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
    ObjectCreate(0, name2, OBJ_TREND, 0, CDateTime, C, DDateTime, D)
    ObjectSetInteger(0, name0, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name1, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name2, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)
    ObjectSetString(0, name0, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' AB')
    ObjectSetString(0, name1, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BC')
    ObjectSetString(0, name2, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' CD')
    ObjectSetInteger(0, name0, OBJPROP_WIDTH, l_width_proj)
    ObjectSetInteger(0, name1, OBJPROP_WIDTH, l_width_proj)
    ObjectSetInteger(0, name2, OBJPROP_WIDTH, l_width_proj)
    ObjectSetInteger(0, name0, OBJPROP_STYLE, Style_Proj)
    ObjectSetInteger(0, name1, OBJPROP_STYLE, Style_Proj)
    ObjectSetInteger(0, name2, OBJPROP_STYLE, Style_Proj)
    if Show_descriptions:
        ObjectCreate(0, pointA, OBJ_TEXT, 0, ADateTime, A)
        ObjectCreate(0, pointB, OBJ_TEXT, 0, BDateTime, B)
        ObjectCreate(0, pointC, OBJ_TEXT, 0, CDateTime, C)
        ObjectCreate(0, pointD, OBJ_TEXT, 0, DDateTime, D)
        ObjectSetString(0, pointA, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PA')
        ObjectSetString(0, pointB, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PB')
        ObjectSetString(0, pointC, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PC')
        ObjectSetString(0, pointD, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PD')
        ObjectSetString(0, pointA, OBJPROP_TEXT, 'A')
        ObjectSetString(0, pointA, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointA, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointA, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
        ObjectSetString(0, pointB, OBJPROP_TEXT, 'B')
        ObjectSetString(0, pointB, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointB, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointB, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
        ObjectSetString(0, pointC, OBJPROP_TEXT, 'C')
        ObjectSetString(0, pointC, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointC, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointC, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
        ObjectSetString(0, pointD, OBJPROP_TEXT, ' D ' + prefix + _patternNames[k])
        ObjectSetString(0, pointD, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointD, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointD, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))

def DisplayProjection_2(k, bullish, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
    unique = UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime)
    prefix = ('Projected Bullish ' if bullish else 'Projected Bearish ')
    prefixName = (('PU ' + _identifier) if bullish else ('PD ' + _identifier))
    name0 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XA' + unique
    name1 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' AB' + unique
    name2 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BC' + unique
    name3 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' CD' + unique
    name4 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XAB' + unique
    name5 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XAD' + unique
    name6 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' ABC' + unique
    name7 = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BCD' + unique
    pointX = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PX' + unique
    pointA = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PA' + unique
    pointB = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PB' + unique
    pointC = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PC' + unique
    pointD = prefixName + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PD' + unique
    xab = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(A - B), MathAbs(X - A)))))
    xad = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(D - A), MathAbs(X - A)))))
    abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - B), MathAbs(B - A)))))
    if (k == CYPHER or k == NENSTAR) or k == NEWCYPHER:
        abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(X - C), MathAbs(X - A)))))
    bcd = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - D), MathAbs(B - C)))))
    ObjectCreate(0, name0, OBJ_TREND, 0, XDateTime, X, ADateTime, A)
    ObjectCreate(0, name1, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
    ObjectCreate(0, name2, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
    ObjectCreate(0, name3, OBJ_TREND, 0, CDateTime, C, DDateTime, D)
    ObjectCreate(0, name4, OBJ_TREND, 0, XDateTime, X, BDateTime, B)
    if k != FIVEO:
        ObjectCreate(0, name5, OBJ_TREND, 0, XDateTime, X, DDateTime, D)
    ObjectCreate(0, name6, OBJ_TREND, 0, ADateTime, A, CDateTime, C)
    ObjectCreate(0, name7, OBJ_TREND, 0, BDateTime, B, DDateTime, D)
    ObjectSetInteger(0, name0, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name1, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name2, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name3, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name4, OBJPROP_COLOR, ClrRatio)
    if k != FIVEO:
        ObjectSetInteger(0, name5, OBJPROP_COLOR, ClrRatio)
    ObjectSetInteger(0, name6, OBJPROP_COLOR, ClrRatio)
    ObjectSetInteger(0, name7, OBJPROP_COLOR, ClrRatio)
    ObjectSetInteger(0, name0, OBJPROP_STYLE, Style_Proj)
    ObjectSetInteger(0, name1, OBJPROP_STYLE, Style_Proj)
    ObjectSetInteger(0, name2, OBJPROP_STYLE, Style_Proj)
    ObjectSetInteger(0, name3, OBJPROP_STYLE, Style_Proj)
    ObjectSetInteger(0, name4, OBJPROP_STYLE, Style_Ratio)
    ObjectSetInteger(0, name5, OBJPROP_STYLE, Style_Ratio)
    ObjectSetInteger(0, name6, OBJPROP_STYLE, Style_Ratio)
    ObjectSetInteger(0, name7, OBJPROP_STYLE, Style_Ratio)
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
    if k != FIVEO:
        ObjectSetString(0, name5, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' XAD=' + xad)
    ObjectSetString(0, name6, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' ABC=' + abc)
    ObjectSetString(0, name7, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' BCD=' + bcd)
    if Show_descriptions:
        ObjectCreate(0, pointX, OBJ_TEXT, 0, XDateTime, X)
        ObjectCreate(0, pointA, OBJ_TEXT, 0, ADateTime, A)
        ObjectCreate(0, pointB, OBJ_TEXT, 0, BDateTime, B)
        ObjectCreate(0, pointC, OBJ_TEXT, 0, CDateTime, C)
        ObjectCreate(0, pointD, OBJ_TEXT, 0, DDateTime, D)
        ObjectSetString(0, pointX, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PX')
        ObjectSetString(0, pointA, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PA')
        ObjectSetString(0, pointB, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PB')
        ObjectSetString(0, pointC, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PC')
        ObjectSetString(0, pointD, OBJPROP_TOOLTIP, prefix + _patternNames[k] + ' PD')
        ObjectSetInteger(0, name0, OBJPROP_WIDTH, l_width_proj)
        ObjectSetInteger(0, name1, OBJPROP_WIDTH, l_width_proj)
        ObjectSetInteger(0, name2, OBJPROP_WIDTH, l_width_proj)
        ObjectSetInteger(0, name3, OBJPROP_WIDTH, l_width_proj)
        ObjectSetString(0, pointX, OBJPROP_TEXT, 'X')
        ObjectSetString(0, pointX, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointX, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointX, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
        ObjectSetString(0, pointA, OBJPROP_TEXT, 'A')
        ObjectSetString(0, pointA, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointA, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointA, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
        ObjectSetString(0, pointB, OBJPROP_TEXT, 'B')
        ObjectSetString(0, pointB, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointB, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointB, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
        ObjectSetString(0, pointC, OBJPROP_TEXT, 'C')
        ObjectSetString(0, pointC, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointC, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointC, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
        ObjectSetString(0, pointD, OBJPROP_TEXT, ' D ' + prefix + _patternNames[k])
        ObjectSetString(0, pointD, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, pointD, OBJPROP_FONTSIZE, Font_size)
        ObjectSetInteger(0, pointD, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))

def UndisplayProjections():
    global _drawnProjectionInstanceCounter
    i = 0
    while i < _drawnProjectionInstanceCounter:
        instance = _copy(_drawnProjectionInstances[i])
        k = instance.patternIndex
        bullish = instance.bullish
        XDateTime = instance.XDateTime
        ADateTime = instance.ADateTime
        BDateTime = instance.BDateTime
        CDateTime = instance.CDateTime
        DDateTime = instance.DDateTime
        unique = (UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime) if Is4PointPattern(k) else UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime))
        prefix = (('PU ' + _identifier) if bullish else ('PD ' + _identifier))
        name0 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XA' + unique
        name1 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' AB' + unique
        name2 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BC' + unique
        name3 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' CD' + unique
        name4 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XAB' + unique
        name5 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' XAD' + unique
        name6 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' ABC' + unique
        name7 = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' BCD' + unique
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
        ObjectDelete(0, pointX)
        ObjectDelete(0, pointA)
        ObjectDelete(0, pointB)
        ObjectDelete(0, pointC)
        ObjectDelete(0, pointD)
        i += 1
    _drawnProjectionInstanceCounter = 0

def UndisplayPatterns():
    i = 0
    while i < _patternInstanceCounter:
        instance = _copy(_patternInstances[i])
        k = instance.patternIndex
        bullish = instance.bullish
        XDateTime = instance.XDateTime
        ADateTime = instance.ADateTime
        BDateTime = instance.BDateTime
        CDateTime = instance.CDateTime
        DDateTime = instance.DDateTime
        unique = (UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime) if Is4PointPattern(k) else UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime))
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
        i += 1

def UndisplayPRZs():
    i = 0
    while i < _patternInstanceCounter:
        instance = _copy(_patternInstances[i])
        k = instance.patternIndex
        bullish = instance.bullish
        XDateTime = instance.XDateTime
        ADateTime = instance.ADateTime
        BDateTime = instance.BDateTime
        CDateTime = instance.CDateTime
        DDateTime = instance.DDateTime
        unique = (UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime) if Is4PointPattern(k) else UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime))
        prefix = (('U ' + _identifier) if bullish else ('D ' + _identifier))
        linePRZ = prefix + StringFormat('%x', _timeOfInit) + IntegerToString(k) + ' PRZ' + unique
        ObjectDelete(0, linePRZ)
        i += 1

def PopulatePatterns():
    global _maxDrawnProjectionInstances, _maxPatternInstances, _maxProjectionInstances
    trendlike1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.382, 0.382, 2.618, 2.618, 0, 0, 0, 0, 0, 0, 0, 0])
    trendlike2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.5, 0.5, 2.0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0])
    perfect_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.618, 0.618, 1.618, 1.618, 0, 0, 0, 0, 0, 0, 0, 0])
    ideal1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.707, 0.707, 1.41, 1.41, 0, 0, 0, 0, 0, 0, 0, 0])
    ideal2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.786, 0.786, 1.27, 1.27, 0, 0, 0, 0, 0, 0, 0, 0])
    rangelike_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.886, 0.886, 1.13, 1.13, 0, 0, 0, 0, 0, 0, 0, 0])
    alt127_trendlike1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.382, 0.382, 2.618, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_trendlike2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.5, 0.5, 2.0, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_perfect_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.618, 0.618, 1.618, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_ideal1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.707, 0.707, 1.41, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_ideal2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.786, 0.786, 1.27, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    alt127_rangelike_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.886, 0.886, 1.13, 3.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272])
    rec_trendlike1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 2.618, 2.618, 0.382, 0.382, 0, 0, 0, 0, 0, 0, 0, 0])
    rec_trendlike2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 2.0, 2.0, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0])
    rec_perfect_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.618, 1.618, 0.618, 0.618, 0, 0, 0, 0, 0, 0, 0, 0])
    rec_ideal1_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.41, 1.41, 0.707, 0.707, 0, 0, 0, 0, 0, 0, 0, 0])
    rec_ideal2_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.27, 1.27, 0.786, 0.786, 0, 0, 0, 0, 0, 0, 0, 0])
    rec_rangelike_abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.13, 1.13, 0.886, 0.886, 0, 0, 0, 0, 0, 0, 0, 0])
    gartley = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.618, 0.382, 0.886, 1.272, 1.618, 0.786, 0.786, 0, 0, 0, 0, 0, 0])
    bat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.5, 0.382, 0.886, 1.618, 2.618, 0.886, 0.886, 0, 0, 0, 0, 0, 0])
    altbat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.382, 0.382, 0.886, 2.0, 3.618, 1.13, 1.13, 0, 0, 0, 0, 0, 0])
    fiveo = _struct_init(PATTERN_DESCRIPTOR(), [1.13, 1.618, 1.618, 2.24, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0])
    butterfly = _struct_init(PATTERN_DESCRIPTOR(), [0.786, 0.786, 0.382, 0.886, 1.618, 2.618, 1.272, 1.618, 0, 0, 0, 0, 0, 0])
    crab = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0.382, 0.886, 2.24, 3.618, 1.618, 1.618, 0, 0, 0, 0, 0, 0])
    deepcrab = _struct_init(PATTERN_DESCRIPTOR(), [0.886, 0.886, 0.382, 0.886, 2.0, 3.618, 1.618, 1.618, 0, 0, 0, 0, 0, 0])
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
    maxbat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0.382, 0.886, 1.272, 2.618, 0.886, 0.886, 0, 0, 0, 0, 0, 0])
    maxgartley = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0.382, 0.886, 1.128, 2.236, 0.618, 0.786, 0, 0, 0, 0, 0, 0])
    maxbutterfly = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.886, 0.382, 0.886, 1.272, 2.618, 1.272, 1.618, 0, 0, 0, 0, 0, 0])
    gartley113 = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.618, 0.382, 0.886, 1.13, 1.13, 0.786, 0.786, 0, 0, 0, 0, 0, 0])
    butterfly113 = _struct_init(PATTERN_DESCRIPTOR(), [0.786, 1, 0.618, 1, 1.128, 1.618, 1.128, 1.128, 0, 0, 0, 0, 0, 0])
    anti_gartley = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.786, 1.129, 2.618, 1.618, 1.618, 1.272, 1.272, 0, 0, 0, 0, 0, 0])
    anti_bat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 1.129, 2.618, 2.0, 2.618, 1.129, 1.129, 0, 0, 0, 0, 0, 0])
    anti_altbat = _struct_init(PATTERN_DESCRIPTOR(), [0.276, 0.5, 1.129, 2.618, 2.618, 2.618, 0.885, 0.885, 0, 0, 0, 0, 0, 0])
    anti_fiveo = _struct_init(PATTERN_DESCRIPTOR(), [2.0, 2.0, 0.446, 0.618, 0.618, 0.885, 0, 0, 0, 0, 0, 0, 0, 0])
    anti_butterfly = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 1.129, 2.618, 1.272, 1.272, 0.618, 0.786, 0, 0, 0, 0, 0, 0])
    anti_crab = _struct_init(PATTERN_DESCRIPTOR(), [0.276, 0.446, 1.129, 2.618, 1.618, 2.618, 0.618, 0.618, 0, 0, 0, 0, 0, 0])
    anti_deepcrab = _struct_init(PATTERN_DESCRIPTOR(), [0.276, 0.5, 1.129, 2.618, 1.129, 1.129, 0.618, 0.618, 0, 0, 0, 0, 0, 0])
    anti_threedrives = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.786, 1.272, 1.618, 0.618, 0.786, 0, 0, 0, 0, 0, 0, 0, 0])
    anti_shark = _struct_init(PATTERN_DESCRIPTOR(), [0.446, 0.618, 0.618, 0.885, 0, 0, 0, 0, 0.885, 1.129, 0, 0, 0, 0])
    anti_cypher = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0, 0, 1.618, 2.618, 0, 0, 1.272, 1.272, 0.707, 0.885, 0, 0])
    anti_nenstar = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0, 0, 1.618, 2.618, 0, 0, 0.786, 0.786, 0.707, 0.885, 0, 0])
    anti_blackswan = _struct_init(PATTERN_DESCRIPTOR(), [0.5, 0.887, 2.0, 4.237, 0.382, 0.724, 0.382, 0.887, 0, 0, 0, 0, 0, 0])
    anti_whiteswan = _struct_init(PATTERN_DESCRIPTOR(), [1.129, 2.0, 0.236, 0.5, 1.381, 2.618, 1.129, 2.618, 0, 0, 0, 0, 0, 0])
    anti_one2one = _struct_init(PATTERN_DESCRIPTOR(), [1.272, 2.618, 0.276, 0.887, 1.272, 2.0, 1.272, 2.618, 0, 0, 0, 0, 0, 0])
    anti_newcypher = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0, 0, 1.618, 2.618, 0, 0, 1.272, 1.272, 0.467, 0.707, 0, 0])
    anti_navarro200 = _struct_init(PATTERN_DESCRIPTOR(), [0.276, 1.129, 0.887, 1.129, 1.272, 2.618, 0.887, 1.129, 0, 0, 0, 0, 0, 0])
    anti_leonardo = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.887, 1.129, 2.618, 2.0, 2.0, 1.272, 1.272, 0, 0, 0, 0, 0, 0])
    anti_kane = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.129, 2.618, 1.46, 1.46, 0.685, 0.685, 0, 0, 0, 0, 0, 0])
    anti_garfly = _struct_init(PATTERN_DESCRIPTOR(), [0.446, 0.618, 1.129, 2.618, 1.618, 1.618, 0.786, 0.786, 0, 0, 0, 0, 0, 0])
    anti_maxbat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.786, 1.129, 2.618, 1.618, 2.618, 1.129, 1.129, 0, 0, 0, 0, 0, 0])
    anti_maxgartley = _struct_init(PATTERN_DESCRIPTOR(), [0.447, 0.887, 1.129, 2.618, 1.618, 2.618, 1.272, 1.618, 0, 0, 0, 0, 0, 0])
    anti_maxbutterfly = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.786, 1.129, 2.618, 1.129, 1.618, 0.618, 0.786, 0, 0, 0, 0, 0, 0])
    anti_gartley113 = _struct_init(PATTERN_DESCRIPTOR(), [0.885, 0.885, 1.129, 2.618, 1.618, 1.618, 1.272, 1.272, 0, 0, 0, 0, 0, 0])
    anti_butterfly113 = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.887, 1.0, 1.618, 1.0, 1.272, 0.887, 0.887, 0, 0, 0, 0, 0, 0])
    _maxProjectionInstances = 4
    _maxPatternInstances = 66 * 10
    _maxDrawnProjectionInstances = 4
    if ArrayResize(_patterns, 66) < 66:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_patternNames, 66) < 66:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_patternX, 66) < 66:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_patternA, 66) < 66:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_patternB, 66) < 66:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_patternC, 66) < 66:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_patternD, 66) < 66:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_patternCounter, 66) < 66:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_patternInstances, _maxPatternInstances) < _maxPatternInstances:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_projectionInstances, _maxProjectionInstances) < _maxProjectionInstances:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    if ArrayResize(_drawnProjectionInstances, _maxDrawnProjectionInstances) < _maxDrawnProjectionInstances:
        printf('Error allocating array: ' + IntegerToString(GetLastError()))
        return INIT_FAILED
    ArrayFill(_patternCounter, 0, 66, 0)
    _assign(_patterns[TRENDLIKE1_ABCD], trendlike1_abcd)
    _patternNames[TRENDLIKE1_ABCD] = 'Trendlike AB=CD #1'
    _assign(_patterns[TRENDLIKE2_ABCD], trendlike2_abcd)
    _patternNames[TRENDLIKE2_ABCD] = 'Trendlike AB=CD #2'
    _assign(_patterns[PERFECT_ABCD], perfect_abcd)
    _patternNames[PERFECT_ABCD] = 'Perfect AB=CD'
    _assign(_patterns[IDEAL1_ABCD], ideal1_abcd)
    _patternNames[IDEAL1_ABCD] = 'Ideal AB=CD #1'
    _assign(_patterns[IDEAL2_ABCD], ideal2_abcd)
    _patternNames[IDEAL2_ABCD] = 'Ideal AB=CD #2'
    _assign(_patterns[RANGELIKE_ABCD], rangelike_abcd)
    _patternNames[RANGELIKE_ABCD] = 'Rangelike AB=CD'
    _assign(_patterns[ALT127_TRENDLIKE1_ABCD], alt127_trendlike1_abcd)
    _patternNames[ALT127_TRENDLIKE1_ABCD] = 'Trendlike 1.27 AB=CD #1'
    _assign(_patterns[ALT127_TRENDLIKE2_ABCD], alt127_trendlike2_abcd)
    _patternNames[ALT127_TRENDLIKE2_ABCD] = 'Trendlike 1.27 AB=CD #2'
    _assign(_patterns[ALT127_PERFECT_ABCD], alt127_perfect_abcd)
    _patternNames[ALT127_PERFECT_ABCD] = 'Perfect 1.27 AB=CD'
    _assign(_patterns[ALT127_IDEAL1_ABCD], alt127_ideal1_abcd)
    _patternNames[ALT127_IDEAL1_ABCD] = 'Ideal 1.27 AB=CD #1'
    _assign(_patterns[ALT127_IDEAL2_ABCD], alt127_ideal2_abcd)
    _patternNames[ALT127_IDEAL2_ABCD] = 'Ideal 1.27 AB=CD #2'
    _assign(_patterns[ALT127_RANGELIKE_ABCD], alt127_rangelike_abcd)
    _patternNames[ALT127_RANGELIKE_ABCD] = 'Rangelike 1.27 AB=CD'
    _assign(_patterns[REC_TRENDLIKE1_ABCD], rec_trendlike1_abcd)
    _patternNames[REC_TRENDLIKE1_ABCD] = 'Rec. Trendlike AB=CD #1'
    _assign(_patterns[REC_TRENDLIKE2_ABCD], rec_trendlike2_abcd)
    _patternNames[REC_TRENDLIKE2_ABCD] = 'Rec. Trendlike AB=CD #2'
    _assign(_patterns[REC_PERFECT_ABCD], rec_perfect_abcd)
    _patternNames[REC_PERFECT_ABCD] = 'Rec. Perfect AB=CD'
    _assign(_patterns[REC_IDEAL1_ABCD], rec_ideal1_abcd)
    _patternNames[REC_IDEAL1_ABCD] = 'Rec. Ideal AB=CD #1'
    _assign(_patterns[REC_IDEAL2_ABCD], rec_ideal2_abcd)
    _patternNames[REC_IDEAL2_ABCD] = 'Rec. Ideal AB=CD #2'
    _assign(_patterns[REC_RANGELIKE_ABCD], rec_rangelike_abcd)
    _patternNames[REC_RANGELIKE_ABCD] = 'Rec. Rangelike AB=CD'
    _assign(_patterns[GARTLEY], gartley)
    _patternNames[GARTLEY] = 'Gartley'
    _assign(_patterns[BAT], bat)
    _patternNames[BAT] = 'Bat'
    _assign(_patterns[ALTBAT], altbat)
    _patternNames[ALTBAT] = 'Alt. Bat'
    _assign(_patterns[FIVEO], fiveo)
    _patternNames[FIVEO] = '5-0'
    _assign(_patterns[BUTTERFLY], butterfly)
    _patternNames[BUTTERFLY] = 'Butterfly'
    _assign(_patterns[CRAB], crab)
    _patternNames[CRAB] = 'Crab'
    _assign(_patterns[DEEPCRAB], deepcrab)
    _patternNames[DEEPCRAB] = 'Deep Crab'
    _assign(_patterns[THREEDRIVES], threedrives)
    _patternNames[THREEDRIVES] = 'Three Drives'
    _assign(_patterns[CYPHER], cypher)
    _patternNames[CYPHER] = 'Cypher'
    _assign(_patterns[SHARK], shark)
    _patternNames[SHARK] = 'Shark'
    _assign(_patterns[NENSTAR], nenstar)
    _patternNames[NENSTAR] = 'Nen Star'
    _assign(_patterns[BLACKSWAN], blackswan)
    _patternNames[BLACKSWAN] = 'Black Swan'
    _assign(_patterns[WHITESWAN], whiteswan)
    _patternNames[WHITESWAN] = 'White Swan'
    _assign(_patterns[ONE2ONE], one2one)
    _patternNames[ONE2ONE] = 'One2One'
    _assign(_patterns[NEWCYPHER], newcypher)
    _patternNames[NEWCYPHER] = 'New Cypher'
    _assign(_patterns[NAVARRO200], navarro200)
    _patternNames[NAVARRO200] = 'Navarro 200'
    _assign(_patterns[LEONARDO], leonardo)
    _patternNames[LEONARDO] = 'Leonardo'
    _assign(_patterns[KANE], kane)
    _patternNames[KANE] = 'Kane'
    _assign(_patterns[GARFLY], garfly)
    _patternNames[GARFLY] = 'Garfly'
    _assign(_patterns[MAXBAT], maxbat)
    _patternNames[MAXBAT] = 'Max. Bat'
    _assign(_patterns[MAXGARTLEY], maxgartley)
    _patternNames[MAXGARTLEY] = 'Max. Gartley'
    _assign(_patterns[MAXBUTTERFLY], maxbutterfly)
    _patternNames[MAXBUTTERFLY] = 'Max. Butterfly'
    _assign(_patterns[GARTLEY113], gartley113)
    _patternNames[GARTLEY113] = 'Gartley 113'
    _assign(_patterns[BUTTERFLY113], butterfly113)
    _patternNames[BUTTERFLY113] = 'Butterfly 113'
    _assign(_patterns[ANTI_GARTLEY], anti_gartley)
    _patternNames[ANTI_GARTLEY] = 'Anti Gartley'
    _assign(_patterns[ANTI_BAT], anti_bat)
    _patternNames[ANTI_BAT] = 'Anti Bat'
    _assign(_patterns[ANTI_ALTBAT], anti_altbat)
    _patternNames[ANTI_ALTBAT] = 'Anti Alt. Bat'
    _assign(_patterns[ANTI_FIVEO], anti_fiveo)
    _patternNames[ANTI_FIVEO] = 'Anti 5-0'
    _assign(_patterns[ANTI_BUTTERFLY], anti_butterfly)
    _patternNames[ANTI_BUTTERFLY] = 'Anti Butterfly'
    _assign(_patterns[ANTI_CRAB], anti_crab)
    _patternNames[ANTI_CRAB] = 'Anti Crab'
    _assign(_patterns[ANTI_DEEPCRAB], anti_deepcrab)
    _patternNames[ANTI_DEEPCRAB] = 'Anti Deep Crab'
    _assign(_patterns[ANTI_THREEDRIVES], anti_threedrives)
    _patternNames[ANTI_THREEDRIVES] = 'Anti Three Drives'
    _assign(_patterns[ANTI_CYPHER], anti_cypher)
    _patternNames[ANTI_CYPHER] = 'Anti Cypher'
    _assign(_patterns[ANTI_SHARK], anti_shark)
    _patternNames[ANTI_SHARK] = 'Anti Shark'
    _assign(_patterns[ANTI_NENSTAR], anti_nenstar)
    _patternNames[ANTI_NENSTAR] = 'Anti Nen Star'
    _assign(_patterns[ANTI_BLACKSWAN], anti_blackswan)
    _patternNames[ANTI_BLACKSWAN] = 'Anti Black Swan'
    _assign(_patterns[ANTI_WHITESWAN], anti_whiteswan)
    _patternNames[ANTI_WHITESWAN] = 'Anti White Swan'
    _assign(_patterns[ANTI_ONE2ONE], anti_one2one)
    _patternNames[ANTI_ONE2ONE] = 'Anti One2One'
    _assign(_patterns[ANTI_NEWCYPHER], anti_newcypher)
    _patternNames[ANTI_NEWCYPHER] = 'Anti New Cypher'
    _assign(_patterns[ANTI_NAVARRO200], anti_navarro200)
    _patternNames[ANTI_NAVARRO200] = 'Anti Navarro 200'
    _assign(_patterns[ANTI_LEONARDO], anti_leonardo)
    _patternNames[ANTI_LEONARDO] = 'Anti Leonardo'
    _assign(_patterns[ANTI_KANE], anti_kane)
    _patternNames[ANTI_KANE] = 'Anti Kane'
    _assign(_patterns[ANTI_GARFLY], anti_garfly)
    _patternNames[ANTI_GARFLY] = 'Anti Garfly'
    _assign(_patterns[ANTI_MAXBAT], anti_maxbat)
    _patternNames[ANTI_MAXBAT] = 'Anti Max. Bat'
    _assign(_patterns[ANTI_MAXGARTLEY], anti_maxgartley)
    _patternNames[ANTI_MAXGARTLEY] = 'Anti Max. Gartley'
    _assign(_patterns[ANTI_MAXBUTTERFLY], anti_maxbutterfly)
    _patternNames[ANTI_MAXBUTTERFLY] = 'Anti Max. Butterfly'
    _assign(_patterns[ANTI_GARTLEY113], anti_gartley113)
    _patternNames[ANTI_GARTLEY113] = 'Anti Gartley 113'
    _assign(_patterns[ANTI_BUTTERFLY113], anti_butterfly113)
    _patternNames[ANTI_BUTTERFLY113] = 'Anti Butterfly 113'
    return INIT_SUCCEEDED

def UniqueIdentifier_1(ADateTime, BDateTime, CDateTime, DDateTime):
    return ' ' + StringFormat('%x', ADateTime) + StringFormat('%x', BDateTime) + StringFormat('%x', CDateTime) + StringFormat('%x', DDateTime)

def UniqueIdentifier_2(XDateTime, ADateTime, BDateTime, CDateTime, DDateTime):
    return ' ' + StringFormat('%x', XDateTime) + StringFormat('%x', ADateTime) + StringFormat('%x', BDateTime) + StringFormat('%x', CDateTime) + StringFormat('%x', DDateTime)

# ---- global variables initialised from expressions
_patternInstances = Arr(0, 0, factory=PATTERN_INSTANCE)
_projectionInstances = Arr(0, 0, factory=PATTERN_INSTANCE)
_drawnProjectionInstances = Arr(0, 0, factory=PATTERN_INSTANCE)
_patterns = Arr(0, 0, factory=PATTERN_DESCRIPTOR)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HarmonicPatternFinderV2(_MQL5Indicator):
    name = 'HarmonicPatternFinderV2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'zztype': _Choice({0: 'Fast ZZ', 1: 'Alexstal ZZ', 2: 'Swing ZZ'}, default=1),  # ZigZag type
        'zzperiod': 12,  # AlexStal ZZ period
        'zzamplitude': 10,  # AlexStal ZZ amplitude
        'zzminmotion': 0,  # AlexStal ZZ minimum motion
        'SwingSize': 200,  # Fast ZZ sensitivity in points
        'BarsAnalyzed': 200,  # Max. bars per pattern
        'History': 1000,  # Max. history bars to process
        'MaxSamePoints': 2,  # Max. shared points per pattern
        'SlackRange': 0.01,  # Max. slack for fib ratios (range)
        'SlackUnary': 0.1,  # Max. slack for fib ratios (unary)
        'Fill_Patterns': False,  # Fill 5 point patterns found
        'Show_descriptions': True,  # Show pattern descriptions
        'Show_PRZ': True,  # Show potential reversal zone (PRZ)
        'EmergingPatterns': True,  # Show emerging patterns
        'OneAheadProjection': False,  # Show "one-ahead" projections
        'showPatternNames': False,  # Show comment box
        'l_width': 2,  # Pattern line width (5 points)
        'l_width4p': 2,  # Patterns line width (4 points)
        'l_width_proj': 2,  # Emerging patterns line width
        'Font_size': 8,  # Font size
        'Style_5P': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Style for 5 points patterns
        'Style_4P': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # Style for 4 points patterns
        'Style_Proj': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Style for projections
        'Style_Ratio': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Style for ratio lines
        'Style_PRZ': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=3),  # Style for PRZ
        'Show_abcd': True,  # Display AB=CD patterns
        'Show_alt127_abcd': True,  # Display 1.27 AB=CD patterns
        'Show_rec_abcd': True,  # Display Rec. AB=CD patterns
        'Show_patterns': True,  # Display normal 5-point patterns
        'Show_antipatterns': False,  # Display anti 5-point patterns
        'Show_trendlike1_abcd': True,  # Display Trendlike AB=CD #1
        'Show_trendlike2_abcd': True,  # Display Trendlike AB=CD #2
        'Show_perfect_abcd': True,  # Display Perfect AB=CD
        'Show_ideal1_abcd': True,  # Display Ideal AB=CD #1
        'Show_ideal2_abcd': True,  # Display Ideal AB=CD #2
        'Show_rangelike_abcd': True,  # Display Rangelike AB=CD
        'Show_alt127_trendlike1_abcd': True,  # Display Trendlike 1.27 AB=CD #1
        'Show_alt127_trendlike2_abcd': True,  # Display Trendlike 1.27 AB=CD #2
        'Show_alt127_perfect_abcd': True,  # Display Perfect 1.27 AB=CD
        'Show_alt127_ideal1_abcd': True,  # Display Ideal 1.27 AB=CD #1
        'Show_alt127_ideal2_abcd': True,  # Display Ideal 1.27 AB=CD #2
        'Show_alt127_rangelike_abcd': True,  # Display Rangelike 1.27 AB=CD
        'Show_rec_trendlike1_abcd': True,  # Display Rec. Trendlike AB=CD #1
        'Show_rec_trendlike2_abcd': True,  # Display Rec. Trendlike AB=CD #2
        'Show_rec_perfect_abcd': True,  # Display Rec. Perfect AB=CD
        'Show_rec_ideal1_abcd': True,  # Display Rec. Ideal AB=CD #1
        'Show_rec_ideal2_abcd': True,  # Display Rec. Ideal AB=CD #2
        'Show_rec_rangelike_abcd': True,  # Display Rec. Rangelike AB=CD
        'Show_gartley': True,  # Display Gartley
        'Show_bat': True,  # Display Bat
        'Show_altbat': True,  # Display Alt. Bat
        'Show_fiveo': True,  # Display 5-0
        'Show_butterfly': True,  # Display Butterfly
        'Show_crab': True,  # Display Crab
        'Show_deepcrab': True,  # Display Deepcrab
        'Show_threedrives': True,  # Display Three Drives
        'Show_cypher': True,  # Display Cypher
        'Show_shark': True,  # Display Shark
        'Show_nenstar': True,  # Display Nen Star
        'Show_blackswan': True,  # Display Black Swan
        'Show_whiteswan': True,  # Display White Swan
        'Show_one2one': True,  # Display One2One
        'Show_newCypher': True,  # Display New Cypher
        'Show_navarro200': True,  # Display Navarro 200
        'Show_leonardo': True,  # Display Leonardo
        'Show_kane': True,  # Display Kane
        'Show_garfly': True,  # Display Garfly
        'Show_maxbat': True,  # Display Max. Bat
        'Show_maxgartley': True,  # Display Max. Gartley
        'Show_maxbutterfly': True,  # Display Max. Butterfly
        'Show_gartley113': True,  # Display Gartley 113
        'Show_butterfly113': True,  # Display Butterfly 113
        'Show_antigartley': True,  # Display Anti Gartley
        'Show_antibat': True,  # Display Anti Bat
        'Show_antialtbat': True,  # Display Anti Alt. Bat
        'Show_antifiveo': True,  # Display Anti 5-0
        'Show_antibutterfly': True,  # Display Anti Butterfly
        'Show_anticrab': True,  # Display Anti Crab
        'Show_antideepcrab': True,  # Display Anti Deepcrab
        'Show_antithreedrives': True,  # Display Anti Three Drives
        'Show_anticypher': True,  # Display Anti Cypher
        'Show_antishark': True,  # Display Anti Shark
        'Show_antinenstar': True,  # Display Anti Nen Star
        'Show_antiblackswan': True,  # Display Anti Black Swan
        'Show_antiwhiteswan': True,  # Display Anti White Swan
        'Show_antione2one': True,  # Display Anti One2One
        'Show_antinewCypher': True,  # Display Anti New Cypher
        'Show_antinavarro200': True,  # Display Anti Navarro 200
        'Show_antileonardo': True,  # Display Anti Leonardo
        'Show_antikane': True,  # Display Anti Kane
        'Show_antigarfly': True,  # Display Anti Garfly
        'Show_antimaxbat': True,  # Display Anti Max. Bat
        'Show_antimaxgartley': True,  # Display Anti Max. Gartley
        'Show_antimaxbutterfly': True,  # Display Anti Max. Butterfly
        'Show_antigartley113': True,  # Display Anti Gartley 113
        'Show_antibutterfly113': True,  # Display Anti Butterfly 113
    }

