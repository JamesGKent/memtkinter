from pysettings import *

try:
	from tkinter.ttk  import * # bring all widgets into local namespace
	from tkinter import ttk # use this ref to subclass
except ImportError:
	# path manipulation needed to ensure that tkinter ttk is loaded
	# otherwise python2 does relative import and tries to import this file
	import sys
	for item in sys.path:
		if item.endswith('lib-tk'):
			sys.path.insert(0, item)
			break
	if not sys.path[0].endswith('lib-tk'):
		raise ImportError('tkinter library path not found')
	mod = sys.modules.pop('memtkinter.ttk')
	ttk = __import__('ttk') # use this ref to subclass
	for k in dir(ttk): # bring all widgets into local namespace
		locals()[k] = getattr(ttk, k)
	sys.modules['memtkinter.ttk'] = mod
	
class Frame(ttk.Frame):
	def __init__(self, master, name, **kw):
		ttk.Frame.__init__(self, master, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
class Labelframe(ttk.Labelframe):
	def __init__(self, master, name, **kw):
		ttk.Labelframe.__init__(self, master, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
LabelFrame = Labelframe
		
class Notebook(ttk.Notebook):
	def __init__(self, master, name, **kw):
		ttk.Notebook.__init__(self, master, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
	def add(self, child, **kw):
		ttk.Notebook.add(self, child, **kw)
		# probably need to map settings here
		
class Panedwindow(ttk.Panedwindow):
	def __init__(self, master, name, **kw):
		ttk.Panedwindow.__init__(self, master, **kw)
		self._num_panes = 0
		self.settings = Settings(name=name, parent=master.settings)
		self.sash_locations = []
		self.settings.sashes = self.sashes_locations
		
	def add(self, child, **kw):
		ttk.Panedwindow.add(self, child, **kw)
		self._num_panes += 1
		if self._num_panes >= 2:
			if len(self.sash_locations) >= (self._num_panes-1):
				self.update() # hacky but doesn't work without update, idletasks isn't enough
				self.sashpos(self._num_panes-2, self.sash_locations[self._num_panes-2])
		
	def remove(self, child):
		ttk.Panedwindow.remove(self, child)
		self._num_panes -= 1
		
	def sashes_locations(self, locations=None):
		if locations:
			self.sash_locations = locations
		else:
			self.sash_locations = []
			for num in range(0, self._num_panes-1):
				self.sash_locations.append(self.sashpos(num))
			return self.sash_locations
		
PanedWindow = Panedwindow

class Checkbutton(ttk.Checkbutton):
	def __init__(self, master, name=None, **kw):
		ttk.Checkbutton.__init__(self, master, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.set(value)
		else:
			return self.get()
			
class Entry(ttk.Entry):
	def __init__(self, master, name=None, cnf={}, **kw):
		ttk.Entry.__init__(self, master, cnf, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.delete(0, 'end')
			self.insert('end', value)
		else:
			return self.get()

class Combobox(ttk.Combobox):
	def __init__(self, master, name=None, **kw):
		ttk.Combobox.__init__(self, master, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			state = self['state']
			self.configure(state='normal')
			self.delete(0, 'end')
			self.insert('end', value)
			self.configure(state=state)
		else:
			return self.get()

class Radiobutton(ttk.Radiobutton):
	def __init__(self, master, name=None, cnf={}, **kw):
		ttk.Radiobutton.__init__(self, master, cnf, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		pass
		
class Scale(ttk.Scale):
	def __init__(self, master, name=None, **kw):
		ttk.Scale.__init__(self, master, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.set(value)
		else:
			return self.get()
			
class LabeledScale(ttk.LabeledScale):
	def __init__(self, master, name=None, variable=None, from_=0, to=10, **kw):
		ttk.LabeledScale.__init__(self, master, variable, from_, to, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.scale.set(value)
		else:
			return self.scale.get()