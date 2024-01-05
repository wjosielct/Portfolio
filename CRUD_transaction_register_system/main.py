from tkinter import Tk, Button, LabelFrame
from register_transaction import onClicking_RegisterTransactionButton
from edit_transaction import onClicking_EditTransactionButton
from delete_transaction import onClicking_DeleteTransactionButton
from view_transactions import onClicking_ViewTransactionsButton

# -------------------------- Start of graphical interface -------------------------------------------------

# Main window
root = Tk()
root.title('Operations')
root.resizable(width = False, height = False) # Not allow to resize the main window

# Label frame
lf = LabelFrame(root, text = 'Choose a operation', borderwidth = 3, relief = 'solid')
lf.pack(padx = 5, pady = 5)

# Operation buttons
Button(lf, text = 'Register transaction', command = lambda : onClicking_RegisterTransactionButton(root), width = 30).grid(row = 0, column = 0, padx = 10, pady = 10)
Button(lf, text = 'Edit transaction', command = lambda :onClicking_EditTransactionButton(root), width = 30).grid(row = 1, column = 0, padx = 10, pady = 10)
Button(lf, text = 'Delete transaction', command = lambda :onClicking_DeleteTransactionButton(root), width = 30).grid(row = 2, column = 0, padx = 10, pady = 10)
Button(lf, text = 'View last 100 transactions', command = lambda :onClicking_ViewTransactionsButton(root), width = 30).grid(row = 3, column = 0, padx = 10, pady = 10)

root.mainloop()