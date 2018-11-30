import memtkinter as tk
from memtkinter.megawidgets import Listbox

if __name__ == '__main__':
	root = tk.Tk(tk.HKCU, './test.xml', 'test')
	l = Listbox(root, scrollbars='auto')
	l.pack(fill='both', expand=True)
	for i in range(0, 10):
		l.insert(tk.END, 'item %i' % i)
	root.mainloop()