# pyinstaller needs this function to create a path for images of icons etc
# https://stackoverflow.com/questions/51264169/pyinstaller-add-folder-with-images-in-exe-file

import os
import sys

# def resource_path(relative_path):
#     config_name = "EEG_weaver_Reporter_1.2"
#     # determine if application is a script file or frozen exe
#     if getattr(sys, 'frozen', False):
#         application_path = os.path.dirname(sys.executable)
#     elif __file__:
#         application_path = os.path.dirname(__file__)
#
#     config_path = os.path.join(application_path, config_name)

# def resource_path(relative_path):
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)
#
# def resource_path(relative):
#     return os.path.join(
#         os.environ.get(
#             "_MEIPASS2",
#             os.path.abspath(".")
#         ),
#         relative
#     )
#     return os.path.join(base_path, relative_path)

# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         # base_path = sys._MEIPASS + "\EEG_weaver_Reporter_1.2" nao funciona
#         # base_path = sys._MEIPASS #nao funciona
#         # base_path = os.path.realpath(__file__)
#
#         base_path = Path(sys.executable).parent  #funciona parcialmente
#         print(base_path)
#     except Exception:
#         base_path = os.path.abspath(".")
#         # base_path = os.getcwd()
#         print(base_path)
#     return os.path.join(base_path, relative_path)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
