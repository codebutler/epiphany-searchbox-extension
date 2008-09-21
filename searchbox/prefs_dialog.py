import gtk
import gtk.glade
import gobject
import opensearch
from os import path

class PreferencesDialog:
	def __init__(self, parent_window, providers):
		# load the glade xml, store some widgets
		currentpath = path.abspath(path.dirname(__file__))
		self._glade = gtk.glade.XML(path.join(currentpath, 'searchbox.glade'),'manage_engines_dialog')
		self.treeview = self._glade.get_widget("engines_treeview")
		self._dialog = self._glade.get_widget("manage_engines_dialog")
		self._dialog.set_transient_for(parent_window)
		self._dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

		# create the tree's model
		self.treemodel = gtk.ListStore(gobject.TYPE_PYOBJECT)
		self.treeview.set_model(self.treemodel)
		
		# create the tree's views
		column = gtk.TreeViewColumn("Name")

		renderer = gtk.CellRendererPixbuf()
		column.pack_start(renderer, False)
		column.set_cell_data_func(renderer, self.icon_func)

		renderer = gtk.CellRendererText()
		column.pack_start(renderer)
		column.set_cell_data_func(renderer, self.text_func)

		self.treeview.append_column(column)

		# populate the tree
		for provider in providers:
			self.treemodel.append([provider])

		# hook up signals
		dict = { "on_remove_button_clicked" : self.on_remove_button_clicked,
		         "on_getmore_button_clicked" : self.on_getmore_button_clicked }
		self._glade.signal_autoconnect (dict)

	def on_remove_button_clicked(self, widget):
		print 'remove me'

	def on_getmore_button_clicked(self, widget):
		print 'getmore!'

	def icon_func(self, treeview, cell, model, iter):
		val = model.get_value(iter, 0)
		cell.set_property("pixbuf", val.get_pixbuf())

	def text_func(self, treeview, cell, model, iter):
		val = model.get_value(iter, 0)
		cell.set_property("text", val.shortname)

	def run(self):
		self._dialog.show()
		result = self._dialog.run()
		self._dialog.destroy()
		return result

	def focus(self):
		self._dialog.grab_focus()
		self._dialog.present()

