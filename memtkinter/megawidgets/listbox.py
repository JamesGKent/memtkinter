import memtkinter as tk
from memtkinter import ttk

__all__ = ['Listbox']

class Listbox:
	def __init__(self):
		'''
	Scrolled Frame widgets
	can be treated as a normal tkinter frame (pack, grid, place)
	both into parent widgets and children into this widget
	'''
	def __init__(self, master, *args, **kwargs):
		'''
		name is used to implement widget memory
		scrollbars argument can be:
			both : both always visible
			x : only horizontal always visible
			y : only vertical always visible
			auto : scrollbars shown only when needed
			none : never shown
		'''
		self._scrollbars = kwargs.pop('scrollbars', None)

		self.outer_attr = set(dir(tk.Widget)) # a list of attributes that the outer frame should handle

		self.outer_frame = tk.Frame(master, 'outerframe')

		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(1, weight=1)

		self.vsb = ttk.Scrollbar(self.outer_frame, orient='vertical')
		self.hsb = ttk.Scrollbar(self.outer_frame, orient='horizontal')
		self.vsb.opts = {'column':2, 'row':1, 'sticky':'nesw'}
		self.hsb.opts = {'column':1, 'row':2, 'sticky':'nesw'}

		self.listbox = tk.Listbox(self.outer_frame)
		self.listbox.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
		self.listbox.grid(column=1, row=1, sticky='nesw')

		self.vsb.config(command=self.listbox.yview)
		self.hsb.config(command=self.listbox.xview)

		self.outer_frame.bind('<Configure>', self._reconfigure)
		
		self.listbox.bind("<Enter>", self._bind_events)
		self.listbox.bind("<Leave>", self._unbind_events)

		self._showscrollbars()
		
		for attr in ['grid_columnconfigure',
					 'grid_rowconfigure',
					 'winfo_reqwidth',
					 'winfo_reqheight',
					 'configure']: # only remove these once all widgets are set up
			self.outer_attr.discard(attr)

	def __getattr__(self, item):
		'''when an attribute is requested, sort out which frame should provide the attribute'''
		if item in self.outer_attr:
			# geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
			return getattr(self.outer_frame, item)
		else:
			# all other attributes (_w, children, etc) are passed to self.inner
			return getattr(self.listbox, item)
	
	def __repr__(self):
		return str(self.outer_frame)

	def _reconfigure(self, event=None):
		self.update_idletasks()
			
		if (self._scrollbars == 'auto'):
			self._showscrollbars()

	def _showscrollbars(self):
		if (self._scrollbars == 'both'):
			self.vsb.grid(**self.vsb.opts)
			self.hsb.grid(**self.hsb.opts)
		elif (self._scrollbars == 'x'):
			self.vsb.grid_remove()
			self.hsb.grid(**self.hsb.opts)
		elif (self._scrollbars == 'y'):
			self.vsb.grid(**self.vsb.opts)
			self.hsb.grid_remove()
		elif (self._scrollbars == 'auto'):
			l_reqsize = (
				self.listbox.winfo_reqwidth(),
				self.listbox.winfo_reqheight())
			# account for frame border
			padding = 2*int(str(self.outer_frame.cget('bd')))
			of_size = (
				self.outer_frame.winfo_width() - padding,
				self.outer_frame.winfo_height() - padding)
			print('of_size: %s' % str(of_size))
			l_size = (self.listbox.winfo_width(), self.listbox.winfo_height())
			print('l_size: %s' % str(l_size))
			vsbw = self.vsb.winfo_reqwidth()
			hsbh = self.hsb.winfo_reqheight()

			# if both smaller
			if (l_reqsize[1] <= of_size[1]) and (l_reqsize[0] <= of_size[0]):
				show_vert = False
				show_horz = False
			# if taller but narrower
			elif (l_reqsize[1] > of_size[1]) and (l_reqsize[0] <= of_size[0]):
				show_vert = True
				# if taller but narrower with scrollbar
				show_horz = (l_reqsize[0] > (of_size[0] - vsbw))
			# wider but shorter
			elif (l_reqsize[1] <= of_size[1]) and (l_reqsize[0] > of_size[0]):
				show_horz = True
				# if wider but shorter with scrollbar
				show_vert = (l_reqsize[1] > (of_size[1] - hsbh))
			else:  # both bigger
				show_vert = True
				show_horz = True

			if show_vert:
#				self.listbox.configure(width=of_size[0] - vsbw)
				self.vsb.grid(**self.vsb.opts)
			else:
				self.vsb.grid_remove()
#				self.listbox.configure(width=of_size[0])

			if show_horz:
#				self.listbox.configure(height=of_size[1] - hsbh)
				self.hsb.grid(**self.hsb.opts)
			else:
				self.hsb.grid_remove()
#				self.listbox.configure(height=of_size[1])
	
	def _bind_events(self, event=None):
		self.listbox.bind_all("<Button-4>", self.onmousewheel)
		self.listbox.bind_all("<Button-5>", self.onmousewheel)
		self.listbox.bind_all("<MouseWheel>", self.onmousewheel)
		
		self.listbox.bind_all("<Next>", self.onkeyscroll) # pagedown
		self.listbox.bind_all("<End>", self.onkeyscroll)
		
	def _unbind_events(self, event=None):
		self.listbox.unbind_all("<Button-4>")
		self.listbox.unbind_all("<Button-5>")
		self.listbox.unbind_all("<MouseWheel>")
		
		self.listbox.unbind_all("<Next>") # pagedown
		self.listbox.unbind_all("<End>")
	
	def onmousewheel(self, event):
		"""Linux uses event.num; Windows / Mac uses event.delta"""
		if event.num == 4 or event.delta == 120:
			self.listbox.yview_scroll(-1, "units" )
		elif event.num == 5 or event.delta == -120:
			self.listbox.yview_scroll(1, "units" )
		return 'break'
		
	def onkeyscroll(self, event):
		if event.keysym in ['Prior', 'Next', 'Home', 'End']:
			if (event.keysym == 'Prior'):
				self.listbox.yview('scroll', -1,'pages')
			elif (event.keysym == 'Next'):
				self.listbox.yview('scroll', 1,'pages')
			elif (event.keysym == 'Home'):
				self.listbox.yview('moveto', 0)
			elif (event.keysym == 'End'):
				self.listbox.yview('moveto', 1)
			return 'break'
		
if __name__ == '__main__':
	root = tk.Tk(None, 'test.xml', 'test')
	l = Listbox(root, scrollbars='auto')
	l.pack(fill='both', expand=True)
	for i in range(0, 10):
		l.insert(tk.END, 'item %i' % i)
	root.mainloop()
