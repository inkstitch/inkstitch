from embroider import Embroider
from install import Install
from params import Params
from print_pdf import Print
from simulate import Simulate
from input import Input
from output import Output
from zip import Zip
from flip import Flip
from object_commands import ObjectCommands
from layer_commands import LayerCommands
from convert_to_satin import ConvertToSatin

from base import InkstitchExtension
import inspect

extensions = []
for item in locals().values():
    if inspect.isclass(item) and \
       issubclass(item, InkstitchExtension) and \
       item is not InkstitchExtension:
            extensions.append(item)
