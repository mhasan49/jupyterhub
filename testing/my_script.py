# This is the string that will be converted to ASCII art
import pyfiglet


class MyBanner:
    """Pyfiglet is the module that will convert regular strings in to ASCII art fonts
    pyfiglet --list_fonts to chose from the fonts
    """

    def __init__(self, my_text):
        self.text = pyfiglet.figlet_format(f"{my_text}", font="slant", justify="center")

    def print_banner(self):
        print(f"{self.text}")

#    def __init__(self, my_text):
#        self.text = pyfiglet.print_figlet(f"{my_text}")

#    def print_banner(self):
#        print(f"{self.text}")







