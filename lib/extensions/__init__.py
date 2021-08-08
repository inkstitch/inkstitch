# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from lib.extensions.troubleshoot import Troubleshoot

from .auto_satin import AutoSatin
from .break_apart import BreakApart
from .cleanup import Cleanup
from .convert_to_satin import ConvertToSatin
from .convert_to_stroke import ConvertToStroke
from .cut_satin import CutSatin
from .duplicate_params import DuplicateParams
from .embroider_settings import EmbroiderSettings
from .flip import Flip
from .global_commands import GlobalCommands
from .import_threadlist import ImportThreadlist
from .input import Input
from .install import Install
from .install_custom_palette import InstallCustomPalette
from .layer_commands import LayerCommands
from .lettering import Lettering
from .lettering_custom_font_dir import LetteringCustomFontDir
from .lettering_generate_json import LetteringGenerateJson
from .lettering_remove_kerning import LetteringRemoveKerning
from .letters_to_font import LettersToFont
from .object_commands import ObjectCommands
from .output import Output
from .params import Params
from .print_pdf import Print
from .remove_embroidery_settings import RemoveEmbroiderySettings
from .reorder import Reorder
from .selection_to_pattern import SelectionToPattern
from .simulator import Simulator
from .stitch_plan_preview import StitchPlanPreview
from .zip import Zip

__all__ = extensions = [StitchPlanPreview,
                        Install,
                        Params,
                        Print,
                        Input,
                        Output,
                        Zip,
                        Flip,
                        SelectionToPattern,
                        ObjectCommands,
                        LayerCommands,
                        GlobalCommands,
                        ConvertToSatin,
                        ConvertToStroke,
                        CutSatin,
                        AutoSatin,
                        Lettering,
                        LetteringGenerateJson,
                        LetteringRemoveKerning,
                        LetteringCustomFontDir,
                        LettersToFont,
                        Troubleshoot,
                        RemoveEmbroiderySettings,
                        Cleanup,
                        BreakApart,
                        ImportThreadlist,
                        InstallCustomPalette,
                        Simulator,
                        Reorder,
                        DuplicateParams,
                        EmbroiderSettings]
