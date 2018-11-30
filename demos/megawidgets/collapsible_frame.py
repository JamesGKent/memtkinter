import memtkinter as tk
from memtkinter.megawidgets import CollapsibleFrame

if __name__ == '__main__':
	root = tk.Tk(keytype=tk.HKCU, filepath=None, name='Software\\CollapsibleFrametest')
	cf = CollapsibleFrame(root, 'cf', text="Test Frame")
	cf.pack()
	for i in range(0, 10):
		tk.Label(cf, text='Test %i' % i).grid(column=1, row=i, sticky='nesw')
	root.mainloop()