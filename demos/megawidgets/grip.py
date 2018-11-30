import memtkinter as tk
from memtkinter.megawidgets import Grip


if __name__ == '__main__':
	root = tk.Tk(keytype=tk.HKCU, filepath=None, name='Software\\griptest')
	
	# this could be any type of widget as long as it has a non zero size
	# i.e. it can be clicked on.
	griplabel = tk.Label(root, text='click and drag to move')
	griplabel.pack()
	grip = Grip(griplabel)
	
	root.mainloop()