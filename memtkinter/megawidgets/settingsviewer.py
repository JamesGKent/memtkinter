import memtkinter as tk
from memtkinter import ttk

__all__ = ['SettingsViewer']

class SettingsViewer(tk.Toplevel):
	def __init__(self, master, name='settingsviewer', cnf={}, **kw):
		tk.Toplevel.__init__(self, master, name, cnf={}, **kw)
		self.protocol("WM_DELETE_WINDOW", self.withdraw)
		self.settings_root = master.settings
		headings = ['Name', 'Type', 'Value']
		self.tree = ttk.Treeview(self, columns=headings)
		self.tree.heading('#0', text='Node')
		for heading in headings:
			self.tree.heading(headings.index(heading), text=heading)
		self.tree.pack(fill=tk.BOTH, expand=True)
		ttk.Button(self, text='Refresh', command=self.refresh).pack(fill='x')
		
		self.refresh()
		
	def add_node(self, parent, node):
		p = self.tree.insert(parent, 0, text=node._name, open=True)
		for key in node._keywords:
			val = getattr(node, key)
			self.tree.insert(p, 'end', values=[key, repr(type(val)), repr(val)])
		for child in node.children:
			if node[child] != self.settings:
				self.add_node(p, node[child])
				
	def refresh(self):
		for item in self.tree.get_children():
			self.tree.delete(item)
		self.add_node('', self.settings_root)
		
if __name__ == '__main__':
	root = tk.Tk(None, './test.xml', 'test')
	
	sv = SettingsViewer(root)
	
	root.mainloop()
