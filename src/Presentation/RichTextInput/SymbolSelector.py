import math
from tkinter import Frame, LEFT, OUTSIDE

from ..StyledTkinter import StyledTkinter


# This class helps to select unicode symbols
class SymbolSelector(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.category_buttons = [
            StyledTkinter.get_dark_button(self, text='\u00F7', command=self.select_math_symbols),
            StyledTkinter.get_dark_button(self, text='\u03C0', command=self.select_greek_symbols),
            StyledTkinter.get_dark_button(self, text='\u00E9', command=self.select_accent_symbols),
            StyledTkinter.get_dark_button(self, text='\u0024', command=self.select_business_symbols)
        ]

        self.greek_symbol_frame = Frame(self)
        self.math_symbol_frame = Frame(self)
        self.accent_symbol_frame = Frame(self)
        self.business_symbol_frame = Frame(self)

        self.greek_symbols = []
        self.math_symbols = []
        self.accent_symbols = []
        self.business_symbols = []
        self.width = 7

        self.init_greek_symbols()
        self.init_math_symbols()
        self.init_accent_symbols()
        self.init_business_symbols()

    def init_greek_symbols(self):
        self.greek_symbols = [
            # Capital
            '\u0393',  # Gamma
            '\u0394',  # Delta
            '\u0398',  # Theta
            '\u039E',  # Xi
            '\u03A0',  # Pi
            '\u03A3',  # Sigma
            '\u03A6',  # Phi
            '\u03A8',  # Psi
            '\u03A9',  # Omega
            # Lowercase
            '\u03B2',  # Beta
            '\u03B4',  # Delta
            '\u03B5',  # Epsilon
            '\u03B6',  # Zeta
            '\u03B7',  # Eta
            '\u03B8',  # Theta
            '\u03BB',  # Lambda
            '\u03BC',  # Mu
            '\u03BE',  # Xi
            '\u03C0',  # Pi
            '\u03C2',  # Final Sigma
            '\u03C3',  # Sigma
            '\u03C6',  # Phi
            '\u03C8',  # Psi
            '\u03C9',  # Omega
            '\u03D6'  # Other Pi
        ]

        self.init_frame(self.greek_symbol_frame, len(self.greek_symbols))
        self.place_symbol_buttons(self.greek_symbol_frame, self.greek_symbols)

    def init_math_symbols(self):
        self.math_symbols = [
            '\u03C0',  # PI
            '\u00F7',  # Division
            '\u0095',  # Dot Multiplication
            '\u00B0',  # Degree
            '\u00B1',  # Plus/Minus
            '\u2070',  # Power of Zero
            '\u00B9',  # Power of one
            '\u00B2',  # Squared
            '\u00B3',  # Cubed
            '\u00BC',  # Power of quarter
            '\u00BD',  # Power of half
            '\u00BE',  # Power of three quarters
            '\u00D7',  # X Multiplication
            '\u00D8',  # Ø
            '\u00F8',  # ø
            '\u2044',  # Fraction Slash
            '\u2107',  # Euler Constant
            '\u221A',  # Square Root
            '\u221B',  # Cube Root
            '\u221C',  # Fourth Root
            '\u221E',  # Infinity
            '\u2260',  # Not equal
        ]

        self.init_frame(self.math_symbol_frame, len(self.math_symbols))
        self.place_symbol_buttons(self.math_symbol_frame, self.math_symbols)

    def init_accent_symbols(self):
        self.accent_symbols = [
            '\u00A1',  # Inverted Exclamation Mark
            '\u00BF',  # Inverted Question Mark
            '\u203D',  # Interrobang
            '\u00C0',  # À
            '\u00E0',  # à
            '\u00C1',  # Á
            '\u00E1',  # á
            '\u00C2',  # Â
            '\u00E2',  # â
            '\u00C7',  # Ç
            '\u00E7',  # ç
            '\u00C8',  # È
            '\u00E8',  # è
            '\u00C9',  # É
            '\u00D9',  # é
            '\u00CA',  # Ê
            '\u00EA',  # ê
            '\u00CF',  # Ï
            '\u00EF',  # ï
            '\u00D1',  # Ñ
            '\u00F1',  # ñ
            '\u00D4',  # Ô
            '\u00F4',  # ô
        ]

        self.init_frame(self.accent_symbol_frame, len(self.accent_symbols))
        self.place_symbol_buttons(self.accent_symbol_frame, self.accent_symbols)

    def init_business_symbols(self):
        self.business_symbols = [
            '\u0080',  # Euro
            '\u0090',  # TM
            '\u00A2',  # Cent
            '\u00A3',  # Pound
            '\u00A4',  # Currency
            '\u00A5',  # Yen
            '\u00A7',  # Section
            '\u00A9',  # Copyright
            '\u00AE',  # Registered
            '\u2052',  # Commercial Minus
            '\u20A0',  # Euro-Currency Sign
            '\u20BF',  # Bitcoin
            '\u2116',  # Numero sign
            '\u2117',  # Sound Copyright sign
            '\u2122',  # Trademark
        ]

        self.init_frame(self.business_symbol_frame, len(self.business_symbols))
        self.place_symbol_buttons(self.business_symbol_frame, self.business_symbols)

    def init_frame(self, frame, num_symbols):
        for i in range(0, self.width):
            frame.columnconfigure(i, weight=1)

        for i in range(0, math.ceil(num_symbols / self.width)):
            frame.rowconfigure(i, weight=1)

    def place_symbol_buttons(self, frame, symbols):
        curr_row = 0
        curr_col = 0
        for symbol in symbols:
            symbol_button = StyledTkinter.get_dark_button(
                frame,
                text=symbol,
                command=lambda: self.select_symbol(symbol))
            symbol_button.grid(row=curr_row, column=curr_col, sticky="news")

            if curr_row >= self.width:
                curr_row = curr_row + 1
                curr_col = 0
            else:
                curr_col = curr_col + 1

    def display(self):
        self.place(x=0, y=25, height=150, width=150, bordermode=OUTSIDE)

        for button in self.category_buttons:
            button.pack(side=LEFT)

        top_offset = 16
        self.math_symbol_frame.place(y=top_offset)
        self.greek_symbol_frame.place(y=top_offset)
        self.accent_symbol_frame.place(y=top_offset)
        self.business_symbol_frame.place(y=top_offset)

    def select_greek_symbols(self):
        self.greek_symbol_frame.tkraise()

    def select_math_symbols(self):
        self.math_symbol_frame.tkraise()

    def select_accent_symbols(self):
        self.accent_symbol_frame.tkraise()

    def select_business_symbols(self):
        self.business_symbol_frame.tkraise()

    def select_symbol(self, symbol):
        pass

    def hide(self):
        self.place_forget()
