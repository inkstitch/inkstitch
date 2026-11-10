# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from importlib import import_module
import sys


_EXTENSION_CLASS_NAMES = (
    "About",
    "ApplyAttribute",
    "ApplyPalette",
    "ApplyThreadlist",
    "AutoRun",
    "AutoSatin",
    "BatchLettering",
    "BreakApart",
    "Cleanup",
    "CommandsScaleSymbols",
    "CrossStitchAssistant",
    "CutSatin",
    "CutworkSegmentation",
    "DensityMap",
    "DisplayStackingOrder",
    "DuplicateParams",
    "ElementInfo",
    "FillToSatin",
    "FillToStroke",
    "Flip",
    "GeneratePalette",
    "GlobalCommands",
    "GradientBlocks",
    "Input",
    "Install",
    "InstallCustomPalette",
    "JumpToStroke",
    "JumpToTrim",
    "KnockdownFill",
    "LayerCommands",
    "Lettering",
    "LetteringAlongPath",
    "LetteringCustomFontDir",
    "LetteringEditJson",
    "LetteringFontSample",
    "LetteringForceLockStitches",
    "LetteringGenerateJson",
    "LetteringOrganizeGlyphs",
    "LetteringRemoveKerning",
    "LetteringSetColorSortIndex",
    "LetteringSvgFontToLayers",
    "LettersToFont",
    "ObjectCommands",
    "ObjectCommandsToggleVisibility",
    "Outline",
    "Output",
    "PaletteSplitText",
    "PaletteToText",
    "Params",
    "PngRealistic",
    "PngSimple",
    "Preferences",
    "Print",
    "Redwork",
    "RemoveDuplicatedPoints",
    "RemoveEmbroiderySettings",
    "Reorder",
    "SatinMulticolor",
    "SatinToStroke",
    "SelectElements",
    "SelectionToAnchorLine",
    "SelectionToGuideLine",
    "SelectionToPattern",
    "SewStackEditor",
    "Simulator",
    "StitchPlanPreview",
    "StitchPlanPreviewUndo",
    "StrokeToLpeSatin",
    "StrokeToSatin",
    "Tartan",
    "TestSwatches",
    "ThreadList",
    "TransformElements",
    "Troubleshoot",
    "UnlinkClone",
    "UpdateSvg",
    "ZigzagLineToSatin",
    "Zip",
)

__all__ = ["extensions", *_EXTENSION_CLASS_NAMES]


def __getattr__(name):
    if name == "extensions":
        extensions = [getattr(sys.modules[__name__], class_name)
                      for class_name in _EXTENSION_CLASS_NAMES]
        globals()[name] = extensions
        return extensions

    if name not in _EXTENSION_CLASS_NAMES:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "Print":
        module_name = "print_pdf"
    else:
        module_name = "".join(
            f"_{character.lower()}" if character.isupper() else character
            for character in name
        ).lstrip("_")

    module = import_module(f".{module_name}", __name__)
    extension_class = getattr(module, name)
    globals()[name] = extension_class
    return extension_class
