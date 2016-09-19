import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import web_module

class TranslateWindow(Gtk.Window):

    def __init__(self, model):
        Gtk.Window.__init__(self, title="Entry Demo")
        self.model = model
        self.set_size_request(200, 300)

        self.timeout_id = None

        self.set_resizable(False)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        # hb.props.title = "HeaderBar example"
        self.set_titlebar(hb)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.input_from = Gtk.Entry()
        icon_name = "system-search-symbolic"
        self.input_from.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
            icon_name)
        hbox.pack_start(self.input_from, True, True, 0)

        self.translate_button = Gtk.Button.new_with_label("Translate")
        self.translate_button.connect("clicked", self.translate_clicked)
        hbox.pack_start(self.translate_button, True, True, 0)
        hb.pack_end(hbox)

        self.sw = Gtk.ScrolledWindow()
        # self.sw.set_policy(Gtk.POLICY_AUTOMATIC, Gtk.POLICY_AUTOMATIC)
        self.input_to = Gtk.TextView()
        self.input_to.set_editable(False)
        self.input_to.set_wrap_mode(Gtk.WrapMode.WORD)
        # self.input_to.set_justification(Gtk.Justification.CENTER)
        self.text_buffer = self.input_to.get_buffer()
        self.sw.add(self.input_to)
        self.sw.show()
        self.input_to.show()
        self.add(self.sw)



    def translate_clicked(self, button):
        from_lang = self.model.get_lang_from()
        to_lang = self.model.get_lang_to()
        text_to_translate = self.input_from.get_text()
        print(from_lang, to_lang, text_to_translate)
        translated_text = web_module.translate(from_lang, to_lang, text_to_translate)
        # Notifier there
        self.text_buffer.set_text(translated_text)
