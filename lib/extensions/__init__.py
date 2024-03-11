# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .apply_palette import ApplyPalette
from .apply_threadlist import ApplyThreadlist
from .auto_run import AutoRun
from .auto_satin import AutoSatin
from .break_apart import BreakApart
from .cleanup import Cleanup
from .commands_scale_symbols import CommandsScaleSymbols
from .convert_to_satin import ConvertToSatin
from .convert_to_stroke import ConvertToStroke
from .cut_satin import CutSatin
from .cutwork_segmentation import CutworkSegmentation
from .density_map import DensityMap
from .display_stacking_order import DisplayStackingOrder
from .duplicate_params import DuplicateParams
from .element_info import ElementInfo
from .fill_to_stroke import FillToStroke
from .flip import Flip
from .generate_palette import GeneratePalette
from .global_commands import GlobalCommands
from .gradient_blocks import GradientBlocks
from .input import Input
from .install import Install
from .install_custom_palette import InstallCustomPalette
from .jump_to_stroke import JumpToStroke
from .layer_commands import LayerCommands
from .lettering import Lettering
from .lettering_along_path import LetteringAlongPath
from .lettering_custom_font_dir import LetteringCustomFontDir
from .lettering_force_lock_stitches import LetteringForceLockStitches
from .lettering_generate_json import LetteringGenerateJson
from .lettering_remove_kerning import LetteringRemoveKerning
from .lettering_update_json_glyphlist import LetteringUpdateJsonGlyphlist
from .letters_to_font import LettersToFont
from .object_commands import ObjectCommands
from .object_commands_toggle_visibility import ObjectCommandsToggleVisibility
from .outline import Outline
from .output import Output
from .palette_split_text import PaletteSplitText
from .palette_to_text import PaletteToText
from .params import Params
from .preferences import Preferences
from .print_pdf import Print
from .remove_embroidery_settings import RemoveEmbroiderySettings
from .reorder import Reorder
from .select_elements import SelectElements
from .selection_to_guide_line import SelectionToGuideLine
from .selection_to_pattern import SelectionToPattern
from .simulator import Simulator
from .stitch_plan_preview import StitchPlanPreview
from .stitch_plan_preview_undo import StitchPlanPreviewUndo
from .stroke_to_lpe_satin import StrokeToLpeSatin
from .test_swatches import TestSwatches
from .troubleshoot import Troubleshoot
from .update_svg import UpdateSvg
from .zigzag_line_to_satin import ZigzagLineToSatin
from .zip import Zip

__all__ = extensions = [ApplyPalette,
                        ApplyThreadlist,
                        AutoRun,
                        AutoSatin,
                        BreakApart,
                        Cleanup,
                        CommandsScaleSymbols,
                        ConvertToSatin,
                        ConvertToStroke,
                        CutSatin,
                        CutworkSegmentation,
                        DensityMap,
                        DisplayStackingOrder,
                        DuplicateParams,
                        ElementInfo,
                        FillToStroke,
                        Flip,
                        GeneratePalette,
                        GlobalCommands,
                        GradientBlocks,
                        Input,
                        Install,
                        InstallCustomPalette,
                        JumpToStroke,
                        LayerCommands,
                        Lettering,
                        LetteringAlongPath,
                        LetteringCustomFontDir,
                        LetteringForceLockStitches,
                        LetteringGenerateJson,
                        LetteringRemoveKerning,
                        LetteringUpdateJsonGlyphlist,
                        LettersToFont,
                        ObjectCommands,
                        ObjectCommandsToggleVisibility,
                        Outline,
                        Output,
                        PaletteSplitText,
                        PaletteToText,
                        Params,
                        Preferences,
                        Print,
                        RemoveEmbroiderySettings,
                        Reorder,
                        SelectElements,
                        SelectionToGuideLine,
                        SelectionToPattern,
                        Simulator,
                        StitchPlanPreview,
                        StitchPlanPreviewUndo,
                        StrokeToLpeSatin,
                        TestSwatches,
                        Troubleshoot,
                        UpdateSvg,
                        ZigzagLineToSatin,
                        Zip]
