__all__ = ['Grip']

class Grip:
	''' Makes a window dragable. '''
	def __init__ (self, parent, disable=None, releasecmd=None) :
		self.parent = parent
		self.root = parent.winfo_toplevel()
#		while True:
#			try:
#				self.root.geometry()
#				break
#			except AttributeError:
#				self.root = self.root.nametowidget(self.root.winfo_parent())
				
		self.disable = disable
		if type(disable) == 'str':
			self.disable = disable.lower()
			
		self.releaseCMD = releasecmd

		self.parent.bind('<Button-1>', self.relative_position)
		self.parent.bind('<ButtonRelease-1>', self.drag_unbind)

	def relative_position (self, event) :
		cx, cy = self.parent.winfo_pointerxy()
		geo = self.root.geometry().split("+")
		self.oriX, self.oriY = int(geo[1]), int(geo[2])
		self.relX = cx - self.oriX
		self.relY = cy - self.oriY

		self.parent.bind('<Motion>', self.drag_wid)

	def drag_wid (self, event) :
		cx, cy = self.parent.winfo_pointerxy()
		d = self.disable
		x = cx - self.relX
		y = cy - self.relY
		if d == 'x' :
			x = self.oriX
		elif d == 'y' :
			y = self.oriY
		self.root.geometry('+%i+%i' % (x, y))

	def drag_unbind (self, event) :
		self.parent.unbind('<Motion>')
		if self.releaseCMD != None :
			self.releaseCMD()