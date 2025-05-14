from tkinter import Frame, Label


# This class helps to select unicode symbols
class SymbolSelector(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.category_symbols = [
            '\u03C0',  # Pi for Greek Symbols
            '\u00F7',  # Division for Math Symbols
            '\u00E9',  # é for Accents
            '\u0024',  # $ for Business
        ]

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
            '\u03D6'   # Other Pi
        ]
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

    def display(self):
        self.pack()

        for unicode_value in self.greek_symbols:
            Label(self, text=u'{unicode_value}'.format(unicode_value=unicode_value)).pack()

    def hide(self):
        self.pack_forget()
