from pysettings import Settings, HKLM, HKCU

try:
	from tkinter.tix  import * # bring all widgets into local namespace
	from tkinter import tix # use this ref to subclass
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
	mod = sys.modules.pop('memtkinter.tix')
	tix = __import__('tix') # use this ref to subclass
	for k in dir(tix): # bring all widgets into local namespace
		locals()[k] = getattr(tix, k)
	sys.modules['memtkinter.tix'] = mod
	
from memtkinter import Frame
	
class Tk(tix.Tk):
	def __init__(self, keytype, filepath, name, screenName=None, baseName=None, className='Tix'):
		super().__init__(screenName, baseName, className)
		self.settings = Settings(keytype=keytype, filepath=filepath, name=name)
		self.settings.geometry = self.geometry
		
	def destroy(self):
		self.settings.save()
		super().destroy()

class LabelFrame(tix.LabelFrame):
	def __init__(self, master, name, cnf={}, **kw):
		super().__init__(master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
class ListNoteBook(tix.ListNoteBook):
	def __init__(self, master, name, cnf={}, **kw):
		super().__init__(master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
	def add(self, name, cnf={}, **kw):
		frame = super().add(name, cnf, **kw)
		frame.settings = Settings(name=name, parent=self.settings)
		return frame
		
class NoteBook(tix.NoteBook):
	def __init__(self, master, name, cnf={}, **kw):
		super().__init__(master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
	def add(self, name, cnf={}, **kw):
		frame = super().add(name, cnf, **kw)
		frame.settings = Settings(name=name, parent=self.settings)
		return frame
		
class PanedWindow(tix.PanedWindow):
	def __init__(self, master, name, cnf={}, **kw):
		super().__init__(master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
	def add(self, name, cnf={}, **kw):
		frame = super().add(name, cnf **kw)
		frame.settings = Settings(name=name, parent=self.settings)
		
class ScrolledWindow(tix.ScrolledWindow):
	def __init__(self, master, name, cnf={}, **kw):
		super().__init__(master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		
class ComboBox(tix.ComboBox):
	def __init__(self, master, name, cnf={}, **kw):
		super().__init__(master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		self.settings.__setattr__(name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.entry.delete(0, 'end')
			self.entry.insert('end', value)
		else:
			return self.entry.get()
			
class Control(tix.Control):
	def __init__(self, master, name, cnf={}, **kw):
		super().__init__(master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		self.settings.__setattr__(name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.entry.delete(0, 'end')
			self.entry.insert('end', value)
		else:
			return self.entry.get()
			
class DirSelectBox(tix.DirSelectBox):
	def __init__(self, master, name, cnf={}, **kw):
		super().__init__(master, cnf, **kw)
		self.settings = Settings(name=name, parent=master.settings)
		self.settings.__setattr__(name, self.__get_set)
		
	def __get_set(self, value=None):
		if value:
			self.selection.set(value)
		else:
			return self.selection.get()