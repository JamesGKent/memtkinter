import memtkinter as tk
from memtkinter.scrolledtext import ScrolledText
from memtkinter import messagebox
import sys

class DummyPipe():
	'''
	dummy class to capture output
	create pipes using:
		pipe = DummyPipe(logger, name)
	then use either as:
		print(something, file=pipe)
	or:
		pipe.write(something)
	'''
	def __init__(self, logger, streamname):
		self.logger = logger
		self.streamname = streamname
	
	def write(self, buf):
		self.logger.write(buf, self.streamname)
		
	def flush(self):
		pass

class LogText(ScrolledText):
	'''
	ScrolledText subclass, can tell when view is at the bottom
	will then scroll with new text
	if scroll away from bottom stays where scrolled to.
	'''
	def __init__(self, master, **kw):
		ScrolledText.__init__(self, master, **kw)
		self.configure(yscrollcommand=self.vbarset)
		self.at_end = True
		
	def vbarset(self, *args):
		if (float(args[1]) == 1.0):
			self.at_end = True
		else:
			self.at_end = False
		self.vbar.set(*args)
		
	def yview(self, *args):
		if (float(args[1]) == 1.0):
			self.at_end = True
		else:
			self.at_end = False
		ScrolledText.yview(self, *args)
		
	def insert(self, index, chars, *args):
		ScrolledText.insert(index, chars, *args)
		if self.at_end:
			self.see(tk.END)

class LiveLogger(tk.Toplevel):
	'''
	Logger window, hides unless error occurs or commanded to show
	'''
	error_types = ["Error", "Exit", "StopIteration"]
	def __init__(self, master, name, cnf={}, **kw):
		tk.Toplevel.__init__(self, master, name, cnf, **kw)
		self.withdraw()
		self.protocol('WM_DELETE_WINDOW', self.withdraw)
		self.logwindow = LogText(self)
		self.logwindow.grid(column=1, row=1, sticky='nesw')
		
		self.streams = {}
		
		for name, buffer, config in [
			('stdout', sys.stdout, {'foreground':'blue',}),
			('stderr', sys.stderr, {'foreground':'red',})
			]:
			self.add_stream(name, buffer, config)

		sys.stdout = DummyPipe(self, 'stdout') # override system wide pipes to catch output
		sys.stderr = DummyPipe(self, 'stderr')
		
	def withdraw(self):
		tk.Toplevel.withdraw(self)
		self.shown = False
		
	def deiconify(self):
		tk.Toplevel.deiconify(self)
		self.shown = True
		
	def add_stream(self, name, buffer, config):
		'''
		add a stream to logger
		must have unique name
		can direct output to another stream using buffer arg
		config is a dict to set the tag config (foreground etc)
		'''
		self.logwindow.tag_configure(name, config)
		if buffer:
			self.streams[name] = buffer
		
	def write(self, buf, stream):
		if stream in self.streams:
			self.streams[stream].write(buf)

		self.logwindow.insert(tk.END, buf, stream)
		if not self.shown:
			if stream == "stderr":
				for entry in self.error_types:
					if entry in str(buf):
						res = messagebox.askyesno("Error", 'An error has occurred, show error log?')
						if res:
							self.deiconify()
		
	def flush(self):
		pass
		
if __name__ == '__main__':
	def normal():
		print("normal text\n")
		
	def special():
		logger.write('special', 'special text')
		
	def error():
		a = b
		
	root = tk.Tk(keytype=tk.HKCU, filepath='./livelogpath', name='Software\\livelogapp')
	
	tk.Button(root, text="normal", command=normal).pack()
	tk.Button(root, text="special", command=special).pack()
	tk.Button(root, text="error", command=error).pack()
	
	logger = LiveLogger(root, 'livelogger')
	
	logger.add_stream('special', None, {'foreground':'green'})
	root.mainloop()