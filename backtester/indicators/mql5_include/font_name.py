"""``GetFontName.mqh`` (Nikolay Kositsin, 2011) — port.

The ``type_font`` input enum (``Font0`` … ``Font56``) and ``CFontName``, which
maps it to a Windows font name for the indicator's chart labels. Converted
indicators draw no text objects, so this only matters for keeping a ported
input list intact; it is used by 54 Codebase indicators.
"""

from __future__ import annotations

FONT_TYPES = (
    "Arial", "Arial Black", "Arial Bold", "Arial Bold Italic", "Arial Italic",
    "Comic Sans MS Bold", "Courier", "Courier New", "Courier New Bold",
    "Courier New Bold Italic", "Courier New Italic", "Estrangelo Edessa",
    "Franklin Gothic Medium", "Gautami", "Georgia", "Georgia Bold", "Georgia Bold Italic",
    "Georgia Italic", "Georgia Italic Impact", "Latha", "Lucida Console",
    "Lucida Sans Unicode", "Modern MS Sans Serif", "MS Sans Serif", "Mv Boli",
    "Palatino Linotype", "Palatino Linotype Bold", "Palatino Linotype Italic", "Roman",
    "Script", "Small Fonts", "Symbol", "Tahoma", "Tahoma Bold", "Times New Roman",
    "Times New Roman Bold", "Times New Roman Bold Italic", "Times New Roman Italic",
    "Trebuchet MS", "Trebuchet MS Bold", "Trebuchet MS Bold Italic", "Trebuchet MS Italic",
    "Tunga", "Verdana", "Verdana Bold", "Verdana Bold Italic", "Verdana Italic",
    "Webdings", "Westminster", "Wingdings", "WST_Czech", "WST_Engl", "WST_Fren",
    "WST_Germ", "WST_Ital", "WST_Span", "WST_Swed",
)

# enum type_font: Font0 = 0 … Font56 = 56
for _i in range(len(FONT_TYPES)):
    globals()[f"Font{_i}"] = _i
del _i


class CFontName:
    def GetFontName(self, FontNumber: int) -> str:
        return FONT_TYPES[int(FontNumber)]
