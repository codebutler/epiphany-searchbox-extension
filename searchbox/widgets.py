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

# XXX: get rid of all this, its just stupid

class Alignment(gtk.Alignment):
	"A container bin"

	def __init__(self, xalign = 0, yalign = 0, xscale = 0, yscale = 0):
		gtk.Alignment.__init__(self, xalign, yalign, xscale, yscale)


class HBox(gtk.HBox):
	"A horizontal container"

	def __init__(self, *args):
		gtk.HBox.__init__(self)

		self.set_spacing(3)
		self.set_border_width(0)

		for widget in args:
			self.pack_start(widget)

class Entry(gtk.Entry):
	"A normal text entry"

	def __init__(self, text = None):
		gtk.Entry.__init__(self)

		self.set_activates_default(True)
		self.set_text(text)


	def set_text(self, text):
		"Sets the entry contents"

		if text is None:
			text = ""

		gtk.Entry.set_text(self, text)

class EventBox(gtk.EventBox):
	"A container which handles events for a widget (for tooltips etc)"

	def __init__(self, widget = None):
		gtk.EventBox.__init__(self)

		self.widget = widget

		if widget is not None:
			self.add(self.widget)
