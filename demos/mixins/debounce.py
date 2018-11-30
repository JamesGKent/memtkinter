import memtkinter as tk
from memtkinter.mixins.debounce import DebounceFrame

if __name__ == '__main__':
	def instance_press(event):
		print("instance_press:\t%s\t%s" % (event.widget, event.keysym))
		
	def instance_release(event):
		print("instance_release:\t%s\t%s" % (event.widget, event.keysym))
		
	def class_press(event):
		print("class_press:\t%s\t%s" % (event.widget, event.keysym))
		
	def class_release(event):
		print("class_release:\t%s\t%s" % (event.widget, event.keysym))
		
	def all_press(event):
		print("all_press:\t%s\t%s" % (event.widget, event.keysym))
		
	def all_release(event):
		print("all_release:\t%s\t%s" % (event.widget, event.keysym))

	root = tk.Tk(keytype=tk.HKCU, filepath='./test.xml', name='Software\\debouncetest')
	frame = DebounceFrame(root, width=100, height=100, bg='red', takefocus=True)
	frame2 = DebounceFrame(root, width=100, height=100, bg='blue', takefocus=True)
	frame.bind("<KeyPress-a>", instance_press, False)
	frame.bind("<KeyRelease-a>", instance_release, False)
	frame.bind("<KeyPress-s>", instance_press)
	frame.bind("<KeyRelease-s>", instance_release)
	
	frame.bind_class("<KeyPress-d>", class_press)
	frame.bind_class("<KeyRelease-d>", class_release)
	
	frame.bind_all('<KeyPress-F1>', all_press)
	frame.bind_all('<KeyRelease-F1>', all_release)

	frame2.bind("<KeyPress-f>", instance_press)
	frame2.bind("<KeyRelease-f>", instance_release)

	frame.pack()
	frame2.pack()
	frame.focus_set()

	root.mainloop()