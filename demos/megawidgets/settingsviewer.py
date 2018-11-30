import memtkinter as tk
from memtkinter.megawidgets import SettingsViewer

if __name__ == '__main__':
	root = tk.Tk(keytype=tk.HKCU, filepath='./test.xml', name='test')
	
	sv = SettingsViewer(root)
	
	root.mainloop()