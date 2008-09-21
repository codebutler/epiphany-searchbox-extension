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

import gtk
import opensearch
import md5

from icon_entry import *
from util import *
from prefs_dialog import *

google_desc = '''<?xml version="1.0"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
<ShortName>Google</ShortName>
<Description>Google</Description>
<Image height="16" width="16" type="image/x-icon">http://www.google.com/favicon.ico</Image>
<Url type="text/html" method="get" template="http://www.google.com/search?ie=utf-8&amp;oe=utf-8&amp;q={searchTerms}"/>
<Url type="application/x-suggestions+json" method="GET" template="http://suggestqueries.google.com/complete/search?output=firefox&amp;client=epiphany&amp;qu={searchTerms}"/>
</OpenSearchDescription>'''

class SearchBoxToolItem(gtk.ToolItem): 
	__gtype_name__ = "SearchBoxToolItem"
	def __init__(self):
		gtk.ToolItem.__init__(self)
		# construct the ui
		self.entry = IconEntry()
		foo = gtk.Alignment(yalign=0.5)
		foo.add(self.entry)
		self.add(foo)
		foo.show_all()
		self.entry.iconebox.connect("button-press-event", self._on_icon_button_pressed)
		self.entry.entry.connect("key-press-event", self._on_entry_key_press)
		
		self.connect("realize", self._on_realized)
		self.connect("unrealize", self._on_unrealized)

		dir = data_dir()

		if os.path.isdir(dir) == False:
			os.makedirs(dir)
			# write an initial search provider (google)
			# XXX: This is not a very good solution!
			f = open(os.path.join(dir,'google.opensearch'), "w")
			f.write(google_desc)
			f.close()

		self.providers = []
		self._availableSearches = []

		files = os.listdir(dir)
		for name in files:
			[file, ext] = os.path.splitext(name)
			if ext != ".opensearch":
				continue

			foo = opensearch.Description("file://" + os.path.join(dir,name))
			self.addProvider(foo)

		# load last selection
		default_file = os.path.join(data_dir(), 'default')
		if os.path.isfile(default_file):
			f = open(default_file, 'r')
			provider_name = f.read()
			f.close()
			for this_provider in self.providers:
				if this_provider.shortname == provider_name:
					self.select_provider(this_provider)
					return
		
		if self.providers[0] != None:
			self.select_provider(self.providers[0])
		else:
			self.select_provider(None)
	
	def _on_realized(self, widget):
		self._browser_window = widget.get_toplevel()
	
	def _on_unrealized(self, widget):
		self._browser_window = None

	def _on_entry_key_press(self, entry, event):
		if event.keyval == gtk.keysyms.Return or event.keyval == gtk.keysyms.KP_Enter:
			url = self.getSelectedProvider().get_best_template()
			query = opensearch.Query(url)
			query.searchTerms = entry.get_text()

			self._browser_window.load_url(query.url())

			entry.set_text("")

	def _on_icon_button_pressed(self, widget, event):
		if event.button != 1:
			return

		widget.emit_stop_by_name("button-press-event")

		provider_menu = gtk.Menu()
		for provider in self.providers:
			item = gtk.ImageMenuItem()
			item.connect("activate", self._menu_item_activated, provider)
			
			pixbuf = provider.get_pixbuf()
			image = gtk.Image()
			image.set_from_pixbuf(pixbuf)
			item.set_image(image)

			label = gtk.Label()
			label.set_alignment(0, 0.5)
			if provider == self.getSelectedProvider():
				label.set_markup("<b>" + provider.shortname + "</b>")
			else:
				label.set_text(provider.shortname)

			item.add(label)
			provider_menu.add(item)
		
		if len(self._availableSearches) > 0:
			provider_menu.add(gtk.SeparatorMenuItem())
			for [title,address] in self._availableSearches:
				item = gtk.MenuItem('Add "' + title + '"')
				provider_menu.add(item)

		provider_menu.add(gtk.SeparatorMenuItem())
		item = gtk.MenuItem("Manage Search Engines...")
		item.connect("activate", self._manage_item_activated)
		provider_menu.add(item)
		provider_menu.show_all()
		provider_menu.attach_to_widget(self.entry, None)
		self.popup_menu(provider_menu)
		return True
	
	def _manage_item_activated(self, widget):
		if hasattr(self, "prefs") == False:
			self.prefs = PreferencesDialog(self.get_toplevel(), self.providers)
			self.prefs.run()
			print "done with prefs"
			self.prefs = None
			delattr(self, "prefs")
		else:
			self.prefs.focus()

	def _menu_item_activated(self, widget, data):
		self.select_provider(data)

	def _get_menu_position(self, menu):
		parent = menu.get_attach_widget()
		if parent:
			x, y = parent.window.get_origin()

			parent_alloc = parent.get_allocation()			
			x += parent_alloc.x + 1
			y += parent_alloc.y - 1

			width, height = menu.get_size_request()
			if y + height >= parent.get_screen().get_height:
				y -= height
			else:
				y += parent_alloc.height

			return x, y, True
		return 0, 0, False

	def _menu_deactivate(self, menu):
		menu.popdown()
		parent = menu.get_attach_widget()
		#if parent:
		#	parent.set_state(gtk.STATE_NORMAL)

	def popup_menu(self, menu, ev = None):
		menu.connect("deactivate", self._menu_deactivate)
		if ev:
			menu.popup(None, None, self._get_menu_position, ev.button, ev.time)
		else:
			menu.popup(None, None, self._get_menu_position, 0, gtk.get_current_event_time())

		# Highlight the parent
		#parent = menu.get_attach_widget()
		#if parent:
		#	parent.set_state(gtk.STATE_SELECTED)

	def addProvider(self, provider):
		self.providers.append(provider)
		#XXX Add to gui!
		
	def select_provider(self, provider):
		self.current_provider = provider
		if provider == None:
			self.entry.set_icon_stock(gtk.STOCK_MISSING_IMAGE, 
						  "Select Search Engine")
		else:
			pixbuf = provider.get_pixbuf()
			self.entry.set_icon(pixbuf, "Select Search Engine")
			self.entry.entry.grab_focus()

		# remember what was selected
		default_file = os.path.join(data_dir(), 'default')
		f = open(default_file, 'w')
		if provider != None:
			f.write(provider.shortname)
		else:
			f.write('')
		f.close()
		
		# xxx: tell any other windows!

	def getSelectedProvider(self):
		return self.current_provider

	def addAvailableSearch(self, title, address):
		# XXX: Parse the address to get the icon!
		self._availableSearches.append([title, address])

	def clearAvailableSearches(self):
		del self._availableSearches[:]
