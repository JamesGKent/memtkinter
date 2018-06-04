import memtkinter as tk
import memtkinter.ttk as ttk
from memtkinter import colorchooser
from pysettings import DummySettings

__all__ = ['ColourButton']

class ColourButton(tk.Button):
	'''
	Simple colour picker control.
	Button that uses the picked colour as background and makes text
	the complementary colour so it stands out.
	'''
	def __init__(self, master, name=None, cnf={}, **kw):
		'''
		provide a name to save between script runs.
		a command callback can be provided.
		'''
		self._command = None
		if 'command' in kw:
			self._command = kw.pop('command')
		kw['command'] = self.choosecolour
		tk.Button.__init__(self, master, cnf, **kw)
		if name:
			self.settings = DummySettings(master.settings, name, self.__get_set)
		
	def __get_set(self, colour=None):
		if colour:
			self.set(colour)
		else:
			return self.get()
		
	def choosecolour(self):
		'''
		invoked when button pushed to prompt user to select a colour
		'''
		colour = colorchooser.askcolor(initialcolor=self['bg'])[1]
		self.configure(bg=colour, fg=self.complementary(colour))
		if self._command:
			self._command()
			
	def complementary(self, colour):
		'''
		internal function used to calculate the complementary colour
		can be provided a colour name, hex code or tuple
		returns hex code
		'''
		r,g,b = self.winfo_rgb(colour)
		r,g,b = int(r/256), int(g/256), int(b/256)
		r,g,b = 255-r, 255-g, 255-b
		return '#%02x%02x%02x' % (r,g,b)#
		
	def get(self):
		'''
		get current colour
		'''
		return self['bg']
		
	def set(self, value):
		'''
		set colour, can be colour name, hex code or tuple
		'''
		self.configure(bg=colour, fg=self.complementary(colour))
			
class ColourTtkButton(ttk.Button):
	'''
	Simple colour picker control.
	ttk Button that uses the picked colour as background and makes text
	the complementary colour so it stands out.
	Note: ttk background is area around button rather than button face
	'''
	_instance_styles = []
	def __init__(self, master, **kw):
		'''
		provide a name to save between script runs.
		a command callback can be provided.
		'''
		self._command = None
		if 'command' in kw:
			self._command = kw.pop('command')
		kw['command'] = self.choosecolour
		_style = 'TButton'
		if 'style' in kw:
			_style = kw.pop('style')
		self._style = "CB%i.%s" % (len(self._instance_styles), _style)
		kw['style'] = self._style
		ttk.Button.__init__(self, master, **kw)
		
	def choosecolour(self):
		'''
		invoked when button pushed to prompt user to select a colour
		'''
		s = ttk.Style()
		kw = s.configure("%s.label" % self._style)
		if 'background' in kw:
			colour = kw['background']
		else:
			colour = 'white'
		colour = colorchooser.askcolor(initialcolor=colour)[1]
		s.configure(self._style, background=colour, foreground='red', highlightcolor='green')
#		print(s.configure(self._style))
		if self._command:
			self._command()
		
if __name__ == '__main__':
	root = tk.Tk(keytype=tk.HKCU, filepath=None, name='Software\\colourbuttontest')
	c1 = ColourButton(root, text="tkbutton", name='testtkcolourbutton')
	c1.pack(fill='both', expand=True)
	c2 = ColourTtkButton(root, text="ttkbutton")
	c2.pack(fill='both', expand=True)
	root.mainloop()
