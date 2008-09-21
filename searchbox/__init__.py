#!/usr/bin/env python
#
#   SearchBox - Epiphany Extension
#   Copyright (C) 2006  Eric Butler <eric@extremeboredom.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# ugh, what a mess.

import gtk
import gobject
import epiphany
import os
import os.path
import xml.dom.minidom
from tempfile import mkstemp
from searchbox import *
from icon_entry  import *
from prefs_dialog import *
from util import *
from tool_item import *
from widgets import *


toolbar_xml = '''<?xml version="1.0"?>
<toolbars version="1.0">
  <available>
    <toolitem name="SearchBox"/>
  </available>
</toolbars>
'''

def on_extension_load():
	model = epiphany.ephy_shell_get_default().get_toolbars_model(False)

	fd, filepath = mkstemp()
	os.write(fd, toolbar_xml)
	os.close(fd)

	model.load_names(filepath)

	os.unlink(filepath)

on_extension_load()

def searchbox_key_press_cb(window, event):
	if event.state & gtk.gdk.CONTROL_MASK:
		keyvalname = gtk.gdk.keyval_name(event.keyval)
		if keyvalname == "k":
			toolbar = window.get_toolbar()
			item = find_widget(toolbar, SearchBoxToolItem)
			item.entry.entry.grab_focus() # XXX: make item.grab_focus() work!
		

def find_widget(widget_to_search, type_to_find):
	for child in widget_to_search.get_children():
		if isinstance(child, type_to_find):
			return child
		elif isinstance(child, gtk.Container):
			result = find_widget(child, type_to_find)
			if result != None:
				return result
	return None
			

def attach_window(window):
	ui_manager = window.get_ui_manager()
	actiongroup = gtk.ActionGroup('SearchBoxActions')
	custom_action = SearchBoxAction()
	actiongroup.add_action(custom_action)
	window._searchbox_actiongroup = actiongroup
	ui_manager.insert_action_group(actiongroup, 0)

	signal = window.connect_after("notify::active-tab", searchbox_active_tab)
	window._searchbox_active_tab_sig = signal

	signal = window.connect("key-press-event", searchbox_key_press_cb)
	window._searchbox_key_press_sig = signal

def detach_window(window):
	ui_manager = window.get_ui_manager()
	if hasattr(window, "_searchbox_actiongroup"):
		ui_manager.remove_action_group (window._searchbox_actiongroup)

	if hasattr(window, "_searchbox_key_press_sig"):
		window.disconnect(window._searchbox_key_press_sig)
		delattr(window, "_searchbox_key_press_sig")

	if hasattr(window, "_searchbox_active_tab_sig"):
		window.disconnect(window._searchbox_active_tab_sig)
		delattr(window, "_searchbox_active_tab_sig")

def attach_tab(window, tab):
	tab._window = window # I dont know any way around this :(
	c_handler_id = tab.connect_after("new-document-now", ephy_ge_content_cb)
	s_handler_id = tab.connect('ge_search_link', ephy_ge_search_cb)
	tab._searchbox_details = [ s_handler_id, c_handler_id ]
	#tab._available_searches = []

def detach_tab(window, tab):
	if hasattr(tab, "_window"):
		tab._window = None
		delattr(tab, "_window")

	if hasattr(tab, "_searchbox_details"):
		[ s_handler_id, c_handler_id ] = tab._searchbox_details
		tab.disconnect(s_handler_id)
		tab.disconnect(c_handler_id)

def searchbox_active_tab(window, pspec):
	item = find_widget(window.get_toolbar(), SearchBoxToolItem)
	if item != None:
		item.clearAvailableSearches()	

	#tab = window.get_active_tab()
	#for [title, address] in tab._available_searches:
	#	item.addAvailableSearch(title, address)

def ephy_ge_search_cb(embed, type, title, address):
	if type == "application/opensearchdescription+xml":
		# get the widget, we need to add something to it
		window = embed._window
		item = find_widget(window.get_toolbar(), SearchBoxToolItem)
		if item != None:
			item.addAvailableSearch(title, address)

def ephy_ge_content_cb(embed, uri):
	# tell the widget to clear any available search providers
	window = embed._window
	item = find_widget(window.get_toolbar(), SearchBoxToolItem)
	if item != None:
		item.clearAvailableSearches()

class SearchBoxAction(gtk.Action):
	__gtype_name__ = "SearchBoxAction"
	def __init__(self):
		gtk.Action.__init__(self, 'SearchBox', 'Search Box', None, None)

# XXX: Move this stuff around
gobject.type_register (SearchBoxToolItem)
gobject.type_register (IconEntry)
gobject.signal_new("changed", IconEntry, gobject.SIGNAL_ACTION, gobject.TYPE_BOOLEAN, ())
gobject.signal_new("populate-popup", IconEntry, gobject.SIGNAL_ACTION, gobject.TYPE_BOOLEAN, (gobject.TYPE_PYOBJECT, ))
SearchBoxAction.set_tool_item_type(SearchBoxToolItem)
