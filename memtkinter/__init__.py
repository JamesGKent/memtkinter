from pysettings import *

try:
	from tkinter import * # bring all widgets into local namespace
	import tkinter as tk # use this ref to subclass
except ImportError:
	from Tkinter import * # bring all widgets into local namespace
	import Tkinter as tk # use this ref to subclass
	
class Tk(tk.Tk):
	def __init__(self, keytype, filepath, name, screenName=None, baseName=None, className='Tk',
                 useTk=1, sync=0, use=None):
		tk.Tk.__init__(self, screenName=None, baseName=None, className='Tk',
                 useTk=1, sync=0, use=None)
		self.settings = Settings(keytype=keytype, filepath=filepath, name=name)
		self.settings.geometry = self.geometry
		self.settings.wm_state = self.wm_state
		self.settings.overrideredirect = self.overrideredirect
		
	def destroy(self):
		self.settings.save()
		tk.Tk.destroy(self)
		
class Toplevel(tk.Toplevel):
	def __init__(self, master, name, cnf={}, **kw):
		tk.Toplevel.__init__(self, master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		self.settings.geometry = self.geometry
		self.settings.wm_state = self.wm_state
		self.settings.overrideredirect = self.overrideredirect
		
#	def destroy(self):
#		self.master.settings.save()
#		tk.Toplevel.destroy(self)
		
class Frame(tk.Frame):
	def __init__(self, master, name, cnf={}, **kw):
		tk.Frame.__init__(self, master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)

class Canvas(tk.Canvas):
	def __init__(self, master, name, cnf={}, **kw):
		tk.Canvas.__init__(self, master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
class LabelFrame(tk.LabelFrame):
	def __init__(self, master, name, cnf={}, **kw):
		tk.LabelFrame.__init__(self, master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
class PanedWindow(tk.PanedWindow):
	def __init__(self, master, name, cnf={}, **kw):
		tk.PanedWindow.__init__(self, master, cnf, **kw)
		self._num_panes = 0
		self.settings = Settings(name=name, parent=master.settings)
		self.sash_locations = []
		self.settings.sashes = self.sashes_locations
		
	def add(self, child, **kw):
		tk.PanedWindow.add(self, child, **kw)
		self._num_panes += 1
		if self._num_panes >= 2:
			if len(self.sash_locations) >= (self._num_panes-1):
				self.update() # hacky but doesn't work without update, idletasks isn't enough
				self.sash_place(self._num_panes-2, *self.sash_locations[self._num_panes-2])
		
	def remove(self, child):
		tk.PanedWindow.remove(self, child)
		self._num_panes -= 1
		
	def sashes_locations(self, locations=None):
		if locations:
			self.sash_locations = locations
		else:
			self.sash_locations = []
			for num in range(0, self._num_panes-1):
				self.sash_locations.append(self.sash_coord(num))
			return self.sash_locations

class Checkbutton(tk.Checkbutton):
	def __init__(self, master, name=None, cnf={}, **kw):
		self._internalvar = tk.IntVar()
		self._internalvar.trace('w', self.__intvartrace)
		self._variable = kw.pop('variable', None)
		if self._variable:
			self._variable.trace('w', self.__vartrace)
		kw['variable'] = self._internalvar
		tk.Checkbutton.__init__(self, master, cnf, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.set(value)
		else:
			return self.get()

	def __vartrace(self, *args):
		self._internalvar.set(self._variable.get())
		
	def __intvartrace(self, *args):
		if self._variable:
			self._variable.set(self._internalvar.get())
			
	def get(self):
		return self._internalvar.get()
		
	def set(self, value):
		self._internalvar.set(value)
	
class Entry(tk.Entry):
	def __init__(self, master, name=None, cnf={}, **kw):
		tk.Entry.__init__(self, master, cnf, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			s = self.cget('state')
			self.configure(state='normal')
			self.delete(0, tk.END)
			self.insert(tk.END, value)
			self.configure(state=s)
		else:
			return self.get()
			
	def destroy(self):
		if hasattr(self, 'settings'):
			self.settings.delete()
		tk.Entry.destroy(self)

class Radiobutton(tk.Radiobutton):
	def __init__(self, master, name, cnf={}, **kw):
		try:
			self._variable = kw['variable']
		except KeyError:
			self._variable = None
		tk.Radiobutton.__init__(self, master, cnf, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set, False)
			
	def __get_set(self, value=None):
		if value:
			self._variable.set(value)
		else:
			return self._variable.get()
			
	def destroy(self):
		if hasattr(self, 'settings'):
			self.settings.delete()
		tk.Radiobutton.destroy(self)

class Scale(tk.Scale):
	def __init__(self, master, name=None, cnf={}, **kw):
		tk.Scale.__init__(self, master, cnf, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.set(value)
		else:
			return self.get()
	
	def destroy(self):
		if hasattr(self, 'settings'):
			self.settings.delete()
		tk.Scale.destroy(self)
			
class Text(tk.Text):
	def __init__(self, master, name=None, cnf={}, **kw):
		tk.Text.__init__(self, master, cnf, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.delete(0.0, tk.END)
			self.insert(tk.END, value)
		else:
			value = self.get(0.0, tk.END)
			if value.endswith('\n'):
				value = value[:-1]
			return value
			
	def destroy(self):
		if hasattr(self, 'settings'):
			self.settings.delete()
		tk.Text.destroy(self)
			
class Spinbox(tk.Spinbox):
	def __init__(self, master, name=None, cnf={}, **kw):
		self._internalvar = tk.StringVar()
		self._internalvar.trace('w', self.__intvartrace)
		self._variable = kw.pop('variable', None)
		if self._variable:
			self._variable.trace('w', self.__vartrace)
		self._textvariable = kw.pop('textvariable', None)
		if self._textvariable:
			self._textvariable.trace('w', self.__textvartrace)
		kw['textvariable'] = self._internalvar
		tk.Spinbox.__init__(self, master, cnf, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.set(value)
		else:
			return self.get()

	def __vartrace(self, *args):
		self._internalvar.set(self._variable.get())
		
	def __textvartrace(self, *args):
		self._internalvar.set(self._textvariable.get())
		
	def __intvartrace(self, *args):
		if self._variable:
			self._variable.set(self._internalvar.get())
		if self._textvariable:
			self._textvariable.set(self._internalvar.get())
			
	def get(self):
		return self._internalvar.get()
		
	def set(self, value):
		self._internalvar.set(value)
		
	def destroy(self):
		if hasattr(self, 'settings'):
			self.settings.delete()
		tk.Spinbox.destroy(self)