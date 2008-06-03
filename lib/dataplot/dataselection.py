# -*-Python-*-

# dataplot - plot hierachical datasets
# Copyright (C) 2008 Werner Hoch <werner.ho@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import gtk, gobject


class DataSelection(gtk.Dialog):

    returns = {}

    def __init__(self, parent, columnnames):
        gtk.Dialog.__init__(self, "Row Selection", parent,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        scrollwin = gtk.ScrolledWindow()
        scrollwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwin.set_size_request(-1, 200)
        
        self.listview = gtk.TreeView()
        x_cell = gtk.CellRendererToggle()
        x_cell.set_property("radio", True)
        x_cell.set_property("activatable", True)
        x_cell.connect('toggled', self.x_toggle, self.listview)
                      
        y_cell = gtk.CellRendererToggle()
        y_cell.set_property("activatable", True)
        y_cell.connect('toggled', self.y_toggle, self.listview)

        self.listview.append_column(gtk.TreeViewColumn("X", x_cell , active=0))
        self.listview.append_column(gtk.TreeViewColumn("Y", y_cell , active=1))
        self.listview.append_column(gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=2))

        liststore = gtk.ListStore( gobject.TYPE_BOOLEAN, gobject.TYPE_BOOLEAN, str)
        for name in columnnames:
            liststore.append([False, False, name])
        self.listview.set_model(liststore)
        
        scrollwin.add_with_viewport(self.listview)
        self.vbox.add(scrollwin)
        self.show_all()
        
        
        #################### Signals
        self.connect("response", self.event_response)
        self.connect("destroy", self.event_destroy)

        
    def event_destroy(self, widget):
        self.destroy()
    

    def event_response(self, widget, response_id):
        if response_id == gtk.RESPONSE_ACCEPT:
            x,y = None, []
            for row in self.listview.get_model():
                if row[0] == True:
                    x = row[2]
                if row[1] == True:
                    y.append(row[2])
            self.returns["x_column"] = x
            self.returns["y_columns"] = y
        self.destroy()
            
        
    def x_toggle(self, cell, path, listview):
        """
        Callback when the toggle buttons of the X-row is toggled.
        Only allow one x-value to be selected from the x-row
        """
        mm = listview.get_model()
        newstate = not mm[path][0]
        for row in mm:
            row[0] = False
        mm[path][0] = newstate
        
    
    def y_toggle(self, cell, path, listview):
        mm = listview.get_model()
        mm[path][1] = not mm[path][1]
        