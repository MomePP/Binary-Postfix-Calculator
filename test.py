from Tkinter import *
import ttk

root = Tk()

tree = ttk.Treeview(root)

tree["columns"] = ("one")
tree.column("one", width=300)
# tree.column("two", width=100)
# tree.heading("one", text="coulmn A")

tree.insert("", 0,    text="Line 1", values=("1A"))

id2 = tree.insert("", 1, "dir2", text="Dir 2")
tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A"))

# alternatively:
tree.insert("", 3, "dir3", text="Dir 3")
tree.insert("dir3", 3, text=" sub dir 3", values=("3A"))

tree.pack()
root.mainloop()
