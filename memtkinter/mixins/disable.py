

class WidgetsDisableMixin():
	def register_widget(self, widget):
		if not hasattr(self, '__widgetlist__'):
			self.__widgetlist__ = []
		if not hasattr(self, '__statedict__'):
			self.__statedict__ = {}
		if widget not in self.__widgetlist__:
			self.__widgetlist__.append(widget)
		
	def enable(self, enable=True):
		if enable:
			for widget in self.__widgetlist__:
				try:
					widget.configure(state=self.__statedict__[widget])
				except KeyError:
					pass
		else:
			self.disable()
		
	def disable(self):
		for widget in self.__widgetlist__:
			if widget['state'] != 'disabled':
				self.__statedict__[widget] = widget['state']
				widget.configure(state='disabled')