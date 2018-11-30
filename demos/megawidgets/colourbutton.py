import memtkinter as tk
from memtkinter.megawidgets import ColourButton

if __name__ == '__main__':
	root = tk.Tk(keytype=tk.HKCU, filepath=None, name='Software\\colourbuttontest')
	c1 = ColourButton(root, text="tkbutton", name='testtkcolourbutton')
	c1.pack(fill='both', expand=True)
	root.mainloop()
