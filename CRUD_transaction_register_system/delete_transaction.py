from tkinter import Toplevel, Label, StringVar, Entry, Button
from tkinter.simpledialog import askinteger
import tkinter.messagebox as messagebox
import sqlite3


# ------------------------ Helper functions ---------------------------

def executeQuery(query, parameters):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        table = cursor.fetchall()
        conn.commit()
    return table

def validateTransactionId(transactionId):
    
    if transactionId == None:
        valid_transactionId = False
        validation_message = 'Operation cancelled'
    
    elif transactionId <= 0:
        valid_transactionId = False
        validation_message = 'Transaction id must be positive'
    
    else:
        query = 'SELECT * FROM transactions WHERE transaction_id = ?;'
        parameters = (transactionId, )
        result = executeQuery(query, parameters)
        
        if len(result) == 1:
            valid_transactionId = True
            validation_message = 'Transaction Id found'
        
        else:
            valid_transactionId = False
            validation_message = 'Transaction Id not found in database'
    
    return valid_transactionId, validation_message


# ------------------------------- Main function -----------------------------------------

def onClicking_DeleteTransactionButton(root):
    
    # ---------------------------- Internal functions ------------------------------------
    
    def onClicking_RemoveTransactionButton():
        
        response = messagebox.askyesno("Delete transaction", "¿Do you want to delete the transaction?")
        
        if response:
            query = 'DELETE FROM transactions WHERE transaction_id = ?;'
            executeQuery(query, (transactionId, ))
            topLevel_window.destroy()
            messagebox.showinfo('Transaction was deleted', 'The transaction was successfully deleted')
    
    
    # --------------------- Asking to input a transaction id -----------------------------
    
    transactionId = askinteger("Required information", "Enter a transaction id:")
    
    valid_transactionId, validation_message = validateTransactionId(transactionId)
    
    if valid_transactionId:

        # ----------------------------- Start of graphical interface --------------------
        
        # Top level window
        topLevel_window = Toplevel(root)
        topLevel_window.title('Delete a transaction')
        topLevel_window.resizable(width = False, height = False) # Not allow to resize the top level window
        topLevel_window.grab_set() # Disable the main window while open the top window

        # ------------------- Column 0 -------------------------------------------------------
        Label(topLevel_window, text = 'Transaction Id:').grid(row = 0, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Entity type:').grid(row = 1, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Entity:').grid(row = 2, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Operation:').grid(row = 3, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Amount (S/):').grid(row = 4, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Commission (S/):').grid(row = 5, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Total (S/):').grid(row = 6, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Time:').grid(row = 7, column = 0, sticky = 'e')

        # ------------------- Column 1 --------------------------------------------------------
        
        #Getting data from transaction
        result = executeQuery('SELECT * FROM transactions WHERE transaction_id = ?;', parameters = (transactionId, ))
        
        # Transaction id section
        transactionId_entry_text = StringVar()
        transactionId_entry_text.set(transactionId)
        transactionId_entry = Entry(topLevel_window, textvariable = transactionId_entry_text, state = 'readonly', width = 30)
        transactionId_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        # Entity type section
        entityType_entry_text = StringVar()
        entityType_entry_text.set(result[0][1])
        entityType_entry = Entry(topLevel_window, textvariable = entityType_entry_text, state = 'readonly', width = 30)
        entityType_entry.grid(row = 1, column = 1, padx = 5, pady = 5)

        # Entity section
        entity_entry_text = StringVar()
        entity_entry_text.set(result[0][2])
        entity_entry = Entry(topLevel_window, textvariable = entity_entry_text, state = 'readonly', width = 30)
        entity_entry.grid(row = 2, column = 1, padx = 5, pady = 5)

        # Operation section
        operation_entry_text = StringVar()
        operation_entry_text.set(result[0][3])
        operation_entry = Entry(topLevel_window, textvariable = operation_entry_text, state = 'readonly', width = 30)
        operation_entry.grid(row = 3, column = 1, padx = 5, pady = 5)

        # Amount section
        amount_entry_text = StringVar()
        amount_entry_text.set(result[0][4])
        amount_entry = Entry(topLevel_window, textvariable = amount_entry_text, state = 'readonly', width = 30)
        amount_entry.grid(row = 4, column = 1, padx = 5, pady = 5)

        # Commission section
        commission_entry_text = StringVar()
        commission_entry_text.set(result[0][5])
        commission_entry = Entry(topLevel_window, textvariable = commission_entry_text, state = 'readonly', width = 30)
        commission_entry.grid(row = 5, column = 1, padx = 5, pady = 5)

        # Total section
        total_entry_text = StringVar()
        total_entry_text.set(result[0][6])
        total_entry = Entry(topLevel_window, textvariable = total_entry_text, state = 'readonly', width = 30)
        total_entry.grid(row = 6, column = 1, padx = 5, pady = 5)

        # Time section
        time_entry_text = StringVar()
        time_entry_text.set(result[0][7])
        time_entry = Entry(topLevel_window, textvariable = time_entry_text, state = 'readonly', width = 30)
        time_entry.grid(row = 7, column = 1, padx = 5, pady = 5)

        # remove transaction Button
        Button(topLevel_window, text = 'Remove transaction', command = onClicking_RemoveTransactionButton).grid(row = 8, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'we')

    else:
        messagebox.showerror('Something is wrong', validation_message)