import secrets
from pathlib import Path


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
        color_id = f"0x{secrets.token_hex(8)}"
        line = f"Solid    {color.hex:<26} {color_id} {color.r:>3} {color.g:>3} {color.b:>3} {color.a:>3}\n"
        return line

    header = "ToonBoomAnimationInc PaletteFile 2\n"
    palette_lines = [_format_line(color) for color in colors]

    plt_path = Path(".") / f"{name}.plt"
    with open(plt_path, "w") as plt:
        plt.write(header)
        plt.writelines(palette_lines)


def main():

    # colourListTxt should be a whitespace-separated string of colours of the format "########" where # is a hex character
    colourListTxt = "ffaaabac ff0072ca 80010203"
    colourList = colourListTxt.split()

    colors = [Color(hex) for hex in colourList]
    write_plt_file("example", colors)


if __name__ == "__main__":
    main()
