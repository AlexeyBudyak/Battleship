class Menu:
    def __init__(self):
        self.filename = ''
        self.quote = ''
        self.lvl = 0
    def __str__(self):
        return f"> {self.filename}{self.quote}  (Enter 'xxx' anytime for previous menu)"
    def lvl1(self, filename):
        self.lvl = 1
        self.filename = filename
    def lvl2(self, num_quote):
        self.quote = f'\Quote {num_quote}'
    def new_lvl(self, lvl):
        if lvl < 2: self.quote = ''
        if lvl < 1: self.filename = ''
        self.lvl = lvl