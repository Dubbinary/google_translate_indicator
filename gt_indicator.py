#!/usr/bin/env python3

import sys
import urllib.request
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib

gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify

from translate_widget import TranslateWindow
from model_data import ModelData

class GTIndicator:

    is_widget_running = False

    def __init__(self):
        self.indicator_id = 'google_translate_indicator'
        self.model = ModelData()
        self.languages = self.model.get_languages()
        self.inflate_ui_components()


    def main(self):
        notify.init(self.indicator_id)
        self.init_clipboard()
        Gtk.main()


#
########################### SIGNAL HENDLERS ####################################
#
    def notifyer(self,widget,new_label,new_guide):
        notify.Notification.new("New translate rule", new_label, None).show()

    def translate(self, widget):
        if(not GTIndicator.is_widget_running):
            self.start_widget()
        # TODO add grab focus feature
        # else:
        #     self.tr_widget.get_toplevel().child_focus(Gtk.DIR_TAB_FORWARD)



    def select_lang_from(self, widget):
        new_lang = self.get_lang_by_title(widget.get_label())
        if(new_lang == self.model.get_lang_from()):
            return
        if(not self.is_swap_languages(new_lang)):
            self.model.set_lang_from(new_lang)
        self.update_app_ind_label()
        self.model.update_config()

    def select_lang_to(self, widget):
        new_lang = self.get_lang_by_title(widget.get_label())
        if(new_lang == self.model.get_lang_to()):
            return
        if(not self.is_swap_languages(new_lang)):
            self.model.set_lang_to(new_lang)
        self.update_app_ind_label()
        self.model.update_config()

    def quit(self, widget):
        notify.uninit()
        Gtk.main_quit()

    def on_delete_widget(widget, event, user_data):
        GTIndicator.is_widget_running = False
        Gtk.main_quit()

##
################################## ADDITIONAL METHODS ##########################
##
    def inflate_ui_components(self):

        # Create appindicator instance
        self.ind = appindicator.Indicator.new(
            self.indicator_id,
            os.path.dirname(os.path.realpath(__file__))+"/img/logo.ico",
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.connect("new-label", self.notifyer)
        self.ind.set_label(self.languages[self.model.get_lang_from()]+"->"+
        self.languages[self.model.get_lang_to()],"None")

        # Create Menu instance
        self.menu = Gtk.Menu()

        # Create MenuItem instance with "Translate" option
        item = Gtk.MenuItem()
        item.set_label("Translate")
        item.connect("activate", self.translate)
        self.menu.append(item)

        prepared_lang_vals = sorted(self.languages.values())

        # Create MenuItem instance with "From" option
        item = Gtk.MenuItem()
        item.set_label("From")
        # Create Sub Menu instance
        sub_menu = Gtk.Menu()
        for lang_val in prepared_lang_vals:
            # Create MenuItem instance with language select option
            menu_item = Gtk.MenuItem(lang_val)
            menu_item.connect("activate", self.select_lang_from)
            sub_menu.append(menu_item)
        item.set_submenu(sub_menu)
        self.menu.append(item)

        # Create MenuItem instance with "To" option
        item = Gtk.MenuItem()
        item.set_label("To")
        # Create Sub Menu instance
        sub_menu = Gtk.Menu()
        for lang_val in prepared_lang_vals:
            # Create MenuItem instance with language select option
            menu_item = Gtk.MenuItem(lang_val)
            menu_item.connect("activate", self.select_lang_to)
            sub_menu.append(menu_item)
        item.set_submenu(sub_menu)
        self.menu.append(item)

        # Create MenuItem instance with "Quit" option
        item = Gtk.MenuItem()
        item.set_label("Quit")
        item.connect("activate", self.quit)
        self.menu.append(item)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def get_lang_by_title(self, lang_title):
        return list(self.languages \
        .keys())[list(self.languages.values()) \
        .index(lang_title)]

    def is_swap_languages(self, new_lang):
        lang_from = self.model.get_lang_from()
        lang_to = self.model.get_lang_to()
        if(new_lang == lang_to or new_lang == lang_from):
            self.model.set_lang_from(lang_to)
            self.model.set_lang_to(lang_from)
            return True
        else:
            return False

    def update_app_ind_label(self):
        self.ind.set_label(self.languages[self.model.get_lang_from()]+"->"+
            self.languages[self.model.get_lang_to()], "None")

    def start_widget(self):
        self.tr_widget = TranslateWindow(self.model)
        self.tr_widget.connect("delete-event", self.on_delete_widget)
        self.tr_widget.show_all()
        GTIndicator.is_widget_running = True
        Gtk.main()

    def init_clipboard(self):
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        text = self.clipboard.wait_for_text()

        # Store the text in clipboard
        # self.clipboard.set_text("Test clipboard", -1)
        # self.clipboard.store()
        print(text)


#
######################### GTIndicator CLASS END ################################
#

if __name__ == '__main__':
    indicator = GTIndicator();
    indicator.main();
