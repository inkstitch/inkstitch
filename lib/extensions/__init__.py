from lib.extensions.troubleshoot import Troubleshoot

from .auto_satin import AutoSatin
from .break_apart import BreakApart
from .cleanup import Cleanup
from .convert_to_satin import ConvertToSatin
from .cut_satin import CutSatin
from .embroider import Embroider
from .flip import Flip
from .global_commands import GlobalCommands
from .import_threadlist import ImportThreadlist
from .input import Input
from .install import Install
from .layer_commands import LayerCommands
from .lettering import Lettering
from .object_commands import ObjectCommands
from .output import Output
from .params import Params
from .print_pdf import Print
from .remove_embroidery_settings import RemoveEmbroiderySettings
from .reorder import Reorder
from .simulator import Simulator
from .stitch_plan_preview import StitchPlanPreview
from .zip import Zip

__all__ = extensions = [Embroider,
                        StitchPlanPreview,
                        Install,
                        Params,
                        Print,
                        Input,
                        Output,
                        Zip,
                        Flip,
                        ObjectCommands,
                        LayerCommands,
                        GlobalCommands,
                        ConvertToSatin,
                        CutSatin,
                        AutoSatin,
                        Lettering,
                        Troubleshoot,
                        RemoveEmbroiderySettings,
                        Cleanup,
                        BreakApart,
                        ImportThreadlist,
                        Simulator,
                        Reorder]
