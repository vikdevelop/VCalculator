# Copyright 2021 vik.dev
#
# Tento program je svobodný software. Můžete jej dále šířit a nebo upravovat
# za podmínek licence GNU General Public License verze 3 (nebo novější verze) vydané
# Free Software Foundation.
#
# Tento program je distribuován v naději, že bude užitečný,
# ale BEZ JAKÉKOLI ZÁRUKY; bez dokonce předpokládané záruky pro
# PRODEJNOST nebo PRO KOMERČNÍ ÚČEL. Viz
# GNU General Public License pro více informací.
#
# Měli byste obdržet kopii GNU General Public License
# spolu s tímto programem. Pokud ne, viz <https://www.gnu.org/licenses/>.

#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Kalkulacka:
    def __init__ (self):
        self.carry = 0
        self.ops = {
            '=': (lambda x, y: self.carry),
            '+': (lambda x, y: x + y ),
            '-': (lambda x, y: x - y  ),
            'x': (lambda x, y: x * y),
            '÷': (lambda x, y: x / y),
            '%': (lambda x, y: x % y),
            '✔': (lambda x, y: x ** y) }
        self.nextOp = self.ops['+']
    def DoOp (self, func, entry):
        self.carry = self.nextOp(self.carry, entry)
        self.nextOp = func
        return self.carry

class HeaderBarWindow (Gtk.Window):

    def __init__ (self):
        super().__init__()
        self.calculator = Kalkulacka()
        self.clearCarry = False
        self.init_ui()

    def init_ui (self):
        self.set_title("Kalkulačka")
        self.set_default_size(250, 250)
        self.set_border_width(16)
        self.set_resizable(False)
        self.connect("destroy", Gtk.main_quit)

        grid = Gtk.Grid()
        grid.set_row_spacing(4)
        grid.set_column_spacing(4)
        self.add(grid)

        entry = Gtk.Label()
        entry.set_selectable(True)
        entry.set_halign(Gtk.Align.START)
        grid.attach(entry, 0, 0, 12, 1)

        gridAdder = lambda btn, x, y: grid.attach(btn, x % 10, y + (x / 10), 2, 1)

        # Add operator buttons row
        x = 0
        for op, func in self.calculator.ops.items():
            btn = Gtk.Button(label=op)
            btn.connect("clicked", lambda widget, func=func: self.BtnOpPress(entry, func))
            gridAdder(btn, x, 1)
            x = x + 2

        # Add number buttons rows
        x = 0
        for n in list(range(1, 10)) + [0, '.']:
            btn = Gtk.Button(label=n)
            btn.connect("clicked", lambda widget, n=n: self.BtnEntryPress(entry, n))
            gridAdder(btn, x, 3)
            x = x + 2

    def BtnOpPress (self, entry, func):
        entry.set_text(str(self.calculator.DoOp(func, float(entry.get_text()))))
        self.clearCarry = True

    def BtnEntryPress (self, entry, num):
        if self.clearCarry:
            self.clearCarry = False
            entry.set_text(str(num))
        else:
            entry.set_text(entry.get_text() + str(num))

win = HeaderBarWindow()
win.show_all()
Gtk.main()
