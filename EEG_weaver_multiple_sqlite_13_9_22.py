# ----------------------------------------------------------------
# Paulo Afonso Medeiros Kanda
# Taubate São Paulo Brazil
# 2022-04-20
# EEG Reporter is part of EEGWeaver project
# to improve clinical use of post-processing EEG
# Yes! If you are here You will see the code is messy, with lots of comments and  debugs
# part of my learning process, indulge me.
# ----------------------------------------------------------------

# https://stackoverflow.com/questions/66302126/linked-tkinter-button-to-sqlite3-database-using-classes
# KANDA, PAULO AFONSO MEDEIROS

import sqlite3
from datetime import date

import os
import os.path

import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
# from tkinter import *
from tkinter import filedialog
from tkinter import StringVar
# from Application import *
from tkinter import messagebox

from EEG_weaver_Reporter_funcs_4_9_22 import Funcs
from pages_to_connect_pages import Pages
import json
from reporter_filepath import resource_path  # to know the path of images when creating exe


class FuncInDBGen:
    """
    attention:
    fidbgen means funcs in database generation (this module)
    because we have another funcs in EEG_weaver_Reporter_funcs
    """
    
    def __init__(self):

        self.db_list_treeview_path = None
        self.EEG_report_databanks_list = None
        self.size = None
        self.path_and_file = None
        self.date = None
        self.name = None
        self.cursor_dbin = None
        self.conn_dbin = None
        self.tree_db = None
        self.db_file_size = None
        self.db_save_name = None
        self.db_date = None
        self.basename = None
        self.db_find_entry = None
        # self.pdf_file_new = ''
        
    def clear_screen_fidbgen(self):
        """
        METHOD to clear entries
        """
        self.db_find_entry.delete(0, tk.END)
    
    def connect_db_fidbgen(self):
        # dbin --> database internal: sql that controls just name and path of
        # sql where reports are to allow access to those databanks
        # it is just one sqlite file while report sqlite can be many
        
        # self.conn_dbin = sqlite3.connect('../kanda_multi_sql3.db')
        self.conn_dbin = sqlite3.connect('kanda_multi_sql3.db')
        
        self.cursor_dbin = self.conn_dbin.cursor()
    
    def disconnect_db_fidbgen(self):
        self.conn_dbin.close()
    
    def create_Table_fidbgen(self):
        self.connect_db_fidbgen()
        
        # create table kanda_dbs in databank kanda_dbs.db
        self.cursor_dbin.execute("""
            CREATE TABLE IF NOT EXISTS kanda_dbs (
                id INTEGER PRIMARY KEY,
                db_name CHAR NOT NULL,
                db_date CHAR,
                db_path CHAR,
                db_size CHAR )
            ; """)
        
        self.conn_dbin.commit()
        self.disconnect_db_fidbgen()
    
    def variables_in_fidbgen(self):
        
        # self.get_database_var gives basename, path,
        self.get_database_var()
        self.name = self.basename
        
        self.add_actual_date()
        self.date = self.db_date
        
        # path and name of listaCli.databank
        self.path_and_file = self.db_save_name
        
        self.give_db_size()

        try:
            self.size = self.db_file_size
        except FileNotFoundError:
            pass
    
    def add_db_fidbgen(self):
        """
        add internal list to identify created databases I call it internal, just one database(not multiples)
        to keep track of external databases criated
        """
        self.variables_in_fidbgen()
        
        self.connect_db_fidbgen()
        self.cursor_dbin.execute(""" INSERT INTO kanda_dbs (
                                db_name,
                                db_date,
                                db_path,
                                db_size)
                                VALUES (?, ?, ?, ?)""",
                                 (self.name,
                                  self.date,
                                  self.path_and_file,
                                  self.size))
        self.conn_dbin.commit()
        self.disconnect_db_fidbgen()
        self.select_list_fidbgen()  # clear list and reselect to update
        self.clear_screen_fidbgen()  # clear find entry
        self.get_path_name_db_list()

        Pages.EEG_report_databanks_list = self.EEG_report_databanks_list
        self.store_after_create_db_list_to_json(self.EEG_report_databanks_list)
    
    @staticmethod
    def store_after_create_db_list_to_json(list_with_new_db):

        # https: // www.section.io / engineering - education / storing - data - in -python - using - json - module /
        # self.get_databk_values_to_cbox()
        updated_list_db_created = list_with_new_db  # create a set of numbers
        
        Pages.updated_list_with_newdb = list_with_new_db
        # updated_list = r'G:\PycharmProjects\EEG_WEAVER\json_objects\updated_list_db_created.json'
        # use the file extension .json
        updated_list = (resource_path('updated_list_db_created.json'))  # use the file extension .json
        
        with open(updated_list, 'w') as file_object:  # open the file in write mode
            json.dump(updated_list_db_created, file_object)  # json.dump() function to stores
            # the set of numbers in numbers.json file
    
    def select_list_fidbgen(self):
        self.tree_db.delete(*self.tree_db.get_children())  # cleantreeview list
        self.connect_db_fidbgen()
        # list = self.cursor_dbin.execute(""" SELECT cod, db_name, db_date, db_path, db_size FROM kanda_dbs
        fidbge_list = self.cursor_dbin.execute(""" SELECT  id, db_name, db_date, db_path, db_size FROM kanda_dbs
                                        ORDER BY db_name ASC; """)  # ASC calls in ascendent order
        
        self.tree_db.tag_configure('oddrow', background='#ebf5fb')
        self.tree_db.tag_configure('evenrow', background="#d4e6f1")
        #
        # for gets the information and insert
        for i in fidbge_list:
            if i[0] % 2 == 0:
                self.tree_db.insert("", tk.END, values=i, tags=('evenrow',))
            if i[0] % 2 != 0:
                self.tree_db.insert("", tk.END, values=i, tags=('oddrow',))
        
        # for parent in self.tree_db.get_children():
        #     print(self.tree_db.item(parent)["values"])
        
        self.disconnect_db_fidbgen()
        # total = concat(self.tree_db.set(item, 3)) for item in self.tree_db.get_children())
        
        # 'this gets the path and name of all databanks used in EEG_weaver_Reporter'
        self.get_path_name_db_list()
    
    def get_path_name_db_list(self):
        
        # this prints all variables of all children:
        # for child in self.tree_db.get_children():
        #     print(self.tree_db.item(child)["values"])
        #
        # for learning:
        # for child in self.tree_db.get_children():
        #    print(self.tree_db.item(child)["values"])
        # this prints
        # [1, 'rest.db', '06/05/2022', 'C:/000_tmp/rest.db', '0.0078125']
        # [4, 'test.db', '07/05/2022', 'C:/000_tmp/test.db', '0.0078125']
        # [2, 'test.db.db', '06/05/2022', 'C:/000_tmp/test.db.db', '0.0078125']
        
        # print(self.tree_db.set(child))
        # {'col1': '1', 'col2': 'rest.db', 'col3': '06/05/2022', 'col4': 'C:/000_tmp/rest.db', 'col5': '0.0078125'}
        
        # this prints all elements of 1 column:
        
        self.EEG_report_databanks_list = []
        for child in self.tree_db.get_children():
            col1, col2, col3, col4, col5 = self.tree_db.item(child)["values"]
            # print (col4)
            self.EEG_report_databanks_list.append(col4)
        #     C: / 000_tmp / rest.db
        #     C: / 000_tmp / test.db
        #     C: / 000_tmp / test.db.db
        
        # self.EEG_report_databanks_list = []
        # for child in self.tree_db.get_children():
        #     self.EEG_report_databanks_list.append(col4)
        # print(i) ['C:/000_tmp/test.db.db', 'C:/000_tmp/test.db.db', 'C:/000_tmp/test.db.db']
        
        # self.EEG_report_databanks_list = []
        # for col in child:
        #     self.EEG_report_databanks_list.append(col4)
        
        Pages.EEG_report_databanks_list = self.EEG_report_databanks_list
        
        # debug
        # print('self.EEG_report_databanks_list in get_path_name_db_list',self.EEG_report_databanks_list)
        # self.EEG_report_databanks_list in get_path_name_db_list[
        # 'C:/000_tmp/111.db', 'C:/000_tmp/222.db', 'C:/000_tmp/paulo0001.db']
        
        return self.EEG_report_databanks_list
    
    def on_left_clic(self, event):
        
        self.clear_screen_fidbgen()
        self.tree_db.selection()  # get info from self.tree_db
        n = ''
        try:
            for n in self.tree_db.selection():
                col1, col2, col3, col4, col5 = self.tree_db.item(n, 'values')
            # ----until here func select clicked items and store them in memory
            # ----don't need to feed entriees because we don't have any
            # keep here for learning purposes:
            # self.cod_entry.insert(END, col1)
            # self.name_entry.insert(END, col2) etc.
            # for n in self.tree_db.selection():
            db_list_treeview = (self.tree_db.item(n, 'values'))
            # print('this is db_list_treeview' , db_list_treeview)
            # this is db_list_treeview('1', 'rest.db', '05/05/2022', 'C:/000_tmp/rest.db', '0.0078125')
            
            self.db_list_treeview_path = db_list_treeview[3]  # path and file name in list treeview
            
            # debug:
            # print('db_list_treeview_path in def on_left_clic', db_list_treeview_path )
            # db_list_treeview_path in def on_left_clic C:/000_tmp / rest.db
            # print("this is db_list_treeview[0] ", db_list_treeview[0]) --> 1
            # print("this is db_list_treeview[1] ", db_list_treeview[1]) --> rest.db
            # print("this is db_list_treeview[2] ", db_list_treeview[2]) --> 06/05/2022
            
            Pages.index_of_inner_treeview = db_list_treeview[0]
            
            Pages.db_list_treeview_path = self.db_list_treeview_path
            # print('Pages.db_list_treeview_path in def on_left_clic', Pages.db_list_treeview_path)
            # Pages.db_list_treeview_path in def on_left_clic C:/ 000
            # _tmp / rest.db
            # curItem = self.tree_db.item(self.tree_db.focus())
            # print ('curItem = ', curItem)
            # curItem = {'text': '', 'image': '', 'values': [1, 'rest.db', '04/05/2022',
            # 'C:/000_tmp/rest.db', '0.0078125'],
            #            'open': 0, 'tags': ''}
        except FileNotFoundError:
            pass
    
    def delete_db_fidbgen(self):
        
        message = Pages.db_list_treeview_path + " DB will be deleted. Are You Sure?"
        result = tk.messagebox.askquestion('Deletion in Progress', message, icon='warning')
        
        if result == 'yes':
            self.variables_in_fidbgen()
            # self.path_and_name is builded when we use askopen... to create file
            # but here we are not creating file, it is already in treeview,
            # so we need to get it from treeview in def on_left_clic() -->  Pages.db_list_treeview_path
            # consequently:
            self.path_and_file = Pages.db_list_treeview_path
            
            # try:      # try to avoi erro in case the file.db is not in directory
            #
            self.connect_db_fidbgen()
            # actual func code
            self.cursor_dbin.execute(""" DELETE FROM kanda_dbs WHERE id = ?""", (Pages.index_of_inner_treeview,))
            
            # self.selected_item = self.tree_db.selection()[0]
            # for self.selected_item in self.tree_db.selection():
            #     self.cursor_dbin.execute("DELETE FROM kanda_dbs WHERE Codigo=?",
            #                            (self.tree_db.set(self.selected_item, "Codigo"),))
            
            try:
                os.remove(Pages.db_list_treeview_path)
            except OSError:
                pass
            
            # os.remove(Pages.db_list_treeview_path)
            
            self.conn_dbin.commit()
            self.disconnect_db_fidbgen()
            # except FileNotFoundError:
            #     # pass
            #     selected_items = self.tree_db.selection()
            #     for selected_item in selected_items:
            #         self.tree_db.delete(selected_item)
            #
            
            self.clear_screen_fidbgen()  # clear entry find
            self.select_list_fidbgen()  # update treeview
            # self.getdata()
        
        # else:
        #     selected_items = self.tree_db.selection()
        #     for selected_item in selected_items:
        #         self.tree_db.delete(selected_item)
        # # self.clear_screen_fidbgen()
        # self.tree_db.delete(*self.tree_db.get_children())
        # # self.connect_db_fidbgen()
        # # # list = self.cursor_dbin.execute(""" SELECT cod, db_name, db_date, db_path, db_size FROM kanda_dbs
        # # list = self.cursor_dbin.execute(""" SELECT  id, db_name, db_date, db_path, db_size FROM kanda_dbs
        # #                                         ORDER BY db_name ASC; """)  # ASC calls in ascendent order
        # #
        # # # for gets the information and insert
        # # for i in list:
        # #     self.tree_db.insert("", tk.END, values=i)
        # #
        # # # for parent in self.tree_db.get_children():
        # # #     print(self.tree_db.item(parent)["values"])
        # #
        # # self.disconnect_db_fidbgen()
        # #
        #
        # # self.select_list_fidbgen()
        #
        else:
            return
    
    def delete_many_db_fidbgen(self):
        response = messagebox.askyesnocancel("Delete Selected????",
                                             "This will DELETE ITEMS SELECTED FROM the Table\nAre you sure? ")
        
        if response == 1:  # yes
            # designate selections
            x = self.tree_db.selection()  # --> it is the lines selected
            
            # create list  of ids for delete
            ids_to_delete = []
            
            # this loop gives us a sequence of ids to  be deleted,
            # but  we must create a list as reference for delect
            # add selections to ids_to_delete list
            for record in x:
                ids_to_delete.append(self.tree_db.item(record, 'values')[0])  # -->index of id
            
            # debug
            # print(ids_to_delete)
            # ['4', '5', '7']
            # we must say delete all records with those ids
            
            # delete from treeview
            for record in x:
                self.tree_db.delete(record)
            
            self.connect_db_fidbgen()
            
            self.cursor_dbin.executemany("DELETE FROM kanda_dbs WHERE id = ?", [(a,) for a in ids_to_delete])
            
            self.conn_dbin.commit()
            self.cursor_dbin.close()
            self.disconnect_db_fidbgen()
            self.clear_screen_fidbgen()
    
    def get_database_var(self):
        pass
    
    def add_actual_date(self):
        pass
    
    def give_db_size(self):
        pass


