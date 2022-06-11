# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from lib.extensions.troubleshoot import Troubleshoot

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
from .duplicate_params import DuplicateParams
from .embroider_settings import EmbroiderSettings
from .flip import Flip
from .generate_palette import GeneratePalette
from .global_commands import GlobalCommands
from .input import Input
from .install import Install
from .install_custom_palette import InstallCustomPalette
from .layer_commands import LayerCommands
from .lettering import Lettering
from .lettering_custom_font_dir import LetteringCustomFontDir
from .lettering_force_lock_stitches import LetteringForceLockStitches
from .lettering_generate_json import LetteringGenerateJson
from .lettering_remove_kerning import LetteringRemoveKerning
from .letters_to_font import LettersToFont
from .object_commands import ObjectCommands
from .object_commands_toggle_visibility import ObjectCommandsToggleVisibility
from .output import Output
from .palette_split_text import PaletteSplitText
from .palette_to_text import PaletteToText
from .params import Params
from .print_pdf import Print
from .remove_embroidery_settings import RemoveEmbroiderySettings
from .reorder import Reorder
from .selection_to_guide_line import SelectionToGuideLine
from .selection_to_pattern import SelectionToPattern
from .simulator import Simulator
from .stitch_plan_preview import StitchPlanPreview
from .stitch_plan_preview_undo import StitchPlanPreviewUndo
from .zip import Zip

__all__ = extensions = [StitchPlanPreview,
                        StitchPlanPreviewUndo,
                        Install,
                        Params,
                        Print,
                        Input,
                        Output,
                        Zip,
                        Flip,
                        SelectionToPattern,
                        SelectionToGuideLine,
                        ObjectCommands,
                        ObjectCommandsToggleVisibility,
                        LayerCommands,
                        GlobalCommands,
                        CommandsScaleSymbols,
                        ConvertToSatin,
                        ConvertToStroke,
                        CutSatin,
                        AutoSatin,
                        AutoRun,
                        Lettering,
                        LetteringGenerateJson,
                        LetteringRemoveKerning,
                        LetteringCustomFontDir,
                        LetteringForceLockStitches,
                        LettersToFont,
                        Troubleshoot,
                        RemoveEmbroiderySettings,
                        Cleanup,
                        BreakApart,
                        ApplyThreadlist,
                        InstallCustomPalette,
                        GeneratePalette,
                        PaletteSplitText,
                        PaletteToText,
                        Simulator,
                        Reorder,
                        DuplicateParams,
                        EmbroiderSettings,
                        CutworkSegmentation]
