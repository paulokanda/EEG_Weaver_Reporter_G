# ----------------------------------------------------------------
# Paulo Afonso Medeiros Kanda
# Taubate São Paulo Brazil
# 2022-04-20
# EEG Reporter is part of EEGWeaver project
# to improve clinical use of post-processing EEG
# Yes! If you are here You will see the code is messy, with lots of comments and  debugs
# part of my learning process, indulge me.
# ----------------------------------------------------------------
# <a target="_blank" href="https://icons8.com/icon
# /R2BKGNY4uJZz/exportar-pdf">Exportar PDF</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
# The paragraph Text can contain XML-like markup including the tags:
# <b> ... </b> - bold
# <i> ... </i> - italics
# <u> ... </u> - underline
# <super> ... </super> - superscript
# <sub> ... </sub> - subscript

# <font name=font family/fontname color=colorname size=float>

# <onDraw name=callable label="a label">

# The whole may be surrounded by <para> </para> tags
#  the intra paragraph tags:
# • <b> or <strong> - bold
# • <i> - italicize
# • <u> - underline
# • <a href> - Adding a link
# • <a name> - Adding an anchor
# • <strike> - Strike-through
# • <br/> - line break
# self.abas.enable_traversal()  # allow cntrl-tab or cntrl-shift-tab to change tab

import os
# from sqlite3 import SQLITE_ALTER_TABLE
import tkinter as tk
from tkinter import Tk, END, Canvas
from tkinter import ttk
from tkinter import PhotoImage
import sv_ttk
from tkinter import font as tkfont  # for convenience

from tkinter import filedialog
from tkinter import messagebox

from PIL import Image
import datetime
from datetime import datetime

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

import webbrowser
from pages_to_connect_pages import Pages

# from EEG_weaver_multiple_sqlite_31_7_22 import FuncInDBGen
# from EEG_weaver_multiple_sqlite_31_7_22 import Databank_Generator
# from EEG_weaver_Reporter_funcs_4_9_22 import Funcs
# from EEG_weaver_Reporter_funcs_4_9_22 import ToolTip
from EEG_weaver_multiple_sqlite_13_9_22 import FuncInDBGen
from EEG_weaver_multiple_sqlite_13_9_22 import DatabankGenerator
from EEG_weaver_Reporter_funcs_13_9_22 import Funcs
from EEG_weaver_Reporter_funcs_13_9_22 import ToolTip

import json
from reporter_filepath import resource_path
import re

root = Tk()
# root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\header.gif"))
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=resource_path("header.gif")))

# Adam Moller multipage for book style page:
# https://stackoverflow.com/questions/48997045/split-long-paragraph
# this is reportlab file to generate EEG Report
# sv_ttk.set_theme("dark")
sv_ttk.set_theme("light")


class Header(Funcs):
    """
    This class strings are the upper header of pdf
    and goes in top of all pages(that is why is separated in a specific class).
    
    The width and height of reportlab's letter page size is (612.0, 792.0). So you can get the starting
    position for your input image by dividing ((page's width/2) - (input image's width/2)).
    """
    
    def __init__(self):
        super().__init__()
        self.styles = None
        self.json_letter_or_A4_radiob1_aba4_var = ''
        self.json_port_eng_radiob34_aba4_var = ''
    
    def coord(self, x, y, unit=1):
        width, height = A4
        
        self.retrieve_letter_or_A4_radiob1_aba4_json()
        self.pageSize_letter_or_A4()
        self.retrieve_portg_or_eng_radiob34_aba4_json()
        
        x, y = x * unit, height - y * unit
        return x, y
    
    def table_style_set(self, data, font_size):
        col_widths = [260, 260]
        
        table = Table(data, colWidths=col_widths)
        # table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), self.my_specific_font, 12),
        table.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), self.my_specific_font, font_size),
                                   ("VALIGN", (1, 1), (-1, -1), "TOP"),
                                   # ("VALIGN", (1, 1), (-1, -1), "MIDDLE"),
                                   ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                   # ('BOX', (0, 0), (-1, -1), 0.25, colors.black), #boox around
                                   # ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                                   # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.darkgrey),
                                   ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
                                   ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.darkgrey),
                                   ('LINEBELOW', (0, -1), (-1, -1), 2, colors.darkgrey)
                                   ]))
    
    def header(self, canvas, doc):
        """
        entry.get() goes in function  EEG_PDF_Report--> def create_Report(self):
        to generate Pages variables like Pages.Header_object
        """
        
        # ------config fonts
        # ------get font selected in combobox aba4 as self.my_specific_font
        self.choose_font_to_use()  # gives variables to ptext
        
        width, height = doc.pagesize
        # width, height = ''
        self.json_port_eng_radiob34_aba4_var = ''
        self.json_letter_or_A4_radiob1_aba4_var = ''
        
        self.retrieve_letter_or_A4_radiob1_aba4_json()
        self.pageSize_letter_or_A4()
        self.retrieve_portg_or_eng_radiob34_aba4_json()  # self.json_port_eng_radiob34_aba4_var
        
        styles = getSampleStyleSheet()
        
        # ---------------------------- debug
        # header_object =
        # Institution: Neurovale Taubaté SP
        # Dept: EEG Laboratory
        # Address: Rua Portugal 131 Taubate
        # Fone: Whatsapp 1234'
        
        # -------------------------
        
        header_object = Pages.header_object  # variable get from variables
        
        # canvas.setfont(self.my_specific_font ,12)
        # ptext = '<font size=12><b> {}' \
        #         '</b></font>'.format(header_object)
        
        # ------------------------- select font
        self.choose_font_to_use()
        my_font = self.my_specific_font
        p_font = 14
        header_text = header_object  # text variable
        header_text_old = ''  # text variable
        
        ptext = """<font name= %s  size=%s color="black">%s</font>
        """ % (my_font, p_font, header_text_old)
        # styles.leading = 100
        # at beginning I create a text and wraped int in canvas
        # then I change it with a table with adress at left and
        # top image at right
        # now it must be kept with header_text_old = ''
        
        # -------------------------wrapOn header_text
        
        p = Paragraph(ptext, styles["Normal"])
        
        p.wrapOn(canvas, width, height)
        
        # ----------------------------------------------
        
        upper_table_text = header_text
        
        # try:
        #     right_head_Image = Image(Pages.listaCli_imagePath_logo, 2.8 * inch, 2.8 * inch, kind='proportional')
        #
        # except FileNotFoundError:
        #     right_head_Image = Image(r"header_image_mockup1920_838.png",
        #                                  2.8 * inch, 2.8 * inch, kind='proportional')
        
        if Pages.listaCli_imagePath_logo == '':  # if user didn't import an image to represent logo
            right_head_Image = Image(r"header_image_mockup1920_838.png",
                                     2.8 * inch, 2.8 * inch, kind='proportional')
        else:  # size of image
            # right_head_Image = Image(Pages.listaCli_imagePath_logo, 2.5 * inch, 2.5 * inch, kind='proportional')
            right_head_Image = Image(Pages.listaCli_imagePath_logo, 2.8 * inch, 2.8 * inch, kind='proportional')
        
        # ---positioning upper header acordingly the page size
        if self.json_letter_or_A4_radiob1_aba4_var == 1:  # 1 =  width, height = letter
            colWidths = [280, 270]
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:  # 2 width, height = A4
            colWidths = [280, 270]
        # colWidths = [260, 240]
        colWidths = [280, 270]  # the left column size pushes the right one
        # rowHeights= (10*mm)
        
        # upper_table_text is the text from report header
        # use of  Paragraph  in (upper_table_text) allows to insert html tags as <i> in table cel
        # to format text in header
        data0 = [[Paragraph(upper_table_text), right_head_Image], ]
        
        table = Table(data0, colWidths=colWidths)  # , rowHeights=rowHeights)
        # self.table_style_set(data0, 14)
        
        table.setStyle([('FONT', (0, 0), (-1, -1), self.my_specific_font, 12),  # , self.line_height),
                        # ("VALIGN", (1, 10), (-1, -1), "MIDDLE"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),  # align left text with right image
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.darkgrey)])
                        ])
        
        table.wrap(0, 0)  # necessary to plot the table
        # table.drawOn(canvas, 72, height --> bigger number upper)
        
        # parameters specify the location of the
        # table.drawOn(canvas,distance from left, from top --> the bigger the number the higher the table)
        # table.drawOn(canvas,73, 600)
        
        # ----------------------------
        # -----------------------------
        # try:  # in  Name/adress of clinic at top
        if self.json_letter_or_A4_radiob1_aba4_var == 1:  # 1 =  width, height = letter
            # table.drawOn(canvas, *self.coord(distance from left, distance from top, mm))
            table.drawOn(canvas, *self.coord(26, 75, mm))
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:  # 2 width, height = A4
            table.drawOn(canvas, *self.coord(23, 65, mm))
        else:
            table.drawOn(canvas, *self.coord(26, 75, mm))
        # except:
        #     table.drawOn(canvas, *self.coord(26, 75, mm))
        
        # debug
        # p.drawOn(canvas, *self.coord(28, 40, mm))  # in letter Name/adress of clinic at top
        
        # --------------------------- Report Id-
        
        header_id_obj2 = Pages.id_object
        # self.define_font_reportLab(canvas, 10)
        
        my_font = self.my_specific_font
        p_font = 10
        header_text2 = header_id_obj2  # text variable
        # try:
        if self.json_port_eng_radiob34_aba4_var == 1:
            # ptext = '<font size=10><b>Report ID: {}' \
            #         '</b></font>'.format(header_id_obj2)
            # header_text2 = header_id_obj2
            ptext = """<font name= %s  size=%s color="black">Report ID: %s</font>
            """ % (my_font, p_font, header_text2)
        
        elif self.json_port_eng_radiob34_aba4_var == 2:
            # ptext = '<font size=10><b>Número de registro do EEG: {}' \
            #         '</b></font>'.format(header_id_obj2)
            # header_text2 = header_id_obj2
            ptext = """<font name= %s  size=%s color="black">Número de registro do EEG: %s</font>
            """ % (my_font, p_font, header_text2)
        
        else:
            # ptext = '<font size=10><b>Report ID: {}' \
            #         '</b></font>'.format(header_id_obj2)
            # header_text2 = header_id_obj2
            ptext = """<font name= %s  size=%s color="black">Report ID: %s</font>
            """ % (my_font, p_font, header_text2)
        
        # canvas.setFont('arial', 10)
        p = Paragraph(ptext, styles["Normal"])
        
        # P= canvas.line(50, 380, 560, 380)
        p.wrapOn(canvas, width, height)
        # try:
        if self.json_letter_or_A4_radiob1_aba4_var == 1:  # 1 =  width, height = letter
            p.drawOn(canvas, *self.coord(28, 69, mm))
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:  # 2 width, height = A4
            # p.drawOn(canvas, *self.coord(28, 47, mm))
            p.drawOn(canvas, *self.coord(25, 58, mm))
        else:
            p.drawOn(canvas, *self.coord(28, 69, mm))
        # except:
        #     p.drawOn(canvas, *self.coord(28, 69, mm))
        #
        # --------------------------------- Pacient Name
        
        my_font = self.my_specific_font
        p_font = 10
        patient_name_object = Pages.patient_object  # variable from module pages_to_connect_pages
        # try:
        if self.json_port_eng_radiob34_aba4_var == 1:
            # ptext = '<font size=10><b>Name: {}' \
            #         '</b></font>'.format(patient_name_object)
            ptext = """<font name= %s  size=%s color="black">Name: %s</font>
            """ % (my_font, p_font, patient_name_object)
        
        elif self.json_port_eng_radiob34_aba4_var == 2:
            # ptext = '<font size=10><b>Nome ou Identificação: {}' \
            #         '</b></font>'.format(patient_name_object)
            ptext = """<font name= %s  size=%s color="black">Identificação: %s</font>
            """ % (my_font, p_font, patient_name_object)
        
        # except:
        else:
            ptext = """<font name= %s  size=%s color="black">Name: %s</font>
            """ % (my_font, p_font, patient_name_object)
        
        p = Paragraph(ptext, styles["Normal"])
        p.wrapOn(canvas, width, height)
        
        # try:
        if self.json_letter_or_A4_radiob1_aba4_var == 1:  # 1 =  width, height = letter
            p.drawOn(canvas, *self.coord(28, 73, mm))
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:  # 2 width, height = A4
            p.drawOn(canvas, *self.coord(25, 62, mm))
        else:
            p.drawOn(canvas, *self.coord(28, 73, mm))
        # except:
        #     p.drawOn(canvas, *self.coord(28, 73, mm))
        
        # p.drawOn(canvas, *self.coord(28, 51, mm))
        
        # --------------------------------- date
        
        my_font = self.my_specific_font
        p_font = 10
        date_object = Pages.date_object  # text variable
        # try:
        if self.json_port_eng_radiob34_aba4_var == 1:
            # ptext = '<font size=10><b>Report Date: {}' \
            #         '</b></font>'.format(date_object)
            ptext = """<font name= %s  size=%s color="black">Report Date: %s</font>
            """ % (my_font, p_font, date_object)
        
        elif self.json_port_eng_radiob34_aba4_var == 2:
            # ptext = '<font size=10><b>Laudo gravado em: {}' \
            #         '</b></font>'.format(date_object)
            ptext = """<font name= %s  size=%s color="black">Laudo gravado em: %s</font>
            """ % (my_font, p_font, date_object)
            
            # else:
            #     ptext = '<font size=10><b>Report Date: {}' \
            #             '</b></font>'.format(date_object)
        # except:
        else:
            ptext = """<font name= %s  size=%s color="black">Report Date: %s</font>
            """ % (my_font, p_font, date_object)
        #
        
        p = Paragraph(ptext, styles["Normal"])
        p.wrapOn(canvas, width, height)
        # try:
        if self.json_letter_or_A4_radiob1_aba4_var == 1:  # 1 =  width, height = letter
            p.drawOn(canvas, *self.coord(28, 77, mm))
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:  # 2 width, height = A4
            p.drawOn(canvas, *self.coord(25, 66, mm))
        else:
            p.drawOn(canvas, *self.coord(28, 77, mm))
        # except:
        #     p.drawOn(canvas, *self.coord(28, 77, mm))
        
        # p.drawOn(canvas, *self.coord(28, 55, mm))
        
        # ----Add page number-------------------------------
        page_num = canvas.getPageNumber()
        text = "Pg %s" % page_num
        canvas.drawRightString(200 * mm, 20 * mm, text)
        # canvas.drawRightString(180 * mm, 20 * mm, text)
        
        # ---------------------------------title EEG Report change language start
        self.styles = getSampleStyleSheet()
        
        # using self.json_port_eng_radiob34_aba4_var returns 2 or 1 if portuguese or english
        # with open('portuguese_or_english_pdf.json')
        self.retrieve_portg_or_eng_radiob34_aba4_json()
        
        # self.retrieve_Pdf_newTitle_typedin_entry_json = ''
        # new name typed in entrybox to substitute 'Electroencephalogram'
        # with open('pdf_Newtitle_from_entry_json.json')
        self.retrieve_Pdf_newTitle_typedin_entry_json()
        
        # returns 1 or 2 if you use default title or new title  by self.retrieved_Pdf_Title_1or2_aba4_var_json
        # with open('pdf_title_1or2_radiob90_json.json')
        self.retrieve_Pdf_Title_1or2_radiob90_aba4_var_json()
        # --> says if we use title electroenc(1) or alternative(2)
        
        my_font = self.my_specific_font
        p_font = 18
        name_Title = 'Electroencephalogram (EEG) Report'  # text variable
        titulo_Inicial = 'Laudo - Eletrencefalograma (EEG)'
        alternative_Title = self.retrieved_Pdf_NewTitle_typedin_entry_json
        # print('self.retrieved_Pdf_NewTitle_typedin_entry_json', self.retrieved_Pdf_NewTitle_typedin_entry_json)
        # try:
        if self.json_port_eng_radiob34_aba4_var == 1:
            if self.retrieved_Pdf_Title_1or2_aba4_var_json == 1:
                ptext = """<font name= %s  size=%s color="black">%s</font>
                        """ % (my_font, p_font, name_Title)
            elif self.retrieved_Pdf_Title_1or2_aba4_var_json == 2:
                ptext = """<font name= %s  size=%s color="black">%s</font>
                        """ % (my_font, p_font, alternative_Title)
        
        elif self.json_port_eng_radiob34_aba4_var == 2:
            if self.retrieved_Pdf_Title_1or2_aba4_var_json == 1:
                ptext = """<font name= %s  size=%s color="black">%s</font>
                        """ % (my_font, p_font, titulo_Inicial)
            
            elif self.retrieved_Pdf_Title_1or2_aba4_var_json == 2:
                ptext = """<font name= %s  size=%s color="black">%s</font>
                        """ % (my_font, p_font, alternative_Title)
        
        # except:
        else:
            ptext = """<font name= %s  size=%s color="black">%s</font>
            """ % (my_font, p_font, name_Title)
        
        # ---------------------------------title EEG Report change change phrase start
        
        # self.retrieve_Pdf_newTitle_typedin_entry_json = ''
        # new name typed in entrybox to substitute 'Electroencephalogram'
        #
        # # returns 1 or 2 if you use defaul title or new title  by self.retrieved_Pdf_Title_1or2_aba4_var_json
        # self.retrieve_Pdf_Title_1or2_radiob90_aba4_var_json()
        
        # ---------------------------------title EEG Report change phrase end
        
        p = Paragraph(ptext, self.styles["Heading2"])
        p.wrapOn(canvas, width, height)
        
        # try:
        if self.json_letter_or_A4_radiob1_aba4_var == 1:  # letter =1
            p.drawOn(canvas, *self.coord(28, 85, mm))
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:  # A2 =2
            p.drawOn(canvas, *self.coord(25, 74, mm))
        else:
            width, height = letter
        
        # except:
        #     width, height = letter
        
        # p.drawOn(canvas, *self.coord(28, 65, mm))  #second number is hight, the bigger the lowest
        
        # --------------------------------- logo
        # # line_x_start = 360
        # # line_width = 200
        # # line_y = 130
        # # # canvas.saveState()
        # #
        # # PartnerLogo = HEADER IMAGE TOP RIGHT
        #
        # try:
        #     PartnerLogo = Pages.listaCli_imagePath_logo
        #     canvas.drawImage(PartnerLogo, 395, 576, width=170, height=200,
        #                      preserveAspectRatio=True)  # , mask='auto')
        #
        # except:
        #     pass
        # ---------------------------------
        my_font = self.my_specific_font
        p_font = 10
        last_footer = Pages.history1_object  # text variable
        
        ptext = """<font name= %s  size=%s color="black">%s</font>
                """ % (my_font, p_font, last_footer)
        
        # ptext = '<font size=10><b> {}' \
        #         '</b></font>'.format(last_footer)
        
        p = Paragraph(ptext, styles["Normal"])
        p.wrapOn(canvas, width, height)
        
        # canvas.setFont(self.my_specific_font, 10)
        
        # try:
        if self.json_letter_or_A4_radiob1_aba4_var == 1:
            # width, height = letter
            p.drawOn(canvas, *self.coord(28, 280, mm))
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:
            width, height = A4
            p.drawOn(canvas, *self.coord(25, 280, mm))
        else:
            p.drawOn(canvas, *self.coord(28, 280, mm))
        # except:
        #     p.drawOn(canvas, *self.coord(28, 280, mm))
        
        # p.drawOn(canvas, *self.coord(90, 260, mm))


