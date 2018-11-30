import memtkinter as tk
from memtkinter import ttk

__all__ = [
	'MultiWidgetScrollbar',
	'MultiColumnListboxScrollbar',
]

class MultiWidgetScrollbar(ttk.Scrollbar):
	'''
	Scrollbar that keeps a list of attached widgets
	by calling the add_widget method with the widget as an argument
	the scrollbar and the widget are configure to keep them in sync.
	'''
	def __init__(self, master=None, **kw):
		ttk.Scrollbar.__init__(self, master, **kw)
		if str(self['orient']) == tk.VERTICAL:
			self.configure(command=self._yview)
		else:
			self.configure(command=self._xview)
		self.widgets = []
		
	def add_widget(self, widget):
		if str(self['orient']) == tk.VERTICAL:
			widget.configure(yscrollcommand=self.set)
		else:
			widget.configure(xscrollcommand=self.set)
		self.widgets.append(widget)
		
	def set(self, *args):
		# override set method to keep widgets in sync
		ttk.Scrollbar.set(self, *args)
		# move all widgets to the new position
		for w in self.widgets:
			w.yview_moveto(args[0])
		
	def _xview(self, *args):
		for w in self.widgets:
			w.xview(*args)
		return 'break'
		
	def _yview(self, *args):
		for w in self.widgets:
			w.yview(*args)
		return 'break'
		

class MultiColumnListboxScrollbar(MultiWidgetScrollbar):
	'''
	Speciallised scrollbar for handling multiple listboxes
	using the add_listbox method to keep track of attached listboxes
	configures the listboxes as required to enable uniform selection
	i.e. selected items are highlighted on all listboxes
	also overrides various methods of listbox to handle the multiple
	widget aspects
	'''
	def add_listbox(self, listbox):
		self.add_widget(listbox)
		# to make selection work
		listbox.configure(exportselection=False)
		# override widget methods
		listbox.delete = self.delete
		listbox.get = self.get
		listbox.insert = self.insert
		listbox.scan_mark = self.scan_mark
		listbox.scan_dragto = self.scan_dragto
		listbox.see = self.see
		listbox.selection_anchor = self.selection_anchor
		listbox.selection_clear = self.selection_clear
		listbox.selection_includes = self.selection_includes
		listbox.selection_set = self.selection_set
		# track changes to keep selection the same on all lists
		listbox.bind('<<ListboxSelect>>', self._onselectchange)
	
	def _onselectchange(self, event):
		sel = event.widget.curselection()
		for l in self.widgets:
			if l != event.widget:
				tk.Listbox.selection_clear(l, 0, tk.END)
				for s in sel:
					tk.Listbox.selection_set(l, s)
				
	def curselection(self):
		"""Return the indices of currently selected item."""
		return self.widgets[0].curselection()
		
	def delete(self, first, last=None):
		"""Delete items from FIRST to LAST (included)."""
		for l in self.widgets:
			tk.Listbox.delete(l, first, last)
		
	def get(self, first, last=None):
		"""Get list of items from FIRST to LAST (included)."""
		data = []
		for l in self.widgets:
			data.append([tk.Listbox.get(l, first, last)])
		return list(zip(*data))
		
	def index(self, index):
		"""Return index of item identified with INDEX."""
		return self.widgets[0].index(index)
		
	def insert(self, index, *elements):
		"""Insert ELEMENTS at INDEX."""
		for elem in elements:
			for l in self.widgets:
				tk.Listbox.insert(l, index, elem[self.widgets.index(l)])
		
	def nearest(self, y):
		"""Get index of item which is nearest to y coordinate Y."""
		return self.widgets[0].nearest(y)
		
	def scan_mark(self, x, y):
		"""Remember the current X, Y coordinates."""
		for l in self.widgets:
			tk.Listbox.scan_mark(l, x, y)
			
	def scan_dragto(self, x, y):
		"""Adjust the view of the listbox to 10 times the
		difference between X and Y and the coordinates given in
		scan_mark."""
		for l in self.widgets:
			tk.Listbox.scan_dragto(l, x, y)
			
	def see(self, index):
		"""Scroll such that INDEX is visible."""
		for l in self.widgets:
			tk.Listbox.see(l, index)
			
	def selection_anchor(self, index):
		"""Set the fixed end oft the selection to INDEX."""
		for l in self.widgets:
			tk.Listbox.selection_anchor(l, index)
	select_anchor = selection_anchor

	def selection_clear(self, first, last=None):
		"""Clear the selection from FIRST to LAST (included)."""
		for l in self.widgets:
			tk.Listbox.selection_clear(l, first, last)
	select_clear = selection_clear

	def selection_includes(self, index):
		"""Return 1 if INDEX is part of the selection."""
		for l in self.widgets:
			tk.Listbox.selection_includes(l, index)
	select_includes = selection_includes

	def selection_set(self, first, last=None):
		"""Set the selection from FIRST to LAST (included) without
		changing the currently selected elements."""
		for l in self.widgets:
			tk.Listbox.selection_set(l, first, last)
	select_set = selection_set

	def size(self):
		"""Return the number of elements in the listbox."""
		return self.widgets[0].size()
		
	def itemcget(self, index, option):
		"""Return the resource value for an ITEM and an OPTION."""
		return self.widgets[0].itemcget(index, option)
			
	def itemconfigure(self, index, cnf=None, **kw):
		"""Configure resources of an ITEM.

		The values for resources are specified as keyword arguments.
		To get an overview about the allowed keyword arguments
		call the method without arguments.
		Valid resource names: background, bg, foreground, fg,
		selectbackground, selectforeground."""
		if cnf == None and not kw:
			return self.widgets[0].itemconfigure(index, cnf, kw)
		for l in self.widgets:
			l.itemconfigure(index, cnf, **kw)
	itemconfig = itemconfigure
	
if __name__ == '__main__':
	root = tk.Tk(None, 'test.xml', 'test')
	
	selmode = tk.EXTENDED
	l1 = tk.Listbox(root, selectmode=selmode)
	l1.grid(column=1, row=1, sticky='nesw')
	l2 = tk.Listbox(root, selectmode=selmode)
	l2.grid(column=2, row=1, sticky='nesw')
	l3 = tk.Listbox(root, selectmode=selmode)
	l3.grid(column=3, row=1, sticky='nesw')
	
	sb = MultiColumnListboxScrollbar(root)
	sb.grid(column=10, row=1, sticky='nesw')
	sb.add_listbox(l1)
	sb.add_listbox(l2)
	sb.add_listbox(l3)
	
	for i in range(0, 20):
		sb.insert(tk.END, ('test %i' % i, 'test %i' % i, 'test %i' % i))
	
	root.mainloop()