# ----------------------------------------------------------------
# Paulo Afonso Medeiros Kanda
# Taubate São Paulo Brazil
# 2022-04-20
# EEG Reporter is part of EEGWeaver project
# to improve clinical use of post-processing EEG
# Yes! If you are here You will see the code is messy, with lots of comments and  debugs
# part of my learning process, indulge me.
# ----------------------------------------------------------------

# import copy

class Pages:
    """
    Start using at 031 EEGwaver 14.5.2021_ANIVERSÁRIO DO FELIPE.py
    every variable from here goes to all classes and all methods
    """
    
    # titleVar =''
    filename = ''
    Controler = ''
    name_of_file = 0
    edf_info = ''
    my_input = ''
    base_directory = ''
    never_opened_directory = ''
    last_opened_directory = ''
    container2_mylist = ""
    inicial_EEG_raw_backup = ''
    EEG_raw = ''
    string_info = ''
    # EEG_raw.ch_names = ''
    inicial_EEG_raw_ch_names = ''
    EEG_raw_ch_names = ''  # (1)
    raw_no_ref = ''
    base_path = ''
    EEG_raw_info_date = ''
    
    p2_facts = ''
    p8_facts = ''
    list_of_channels = []  # to populate listbox of channels to edit channels
    # montage = mne.channels.make_standard_montage('standard_1020')  # make standard montage before read raw data
    montage = ''
    listbox_new_data = ''
    listbox_var1 = ''  # edited data from listbox in page2  but in class EditableListBox
    final_list_channels = ''
    pre_rename_channels = ''
    chan_names_no_extra_words = ''
    EEG_raw_bipolar = ''
    model_to_channel_order = ''
    neuronSpectrum_no_extra_words = ''
    original_chan_names_no_extra_words = ''
    ch_names_split = ''
    desired_chan_name_order = ''
    desired_chan_names_order1 = ''
    reordered_chan1 = ''
    montage_referencial01 = ''
    montage_referencial02 = ''
    EEG_Mont_Referencial01 = ''
    EEG_Mont_Referencial02 = ''
    EEG_Mont_Referencial01_ch_names = ''
    dismantle_Bipolar = ''
    EEG_Referencial01 = ['Fp1', 'F7', 'F3', 'T3', 'C3', 'T5', 'P3', 'O1',
                         'Fp2', 'F8', 'F4', 'T4', 'C4', 'T6', 'P4', 'O2', 'Fz', 'Cz', 'Pz', 'Oz']
    # desired_chan_names_order01
    
    EEG_Referencial02 = ['Fp1', 'Fp2', 'F7', 'F8', 'F3', 'F4', 'Fz', 'T3', 'T4', 'C3',  # desired_chan_names_order02
                         'C4', 'Cz', 'T5', 'T6', 'P3', 'P4', 'Pz', 'O1', 'O2', 'Oz']
    
    # it_is_neurosoft_channels = ['EEG FP1-A1', 'EEG FP2-A2', 'EEG F7-A1', 'EEG F8-A2', 'EEG F3-A1', 'EEG FZ-A2',
    #                              'EEG F4-A2', 'EEG T3-A1', 'EEG T4-A2', 'EEG C3-A1', 'EEG CZ-A1', 'EEG C4-A2',
    #                              'EEG T5-A1', 'EEG T6-A2', 'EEG P3-A1', 'EEG PZ-A2', 'EEG P4-A2', 'EEG O1-A1',
    #                              'EEG OZ-A1', 'EEG O2-A2']
    
    it_is_neurosoft_channels = ['FP1-A1', 'FP2-A2', 'F7-A1', 'F8-A2', 'F3-A1', 'FZ-A2', 'F4-A2', 'T3-A1', 'T4-A2',
                                'C3-A1', 'CZ-A1', 'C4-A2', 'T5-A1', 'T6-A2', 'P3-A1', 'PZ-A2', 'P4-A2', 'O1-A1',
                                'OZ-A1', 'O2-A2']
    
    emsa_electrodes = ['EEG F7', 'EEG T3', 'EEG T5', 'EEG Fp1', 'EEG F3', 'EEG C3', 'EEG P3', 'EEG O1',
                       'EEG F8', 'EEG T4', 'EEG T6', 'EEG Fp2', 'EEG F4', 'EEG C4', 'EEG P4', 'EEG O2',
                       'EEG Fz', 'EEG Cz', 'EEG Pz', 'EEG Oz']
    it_is_emsa = emsa_electrodes
    
    it_is_Picone = ['EEG FP1-LE', 'EEG FP2-LE', 'EEG F3-LE', 'EEG F4-LE', 'EEG C3-LE', 'EEG C4-LE', 'EEG A1-LE',
                    'EEG A2-LE', 'EEG P3-LE', 'EEG P4-LE', 'EEG O1-LE', 'EEG O2-LE', 'EEG F7-LE', 'EEG F8-LE',
                    'EEG T3-LE', 'EEG T4-LE', 'EEG T5-LE', 'EEG T6-LE', 'EEG FZ-LE', 'EEG CZ-LE', 'EEG PZ-LE',
                    'EEG OZ-LE', 'EEG PG1-LE', 'EEG PG2-LE', 'EEG EKG-LE', 'EEG SP2-LE', 'EEG SP1-LE', 'EEG RLC-LE',
                    'EEG LUC-LE', 'EEG 30-LE', 'EEG T1-LE', 'EEG T2-LE', 'PHOTIC PH']
    
    # ---------------------------------to create bipolar 01 start
    
    anode01 = ['Fp1', 'F7', 'T3', 'T5', 'Fp1', 'F3', 'C3', 'P3', 'Fp2', 'F8', 'T4', 'T6', 'Fp2', 'F4', 'C4', 'P4',
               'Fz', 'Cz', 'Pz']
    
    cathode01 = ['F7', 'T3', 'T5', 'O1', 'F3', 'C3', 'P3', 'O1', 'F8', 'T4', 'T6', 'O2', 'F4', 'C4', 'P4', 'O2', 'Cz',
                 'Pz', 'Oz']
    
    # ---------------------------------to create bipolar 01 end
    
    # ---------------------------------to create bipolar 02 start
    
    anode02 = ['Fp1', 'F7', 'F3', 'Fz', 'F4', 'T3', 'C3', 'Cz', 'C4', 'T5', 'P3', 'Pz', 'P4', 'T5', 'O1', 'Oz', 'T6']
    cathode02 = ['Fp2', 'F3', 'Fz', 'F4', 'F8', 'C3', 'Cz', 'C4', 'T4', 'P3', 'Pz', 'P4', 'T6', 'O1', 'Oz', 'O2', 'O2']
    
    # ---------------------------------to create bipolar 02 start
    
    bipolar_ch_name01 = ['Fp1-F7', 'F7-T3', 'T3-T5', 'T5-O1', 'Fp1-F3', 'F3-C3', 'C3-P3', 'P3-O1',
                         'Fp2-F8', 'F8-T4', 'T4-T6', 'T6-O2', 'Fp2-F4', 'F4-C4', 'C4-P4', 'P4-O2',
                         'Fz-Cz', 'Cz-Pz', 'Pz-Oz']
    
    # to use in def re_referencing_montages(self, re_reference, re_electrode_pairs ): --> StartPage
    re_reference_bipolar01 = [('Fp1', 'F7'), ('F7', 'T3'), ('T3', 'T5'), ('T5', 'O1'), ('Fp1', 'F3'), ('F3', 'C3'),
                              ('C3', 'P3'),
                              ('P3', 'O1'), ('Fp2', 'F8'), ('F8', 'T4'), ('T4', 'T6'), ('T6', 'O2'), ('Fp2', 'F4'),
                              ('F4', 'C4'),
                              ('C4', 'P4'), ('P4', 'O2'), ('Fz', 'Cz'), ('Cz', 'Pz'), ('Pz', 'Oz')]
    
    bipolar01 = ''  # Pages.bipolar01 is the original referenced  bipolar01
    
    # to use in def re_referencing_montages(self, re_reference, re_electrode_pairs ): --> StartPage
    bipolar_ch_name02 = ['Fp1-Fp2', 'F7-F3', 'F3-Fz', 'Fz-F4', 'F4-F8', 'T3-C3', 'C3-Cz', 'Cz-C4',
                         'C4-T4', 'T5-P3', 'P3-Pz', 'Pz-P4', 'P4-T4', 'T5-O1', 'O1-Oz', 'Oz-O2',
                         'T6-O2']
    bipolar02 = ''  # Pages.bipolar02 is the original referenced  bipolar02
    
    # to use in def re_referencing_montages(self, re_reference, re_electrode_pairs ): --> StartPage
    re_reference_bipolar02 = [('Fp1', 'Fp2'), ('F7', 'F3'), ('F3', 'Fz'), ('Fz', 'F4'), ('F4', 'F8'), ('T3', 'C3'),
                              ('C3', 'Cz'), ('Cz', 'C4'),
                              ('C4', 'T4'), ('T5', 'P3'), ('P3', 'Pz'), ('Pz', 'P4'), ('P4', 'T4'), ('T5', 'O1'),
                              ('O1', 'Oz'), ('Oz', 'O2'),
                              ('T6', 'O2')]
    
    ok_for_bipolar = ['Fp1', 'F7', 'T3', 'T5', 'O1', 'F3', 'C3', 'P3', 'Fp2',
                      'F8', 'T4', 'T6', 'O2', 'F4', 'C4', 'P4', 'Fz', 'Cz', 'Pz', 'Oz']
    
    EEG_raw_rest = ''
    EEG_raw_averaged = ''
    
    RefreshList = ''
    
    container2_lbox = ''
    dict_to_container2lbox = ''
    new_lbox_pathContainer2 = ''
    
    # -------------------- END OF every variable from here goes to all classes and all methods
    # https://python-forum.io/Thread-How-can-I-pass-a-variable-to-another-class-especially-in-this-situation
    lbox_file = ''
    just_cleaned_01 = ''
    EEG_raw_restored_inicial = ''
    
    # ----------------------- Montages start
    
    EEG_raw_bipolar01 = ''
    # ----------------------- Montages end
    
    montage_Result = ''
    
    comboboxMontages_set = ''
    # --------------------------references
    changed_to_Reference_Original = ''
    EEG_changed_to_Reference_Cz = ''
    montage_referencial01_Cz = ''
    EEG_cleaned_01_Cz = ''
    EEG_original_Montage_with_Cz = ''
    montage_Referencial02_Cz = ''
    montage_original = ''
    EEG_raw_bipolar1_or_2_Cz = ''
    
    EEG_cleaned_01_Car = ''
    EEG_original_Montage_Car = ''
    montage_Referencial01_Car = ''
    montage_Referencial02_Car = ''
    EEG_changed_to_Reference_Car = ''
    EEG_raw_bipolar1_or_2_Car = ''
    EEG_cleaned_01_Car_to_Cz = ''
    bipolar01_done_Ref_REST = ''
    
    # -----------------------------stablish position of mouse or keys (<---  --->) in EEG_raw plot()
    # Position_of_mouse =''
    # Position_of_key = ''
    
    name_of_used_file_list = []
    
    # update_scrollbar = ''
    scrolling_position_Mouse = ''
    scrolling_position_ArrowKeys = ''
    event_xdata = ''
    event1_xdata = ''
    # main_EEG_record_fig = ''
    new_file_openned = ''
    # fig = figure.plot()
    # fig.mne.t_start =''
    fig = ''
    event_xdata = ''
    event1_xdata = ''
    
    # --------------------------to plot  startpage main EEG image
    notebkStartPage_frame1 = ''
    notebkStartPage_frame2 = ''
    base_file_name = ''
    
    # --------------------------------
    ten_twenty_EEG_montage = ''
    
    EEG_raw_rest = ''
    
    EEG_raw_automatic = ''
    
    Picone_electrodes = ['EEG FP1-LE', 'EEG FP2-LE', 'EEG F3-LE', 'EEG F4-LE', 'EEG C3-LE', 'EEG C4-LE',
                         'EEG P3-LE', 'EEG P4-LE', 'EEG O1-LE', 'EEG O2-LE', 'EEG F7-LE', 'EEG F8-LE', 'EEG T3-LE',
                         'EEG T4-LE', 'EEG T5-LE', 'EEG T6-LE', 'EEG FZ-LE', 'EEG CZ-LE', 'EEG PZ-LE']
    
    highPassFilter_Result = ""
    EEG_raw_without_filter = ''
    CuttOff = ''
    lowPassFilter_Result = ''
    High_Freq_Stop = ''
    my_fir_window = ''
    EEG_raw_without_notch = ''
    
    ch_Names_result = ''
    
    dirty_EDF = ''  # it is a copy.deepcopy(Pages.inicial_EEG_raw_backup) with all channels to be used in
    # channels edition in page 8 and at end op page 8 its clean to use in start page
    dirty_edf_ch_names_list = ''  # list of channels at end of all
    # work in " EditEDF Page (pag8)" to be used as reference
    # to original referencial channel order, it is used in StartPage in method montage_original
    
    EEG_raw_deleted_checkboxes_pg8 = ''
    
    combobox_result_pg8 = ''
    
    # use in startpage to change reference:
    
    montage_original_Cz = ''
    montage_referencial01_Cz = ''
    montage_referencial02_Cz = ''
    bipolar01_Cz = ''
    bipolar02_Cz = ''
    
    dirty_EDF_average = ''
    montage_referencial01_average = ''
    montage_referencial02_average = ''
    montage_referencial01_Cz_average = ''
    montage_referencial02_Cz_average = ''
    bipolar01_average = ''  # it is a referential montagem, its name is a reference to its origin
    # -----------------------------
    # -----------------------------
    montageANDreference_originals = ''
    montage_original_Ref = ''
    montage_original_Cz = ''
    montage_original_CAR = ''
    montage_original_CSD = ''
    montage_original_REST = ''
    
    montage_referencial_01_Ref = ''
    montage_referencial_01_Cz = ''
    montage_referencial_01_CAR = ''
    montage_referencial_01_CSD = ''
    montage_referencial_01_REST = ''
    
    montage_referencial_02_Ref = ''
    montage_referencial_02_Cz = ''
    montage_referencial_02_CAR = ''
    montage_referencial_02_CSD = ''
    montage_referencial_02_REST = ''
    
    bipolar_01 = ''
    bipolar01_done_Ref_CAR = ''
    bipolar01_done_Ref_CSD = ''
    bipolar01_done_Ref_Cz = ''
    
    bipolar_02 = ''
    
    # #------------------rest reference
    # montage_Original_REST = ''
    #
    # referencial01_REST = ''
    # referencial02_REST = ''
    #
    # #------------------ current source density
    #
    # montage_original_CSD = ''
    # montage_referencial01_csd = ''
    # montage_referencial02_csd = ''
    # bipolar01_csd = ''
    # bipolar02_csd = ''
    #
    # #--------------re_reference
    #
    # re_referenced_raw = ''  #gerated inside function def re_referencing_montages(self) in StartPage (Home)
    # # EEG_raw.first_samp = ''
    #
    # #---------for reference Cz:
    # bipolar01_Ref_Cz = ''
    # bipolar02_Ref_Cz = ''
    # bipolar01_done_Ref_Cz = ''
    # bipolar02_done_Ref_Cz = ''
    #
    # #----------for reference CAR
    # montage_original_CAR = ''
    # bipolar01_done_Ref_averaged = ''
    # bipolar01_car = ''
    # bipolarMontage01_averaged = ''
    # bipolarMontage01_CAR =  ''
    # bipolarMontage01_CAR = ''
    # bipolar01_done_Ref_CAR = ''
    # bipolar02_done_Ref_CAR = ''
    #
    # ----------------------- used in window filter combobox
    windowFilter_Result = ''
    
    # ----------------------PageTwoICA start
    filt_ICA_EEG_raw = ''
    ICA_highPassFilter_Result = ''
    ICA_EEG_raw = ''  # this is Pages.EEG_raw for iCA preprocessing
    ICA_hp_filter = ''  # when we choose 1 or 2 in comboboxes
    # of notebook tab 2 in pagetwo this is the variable  meaning 1 or 2
    ica: ''
    
    # ----------------------------PageTwoICA end
    
    # ----------------------pg8
    chkboxPg8_after_drop_ch = ''  # used im page 8 to say if number of channels in   chkboxPg8_after_drop_ch it means
    # (after drop) is not the same as
    
    # ------------------------reportlab to generate pdf start
    my_code = ''
    my_fileName = ''
    my_header_Report = ''
    my_footer_Report = ''
    my_body_Report = ''
    # ------------------------reportlab to generate pdf end
    
    # ------------------------for use in page8 automatic_clean_channels
    # this is just to filter EEG_dirty
    auto_clean_channels = ['Fp1', 'FP1', 'F7', 'F3', 'T3', 'C3', 'T5', 'P3', 'O1', 'Fp2', 'FP2',
                           'F8', 'F4', 'T4', 'C4', 'T6', 'P4', 'O2', 'Fz', 'Cz', 'Pz', 'Oz', 'FZ', 'CZ', 'PZ', 'OZ']
    
    # created in "def automatic_clean_channels(self): " to be used when file is saved in
    # class Eeg_Weaver(tk.Tk)  def save_file(self): --> to save file as referencial and not as
    # bipolar because bipolar can't reconstruct referencial channels but referencial can reconstruct
    # bipolar, so we have to save in referencial
    #
    automatic_clean_to_save_file = ''
    
    # --------------
    txt_history = ''  # in tab 2 report
    
    signature_image = ''
    recovered_image = ''
    recovered_image_string = ''
    
    # ----------------string variables inside eeg_weaver_reporter to multipage_pdf_generator--------
    id_object = ''
    header_object = ''
    date_object = ''
    patient_object = ''
    gender_object = ''
    age_object = ''
    diagnosis_object = ''
    sample_rate_object = ''
    low_f_f_object = ''
    high_f_f_object = ''
    doctor_name = ''
    signature_image_list = ''
    # recovered_image_object =''
    
    listaCli_imagePath_logo = ''
    listaCli_imagePath = ''
    
    body_Report_text = ''  # it is placed instead of :
    body_Report_object = ''
    # recovered_image_string = ''
    history1_object = ''
    history_report_object = ''
    # txt_last_aba1 = ''
    history_ref1 = ''
    signature_image = ''
    # Pages signature image is --> self.signature_image
    # which is self.signature_image = fd.askopenfilename... etc
    
    # ---------------- debug
    # self.signature_image_pluscotes = ("'" + '"' + self.signature_image + '"' + "'")
    # print('self.signature_image in  collect_image_footer', self.signature_image)
    # self.signature_image in collect_image_footer
    # '"G:/FOTOS PARA REVELAÇÃO/16997548134_4f805a60a4_o.jpg"'
    # name with two cotes to avoid bug of spaces inter istrings in path
    # Pages.signature_image_pluscotes = self.signature_image_pluscotes
    # Pages.signature_image make local variable self.signature_image to global.
    recovered_image_from_db_object = ''
    
    # ----------------
    # used in EEG_weaver_multiple_sqlite to get the path were database are stored
    dbfile_path_and_name = ''
    
    db_list_treeview_path = ''
    
    # used in EEG_weaver_multiple_sqlite def get_database_var() to get name of database
    basename_db = ''
    
    # used in EEG_weaver_multiple_sqlite on_left_clic()
    index_of_inner_treeview = ''
    
    # used in EEG_weaver_multiple_sqlite def getdata(self)
    EEG_report_databanks_list = ''
    
    # created in def retrieve_db_cbox(self): in EEG_weaver_Reporter_funcs to be used in EEG_weaver_Reporter_funcs
    # as the name of the databank
    current_main_db_in_use = ''
    
    # inside def store_after_create_db_list_to_json(self, list_with_new_db):  in EEG_weaver_multiple_sqlite module
    updated_list_with_newdb = ''  # this is the list after new db is created to populate combobox in EEGweaver reporter
    
    # -------------------letter_or_A4 goes in EEG_weaver_Reporter_funcs no determine page size
    
    # letter_or_A4 = ''
    
    radiab1_to_use = ''
    
    # used in reportlab classes in EEG_weaver_Reporter to
    # change language of pdf
    portuguese_or_english = ''
    
    show_or_not_pdf_after_creation = ''
    
    outfilepath_to_pages = ''  # get the full path of pdf created to use in show pdf --> EEG_Report.print_Report()
    
    # this says that we are creating a report history and not a main report
    create_clinical_info_report = ''
    
    terms_of_use = """
TERMS OF USE
    
EEG WeaverEDF Module Report 1.0

 This program is made by Paulo Afonso Medeiros Kanda.
 
 Taubaté São Paulo - Brasil

 Copyright (C) 2022 Paulo Afonso Medeiros Kanda.

 Email: paulokanda@gmail.com

 Disclaimer:
 Despite this software is intend to be useful, there is no warranty, use this software at your own risk!
 EEG WeaverEDF may NOT be used in safety-critical applications, such as life-support medical systems.
 The author is NOT responsible for any consequences. For research and educational purpose only.


                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2022 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

   The GNU General Public License is a free, copyleft license for
 software and other kinds of works.

   The licenses for most software and other practical works are designed
 to take away your freedom to share and change the works.  By contrast,
 the GNU General Public License is intended to guarantee your freedom to
 share and change all versions of a program--to make sure it remains free
 software for all its users.  We, the Free Software Foundation, use the
 GNU General Public License for most of our software; it applies also to
 any other work released this way by its authors.  You can apply it to
 your programs, too.

   When we speak of free software, we are referring to freedom, not
 price.  Our General Public Licenses are designed to make sure that you
 have the freedom to distribute copies of free software (and charge for
 them if you wish), that you receive source code or can get it if you
 want it, that you can change the software or use pieces of it in new
 free programs, and that you know you can do these things.

   To protect your rights, we need to prevent others from denying you
 these rights or asking you to surrender the rights.  Therefore, you have
 certain responsibilities if you distribute copies of the software, or if
 you modify it: responsibilities to respect the freedom of others.

   For example, if you distribute copies of such a program, whether
 gratis or for a fee, you must pass on to the recipients the same
 freedoms that you received.  You must make sure that they, too, receive
 or can get the source code.  And you must show them these terms so they
 know their rights.


   Developers that use the GNU GPL protect your rights with two steps:
 (1) assert copyright on the software, and (2) offer you this License
 giving you legal permission to copy, distribute and/or modify it.

   For the developers' and authors' protection, the GPL clearly explains
 that there is no warranty for this free software.  For both users' and
 authors' sake, the GPL requires that modified versions be marked as
 changed, so that their problems will not be attributed erroneously to
 authors of previous versions.

   Some devices are designed to deny users access to install or run
 modified versions of the software inside them, although the manufacturer
 can do so.  This is fundamentally incompatible with the aim of
 protecting users' freedom to change the software.  The systematic
 pattern of such abuse occurs in the area of products for individuals to
 use, which is precisely where it is most unacceptable.  Therefore, we
 have designed this version of the GPL to prohibit the practice for those
 products.  If such problems arise substantially in other domains, we
 stand ready to extend this provision to those domains in future versions
 of the GPL, as needed to protect the freedom of users.

   Finally, every program is threatened constantly by software patents.
 States should not allow patents to restrict development and use of
 software on general-purpose computers, but in those that do, we wish to
 avoid the special danger that patents applied to a free program could
 make it effectively proprietary.  To prevent this, the GPL assures that
 patents cannot be used to render the program non-free.

   The precise terms and conditions for copying, distribution and
 modification follow.


                        TERMS AND CONDITIONS

   0. Definitions.

   "This License" refers to version 3 of the GNU General Public License.

   "Copyright" also means copyright-like laws that apply to other kinds of
 works, such as semiconductor masks.

   "The Program" refers to any copyrightable work licensed under this
 License.  Each licensee is addressed as "you".  "Licensees" and
 "recipients" may be individuals or organizations.

   To "modify" a work means to copy from or adapt all or part of the work
 in a fashion requiring copyright permission, other than the making of an
 exact copy.  The resulting work is called a "modified version" of the
 earlier work or a work "based on" the earlier work.

   A "covered work" means either the unmodified Program or a work based
 on the Program.

   To "propagate" a work means to do anything with it that, without
 permission, would make you directly or secondarily liable for
 infringement under applicable copyright law, except executing it on a
 computer or modifying a private copy.  Propagation includes copying,
 distribution (with or without modification), making available to the
 public, and in some countries other activities as well.

   To "convey" a work means any kind of propagation that enables other
 parties to make or receive copies.  Mere interaction with a user through
 a computer network, with no transfer of a copy, is not conveying.

   An interactive user interface displays "Appropriate Legal Notices"
 to the extent that it includes a convenient and prominently visible
 feature that (1) displays an appropriate copyright notice, and (2)
 tells the user that there is no warranty for the work (except to the
 extent that warranties are provided), that licensees may convey the
 work under this License, and how to view a copy of this License.  If
 the interface presents a list of user commands or options, such as a
 menu, a prominent item in the list meets this criterion.


   1. Source Code.

   The "source code" for a work means the preferred form of the work
 for making modifications to it.  "Object code" means any non-source
 form of a work.

   A "Standard Interface" means an interface that either is an official
 standard defined by a recognized standards body, or, in the case of
 interfaces specified for a particular programming language, one that
 is widely used among developers working in that language.

   The "System Libraries" of an executable work include anything, other
 than the work as a whole, that (a) is included in the normal form of
 packaging a Major Component, but which is not part of that Major
 Component, and (b) serves only to enable use of the work with that
 Major Component, or to implement a Standard Interface for which an
 implementation is available to the public in source code form.  A
 "Major Component", in this context, means a major essential component
 (kernel, window system, and so on) of the specific operating system
 (if any) on which the executable work runs, or a compiler used to
 produce the work, or an object code interpreter used to run it.

   The "Corresponding Source" for a work in object code form means all
 the source code needed to generate, install, and (for an executable
 work) run the object code and to modify the work, including scripts to
 control those activities.  However, it does not include the work's
 System Libraries, or general-purpose tools or generally available free
 programs which are used unmodified in performing those activities but
 which are not part of the work.  For example, Corresponding Source
 includes interface definition files associated with source files for
 the work, and the source code for shared libraries and dynamically
 linked subprograms that the work is specifically designed to require,
 such as by intimate data communication or control flow between those
 subprograms and other parts of the work.

   The Corresponding Source need not include anything that users
 can regenerate automatically from other parts of the Corresponding
 Source.

   The Corresponding Source for a work in source code form is that
 same work.


   2. Basic Permissions.

   All rights granted under this License are granted for the term of
 copyright on the Program, and are irrevocable provided the stated
 conditions are met.  This License explicitly affirms your unlimited
 permission to run the unmodified Program.  The output from running a
 covered work is covered by this License only if the output, given its
 content, constitutes a covered work.  This License acknowledges your
 rights of fair use or other equivalent, as provided by copyright law.

   You may make, run and propagate covered works that you do not
 convey, without conditions so long as your license otherwise remains
 in force.  You may convey covered works to others for the sole purpose
 of having them make modifications exclusively for you, or provide you
 with facilities for running those works, provided that you comply with
 the terms of this License in conveying all material for which you do
 not control copyright.  Those thus making or running the covered works
 for you must do so exclusively on your behalf, under your direction
 and control, on terms that prohibit them from making any copies of
 your copyrighted material outside their relationship with you.

   Conveying under any other circumstances is permitted solely under
 the conditions stated below.  Sublicensing is not allowed; section 10
 makes it unnecessary.


   3. Protecting Users' Legal Rights From Anti-Circumvention Law.

   No covered work shall be deemed part of an effective technological
 measure under any applicable law fulfilling obligations under article
 11 of the WIPO copyright treaty adopted on 20 December 1996, or
 similar laws prohibiting or restricting circumvention of such
 measures.

   When you convey a covered work, you waive any legal power to forbid
 circumvention of technological measures to the extent such circumvention
 is effected by exercising rights under this License with respect to
 the covered work, and you disclaim any intention to limit operation or
 modification of the work as a means of enforcing, against the work's
 users, your or third parties' legal rights to forbid circumvention of
 technological measures.

   4. Conveying Verbatim Copies.

   You may convey verbatim copies of the Program's source code as you
 receive it, in any medium, provided that you conspicuously and
 appropriately publish on each copy an appropriate copyright notice;
 keep intact all notices stating that this License and any
 non-permissive terms added in accord with section 7 apply to the code;
 keep intact all notices of the absence of any warranty; and give all
 recipients a copy of this License along with the Program.

   You may charge any price or no price for each copy that you convey,
 and you may offer support or warranty protection for a fee.


   5. Conveying Modified Source Versions.

   You may convey a work based on the Program, or the modifications to
 produce it from the Program, in the form of source code under the
 terms of section 4, provided that you also meet all of these conditions:

     a) The work must carry prominent notices stating that you modified
     it, and giving a relevant date.

     b) The work must carry prominent notices stating that it is
     released under this License and any conditions added under section
     7.  This requirement modifies the requirement in section 4 to
     "keep intact all notices".

     c) You must license the entire work, as a whole, under this
     License to anyone who comes into possession of a copy.  This
     License will therefore apply, along with any applicable section 7
     additional terms, to the whole of the work, and all its parts,
     regardless of how they are packaged.  This License gives no
     permission to license the work in any other way, but it does not
     invalidate such permission if you have separately received it.

     d) If the work has interactive user interfaces, each must display
     Appropriate Legal Notices; however, if the Program has interactive
     interfaces that do not display Appropriate Legal Notices, your
     work need not make them do so.

   A compilation of a covered work with other separate and independent
 works, which are not by their nature extensions of the covered work,
 and which are not combined with it such as to form a larger program,
 in or on a volume of a storage or distribution medium, is called an
 "aggregate" if the compilation and its resulting copyright are not
 used to limit the access or legal rights of the compilation's users
 beyond what the individual works permit.  Inclusion of a covered work
 in an aggregate does not cause this License to apply to the other
 parts of the aggregate.


   6. Conveying Non-Source Forms.

   You may convey a covered work in object code form under the terms
 of sections 4 and 5, provided that you also convey the
 machine-readable Corresponding Source under the terms of this License,
 in one of these ways:

     a) Convey the object code in, or embodied in, a physical product
     (including a physical distribution medium), accompanied by the
     Corresponding Source fixed on a durable physical medium
     customarily used for software interchange.

     b) Convey the object code in, or embodied in, a physical product
     (including a physical distribution medium), accompanied by a
     written offer, valid for at least three years and valid for as
     long as you offer spare parts or customer support for that product
     model, to give anyone who possesses the object code either (1) a
     copy of the Corresponding Source for all the software in the
     product that is covered by this License, on a durable physical
     medium customarily used for software interchange, for a price no
     more than your reasonable cost of physically performing this
     conveying of source, or (2) access to copy the
     Corresponding Source from a network server at no charge.

     c) Convey individual copies of the object code with a copy of the
     written offer to provide the Corresponding Source.  This
     alternative is allowed only occasionally and noncommercially, and
     only if you received the object code with such an offer, in accord
     with subsection 6b.

     d) Convey the object code by offering access from a designated
     place (gratis or for a charge), and offer equivalent access to the
     Corresponding Source in the same way through the same place at no
     further charge.  You need not require recipients to copy the
     Corresponding Source along with the object code.  If the place to
     copy the object code is a network server, the Corresponding Source
     may be on a different server (operated by you or a third party)
     that supports equivalent copying facilities, provided you maintain
     clear directions next to the object code saying where to find the
     Corresponding Source.  Regardless of what server hosts the
     Corresponding Source, you remain obligated to ensure that it is
     available for as long as needed to satisfy these requirements.

     e) Convey the object code using peer-to-peer transmission, provided
     you inform other peers where the object code and Corresponding
     Source of the work are being offered to the general public at no
     charge under subsection 6d.

   A separable portion of the object code, whose source code is excluded
 from the Corresponding Source as a System Library, need not be
 included in conveying the object code work.

   A "User Product" is either (1) a "consumer product", which means any
 tangible personal property which is normally used for personal, family,
 or household purposes, or (2) anything designed or sold for incorporation
 into a dwelling.  In determining whether a product is a consumer product,
 doubtful cases shall be resolved in favor of coverage.  For a particular
 product received by a particular user, "normally used" refers to a
 typical or common use of that class of product, regardless of the status
 of the particular user or of the way in which the particular user
 actually uses, or expects or is expected to use, the product.  A product
 is a consumer product regardless of whether the product has substantial
 commercial, industrial or non-consumer uses, unless such uses represent
 the only significant mode of use of the product.

   "Installation Information" for a User Product means any methods,
 procedures, authorization keys, or other information required to install
 and execute modified versions of a covered work in that User Product from
 a modified version of its Corresponding Source.  The information must
 suffice to ensure that the continued functioning of the modified object
 code is in no case prevented or interfered with solely because
 modification has been made.

   If you convey an object code work under this section in, or with, or
 specifically for use in, a User Product, and the conveying occurs as
 part of a transaction in which the right of possession and use of the
 User Product is transferred to the recipient in perpetuity or for a
 fixed term (regardless of how the transaction is characterized), the
 Corresponding Source conveyed under this section must be accompanied
 by the Installation Information.  But this requirement does not apply
 if neither you nor any third party retains the ability to install
 modified object code on the User Product (for example, the work has
 been installed in ROM).

   The requirement to provide Installation Information does not include a
 requirement to continue to provide support service, warranty, or updates
 for a work that has been modified or installed by the recipient, or for
 the User Product in which it has been modified or installed.  Access to a
 network may be denied when the modification itself materially and
 adversely affects the operation of the network or violates the rules and
 protocols for communication across the network.

   Corresponding Source conveyed, and Installation Information provided,
 in accord with this section must be in a format that is publicly
 documented (and with an implementation available to the public in
 source code form), and must require no special password or key for
 unpacking, reading or copying.


   7. Additional Terms.

   "Additional permissions" are terms that supplement the terms of this
 License by making exceptions from one or more of its conditions.
 Additional permissions that are applicable to the entire Program shall
 be treated as though they were included in this License, to the extent
 that they are valid under applicable law.  If additional permissions
 apply only to part of the Program, that part may be used separately
 under those permissions, but the entire Program remains governed by
 this License without regard to the additional permissions.

   When you convey a copy of a covered work, you may at your option
 remove any additional permissions from that copy, or from any part of
 it.  (Additional permissions may be written to require their own
 removal in certain cases when you modify the work.)  You may place
 additional permissions on material, added by you to a covered work,
 for which you have or can give appropriate copyright permission.

   Notwithstanding any other provision of this License, for material you
 add to a covered work, you may (if authorized by the copyright holders of
 that material) supplement the terms of this License with terms:

     a) Disclaiming warranty or limiting liability differently from the
     terms of sections 15 and 16 of this License; or

     b) Requiring preservation of specified reasonable legal notices or
     author attributions in that material or in the Appropriate Legal
     Notices displayed by works containing it; or

     c) Prohibiting misrepresentation of the origin of that material, or
     requiring that modified versions of such material be marked in
     reasonable ways as different from the original version; or

     d) Limiting the use for publicity purposes of names of licensors or
     authors of the material; or

     e) Declining to grant rights under trademark law for use of some
     trade names, trademarks, or service marks; or

     f) Requiring indemnification of licensors and authors of that
     material by anyone who conveys the material (or modified versions of
     it) with contractual assumptions of liability to the recipient, for
     any liability that these contractual assumptions directly impose on
     those licensors and authors.

   All other non-permissive additional terms are considered "further
 restrictions" within the meaning of section 10.  If the Program as you
 received it, or any part of it, contains a notice stating that it is
 governed by this License along with a term that is a further
 restriction, you may remove that term.  If a license document contains
 a further restriction but permits relicensing or conveying under this
 License, you may add to a covered work material governed by the terms
 of that license document, provided that the further restriction does
 not survive such relicensing or conveying.

   If you add terms to a covered work in accord with this section, you
 must place, in the relevant source files, a statement of the
 additional terms that apply to those files, or a notice indicating
 where to find the applicable terms.

   Additional terms, permissive or non-permissive, may be stated in the
 form of a separately written license, or stated as exceptions;
 the above requirements apply either way.


   8. Termination.

   You may not propagate or modify a covered work except as expressly
 provided under this License.  Any attempt otherwise to propagate or
 modify it is void, and will automatically terminate your rights under
 this License (including any patent licenses granted under the third
 paragraph of section 11).

   However, if you cease all violation of this License, then your
 license from a particular copyright holder is reinstated (a)
 provisionally, unless and until the copyright holder explicitly and
 finally terminates your license, and (b) permanently, if the copyright
 holder fails to notify you of the violation by some reasonable means
 prior to 60 days after the cessation.

   Moreover, your license from a particular copyright holder is
 reinstated permanently if the copyright holder notifies you of the
 violation by some reasonable means, this is the first time you have
 received notice of violation of this License (for any work) from that
 copyright holder, and you cure the violation prior to 30 days after
 your receipt of the notice.

   Termination of your rights under this section does not terminate the
 licenses of parties who have received copies or rights from you under
 this License.  If your rights have been terminated and not permanently
 reinstated, you do not qualify to receive new licenses for the same
 material under section 10.

   9. Acceptance Not Required for Having Copies.

   You are not required to accept this License in order to receive or
 run a copy of the Program.  Ancillary propagation of a covered work
 occurring solely as a consequence of using peer-to-peer transmission
 to receive a copy likewise does not require acceptance.  However,
 nothing other than this License grants you permission to propagate or
 modify any covered work.  These actions infringe copyright if you do
 not accept this License.  Therefore, by modifying or propagating a
 covered work, you indicate your acceptance of this License to do so.

   10. Automatic Licensing of Downstream Recipients.

   Each time you convey a covered work, the recipient automatically
 receives a license from the original licensors, to run, modify and
 propagate that work, subject to this License.  You are not responsible
 for enforcing compliance by third parties with this License.

   An "entity transaction" is a transaction transferring control of an
 organization, or substantially all assets of one, or subdividing an
 organization, or merging organizations.  If propagation of a covered
 work results from an entity transaction, each party to that
 transaction who receives a copy of the work also receives whatever
 licenses to the work the party's predecessor in interest had or could
 give under the previous paragraph, plus a right to possession of the
 Corresponding Source of the work from the predecessor in interest, if
 the predecessor has it or can get it with reasonable efforts.

   You may not impose any further restrictions on the exercise of the
 rights granted or affirmed under this License.  For example, you may
 not impose a license fee, royalty, or other charge for exercise of
 rights granted under this License, and you may not initiate litigation
 (including a cross-claim or counterclaim in a lawsuit) alleging that
 any patent claim is infringed by making, using, selling, offering for
 sale, or importing the Program or any portion of it.


   11. Patents.

   A "contributor" is a copyright holder who authorizes use under this
 License of the Program or a work on which the Program is based.  The
 work thus licensed is called the contributor's "contributor version".

   A contributor's "essential patent claims" are all patent claims
 owned or controlled by the contributor, whether already acquired or
 hereafter acquired, that would be infringed by some manner, permitted
 by this License, of making, using, or selling its contributor version,
 but do not include claims that would be infringed only as a
 consequence of further modification of the contributor version.  For
 purposes of this definition, "control" includes the right to grant
 patent sublicenses in a manner consistent with the requirements of
 this License.

   Each contributor grants you a non-exclusive, worldwide, royalty-free
 patent license under the contributor's essential patent claims, to
 make, use, sell, offer for sale, import and otherwise run, modify and
 propagate the contents of its contributor version.
   In the following three paragraphs, a "patent license" is any express
 agreement or commitment, however denominated, not to enforce a patent
 (such as an express permission to practice a patent or covenant not to
 sue for patent infringement).  To "grant" such a patent license to a
 party means to make such an agreement or commitment not to enforce a
 patent against the party.

   If you convey a covered work, knowingly relying on a patent license,
 and the Corresponding Source of the work is not available for anyone
 to copy, free of charge and under the terms of this License, through a
 publicly available network server or other readily accessible means,
 then you must either (1) cause the Corresponding Source to be so
 available, or (2) arrange to deprive yourself of the benefit of the
 patent license for this particular work, or (3) arrange, in a manner
 consistent with the requirements of this License, to extend the patent
 license to downstream recipients.  "Knowingly relying" means you have
 actual knowledge that, but for the patent license, your conveying the
 covered work in a country, or your recipient's use of the covered work
 in a country, would infringe one or more identifiable patents in that
 country that you have reason to believe are valid.

   If, pursuant to or in connection with a single transaction or
 arrangement, you convey, or propagate by procuring conveyance of, a
 covered work, and grant a patent license to some of the parties
 receiving the covered work authorizing them to use, propagate, modify
 or convey a specific copy of the covered work, then the patent license
 you grant is automatically extended to all recipients of the covered
 work and works based on it.

   A patent license is "discriminatory" if it does not include within
 the scope of its coverage, prohibits the exercise of, or is
 conditioned on the non-exercise of one or more of the rights that are
 specifically granted under this License.  You may not convey a covered
 work if you are a party to an arrangement with a third party that is
 in the business of distributing software, under which you make payment
 to the third party based on the extent of your activity of conveying
 the work, and under which the third party grants, to any of the
 parties who would receive the covered work from you, a discriminatory
 patent license (a) in connection with copies of the covered work
 conveyed by you (or copies made from those copies), or (b) primarily
 for and in connection with specific products or compilations that
 contain the covered work, unless you entered into that arrangement,
 or that patent license was granted, prior to 28 March 2007.

   Nothing in this License shall be construed as excluding or limiting
 any implied license or other defenses to infringement that may
 otherwise be available to you under applicable patent law.


   12. No Surrender of Others' Freedom.

   If conditions are imposed on you (whether by court order, agreement or
 otherwise) that contradict the conditions of this License, they do not
 excuse you from the conditions of this License.  If you cannot convey a
 covered work so as to satisfy simultaneously your obligations under this
 License and any other pertinent obligations, then as a consequence you may
 not convey it at all.  For example, if you agree to terms that obligate you
 to collect a royalty for further conveying from those to whom you convey
 the Program, the only way you could satisfy both those terms and this
 License would be to refrain entirely from conveying the Program.

   13. Use with the GNU Affero General Public License.

   Notwithstanding any other provision of this License, you have
 permission to link or combine any covered work with a work licensed
 under version 3 of the GNU Affero General Public License into a single
 combined work, and to convey the resulting work.  The terms of this
 License will continue to apply to the part which is the covered work,
 but the special requirements of the GNU Affero General Public License,
 section 13, concerning interaction through a network will apply to the
 combination as such.

   14. Revised Versions of this License.

   The Free Software Foundation may publish revised and/or new versions of
 the GNU General Public License from time to time.  Such new versions will
 be similar in spirit to the present version, but may differ in detail to
 address new problems or concerns.

   Each version is given a distinguishing version number.  If the
 Program specifies that a certain numbered version of the GNU General
 Public License "or any later version" applies to it, you have the
 option of following the terms and conditions either of that numbered
 version or of any later version published by the Free Software
 Foundation.  If the Program does not specify a version number of the
 GNU General Public License, you may choose any version ever published
 by the Free Software Foundation.

   If the Program specifies that a proxy can decide which future
 versions of the GNU General Public License can be used, that proxy's
 public statement of acceptance of a version permanently authorizes you
 to choose that version for the Program.

   Later license versions may give you additional or different
 permissions.  However, no additional obligations are imposed on any
 author or copyright holder as a result of your choosing to follow a
 later version.

   15. Disclaimer of Warranty.

   THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
 APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
 HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
 OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
 IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
 ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

   16. Limitation of Liability.

   IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
 WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
 THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
 GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
 USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
 DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
 PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
 EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
 SUCH DAMAGES.

   17. Interpretation of Sections 15 and 16.

   If the disclaimer of warranty and limitation of liability provided
 above cannot be given local legal effect according to their terms,
 reviewing courts shall apply local law that most closely approximates
 an absolute waiver of all civil liability in connection with the
 Program, unless a warranty or assumption of liability accompanies a
 copy of the Program in return for a fee.

                      END OF TERMS OF USE

"""
    
    # ________________________________
    #     Pages.database_path_name_to_import is created in eeg_weaver_multiple_sqlite
    #     as variable to path_file been imported
    database_path_name_to_import = ''
