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
from widgets import *

class IconEntry(Alignment):
	"An entry with an icon in it"

	def __init__(self, text = None):
		Alignment.__init__(self)

		self.set_border_width(1)

		self.tooltips	= gtk.Tooltips()
		self.icon	= None
		self.icontip	= None

		# set up ui
		self.hbox = HBox()
		self.add(self.hbox)

		self.entry = Entry(text)
		self.entry.set_has_frame(False)

		self.iconebox	= EventBox()
		self.iconebox.set_visible_window(False)

		self.iconalign	= Alignment(1.0, 0.5, 0, 0)
		self.iconalign.set_padding(1, 1, 2, 0)
		self.iconalign.add(self.iconebox)

		self.icon = gtk.Image()
		self.iconebox.add(self.icon)

		self.hbox.pack_start(self.iconalign, False, False)
		self.hbox.pack_start(self.entry)
		self.hbox.show_all()

		# connect signals
		self.connect("expose-event", self.__cb_expose)
		self.connect("size-allocate", self.__cb_size_allocate)
		self.connect("size-request", self.__cb_size_request)

		self.entry.connect_after("focus-in-event", lambda w,d: self.queue_draw())
		self.entry.connect_after("focus-out-event", lambda w,d: self.queue_draw())

		self.entry.connect("changed", lambda w: self.emit("changed"))
		self.entry.connect("populate-popup", lambda w,m: self.emit("populate-popup", m))


	def __cb_expose(self, widget, data):
		"Draws the widget borders on expose"

		allocation	= self.get_allocation()
		style		= self.entry.get_style()
		intfocus	= self.entry.style_get_property("interior-focus")
		focuswidth	= self.entry.style_get_property("focus-line-width")

		x		= allocation.x
		y		= allocation.y
		width		= allocation.width
		height		= allocation.height

		if self.entry.flags() & gtk.HAS_FOCUS == gtk.HAS_FOCUS and intfocus == False:
			x	+= focuswidth
			y	+= focuswidth
			width	-= 2 * focuswidth
			height	-= 2 * focuswidth

		style.paint_flat_box(self.window, self.entry.state,
		                     gtk.SHADOW_NONE, None, self.entry,
				     "entry_bg", x, y, width, height)

		style.paint_shadow(self.window, gtk.STATE_NORMAL,
		                   gtk.SHADOW_IN, None, self.entry,
				   "entry", x, y, width, height)

		if self.entry.flags() & gtk.HAS_FOCUS == gtk.HAS_FOCUS and intfocus == False:
			x	-= focuswidth
			y	-= focuswidth
			width	+= 2 * focuswidth
			height	+= 2 * focuswidth

			style.paint_focus(self.window, self.entry.state, None, self.entry, "entry", x, y, width, height)


	def __cb_size_allocate(self, widget, allocation):
		"Modifies the widget size allocation"
		
		self.allocation 	= allocation

		child_allocation	= gtk.gdk.Rectangle()
		xborder, yborder	= self.__entry_get_borders()

		child_allocation.x	= allocation.x + self.border_width + xborder
		child_allocation.y	= allocation.y + self.border_width + yborder
		child_allocation.width	= max(allocation.width - (self.border_width + xborder) * 2, 0)
		child_allocation.height	= max(allocation.height - (self.border_width + yborder) * 2, 0)

		self.hbox.size_allocate(child_allocation)
		self.queue_draw()

	def __cb_size_request(self, widget, requisition):
		"Modifies the widget size request"

		requisition.width	= self.border_width * 2
		requisition.height	= self.border_width * 2
		xborder, yborder	= self.__entry_get_borders()

		entrywidth, entryheight	= self.entry.size_request()
		requisition.width 	+= entrywidth;
		requisition.height	+= entryheight >= 18 and entryheight or 18

		requisition.width	+= 2 * xborder
		requisition.height	+= 2 * yborder

	def __entry_get_borders(self):
		"Returns the border sizes of an entry"

		style		= self.entry.get_style()
		intfocus	= self.entry.style_get_property("interior-focus")
		focuswidth	= self.entry.style_get_property("focus-line-width")

		xborder		= style.xthickness
		yborder		= style.ythickness

		if intfocus == False:
			xborder	+= focuswidth
			yborder	+= focuswidth

		return xborder, yborder


	def get_text(self):
		"Wrapper for the entry"

		return self.entry.get_text()


	def remove_icon(self):
		"Removes the icon from the entry"

		self.set_icon(None, "")
		self.tooltips.set_tip(self.iconebox, tooltip)

	def set_icon_stock(self, stock, tooltip = ""):
		self.icon.set_from_stock(stock, gtk.ICON_SIZE_MENU)
		self.tooltips.set_tip(self.iconebox, tooltip)

	def set_icon(self, pixbuf, tooltip = ""):
		if pixbuf:
			self.icon.set_from_pixbuf(pixbuf)
		else:
			self.icon.set_from_stock('gtk-missing-image', gtk.ICON_SIZE_MENU)
		self.tooltips.set_tip(self.iconebox, tooltip)

	def set_text(self, text):
		"Wrapper for the entry"

		self.entry.set_text(text)

	def set_visibility(self, visibility):
		"Wrapper for the entry"

		self.entry.set_visibility(visibility)
