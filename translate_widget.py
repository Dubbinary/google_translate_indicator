import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class TranslateWindow(Gtk.Window):

    def __init__(self, model):
        Gtk.Window.__init__(self, title="Entry Demo")
        self.set_size_request(200, 100)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        self.input_from = Gtk.Entry()
        icon_name = "system-search-symbolic"
        self.input_from.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
            icon_name)
        hbox.pack_start(self.input_from, True, True, 0)

        self.translate_button = Gtk.Button.new_with_label("Translate")
        self.translate_button.connect("clicked", self.translate_clicked)
        hbox.pack_start(self.translate_button, True, True, 0)

        self.input_to = Gtk.Entry()
        self.input_to.set_editable(False)
        vbox.pack_start(self.input_to, True, True, 0)


    def translate_clicked(self, button):
        self.input_to.set_text(self.input_from.get_text()[::-1])
