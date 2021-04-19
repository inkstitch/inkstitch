import os

application = 'inkstitch.app'
appname = os.path.basename(application)
format = 'UDBZ'
files = [application]
symlinks = {'Applications': '/Applications/Inkscape.app/Contents/Resources/share/inkscape/extensions'}
background = os.path.join(os.getcwd(), '..', 'dmg', 'dmg-background.png')
icon =  os.path.join(os.getcwd(), '..', 'dmg', 'icon.icns')

icon_locations = {
    appname:        (150, 230),
    'Applications': (450, 230),
}

window_rect = ((100, 100), (600, 400))
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
sidebar_width = 180

arrange_by = None
grid_offset = (0, 0)
grid_spacing = 100
scroll_position = (0, 0)
label_pos = 'bottom'
text_size = 14
icon_size = 95