class DatabankGenerator(FuncInDBGen, Funcs):
    """
    This script just create databanks  for report diferent eegs, for instance
    depending on diagnosis. As many databanks as you need,
    the sqlite here only shows the name and localization
    of such databanks
    and allows selecting one at time to be used in eeg reporter app
    EEG_Reporter detain the 'sqlits'
    
     inside this module we create two databases  one to be used with EEG reports(external database)
     we don't mess with this database here --> we just create it and show its location
     and
     another  database (inner database) to name and localize  EEG report databases

    in this module we have 2 DB (1 --> internal) local that just list the EEG reports Databank created
    this DB is used just as reference for localization etc. of DB external (main dbs)
    (2---> external) the main DBs created here and used by EEG_weaver_Reporter to store all info about reports
    external means variables that say something about related to DB(2) not local db used do list EEG Report
    IN this method we get the name and location of (2) and store it in (1) as reference
    """
    
    def __init__(self, parent):
        super().__init__()
        self.import_path_and_file = None
        self.db_path_to_import = None
        self.import_basename = None
        self.import_date = None
        self.imp_db_file_size = None
        self.new_db_plus_path = None
        self.cursor = None
        self.conn = None
        self.db_path = None
        self.dbfile_path_and_name = None
        self.scrool_db = None
        self.treevw_frame = None
        self.button_close = None
        self.button_use_db = None
        self.button_delete_db = None
        self.button_find_db = None
        self.entry_var_find = None
        self.label_find = None
        self.button_import_db = None
        self.button_create_db = None
        self.label_search_heading = None
        self.frame_buttons = None
        self.master = parent
        self.frame = tk.Frame(self.master)
        self.master.title('EDIT EEG REPORT DATABASES')
        self.master.geometry('850x600')
        self.master.resizable(False, False)
        # self.master.tk.call('wm', 'iconphoto', self.master._w, PhotoImage(
        # file=r"G:\PycharmProjects\EEG_WEAVER\images\header.gif"))
        self.master.tk.call('wm', 'iconphoto', self.master._w, PhotoImage(file=resource_path("header.gif")))
        # learning purposes:
        # self.master.configure(background= '#4E6172')
        # self.master.configure(background= '#778899')
        self.master.configure(background='#A9A9A9')
        # -----------------------frame buttons start
        
        self.create_buttons()
        self.create_treeview_dbs()
        self.create_Table_fidbgen()
        self.select_list_fidbgen()
        self.entry_var = StringVar()
    
    def close_multiple_sqlite_win(self):
        
        self.get_path_name_db_list()
        
        Pages.updated_list_with_newdb = self.EEG_report_databanks_list
        # parent.db_path_cbox = self.EEG_report_databanks_list
        self.master.destroy()
    
    def create_buttons(self):
        # self.frame_buttons = tk.Frame(self.master, highlightbackground="black", highlightthickness=1)
        self.frame_buttons = tk.Frame(self.master, bd=2, bg='#4E6172',
                                      highlightbackground="black", highlightthickness=1)
        # highlightbackground='#36454F',
        # highlightthickness=1)
        
        self.frame_buttons.place(relx=0.02, rely=0.02, relwidth=0.961, relheight=0.23)
        
        boldStyle = ttk.Style(self.frame_buttons)
        boldStyle.theme_use('clam')
        # boldStyle.configure("Bold.TButton", font=('Sans', '10', 'bold'))
        boldStyle.configure("Bold.TButton", font=('Helvetica', '10', 'bold'), relief='flat')
        
        self.label_search_heading = ttk.Label(self.frame_buttons, text='DATABASES', style='Bold.TButton')
        # font=('bold', 14), pady=10)
        self.label_search_heading.configure(font='helvetica 12')
        self.label_search_heading.place(relx=0.02, rely=0.4, relwidth=0.15, relheight=0.4)
        
        self.button_create_db = ttk.Button(self.frame_buttons, text='Select Folder and Create New Database',
                                           style='Bold.TButton', command=self.create_database_external)
        self.button_create_db.place(relx=0.05, rely=0.085, relwidth=0.42, relheight=0.25)
        
        self.button_import_db = ttk.Button(self.frame_buttons, text='Import Database to List',
                                           style='Bold.TButton', command=self.import_data_to_internal_list)
        self.button_import_db.place(relx=0.55, rely=0.085, relwidth=0.42, relheight=0.25)
        
        self.label_find = ttk.Label(self.frame_buttons, text='Find Database Name',
                                    style='Bold.TButton')  # font=('bold', 14), pady=10)
        self.label_find.configure(font='helvetica 12')
        self.label_find.place(relx=0.18, rely=0.4, relwidth=0.21, relheight=0.25)
        
        self.entry_var_find = StringVar()  # initializing a string var   to get  typed name of databank
        self.db_find_entry = ttk.Entry(self.frame_buttons, textvariable=self.entry_var_find)
        self.db_find_entry.place(relx=0.39, rely=0.4, relwidth=0.20, relheight=0.25)
        
        self.button_find_db = ttk.Button(self.frame_buttons, text='find', style='Bold.TButton')
        self.button_find_db.place(relx=0.61, rely=0.4, relwidth=0.09, relheight=0.25)
        
        self.button_delete_db = ttk.Button(self.frame_buttons, text='delete one', style='Bold.TButton',
                                           command=self.delete_db_fidbgen)
        # command = self.remove_one)
        self.button_delete_db.place(relx=0.18, rely=0.73, relwidth=0.12, relheight=0.25)
        
        self.button_use_db = ttk.Button(self.frame_buttons, text='Delete Many', style='Bold.TButton',
                                        command=self.delete_many_db_fidbgen)
        self.button_use_db.place(relx=0.3, rely=0.73, relwidth=0.13, relheight=0.25)
        
        self.button_close = ttk.Button(self.frame_buttons, text='Close', style='Bold.TButton',
                                       command=self.close_multiple_sqlite_win)
        self.button_close.place(relx=0.83, rely=0.73, relwidth=0.13, relheight=0.25)

        # -----------------------frame buttons end
    
    def ascending_fidbgen(self):
        self.connect_db_fidbgen()
        
        self.tree_db.delete(*self.tree_db.get_children())
        
        self.cursor_dbin.execute("SELECT * FROM kanda_dbs ORDER BY `id` ASC")
        # list = self.cursor_dbin.execute(""" SELECT  id, db_name, db_date, db_path, db_size FROM kanda_dbs
        #                                 ORDER BY db_name DESC; """)
        #                                 # ORDER BY db_name ASC; """)
        
        fetch = self.cursor_dbin.fetchall()
        # print(fetch)
        
        self.tree_db.tag_configure('oddrow', background='#ebf5fb')
        self.tree_db.tag_configure('evenrow', background="#d4e6f1")
        #
        # for gets the information and insert
        for i in fetch:
            if i[0] % 2 == 0:
                self.tree_db.insert("", tk.END, values=i, tags=('evenrow',))
            if i[0] % 2 != 0:
                self.tree_db.insert("", tk.END, values=i, tags=('oddrow',))
        
        self.cursor_dbin.close()
        self.disconnect_db_fidbgen()
        
        # -----------------------frame treeview start
    
    def descending_fidbgen(self):
        """
        make order in treeview list ascending
        """
        self.connect_db_fidbgen()
        
        self.tree_db.delete(*self.tree_db.get_children())
        
        self.cursor_dbin.execute("SELECT * FROM kanda_dbs ORDER BY `id` DESC")
        # list = self.cursor_dbin.execute(""" SELECT  id, db_name, db_date, db_path, db_size FROM kanda_dbs
        #                                 ORDER BY db_name DESC; """)
        #                                 # ORDER BY db_name ASC; """)
        
        fetch = self.cursor_dbin.fetchall()
        # print(fetch)
        
        self.tree_db.tag_configure('oddrow', background='#ebf5fb')
        self.tree_db.tag_configure('evenrow', background="#d4e6f1")
        #
        # for gets the information and insert
        for i in fetch:
            if i[0] % 2 == 0:
                self.tree_db.insert("", tk.END, values=i, tags=('evenrow',))
            if i[0] % 2 != 0:
                self.tree_db.insert("", tk.END, values=i, tags=('oddrow',))
        
        self.cursor_dbin.close()
        self.disconnect_db_fidbgen()
        
        # -----------------------frame treeview start
    
    def create_treeview_dbs(self):
        """
        This treeview only shows the names localization and size of  databanks where really are the reports
        Those databanks are created in this module and used in EEG_weaver_Reporter module
        to Remember --> in this module = this treeview and kanda_dbs.db to store localization of new
        databanks created to
        be used in  EEG_weaver_Reporter module
        """
        
        boldStyle = ttk.Style(self.master)
        boldStyle.theme_use('clam')
        # boldStyle.configure("Bold.TButton", font=('Sans', '10', 'bold'))
        boldStyle.configure("Bold.TButton", font=('Helvetica', '10', 'bold'), relief='flat')
        # boldStyle.configure("Bold.TButton", font=('Helvetica', '10'), relief='flat')
        
        boldStyle.configure("Treeview", background="#D3D3D3",
                            fieldbackground="#899499", foreground="black")
        
        self.treevw_frame = tk.Frame(self.master, bd=1, bg='#A9A9A9',
                                     highlightbackground="black", highlightthickness=1)
        
        self.treevw_frame.place(relx=0.02, rely=0.27, relwidth=0.961, relheight=0.71)
        # ttk.Style().configure("Treeview", background='#A9A9A9',
        #                       foreground='#A9A9A9', fieldbackground='#DCDCDC')
        
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=1, bd=2,
                        # font=('Arial', 11))  # Modify the font of the body
                        font=('Calibri', 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 10, 'bold'))  # Modify the font of the headings
        # style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        
        boldStyle = ttk.Style(self.treevw_frame)
        boldStyle.theme_use('clam')
        # boldStyle.configure("Bold.TButton", font=('Sans', '10', 'bold'))
        boldStyle.configure("Bold.TButton", font=('Helvetica', '10', 'bold'), relief='flat')
        
        self.tree_db = ttk.Treeview(self.treevw_frame, height='12',
                                    column=('col1', 'col2', 'col3', 'col4', 'col5'),
                                    show='headings', style="mystyle.Treeview")
        self.tree_db.place(relx=0.01, rely=0.01, relwidth=0.983, relheight=0.57)
        
        self.tree_db.heading('#0', text='')
        self.tree_db.heading('#1', text='Id', anchor='w', command=self.ascending_fidbgen)
        self.tree_db.heading('#2', text='Database Name', anchor='w', command=self.descending_fidbgen)
        self.tree_db.heading('#3', text='Creation Date', anchor='w')
        self.tree_db.heading('#4', text='Path', anchor='w')
        self.tree_db.heading('#5', text='Size MB', anchor='w')
        
        self.tree_db.column('#0', width=0, stretch="no")
        self.tree_db.column('#1', anchor=tk.W, width=100)
        self.tree_db.column('#2', anchor=tk.W, width=100)
        self.tree_db.column('#3', anchor=tk.W, width=100)
        self.tree_db.column('#4', anchor=tk.W, width=100)
        self.tree_db.column('#5', anchor=tk.W, width=100)
        
        self.scrool_db = ttk.Scrollbar(self.treevw_frame, orient='vertical')
        self.tree_db.configure(yscroll=self.scrool_db.set)
        self.scrool_db.place(relx=0.965, rely=0.092, relwidth=.03, relheight=0.835)
        self.tree_db.bind("<<TreeviewSelect>>", self.on_left_clic)
        # "<<TreeviewSelect>>" do the action as soon as treeview is selected
        
        # Add data
        # self.tree_db.insert(parent='', index='end', iid=0, text='Parent',
        #                  values=('John', 'John@gmail.com'))
        # self.tree_db.insert(parent='', index='end', iid=1, text='Parent',
        #                  values=('John', 'John@gmail.com'))
        #
        self.tree_db.place(relx=0.01, rely=0.03, relwidth=0.985, relheight=0.9)
        
        # -----------------------frame treeview end

        # ------------------------
        
        # Label1 = ttk.Label(self.treevw_frame, text ='Name',)
        # Label1.place(relx=0.01, rely=0.94, relwidth=0.09, relheight=0.19)
        #
        # Label1 = ttk.Label(self.treevw_frame, text ='Id')
        # Label1.place(relx=0.3, rely=0.94, relwidth=0.09, relheight=0.19)
        #
        # Label1 = ttk.Label(self.treevw_frame, text ='Localization')
        # Label1.place(relx=0.7, rely=0.94, relwidth=0.09, relheight=0.19)
        #
        # name_box = tk.Entry(self.treevw_frame)
        # name_box.place(relx=0.1, rely=0.94, relwidth=0.09, relheight=0.19)
        #
        # name_box = tk.Entry(self.treevw_frame)
        # name_box.place(relx=0.4, rely=0.94, relwidth=0.09, relheight=0.19)
        #
        # name_box = tk.Entry(self.treevw_frame)
        # name_box.place(relx=0.8, rely=0.94, relwidth=0.09, relheight=0.19)
        
        # ------------------------buttons
    
    def remove_one(self):  # innerdatabase
        x = self.tree_db.selection()[0]
        self.tree_db.delete(x)

    
    def add_record(self, db_new_name, db_date, db_path, db_file_size):  # inner database
        
        # self.add_actual_date()
        # db_file_size = ''
        # self.size_of_db()
        
        self.tree_db.insert(parent='', index='end', text='Parent',
                            values=(db_new_name, db_date, db_path, db_file_size))
    
    # def get_entry_new_name(self) -> str:
    #     """
    #     Just for learning purposes because I removed entry boxes for this  module
    #     get new name you give to databank in entry name
    #     get the entry name to create variable db_new_name which will form
    #     the name of new database during its creation
    #     """
    #     self.db_new_name = self.entry_var_name.get()
    #     print('self.entry_var = StringVar()', self.db_new_name)
    #     return self.db_new_name
    #
    
    def get_main_db_path(self):
        """
        #this is the name of the databank.db file you generate from  filedialog.asksaveasfile(
        # print('This is self.dbfile_path_and_name in def get_main_db_path', self.dbfile_path_and_name)
        # This is self.dbfile_path_and_name in def get_main_db_path < _io.TextIOWrapper
        # name = 'C:/000_tmp/new_002.db' mode = 'w'  encoding = 'cp1252' >
        # to to get only   'C:/000_tmp/new_002.db' -->  self.dbfile_path_and_name.name
        """
        
        self.dbfile_path_and_name = filedialog.asksaveasfile(
            # initialdir="C:/",
            mode="w",
            defaultextension=".db",
            filetypes=(("DB", "*.db"), ("DB", "*.db"))  # ("All files", "*"))
        )
        
        #     <_io.TextIOWrapper...
        try:
            self.db_path = os.path.dirname(self.dbfile_path_and_name.name)  # gives just the path without file name
        except FileNotFoundError:
            pass
        # debug -----------------
        # because   .name  in  self.dbfile_path_and_name.name  --> self.db_path = C:/000_tmp
        # without .name    in  self.dbfile_path_and_name       --> elf.db_path = < _io.TextIOWrapper...
        
        # self.dbfile_path_and_name =  < _io.TextIOWrapper...
        # self.dbfile_path_and_name.name = C:/000_tmp/paulo0002.db
        # print('self.dbfile_path_and_name  in def get_main_db_path(self)', self.dbfile_path_and_name.name)
        # self.dbfile_path_and_name in def get_main_db_path(self) C:/000_tmp/paulo0002.db
        #
        # print('self.db_path  in def get_main_db_path(self)', self.db_path)
        # self.db_path in   def get_main_db_path(self) C:/000_tmp
        
        # print('self.dbfile_path_and_name.name ', self.dbfile_path_and_name.name)
        # parameter .name gives correct path and file
        # debug -----------------
        
        if self.dbfile_path_and_name is None:
            return
        else:
            # This is self.dbfile_path_and_name in def get_main_db_path <_io.TextIOWrapper...
            Pages.dbfile_path_and_name = self.dbfile_path_and_name.name
            return self.dbfile_path_and_name.name
    
    def get_database_var(self):  # external inner database
        """
        get name of the folder where each main databases are
        """
        
        if Pages.dbfile_path_and_name == '':
            self.db_save_name = Pages.db_list_treeview_path  # --> this gets path&name from treeview
        # when creating a new database--> self.db_save_name returns _io.TextIOWrapper
        # self.db_list_treeview_path = db_list_treeview[3]   # path and file name in list treeview
        # self.db_save_name.name returns C:/000_tmp/test.db -->.name make the change
        else:
            self.db_save_name = Pages.dbfile_path_and_name  # --> this when creating a new file
            # print('self.db_save_name in def get_database_var(self)',
            # self.db_save_name)   # db_save_name C:/000_tmp/test.db
        
        self.basename = os.path.basename(self.db_save_name)
        Pages.basename_db = self.basename
        # print('self.basename', self.basename) # basename --> test.db
        self.db_path = os.path.dirname(self.db_save_name)
        # print('this is  self.db_path in get_database_var', self.db_path)   #C:/000_tmp
        # gd_data = {"gsd_designer": designer_nameE.get(), "gd_design": design_nameE.get(),
        #            etc, etc.
    
    def add_actual_date(self):
        today = date.today()
        # dd/mm/YY
        self.db_date = today.strftime("%d/%m/%Y")
        return self.db_date
    
    def give_db_size(self):
        """
        put in internal  treeview the size of the external database
        when creating databases , not when importing databanks
        """
        self.get_database_var()
        
        try:
            
            if self.db_save_name == '':
                self.db_save_name = Pages.db_list_treeview_path
            else:
                # self.db_save_name = Pages.dbfile_path_and_name.name
                self.db_save_name = Pages.dbfile_path_and_name
            
            if Pages.dbfile_path_and_name != '':  # if we use asksave etc. we create this file
                self.db_file_size = os.path.getsize(Pages.dbfile_path_and_name)  # bytes
                self.db_file_size = self.db_file_size / (1024 * 1024)
            elif Pages.dbfile_path_and_name == '':
                self.db_file_size = os.path.getsize(self.db_list_treeview_path)  # bytes
                # self.db_file_size = os.path.getsize(Pages.dbfile_path_and_name.name)  #bytes
                self.db_file_size = self.db_file_size / (1024 * 1024)  # megabytes
            else:
                self.db_file_size = 0
                
        except FileNotFoundError:
            # print('File does not exist')
            pass
        finally:
            pass
            # f.close()
            # print("File Closed")
    
    # --------------creation of multiple data banks-------------
    
    # noinspection PyMethodOverriding
    def connect_db(self, db_new_name):
        """
        external database creation
        here we really start creating new multiple database external
        """
        
        self.conn = sqlite3.connect(db_new_name)  # databank name
        self.cursor = self.conn.cursor()
    
    # ______________________database to be created
    
    def create_database_external(self):  # external database
        # Funcs.create_Table(self)
        
        self.get_main_db_path()
        self.add_actual_date()  # get db_date path
        
        # self.basename=''
        # self.db_save_name = ''
        self.get_database_var()  # get db path and file
        # print('this is path', db_path)
        
        # path and name of new db
        self.new_db_plus_path = self.db_save_name
        # new_db_plus_path = new_db_plus_path.replace('\\', '/')
        # print('this is new_db_plus_path:', new_db_plus_path)
        
        self.connect_db(self.db_save_name)
        # 
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY,
                        patient_name CHAR NOT NULL,
                        gender CHAR,
                        age CHAR,
                        diagnosis CHAR,
                        lff FLOAT,
                        hff FLOAT,
                        sampling_rate INTEGER,
                        recdate DATE,
                        header  CHAR,
                        body  CHAR,
                        footer  CHAR,
                        signature_image_db_logo CHAR,
                        signature_image_db CHAR,
                        patient_history1 CHAR,
                        patient_history CHAR)
                """)
        
        self.conn.commit()
        self.cursor.close()
        self.disconnect_db()
        
        self.give_db_size()
        # self.db_file_size = os.path.getsize(self.new_db_plus_path)  #bytes
        # self.db_file_size = self.db_file_size/(1024*1024)  #megabytes
        #
        # self.add_record(self.basename, self.db_date, self.db_path, self.db_file_size)

        # --> add values of name, folder, etc., not to this sqlite db  but to internal above sqlite
        self.add_db_fidbgen()
        # print('database created')
        # self.get_path_name_db_list()
        #
        # print('self.EEG_report_databanks_list in def create_database_external(self)', self.EEG_report_databanks_list)
        # ok = prints updated
    
    def give_db_size_when_importing(self):
        
        if Pages.database_path_name_to_import != '':  # if we use asksave etc. we create this file
            self.imp_db_file_size = os.path.getsize(Pages.database_path_name_to_import)  # bytes
            self.imp_db_file_size = self.imp_db_file_size / (1024 * 1024)
        elif Pages.database_path_name_to_import == '':
            self.imp_db_file_size = os.path.getsize(self.db_list_treeview_path)  # bytes
            # self.db_file_size = os.path.getsize(Pages.dbfile_path_and_name.name)  #bytes
            self.imp_db_file_size = self.imp_db_file_size / (1024 * 1024)  # megabytes
        else:
            self.imp_db_file_size = 0
    
    def import_data_to_internal_list(self):
        """
        get existing database, don't create it, and import to internal databank to show
        how many (external) main databases whe have. Internal database(kanda.db) contains the names
        of all databases created, ex, normal.db, alzheimer.db, etc
        
        """
        
        database_to_import = tk.filedialog.askopenfile(
            title='select', filetypes=[
                ("DB", "*.db"),])
        # (("DB", "*.db"), ("DB", "*.db")
        if database_to_import:
            print(database_to_import.name)
        
        database_to_import_path = database_to_import.name  # complete path and name ex C:/000_tmp/23_5/test.pdf
        
        Pages.database_path_name_to_import = database_to_import.name
        
        self.add_actual_date()  # get db_date path
        
        self.import_date = self.db_date
        
        self.import_basename = os.path.basename(database_to_import_path)
        # Pages.basename_db = self.basename
        # print('self.import_basename', self.import_basename) # basename --> test.db
        self.db_path_to_import = os.path.dirname(database_to_import_path)
        # print('this is self.db_path_to_import in import_data_to_internal_list', self.db_path_to_import)   #C:/000_tmp
        
        # path and name of listaCli.databank
        
        # self.path_and_file = self.db_save_name is substituted here for self.import_path_and_file
        # which is the complete path
        self.import_path_and_file = database_to_import.name
        
        # self.give_db_size()
        self.give_db_size_when_importing()
        # self.db_file_size
        try:
            self.size = self.imp_db_file_size
        except FileNotFoundError:
            pass
        
        self.connect_db_fidbgen()
        self.cursor_dbin.execute(""" INSERT INTO kanda_dbs (
                                db_name,
                                db_date,
                                db_path,
                                db_size)
                                VALUES (?, ?, ?, ?)""",
                                 (self.import_basename,
                                  self.import_date,
                                  self.import_path_and_file,
                                  self.size))
        self.conn_dbin.commit()
        self.disconnect_db_fidbgen()
        self.select_list_fidbgen()  # clear list and reselect to update
        self.clear_screen_fidbgen()  # clear find entry
        self.get_path_name_db_list()
        
        # print('self.EEG_report_databanks_list import_data_to_internal_list', self.EEG_report_databanks_list)
        
        # ok = prints updated
        Pages.EEG_report_databanks_list = self.EEG_report_databanks_list
        self.store_after_create_db_list_to_json(self.EEG_report_databanks_list)

# def main():
#
#     root = tk.Tk()
#     app = Databank_Generator(root)
#     root.mainloop()
#
#
# if __name__ == '__main__':
#     main()
