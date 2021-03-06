import sys, operator
from tkinter import ttk
from tkinter import *

operators = ['+', '-', '*', '/']

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '/' : operator.truediv,
        }[op]

#* An expression tree node
class BinaryTree:
    #* Constructor to create a node
    def __init__(self, value, exp=None, res=None):
        self.value = value
        self.left = None
        self.right = None
        self.expression = exp
        self.result = res


#* create expression string for showing in UI
def createExpressionString(t1, t2, char):
    tmp_exp = ''
    if t1.value not in operators and t2.value not in operators:
        tmp_exp = str(t2.expression + char + t1.expression)
    elif t1.value not in operators:
        tmp_exp = str('(' + t2.expression + ')' + char + t1.expression)
    elif t2.value not in operators:
        tmp_exp = str(t2.expression + char + '(' + t1.expression + ')')
    else:
        tmp_exp = str('(' + t2.expression + ')' + char + '(' + t1.expression + ')')
    return tmp_exp


def calculate_result(t1, t2, char):
    op1, op2 = t1.result, t2.result
    return get_operator_fn(char)(op2, op1)


def constructTree(postfix):
    root = Tk()

    tree = ttk.Treeview(root)

    tree["columns"] = ("one")
    tree.column("#0", width=200)
    tree.column("one", width=300)
    tree.heading("#0", text="Operator/Operand")
    tree.heading("one", text="Expression")

    stack = []
    isRoot = True
    _root = 1
    _id = 1
    still_in_bracket = True

    #! Traverse through every character of input expression
    for index, char in enumerate(postfix):

        #! if operand, simply push into stack
        if char not in operators:
            t = BinaryTree(char, char, int(char))
            stack.append(t)

        #! Operator
        else:
            #* Pop two top nodes
            t1 = stack.pop()
            t2 = stack.pop()
            t = BinaryTree(char, createExpressionString(t1, t2, char), calculate_result(t1, t2, char))

            #* make them children
            t.right = t1
            t.left = t2
            
            #* Add this subexpression to stack
            stack.append(t)
            
            #* add tree to TreeView
            if isRoot: # because its first node need to create all of it
                tree.insert("", _id, _root, text=(t.value), values=(t.expression + '=' + str(t.result))) # insert operator
                tree.insert(_root, _id, text=(t2.value), values=(t2.value)) # add all the children nodes
                tree.insert(_root, _id+1, text=(t1.value), values=(t1.value))
                isRoot = False

            else: # we need to set new root (new operator is new root)
                tree.insert("", _id, _root+1, text=(t.value), values=(t.expression + '=' + str(t.result))) # create new root node

                #! check pop value that should be in current bracket !?
                if t1.value not in operators and t2.value not in operators:
                    tree.insert(_root+1, _id, text=(t2.value), values=(t2.value))
                    tree.insert(_root+1, _id+1, text=(t1.value), values=(t1.value))

                elif t2.value not in operators: # only create child node (operand) for attach to root node (operator)
                    tree.insert(_root+1, _id, text=(t2.value), values=(t2.value))
                    still_in_bracket = True # its not done yet still need to attach to root node
                
                elif t1.value not in operators: # only create child node (operand) for attach to root node (operator)
                    tree.insert(_root+1, _id+1, text=(t1.value), values=(t1.value))
                    still_in_bracket = True # its not done yet still need to attach to root node
                
                else: # put all old root nodes into the new one -> new root node that just created
                    rootItems = tree.get_children()
                    currentRoot = str(max([int(i) for i in rootItems]))
                    # print 'currentRoot:', currentRoot, ' rootIltems:',rootItems
                    for index, item in enumerate(rootItems):
                        if item != currentRoot:
                            tree.detach(item)
                            tree.reattach(item, currentRoot, _id+index)
                    # print 'other operator', t1.value, t2.value
                    # print 'currentRoot:', max(tree.get_children()), ' rootIltems:',tree.get_children()
                    still_in_bracket = True

                #! skip reattach because its operator from other bracket
                if still_in_bracket:
                    tree.detach(_root) # detach prev root node
                    tree.reattach(_root, _root+1, _id) # add to new root node
                    # print 'detach ', _root, '->', _root+1
                
                _root += 1
            
        
        #* check stack already done with bracket
        for item in stack:
            if len(stack) == 1 and item.value in operators:
                still_in_bracket = False
                # print 'done bracket'

        #? debug stuff
        # print 'stack: ',
        # for i in stack:
        #     print i.value,
        # print ''
        # print 'root position', tree.get_children()
        # print index, ': ', char, ' ->', _root
        # print '\n'

    tree.pack()
    root.mainloop()


if __name__ == '__main__':
    input_str = sys.argv[1]
    constructTree(input_str)
