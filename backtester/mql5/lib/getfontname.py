"""getfontname.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *

# enum type_font
Font0 = 0
Font1 = 1
Font2 = 2
Font3 = 3
Font4 = 4
Font5 = 5
Font6 = 6
Font7 = 7
Font8 = 8
Font9 = 9
Font10 = 10
Font11 = 11
Font12 = 12
Font13 = 13
Font14 = 14
Font15 = 15
Font16 = 16
Font17 = 17
Font18 = 18
Font19 = 19
Font20 = 20
Font21 = 21
Font22 = 22
Font23 = 23
Font24 = 24
Font25 = 25
Font26 = 26
Font27 = 27
Font28 = 28
Font29 = 29
Font30 = 30
Font31 = 31
Font32 = 32
Font33 = 33
Font34 = 34
Font35 = 35
Font36 = 36
Font37 = 37
Font38 = 38
Font39 = 39
Font40 = 40
Font41 = 41
Font42 = 42
Font43 = 43
Font44 = 44
Font45 = 45
Font46 = 46
Font47 = 47
Font48 = 48
Font49 = 49
Font50 = 50
Font51 = 51
Font52 = 52
Font53 = 53
Font54 = 54
Font55 = 55
Font56 = 56
_enum('type_font', {0: 'Font0', 1: 'Font1', 2: 'Font2', 3: 'Font3', 4: 'Font4', 5: 'Font5', 6: 'Font6', 7: 'Font7', 8: 'Font8', 9: 'Font9', 10: 'Font10', 11: 'Font11', 12: 'Font12', 13: 'Font13', 14: 'Font14', 15: 'Font15', 16: 'Font16', 17: 'Font17', 18: 'Font18', 19: 'Font19', 20: 'Font20', 21: 'Font21', 22: 'Font22', 23: 'Font23', 24: 'Font24', 25: 'Font25', 26: 'Font26', 27: 'Font27', 28: 'Font28', 29: 'Font29', 30: 'Font30', 31: 'Font31', 32: 'Font32', 33: 'Font33', 34: 'Font34', 35: 'Font35', 36: 'Font36', 37: 'Font37', 38: 'Font38', 39: 'Font39', 40: 'Font40', 41: 'Font41', 42: 'Font42', 43: 'Font43', 44: 'Font44', 45: 'Font45', 46: 'Font46', 47: 'Font47', 48: 'Font48', 49: 'Font49', 50: 'Font50', 51: 'Font51', 52: 'Font52', 53: 'Font53', 54: 'Font54', 55: 'Font55', 56: 'Font56'})


class CFontName(MqlObject):
    _q_fields = ()
    def __init__(self, *args):
        pass
    def GetFontName(self, FontNumber):
        FontTypes = Arr.of(['Arial', 'Arial Black', 'Arial Bold', 'Arial Bold Italic', 'Arial Italic', 'Comic Sans MS Bold', 'Courier', 'Courier New', 'Courier New Bold', 'Courier New Bold Italic', 'Courier New Italic', 'Estrangelo Edessa', 'Franklin Gothic Medium', 'Gautami', 'Georgia', 'Georgia Bold', 'Georgia Bold Italic', 'Georgia Italic', 'Georgia Italic Impact', 'Latha', 'Lucida Console', 'Lucida Sans Unicode', 'Modern MS Sans Serif', 'MS Sans Serif', 'Mv Boli', 'Palatino Linotype', 'Palatino Linotype Bold', 'Palatino Linotype Italic', 'Roman', 'Script', 'Small Fonts', 'Symbol', 'Tahoma', 'Tahoma Bold', 'Times New Roman', 'Times New Roman Bold', 'Times New Roman Bold Italic', 'Times New Roman Italic', 'Trebuchet MS', 'Trebuchet MS Bold', 'Trebuchet MS Bold Italic', 'Trebuchet MS Italic', 'Tunga', 'Verdana', 'Verdana Bold', 'Verdana Bold Italic', 'Verdana Italic', 'Webdings', 'Westminster', 'Wingdings', 'WST_Czech', 'WST_Engl', 'WST_Fren', 'WST_Germ', 'WST_Ital', 'WST_Span', 'WST_Swed'], fill="")
        return FontTypes[FontNumber]

__all__ = ['Font0', 'Font1', 'Font2', 'Font3', 'Font4', 'Font5', 'Font6', 'Font7', 'Font8', 'Font9', 'Font10', 'Font11', 'Font12', 'Font13', 'Font14', 'Font15', 'Font16', 'Font17', 'Font18', 'Font19', 'Font20', 'Font21', 'Font22', 'Font23', 'Font24', 'Font25', 'Font26', 'Font27', 'Font28', 'Font29', 'Font30', 'Font31', 'Font32', 'Font33', 'Font34', 'Font35', 'Font36', 'Font37', 'Font38', 'Font39', 'Font40', 'Font41', 'Font42', 'Font43', 'Font44', 'Font45', 'Font46', 'Font47', 'Font48', 'Font49', 'Font50', 'Font51', 'Font52', 'Font53', 'Font54', 'Font55', 'Font56', 'CFontName']
