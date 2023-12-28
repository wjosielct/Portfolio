import sqlite3
from tkinter import Toplevel, Label, StringVar, Entry, Button
from tkinter.ttk import Combobox
from tkinter.simpledialog import askinteger
import tkinter.messagebox as messagebox
from datetime import datetime

# ------------------------------- Global variables ----------------------------------

entityTypes = ["Banks", "Utility companies"]
banks = ["BCP", "Interbank", "BBVA", "ScotiaBank"]
utilityCompanies = ["SEDAPAL", "Edelnor", "Calidda"]

# ------------------------------ Helper functions -----------------------------------

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

# ---------------------------------- Main function -----------------------------------

def onClicking_EditTransactionButton(root):

    # -------------------------- Internal functions -----------------------------------------
    
    def validateTransactionData():
        valid_data = False
        
        if entityType_cb_new_text.get() == 'Select an entity type':
            validation_message = 'Entity type is required'
        
        elif entity_cb_new_text.get() in ['', 'Select a bank', 'Select a utility company']:
            validation_message = 'Entity is required'
        
        elif operation_cb_new_text.get() in ['', 'Select bank operation', 'Select utility company operation']:
            validation_message = 'Operation is required'
        
        elif amount_entry_new_text.get() == '':
            validation_message = 'Amount is required'
        
        elif commission_entry_new_text.get() == 'Error':
            validation_message = 'Insert a valid amount'
        
        elif float(amount_entry_new_text.get()) <= 0:
            validation_message = 'Insert an amount greater than 0'
        
        else:
            validation_message = 'Successful validation'
            valid_data = True
        
        return valid_data, validation_message

    
    def onClicking_UpdateTransactionButton():
        
        valid_data, validation_message = validateTransactionData()
        
        if valid_data:
            response = messagebox.askyesno("Question", "Do you want to update this transaction?")
            
            if response:
                query = 'UPDATE transactions SET entity_type = ?, entity_name = ?, operation_type = ?, amount = ?, commission = ?, total = ?, time = ? WHERE transaction_id = ?;'
                entity_type = entityType_cb_new_text.get()
                entity_name = entity_cb_new_text.get()
                operation_type = operation_cb_new_text.get()
                amount_value = amount_entry_new_text.get()
                commission_value = commission_entry_new_text.get()
                total_value = total_entry_new_text.get()
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #Get the current time
                parameters = (entity_type, entity_name, operation_type, amount_value, commission_value, total_value, current_time, transactionId)
                executeQuery(query, parameters)
                topLevel_window.destroy()
                messagebox.showinfo('Inportant information', 'The transaction has been successfully updated')
        
        else:
            messagebox.showerror("Something is wrong", validation_message)
    
    
    def onEntityTypeSelected(event):
        
        operation_cb_new_text.set('')
        operation_cb_new['values'] = '' # Setting the list of values of the combo box
        selectedEntityType = entityType_cb_new_text.get()
        
        if selectedEntityType == "Banks":
            entity_cb_new_text.set("Select a bank")
            entity_cb_new['values'] = banks # Setting the list of values of the combo box
            
        elif selectedEntityType == "Utility companies":
            entity_cb_new_text.set("Select a utility company")
            entity_cb_new['values'] = utilityCompanies # Setting the list of values of the combo box

    
    def onEntitySelected(event):
        
        selectedEntityType = entityType_cb_new_text.get()
        
        if selectedEntityType == "Banks":
            operation_cb_new_text.set('Select bank operation')
            operation_cb_new['values'] = ['Drawback', 'Deposit'] # Setting the list of values of the combo box

        elif selectedEntityType == "Utility companies":
            operation_cb_new_text.set('Select utility company operation')
            operation_cb_new['values'] = ['Bill payment'] # Setting the list of values of the combo box

    
    def onInsertionOfText(event):
        
        try:
            amount = float(amount_entry_new_text.get())
            commission = round(amount * 0.01, 2)
            total = round(amount + commission, 2)
            
            # Update the comission entry
            commission_entry_new['fg'] = 'blue'
            commission_entry_new_text.set(commission)

            # Udate the total entry
            total_entry_new['fg'] = 'blue'
            total_entry_new_text.set(total)
        
        except ValueError as e:
            
            if amount_entry_new_text.get() == '':
                commission_entry_new_text.set('')
                total_entry_new_text.set('')
            
            else:
                commission_entry_new['fg'] = 'red'
                commission_entry_new_text.set('Error')

                total_entry_new['fg'] = 'red'
                total_entry_new_text.set('Error')

    
    # --------------------- Asking to input a transaction id ----------------------
    
    transactionId = askinteger("Required information", "Enter a transaction id:")
    
    valid_transactionId, validation_message = validateTransactionId(transactionId)
    
    if valid_transactionId:

        # ------------------ Start of graphical interface --------------------------------
        
        # Top level window
        topLevel_window = Toplevel(root)
        topLevel_window.title('Update a transaction')
        topLevel_window.resizable(width = False, height = False) # Not allow to resize the top window
        topLevel_window.grab_set() # Disable the main window while open the top window

        # ------------------- Column 0 ---------------------------------------------------
        
        Label(topLevel_window, text = 'Entity type:').grid(row = 1, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Entity:').grid(row = 2, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Operation:').grid(row = 3, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Amount (S/):').grid(row = 4, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Commission (S/):').grid(row = 5, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Total (S/):').grid(row = 6, column = 0, sticky = 'e')
        Label(topLevel_window, text = 'Time:').grid(row = 7, column = 0, sticky = 'e')

        # ------------------- Column 1 ---------------------------------------------------
        
        Label(topLevel_window, text = f'OLD info for transaction Id {transactionId}:').grid(row = 0, column = 1)

        #Getting data from transaction
        result = executeQuery('SELECT * FROM transactions WHERE transaction_id = ?;', parameters = (transactionId, ))
        
        # Entity type section
        entityType_entry_old_text = StringVar()
        entityType_entry_old_text.set(result[0][1])
        entityType_entry_old = Entry(topLevel_window, textvariable = entityType_entry_old_text, state = 'readonly', width = 40)
        entityType_entry_old.grid(row = 1, column = 1, padx = 5, pady = 5)

        # Entity section
        entity_entry_old_text = StringVar()
        entity_entry_old_text.set(result[0][2])
        entity_entry_old = Entry(topLevel_window, textvariable = entity_entry_old_text, state = 'readonly', width = 40)
        entity_entry_old.grid(row = 2, column = 1, padx = 5, pady = 5)

        # Operation section
        operation_entry_old_text = StringVar()
        operation_entry_old_text.set(result[0][3])
        operation_entry_old = Entry(topLevel_window, textvariable = operation_entry_old_text, state = 'readonly', width = 40)
        operation_entry_old.grid(row = 3, column = 1, padx = 5, pady = 5)

        # Amount section
        amount_entry_old_text = StringVar()
        amount_entry_old_text.set(result[0][4])
        amount_entry_old = Entry(topLevel_window, textvariable = amount_entry_old_text, state = 'readonly', width = 40)
        amount_entry_old.grid(row = 4, column = 1, padx = 5, pady = 5)

        # Commission section
        commission_entry_old_text = StringVar()
        commission_entry_old_text.set(result[0][5])
        commission_entry_old = Entry(topLevel_window, textvariable = commission_entry_old_text, state = 'readonly', width = 40)
        commission_entry_old.grid(row = 5, column = 1, padx = 5, pady = 5)

        # Total section
        total_entry_old_text = StringVar()
        total_entry_old_text.set(result[0][6])
        total_entry_old = Entry(topLevel_window, textvariable = total_entry_old_text, state = 'readonly', width = 40)
        total_entry_old.grid(row = 6, column = 1, padx = 5, pady = 5)

        # Time section
        time_entry_old_text = StringVar()
        time_entry_old_text.set(result[0][7])
        time_entry_old = Entry(topLevel_window, textvariable = time_entry_old_text, state = 'readonly', width = 40)
        time_entry_old.grid(row = 7, column = 1, padx = 5, pady = 5)

        # ------------------- Column 2 ---------------------------------------------------
        
        Label(topLevel_window, text = f'NEW info for transaction Id {transactionId}:').grid(row = 0, column = 2)

        # Entity Type section
        entityType_cb_new_text = StringVar()
        entityType_cb_new_text.set('Select an entity type')
        entityType_cb_new = Combobox(topLevel_window, textvariable = entityType_cb_new_text, values = entityTypes, state = 'readonly')
        entityType_cb_new.bind('<<ComboboxSelected>>', onEntityTypeSelected)
        entityType_cb_new.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'we')

        # Entity section
        entity_cb_new_text = StringVar()
        entity_cb_new_text.set('')
        entity_cb_new = Combobox(topLevel_window, textvariable = entity_cb_new_text, state = 'readonly')
        entity_cb_new.bind('<<ComboboxSelected>>', onEntitySelected)
        entity_cb_new.grid(row = 2, column = 2, padx = 5, pady = 5, sticky = 'we')

        # Operation section
        operation_cb_new_text = StringVar()
        operation_cb_new_text.set('')
        operation_cb_new = Combobox(topLevel_window, textvariable = operation_cb_new_text, state = 'readonly')
        operation_cb_new.grid(row = 3, column = 2, padx = 5, pady = 5, sticky = 'we')

        # Amount section
        amount_entry_new_text = StringVar()
        amount_entry_new_text.set('')
        amount_entry_new = Entry(topLevel_window, width = 40, textvariable = amount_entry_new_text, fg = 'blue')
        amount_entry_new.bind('<KeyRelease>', onInsertionOfText)
        amount_entry_new.grid(row = 4, column = 2, padx = 5, pady = 5)

        # Commission section
        commission_entry_new_text = StringVar()
        commission_entry_new_text.set('')
        commission_entry_new = Entry(topLevel_window, width = 40, textvariable = commission_entry_new_text, fg= 'blue', state = 'readonly')
        commission_entry_new.grid(row = 5, column = 2, padx = 5, pady = 5)

        # Total section
        total_entry_new_text = StringVar()
        total_entry_new_text.set('')
        total_entry_new = Entry(topLevel_window, width = 40, textvariable = total_entry_new_text, fg = 'blue', state = 'readonly')
        total_entry_new.grid(row = 6, column = 2, padx = 5, pady = 5)

        # Update button
        Button(topLevel_window, text = 'Update transaction', command = onClicking_UpdateTransactionButton).grid(row = 7, column = 2, padx = 5, pady = 5, sticky = 'we')

    else:
        messagebox.showerror('Something is wrong', validation_message)