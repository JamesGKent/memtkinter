import memtkinter as tk
from memtkinter.mixins import MultiColumnListboxScrollbar

if __name__ == '__main__':
	root = tk.Tk(tk.HKCU, './test.xml', 'Software\\Multiwidgetscrolltest')
	root.grid_columnconfigure(1, weight=1)
	root.grid_columnconfigure(2, weight=1)
	root.grid_columnconfigure(3, weight=1)
	
	root.grid_rowconfigure(1, weight=1)
	
	selmode = tk.EXTENDED
	l1 = tk.Listbox(root, selectmode=selmode)
	l1.grid(column=1, row=1, sticky='nesw')
	l2 = tk.Listbox(root, selectmode=selmode)
	l2.grid(column=2, row=1, sticky='nesw')
	l3 = tk.Listbox(root, selectmode=selmode)
	l3.grid(column=3, row=1, sticky='nesw')
	
	sb = MultiColumnListboxScrollbar(root)
	sb.grid(column=10, row=1, sticky='nesw')
	sb.add_listbox(l1)
	sb.add_listbox(l2)
	sb.add_listbox(l3)
	
	for i in range(0, 20):
		sb.insert(tk.END, ('test %i' % i, 'test %i' % i, 'test %i' % i))
	
	root.mainloop()