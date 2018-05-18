import memtkinter as tk
import memtkinter.ttk as ttk

class CollapsibleFrame():
	'''
	Collapsible Frame widget
	use as a normal frame (pack widgets into, pack widget into parent etc.)
	shows an up or down arrow to indicate collapse state.
	'''
	def __init__(self, master, name, cnf={}, **kw):
		'''
		provide a name to save between script runs.
		'''
		self.outer_attr = set(dir(tk.Widget)) # a list of attributes that the outer frame should handle
		self.outer = tk.LabelFrame(master, name, cnf)
		self.settings = self.outer.settings
		
		self.outer.bind('<Button-1>', self._toggle)
		
		self.inner = tk.Frame(self.outer, name='inner')
		self.placeholder = tk.Label(self.outer)
		
		self.text = ''
		
		for attr in ['grid_columnconfigure',
					 'grid_rowconfigure',
					 'winfo_reqwidth',
					 'winfo_reqheight',
					 'settings']: # only remove these once all widgets are set up
			self.outer_attr.discard(attr)
		self.config(**kw)
		if not hasattr(self.settings, 'collapsed'):
			self.settings.collapsed = False
		self._show_hide()
			
	def __getattr__(self, item):
		'''when an attribute is requested, sort out which frame should provide the attribute'''
		if item in self.outer_attr:
			# geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
			return getattr(self.outer, item)
		else:
			# all other attributes (_w, children, etc) are passed to self.inner
			return getattr(self.inner, item)
			
	def __repr__(self):
		return str(self.outer)
		
	def config(self, **kw):
		if ('collapsed' in kw):
			self.settings.collapsed = kw.pop('collapsed')
		if 'text' in kw:
			self.text = kw['text']
		self.outer.config(**kw)
		
	def configure(self, **kw):
		self.config(**kw)
		
	def _toggle(self, event=None):
		'''
		toggle collapsed state
		'''
		self.settings.collapsed = not self.settings.collapsed
		self._show_hide()
		
	def _show_hide(self):
		if self.settings.collapsed:
			self.inner.pack_forget()
			self.placeholder.pack()
			symbol = '\u25BC' # down arrow
		else:
			self.placeholder.pack_forget()
			self.inner.pack(fill='both', expand='True')
			symbol = '\u25B2' # up arrow

		if self.text != '':
			text = "%s %s" % (self.text, symbol)
		else:
			text = symbol
		self.outer.configure(text=text)
		
if __name__ == '__main__':
	root = tk.Tk(keytype=tk.HKCU, filepath=None, name='Software\\CollapsibleFrametest')
	cf = CollapsibleFrame(root, 'cf', text="Test Frame")
	cf.pack()
	for i in range(0, 10):
		tk.Label(cf, text='meow').grid(column=1, row=i, sticky='nesw')
	root.mainloop()