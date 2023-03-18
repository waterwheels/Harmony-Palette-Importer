import secrets
from pathlib import Path
from sys import argv


def hex_to_argb(hex_string: str) -> tuple[int, int, int, int]:
    """Convert hexidecimal color information in ARGB order to tuple of binary values."""
    _hex = int(hex_string, 16)
    a = _hex >> 24 & 0xFF
    r = _hex >> 16 & 0xFF
    g = _hex >> 8 & 0xFF
    b = _hex & 0xFF

    return (a, r, g, b)


class Color:
    def __init__(self, hex: str):
        self.hex = hex
        _a, _r, _g, _b = hex_to_argb(self.hex)
        self.a = _a
        self.r = _r
        self.g = _g
        self.b = _b

    def __repr__(self):
        return f"Color(hex='{self.hex}', a='{self.a}', r='{self.r}', g='{self.g}', b='{self.b}')"


def write_plt_file(name: str, colors: list[Color]):
    """Write the list of Colors to a .plt file"""

    def _format_line(color: Color) -> str:
        """Return a line formatted for entry into a Harmony palette file (.plt)"""
        color_id = f"0x{secrets.token_hex(8)}" # generate random new colour id
        line = f"Solid    {color.hex:<26} {color_id} {color.r:>3} {color.g:>3} {color.b:>3} {color.a:>3}\n"
        return line

    header = "ToonBoomAnimationInc PaletteFile 2\n"
    palette_lines = [_format_line(color) for color in colors]

    plt_path = Path(".") / f"{name}.plt"
    with open(plt_path, "w") as plt:
        plt.write(header)
        plt.writelines(palette_lines)

def read_input_file(input_path: str):
    """Read the contents of the input file and return list of colour strings"""
    with open(input_path, "r") as in_plt:
        txt_list = in_plt.read().splitlines()

    if txt_list[0] == ";paint.net Palette File":
        txt_list = [line for line in txt_list if line[0] != ";"] # strip comments
    # could add other input parsers for different text formats?

    return txt_list

def main():
    # test right number of argv?
    # test input file exists here?

    colourList = read_input_file(argv[1])

    colors = [Color(hex) for hex in colourList]

    if argv[2]:
        name = argv[2].split(".")[0] # allow user to write "blah.plt", but strip it off and add it back in write_plt_file
    else:
        name = "output"

    write_plt_file(name, colors)


if __name__ == "__main__":
    main()