# noinspection PyGlobalUndefined
class EegPdfReport(Header):
    """
    Main PDF Class generates pdf header, body and footer using reportlab library
    """
    
    def __init__(self, pdf_file_new):
        """"""
        
        # definition of the type of page if letter or A4
        # margins of body of document main part with table and report text:
        # self.json_port_eng_radiob34_aba4_var = ''
        # self.json_show_or_not_PDFradiob56_aba4_var = ''
        # self.json_letter_or_A4_radiob1_aba4_var = ''
        # self.json_show_or_not_Table_radiob78_aba4_var = ''
        
        super().__init__()
        
        self.json_show_or_not_PDFradiob56_aba4_var = ''
        self.json_show_or_not_Table_radiob78_aba4_var = ''
        self.txt_header = None
        self.Id_entry = None
        self.report_Date_entry = None
        self.patient_entry = None
        self.gender_chosen = None
        self.age_entry = None
        self.diag_entry = None
        self.LFF_entry = None
        self.HFF_entry = None
        self.srate_entry = None
        self.txt_footer = None
        self.signature_img_entry_logo = None
        self.signature_img_entry = None
        self.txt_history1 = None
        self.txt_body = None
        self.txt_history = None
        
        self.retrieve_letter_or_A4_radiob1_aba4_json()
        self.pageSize_letter_or_A4()
        self.retrieve_portg_or_eng_radiob34_aba4_json()
        self.retrieve_show_or_not_pdf_radiob56_aba4_json()
        
        # size of body of page text
        # try:
        if self.json_letter_or_A4_radiob1_aba4_var == 1:  # letter =1
            self.doc = SimpleDocTemplate(
                pdf_file_new, pagesize=letter,
                rightMargin=45, leftMargin=72,
                topMargin=200, bottomMargin=65)
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:  # A2 =2
            self.doc = SimpleDocTemplate(
                pdf_file_new, pagesize=A4,
                rightMargin=40, leftMargin=65,
                topMargin=230, bottomMargin=65)
        else:
            self.doc = SimpleDocTemplate(
                pdf_file_new, pagesize=letter,
                rightMargin=45, leftMargin=72,
                topMargin=200, bottomMargin=65)
        # except:
        #     self.doc = SimpleDocTemplate(
        #         pdf_file_new, pagesize=letter,
        #         rightMargin=45, leftMargin=72,
        #         topMargin=200, bottomMargin=65)
        #
        self.elements = []
        self.styles = getSampleStyleSheet()
        # self.width, self.height = letter
        # try:
        if self.json_letter_or_A4_radiob1_aba4_var == 1:
            self.width, self.height = letter
        elif self.json_letter_or_A4_radiob1_aba4_var == 2:
            self.width, self.height = A4
        else:
            self.width, self.height = letter
        # except:
        #     self.width, self.height = letter
    
    def create_header(self):
        """"""
        header = Header()
        self.elements.append(header)
        # self.elements.append(Spacer(1, 50))
        # self.elements.append(Spacer(1,0.01*inch))
    
    def create_text(self, text, size=10, bold=False):
        """"""
        
        if bold:
            return Paragraph('''<font size={size}><b>
            {text}</b></font>
            '''.format(size=size, text=text),
                             self.styles['Normal'])
        
        return Paragraph('''<font size={size}>
        {text}</font>
        '''.format(size=size, text=text),
                         self.styles['Normal'])
    
    def eeg_report_title(self):
        """
        It is a table were some parameters are described
        we get all variables type Pages.something_object from
        method -->  def create_Report
        """
        # table = Table()
        # get font selected in combobox aba4 as  self.my_specific_font
        self.choose_font_to_use()  # gives variables to ptext
        
        # debug:
        # ptext = '<font size=18>EEG Report</font>'
        # p = Paragraph(ptext, self.styles["Heading2"])
        # self.elements.append(p)
        # self.elements.append(Spacer(1, 10))
        self.elements.append(KeepTogether(Spacer(1, 20)))
        # self.elements.append(KeepTogether(Spacer(1, 20)))
        # colWidths = [55, 125, 50, 125, 50, 150]
        colWidths = [70, 240, 90, 80]
        
        data1 = [[self.create_text('Patient', bold=True), self.create_text(Pages.patient_object, bold=True),
                  self.create_text('EEG Scope', bold=True), self.create_text('Settings', bold=True)],
                 [self.create_text('Gender', bold=True), self.create_text(Pages.gender_object, bold=True),
                  self.create_text('Sample Rate', bold=True), self.create_text(Pages.sample_rate_object, bold=True)],
                 [self.create_text('Age', bold=True),
                  self.create_text(Pages.age_object, bold=True),
                  self.create_text('Low Freq Filter', bold=True),
                  self.create_text(Pages.low_f_f_object, bold=True)],
                 [self.create_text('Diagnosis', bold=True),
                  self.create_text(Pages.diagnosis_object, bold=True),
                  self.create_text('High Freq Filter', bold=True),
                  self.create_text(Pages.high_f_f_object, bold=True)],
                 ]
        
        data2 = [[self.create_text('Paciente', bold=True), self.create_text(Pages.patient_object, bold=True),
                  self.create_text('EEG', bold=True), self.create_text('Parâmetros', bold=True)],
                 [self.create_text('Gênero', bold=True), self.create_text(Pages.gender_object, bold=True),
                  self.create_text('Taxa Amostral', bold=True), self.create_text(Pages.sample_rate_object, bold=True)],
                 [self.create_text('Idade', bold=True),
                  self.create_text(Pages.age_object, bold=True),
                  self.create_text('Filtro Fr. Baixa', bold=True),
                  self.create_text(Pages.low_f_f_object, bold=True)],
                 [self.create_text('Diagnóstico', bold=True),
                  self.create_text(Pages.diagnosis_object, bold=True),
                  self.create_text('Filtro Fr. Alta', bold=True),
                  self.create_text(Pages.high_f_f_object, bold=True)],
                 ]
        
        # self.elements.append(Indenter(left=77))
        # self.elements.append(Indenter(right=100))
        
        table = ''
        # try:
        if self.json_port_eng_radiob34_aba4_var == 1:
            table = Table(data1, colWidths=colWidths)
        elif self.json_port_eng_radiob34_aba4_var == 2:
            table = Table(data2, colWidths=colWidths)
        # except:
        else:
            table = Table(data1, colWidths=colWidths)
        #
        table.setStyle([('FONT', (0, 0), (-1, -1), self.my_specific_font, 12),  # , self.line_height),
                        ("VALIGN", (1, 10), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.darkgrey)])
        
        self.elements.append(KeepTogether(table))
        # self.elements.append(table)
        # self.elements.append(Spacer(1,85))
        self.elements.append(KeepTogether(Spacer(1, 20)))
        # self.elements.append(Spacer(1,0.1*inch))
        # self.elements.append(Indenter(left=-60))
    
    def create_body(self):
        """
        this is Alam Molle's multipage for just plain text. We ussually find
        multipage for table but for report EEG we need this
        """
        
        # get font selected in combobox aba4 as  self.my_specific_font
        self.choose_font_to_use()  # gives variables to ptext
        
        # pdfmetrics.registerFont(fonts.TTFont('TNR', 'times.ttf'))
        # pdfmetrics.registerFont(ttfonts.TTFont('TNRB', 'timesbd.ttf'))
        # self.elements.append(Spacer(1, 40))
        stylesheet = getSampleStyleSheet()
        stylesheet.add(ParagraphStyle(name='Paragraph',
                                      # fontName='TNR',
                                      # firstLineIndent=100,
                                      fontName=self.my_specific_font,
                                      fontSize=12,
                                      spaceAfter=10,
                                      leading=20, parent=stylesheet['Normal'],
                                      spaceBefore=4,
                                      # firstLineIndent=100
                                      # leftIndent=36
                                      ))  # space before push from top
        stylesheet['Normal'].firstLineIndent = 50
        
        # debug:
        # leading =space among lines
        # leading=20, parent=stylesheet['BodyText']))  # leading =space among lines
        # stylesheet.leftIndent = first.leftIndent
        # stylesheet.add(ParagraphStyle(name='Paragraph',
        #                            # fontName="Helvetica-Bold",
        #                            fontName="Helvetica",
        #                            fontSize=12,
        #                            parent=stylesheet['Normal'],
        #                            alignment=1,
        #                            spaceAfter=14))
        
        # elements = []
        # Create a long paragraph with multiple line breaks.
        # self.elements.append(Spacer(1, 40))
        # ----------------------
        # here we have a trick reportlab doesnot accept <Tab>, to space it uses "&nbsp"
        # so in Text widget we insert <Tab> and here we replace to allow tabulation in final pdf
        Pages.body_Report_object = Pages.body_Report_object.replace(
            "<Tab>", "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp"
                     ";&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        paragraph = Pages.body_Report_object
        
        # paragraph += "<br/><br/>"
        # paragraph += "Lorem ipsum dolor sit amet, consectetur adipiscing elit." * 10
        # paragraph += "<br/><br/>"
        # paragraph *= 10
        
        self.elements.append(Paragraph(paragraph, stylesheet['Paragraph']))
        self.elements.append(Spacer(1, 30))
        
        ############
    
    def create_history_title(self):
        """
        just the title of clinical story
        """
        self.choose_font_to_use()  # returns  if radiob1= helvética, if radib2= another font
        self.elements = []
        stylesheet = getSampleStyleSheet()
        stylesheet.add(ParagraphStyle(name='Paragraph',
                                      # fontName='TNR',
                                      fontName=self.my_specific_font,
                                      # fontName="Helvetica-Bold",
                                      fontSize=14,
                                      spaceAfter=10,
                                      leading=20, parent=stylesheet['Normal']))
        
        paragraph = 'CLINICAL HISTORY'
        
        self.elements.append(Paragraph(paragraph, stylesheet['Paragraph']))
        self.elements.append(Spacer(1, 10))
    
    ############
    
    def eeg_report_footer(self):
        """"""
        # get font selected in combobox aba4 as  self.my_specific_font
        self.choose_font_to_use()  # gives variables to ptext
        
        my_font = self.my_specific_font
        p_font = 12
        name_Title = 'Interpreted and Reviewed by: '  # text variable
        titulo_nome = 'Laudado e Revisado por: '
        ptext = ''
        
        # try:
        if self.json_port_eng_radiob34_aba4_var == 1:
            # ptext = '<font size=12>Interpreted and Reviewed by:</font>'
            ptext = """<font name= %s  size=%s color="black">%s</font>
                    """ % (my_font, p_font, name_Title)
        
        elif self.json_port_eng_radiob34_aba4_var == 2:
            # ptext = '<font size=12>Laudado e Revisado por:</font>'
            ptext = """<font name= %s  size=%s color="black">%s</font>
                    """ % (my_font, p_font, titulo_nome)
        
        # except:
        else:
            # ptext = '<font size=12>Interpreted and Reviewed by:</font>'
            ptext = """<font name= %s  size=%s color="black">%s</font>
                    """ % (my_font, p_font, name_Title)
        
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Justify', fontName='Times', fontSize=10))
        # paragraph = Paragraph(ptext, self.styles["Heading1"])
        paragraph = Paragraph(ptext, self.styles['Justify'])
        date_object = Pages.date_object
        
        # ------------------------------------------------
        if Pages.listaCli_imagePath == '':  # if user didn't import an image to represent signature in footer
            # Pages.listaCli_imagePath = 'images/ref_mage.png'
            # right_foot_Image = Image(Pages.listaCli_imagePath, 1 * inch, 1 * inch)
            right_foot_Image = ''
        else:
            right_foot_Image = Image(Pages.listaCli_imagePath, 1 * inch, 1 * inch, kind='proportional')
        
        colWidths = [260, 240]
        # print(" Pages.listaCli_imagePath í footer ",  Pages.listaCli_imagePath )
        # Patient_config = Paragraph(
        #     '<font size=11>Patient</font>',
        #     self.styles["Normal"])
        # parameters_config = Paragraph(
        #     '<font size=10>EEG parameters</font>',
        #     self.styles["Normal"])
        # colWidths = [1, 260, 260, 1]
        # data = [['', '', '', ''],
        #         [(''),  # space left to main text
        #          self.create_bold_text(self.footer_ref),
        #          right_foot_Image,  # image from treeviewpath
        #          (''),  # space right to main text
        #          ]]
        
        data = [[paragraph, date_object],
                [self.create_text(Pages.doctor_name, bold=True),
                 right_foot_Image],
                ]
        
        # self.elements.append(Indenter(left=77))
        table = Table(data, colWidths=colWidths)
        self.table_style_set(data, 12)
        # table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), self.my_specific_font, 12),
        #                 ("VALIGN", (1, 1), (-1, -1), "TOP"),
        #                 # ("VALIGN", (1, 1), (-1, -1), "MIDDLE"),
        #                 ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        #                 # ('BOX', (0, 0), (-1, -1), 0.25, colors.black), #boox around
        #                 # ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        #                 # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.darkgrey),
        #                 ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
        #                 ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.darkgrey),
        #                 ('LINEBELOW', (0, -1), (-1, -1), 2, colors.darkgrey)
        #                 ]))
        
        # self.elements.append(Spacer(1,85))
        self.elements.append(KeepTogether(table))
        # self.elements.append(table)
        # self.elements.append(Indenter(left=-60))
    
    # ---------------------------------- create clinical history in aba2 start
    #
    # def create_clinical_history(self):
    #     """
    #     this is Alam Molle's multipage for just plain text. We ussually find
    #     multipage for table but for report EEG we need this
    #     """
    #     # pdfmetrics.registerFont(ttfonts.TTFont('TNR', 'times.ttf'))
    #     # pdfmetrics.registerFont(ttfonts.TTFont('TNRB', 'timesbd.ttf'))
    #
    #
    #     # self.styles = getSampleStyleSheet()
    #     # full_name_Title = 'Clinical History'
    #     #
    #     # ptext = '<font size=18>%s</font>' % full_name_Title
    #     #
    #     # p = Paragraph(ptext, self.styles["Heading2"])
    #     # self.elements.append(Paragraph(ptext, self.styles["Heading2"]))
    #     # p.wrapOn(canvas, width, height)
    #     # self.elements.append(Paragraph(paragraph, stylesheet['Paragraph']))
    #
    #
    #     stylesheet = getSampleStyleSheet()
    #     stylesheet.add(ParagraphStyle(name='Paragraph',
    #                                   # fontName='TNR',
    #                                   # fontName="Helvetica",
    #                                   fontSize=12,
    #                                   spaceAfter=10,
    #                                   leading=20, parent=stylesheet['Normal']))  # leading =space among lines
    #     # leading=20, parent=stylesheet['BodyText']))  # leading =space among lines
    #     # stylesheet.leftIndent = first.leftIndent
    #     # stylesheet.add(ParagraphStyle(name='Paragraph',
    #     #                            # fontName="Helvetica-Bold",
    #     #                            fontName="Helvetica",
    #     #                            fontSize=12,
    #     #                            parent=stylesheet['Normal'],
    #     #                            alignment=1,
    #     #                            spaceAfter=14))
    #     #
    #
    #     elements = []
    #     # Create a long paragraph with multiple line breaks.
    #
    #     paragraph = Pages.history_report_object
    #         # paragraph += "<br/><br/>"
    #     # paragraph += "Lorem ipsum dolor sit amet, consectetur adipiscing elit." * 10
    #     # paragraph += "<br/><br/>"
    #     # paragraph *= 10
    #     # self.elements.append(Paragraph(ptext, self.styles["Heading2"]))
    #     # self.elements.append(p)
    #     self.elements.append(Paragraph(paragraph, stylesheet['Paragraph']))
    #     self.elements.append(Spacer(1, 30))
    
    # ----------------------------------
    
    def create_complete_pdf(self):
        """
        This is the main pdf creator
        """
        # ------------------to allow or deny table in pdf header start
        self.retrieve_Table_header_YorN_radiob78_json()
        # print('self.json_show_or_not_Table_radiob78_aba4_var in create',
        # self.json_show_or_not_Table_radiob78_aba4_var)
        
        # try:
        if self.json_show_or_not_Table_radiob78_aba4_var == 1:
            self.eeg_report_title()  # = this allows table in header
        elif self.json_show_or_not_Table_radiob78_aba4_var == 2:
            pass
        # except:
        else:
            # self.eeg_report_title()
            return
        # ------------------to allow or deny table in pdf header end
        
        if Pages.create_clinical_info_report == 1:  # says that we are creating a clinical history and not main pdf
            self.create_history_title()  # use title "CLINICAL HISTORY"
        else:  # exclude the title of history because we are creating the main pdf
            pass  # dont use title "CLINICAL HISTORY'
        
        self.create_body()
        # self.create_clinical_history()     #with this it prints report and pdf
        self.eeg_report_footer()
        # self.end_footer()
        self.header_in_all_pages()
        
        # self.footer_end()
    
    def header_in_all_pages(self):
        """"""
        a = Header()
        # doc = self.doc
        # self.elements.append(KeepTogether(Spacer(self.width, self. height)))
        try:
            self.doc.build(self.elements, onFirstPage=a.header, onLaterPages=a.header)
            return
        
        except FileNotFoundError:
            # try:
            if self.json_port_eng_radiob34_aba4_var == 1:
                tk.messagebox.showerror(title='Houston We Have A Problem...',
                                        message="You are trying to overwrite"
                                                " an open File or,"
                                                " header or signature images,"
                                                " are missing.")
            elif self.json_port_eng_radiob34_aba4_var == 2:
                tk.messagebox.showerror(title='Algo deu errado, desculpe!',
                                        message="Você está tentando sobrescrever"
                                                "um pdf aberto, ou imagens, "
                                                " não foram encontradas.")
        
        #     except:
        #         # tk.messagebox.showerror(title='Houston We Have A Problem...',
        #         #                         message="You are trying to recreate"
        #         #                                 "an open File, close it first,"
        #         #                                 " please.")
        #         pass
        # #
        
        # debug:
        # self.doc.build(canvas, onFirstPage=a.header, onLaterPages=a.header)
        # ,  onFirstPage=self.gen_Header_Table, onLaterPages=self.gen_Header_Table) #, onFirstPage=self.create_header)
    
    @staticmethod
    def print_report():
        # webbrowser.open(Pages.patient_object +'.pdf')
        webbrowser.open(Pages.outfilepath_to_pages)
    
    @staticmethod
    def store_path_of_mainfile_json(from_askfile):
        """
        store json to build pdf portuguese or english not used yet , created just in case
        """
        filepath_get = from_askfile
        # Pages.portuguese_or_english = portuguese_or_english_get
        # current_path_file = '../main_file_path_to_use.json'  # use the file extension .json
        current_path_file = 'main_file_path_to_use.json'  # use the file extension .json
        with open(current_path_file, 'w') as file_object:  # open the file in write mode
            json.dump(filepath_get, file_object)
            # json.dump() function to store the set of numbers in numbers.json file
    
    @staticmethod
    def retrieve_path_of_mainfile_json():
        """
        retrieve_lframe1_aba4_json
        get option from aba4 if page size chosen is  letter (1) or A4(2)
        """
        
        # try:
        # with open('../main_file_path_to_use.json') as file_object_db:
        with open('main_file_path_to_use.json') as file_object_db:
            main_filename = json.load(file_object_db)
            return main_filename
        # except:
        #     main_filename = "C://"
        #     return main_filename
    
    def list_report_variables(self):
        
        Pages.header_object = self.txt_header.get('1.0', 'end-1c')
        Pages.id_object = self.Id_entry.get()
        Pages.date_object = self.report_Date_entry.get()
        Pages.patient_object = self.patient_entry.get()
        Pages.gender_object = self.gender_chosen
        Pages.age_object = self.age_entry.get()
        Pages.diagnosis_object = self.diag_entry.get()
        Pages.low_f_f_object = self.LFF_entry.get()
        Pages.high_f_f_object = self.HFF_entry.get()
        Pages.sample_rate_object = self.srate_entry.get()
        Pages.body_Report_object = self.txt_body.get('1.0', 'end-1c')
        Pages.doctor_name = self.txt_footer.get('1.0', 'end-1c')
        Pages.listaCli_imagePath_logo = self.signature_img_entry_logo.get()
        Pages.listaCli_imagePath = self.signature_img_entry.get()
        Pages.history1_object = self.txt_history1.get('1.0', 'end-1c')
        Pages.history_report_object = self.txt_history.get('1.0', 'end-1c')
    
    def create_individual_reports(self):
        """
        before creating pdf
        we must 'entry.get'  the variables
        this function is used inside  other functions
        as 'create_main_body_report(self)'
        to generate different pdfs
        the catch is the following: all pdfs have same header and footer info,
        the  body is different for each new pdf, for instance
        'create_main_body_report()'= is the pdf for main report
        but  'create_clinical_info_report' pdfs is in aba2 and so on.
        We call this function to have all variables updated in pdf

        """
        global pdf_file
        self.list_report_variables()
        
        # ---------------------------
        # get initialdir='/':
        
        main_filename = ''
        self.retrieve_path_of_mainfile_json()
        
        # ---------------------------
        # try:
        # pdf_file = "discoll_multipage6.pdf"
        if Pages.create_clinical_info_report == 0:  # says we are creating main report
            if Pages.patient_object == '':
                pdf_file = (Pages.id_object + '.pdf')
            else:
                pdf_file = (Pages.patient_object + '.pdf')
        
        elif Pages.create_clinical_info_report == 1:
            if Pages.patient_object == '':
                pdf_file = (Pages.id_object + 'history.pdf')
            else:
                pdf_file = (Pages.patient_object + '_history.pdf')
        
        # except:
        else:
            pdf_file = (Pages.id_object + 'history.pdf')
        
        # data_pdf = [("All Files", "*.*"),('PDF Files', '*.pdf')]
        data_pdf = [('PDF Files', '*.pdf')]
        main_filename = filedialog.asksaveasfilename(initialdir=main_filename, title='Save File',
                                                     # main_filename = filedialog.asksaveasfilename(
                                                     # initialdir=os.path.normpath("C://"), title='Save File',
                                                     initialfile=pdf_file, filetypes=data_pdf,
                                                     defaultextension="*.pdf")  # don't need to write extension
        
        # print(main_filename) --> C:/000_tmp/teste09.pdf
        if not main_filename:  # if you cancel folder opening
            initialdir = os.path.normpath("C://")
        #
        else:
            self.store_path_of_mainfile_json(main_filename)
            # creates 'main_file_path_to_use.json'  that goes in initialdir above
            # it allows to open in the last folder used
            
            # outfilename = pdf_file
            outfiledir = main_filename
            # outfilepath = os.path.join(outfiledir, outfilename)
            outfilepath = os.path.join(outfiledir)  # this is just the path without the file at end
            Pages.outfilepath_to_pages = outfilepath
            # doc = SimpleDocTemplate(outfilepath)
            # EEG_Report = EEG_PDF_Report(pdf_file)
            
            EEG_Report = EegPdfReport(outfilepath)
            
            EEG_Report.create_complete_pdf()  # here we are creating pdf in fact
            
            # ------ show or not the pdf after creation in another app like acrobat
            self.retrieve_show_or_not_pdf_radiob56_aba4_json()
            
            # try:
            if self.json_show_or_not_PDFradiob56_aba4_var == 1:
                EEG_Report.print_report()
            elif self.json_show_or_not_PDFradiob56_aba4_var == 2:
                return
            # except:
            else:
                return
                # EEG_Report.print_Report()
    
    def create_main_body_report(self):
        
        # this is the main text of primary report:
        Pages.body_Report_object = self.txt_body.get('1.0', 'end-1c')
        Pages.create_clinical_info_report = 0
        self.create_individual_reports()
    
    def create_clinical_info_report(self):
        # this is the main text of primary report:
        # self.styles = getSampleStyleSheet()
        # self.elements = []
        # paragraph = 'test'
        # self.elements.append(Paragraph(paragraph, self.styles['Paragraph']))
        #
        Pages.create_clinical_info_report = 1  # says we are getting  self.txt_history
        # self.create_history_title() # function that just creates the title of clinical
        # history before main text
        Pages.body_Report_object = self.txt_history.get('1.0', 'end-1c')
        
        self.create_individual_reports()


class Application(FuncInDBGen, EegPdfReport, Funcs, ToolTip):  # Funcs to application use Funcs functions
    
    def __init__(self):
        
        super().__init__()

        self.bt_text_subscript = None
        self.tkimage4e = None
        self.bt_text_superscript = None
        self.tkimage4d = None
        self.bt_text_underline = None
        self.tkimage4c = None
        self.bt_text_italics = None
        self.tkimage4b = None
        self.bt_text_bold = None
        self.tkimage4a = None
        self.bt_delete_all3 = None
        self.lframe5_aba4 = None
        self.radiob1_arrow_aba4 = None
        self.collected_image = None
        self.lb_frame_Tree_aba3 = None
        self.scrool_List = None
        self.listaCli = None
        self.scrool_history = None
        self.bt_Report_aba2 = None
        self.bt_save_update_aba2 = None
        self.bt_delete_history = None
        self.frame_Tree_aba3 = None
        self.frame_history = None
        self.scrool_txt_history1 = None
        self.lb_txt_history1 = None
        self.scrool_footer = None
        self.lb_footer = None
        self.scrool_body = None
        self.lb_body = None
        self.scrool_header = None
        self.lb_header = None
        self.lframe10_button = None
        self.lframe10_label = None
        self.lframe10_aba4 = None
        self.lframe9_label1 = None
        self.lframe9_aba4 = None
        self.radiob2_arrow_aba4 = None
        self.radiob_arrow_aba4_var = None
        self.lframe8_aba4 = None
        self.lframe7_button = None
        self.lframe7_label = None
        self.lframe7_aba4 = None
        self.pdf_combo2label = None
        self.radiob2_cbox_aba4 = None
        self.radiob1_cbox_aba4 = None
        self.radiob90_1or2_aba4_var = None
        self.radiob_cbox_aba4_var = None
        self.pdf_combo1label = None
        self.font_comboB_aba4 = None
        self.reportlab_fonts_to_use = None
        self.font_chosen_cbox = None
        self.lframe6_aba4 = None
        self.pdf_titlename_entry = None
        self.pdf_titlename_var = None
        self.pdf_titlenamelabel = None
        self.radiobutton0 = None
        self.radiobutton9 = None
        self.radiobutton8 = None
        self.radiobutton7 = None
        self.radiob78_aba4_var = None
        self.lframe4_aba4 = None
        self.radiobutton6 = None
        self.radiobutton5 = None
        self.radiob56_aba4_var = None
        self.lframe3_aba4 = None
        self.radiobutton4 = None
        self.radiobutton3 = None
        self.radiob34_aba4_var = None
        self.lframe2_aba4 = None
        self.radiobutton2 = None
        self.radiobutton1 = None
        self.radiob1_aba4_var = None
        self.bt_image_stop_ab4 = None
        self.lframe1_aba4 = None
        self.label_1_canvas2_aba4 = None
        self.text_l1Cvas2aba4 = None
        self.canvas1_aba4 = None
        self.frame_patient_history1 = None
        self.frame_footer = None
        self.frame_body = None
        self.frame_header = None
        self.report_date = None
        self.report_Date_label = None
        self.srate_label = None
        self.HFF_label = None
        self.LFF_label = None
        self.diag_label = None
        self.age_label = None
        self.comboGender = None
        self.sex_chosen = None
        self.gender_label = None
        self.patient_label_aba1 = None
        self.Id_label = None
        self.bt_image_stop_ab3 = None
        self.bt_image_stop_ab2 = None
        self.bt_image_stop = None
        self.tkimage6 = None
        self.bt_image_help = None
        self.tkimage5a = None
        self.bt_Report_aba1 = None
        self.db_path_cbox = None
        self.db_path_aba3_cbox = None
        self.db_path_aba3 = None
        self.bt_Report3 = None
        self.bt_get_signature_aba3 = None
        self.bt_get_signature_aba1 = None
        self.bt_get_logo_aba3 = None
        self.bt_get_logo_aba1 = None
        self.bt_movedown3 = None
        self.bt_ascending3 = None
        self.bt_delete_1 = None
        self.bt_save_update_aba1 = None
        self.bt_add_record = None
        self.bt_delete_signature_aba3 = None
        self.bt_delete_logo_aba3 = None
        self.search_patient_entry3 = None
        self.bt_search3 = None
        self.canvas = None
        self.aba4 = None
        self.aba3 = None
        self.aba2 = None
        self.aba1 = None
        self.abas = None
        self.bt_delete_table = None
        self.tkimage10 = None
        self.bt_show_all = None
        self.tkimage14 = None
        self.bt_del_many = None
        self.tkimage13 = None
        self.bt_del_this_one = None
        self.tkimage12 = None
        self.bt_duplicate3 = None
        self.tkimage11 = None
        self.bt_delete_report = None
        self.tkimage9 = None
        self.bt_pdf_history = None
        self.tkimage82 = None
        self.bt_delete_history_only = None
        self.tkimage81 = None
        self.bt_save_history = None
        self.tkimage80 = None
        self.bt_not_history = None
        self.tkimage8 = None
        self.bt_clear_fields = None
        self.tkimage7 = PhotoImage(file=resource_path("del_all.png"))
        self.bt_image_pdf = None
        self.tkimage5 = PhotoImage(file=resource_path("main_pdf.png"))
        self.bt_image_update = None
        self.tkimage4 = PhotoImage(file=resource_path("salvar_update_100.png"))
        self.bt_image_save = None
        self.tkimage3 = PhotoImage(file=resource_path("salvar_100.png"))
        self.signature_image_logo = None
        self.text_bt_image_save = None
        self.text_bt_delete_table = None
        self.text_bt_show_all = None
        self.text_bt_del_many = None
        self.text_bt_del_this_one = None
        self.text_bt_duplicate3 = None
        self.text_bt_delete_report = None
        self.text_bt_pdf_history = None
        self.text_bt_delete_history_only = None
        self.text_bt_save_history = None
        self.text_bt_clear_keep_story = None
        self.text_bt_clear_fields = None
        self.text_bt_image_pdf = None
        self.text_bt_image_update = None
        self.scrool_terms = None
        self.lb_history = None
        self.txt_terms = None
        self.termsUse_label = None
        self.termsUse_var = None
        self.multiple_termsUseWindow = None
        self.multiple_sqliteWindow = None
        self.active_text_frame = None
        self.retrieved_Pdf_Title_radiob90_aba4_var_json = None
        self.aba = None
        self.json_port_eng_radiob34_aba4_var = None
        self.widgets_with_icon()
        self.root = root
        
        self.make_frames_widgets()
        self.tela()
        self.icon_images()
        
        # goes to self.db_path_aba3_cbox ['values'] = Pages.EEG_report_databanks_list:
        now = datetime.now()
        self.determine_date()
        self.get_databk_values_to_cbox()
        self.root_widgets()
        self.make_frames_widgets()
        # Funcs()
        # Pages.EEG_report_databanks_list == ''
        self.frame_Sql3_List(self.frame_Tree_aba3)
        self.create_Table()
        self.select_lista()
        self.report_variables()
        
        self.translate_lang_01()
        
        self.aba4_translation()
        
        self.widgets_with_icon()
        # self.translate_ToolTip()
        
        # self.collect_image_footer()
        self.organize_list_arrow()
        root.mainloop()
    
    def tela(self):
        self.root.title('EEG Weaver Module Report 1.1')
        # self.root.configure(background='#d1d1d1')
        self.root.configure(background='#708090')
        # self.root.configure(background='#353935')
        # Hex Codes: #d1d1d1 // #e1dbd6 // #e2e2e2 // #f9f6f2 // #ffffff
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        # self.root.geometry(f'{width/2}x{height/2}')  # half of fullscreen
        # self.root.geometry('%sx%s' % (int(width), int(height)))
        self.root.geometry('%sx%s' % (int(width / 1.2), int(height / 1.07)))  # percentage of fullscreen
        self.center()
        # self.root.resizable(False, False)
        self.root.resizable(True, True)
        # self.minsize(height, width)
        self.root.maxsize(int(width), int(height))
    
    def get_databk_values_to_cbox(self):
        # values of self.db_path_aba3_cbox combobox comes from module EEG_weaver_multiple_sqlite:
        # open Databank_generator in multiple_sqlite_window
        # to get path_name of Reporter DB
        # we call multiple_sqlite_window to get the list of path and names of the report databanks created
        # to use in self.db_path_aba3_cbox
        
        self.multiple_sqlite_window()  # open module
        # print('ANTES', Pages.EEG_report_databanks_list)
        # then we close it to avoid topwindow over main window:
        self.exit_multiple_sqlite_window()  # close module
        # now we've  got the information -->
        # print('depois',Pages.EEG_report_databanks_list) from treeview
        # print('depois get_databk_values_to_cbox',Pages.EEG_report_databanks_list)
        # ['C:/000_tmp/test.db.db', 'C:/000_tmp/test.db.db', 'C:/000_tmp/test.db.db']
    
    # def get_databk_values_to_cbox2(self):
    #
    #     self.exit_multiple_sqlite_window()  # close module
    #     self.multiple_sqlite_window()  # open module
    
    def click_frame(self, event):
        """
        this method works when we click inside a frame (in this case text widgets)
         to get the name of the frame
        the name used in these funtions  bellow allow us to change the parameter
         ex self.txt_header (name of text widgets)
        
        example:
        self.make_normal(self.txt_header)
        self.make_bold(self.txt_header)
        because we have 3 text widgets (frames) in aba one, we must change the self.txt_header
        for other frames to change text bold or normal in each frame using the same buttons
        
        """
        self.active_text_frame = event.widget.widget
        return self.active_text_frame
    
    def exit_multiple_sqlite_window(self):
        # newWindow = lay[0]
        self.multiple_sqliteWindow.quit()
        self.multiple_sqliteWindow.destroy()
    
    def multiple_sqlite_window(self):
        """
        this is a modal window (freezes other windows) to open the window that builds
        new databanks when  "Data Banks" are clicked in aba3.
        """
        x = root.winfo_x()
        y = root.winfo_y()
        # self.multiple_sqliteWindow = tk.Toplevel(root)
        self.multiple_sqliteWindow = tk.Toplevel()
        self.multiple_sqliteWindow.geometry('850x600')
        self.multiple_sqliteWindow.geometry("+%d+%d" % (x + -100, y + 200))
        self.multiple_sqliteWindow.resizable(False, False)
        # self.multiple_sqliteWindow.transient(self.root)
        self.multiple_sqliteWindow.focus_force()  # stays in fronmt
        
        self.multiple_sqliteWindow.grab_set()  # deny typing in another window
        DatabankGenerator(self.multiple_sqliteWindow)
        # self.multiple_sqliteWindow.wait_window()  # and wait here until win destroyed
        # self.make_it_modal()
        
        # Databank_Generator.create_Table_fidbgen(Databank_Generator)
        # FuncInDBGen.get_path_name_db_list(FuncInDBGen)
        # print(Pages.EEG_report_databanks_list)
        
        # def multiple_sqlite_window_1(self):
        #     x = root.winfo_x()
        #     y = root.winfo_y()
        #     # self.multiple_sqliteWindow = tk.Toplevel(root)
        #     self.multiple_sqliteWindow = tk.Toplevel()
        #     self.multiple_sqliteWindow.geometry('850x600')
        #     self.multiple_sqliteWindow.geometry("+%d+%d" % (x + -100, y + 200))
        #     self.multiple_sqliteWindow.resizable(False, False)
        #     # self.multiple_sqliteWindow.transient(self.root)
        #     self.multiple_sqliteWindow.focus_force()  # stays in fronmt
        #
        #     self.multiple_sqliteWindow.grab_set()  # deny typing in another window
        #     Databank_Generator(self.multiple_sqliteWindow)
        # -------------------------
    
    def multiple_window_terms_use(self):
        """
        create a modal window for show terms of use
        """
        
        x = root.winfo_x()  # where this windows appear in screen coordinates
        y = root.winfo_y()  # where this windows appear in screen coordinates
        self.multiple_termsUseWindow = tk.Toplevel()
        # self.multiple_termsUseWindow = tk.Toplevel()
        self.multiple_termsUseWindow.geometry('850x600')
        self.multiple_termsUseWindow.geometry("+%d+%d" % (x + -100, y + 200))
        self.multiple_termsUseWindow.resizable(False, False)
        # self.multiple_sqliteWindow.transient(self.root)
        self.multiple_termsUseWindow.focus_force()  # stays in fronmt
        
        self.multiple_termsUseWindow.grab_set()  # deny typing in another window
        self.config_label_style()
        
        self.termsUse_var = tk.StringVar()
        
        self.termsUse_var.set("TERMS OF USE.")
        
        self.termsUse_label = ttk.Label(self.multiple_termsUseWindow,
                                        textvariable=self.termsUse_var,
                                        style="Custom.TLabel",
                                        font="Helvetica 20 bold",
                                        )
        self.termsUse_label.place(relx=0.007, rely=0.05, relwidth=0.986, relheight=0.12)
        # ------------------------
        self.txt_terms = tk.Text(self.multiple_termsUseWindow, bg='#DCDCDC', height=5)
        # self.txt_history.configure(font=Font_tuple)  #CONFIGURE FONT
        self.txt_terms.place(relx=0.03, rely=0.215, relwidth=0.935, relheight=0.7)
        self.txt_terms.insert(tk.END, Pages.terms_of_use)
        self.txt_terms.config(state=tk.DISABLED)
        
        self.lb_history = tk.Label(self.multiple_termsUseWindow, text='READ..WITH..ATTENTION', font='Arial 8 bold',
                                   wraplength=1)
        self.lb_history.place(relx=0.01, rely=0.215, relwidth=0.02, relheight=0.7)
        
        # this make </br> insert in tk.Text when <Return> is pressed
        # self.txt_history.bind("<Return>", lambda event: self.insert_in_Textwidget(event, self.txt_history))
        
        # self.scrool_terms = tk.Scrollbar(self.multiple_termsUseWindow,
        # orient='vertical', command=self.txt_header.yview)
        self.scrool_terms = tk.Scrollbar(self.multiple_termsUseWindow, orient='vertical', command=self.txt_terms.yview)
        self.txt_terms.configure(yscroll=self.scrool_history.set)
        self.scrool_terms.place(relx=0.965, rely=0.215, relwidth=0.025, relheight=0.7)
        
        # -------------------------
    
    # def make_it_modal(self):
    #     """
    #     modal mode  .wait_window() very important to stop main gui
    #     open another one, create and get information, close second window
    #     and give info back to main gui
    #     """
    #     self.multiple_sqliteWindow.wait_window()
    
    def make_it_modal(self, opended_window):
        """
        modal mode  .wait_window() very important to stop main gui
        open another one, create and get information, close second window
        and give info back to main gui
        """
        if opended_window == self.multiple_sqliteWindow:
            self.multiple_sqliteWindow.wait_window()
        
        elif opended_window == self.multiple_termsUseWindow:
            self.multiple_termsUseWindow.wait_window()
    
    def multiple_window_terms_use_modal(self):
        """
        modal stops the loop and waits closing the window to get the variable needed
        
        https://stackoverflow.com/questions/67754560/how-to-get-the-updated-entry-string
        -from-a-toplevel-window-before-the-tkinter-ma
        
        """
        # def multiple_sqlite_window(self)
        
        self.multiple_window_terms_use()
        self.make_it_modal(self.multiple_termsUseWindow)
        # Pages.EEG_report_databanks_list = self.db_path_cbox
        
        # self.db_path_cbox =  Pages.EEG_report_databanks_list
        # self.db_path_aba3_cbox.config(values=Pages.EEG_report_databanks_list)
    
    # -----------------------
    def multiple_sqlite_window_modal(self):
        """
        modal stops the loop and waits closing the window to get the variable needed

        https://stackoverflow.com/questions/67754560/how-to-get-the-updated-entry-string
        -from-a-toplevel-window-before-the-tkinter-ma

        def multiple_sqlite_window(self) is used in many places , so modal .wait_window
        deny visualization of main window if always associated, modal must be used just here in
        button Data Bases |(use of this function)

        """
        # def multiple_sqlite_window(self)
        
        self.multiple_sqlite_window()
        self.make_it_modal(self.multiple_sqliteWindow)
        # Pages.EEG_report_databanks_list = self.db_path_cbox
        
        # self.db_path_cbox =  Pages.EEG_report_databanks_list
        self.db_path_aba3_cbox.config(values=Pages.EEG_report_databanks_list)
    
    # -----------------------
    
    def select_radiob34_aba4_var(self):
        """
        returns '1' or '2', if 1 english is 2 portuguese
        to be used in Reportlab classes above
        """
        choice = self.radiob34_aba4_var.get()
        self.json_port_eng_radiob34_aba4_var = self.radiob34_aba4_var.get()
        
        # print('this is choice in select_radiob34_aba4_var', choice )
        
        Pages.portuguese_or_english = choice
        self.store_port_or_engl_json()
        # Application()
        return self.json_port_eng_radiob34_aba4_var
    
    def select_radiob56_aba4_var(self):
        """
        returns '1' or '2', if 1 show pdf after creation
        2 don't show pdf after creation
        to be used in Reportlab classes above
        """
        choice = self.radiob56_aba4_var.get()
        Pages.show_or_not_pdf_after_creation = choice
        self.store_show_or_not_pdf_json()
        # Application()
        return self.radiob56_aba4_var.get()
    
    def select_radiob78_aba4_var(self):
        """
        returns '1' or '2', if 1 keep table in header of pdf
        2 don't keep table in header of pdf
        to be used in Reportlab
        """
        choice = self.radiob78_aba4_var.get()
        # Pages.show_or_not_pdf_after_creation = choice
        self.store_Table_header_YorN_radiob78_json()
        # Application()
        # return self.radiob78_aba4_var.get()
    
    def store_newPdfTitle_entry_aba4(self):
        """
        create new name in  self.pdf_titlename_entry selected in def root_widgets
        to be used instead of title= Electroencephalogram
        correspond to  self.radiob90_1or2_aba4_var
        """
        self.radiob90_1or2_aba4_var.get()  # get 1 "Electroencefalogram" or 2 "new name" from radiobutton9
        
        if self.radiob90_1or2_aba4_var.get() == 1:
            pdf_Newtitle_from_entry_json = 'Electroencephalogram (EEG) Report'
            # return pdf_Newtitle_from_entry_json
        
        else:  # or 2 if you will
            # # get from self.pdf_titlename_entry:
            #
            pdf_Newtitle_from_entry_json = self.pdf_titlename_var.get()
        
        current_pdf_title_from_entry = resource_path('pdf_Newtitle_from_entry_json.json')
        #
        with open(current_pdf_title_from_entry, 'w') as file_object:  # open the file in write mode
            json.dump(pdf_Newtitle_from_entry_json, file_object)
            # json.dump() function to stores the set of numbers in numbers.json file
            #
            return pdf_Newtitle_from_entry_json
        # print(self.radiob90_1or2_aba4_var.get())
    
    def translate_tool_tip(self):
        try:
            if self.json_port_eng_radiob34_aba4_var == 1:
                self.text_bt_image_save = 'Save as New Report'
                self.text_bt_image_update = 'Save Changes Before Closing'
                self.text_bt_image_pdf = 'Create and Save Report to PDF'
                self.text_bt_clear_fields = 'Delete all Fields'
                self.text_bt_clear_keep_story = 'Delete all Fields keep Clinical Story'
                self.text_bt_save_history = 'Save Clinical Story Text'
                self.text_bt_pdf_history = 'Clinical History to PDF'
                self.text_bt_delete_report = 'Delete This Report'
                self.text_bt_duplicate3 = 'Duplicate Report'  # delete table =same as delete report
                self.text_bt_del_this_one = 'Delete Report Selected'  # delete table =same as delete report
                self.text_bt_del_many = 'Delete Many - Ctrl-Lmouse'  # delete table =same as delete report
                self.text_bt_show_all = 'Show All Reports'  # delete table =same as delete report
                self.text_bt_delete_table = "Delete All Reports"
                # 'Drop Table'     #delete table =same as delete report
            
            elif self.json_port_eng_radiob34_aba4_var == 2:
                self.text_bt_image_save = 'Salve como Laudo Novo'
                self.text_bt_image_update = 'Salve Atualizações antes de Fechar'
                self.text_bt_image_pdf = 'Crie e Salve Laudo em PDF'
                self.text_bt_clear_fields = 'Apague todos os Campos'
                self.text_bt_clear_keep_story = 'Apague todos os Campos mantenha História Clínica'
                self.text_bt_save_history = 'Salve História Clínical'
                self.text_bt_delete_history_only = 'Delete History Only'
                self.text_bt_delete_history_only = 'Apague Apenas a História Clínica'
                self.text_bt_pdf_history = 'Crie PDF da História Clínica'
                self.text_bt_delete_report = 'Apague este Laudo'
                self.text_bt_duplicate3 = 'Duplicar o Laudo'  # delete table =same as delete report
                self.text_bt_del_this_one = 'Apague Laudo Selecionado'  # delete table =same as delete report
                self.text_bt_del_many = 'Apague Vários - Ctrl-Lmouse'  # delete table =same as delete report
                self.text_bt_show_all = 'Listar todos os Laudos'  # delete table =same as delete report
                self.text_bt_delete_table = "Apague Todos os Laudos"
                # 'Drop Table'     #delete table =same as delete report
        
        except OSError:
            self.text_bt_image_save = 'save as new report'
            # FileNotFoundError is a subclass of OSError,
        
        self.create_tool_tip(self.bt_image_save, self.text_bt_image_save)
        self.create_tool_tip(self.bt_image_update, self.text_bt_image_update)
        self.create_tool_tip(self.bt_image_pdf, self.text_bt_image_pdf)
        self.create_tool_tip(self.bt_clear_fields, self.text_bt_clear_fields)
        self.create_tool_tip(self.bt_not_history, self.text_bt_clear_keep_story)
        self.create_tool_tip(self.bt_save_history, self.text_bt_save_history)
        self.create_tool_tip(self.bt_delete_history_only, self.text_bt_delete_history_only)
        self.create_tool_tip(self.bt_pdf_history, self.text_bt_pdf_history)
        self.create_tool_tip(self.bt_delete_report, self.text_bt_delete_report)
        self.create_tool_tip(self.bt_duplicate3, self.text_bt_duplicate3)
        self.create_tool_tip(self.bt_del_this_one, self.text_bt_del_this_one)
        self.create_tool_tip(self.bt_del_many, self.text_bt_del_many)
        self.create_tool_tip(self.bt_show_all, self.text_bt_show_all)
        self.create_tool_tip(self.bt_delete_table, self.text_bt_delete_table)
    
    def translate_lang_01(self):
        # Funcs.retrieve_portg_or_eng_radiob34_aba4_json()
        # function to get the value of
        # self.json_port_eng_radiob34_aba4_var in Funcs
        # style = ttk.Style()
        # try:
        if self.json_port_eng_radiob34_aba4_var == 1:
            self.abas.add(self.aba1, text="Edit Report and create PDF")
            self.abas.add(self.aba2, text="Add Clinical History")
            self.abas.add(self.aba3, text="Report List")
            self.abas.add(self.aba4, text="Configure")
            
            self.bt_clear_fields.config(text='Clear Fields')
            self.bt_not_history.config(text='Clear Keep History')
            self.bt_search3.config(text="Search Patient's name:")
            # self.bt_show_all_aba3.config(text="Show all Reports")
            self.bt_delete_logo_aba3.config(text="Delete Logo")
            self.bt_delete_signature_aba3.config(text="Delete Signature")
            self.bt_add_record.config(text='Save New')
            # self.bt_add_record3.config(text='Save New')
            self.bt_save_update_aba2.config(text='Save Update')
            # self.bt_save_update3.config(text='Save Update')
            self.bt_duplicate3.config(text='Duplicate Report')
            self.bt_delete_1.config(text='Delete This Report')
            # self.bt_delete_3.config(text='Delete One Selected')
            # self.bt_delete_many3.config(text='Delete Many')
            # self.bt_delete_all3.config(text='Delete All')
            self.bt_get_logo_aba1.config(text='Get Logo')
            self.bt_get_logo_aba3.config(text='Get Logo')
            self.bt_get_signature_aba1.config(text='Get Signature')
            self.bt_get_signature_aba3.config(text='Get Signature')
            self.bt_Report3.config(text='Report to PDF')
            # self.bt_Report.config(text='Report to PDF')
            # self.patient_label.config(text='Patient:')
            self.gender_label.config(text='Gender:')
            # self.radiobutton1.config(text="Letter")
            # self.sex_chosen = ["Male", "Female"]
            self.age_label.config(text='Age:')
            self.diag_label.config(text='Diagnosis:')
            self.srate_label.config(text='Sampling Rate:')
            self.report_Date_label.config(text='Report Date:')
            # self.lframe1_aba4.config(text="Page size")
            # self.lframe2_aba4.config(text='Switch Language')
            # self.lframe3_aba4.config(text='Show PDF after creation?')
            # self.radiobutton5.config(text="Show PDF File")
            # self.radiobutton6.config(text="Don't Show PDF.")
            self.bt_delete_history.config(text='Delete History Only')
            # self.bt_save_update.config(text='Save Text')
            # self.bt_Report.config(text='Clinical History to PDF')
            self.lb_header.config(text='HEADER')
            self.lb_body.config(text='EEG..REPORT.. BODY')
            self.lb_footer.config(text="DOCTOR")
            self.lb_txt_history1.config(text="END")
            self.lb_history.config(text='PATIENT..HISTORY')
            
            # self.listaCli.heading("#0", text="")  # do not have a column associated
            # self.listaCli.heading("#1", text="Id")
            # self.listaCli.heading("#2", text="Patient")
            # self.listaCli.heading("#3", text="Gender")
            # self.listaCli.heading("#4", text="Age")
            # self.listaCli.heading("#5", text="Diagnosis")
            # self.listaCli.heading("#6", text="LFF")
            # self.listaCli.heading("#7", text="HFF")
            # self.listaCli.heading("#8", text="SRate")
            # self.listaCli.heading("#9", text="RecDate")
            # self.listaCli.heading("#10", text="Header")
            # self.listaCli.heading("#11", text="Report")
            # self.listaCli.heading("#12", text="Doctor")
            # self.listaCli.heading("#13", text="Logo")
            # self.listaCli.heading("#14", text="Sign")
            # self.listaCli.heading("#15", text="End")
            # self.listaCli.heading("#16", text="History")
            #
            #
        
        elif self.json_port_eng_radiob34_aba4_var == 2:
            self.abas.add(self.aba1, text="Edite o Laudo e Crie o PDF")
            self.abas.add(self.aba2, text="História Clínica")
            self.abas.add(self.aba3, text="Lista de Laudos")
            self.abas.add(self.aba4, text="Configure")
            
            self.lb_header.config(text='TÍTULO')
            self.lb_body.config(text='EEG..CORPO..DO..LAUDO')
            self.lb_footer.config(text="DOUTOR")
            self.lb_txt_history1.config(text="FIM")
            self.lb_history.config(text='PACIENTE..HISTÓRIA')
            
            self.bt_add_record.config(text='Salve Novo')  # aba1
            self.bt_save_update_aba1.config(text='Salve Atualize')
            self.bt_save_update_aba2.config(text='Salve Atualize')
            self.bt_delete_1.config(text='Apagar este  Laudo')
            self.bt_get_logo_aba1.config(text='Pegar Logo')
            self.bt_get_logo_aba3.config(text='Pegar Logo')
            self.bt_get_signature_aba1.config(text='Pegar Assinatura')
            self.bt_get_signature_aba3.config(text='Pegar Assinatura')
            self.bt_Report_aba1.config(text='Gerar PDF')
            self.patient_label_aba1.config(text='Paciente:')
            self.gender_label.config(text='Gênero:')
            self.age_label.config(text='Idade:')
            self.diag_label.config(text='Diagnóstico:')
            self.srate_label.config(text='Amostragem:')
            self.report_Date_label.config(text='Data do Laudo:')
            
            self.bt_search3.config(text="Procurar Nome:")
            # self.bt_show_all_aba3.config(text="Mostrar todos Laudos")
            self.bt_delete_logo_aba3.config(text="Apagar Logo")
            self.bt_delete_signature_aba3.config(text="Apagar Assinatura")
            # self.bt_add_record3.config(text='Salve Novo')
            # self.bt_save_update3.config(text='Gravar mudança')
            self.bt_duplicate3.config(text='Duplicar Laudo')
            # self.bt_delete_1.config(text='Apagar este  Laudo')
            # self.bt_delete_3.config(text='Apagar Um Selecionado')
            # self.bt_delete_many3.config(text='Apagar Vários')
            self.bt_delete_all3.config(text='Apagar Todos')
            # self.bt_get_logo_aba1.config(text='Pegar Logo')
            # self.bt_get_logo_aba3.config(text='Pegar Logo')
            # self.bt_get_signature_aba1.config(text='Pegar Assinatura')
            # self.bt_get_signature_aba3.config(text='Pegar Assinatura')
            self.bt_Report3.config(text='Gerar PDF')
            # self.bt_Report.config(text='Gerar PDF')
            
            # self.sex_chosen = ["Homem", "Mulher"]
            # self.text_l1Cvas2aba4.set("Configure Opções e PDF.")
            
            # self.lframe1_aba4.config(text="Tamanho de Página")
            # self.lframe2_aba4.config(text="Mudar Idioma")
            # self.lframe3_aba4.config(text='Mostrar PDF após criado?')
            # self.radiobutton5.config(text='Mostrar PDF?')
            # self.radiobutton6.config(text="Não, depois vejo.")
            self.bt_delete_history.config(text='Apagar Apenas História')
            # self.bt_save_update.config(text='Salve Texto')
            self.bt_Report_aba2.config(text='História Clínica cria PDF')
            # self.radiobutton1.config(text="Carta")
            
            # self.listaCli.heading("#0", text="")  # do not have a column associated
            # self.listaCli.heading("#1", text="Id")
            # self.listaCli.heading("#2", text="Paciente")
            # self.listaCli.heading("#3", text="Sexo")
            # self.listaCli.heading("#4", text="Idade")
            # self.listaCli.heading("#5", text="Diagnóstico")
            # self.listaCli.heading("#6", text="LFF")
            # self.listaCli.heading("#7", text="HFF")
            # self.listaCli.heading("#8", text="txAmst")
            # self.listaCli.heading("#9", text="Data")
            # self.listaCli.heading("#10", text="Cabeçalho")
            # self.listaCli.heading("#11", text="Laudo")
            # self.listaCli.heading("#12", text="Doutor")
            # self.listaCli.heading("#13", text="Logo")
            # self.listaCli.heading("#14", text="Assin")
            # self.listaCli.heading("#15", text="Fim")
            # self.listaCli.heading("#16", text="História")
        
        # except Exception:
        #     return
    
    # def lista_cli_translate(self):
    #     current_db = (resource_path("current_db_used.json"))
    #
    #     if self.json_port_eng_radiob34_aba4_var == 1:
    #
    #         ALTER TABLE current_db RENAME COLUMN "Paciente" TO "Patient";
    #         ALTER TABLE current_db RENAME COLUMN "Sexo" TO "Gender";
    #         ALTER TABLE current_db RENAME COLUMN "Idade" TO "Age";
    #         ALTER TABLE current_db RENAME COLUMN "Diagnóstico" TO "Diagnosis";
    #         ALTER TABLE current_db RENAME COLUMN "txAmst" TO "txAmst";
    #         ALTER TABLE current_db RENAME COLUMN "Data" TO "RecDate";
    #         ALTER TABLE current_db RENAME COLUMN "Cabeçalho" TO "Header";
    #         ALTER TABLE current_db RENAME COLUMN "Laudo" TO "Report";
    #         ALTER TABLE current_db RENAME COLUMN "Doutor" TO "Doctor";
    #         ALTER TABLE current_db RENAME COLUMN "Assin" TO "Sign";
    #         ALTER TABLE current_db RENAME COLUMN "Fim" TO "End";
    #         ALTER TABLE current_db RENAME COLUMN "História" TO "History";
    #
    #     elif self.json_port_eng_radiob34_aba4_var == 2:
    #         ALTER TABLE current_db RENAME COLUMN "Paciente" TO "Patient";
    #         ALTER TABLE current_db RENAME COLUMN "Sexo" TO "Gender";
    #         ALTER TABLE current_db RENAME COLUMN "Idade" TO "Age";
    #         ALTER TABLE current_db RENAME COLUMN "Diagnóstico" TO "Diagnosis";
    #         ALTER TABLE current_db RENAME COLUMN "txAmst" TO "txAmst";
    #         ALTER TABLE current_db RENAME COLUMN "Data" TO "RecDate";
    #         ALTER TABLE current_db RENAME COLUMN "Cabeçalho" TO "Header";
    #         ALTER TABLE current_db RENAME COLUMN "Laudo" TO "Report";
    #         ALTER TABLE current_db RENAME COLUMN "Doutor" TO "Doctor";
    #         ALTER TABLE current_db RENAME COLUMN "Assin" TO "Sign";
    #         ALTER TABLE current_db RENAME COLUMN "Fim" TO "End";
    #         ALTER TABLE current_db RENAME COLUMN "História" TO "History";
    #
    #
    
    def collect_image_logo(self):
        """
        collect logo image from windows
        """
        self.collect_image()
        
        self.signature_image_logo = self.collected_image
        # print('self.signature_image_logo ', self.signature_image_logo)
        # G: / FOTOS PARA REVELAÇÃO /16997548134_4f805a60a4_o.jpg
        
        self.signature_img_entry_logo.delete(0, END)  # Remove any previous content from entry widget
        self.signature_img_entry_logo.insert(0, self.signature_image_logo)  # Insert new content in entry widget
        
        # debug
        # print("self.signature_img_entry_logo.get()",self.signature_img_entry_logo.get())
        # self.signature_img_entry_logo.get(),  G:/FOTOS PARA REVELAÇÃO/16997548134_4f805a60a4_o.jpg
        
        # self.get_footer_image_logo()
        # self.get_footer_image()
        # Pages.listaCli_imagePath_logo = self.listaCli_imagePath_logo
    
    def get_pdf_title_1_or_2(self):
        self.retrieve_Pdf_Title_1or2_radiob90_aba4_var_json()
        
        # try:
        if self.retrieved_Pdf_Title_radiob90_aba4_var_json == '':
            self.radiob90_1or2_aba4_var.set(1)
        else:
            self.radiob90_1or2_aba4_var.set(self.retrieved_Pdf_Title_1or2_aba4_var_json)
        # except Exception:
        #     self.radiob90_1or2_aba4_var.set(1)
    
    @staticmethod
    def create_tool_tip(widget, text):
        toolTip = ToolTip(widget)
        
        def enter(event):
            toolTip.showtip(text)
        
        def leave(event):
            toolTip.hidetip()
        
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)
    
    @staticmethod
    def help_html():
        """
        create a html help tha opens in browser
        """
        
        new = 1  # open in same tab, if possible
        # url = r"G:\PycharmProjects\EEG_WEAVER\reporter_compilation\html\index.html"
        # url = (resource_path("\html\index.html"))
        # url = 'resource_path\html\index.html'
        url = os.path.abspath("html/index.html")
        
        webbrowser.open(url, new=new)
    
    @staticmethod
    def restart_application():
        
        Application()
    
    def widgets_with_icon(self):
        # -----------------widgets aba1 and aba3 --------------- start
        
        abas = (self.aba1, self.aba2, self.aba3)
        
        for self.aba in abas:
            # self.tkimage3 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\salvar_100.png")
            # self.tkimage3 = self.tkimage3.zoom(25)  # with 250, I ended up running out of memory
            # self.tkimage3 = self.tkimage3.subsample(20)  # mechanically, here it is adjusted to 32 instead of 320
            self.tkimage3 = PhotoImage(file=resource_path("salvar_100.png"))
            
            self.bt_image_save = tk.Button(self.aba, image=self.tkimage3, compound=tk.LEFT, bd=0,
                                           bg='#A9A9A9', activebackground='#A9A9A9', command=self.save_report)
            
            self.bt_image_save.image = self.tkimage3  # reference to image not garbage collect
            self.bt_image_save.place(relx=0.01, rely=0.01, relwidth=0.03, relheight=0.04)
            self.bt_image_save.image = self.tkimage3  # reference to image not garbage collect
            #
            self.text_bt_image_save = 'save new report'
            
            self.create_tool_tip(self.bt_image_save, self.text_bt_image_save)
            
            # ---------------------
            
            # self.tkimage4 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\salvar_update_100.png")
            self.tkimage4 = PhotoImage(file=resource_path("salvar_update_100.png"))
            
            # self.tkimage3 = self.tkimage3.zoom(25)  # with 250, I ended up running out of memory
            # self.tkimage3 = self.tkimage3.subsample(20)  # mechanically, here it is adjusted to 32 instead of 320
            
            self.bt_image_update = tk.Button(self.aba, image=self.tkimage4, compound=tk.LEFT, bd=0,
                                             bg='#A9A9A9', activebackground='#A9A9A9', command=self.update_report)
            self.bt_image_update.image = self.tkimage4  # reference to image not garbage collect
            self.bt_image_update.place(relx=0.051, rely=0.01, relwidth=0.025, relheight=0.04)
            
            self.text_bt_image_update = 'Save Changes Before Closing'
            self.create_tool_tip(self.bt_image_update, self.text_bt_image_update)
            
            # --------------------- button create pdf start
            # self.tkimage5 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\main_pdf.png")
            self.tkimage5 = PhotoImage(file=resource_path("main_pdf.png"))
            # self.tkimage3 = self.tkimage3.zoom(25)  # with 250, I ended up running out of memory
            # self.tkimage3 = self.tkimage3.subsample(20)  # mechanically, here it is adjusted to 32 instead of 320
            
            self.bt_image_pdf = tk.Button(self.aba, image=self.tkimage5, compound=tk.LEFT, bd=0,
                                          bg='#A9A9A9', activebackground='#A9A9A9',
                                          command=self.create_main_body_report)
            self.bt_image_pdf.image = self.tkimage5  # reference to image not garbage collect
            self.bt_image_pdf.place(relx=0.087, rely=0.01, relwidth=0.023, relheight=0.04)
            
            self.text_bt_image_pdf = 'Create Report PDF and Save to Folder'
            self.create_tool_tip(self.bt_image_pdf, self.text_bt_image_pdf)
            
            # ---------------------  button create pdf end
            
            # # ---------------------  button clear al fields
            # self.tkimage7 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\del_all.png")
            self.tkimage7 = PhotoImage(file=resource_path("del_all.png"))
            
            self.bt_clear_fields = tk.Button(self.aba, image=self.tkimage7, compound=tk.LEFT, bd=0,
                                             bg='#A9A9A9', activebackground='#A9A9A9',
                                             command=self.clear_screen_funcs)
            self.bt_clear_fields.place(relx=0.125, rely=0.0098, relwidth=0.0237, relheight=0.04)
            self.bt_clear_fields.image = self.tkimage7  # reference to image not garbage collect
            
            self.text_bt_clear_fields = 'Delete all Fields'
            self.create_tool_tip(self.bt_clear_fields, self.text_bt_clear_fields)
            #
            # # ----------------------------------------------------
            #
            # self.tkimage8 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\story.png")
            self.tkimage8 = PhotoImage(file=resource_path("story.png"))
            
            self.bt_not_history = tk.Button(self.aba, image=self.tkimage8, compound=tk.LEFT, bd=0,
                                            bg='#A9A9A9', activebackground='#A9A9A9',
                                            command=self.clear_screen_but_history)
            
            self.bt_not_history.place(relx=0.165, rely=0.012, relwidth=0.0237, relheight=0.04)
            self.bt_not_history.image = self.tkimage8  # reference to image not garbage collect
            
            self.text_bt_clear_keep_story = 'Delete all Fields keep Clinical Story'
            self.create_tool_tip(self.bt_not_history, self.text_bt_clear_keep_story)
            #
            # ----------------------------------------------------
            
            # self.tkimage80 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\save_history_only.png")
            self.tkimage80 = PhotoImage(file=resource_path("save_history_only.png"))
            
            self.bt_save_history = tk.Button(self.aba, image=self.tkimage80, compound=tk.LEFT, bd=0,
                                             bg='#A9A9A9', activebackground='#A9A9A9',
                                             command=self.clear_screen_but_history)
            
            self.bt_save_history.place(relx=0.202, rely=0.012, relwidth=0.0237, relheight=0.04)
            self.bt_save_history.image = self.tkimage80  # reference to image not garbage collect
            
            self.text_bt_save_history = 'Save Clinical Story Text'
            self.create_tool_tip(self.bt_save_history, self.text_bt_save_history)
            
            # ----------------------------------------------------
            # self.tkimage81 = PhotoImage(file= delete_story_only.png")
            self.tkimage81 = PhotoImage(file=resource_path("delete_story_only.png"))
            self.bt_delete_history_only = tk.Button(self.aba, image=self.tkimage81, compound=tk.LEFT, bd=0,
                                                    bg='#A9A9A9', activebackground='#A9A9A9',
                                                    command=self.delete_history)
            self.bt_delete_history_only.place(relx=0.238, rely=0.0127, relwidth=0.0237, relheight=0.043)
            self.bt_delete_history_only.image = self.tkimage81  # reference to image not garbage collect
            
            self.text_bt_delete_history_only = 'Delete History Only'
            self.create_tool_tip(self.bt_delete_history_only, self.text_bt_delete_history_only)
            
            # ----------------------------------------------------
            
            # self.tkimage82 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\pdf_history.png")
            self.tkimage82 = PhotoImage(file=resource_path("pdf_history.png"))
            self.bt_pdf_history = tk.Button(self.aba, image=self.tkimage82, compound=tk.LEFT, bd=0,
                                            bg='#A9A9A9', activebackground='#A9A9A9',
                                            command=self.create_clinical_info_report)
            self.bt_pdf_history.place(relx=0.274, rely=0.0127, relwidth=0.0237, relheight=0.043)
            self.bt_pdf_history.image = self.tkimage82  # reference to image not garbage collect
            
            self.text_bt_pdf_history = 'Clinical History to PDF'
            self.create_tool_tip(self.bt_pdf_history, self.text_bt_pdf_history)
            
            # ----------------------------------------------------
            
            # self.tkimage9 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\delete_db_report.png")
            self.tkimage9 = PhotoImage(file=resource_path("delete_db_report.png"))
            self.bt_delete_report = tk.Button(self.aba, image=self.tkimage9, compound=tk.LEFT, bd=0,
                                              bg='#A9A9A9', activebackground='#A9A9A9', command=self.delete_report)
            self.bt_delete_report.place(relx=0.312, rely=0.0127, relwidth=0.0237, relheight=0.043)
            self.bt_delete_report.image = self.tkimage9  # reference to image not garbage collect
            
            self.text_bt_delete_report = 'Delete This Report'
            self.create_tool_tip(self.bt_delete_report, self.text_bt_delete_report)
            
            # -----------------------
            
            # self.tkimage11 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\duplicate.png")
            self.tkimage11 = PhotoImage(file=resource_path("duplicate.png"))
            self.bt_duplicate3 = tk.Button(self.aba3, image=self.tkimage11, compound=tk.LEFT, bd=0,
                                           bg='#A9A9A9', activebackground='#A9A9A9', command=self.duplicate_report)
            self.bt_duplicate3.place(relx=0.35, rely=0.0127, relwidth=0.0237, relheight=0.043)
            self.bt_duplicate3.image = self.tkimage11  # reference to image not garbage collect
            
            self.text_bt_duplicate3 = 'Duplicate Report'  # delete table =same as delete report
            self.create_tool_tip(self.bt_duplicate3, self.text_bt_duplicate3)
            
            # ----------------------------------------------------
            #     self.tkimage12 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\delete_this.png")
            self.tkimage12 = PhotoImage(file=resource_path("delete_this.png"))
            self.bt_del_this_one = tk.Button(self.aba3, image=self.tkimage12, compound=tk.LEFT, bd=0,
                                             bg='#A9A9A9', activebackground='#A9A9A9', command=self.delete_report)
            self.bt_del_this_one.place(relx=0.387, rely=0.0127, relwidth=0.0237, relheight=0.043)
            self.bt_del_this_one.image = self.tkimage12  # reference to image not garbage collect
            
            self.text_bt_del_this_one = 'Delete Report Selected'  # delete table =same as delete report
            self.create_tool_tip(self.bt_del_this_one, self.text_bt_del_this_one)
            
            # self.bt_delete_3  = ttk.Button(self.aba3, text='Delete One Selected', style= 'Bold.TButton',
            #                                command = self.delete_report)
            # self.bt_delete_3.place(relx=0.357, rely=0.01, relwidth=0.14, relheight=0.04)
            # ----------------------------------------------------
            #     self.tkimage13 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\delete_many.png")
            self.tkimage13 = PhotoImage(file=resource_path("delete_many.png"))
            self.bt_del_many = tk.Button(self.aba3, image=self.tkimage13, compound=tk.LEFT, bd=0,
                                         bg='#A9A9A9', activebackground='#A9A9A9', command=self.delete_many)
            self.bt_del_many.place(relx=0.424, rely=0.0127, relwidth=0.0237, relheight=0.043)
            self.bt_del_many.image = self.tkimage13  # reference to image not garbage collect
            
            self.text_bt_del_many = 'Delete Many - Ctrl-Lmouse'  # delete table =same as delete report
            self.create_tool_tip(self.bt_del_many, self.text_bt_del_many)
            
            # ---------------------------------------------------
            #     self.tkimage14 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\show_all_reports.png")
            self.tkimage14 = PhotoImage(file=resource_path("show_all_reports.png"))
            self.bt_show_all = tk.Button(self.aba3, image=self.tkimage14, compound=tk.LEFT, bd=0,
                                         bg='#A9A9A9', activebackground='#A9A9A9', command=self.select_lista)
            self.bt_show_all.place(relx=0.465, rely=0.0127, relwidth=0.0237, relheight=0.043)
            self.bt_show_all.image = self.tkimage14  # reference to image not garbage collect
            
            self.text_bt_show_all = 'Show All Reports'  # delete table =same as delete report
            self.create_tool_tip(self.bt_show_all, self.text_bt_show_all)
            
            # ----------------------------------------------------
            #     delete evething from table
            
            # self.tkimage10 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\drop_table.png")
            self.tkimage10 = PhotoImage(file=resource_path("drop_table.png"))
            self.bt_delete_table = tk.Button(self.aba3, image=self.tkimage10, compound=tk.LEFT, bd=0,
                                             bg='#A9A9A9', activebackground='#A9A9A9', command=self.drop_table_all)
            self.bt_delete_table.place(relx=0.65, rely=0.0127, relwidth=0.0237, relheight=0.043)
            self.bt_delete_table.image = self.tkimage10  # reference to image not garbage collect
            
            self.text_bt_delete_table = "Delete All Reports"  # 'Drop Table'     #delete table =same as delete report
            self.create_tool_tip(self.bt_delete_table, self.text_bt_delete_table)
            
            self.translate_tool_tip()
        # ----------------------------------------------------
        # ----------------------------------------------------
    
    def aba4_translation(self):
        
        if self.json_port_eng_radiob34_aba4_var == 1:
            self.text_l1Cvas2aba4.set("Configure Options and PDF.")
            self.lframe1_aba4.config(text="Page size")
            self.radiobutton1.config(text="Letter")
            self.radiobutton2.config(text="A4")
            self.lframe2_aba4.config(text='Switch Language')
            self.lframe3_aba4.config(text='Show PDF after creation?')
            self.radiobutton5.config(text="Show PDF File")
            self.radiobutton6.config(text="Don't Show PDF.")
            self.lframe4_aba4.config(text='Show Header Table?')
            self.radiobutton7.config(text="Show Table                  ")
            self.radiobutton8.config(text="Dismiss Header Table")
            self.lframe5_aba4.config(text='Select Main Title')
            self.radiobutton9.config(text="Use Electroencephalogram")
            self.radiobutton0.config(text="Create Another Title            ")
            self.pdf_titlenamelabel.config(text="or you can write a new\nmainTitle and just "
                                                "after\nthat... check button\nEnd Config.")
            self.lframe6_aba4.config(text='Select Font')
            self.pdf_combo1label.config(text="For default font \n Helvetica click End Config.")
            self.radiob1_cbox_aba4.config(text="Default font.")
            self.radiob2_cbox_aba4.config(text="Selected font.")
            self.pdf_combo2label.config(text="or First select a font and\nafter that check button\nEnd Config.")
            
            self.lframe7_aba4.config(text='End Config')
            self.lframe7_label.config(text="Click bellow\nto confirm changes.")
            self.lframe7_button.config(text='Do It!')
        
        elif self.json_port_eng_radiob34_aba4_var == 2:
            self.text_l1Cvas2aba4.set("Configure Opções e PDF.")
            self.lframe1_aba4.config(text="Tamanho da Página")
            self.radiobutton1.config(text="Carta   ")
            self.radiobutton2.config(text="A quatro")
            self.lframe2_aba4.config(text="Mudar Idioma")
            self.lframe3_aba4.config(text='Mostrar PDF após criado?')
            self.radiobutton5.config(text='Mostrar PDF?')
            self.radiobutton6.config(text="Não, depois vejo.")
            self.lframe4_aba4.config(text='Mostrar Tabela Superior?')
            self.radiobutton7.config(text="Mostrar Tabela ")
            self.radiobutton8.config(text="Esconder Table")
            self.lframe5_aba4.config(text='Selecionar Título')
            self.radiobutton9.config(text="Use Eletrencefalograma")
            self.radiobutton0.config(text="Crie Outro Título            ")
            self.pdf_titlenamelabel.config(text="ou você escreve um novo\n Título e "
                                                "apenas após...\n clique no botão\nFeito.")
            self.lframe6_aba4.config(text='Selecione Fonte')
            self.pdf_combo1label.config(text="Para usar fonte padrão\n Helvetica click Feito.")
            self.radiob1_cbox_aba4.config(text="Fonte padrão.")
            self.radiob2_cbox_aba4.config(text="Use fonte escolhida.")
            self.pdf_combo2label.config(text="ou selecione uma fonte e\n click Feito.")
            self.lframe7_aba4.config(text='Feito.')
            self.lframe7_label.config(text="Click abaixo para\nconfirmar mudanças.")
            self.lframe7_button.config(text='Confirme alterações!')
    
    @staticmethod
    def take_text_from_report(textwidget, my_tag):
        """
        method used in buttons like "self.bt_text_italics", when click on this button,
        we select a part of a string inside a Text.widget, for example "HEADER"
        with "selexion = textwidget.get(tk.SEL_FIRST, tk.SEL_LAST)"
        
        then if there is a html tab in the selected string, we remove it, if not we insert it
        to insert or remove tag to italics or bold or etc.
        
        strip() removes the spaces left when removing for example " <i>" + selexion + "</i> "
        
        same for subscript/ superscript/ underline/ bold /italics
        
        my_tag can be
        # <b> ... </b> - bold
        # <i> ... </i> - italics ---> "i>"
        # <u> ... </u> - underline
        # <super> ... </super> - superscript
        # <sub> ... </sub> - subscript
        
        atention: to use those tags reportlab must use "Paragraph" in text and/or tables
        """
        
        # ranges = textwidget.tag_ranges(tk.SEL)
        # if ranges:
        #     print('SELECTED Text is %r' % textwidget.get(*ranges))
        # else:
        #     print('NO Selected Text')
        clean = ''
        try:
            selexion = textwidget.get(tk.SEL_FIRST, tk.SEL_LAST)  # get original string
            rpl = selexion
            # if selexion:
            #     # selexion = textwidget.get(tk.SEL_FIRST,tk.SEL_LAST) # get original string
            #     rpl = " <i>" + selexion + "</i> " # costruct new string
            #     # rpl = " <p>" + ranges + "</p> " # costruct new string
            #     textwidget.insert(tk.INSERT,rpl) # insert new string
            #     textwidget.delete(tk.SEL_FIRST, tk.SEL_LAST) # delete old string
            #     return
            # else:
            #     return
            # rpl = ''
            # if selexion:
            
            # if "i>" in selexion:  # "i>" por example is my_tag
            if my_tag in selexion:
                # selexion = textwidget.get(tk.SEL_FIRST,tk.SEL_LAST) # get original string
                # Remove html tags from a string
                # clean = re.compile('<.*?>')
                
                if my_tag == "b>":
                    # clean = re.compile('<.i?>')
                    clean = re.compile(r'<b>|</b>')
                if my_tag == "i>":
                    # clean = re.compile('<.i?>')
                    clean = re.compile(r'<i>|</i>')  # if find, remove <i> and </i>
                elif my_tag == "u>":
                    # clean = re.compile('<.u?>')
                    clean = re.compile(r'<u>|</u>')
                elif my_tag == "super>":
                    # clean = re.compile('<.u?>')
                    clean = re.compile(r'<super>|</super>')
                elif my_tag == "sub>":
                    # clean = re.compile('<.u?>')
                    clean = re.compile(r'<sub>|</sub>')
                
                selexion = re.sub(clean, '', selexion).strip()
                rpl = selexion  # costruct new string
                # rpl = " <p>" + ranges + "</p> " # costruct new string
                textwidget.insert(tk.INSERT, rpl)  # insert new string
                textwidget.delete(tk.SEL_FIRST, tk.SEL_LAST)  # delete old string
                return
            
            else:
                if my_tag == "b>":
                    rpl = "<b>" + selexion + "</b>"  # costruct new string
                if my_tag == "i>":
                    rpl = "<i>" + selexion + "</i>"  # costruct new string
                # rpl = " <p>" + ranges + "</p> " # costruct new string
                elif my_tag == "u>":
                    rpl = "<u>" + selexion + "</u>"
                elif my_tag == "super>":
                    rpl = "<super>" + selexion + "</super>"
                elif my_tag == "sub>":
                    rpl = "<sub>" + selexion + "</sub>"
                
                textwidget.insert(tk.INSERT, rpl)  # insert new string
                textwidget.delete(tk.SEL_FIRST, tk.SEL_LAST)  # delete old string
                return
        
        except tk.TclError:
            return
        
        # textwidget.tag_configure("boldtext",font=textwidget.cget("font")+" bold")
        # textwidget.tag_configure(ranges)
        # textwidget.tag_add("boldtext","sel.first","sel.last")
        # # textwidget.configure(command=change_bold)
        # textwidget.tag_config("bt", font=("Georgia", "12", "bold"))
        # textwidget.tag_add("bt", "sel.first", "sel.last")
    
    def root_widgets(self):
        """
        func notebooks and their widgets , frames , etc
        """
        self.abas = ttk.Notebook(self.root)
        self.abas.enable_traversal()  # allow cntrl-tab or cntrl-shift-tab to change tab
        self.aba1 = tk.Frame(self.abas, highlightthickness=0)
        self.aba2 = tk.Frame(self.abas, highlightthickness=0)
        self.aba3 = tk.Frame(self.abas, highlightthickness=0)
        self.aba4 = tk.Frame(self.abas, highlightthickness=0)
        
        # -------------------------
        self.retrieve_portg_or_eng_radiob34_aba4_json()
        # returns self.json_port_eng_radiob34_aba4_var --> 1 or 2
        # debug
        # self.aba1.configure(background= '#708090')
        self.aba1.configure(background='#A9A9A9')
        # self.aba1.configure(background= '#343434')
        # self.aba1.configure(background= '#28282B')
        self.aba2.configure(background='#A9A9A9')
        self.aba3.configure(background='#A9A9A9')
        self.aba4.configure(background='#A9A9A9')
        
        self.abas.add(self.aba1, text="Edit Report and create PDF", underline=0)
        self.abas.add(self.aba2, text="Add Clinical History", underline=0)
        self.abas.add(self.aba3, text="Report List", underline=0)
        self.abas.add(self.aba4, text="Configure", underline=0)
        # underline gets the n caracter 0= E  A  R or C and Alt-e goes to first tab etc
        self.abas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        boldStyle = ttk.Style(self.aba1)
        boldStyle.theme_use('clam')
        # boldStyle.theme_use('default')
        # boldStyle.theme_use('classic')
        boldStyle.configure("Bold.TButton", font=('Sans', '10', 'bold'))  # '#A9A9A9'
        boldStyle.configure("Bold.TButton", background='#A9A9A9', font=('Helvetica', '10', 'bold'), relief='flat')
        # boldStyle.configure('TNotebook.Tab', background="Red")
        
        # -----------------widgets aba1 and aba3 --------------- start
        
        # ----------------search patient widgets--------------start
        # just a black canvas around  self bt_search  and entry3
        self.canvas = Canvas(self.aba3, highlightthickness=1, highlightbackground="black", bg='#A9A9A9')
        self.canvas.place(relx=0.01, rely=0.06, relwidth=0.31, relheight=0.05)
        
        self.bt_search3 = ttk.Button(self.aba3, text="Search Patient's name:", style='Bold.TButton',
                                     command=self.search_report)
        self.bt_search3.place(relx=0.016, rely=0.065, relwidth=0.13, relheight=0.04)
        
        self.search_patient_entry3 = ttk.Entry(self.aba3, style='style.TEntry', font='sans 10 bold')
        self.search_patient_entry3.place(relx=0.155, rely=0.07, relwidth=0.16, relheight=0.03)
        
        # connect  self.search_patient_entry3 with ENTER to execute self.search_report:
        self.search_patient_entry3.bind('<Return>', self.search_report)
        
        # ----------------search patient--------------end
        
        # self.bt_show_all_aba3  = ttk.Button(self.aba3, text= "Show all Reports", style= 'Bold.TButton',
        #                              command =self.select_lista)
        # self.bt_show_all_aba3.place(relx=0.77, rely=0.01, relwidth=0.12, relheight=0.04)
        
        # ---------------------delete logo and signature
        self.bt_delete_logo_aba3 = ttk.Button(self.aba3, text="Delete Logo", style='Bold.TButton',
                                              command=self.delete_logo)
        self.bt_delete_logo_aba3.place(relx=0.513, rely=0.065, relwidth=0.08, relheight=0.04)
        
        self.bt_delete_signature_aba3 = ttk.Button(self.aba3, text="Delete Signature", style='Bold.TButton',
                                                   command=self.delete_signature)
        self.bt_delete_signature_aba3.place(relx=0.60, rely=0.065, relwidth=0.11, relheight=0.04)
        # ---------------------
        
        self.bt_add_record = ttk.Button(self.aba1, text='Save New', style='Bold.TButton',
                                        command=self.save_report)
        self.bt_add_record.place(relx=0.345, rely=0.01, relwidth=0.07, relheight=0.04)
        # self.bt_add_record3  = ttk.Button(self.aba3, text='Save New', style= 'Bold.TButton',
        #                            command = self.save_report)
        # self.bt_add_record3.place(relx=0.105, rely=0.01, relwidth=0.07, relheight=0.04)
        
        self.bt_save_update_aba1 = ttk.Button(self.aba1, text='Save Update', style='Bold.TButton',
                                              command=self.update_report)
        self.bt_save_update_aba1.place(relx=0.417, rely=0.01, relwidth=0.09, relheight=0.04)
        
        # ------delete report
        
        self.bt_delete_1 = ttk.Button(self.aba1, text='Delete This Report', style='Bold.TButton',
                                      command=self.delete_report)
        self.bt_delete_1.place(relx=0.51, rely=0.01, relwidth=0.12, relheight=0.04)
        
        # self.bt_delete_3  = ttk.Button(self.aba3, text='Delete One Selected', style= 'Bold.TButton',
        #                                command = self.delete_report)
        # self.bt_delete_3.place(relx=0.357, rely=0.01, relwidth=0.14, relheight=0.04)
        
        # ------------------------------buttons up down
        
        self.bt_ascending3 = tk.Button(self.aba3, image=self.tkimage1, compound=tk.LEFT, bd=0,
                                       bg='#A9A9A9', activebackground='#A9A9A9', command=self.ascending)
        self.bt_ascending3.image = self.tkimage1  # reference to image not garbage collect
        self.bt_ascending3.place(relx=0.71, rely=0.015, relwidth=0.017, relheight=0.035)
        
        text_bt_ascending3 = 'List Ascending'
        self.create_tool_tip(self.bt_ascending3, text_bt_ascending3)
        
        # get self.tkimage2 from "def icon_images(self)" in class functions:
        self.bt_movedown3 = tk.Button(self.aba3, image=self.tkimage2, compound=tk.LEFT, bd=0,
                                      bg='#A9A9A9', activebackground='#A9A9A9', command=self.descending)
        self.bt_movedown3.image = self.tkimage2
        self.bt_movedown3.place(relx=0.74, rely=0.015, relwidth=0.017, relheight=0.035)
        text_bt_movedown3 = 'List Descending'
        self.create_tool_tip(self.bt_movedown3, text_bt_movedown3)
        # ------------------------------
        
        self.bt_get_logo_aba1 = ttk.Button(self.aba1, text='Get Logo', style='Bold.TButton',
                                           command=self.collect_image_logo)
        self.bt_get_logo_aba1.place(relx=0.634, rely=0.01, relwidth=0.06, relheight=0.04)
        self.bt_get_logo_aba3 = ttk.Button(self.aba3, text='Get Logo', style='Bold.TButton',
                                           command=self.collect_image_logo)
        self.bt_get_logo_aba3.place(relx=0.32, rely=0.065, relwidth=0.09, relheight=0.04)
        
        self.bt_get_signature_aba1 = ttk.Button(self.aba1, text='Get Signature', style='Bold.TButton',
                                                command=self.collect_image_footer)
        self.bt_get_signature_aba1.place(relx=0.71, rely=0.01, relwidth=0.09, relheight=0.04)
        self.bt_get_signature_aba3 = ttk.Button(self.aba3, text='Get Signature', style='Bold.TButton',
                                                command=self.collect_image_footer)
        self.bt_get_signature_aba3.place(relx=0.41, rely=0.065, relwidth=0.1, relheight=0.04)
        
        # --------------icons bold and normal  aba1        # self.icon_images()    comes here
        
        self.bt_Report3 = ttk.Button(self.aba3, text='Data Bases', style='Bold.TButton',
                                     command=self.multiple_sqlite_window_modal)
        self.bt_Report3.place(relx=0.80, rely=0.01, relwidth=0.1, relheight=0.04)
        
        # self.label = tk.Label(self.aba3)
        # self.label.place(relx=0.7, rely=0.01, relwidth=0.10, relheight=0.04)
        
        # --------------------------------------------------------
        combostyle = ttk.Style()
        # debug:
        # combostyle.theme_create('combostyle', parent='alt',
        #                         settings={'TCombobox':
        #                                       {'configure':
        #                                            {'selectbackground': 'blue',
        #                                             'fieldbackground': 'red',
        #                                             'background': 'green'
        #                                             }}}
        #                         )
        # # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        # combostyle.theme_use('combostyle')
        
        # self.aba3.option_add("*TCombobox*Listbox*Background", 'green')
        
        # combostyle = ttk.Style()
        # combostyle.theme_create('combostyle', parent='alt', settings={'TCombobox': {'configure':
        #                                                                                 {'fieldbackground': '#ffff99',
        #                                                                                  'background': '#ffcc66'}}})
        # combostyle.theme_use('combostyle')
        #
        
        # combostyle = ttk.Style()
        combostyle.configure('ARD.TCombobox', foreground='#708090', background='#708090',
                             insertbackground='#708090',
                             fieldbackground='#708090')  # background="#ffcc66", fieldbackground="#ffff99")
        
        self.db_path_aba3 = tk.StringVar()
        self.db_path_aba3_cbox = ttk.Combobox(self.aba3, style='ARD.TCombobox',
                                              textvariable=self.db_path_aba3,
                                              state='readonly')
        # postcommand = self.retrieve_updated_list_db_cbox)
        
        if Pages.EEG_report_databanks_list == '':
            self.db_path_cbox = []
        
        else:
            self.db_path_cbox = Pages.EEG_report_databanks_list
        
        self.db_path_aba3_cbox.config(values=self.db_path_cbox)  # list that appears in combobox
        
        # self.db_path_aba3_cbox.bind("<<ComboboxSelected>>",  lambda _ : print("labda",self.db_path_aba3))
        self.db_path_aba3_cbox.bind("<<ComboboxSelected>>", self.bind_db_path_aba3_cbox)
        # self.db_path_aba3_cbox.bind("<<ComboboxSelected>>", self.store_db_to_json)
        self.db_path_aba3_cbox.place(relx=0.72, rely=0.065, relwidth=0.21, relheight=0.04)
        
        # #this gets the value of combobox chosen in previous session and stored in current_db_used.json.old
        # #populate combobox, it means, the databank in use
        # with open('current_db_used.json.old') as file_object_db:
        #     current_db = json.load(file_object_db)
        self.retrieve_db_cbox()
        self.db_path_aba3_cbox.set(self.current_db)
        
        # ----------------------------change font---------------------start aba1
        
        all_commands_bold = lambda: [self.take_text_from_report(self.txt_header, "b>"),
                                     self.take_text_from_report(self.txt_body, "b>"),
                                     self.take_text_from_report(self.txt_footer, "b>"),
                                     self.take_text_from_report(self.txt_history1, "b>"),
                                     self.take_text_from_report(self.txt_history, "b>")]
        
        all_commands_italic = lambda: [self.take_text_from_report(self.txt_header, "i>"),
                                       self.take_text_from_report(self.txt_body, "i>"),
                                       self.take_text_from_report(self.txt_footer, "i>"),
                                       self.take_text_from_report(self.txt_history1, "i>"),
                                       self.take_text_from_report(self.txt_history, "i>")]
        
        all_commands_underline = lambda: [self.take_text_from_report(self.txt_header, "u>"),
                                          self.take_text_from_report(self.txt_body, "u>"),
                                          self.take_text_from_report(self.txt_footer, "u>"),
                                          self.take_text_from_report(self.txt_history1, "u>"),
                                          self.take_text_from_report(self.txt_history, "u>")]
        
        all_commands_super = lambda: [self.take_text_from_report(self.txt_header, "super>"),
                                      self.take_text_from_report(self.txt_body, "super>"),
                                      self.take_text_from_report(self.txt_footer, "super>"),
                                      self.take_text_from_report(self.txt_history1, "super>"),
                                      self.take_text_from_report(self.txt_history, "super>")]
        
        all_commands_sub = lambda: [self.take_text_from_report(self.txt_header, "sub>"),
                                    self.take_text_from_report(self.txt_body, "sub>"),
                                    self.take_text_from_report(self.txt_footer, "sub>"),
                                    self.take_text_from_report(self.txt_history1, "sub>"),
                                    self.take_text_from_report(self.txt_history, "sub>")]
        
        # self.tkimage4a = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\help.png")
        # < a
        # href = "https://www.flaticon.com/free-icons/bold-text"
        # title = "bold text icons" > Bold text icons created by surang - Flaticon < / a >
        
        abas_1_e_2 = [self.aba1, self.aba2]
        for aba in abas_1_e_2:
            self.tkimage4a = PhotoImage(file=resource_path("bold.png"))
            
            self.bt_text_bold = tk.Button(self.aba, image=self.tkimage4a, compound=tk.LEFT, bd=0,
                                          bg='#A9A9A9', activebackground='#A9A9A9', command=all_commands_bold)
            # lambda: self.take_text_from_report(textwidgets, "b>"))
            self.bt_text_bold.image = self.tkimage4a  # reference to image not garbage collect
            self.bt_text_bold.place(relx=0.9, rely=0.0425, relwidth=0.03, relheight=0.04)
            
            text = 'Bold'
            self.create_tool_tip(self.bt_text_bold, text)
            
            # self.tkimage4b = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\help.png")
            # < a
            # href = "https://www.flaticon.com/free-icons/italic"
            # title = "italic icons" > Italic icons created by surang - Flaticon < / a >
            
            # -------------------------------------------------------------------
            
            self.tkimage4b = PhotoImage(file=resource_path("italic.png"))
            
            self.bt_text_italics = tk.Button(self.aba, image=self.tkimage4b, compound=tk.LEFT, bd=0,
                                             bg='#A9A9A9', activebackground='#A9A9A9', command=all_commands_italic)
            
            # bg='#A9A9A9', activebackground='#A9A9A9', command=self.help_html)
            self.bt_text_italics.image = self.tkimage4b  # reference to image not garbage collect
            self.bt_text_italics.place(relx=0.875, rely=0.0425, relwidth=0.03, relheight=0.04)
            
            text = 'italics'
            self.create_tool_tip(self.bt_text_italics, text)
            
            # < a
            # href = "https://www.flaticon.com/free-icons/numbers"
            # title = "numbers icons" > Numbers
            # icons created by Md Tanvirul Haque - Flaticon < / a >
            
            # -------------------------------------------------------------------
            
            self.tkimage4c = PhotoImage(file=resource_path("underline.png"))
            
            self.bt_text_underline = tk.Button(self.aba, image=self.tkimage4c, compound=tk.LEFT, bd=0,
                                               bg='#A9A9A9', activebackground='#A9A9A9', command=all_commands_underline)
            # lambda: self.take_text_from_report(self.txt_header, "u>"))
            self.bt_text_underline.image = self.tkimage4c  # reference to image not garbage collect
            self.bt_text_underline.place(relx=0.85, rely=0.0425, relwidth=0.03, relheight=0.04)
            
            text = 'underline'
            self.create_tool_tip(self.bt_text_underline, text)
            
            # -------------------------------------------------------------------
            
            self.tkimage4d = PhotoImage(file=resource_path("superscript.png"))
            
            self.bt_text_superscript = tk.Button(self.aba, image=self.tkimage4d, compound=tk.LEFT, bd=0,
                                                 bg='#A9A9A9', activebackground='#A9A9A9', command=all_commands_super)
            # lambda: self.take_text_from_report(self.txt_header, "super>"))
            # bg='#A9A9A9', activebackground='#A9A9A9', command=self.help_html)
            self.bt_text_superscript.image = self.tkimage4d  # reference to image not garbage collect
            self.bt_text_superscript.place(relx=0.825, rely=0.0425, relwidth=0.03, relheight=0.04)
            
            text = 'superscript'
            self.create_tool_tip(self.bt_text_superscript, text)
            
            # -------------------------------------------------------------------
            
            self.tkimage4e = PhotoImage(file=resource_path("subscript.png"))
            
            self.bt_text_subscript = tk.Button(self.aba, image=self.tkimage4e, compound=tk.LEFT, bd=0,
                                               bg='#A9A9A9', activebackground='#A9A9A9', command=all_commands_sub)
            # lambda: self.take_text_from_report(self.txt_header, "sub>"))
            self.bt_text_subscript.image = self.tkimage4e  # reference to image not garbage collect
            self.bt_text_subscript.place(relx=0.80, rely=0.0425, relwidth=0.03, relheight=0.04)
            
            text = 'subscript'
            self.create_tool_tip(self.bt_text_subscript, text)
        
        # -----------------close program aba1
        
        # self.tkimage5a = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\help.png")
        self.tkimage5a = PhotoImage(file=resource_path("help.png"))
        
        self.bt_image_help = tk.Button(self.aba1, image=self.tkimage5a, compound=tk.LEFT, bd=0,
                                       bg='#A9A9A9', activebackground='#A9A9A9', command=self.help_html)
        self.bt_image_help.image = self.tkimage5a  # reference to image not garbage collect
        self.bt_image_help.place(relx=0.925, rely=0.01, relwidth=0.03, relheight=0.04)
        
        text = 'Help me'
        self.create_tool_tip(self.bt_image_help, text)
        
        # -------------------
        
        self.bt_image_help = tk.Button(self.aba2, image=self.tkimage5a, compound=tk.LEFT, bd=0,
                                       bg='#A9A9A9', activebackground='#A9A9A9', command=self.help_html)
        self.bt_image_help.image = self.tkimage5a  # reference to image not garbage collect
        self.bt_image_help.place(relx=0.925, rely=0.01, relwidth=0.03, relheight=0.04)
        
        text = 'Help me'
        self.create_tool_tip(self.bt_image_help, text)
        
        # -------------------
        
        self.bt_image_help = tk.Button(self.aba3, image=self.tkimage5a, compound=tk.LEFT, bd=0,
                                       bg='#A9A9A9', activebackground='#A9A9A9', command=self.help_html)
        self.bt_image_help.image = self.tkimage5a  # reference to image not garbage collect
        self.bt_image_help.place(relx=0.925, rely=0.01, relwidth=0.03, relheight=0.04)
        
        text = 'Help me'
        self.create_tool_tip(self.bt_image_help, text)
        
        # self.tkimage6 = PhotoImage(file=r"G:\PycharmProjects\EEG_WEAVER\images\stop.png")
        self.tkimage6 = PhotoImage(file=resource_path("stop.png"))
        # self.tkimage3 = self.tkimage3.zoom(25)  # with 250, I ended up running out of memory
        # self.tkimage3 = self.tkimage3.subsample(20)  # mechanically, here it is adjusted to 32 instead of 320
        
        self.bt_image_stop = tk.Button(self.aba1, image=self.tkimage6, compound=tk.LEFT, bd=0,
                                       bg='#A9A9A9', activebackground='#A9A9A9', command=self.quit_weaver_reporter)
        self.bt_image_stop.image = self.tkimage6  # reference to image not garbage collect
        self.bt_image_stop.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.04)
        
        text = 'Bye bye!!!'
        self.create_tool_tip(self.bt_image_stop, text)
        
        # ---------------------close program aba2
        
        self.bt_image_stop_ab2 = tk.Button(self.aba2, image=self.tkimage6, compound=tk.LEFT, bd=0,
                                           bg='#A9A9A9', activebackground='#A9A9A9', command=self.quit_weaver_reporter)
        self.bt_image_stop_ab2.image = self.tkimage6  # reference to image not garbage collect
        self.bt_image_stop_ab2.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.04)
        
        text = 'Bye bye!!!'
        self.create_tool_tip(self.bt_image_stop_ab2, text)
        
        # ---------------------close program aba3
        
        self.bt_image_stop_ab3 = tk.Button(self.aba3, image=self.tkimage6, compound=tk.LEFT, bd=0,
                                           bg='#A9A9A9', activebackground='#A9A9A9', command=self.quit_weaver_reporter)
        self.bt_image_stop_ab3.image = self.tkimage6  # reference to image not garbage collect
        self.bt_image_stop_ab3.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.04)
        
        text = 'Bye bye!!!'
        self.create_tool_tip(self.bt_image_stop_ab3, text)
        
        # ---------------------close program aba4
        
        # ----------------labels and entries in aba1 aba3---------
        labelStyle = ttk.Style(self.aba1)
        labelStyle = ttk.Style(self.aba3)
        labelStyle.theme_use('clam')
        # boldStyle.configure("Bold.TButton", font=('Sans', '10', 'bold'))
        labelStyle.configure("Bold.Label", font=('Helvetica', '10', 'bold'),
                             relief='flat', background='#A9A9A9')
        
        entry_Style = ttk.Style(self.aba1)
        entry_Style = ttk.Style(self.aba3)
        entry_Style.theme_use('clam')
        entry_Style.configure('style.TEntry', fieldbackground='#4E6172',
                              foreground="white")
        
        # Define the style for combobox widget
        combobox_Style = ttk.Style()
        combobox_Style.theme_use('clam')
        # style.configure("TCombobox", fieldbackground="orange", background="white")
        
        combobox_Style.configure('TCombobox', fieldbackground='#4E6172',
                                 foreground="white")
        
        self.Id_label = ttk.Label(self.aba1, text='Id:', style="Bold.Label")
        self.Id_label.place(relx=0.01, rely=0.06)
        
        self.Id_entry = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')
        self.Id_entry.config(state="disable", foreground='white')
        # the user do not insert a value, but must enable to get code from treeview
        
        self.Id_entry.place(relx=0.03, rely=0.06, relwidth=0.04)
        
        self.patient_label_aba1 = ttk.Label(self.aba1, text='Patient:', style="Bold.Label")
        self.patient_label_aba1.place(relx=0.08, rely=0.06, relwidth=0.05)
        self.patient_entry = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')
        self.patient_entry.place(relx=0.125, rely=0.06, relwidth=0.16)
        
        # self.search_patient_entry3 = ttk.Entry(self.aba3, style ='style.TEntry', font='sans 10 bold')
        # self.search_patient_entry3.place(relx=0.145, rely=0.07, relwidth=0.16)
        
        self.gender_label = ttk.Label(self.aba1, text='Gender:', style="Bold.Label")
        self.gender_label.place(relx=0.295, rely=0.06, relwidth=0.05)
        
        self.sex_chosen = ''
        if self.json_port_eng_radiob34_aba4_var == 1:
            self.sex_chosen = ["Male", "Female"]
        
        elif self.json_port_eng_radiob34_aba4_var == 2:
            self.sex_chosen = ["Masc.", "Femin."]
        
        self.comboGender = ttk.Combobox(self.aba1, values=self.sex_chosen)
        self.comboGender.set("Sex")
        self.comboGender.place(relx=0.34, rely=0.06, relwidth=0.045)
        
        self.age_label = ttk.Label(self.aba1, text='Age:', style="Bold.Label")
        self.age_label.place(relx=0.398, rely=0.06, relwidth=0.03)
        self.age_entry = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')
        self.age_entry.place(relx=0.427, rely=0.06, relwidth=0.025)
        Pages.report_age = self.age_entry.get()
        # print('Pages.report_age', Pages.report_age)
        
        self.diag_label = ttk.Label(self.aba1, text='Diagnosis:', style="Bold.Label")
        self.diag_label.place(relx=0.458, rely=0.06, relwidth=0.07)
        self.diag_entry = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')
        self.diag_entry.place(relx=0.515, rely=0.06, relwidth=0.1)
        
        self.LFF_label = ttk.Label(self.aba1, text='LFF:', style="Bold.Label")
        self.LFF_label.place(relx=0.625, rely=0.06, relwidth=0.03)
        self.LFF_entry = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')  # ,
        # validate = 'key', validatecommand = vcmd)
        self.LFF_entry.place(relx=0.65, rely=0.06, relwidth=0.03)
        
        self.HFF_label = ttk.Label(self.aba1, text='HFF:', style="Bold.Label")
        self.HFF_label.place(relx=0.688, rely=0.06, relwidth=0.03)
        self.HFF_entry = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')  # ,
        # validate = 'key', validatecommand = vcmd)
        self.HFF_entry.place(relx=0.715, rely=0.06, relwidth=0.02)
        
        self.srate_label = ttk.Label(self.aba1, text='Sampling Rate:', style="Bold.Label")
        self.srate_label.place(relx=0.745, rely=0.06, relwidth=0.16)
        self.srate_entry = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')  # ,
        # validate = 'key', validatecommand = vcmd)
        self.srate_entry.place(relx=0.816, rely=0.06, relwidth=0.03)
        
        self.report_Date_label = ttk.Label(self.aba1, text='Report Date:', style="Bold.Label")
        self.report_Date_label.place(relx=0.855, rely=0.06, relwidth=0.16)
        self.report_Date_entry = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')
        self.report_Date_entry.place(relx=0.93, rely=0.06, relwidth=0.056)
        
        # --------------get date for today
        now = datetime.now()
        
        self.json_port_eng_radiob34_aba4_var = self.retrieve_portg_or_eng_radiob34_aba4_json()
        # try:
        if self.json_port_eng_radiob34_aba4_var == 1:
            self.report_date = (now.strftime("%m-%d-%Y"))
        elif self.json_port_eng_radiob34_aba4_var == 2:
            self.report_date = (now.strftime("%d-%m-%Y"))  # report_date(now.strftime("%d-%m-%y %H:%M:%S"))    #
        # except FileNotFoundError:
        #     self.report_date = (now.strftime("%m-%d-%Y"))
        
        self.report_Date_entry.insert(END, self.report_date)  #
        
        # -------------------- frames in aba1------------------------start
        
        self.frame_header = tk.Frame(self.aba1, bd=2, bg='#C0C0C0',
                                     highlightbackground='#36454F',
                                     highlightthickness=1)
        
        # debug:
        # relx rely =place relatively
        # relx 0 a 1  esquerda direta da tela
        # relx = 01 means 10% from left
        # relwidth 98% of the width of frame
        # relheight = is the up downsize
        self.frame_header.place(relx=0.003, rely=0.10, relwidth=0.995,
                                relheight=0.13)
        
        # --------------------------------
        self.frame_body = tk.Frame(self.aba1, bd=2, bg='#C0C0C0',
                                   highlightbackground='#36454F',
                                   highlightthickness=1)
        
        self.frame_body.place(relx=0.003, rely=0.230, relwidth=0.995,
                              relheight=0.54)
        
        # --------------------------------
        self.frame_footer = tk.Frame(self.aba1, bd=2, bg='#C0C0C0',
                                     highlightbackground='#36454F',
                                     highlightthickness=1)
        self.frame_footer.place(relx=0.003, rely=0.77, relwidth=0.995,
                                relheight=0.15)
        #
        
        # footer image should be here, but we get it from askopen.etc
        
        # --------------------  aba4 configure-----------------------end
        # just a black canvas around  self bt_search  and entry3
        self.canvas1_aba4 = Canvas(self.aba4, highlightthickness=1, highlightbackground='#343434', bg='#A9A9A9')
        self.canvas1_aba4.place(relx=0.003, rely=0.01, relwidth=0.995, relheight=0.985)
        
        # self.canvas2_aba4 = Canvas(self.aba4, highlightthickness=1, highlightbackground='#36454F', bg='#A9A9A9')
        # self.canvas2_aba4.place(relx=0.04, rely=0.06, relwidth=0.925, relheight=0.12)
        
        self.config_label_style()
        
        # style = ttk.Style()
        # style.configure("Custom.TLabel",foreground="#DCDCDC",
        # # style.configure("Custom.TLabel",foreground="#708090",
        #                                 background='#36454F',
        #                                 # background='#000000',
        #                                 padding=[10, 10, 10, 10],
        #                                 relief = "groove",
        #                                 # relief = "solid",
        #                                 # font="Times 30 bold italic",
        #                                 # font="Arial 30 Black",
        #                                 # width=18,
        #                                 anchor=tk.CENTER,
        #                                 highlightbackground="black",
        #                                 bordercolor= '#36454F',
        #                                 borderwidth='1')
        
        # --------------------------------------------self.lframe1_aba4
        self.text_l1Cvas2aba4 = tk.StringVar()
        
        self.text_l1Cvas2aba4.set("Configure Options and PDF.")
        
        self.label_1_canvas2_aba4 = ttk.Label(self.canvas1_aba4,
                                              textvariable=self.text_l1Cvas2aba4,
                                              style="Custom.TLabel",
                                              # background='#DCDCDC',
                                              # borderwidth='10',
                                              # relief=tk.GROOVE,
                                              # relief=tk.RAISED,
                                              # padding=25,
                                              font="Helvetica 20 bold",
                                              # font="Arial 30 bold",
                                              # foreground="#708090",
                                              # underline=4,
                                              # width=18,
                                              # anchor=tk.CENTER) #,
                                              # compound=tk.LEFT)
                                              # text='A Label with the Helvetica font',
                                              # # ttk.CENTER,
                                              # font=("Helvetica", 14))  )
                                              )
        self.label_1_canvas2_aba4.place(relx=0.007, rely=0.05, relwidth=0.986, relheight=0.12)
        # self.frame1_aba4 = tk.Frame(self.aba4, bd=1, bg='#DCDCDC', highlightbackground='#708090',
        #                            highlightthickness=1)
        # self.frame1_aba4.place(relx=0.03, rely=0.05, relwidth=0.3, relheight=0.9)
        #
        self.lframe1_aba4 = tk.LabelFrame(self.aba4, text="Page size", bg='#A9A9A9', relief=tk.GROOVE, bd=4)
        self.lframe1_aba4.place(relx=0.04, rely=0.2, relwidth=0.2, relheight=0.2)
        
        # # self.canvas1_aba4
        self.bt_image_stop_ab4 = tk.Button(self.aba4, image=self.tkimage6, compound=tk.LEFT, bd=0,
                                           bg='#A9A9A9', activebackground='#A9A9A9', command=self.quit_weaver_reporter)
        self.bt_image_stop_ab4.image = self.tkimage6  # reference to image not garbage collect
        self.bt_image_stop_ab4.place(relx=0.95, rely=0.015, relwidth=0.03, relheight=0.04)
        
        text = 'Bye bye!!!'
        self.create_tool_tip(self.bt_image_stop_ab4, text)
        
        # ---------------configure  self.radiob1_aba4_var
        # store radio selection in variable
        self.radiob1_aba4_var = tk.IntVar()
        
        # last time app was used we saved option in json here self.retrieve... gets it back
        
        self.json_letter_or_A4_radiob1_aba4_var = ''
        self.retrieve_letter_or_A4_radiob1_aba4_json()
        if self.json_letter_or_A4_radiob1_aba4_var == '':
            self.radiob1_aba4_var.set(1)
        else:
            self.radiob1_aba4_var.set(self.json_letter_or_A4_radiob1_aba4_var)
        
        # config font of radio button
        helv20 = tkfont.Font(family='Helvetica', size=12)  # , weight='bold')
        
        self.radiobutton1 = tk.Radiobutton(self.lframe1_aba4, text="Letter",
                                           font=helv20,
                                           variable=self.radiob1_aba4_var, relief=tk.GROOVE, background='#A9A9A9',
                                           activebackground='#A9A9A9', value=1, indicatoron=1, justify=tk.LEFT,
                                           command=self.store_letter_or_A4_json)
        self.radiobutton1.place(relx=0.05, rely=0.1, relwidth=0.7, relheight=0.3)
        
        self.radiobutton2 = tk.Radiobutton(self.lframe1_aba4, text="A4   ", font=helv20,
                                           variable=self.radiob1_aba4_var, relief=tk.GROOVE, background='#A9A9A9',
                                           activebackground='#A9A9A9', value=2, indicatoron=1, justify=tk.LEFT,
                                           command=self.store_letter_or_A4_json)
        self.radiobutton2.place(relx=0.05, rely=0.6, relwidth=0.7, relheight=0.3)
        
        # --------------------------------------------self.lframe2_aba4
        
        self.lframe2_aba4 = tk.LabelFrame(self.aba4, text="Switch Language", bg='#A9A9A9', relief=tk.GROOVE, bd=4)
        self.lframe2_aba4.place(relx=0.04, rely=0.463, relwidth=0.2, relheight=0.2)
        
        # ---------------configure  self.radiob34_aba4_var
        # self.radiobutton3 and self.radiobutton4 select if we will make pdf in
        # portuguese of in english, saving options 1 or 2 to Pages.portuguese_or_english
        # Pages.portuguese_or_english will be just 1 or to
        # inside reportlab classes above we will state--> if 1 do this if 2 do that
        # no rocket science
        
        # generate reference variable to clicked radiob
        self.radiob34_aba4_var = tk.IntVar()
        
        # retrieve
        self.json_port_eng_radiob34_aba4_var = self.retrieve_portg_or_eng_radiob34_aba4_json()
        # try:
        if self.json_port_eng_radiob34_aba4_var == '':
            self.radiob34_aba4_var.set(1)
        else:
            self.radiob34_aba4_var.set(self.json_port_eng_radiob34_aba4_var)
        # except:
        #     self.radiob34_aba4_var.set(1)
        
        helv20 = tkfont.Font(family='Helvetica', size=12)  # , weight='bold')
        
        # self.radiob34_aba4_var = tk.IntVar()
        # select_radiob34_aba4_var stores radiob selectes in json and in  Pages.portuguese_or_english
        self.radiobutton3 = tk.Radiobutton(self.lframe2_aba4, text="English                       ", font=helv20,
                                           variable=self.radiob34_aba4_var, relief=tk.GROOVE, background='#A9A9A9',
                                           activebackground='#A9A9A9', value=1, indicatoron=1, justify=tk.LEFT,
                                           command=self.select_radiob34_aba4_var)
        self.radiobutton3.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.3)
        
        self.radiobutton4 = tk.Radiobutton(self.lframe2_aba4, text="Português                    ", font=helv20,
                                           variable=self.radiob34_aba4_var, relief=tk.GROOVE, background='#A9A9A9',
                                           activebackground='#A9A9A9', value=2, indicatoron=1, justify=tk.LEFT,
                                           command=self.select_radiob34_aba4_var)
        self.radiobutton4.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.3)
        
        # ------------------inferior radiobutton----------self.lframe3_aba4
        
        self.lframe3_aba4 = tk.LabelFrame(self.aba4, text='Show PDF after creation?', bg='#A9A9A9',
                                          relief=tk.GROOVE, bd=4)
        self.lframe3_aba4.place(relx=0.04, rely=0.725, relwidth=0.2, relheight=0.2)
        
        self.radiob56_aba4_var = tk.IntVar()  # we store this radiobutton option with function "store" in json file
        # to use as variable
        
        # retrieve  self.json_show_or_not_PDFradiob56_aba4_var --> values of radio box from file
        self.retrieve_show_or_not_pdf_radiob56_aba4_json()
        
        # try:
        if self.json_show_or_not_PDFradiob56_aba4_var == '':
            self.radiob56_aba4_var.set(1)
        else:
            self.radiob56_aba4_var.set(self.json_show_or_not_PDFradiob56_aba4_var)
        # except Exception:
        #     self.radiob56_aba4_var.set(1)
        
        helv20 = tkfont.Font(family='Helvetica', size=12)  # , weight='bold')
        
        # select_radiob34_aba4_var stores radiob selectes in json and in  Pages.portuguese_or_english
        self.radiobutton5 = tk.Radiobutton(self.lframe3_aba4, text="Show PDF File        ", font=helv20,
                                           variable=self.radiob56_aba4_var, relief=tk.GROOVE, background='#A9A9A9',
                                           activebackground='#A9A9A9', value=1, indicatoron=1, justify=tk.LEFT,
                                           command=self.select_radiob56_aba4_var)
        self.radiobutton5.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.3)
        
        self.radiobutton6 = tk.Radiobutton(self.lframe3_aba4, text="Don't Show PDF File", font=helv20,
                                           variable=self.radiob56_aba4_var, relief=tk.GROOVE, background='#A9A9A9',
                                           activebackground='#A9A9A9', value=2, indicatoron=1, justify=tk.LEFT,
                                           command=self.select_radiob56_aba4_var)
        self.radiobutton6.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.3)
        
        # ---------------------------------self.lframe3_aba4 end
        
        # ---------------------------------self.lframe4_aba4 --> upper labelframe in 2 colune from left
        
        self.lframe4_aba4 = tk.LabelFrame(self.aba4, text='Show Header Table?', bg='#A9A9A9',
                                          relief=tk.GROOVE, bd=4)
        self.lframe4_aba4.place(relx=0.28, rely=0.2, relwidth=0.2, relheight=0.2)
        
        self.radiob78_aba4_var = tk.IntVar()
        
        # retrieve  self.json_show_or_not_PDFradiob56_aba4_var --> values of radio box from file
        self.retrieve_Table_header_YorN_radiob78_json()  # --> this method gets value stored in json file
        # and presents here if is 1 or 2 to be used bellow (1 is first radiobutton7 and 2 is radiobutton8)
        
        # try:
        if self.json_show_or_not_Table_radiob78_aba4_var == '':
            self.radiob78_aba4_var.set(1)
        else:
            self.radiob78_aba4_var.set(self.json_show_or_not_Table_radiob78_aba4_var)
        # except Exception:
        #     self.radiob78_aba4_var.set(1)
        
        helv20 = tkfont.Font(family='Helvetica', size=12)  # , weight='bold')
        
        # select_radiob34_aba4_var stores radiob selectes in json and in  Pages.portuguese_or_english
        self.radiobutton7 = tk.Radiobutton(self.lframe4_aba4, text="Show Table                  ", font=helv20,
                                           variable=self.radiob78_aba4_var, relief=tk.GROOVE, background='#A9A9A9',
                                           activebackground='#A9A9A9', value=1, indicatoron=1, justify=tk.LEFT,
                                           command=self.select_radiob78_aba4_var)
        self.radiobutton7.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.3)
        
        self.radiobutton8 = tk.Radiobutton(self.lframe4_aba4, text="Dismiss Header Table", font=helv20,
                                           variable=self.radiob78_aba4_var, relief=tk.GROOVE, background='#A9A9A9',
                                           activebackground='#A9A9A9', value=2, indicatoron=1, justify=tk.LEFT,
                                           command=self.select_radiob78_aba4_var)
        
        self.radiobutton8.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.3)
        # ----------------------------------------------self.lframe4_aba4 END
        
        # ----------------------------------------#self.lframe5_aba4 --> middle labelframe in 2 colune from left start
        
        self.lframe5_aba4 = tk.LabelFrame(self.aba4, text='Select Main Title', bg='#A9A9A9',
                                          relief=tk.GROOVE, bd=4)
        self.lframe5_aba4.place(relx=0.28, rely=0.46, relwidth=0.2, relheight=0.465)
        
        self.radiob90_1or2_aba4_var = tk.IntVar()
        
        # retrieve  self.json_show_or_not_PDFradiob56_aba4_var --> values of radio box from file
        # self.retrieve_main_title_radiob90_json()  # --> this method gets value stored in json file
        # and presents here if is 1 or 2 to be used bellow (1 is first radiobutton7 and 2 is radiobutton8)
        
        # self.retrieve_Pdf_Title_1or2_radiob90_aba4_var_json()
        #
        # try:
        #     if self.retrieved_Pdf_Title_radiob90_aba4_var_json == '':
        #         self.radiob90_1or2_aba4_var.set(1)
        #     else:
        #         self.radiob90_1or2_aba4_var.set(self.retrieved_Pdf_Title_1or2_aba4_var_json)
        # except Exception:
        #     self.radiob90_1or2_aba4_var.set(1)
        
        self.get_pdf_title_1_or_2()
        
        helv20 = tkfont.Font(family='Helvetica', size=12)  # , weight='bold')
        
        # select_radiob34_aba4_var stores radiob selectes in json and in  Pages.portuguese_or_english
        self.radiobutton9 = tk.Radiobutton(self.lframe5_aba4, text="Use Electroencephalogram", font=helv20,
                                           variable=self.radiob90_1or2_aba4_var, relief=tk.GROOVE, background='#BEBEBE',
                                           activebackground='#BEBEBE', value=1, indicatoron=0, justify=tk.LEFT,
                                           command=self.store_newPdfTitle_entry_aba4)
        self.radiobutton9.place(relx=0.05, rely=0.03, relwidth=0.9, relheight=0.15)
        self.radiobutton9.config(foreground='black', selectcolor='#BEBEBE')
        
        # print(self.radiob90_1or2_aba4_var.get())
        
        self.radiobutton0 = tk.Radiobutton(self.lframe5_aba4, text="Create Another Title    ", font=helv20,
                                           variable=self.radiob90_1or2_aba4_var, relief=tk.GROOVE, background='#A9A9A9',
                                           activebackground='#BEBEBE', value=2, indicatoron=0, justify=tk.LEFT,
                                           command=self.store_newPdfTitle_entry_aba4)
        self.radiobutton0.config(foreground='black', selectcolor='#BEBEBE')
        self.radiobutton0.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.15)
        
        # ------------------------------------------------
        # Entry Widget
        # highlightthickness for thickness of the border
        # self.pdf_titlename_entry = tk.Entry(highlightthickness=2)
        
        # highlightbackground and highlightcolor for the border color
        # ------------------------------------------------
        
        self.pdf_titlenamelabel = tk.Label(self.lframe5_aba4, text="or you can write down a new\nmainTitle and just "
                                                                   "after\nthat... check button bellow.",
                                           font=("Helvetica", 12),
                                           borderwidth=1, relief="solid")
        
        self.pdf_titlenamelabel.place(relx=0.05, rely=0.23, relwidth=0.9, relheight=0.32)
        self.pdf_titlenamelabel.config(background='#C8C8C8', highlightbackground="#404040",
                                       highlightthickness=1, highlightcolor="#404040")
        # ------------------------------------------------
        
        self.pdf_titlename_var = tk.StringVar()
        self.pdf_titlename_entry = tk.Entry(self.lframe5_aba4, textvariable=self.pdf_titlename_var,
                                            font=('calibre', 10, 'normal'), highlightthickness=2)
        self.pdf_titlename_entry.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.15)
        self.pdf_titlename_entry.config(background='#C8C8C8', highlightbackground="#404040", highlightcolor="#696969")
        
        # ------------------self.lframe5_aba4 --> middle labelframe in 2 colune from left end
        
        # ------------------self.lframe6_aba4 -->third column from left in aba4 start
        # show all fonts availables, it is associated with EEG_Reporter_funcs  def get_font_from_cbox
        
        self.lframe6_aba4 = tk.LabelFrame(self.aba4, text='Select Font', bg='#A9A9A9',
                                          relief=tk.GROOVE, bd=4)
        self.lframe6_aba4.place(relx=0.525, rely=0.2, relwidth=0.2, relheight=0.5)
        
        # ---------------create list of python fonts
        self.font_chosen_cbox = tk.StringVar()
        # https://stackoverflow.com/questions/69409837/tkinter-combobox-loop-again-getting-the-results
        
        # -------------------------- just to chance color of combobox start
        
        style = ttk.Style()  # styles --> ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        
        # Note the code line below.
        # Be sure to include this or style.map() won't function as expected.
        # style.theme_use('alt')
        style.theme_use('classic')
        
        # https://stackoverflow.com/questions/31545559/how-to-change-background-color-in-ttk-comboboxs-listview
        # variables created for colors
        ebg = '#404040'
        fg = '#FFFFFF'
        # the following alters the Listbox
        self.lframe6_aba4.option_add('*TCombobox*Listbox*Background', ebg)
        self.lframe6_aba4.option_add('*TCombobox*Listbox*Foreground', fg)
        self.lframe6_aba4.option_add('*TCombobox*Listbox*selectBackground', fg)
        self.lframe6_aba4.option_add('*TCombobox*Listbox*selectForeground', ebg)
        
        # the following alters the Combobox entry field
        style.map('TCombobox', fieldbackground=[('readonly', ebg)])
        style.map('TCombobox', selectbackground=[('readonly', ebg)])
        style.map('TCombobox', selectforeground=[('readonly', fg)])
        style.map('TCombobox', background=[('readonly', '#c4c3d0')])
        style.map('TCombobox', foreground=[('readonly', '#c4c3d0')])
        
        # --------------------------
        
        # it is appended inside  self.list_font_available_reportLab()
        self.list_font_available_reportLab()
        
        self.reportlab_fonts_to_use = sorted(self.reportlab_fonts_to_use, reverse=0)  # fonts I selected
        
        self.font_comboB_aba4 = ttk.Combobox(self.lframe6_aba4, values=self.reportlab_fonts_to_use,  # usefull_fonts,
                                             textvariable=self.font_chosen_cbox, font=('Helvetica', 16))
        
        self.font_comboB_aba4.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.13)
        self.font_comboB_aba4.bind("<<ComboboxSelected>>", self.store_font_cbox_aba4_json)
        
        # ----------------combobox to list fonts
        
        self.pdf_combo1label = tk.Label(self.lframe6_aba4, text="To use default font \n Helvetica "
                                                                "check button.",
                                        font=("Helvetica", 12),
                                        borderwidth=1, relief="solid")
        
        self.pdf_combo1label.place(relx=0.05, rely=0.03, relwidth=0.9, relheight=0.13)
        self.pdf_combo1label.config(background='#C8C8C8', highlightbackground="#404040",
                                    highlightthickness=1, highlightcolor="#404040")
        
        # -----------------------radio buttons:
        # https://stackoverflow.com/questions/40684739/why-do-tkinters-radio-buttons-all-start-selected-when-using-
        # stringvar-but-not-i
        
        self.radiob_cbox_aba4_var = tk.IntVar()
        
        self.retrieve_radiob1_cbox_aba4_json()  # returns self.retrieved_currentFont_comBx_aba4_json
        
        # try:
        if self.retrieved_radiob1_cbox_aba4_json == '':
            self.radiob_cbox_aba4_var.set(1)
        else:
            self.radiob_cbox_aba4_var.set(self.retrieved_radiob1_cbox_aba4_json)
        # except:
        # else:
        #     self.radiob_cbox_aba4_var.set(1)
        
        # self.radiob_cbox_aba4_var = tk.StringVar()    #one type of variable for each set of radiobuttons
        
        self.radiob1_cbox_aba4 = tk.Radiobutton(self.lframe6_aba4, text="Default font.                 ",
                                                font=helv20,
                                                variable=self.radiob_cbox_aba4_var, relief=tk.GROOVE,
                                                background='#A9A9A9',
                                                activebackground='#A9A9A9', value=1, indicatoron=1, justify=tk.LEFT,
                                                command=self.store_radiob1_cbox_aba4_var)
        self.radiob1_cbox_aba4.place(relx=0.05, rely=0.23, relwidth=0.9, relheight=0.13)
        
        self.radiob2_cbox_aba4 = tk.Radiobutton(self.lframe6_aba4, text="Selected font.             ", font=helv20,
                                                variable=self.radiob_cbox_aba4_var, relief=tk.GROOVE,
                                                background='#A9A9A9',
                                                activebackground='#A9A9A9', value=2, indicatoron=1, justify=tk.LEFT,
                                                command=self.store_radiob1_cbox_aba4_var)
        self.radiob2_cbox_aba4.place(relx=0.05, rely=0.838, relwidth=0.9, relheight=0.13)
        
        # ------------------------------------
        self.pdf_combo2label = tk.Label(self.lframe6_aba4, text="or First select a font and"
                                                                "\nafter that check button bellow.",
                                        font=("Helvetica", 10),
                                        borderwidth=1, relief="solid")
        
        self.pdf_combo2label.place(relx=0.05, rely=0.46, relwidth=0.9, relheight=0.13)
        self.pdf_combo2label.config(background='#C8C8C8', highlightbackground="#404040",
                                    highlightthickness=1, highlightcolor="#404040")
        
        # ------------------self.lframe6_aba4 -->third column from left in aba4 end
        # ------------------self.lframe7_aba4 -->third column from left in aba4 end
        
        self.lframe7_aba4 = tk.LabelFrame(self.aba4, text='End Config', bg='#A9A9A9',
                                          relief=tk.GROOVE, bd=4)
        # self.lframe7_aba4.place(relx=0.525, rely=0.74, relwidth=0.2, relheight=0.185)
        self.lframe7_aba4.place(relx=0.765, rely=0.46, relwidth=0.2, relheight=0.2)
        
        self.lframe7_label = tk.Label(self.lframe7_aba4, text="Click bellow"
                                                              "\nto confirm changes.",
                                      font=("Helvetica", 12),
                                      borderwidth=1, relief="solid")
        self.lframe7_label.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.45)
        self.lframe7_label.config(background='#C8C8C8', highlightbackground="#404040",
                                  highlightthickness=1, highlightcolor="#404040")
        
        # helv20 = tkfont.Font(family='Helvetica', size=12)
        self.lframe7_button = tk.Button(self.lframe7_aba4, text='Do It!', width=25,
                                        font=('Helvetica', 12), relief=tk.RAISED, background='#A9A9A9',
                                        activebackground='#BEBEBE', justify=tk.LEFT,
                                        command=self.restart_application)
        self.lframe7_button.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.4)
        
        # self.widgets_with_icon()
        # self.translate_lang_01()  #change language of all variables  above (inside this method)
        
        # -----------------------------------
        
        self.lframe8_aba4 = tk.LabelFrame(self.aba4, text='Organize List', bg='#A9A9A9',
                                          relief=tk.GROOVE, bd=4)
        self.lframe8_aba4.place(relx=0.765, rely=0.2, relwidth=0.2, relheight=0.2)
        
        self.radiob_arrow_aba4_var = tk.IntVar()
        #
        self.retrieve_radiob_arrow_aba4_json()  # returns self.retrieved_radiob_arrow_aba4_json
        
        try:
            if self.retrieved_radiob_arrow_aba4_json == '':
                self.radiob_arrow_aba4_var.set(1)
            else:
                # self.retrieved_radiob_arrow_aba4_json == 1:
                self.radiob_arrow_aba4_var.set(self.retrieved_radiob_arrow_aba4_json)
        except (IOError, EOFError) as e:
            self.radiob_arrow_aba4_var.set(1)
        
        self.radiob1_arrow_aba4 = tk.Radiobutton(self.lframe8_aba4, text="Ascending    ", font=helv20,
                                                 variable=self.radiob_arrow_aba4_var, relief=tk.GROOVE,
                                                 background='#A9A9A9',
                                                 activebackground='#A9A9A9', value=1, indicatoron=1, justify=tk.LEFT,
                                                 command=self.store_radiob1_arrow_aba4_var)
        self.radiob1_arrow_aba4.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.35)
        
        self.radiob2_arrow_aba4 = tk.Radiobutton(self.lframe8_aba4, text="Descending   ", font=helv20,
                                                 variable=self.radiob_arrow_aba4_var, relief=tk.GROOVE,
                                                 background='#A9A9A9',
                                                 activebackground='#A9A9A9', value=2, indicatoron=1, justify=tk.LEFT,
                                                 command=self.store_radiob1_arrow_aba4_var)
        self.radiob2_arrow_aba4.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.35)
        
        # ------------------------------------------------------
        self.lframe9_aba4 = tk.LabelFrame(self.aba4, text='Here I Am', bg='#A9A9A9',
                                          relief=tk.GROOVE, bd=4)
        # self.lframe9_aba4.place(relx=0.765, rely=0.46, relwidth=0.2, relheight=0.2)
        self.lframe9_aba4.place(relx=0.525, rely=0.74, relwidth=0.2, relheight=0.185)
        
        self.lframe9_label1 = tk.Label(self.lframe9_aba4, text="Site: sinapsy.com.br."
                                                               "\nInstagram: EEGTube"
                                                               "\nyoutube: EEGTube"
                                                               "\ncontact: \npkanda@alumni.usp.br",
                                       # font=("Helvetica", 12),
                                       font=("Helvetica-Bold", 10, "bold"),
                                       borderwidth=1, relief="raised")
        self.lframe9_label1.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        self.lframe9_label1.config(background='#C8C8C8', highlightbackground="#404040",
                                   highlightthickness=1, highlightcolor="#404040")
        
        # ---------------------------------------------
        self.config_label_style()
        self.lframe10_aba4 = tk.LabelFrame(self.aba4, text='Terms of Use', bg='#A9A9A9',
                                           relief=tk.GROOVE, bd=4)
        # self.lframe7_aba4.place(relx=0.525, rely=0.74, relwidth=0.2, relheight=0.185)
        self.lframe10_aba4.place(relx=0.765, rely=0.74, relwidth=0.2, relheight=0.185)
        
        self.lframe10_label = tk.Label(self.lframe10_aba4, text="Click bellow"
                                                                "\nto to know our terms.",
                                       font=("Helvetica", 12),
                                       borderwidth=1, relief="solid")
        self.lframe10_label.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.45)
        self.lframe10_label.config(background='#C8C8C8', highlightbackground="#404040",
                                   highlightthickness=1, highlightcolor="#404040")
        
        self.lframe10_button = ttk.Button(self.lframe10_aba4, text='Go to Terms!', width=25,
                                          command=self.multiple_window_terms_use_modal)
        self.lframe10_button.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.4)
        
        # -----------------------------------
    
    def combobox_chosen(self):
        """
        get gender from combobox
        """
        self.gender_chosen = self.comboGender.get()
        return self.gender_chosen
    
    @staticmethod
    def make_normal(textwidget):
        """
        https://stackoverflow.com/questions/64081647/how-to-bold-selected-text-in-tkinter
        """
        if "boldtext" in textwidget.tag_names("sel.first"):
            textwidget.tag_remove("boldtext", "sel.first", "sel.last")
        else:
            textwidget.tag_add("boldtext", "sel.first", "sel.last")
    
    # def check_pos(self, event):
    #     '''
    #     find cursor position  in Text widget to posteriorly insert html commands
    #     '''
    #     print(self.txt_body.index(tk.INSERT))
    
    # def handle(self, event):
    #     print(self.txt_body.index(f"@{event.x},{event.y}"), self.txt_body.index("current"))
    
    # def move_mouse_over_text(self, event):
    #     x, y = event.x, event.y
    #
    #     x1, y2 = self.txt_body.old_coords
    #     if self.txt_body.old_coords:
    #         x1, y1 = self.txt_body.old_coords
    #     print(x,y,x1,y1)
    
    #     canvas.create_line(x, y, x1, y1)
    # canvas.old_coords = x, y
    # x, y = event.x, event.y
    
    # if str(event.type) == 'ButtonPress':
    #     # self.txt_body.old_coords = event.x , event.y
    #     x, y = event.x , event.y
    #     print(x ,y)
    #
    #
    
    # elif str(event.type) == 'ButtonRelease':
    #     x, y = event.x, event.y
    #     x1, y1 =self.txt_body.old_coords
    # print(x,y,x1,y1)
    
    def make_frames_widgets(self):
        """
        these widgets are those that contain text in frames header/ body/footer
        """
        
        # get font selected in combobox aba4 as  self.my_specific_font
        self.choose_font_to_use()  # gives variables to ptext       --> needed to change font
        # Font_tuple = (self.my_specific_font, 10, "bold")
        Font_tuple = tkfont.Font(family=self.my_specific_font, size=12)  # , weight='normal', slant='roman')
        
        # --------------------HEADER --> NAME OF CLINIC, ADRESS, TEL , ETC
        # text field for Report header
        self.txt_header = tk.Text(self.frame_header, bg='#DCDCDC', height=5, undo=True)
        self.txt_header.configure(font=Font_tuple)  # CONFIGURE FONT
        # self.txt_header.configure(font=(self.my_specific_font, 10, "bold"))  #CONFIGURE FONT
        
        # -------------------------------------------
        # when click ENTER inserts <b/> in text
        # self.txt_header.bind("<Return>", lambda event:self.insert_in_Textwidget(event,self.txt_header))
        # -------------------------------------------
        
        self.txt_header.place(relx=0.02, rely=0.00, relwidth=0.96, relheight=1)
        self.lb_header = tk.Label(self.frame_header, text='HEADER', font='Arial 8 bold', wraplength=1)
        self.lb_header.place(relx=0.0, rely=0.00, relwidth=0.02, relheight=1)
        
        # here we say to click_frame(self, event) that active frame is self.txt_header
        # self.active_text_frame in  self.make_normal(self.active_text_frame) and in
        # self.make_bold(self.active_text_frame)  says wich frame is active to style fonts
        
        # -----------------------------------------------------
        # this links
        # self.txt_header.widget = self.txt_header
        # self.txt_header.bind("<Button-1>", self.click_frame)
        # self.txt_header.bind("<Button-2>", self.focus_next_window)
        
        # -------- this make </br> insert in tk.Text when <Return> is pressed
        
        self.txt_header.bind("<Return>", lambda event: self.insert_in_Textwidget(event, self.txt_header))
        self.txt_header.bind('<Tab>', lambda event: self.insert_Tab_in_Textwidget(event, self.txt_header))
        self.txt_header.widget = self.txt_header
        # self.txt_header.bind("<Button-1>", self.click_frame)
        # -----------------------------------------------------
        
        self.scrool_header = tk.Scrollbar(self.frame_header, orient='vertical', command=self.txt_header.yview)
        self.txt_header.configure(yscroll=self.scrool_header.set)
        # self.scrool_header.place(relx=0.985, rely=0.01, relwidth=0.01, relheight=0.99)
        self.scrool_header.place(relx=0.985, rely=0.01, relwidth=0.01, relheight=0.99)
        
        # --------------------------
        
        # text field for Report Body
        # self.txt_body = tk.Text(self.frame_body, bg = '#DCDCDC', height=5, undo=True)
        self.txt_body = tk.Text(self.frame_body, bg='WHITE', height=5, undo=True)
        self.txt_body.configure(font=Font_tuple)  # CONFIGURE FONT
        self.txt_body.place(relx=0.02, rely=0.00, relwidth=0.96, relheight=1)
        self.lb_body = tk.Label(self.frame_body, text='EEG..REPORT.. BODY', font='Arial 8 bold', wraplength=1)
        self.lb_body.place(relx=0.0, rely=0.00, relwidth=0.02, relheight=1)
        
        # self.txt_body.old_coords = None
        # self.txt_body.bind("<space>",self.handle)
        # self.txt_body.bind('<B1-Motion>',self.move_mouse_over_text)
        # self.txt_body.old_coords = None
        # self.txt_body.bind('<ButtonPress-1>', self.move_mouse_over_text)
        # self.txt_body.bind('<ButtonRelease-1>', self.move_mouse_over_text)
        
        # -------- this make </br> insert in tk.Text when <Return> is pressed
        self.txt_body.bind("<Return>", lambda event: self.insert_in_Textwidget(event, self.txt_body))
        self.txt_body.bind('<Tab>', lambda event: self.insert_Tab_in_Textwidget(event, self.txt_body))
        # bind('<Tab>', enter_tab)
        
        # here we say to click_frame(self, event) that active frame is self.txt_header
        # self.active_text_frame in  self.make_normal(self.active_text_frame) and in
        # self.make_bold(self.active_text_frame)  says wich frame is active to style fonts
        self.txt_body.widget = self.txt_body
        self.txt_body.bind("<Button-1>", self.click_frame)
        
        # self.txt_body.bindtags(('Text', 'post-class-bindings', '.', 'all'))
        # # self.txt_body.bind_class("post-class-bindings", "<KeyPress>", self.check_pos)
        # self.txt_body.bind_class("post-class-bindings", "<Button-2>", self.check_pos)
        
        self.scrool_body = tk.Scrollbar(self.frame_body, orient='vertical', command=self.txt_body.yview)
        self.txt_body.configure(yscroll=self.scrool_body.set)
        self.scrool_body.place(relx=0.985, rely=0.01, relwidth=0.01, relheight=0.99)
        
        # ------------------text footer
        
        self.txt_footer = tk.Text(self.frame_footer, bg='#DCDCDC', height=5, undo=True)
        self.txt_footer.configure(font=Font_tuple)  # CONFIGURE FONT
        self.txt_footer.place(relx=0.02, rely=0.00, relwidth=0.96, relheight=1)
        self.lb_footer = tk.Label(self.frame_footer, text="DOCTOR", font='Arial 8 bold', wraplength=1)
        self.lb_footer.place(relx=0, rely=0, relwidth=0.02, relheight=1)
        
        # this make </br> insert in tk.Text when <Return> is pressed
        self.txt_footer.bind("<Return>", lambda event: self.insert_in_Textwidget(event, self.txt_footer))
        
        # to style font bold or normal:
        self.txt_footer.widget = self.txt_footer
        self.txt_footer.bind("<Button-1>", self.click_frame)
        
        self.scrool_footer = tk.Scrollbar(self.frame_footer, orient='vertical', command=self.txt_footer.yview)
        self.txt_footer.configure(yscroll=self.scrool_footer.set)
        self.scrool_footer.place(relx=0.985, rely=0.01, relwidth=0.01, relheight=0.99)
        
        # #-----------------------------------------------------------------------------
        # it was very difficult to find a way to get a path 'c:\temp\my_file.jpg' and
        # insert it in treeview, treev do not
        # accept strings, after most of diverse tries what works is put the string in
        # an entry, and then I can insert it in
        # treeview, besides I don't have to "place"  self.signature_img_entry.
        
        # Just to insert image in treeview --> do not need place
        self.signature_img_entry_logo = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')  # ,
        # Just to insert image in treeview --> do not need place
        self.signature_img_entry = ttk.Entry(self.aba1, style='style.TEntry', font='sans 10 bold')  # ,
        # self.signature_img_entry.place(relx=0.65, rely=0.08, relwidth=0.03)
        
        # -----------------------------------------------------------------------------
        # just one line of code at end of tab1
        
        # -------------------------------last line in aba1
        
        self.frame_patient_history1 = tk.Frame(self.aba1, bd=1, bg='#C0C0C0', highlightbackground='#36454F',
                                               highlightthickness=1)
        self.frame_patient_history1.place(relx=0.003, rely=0.92, relwidth=0.995, relheight=0.077)
        
        self.txt_history1 = tk.Text(self.frame_patient_history1, bg='#DCDCDC', height=5, undo=True)
        self.txt_history1.configure(font=Font_tuple)  # CONFIGURE FONT
        self.txt_history1.place(relx=0.02, rely=0.00, relwidth=0.96, relheight=0.98)
        self.lb_txt_history1 = tk.Label(self.frame_patient_history1, text="END", font='Arial 8 bold', wraplength=1)
        self.lb_txt_history1.place(relx=0, rely=0, relwidth=0.02, relheight=1)
        
        # this make </br> insert in tk.Text when <Return> is pressed
        self.txt_history1.bind("<Return>", lambda event: self.insert_in_Textwidget(event, self.txt_history1))
        
        # style font:
        self.txt_history1.widget = self.txt_history1
        self.txt_history1.bind("<Button-1>", self.click_frame)
        
        # scrool bar:
        self.scrool_txt_history1 = tk.Scrollbar(self.frame_patient_history1, orient='vertical',
                                                command=self.txt_history1.yview)
        self.txt_history1.configure(yscroll=self.scrool_txt_history1.set)
        self.scrool_txt_history1.place(relx=0.985, rely=0.01, relwidth=0.01, relheight=0.99)
        
        # -------------------- frames in aba1-----------------------end
        
        # -------------------------------------------------------------------------aba2 widgets
        
        # -------------------------------- frame in tab 2
        self.frame_history = tk.Frame(self.aba2, bd=2, bg='#C0C0C0',
                                      highlightbackground='#36454F',
                                      highlightthickness=1)
        self.frame_history.place(relx=0.003, rely=0.07, relwidth=0.995,
                                 relheight=0.925)
        # -------------------------------- frame in tab 2 end
        
        # -------------------------------- frame in tab 3 start
        
        self.frame_Tree_aba3 = tk.Frame(self.aba3, bd=1, bg='#C0C0C0', highlightbackground='#36454F',
                                        highlightthickness=1)
        self.frame_Tree_aba3.place(relx=0.003, rely=0.12, relwidth=0.995, relheight=0.875)
        
        # self.lb_frame_Tree_aba3 = tk.Label(self.frame_Tree_aba3, text=("ALL-REPORT-MODELS"),
        #                                    font='Arial 8 bold', wraplength=1)
        #                                     # , command = self.charge_treeV_to_aba3)
        # self.lb_frame_Tree_aba3.place(relx=0, rely=0.01, relwidth=0.02, relheight=0.97)
        
        # -------------------------------- frame in tab 3 end
        
        # -------------------------------- buttons and commands in page two (aba2)
        
        # clears only clinical history
        self.bt_delete_history = ttk.Button(self.aba2, text='Delete History Only', style='Bold.TButton',
                                            command=self.delete_history)
        self.bt_delete_history.place(relx=0.35, rely=0.01, relwidth=0.11, relheight=0.05)
        
        self.bt_save_update_aba2 = ttk.Button(self.aba2, text='Save History', style='Bold.TButton',
                                              command=self.update_report)
        self.bt_save_update_aba2.place(relx=0.463, rely=0.01, relwidth=0.09, relheight=0.05)
        
        self.bt_Report_aba2 = ttk.Button(self.aba2, text='Clinical History to PDF', style='Bold.TButton',
                                         command=self.create_clinical_info_report)
        self.bt_Report_aba2.place(relx=0.55, rely=0.01, relwidth=0.14, relheight=0.05)
        
        # ----------------------------change font bold normal---------------------start aba1
        
        # #--------------icons bold and normal  aba1        # self.icon_images()    comes here
        #
        # self.bt_text_bold_aba1 = tk.Button(self.aba1, image=self.tkimage_font_bold, compound=tk.LEFT,
        #                                    bd=0, bg='#A9A9A9', activebackground='#A9A9A9',
        #                                    command=lambda: self.make_bold(self.txt_header))
        #                                                                   # self.txt_body,
        #                                                                   # self.txt_footer,
        #                                                                   # self.txt_history1)),
        # self.bt_text_bold_aba1.image =self.tkimage_font_bold  # to avoid image garbaged collected
        # self.bt_text_bold_aba1.place(relx=0.62, rely=0.01, relwidth=0.034, relheight=0.05)
        #
        # # self.bt_text_normal_aba2 = ttk.Button(self.aba2, text='normal', style='Bold.TButton',
        # self.bt_text_normal_aba1 = tk.Button(self.aba1, image=self.tkimage_font_normal, compound=tk.LEFT,
        #                                      bd=0, bg='#A9A9A9', activebackground='#A9A9A9',
        #                                      command=lambda: self.make_normal(self.txt_header))
        # self.bt_text_normal_aba1.image = self.tkimage_font_normal
        # self.bt_text_normal_aba1.place(relx=0.65, rely=0.01, relwidth=0.034, relheight=0.05)
        
        # ----------icons bold normal  aba2
        # self.bt_text_bold_aba2 = ttk.Button(self.aba2, text='Bold', style='Bold.TButton',
        # self.bt_text_bold_aba2 = tk.Button(self.aba2, image=self.tkimage_font_bold, compound=tk.LEFT,
        #                                    bd=0, bg='#A9A9A9', activebackground='#A9A9A9',
        #                                    command= lambda: self.make_bold(self.txt_history))
        # self.bt_text_bold_aba2.image = self.tkimage_font_bold   #to avoid image garbaged collected
        # self.bt_text_bold_aba2.place(relx=0.4, rely=0.01, relwidth=0.034, relheight=0.05)
        
        # self.bt_text_normal_aba2 = ttk.Button(self.aba2, text='normal', style='Bold.TButton',
        # self.bt_text_normal_aba2 = tk.Button(self.aba2, image=self.tkimage_font_normal, compound=tk.LEFT,
        #                                    bd=0, bg='#A9A9A9', activebackground='#A9A9A9',
        #                                    command= lambda: self.make_normal(self.txt_history))
        # self.bt_text_normal_aba2.image = self.tkimage_font_normal
        # self.bt_text_normal_aba2.place(relx=0.43, rely=0.01, relwidth=0.034, relheight=0.05)
        #
        
        # ----------------------------change font bold normal---------------------end aba2
        
        # text field for Report Body
        self.txt_history = tk.Text(self.frame_history, bg='#DCDCDC', height=5, undo=True)
        self.txt_history.configure(font=Font_tuple)  # CONFIGURE FONT
        self.txt_history.place(relx=0.025, rely=0.01, relwidth=0.958, relheight=0.978)
        self.txt_history.bind("<Return>", lambda event: self.insert_in_Textwidget(event, self.txt_history))
        
        self.lb_history = tk.Label(self.frame_history, text='PATIENT..HISTORY', font='Arial 8 bold', wraplength=1)
        self.lb_history.place(relx=0.0, rely=0.00, relwidth=0.02, relheight=1)
        
        # this make </br> insert in tk.Text when <Return> is pressed
        self.txt_history.bind("<Return>", lambda event: self.insert_in_Textwidget(event, self.txt_history))
        
        self.scrool_history = tk.Scrollbar(self.frame_history, orient='vertical', command=self.txt_header.yview)
        self.txt_history.configure(yscroll=self.scrool_history.set)
        self.scrool_history.place(relx=0.985, rely=0.01, relwidth=0.01, relheight=0.98)
        
        try:
            if self.json_port_eng_radiob34_aba4_var == 1:
                self.bt_delete_history.config(text='Delete History Only')
                # self.bt_save_update.config(text='Save Text')
                # self.bt_Report.config(text='Clinical History to PDF')
                self.lb_history.config(text='PATIENT..HISTORY')
            
            elif self.json_port_eng_radiob34_aba4_var == 2:
                self.bt_delete_history.config(text='Apagar Só História')
                # self.bt_save_update.config(text='Salve Texto')
                # self.bt_Report.config(text='História Clínica para PDF')
                self.lb_history.config(text='HISTORIA...DO...PACIENTE')
        except (IOError, EOFError) as e:
            pass
    
    def frame_Sql3_List(self, treeframe):  # lista cli   treeview list
        """
        treeframe  is the generic frame to be substituted by frame in aba1
        or frame in aba3
        
        list name --> lista cli  is done with treeview widget from ttk
        this is the treeview list inside frame_Sql3
        

        """
        # -----------------treeview style---start
        style = ttk.Style()  # Modify the font of the headings
        ttk.Style().configure("Treeview", background='#A9A9A9',
                              foreground='#A9A9A9', fieldbackground='#DCDCDC')
        style.configure("mystyle.Treeview", highlightthickness=1, bd=2,
                        font=('Calibri', 11))  # Modify the font of the body
        # style.configure("mystyle.Treeview.Heading", font=('Calibri', 12))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 10, 'bold'))  # Modify the font of the headings
        # style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        
        # boldStyle = ttk.Style(self.frame_end_aba1)-----------------
        # boldStyle is the font style of abas
        
        boldStyle = ttk.Style(treeframe)
        boldStyle.theme_use('clam')
        # boldStyle.configure("Bold.TButton", font=('Sans', '10', 'bold'))
        boldStyle.configure("Bold.TButton", font=('Helvetica', '10', 'bold'), relief='flat')
        # boldStyle.configure("Bold.TButton", font=('Helvetica', '10'), relief='flat')
        
        boldStyle.configure("Treeview", background="#D3D3D3",
                            fieldbackground="#899499", foreground="black")
        
        # -----------------treeview style---end
        # this is the treeview list
        self.listaCli = ttk.Treeview(treeframe, height=3,
                                     column=('col1', 'col2', 'col3', 'col4', 'col5',
                                             'col6', 'col7', 'col8', 'col9', 'col10',
                                             'col11', 'col12', 'col13', 'col14', 'col15', 'col16'),
                                     style="mystyle.Treeview"
                                     )
        
        # create header of columns
        self.listaCli.heading("#0", text="")  # do not have a column associated
        self.listaCli.heading("#1", text="Id", command=self.ascending)
        self.listaCli.heading("#2", text="Patient", command=self.descending)
        self.listaCli.heading("#3", text="Gender")
        self.listaCli.heading("#4", text="Age")
        self.listaCli.heading("#5", text="Diagnosis")
        self.listaCli.heading("#6", text="LFF")
        self.listaCli.heading("#7", text="HFF")
        self.listaCli.heading("#8", text="SRate")
        self.listaCli.heading("#9", text="RecDate")
        self.listaCli.heading("#10", text="Header")
        self.listaCli.heading("#11", text="Report")
        self.listaCli.heading("#12", text="Doctor")
        self.listaCli.heading("#13", text="Logo")
        self.listaCli.heading("#14", text="Sign")
        self.listaCli.heading("#15", text="End")
        self.listaCli.heading("#16", text="History")
        
        # the proportion 1 aproximately 500 full size --> we trial and error to find
        self.listaCli.column('#0', width=0, stretch="no")
        self.listaCli.column('#1', width=7)  # 'Id'
        self.listaCli.column('#2', width=200)  # Patient
        self.listaCli.column('#3', width=4)  # gender
        self.listaCli.column('#4', width=5)  # age
        self.listaCli.column('#5', width=100)  # diagnosis
        self.listaCli.column('#6', width=5)  # lff
        self.listaCli.column('#7', width=5)  # HFF
        self.listaCli.column('#8', width=3)  # srate
        self.listaCli.column('#9', width=28)  # record date
        self.listaCli.column('#10', width=100)  # header
        self.listaCli.column('#11', width=100)  # report
        self.listaCli.column('#12', width=80)  # doctor
        self.listaCli.column('#13', width=30)  # self.signature image
        self.listaCli.column('#14', width=30)  # self.signature image
        self.listaCli.column('#15', width=30)  # history1
        self.listaCli.column('#16', width=30)  # history
        
        self.listaCli.place(relx=0.025, rely=0.01, relwidth=0.963, relheight=0.96)
        self.translate_lang_01()
        # self.listaCli.tag_configure('oddrow', background = "#D3D3D3")
        # self.listaCli.tag_configure('evenrow', background = "#000000")
        
        # treeview scroolbar
        self.scrool_List = tk.Scrollbar(treeframe, orient='vertical', command=self.listaCli.yview)
        self.listaCli.configure(yscroll=self.scrool_List.set)
        self.scrool_List.place(relx=0.988, rely=0.01, relwidth=0.01, relheight=0.96)
        
        self.scrool_List = tk.Scrollbar(treeframe, orient='horizontal', command=self.listaCli.xview)
        self.listaCli.configure(xscroll=self.scrool_List.set)
        self.scrool_List.place(relx=0.02, rely=0.97, relwidth=0.966, relheight=0.02)
        
        # self.clear_screen()
        self.listaCli.bind("<ButtonRelease-1>", self.LeftButtonClick)
        # self.listaCli.bind("<Double-Button-1>", self.LeftButtonClick)
        # self.clear_screen()
        
        self.lb_frame_Tree_aba3 = tk.Label(treeframe, text="REPORT...MODELS",
                                           font='Arial 8 bold', wraplength=1)
        # , command = self.charge_treeV_to_aba3)
        self.lb_frame_Tree_aba3.place(relx=0.0035, rely=0.01, relwidth=0.02, relheight=0.98)
        
        # try:
        if self.json_port_eng_radiob34_aba4_var == 1:
            self.lb_frame_Tree_aba3.config(text="REPORT...MODELS")
        elif self.json_port_eng_radiob34_aba4_var == 2:
            self.lb_frame_Tree_aba3.config(text="MODELOS... DE... LAUDO")
        # except Exception:
        #     pass
        #
    
    def collect_image(self) -> str:
        """
        to be used in collect_image_footer and "def collect_image_logo(self)"
        to get paths of images
        """
        filetypes = ([
            ('image files', '.png'),
            ('image files', '.jpg'),
        ])
        
        # path and file of image
        self.collected_image = filedialog.askopenfilename(title='Open a file',
                                                          initialdir='/',
                                                          filetypes=filetypes)
        # print('self.collected_image', self.collected_image)
        return self.collected_image
    
    # -----
    
    # def collect_image_logo(self):
    #     """
    #     collect logo image from windows
    #     """
    #     self.collect_image()
    #
    #     self.signature_image_logo = self.collected_image
    #     # print('self.signature_image_logo ', self.signature_image_logo )
    #     # G: / FOTOS PARA REVELAÇÃO /16997548134_4f805a60a4_o.jpg
    #
    #     self.signature_img_entry_logo.delete(0, END)  # Remove any previous content
    #
    #     # try:
    #     self.signature_img_entry_logo.insert(0, self.signature_image_logo)  # Insert new content
    #
    #     # except FileNotFoundError:
    #     #     self.tkimage_signature = PhotoImage(file= resource_path("signature_not_found.png"))
    #     #     self.signature_image_logo = self.tkimage_signature
    #     #     self.signature_img_entry_logo.insert(0, self.signature_image_logo)
    #     #
    #
    #     self.get_footer_image_logo()
    #     # self.get_footer_image()
    #     Pages.listaCli_imagePath_logo = self.listaCli_imagePath_logo
    #
    # # # -----
    # #
    #
    # def collect_image_footer(self) -> typing.Union[str, pathlib.Path]:
    #     """
    #     That was  tough because treeview doesnot accept strings just tuples and lists
    #     get image to use as signature in right part of footer
    #     this function generates a path an file
    #     example: self.signature_image  C:/000_tmp/Paulo.png
    #     https://stackoverflow.com/questions/54358461/how-to-correctly-save-a-absolute-path-as-the-values-of-a-treeview
    #     """
    #     self.collect_image()
    #
    #     self.signature_image = self.collected_image
    #     self.signature_img_entry.delete(0, END)  # Remove any previous content
    #     self.signature_img_entry.insert(0, self.signature_image)  # Insert new content
    #
    #
    #     #
    #     # # debug
    #     # # self.signature_image  C:/000_tmp/Paulo.png
    #     # # ("'" + '"' + self.signature_image + '"'+ "'") The outer set of '
    #     # # means "send this string (including the double quotes ") to the shell –
    #     # # SiHa May 13, 2015 at 11:52
    #     # # https://stackoverflow.com/questions/30212375/python-error-for-space-in-path
    #     # Pages.signature_image = self.signature_image
    #     # print("Pages.signature_image in  self.collect_image_footer", Pages.signature_image)
    #     # # raw name of file G:/FOTOS PARA REVELAÇÃO/16997548134_4f805a60a4_o.jpg
    #     #
    #     # self.signature_image_pluscotes = ("'" + '"' + self.signature_image + '"'+ "'")
    #     # print('self.signature_image in  collect_image_footer', self.signature_image)
    #     # # self.signature_image in collect_image_footer '"G:/FOTOS PARA REVELAÇÃO/16997548134_4f805a60a4_o.jpg"'
    #     # #name with two cotes to avoid bug of spaces inter istrings in path
    #     # Pages.signature_image_pluscotes = self.signature_image_pluscotes
    #     # print('Pages.signature_image_pluscotes', Pages.signature_image_pluscotes)
    #     #
    #     # # Pages.signature_image make local variable self.signature_image to global.
    #     #
    #     # # self.signature_image_to_list()
    #     # self.signature_image_list = (self.signature_image)
    #     # # self.signature_image_list.append(self.signature_image)
    #     # print('self.signature_image_list in  collect_image_footer', self.signature_image_list)
    #     #
    #     # #bellow   self.signature_image_list['"C:/000_tmp/2021-12-13_gui.jpg"']
    #     # # this format is used to insert path in treeview and double cotation to accept spaces in path
    #     # # return self.signature_image_list
    #
    #     self.get_footer_image()
    #     Pages.listaCli_imagePath = self.listaCli_imagePath
    #
    #
    #
    #
    @staticmethod
    def center():  # only to center tkinter screen in pc screen
        """
        centers a tkinter window
        param root the main rootdow or Toplevel rootdow to center
        """
        root.update_idletasks()
        width = root.winfo_width()
        frm_width = root.winfo_rootx() - root.winfo_x()
        root_width = width + 2 * frm_width
        height = root.winfo_height()
        titlebar_height = root.winfo_rooty() - root.winfo_y()
        root_height = height + titlebar_height + frm_width
        x = root.winfo_screenwidth() // 2 - root_width // 2
        y = root.winfo_screenheight() // 2 - root_height // 2
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        root.deiconify()


