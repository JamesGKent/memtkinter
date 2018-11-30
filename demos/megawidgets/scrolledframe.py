import memtkinter as tk
from memtkinter.megawidgets import ScrolledFrame

if __name__ == '__main__':
	root = tk.Tk(keytype=tk.HKCU, filepath=None, name='Software\\ScrolledFrametest')
	sf = ScrolledFrame(root, 'cf', scrollbars='auto')
	sf.pack(fill='both', expand=True)
	for i in range(0, 10):
		tk.Label(sf, text='Test %i' % i).grid(column=1, row=i, sticky='nesw')
	root.mainloop()
