import sys, ttk
from Tkinter import *

operators = ['+', '-', '*', '/']

#* An expression tree node
class BinaryTree:
    #* Constructor to create a node
    def __init__(self, value, exp=None):
        self.value = value
        self.left = None
        self.right = None
        self.expression = exp


def constructTree(postfix):
    root = Tk()

    tree = ttk.Treeview(root)

    tree["columns"] = ("one")
    tree.column("#0", width=200)
    tree.column("one", width=300)
    # # tree.column("two", width=100)
    tree.heading("#0", text="Expression")
    tree.heading("one", text="Value")

    # tree.insert("", 0,    text="Line 1", values=("1A"))

    # id2 = tree.insert("", 1, "dir2", text="Dir 2")
    # tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A"))

    # # alternatively:
    # tree.insert("", 3, "dir3", text="Dir 3")
    # tree.insert("dir3", 3, text=" sub dir 3", values=("3A"))

    
    stack = []
    isRoot = True
    _root = 1
    _id = 1
    still_in_bracket = True

    # Traverse through every character of input expression
    for index, char in enumerate(postfix):

        # if operand, simply push into stack
        if char not in operators:
            t = BinaryTree(char)
            stack.append(t)

        # Operator
        else:

            #* Pop two top nodes
            t = BinaryTree(char)
            t1 = stack.pop()
            t2 = stack.pop()

            #* make them children
            t.right = t1
            t.left = t2
            
            #* Add this subexpression to stack
            stack.append(t)
            
            #* add to UI
            if isRoot: # because its first node need to create all of it
                tree.insert("", _id, _root, text=(t.value), values=(t.value)) # insert operator
                tree.insert(_root, _id, text=(t2.value), values=(t2.value)) # add all the children nodes
                tree.insert(_root, _id+1, text=(t1.value), values=(t1.value))
                isRoot = False

            else: # we need to set new root (new operator is new root)
                tree.insert("", _id, _root+1, text=(t.value), values=(t.value)) # create new root node

                #! check pop value that should be in current bracket !?
                if t1.value not in operators and t2.value not in operators:
                    tree.insert(_root+1, _id, text=(t2.value), values=(t2.value))
                    tree.insert(_root+1, _id+1, text=(t1.value), values=(t1.value)) # add all the children nodes
                    # still_in_bracket = True

                elif t2.value not in operators:
                    tree.insert(_root+1, _id, text=(t2.value), values=(t2.value))
                    # still_in_bracket = True
                
                elif t1.value not in operators:
                    tree.insert(_root+1, _id+1, text=(t1.value), values=(t1.value)) # add all the children nodes
                    # still_in_bracket = True
                
                else:
                    rootItems = tree.get_children()
                    currentRoot = max(rootItems)
                    for index, item in enumerate(rootItems):
                        if item != currentRoot:
                            tree.detach(item)
                            tree.reattach(item, currentRoot, _id+index)
                        # tree.detach(item)
                    # tree.detach(rootItems[0]) # detach prev root node
                    # tree.reattach(rootItems[0], rootItems[1], _id+1) # add to new root node
                    print 'other operator', t1.value, t2.value
                    still_in_bracket = True


                if still_in_bracket: # skip reattach because its operator from other bracket
                    tree.detach(_root) # detach prev root node
                    tree.reattach(_root, _root+1, _id) # add to new root node
                    print 'detach ', _root, '->', _root+1
                
                _root += 1
            
        
        #* check stack already done with bracket
        for item in stack:
            if len(stack) == 1 and item.value in operators:
                still_in_bracket = False
                print 'done bracket'

        print 'stack: ',
        for i in stack:
            print i.value,
        print ''
        print 'root position', tree.get_children()
        print index, ': ', char, ' ->', _root
        print '\n'


    # Only element will be the root of expression tree
    t = stack.pop()

    tree.pack()
    root.mainloop()

    # return t

# A utility function to do inorder traversal
def inorder(t):
    if t is not None:
        inorder(t.left)
        print t.value,
        inorder(t.right)


if __name__ == '__main__':
    input_str = sys.argv[1]
    # input_str = '251-*32*+'
    constructTree(input_str)
    # inorder(constructTree(input_str))
