#!/usr/bin/env python3

import sys
import urllib.request
import hashlib
import lxml.html

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib

gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify


class MyIndicator:
    def __init__(self):
        self.hash = ''
        self.indicator_id = 'test'
        self.ind = appindicator.Indicator.new(
            self.indicator_id,
            "/home/dubbinary/DEV/PycharmProjects/google_translate_indicator/img/logo.png",
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        # notify.init(self.indicator_id)
        self.ind.connect("new-label", self.notifyer)
        self.ind.set_label("Label","guide")
        self.menu = Gtk.Menu()

        # Input
        item = Gtk.Entry()
        item.set_visibility(True)
        self.menu.append(item)

        # Clear
        item = Gtk.MenuItem()
        item.set_label("Clear")
        item.connect("activate", self.clear)
        self.menu.append(item)

        # Exit
        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.quit)
        self.menu.append(item)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def notifyer(self,ind_obj,new_label,new_guide):
        notify.Notification.new("Signal", "Label changed!", None).show()

    def main(self):
        self.check_site()
        GLib.timeout_add_seconds(10, self.check_site)
        notify.init(self.indicator_id)
        Gtk.main()

    def clear(self, widget):
        self.hash = self.remote_hash
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

    def check_site(self):
        remote_data = urllib.request.urlopen('http://habrahabr.ru').read()
        self.remote_hash = hashlib.md5(remote_data).hexdigest()
        if self.hash == '':
            self.hash = self.remote_hash
            print("======INITIAL======")
            print(self.remote_hash)
        else:
            print("======TRIGGERED=======");
            print("Local hash: " + self.hash)
            print("Remote hash: " + self.remote_hash)
            if self.hash != self.remote_hash:
                print("======ATTENTION=======");
                self.ind.set_status(appindicator.IndicatorStatus.ATTENTION)
                # self.ind.set_icon_full("/home/dubbinary/DEV/PycharmProjects/wifi/notif.svg","")
                notify.Notification.new("Test", "New updates!", None).show()
        return True

    def quit(self, widget):
        notify.uninit()
        Gtk.main_quit()


if __name__ == '__main__':
    indicator = MyIndicator();
    indicator.main();
