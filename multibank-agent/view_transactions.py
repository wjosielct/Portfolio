from tkinter import Toplevel
from tkinter.ttk import Treeview
import sqlite3

# ---------------------------- Helper functions ------------------------------

def executeQuery(query, parameters):
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        table = cursor.fetchall()
        conn.commit()
    
    return table

# --------------------------- Main function ----------------------------------

def onClicking_ViewTransactionsButton(root):


    # -------------------------- Start of graphical interface ---------------------------
    
    # Top level window
    topLevel_window = Toplevel(root)
    topLevel_window.title('Last 100 transactions')
    topLevel_window.resizable(width = False, height = False) # Not allow to resize the top level window
    topLevel_window.grab_set() # Disable the main window while open the top window
    
    # Table
    columns = ('Transaction Id', 'Entity type', 'Entity', 'Operation', 'Amount', 'Commission', 'Total', 'Transaction time')
    tree = Treeview(topLevel_window, columns = columns, show = 'headings')

    for column in columns:
        tree.heading(column, text = column)
        tree.column(column, width = 150, anchor = 'e')

    tree.pack(padx = 10, pady = 10)
    
    query = 'SELECT * FROM transactions ORDER BY transaction_id DESC LIMIT 100;'
    table = executeQuery(query, parameters = ())
    
    for row in table:
        tree.insert("", "end", values = row)