# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
# Additional credits to https://github.com/clsn/pyTartan

# tartan colors according to https://www.tartanregister.gov.uk/docs/Colour_shades.pdf (as of december 2023)
# Problem: ambigious due to multiple usage of same color code

def string_to_color(color_string: str) -> str:
    """
    Converts a color code from the tartan register to a hex color code or defaults to empty

    :param color_string: color code from the tartan register
    :returns: hex color code or empty string
    """
    standards = {
        # 'LR': '#F4CCCC',  # Light Red
        'LR': '#E87878',  # Light Red
        # 'LR': '#F04DB0',  # Light Red
        # 'R': '#A00048',  # Red
        # 'R': '#FA4B00',  # Red
        'R': '#FF0000',  # Red
        # 'R': '#DC0000',  # Red
        # 'R': '#C80000',  # Red
        # 'R': '#C82828',  # Red
        # 'R': '#C8002C',  # Red
        # 'R': '#B03000',  # Red
        # 'DR': '#A00000',  # Dark Red
        # 'DR': '#960000',  # Dark Red
        # 'DR': '#960028',  # Dark Red
        'DR': '#880000',  # Dark Red
        # 'DR': '#800028',  # Dark Red
        # 'DR': '#781C38',  # Dark Red
        # 'DR': '#4C0000',  # Dark Red
        # 'DR': '#901C38',  # Dark Red
        # 'DR': '#680028',  # Dark Red
        # 'O': '#EC8048',  # Orange
        # 'O': '#E86000',  # Orange
        'O': '#FF5000',  # Orange
        # 'O': '#DC943C',  # Orange
        # 'O': '#D87C00',  # Orange
        'DO': '#BE7832',  # Dark Orange
        'LY': '#F9F5C8',  # Light Yellow
        # 'LY': '#F8E38C',  # Light Yellow
        'Y': '#FFFF00',  # Yellow
        # 'Y': '#FFE600',  # Yellow
        # 'Y': '#FFD700',  # Yellow
        # 'Y': '#FCCC00',  # Yellow
        # 'Y': '#E0A126',  # Yellow
        # 'Y': '#E8C000',  # Yellow
        # 'Y': '#D8B000',  # Yellow
        # 'DY': '#BC8C00',  # Dark Yellow
        # 'DY': '#C89800',  # Dark Yellow
        'DY': '#C88C00',  # Dark Yellow
        # 'LG': '#789484',  # Light Green
        # 'LG': '#C4BC68',  # Light Green
        # 'LG': '#9C9C00',  # Light Green
        'LG': '#ACD74A',  # Light Green
        # 'LG': '#86C67C',  # Light Green
        # 'LG': '#649848',  # Light Green
        # 'G': '#008B00',  # Green
        # 'G': '#408060',  # Green
        'G': '#289C18',  # Green
        # 'G': '#006400',  # Green
        # 'G': '#007800',  # Green
        # 'G': '#3F5642',  # Green
        # 'G': '#767E52',  # Green
        # 'G': '#5C6428',  # Green
        # 'G': '#00643C',  # Green
        # 'G': '#146400',  # Green
        # 'G': '#006818',  # Green
        # 'G': '#004C00',  # Green
        # 'G': '#285800',  # Green
        # 'G': '#005020',  # Green
        # 'G': '#005448',  # Green
        # 'DG': '#003C14',  # Dark Green
        # 'DG': '#003820',  # Dark Green
        'DG': '#004028',  # Dark Green
        # 'DG': '#002814',  # Dark Green
        # 'LB': '#98C8E8',  # Light Blue
        'LB': '#82CFFD',  # Light Blue
        # 'LB': '#00FCFC',  # Light Blue
        # 'B': '#BCC3D2',  # Blue
        # 'B': '#048888',  # Blue
        # 'B': '#3C82AF',  # Blue
        # 'B': '#5C8CA8',  # Blue
        # 'B': '#2888C4',  # Blue
        # 'B': '#48A4C0',  # Blue
        # 'B': '#2474E8',  # Blue
        # 'B': '#0596FA',  # Blue
        'B': '#0000FF',  # Blue
        # 'B': '#3850C8',  # Blue
        # 'B': '#788CB4',  # Blue
        # 'B': '#5F749C',  # Blue
        # 'B': '#1870A4',  # Blue
        # 'B': '#1474B4',  # Blue
        # 'B': '#0000CD',  # Blue
        # 'B': '#2C4084',  # Blue
        # 'DB': '#055183',  # Dark Blue
        # 'DB': '#003C64',  # Dark Blue
        'DB': '#00008C',  # Dark Blue
        # 'DB': '#2C2C80',  # Dark Blue
        # 'DB': '#1C0070',  # Dark Blue
        # 'DB': '#000064',  # Dark Blue
        # 'DB': '#202060',  # Dark Blue
        # 'DB': '#000048',  # Dark Blue
        # 'DB': '#141E46',  # Dark Blue
        # 'DB': '#1C1C50',  # Dark Blue
        'LP': '#A8ACE8',  # Light Purple
        # 'LP': '#C49CD8',  # Light Purple
        # 'LP': '#806D84',  # Light Purple
        # 'LP': '#9C68A4',  # Light Purple
        # 'P': '#9058D8',  # Purple
        # 'P': '#AA00FF',  # Purple
        # 'P': '#B458AC',  # Purple
        # 'P': '#6C0070',  # Purple
        # 'P': '#5A008C',  # Purple
        # 'P': '#64008C',  # Purple
        'P': '#780078',  # Purple
        # 'DP': '#440044',  # Dark Purple
        'DP': '#1E0948',  # Dark Purple
        # 'W': '#E5DDD1',  # White
        # 'W': '#E8CCB8',  # White
        # 'W': '#F0E0C8',  # White
        # 'W': '#FCFCFC',  # White
        'W': '#FFFFFF',  # White
        # 'W': '#F8F8F8',  # White
        'LN': '#E0E0E0',  # Light Grey
        # 'N': '#C8C8C8',  # Grey
        # 'N': '#C0C0C0',  # Grey
        # 'N': '#B0B0B0',  # Grey
        'N': '#A0A0A0',  # Grey
        # 'N': '#808080',  # Grey
        # 'N': '#888888',  # Grey
        # 'N': '#646464',  # Grey
        # 'N': '#505050',  # Dark Grey
        'DN': '#555a64',  # Dark Grey
        # 'DN': '#1C1714',  # Dark Grey
        # 'DN': '#14283C',  # Dark Grey
        # 'DN': '#1C1C1C',  # Dark Grey
        # 'K': '#101010',  # Black
        'K': '#000000',  # Black
        # 'LT': '#A08858',  # Light Brown
        # 'LT': '#8C7038',  # Light Brown
        'LT': '#A07C58',  # Light Brown
        # 'LT': '#B07430',  # Light Brown
        # 'T': '#98481C',  # Brown
        'T': '#603800',  # Brown
        # 'T': '#604000',  # Brown
        # 'T': '#503C14',  # Brown
        # 'DT': '#4C3428',  # Dark Brown
        'DT': '#441800',  # Dark Brown
        # 'DT': '#230D00'  # Dark Brown
    }
    try:
        return standards[color_string.upper()]
    except KeyError:
        return ''
