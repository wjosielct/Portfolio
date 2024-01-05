import sqlite3
from tkinter import Toplevel, Label, StringVar, Entry, Button
from tkinter.ttk import Combobox
import tkinter.messagebox as messagebox
from datetime import datetime

# -------------------------- Global variables ----------------------------------------

entityTypes = ["Banks", "Utility companies"]
banks = ["BCP", "Interbank", "BBVA", "ScotiaBank"]
utilityCompanies = ["SEDAPAL", "Edelnor", "Calidda"]

# ------------------------------------- Helper Functions  ------------------------------

def executeQuery(query, parameters):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        table = cursor.fetchall()
        conn.commit()
    return table


# -------------------------------------- Main function ---------------------------------------------

def onClicking_RegisterTransactionButton(root):

    # ---------------------------- Internal functions -------------------------------------------------
    
    def validateTransactionData():
        
        valid_data = False

        if entityType_cb_text.get() == 'Select an entity type':
            validation_message = 'Entity type is required'
        elif entity_cb_text.get() in ['', 'Select a bank', 'Select a utility company']:
            validation_message = 'Entity is required'
        elif operation_cb_text.get() in ['', 'Select bank operation', 'Select utility company operation']:
            validation_message = 'Operation is required'
        elif amount_entry_text.get() == '':
            validation_message = 'Amount is required'
        elif commission_entry_text.get() == 'Error':
            validation_message = 'Insert a valid amount'
        elif float(amount_entry_text.get()) <= 0:
            validation_message = 'Insert an amount greater than 0'
        else:
            validation_message = 'Successful validation'
            valid_data = True
        
        return valid_data, validation_message

    
    def onClicking_SaveTransactionButton():
        
        valid_data, validation_message = validateTransactionData()
        
        if valid_data:
            
            response = messagebox.askyesno("Question", "Do you want to save this transaction?")
            
            if response:
                query = 'INSERT INTO transactions (entity_type, entity_name, operation_type, amount, commission, total, time) VALUES (?, ?, ?, ?, ?, ?, ?);'
                entity_type = entityType_cb_text.get()
                entity_name = entity_cb_text.get()
                operation_type = operation_cb_text.get()
                amount_value = amount_entry_text.get()
                commission_value = commission_entry_text.get()
                total_value = total_entry_text.get()
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #Get the current time
                parameters = (entity_type, entity_name, operation_type, amount_value, commission_value, total_value, current_time)
                executeQuery(query, parameters)
                topLevel_window.destroy()
                messagebox.showinfo('Inportant information', 'The transaction has been successfully saved')
        else:
            messagebox.showerror("Something is wrong", validation_message)
    
    
    def onEntityTypeSelected(event):
        
        operation_cb_text.set('')
        operation_cb['values'] = '' # Setting the list of values of the combo box
        selectedEntityType = entityType_cb_text.get()
        
        if selectedEntityType == "Banks":
            entity_cb_text.set("Select a bank")
            entity_cb['values'] = banks # Setting the list of values of the combo box
            
        elif selectedEntityType == "Utility companies":
            entity_cb_text.set("Select a utility company")
            entity_cb['values'] = utilityCompanies # Setting the list of values of the combo box

    
    def onEntitySelected(event):
        
        selectedEntityType = entityType_cb_text.get()
        
        if selectedEntityType == "Banks":
            operation_cb_text.set('Select bank operation')
            operation_cb['values'] = ['Drawback', 'Deposit'] # Setting the list of values of the combo box

        elif selectedEntityType == "Utility companies":
            operation_cb_text.set('Select utility company operation')
            operation_cb['values'] = ['Bill payment'] # Setting the list of values of the combo box

    
    def onInsertionOfText(event):
        
        try:
            amount = float(amount_entry_text.get())
            commission = round(amount * 0.01, 2)
            total = round(amount + commission, 2)
            
            # Update the comission entry
            commission_entry['fg'] = 'blue'
            commission_entry_text.set(commission)

            # Update the total entry
            total_entry['fg'] = 'blue'
            total_entry_text.set(total)
        
        except ValueError as e:
            if amount_entry_text.get() == '':
                commission_entry_text.set('')
                total_entry_text.set('')
            else:
                commission_entry['fg'] = 'red'
                commission_entry_text.set('Error')

                total_entry['fg'] = 'red'
                total_entry_text.set('Error')

    # --------------------------- Start of graphical interface --------------------------------------

    # Top level window
    topLevel_window = Toplevel(root)
    topLevel_window.title(f'Register a transaction')
    topLevel_window.resizable(width = False, height = False) # Not allow to resize the top window
    topLevel_window.grab_set() # Disable the main window while open the top window

    # ------------------------- Entity Type section ------------------------------------------------
    Label(topLevel_window, text = 'Entity type:').grid(row = 0, column = 0, sticky = 'e')
    entityType_cb_text = StringVar()
    entityType_cb_text.set('Select an entity type')
    entityType_cb = Combobox(topLevel_window, textvariable = entityType_cb_text, values = entityTypes, state = 'readonly')
    entityType_cb.bind('<<ComboboxSelected>>', onEntityTypeSelected)
    entityType_cb.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'we')

    # ----------------------------------- Entity section -----------------------------------------------
    Label(topLevel_window, text = 'Entity:').grid(row = 1, column = 0, sticky = 'e')
    entity_cb_text = StringVar()
    entity_cb_text.set('')
    entity_cb = Combobox(topLevel_window, textvariable = entity_cb_text, state = 'readonly')
    entity_cb.bind('<<ComboboxSelected>>', onEntitySelected)
    entity_cb.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'we')

    # ------------------------------ Operation section ------------------------------------------
    Label(topLevel_window, text = 'Operation:').grid(row = 2, column = 0, sticky = 'e')
    operation_cb_text = StringVar()
    operation_cb_text.set('')
    operation_cb = Combobox(topLevel_window, textvariable = operation_cb_text, state = 'readonly')
    operation_cb.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'we')

    # -------------------------------- Amount section ----------------------------------------------
    Label(topLevel_window, text = 'Amount (S/):').grid(row = 3, column = 0, sticky = 'e')
    amount_entry_text = StringVar()
    amount_entry_text.set('')
    amount_entry = Entry(topLevel_window, width = 40, textvariable = amount_entry_text, fg = 'blue')
    amount_entry.bind('<KeyRelease>', onInsertionOfText)
    amount_entry.grid(row = 3, column = 1, padx = 10, pady = 5, sticky = 'w')

    # ------------------------------------ Commission section ---------------------------------------------
    Label(topLevel_window, text = 'Commission (S/):').grid(row = 4, column = 0, sticky = 'e')
    commission_entry_text = StringVar()
    commission_entry_text.set('')
    commission_entry = Entry(topLevel_window, width = 40, textvariable = commission_entry_text, fg= 'blue', state = 'readonly')
    commission_entry.grid(row = 4, column = 1, padx = 10, pady = 5, sticky = 'w')

    # --------------------------------------- Total section ------------------------------------------------------
    Label(topLevel_window, text = 'Total: (S/)').grid(row = 5, column = 0, sticky = 'e')
    total_entry_text = StringVar()
    total_entry_text.set('')
    total_entry = Entry(topLevel_window, width = 40, textvariable = total_entry_text, fg = 'blue', state = 'readonly')
    total_entry.grid(row = 5, column = 1, padx = 10, pady = 5, sticky = 'w')

    # ------------------------------------ Add transaction button ---------------------------------------------------------
    Button(topLevel_window, text = 'Save transaction', command = onClicking_SaveTransactionButton).grid(row = 6, column = 0, columnspan = 2, sticky = 'we', padx = 10, pady = 5)