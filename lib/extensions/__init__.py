from auto_satin import AutoSatin
from convert_to_satin import ConvertToSatin
from cut_satin import CutSatin
from electron_simulator import ElectronSimulator
from embroider import Embroider
from flip import Flip
from global_commands import GlobalCommands
from input import Input
from install import Install
from layer_commands import LayerCommands
from lettering import Lettering
from lib.extensions.troubleshoot import Troubleshoot
from object_commands import ObjectCommands
from output import Output
from params import Params
from print_pdf import Print
from remove_embroidery_settings import RemoveEmbroiderySettings
from simulate import Simulate
from zip import Zip


__all__ = extensions = [Embroider,
                        Install,
                        Params,
                        Print,
                        Simulate,
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
                        ElectronSimulator]
