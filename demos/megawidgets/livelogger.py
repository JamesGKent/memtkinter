import memtkinter as tk
from memtkinter.megawidgets import LiveLogger

if __name__ == '__main__':
	def normal():
		print('normal text\n')
		
	def special():
		logger.write('special\n', 'special text')
		
	def error():
		a = b
		
	root = tk.Tk(keytype=tk.HKCU, filepath='./livelogpath', name='Software\\livelogapp')
	
	tk.Button(root, text='normal', command=normal).pack()
	tk.Button(root, text='special', command=special).pack()
	tk.Button(root, text='error', command=error).pack()
	
	logger = LiveLogger(root, 'livelogger')
	
	logger.add_stream('special', None, {'foreground':'green'})
	root.mainloop()
