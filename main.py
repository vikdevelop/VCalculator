#!/usr/bin/env python3
import gi
import sys
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio

class VCalculator:
    def __init__ (self):
        self.carry = 0
        self.ops = {
            '=': (lambda x, y: self.carry),
            '+': (lambda x, y: x + y ),
            '-': (lambda x, y: x - y  ),
            'x': (lambda x, y: x * y),
            '÷': (lambda x, y: x / y),
            '%': (lambda x, y: x % y) }
        self.nextOp = self.ops['+']
    def DoOp (self, func, entry):
        self.carry = self.nextOp(self.carry, entry)
        self.nextOp = func
        return self.carry

class VCalculatorWindow (Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculator = VCalculator()
        self.clearCarry = False
        self.application = kwargs.get('application')
        self.init_ui()

    def init_ui (self):
        self.set_title("VCalculator")
        self.set_default_size(200, 300)
        self.set_resizable(False)
        
        self.set_title(title="VCalculator")
        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)
        # App menu
        menu_button_model = Gio.Menu()
        menu_button_model.append("About VCalculator", 'app.about')
        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        grid = Gtk.Grid()
        grid.set_row_spacing(4)
        grid.set_column_spacing(4)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        self.set_child(child=grid)
        
        listbox = Gtk.ListBox.new()
        listbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        listbox.get_style_context().add_class(class_name='boxed-list')
        grid.attach(listbox, 0, 0, 12, 1)
        
        label = Gtk.Label()
        label.set_label('\n')
        grid.attach(label, 0, 0, 12, 1)
        
        self.button = Gtk.Button.new_from_icon_name('edit-clear-symbolic')
        self.button.connect('clicked', self.on_button_clicked)
        bc = self.button.get_style_context()
        bc.add_class('destructive-action')
        bc.add_class('pill')
        
        self.entry = Adw.EntryRow()
        self.entry.set_editable(True)
        self.entry.set_title('=')
        self.entry.set_use_markup('<bold>')
        #self.entry.add_suffix(widget=self.button)
        self.entry.set_halign(Gtk.Align.START)
        adw_action_row_01 = Adw.ActionRow.new()
        adw_action_row_01.set_icon_name(icon_name='com.github.vikdevelop.VCalculator')
        adw_action_row_01.set_title(title='')
        adw_action_row_01.set_subtitle(subtitle='')
        adw_action_row_01.add_suffix(widget=self.entry)
        adw_action_row_01.add_suffix(widget=self.button)
        listbox.append(child=adw_action_row_01)
        #grid.attach(self.entry, 0, 0, 12, 1)

        gridAdder = lambda btn, x, y: grid.attach(btn, x % 10, y + (x / 10), 2, 1)

        # Add operator buttons row
        x = 0
        for op, func in self.calculator.ops.items():
            self.button = Gtk.Button.new_from_icon_name('edit-clear-symbolic')
            self.button.connect('clicked', self.on_button_clicked)
            bc = self.button.get_style_context()
            bc.add_class('destructive-action')
            bc.add_class('pill')
            btn = Gtk.Button(label=op)
            btnc = btn.get_style_context()
            btnc.add_class('suggested-action')
            btn.connect("clicked", lambda widget, func=func: self.BtnOpPress(self.entry, func))
            gridAdder(btn, x, 1)
            x = x + 2

        # Add number buttons rows
        x = 0
        for n in list(range(1, 10)) + [0, '.']:
            btn = Gtk.Button(label=n)
            btn.connect("clicked", lambda widget, n=n: self.BtnEntryPress(self.entry, n))
            gridAdder(btn, x, 3)
            x = x + 2
        
        label2 = Gtk.Label()
        label2.set_label('\n')
        grid.attach(label2, 0, 0, 12, 1)
    
    def BtnOpPress (self, entry, func):
        self.entry.set_text(str(self.calculator.DoOp(func, float(entry.get_text()))))
        self.clearCarry = True

    def BtnEntryPress (self, entry, num):
        if self.clearCarry:
            self.clearCarry = False
            self.entry.set_text(str(num))
        else:
            self.entry.set_text(entry.get_text() + str(num))
            
    def on_button_clicked(self, widget, *args):
        self.entry.set_text(' ')

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        self.create_action('about', self.on_about_action)

    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name("VCalculator")
        dialog.set_version("1.0.8")
        dialog.set_developer_name("vikdevelop")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/VCalculator")
        dialog.set_issue_url("https://github.com/vikdevelop/VCalculator/issues")
        dialog.set_copyright("© 2022 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_application_icon("com.github.vikdevelop.VCalculator")
        dialog.show()
        
    def on_settings_action(self, action, param):
        self.dialog = Dialog_settings(self)

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)
    
    def on_activate(self, app):
        self.win = VCalculatorWindow(application=app)
        self.win.present()
app = MyApp(application_id="com.github.vikdevelop.VCalculator")
app.run(sys.argv)