Application()
# Databank_Generator()

'''
python -m PyInstaller  --noconfirm --onefile --windowed --add-data "c:/
python3102/Lib/site-packages/tkinterdnd2;tkinterdnd2/" "EEG_weaver_Reporter_19_7_22_10h.py"


(file=r"G:\PycharmProjects\EEG_WEAVER\images\salvar_100.png")

put all in one file and remember image localization  ---> file= resource_path("image.png") from
https://stackoverflow.com/questions/51264169/pyinstaller-add-folder-with-images-in-exe-file

r'G:\PycharmProjects\EEG_WEAVER\json_objects\


python -m PyInstaller  --noconfirm --onefile -i "G:/PycharmProjects/EEG_WEAVER/images/header_pdf.ico" --windowed --add
-data "c:/python3102/Lib/site-packages/tkinterdnd2;tkinterdnd2/" "EEG_weaver_Reporter_19_7_22_10h.py"

-----------------
nuitka

--enable-plugin=tk-inter

--windows-icon=ICON_PATH

multiple files:
python.exe -m nuitka --enable-plugin=tk-inter --mingw64 --standalone --onefile --windows-disable-console --windows-icon
-from-ico=G:/PycharmProjects/EEG_WEAVER/images/header_pdf.ico  EEG_weaver_Reporter_19_7_22_10h.py

one file:
--onefile

--onefile
0

Since version 0.6.10 (Dec. 2020) or so, Nuitka has added --onefile option. Docs are a bit scattered/thin, but here are
some examples (also search the page for "onefile"). But basically just to add the --onefile argument (--standalone is
not required). You can also use the -o argument to name the final executable as something other than the name of the
.py script being built (see --help). Not sure when that was added.

-o EEG_weaver_Reporter1.0
python.exe -m nuitka --enable-plugin=tk-inter --mingw64 --onefile --standalone --windows-disable-console --windows
-icon-from-ico=G:/PycharmProjects/EEG_WEAVER/images/header_pdf.ico  EEG_weaver_Reporter_19_7_22_10h.py

python -m auto_py_to_exe

to create one file = explain the localization of files with reporter filepath.py

python -m sphinx.cmd.quickstart

'''
