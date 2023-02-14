import dearpygui.dearpygui as dpg #pip install dearpygui
import cv2 #pip install opencv-python
import os
import pandas as pd
import cv2 #pip install opencv-python
import easyocr

width1, height1, channels1, data1 = dpg.load_image("src/dory.jpg")
width2, height2, channels2, data2 = dpg.load_image("src/sishik.jpg")
def_width, def_height, def_channels, def_data = dpg.load_image("src/default.jpg")

Langs = ['en','ru']
selected_file = None
selected_lang = 'en' #set as default to find eng
dpg.create_context()


def callback(sender, data): #OK button
    global selected_file
    selected_file = str(data['selections'])
    index = selected_file.find("\': '")
    selected_file = selected_file[index+4:-2]    
    dpg.set_value("selected", ("Selected file: " + selected_file))


def selectLanguage(seder):
    val = dpg.get_value(seder)
    global selected_lang
    selected_lang = val

def proc(path, language):
    if(path == None): 
        dpg.set_value("ans", "File is not selected!")
        return
    dpg.set_value("ans", "Converting image to a text...")    
    img = cv2.imread(path)    
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except: 
        dpg.set_value("ans", "Error! Selected type is not an image.")
        dpg.set_value("img", data1)
        dpg.set_value("status", "\t\t\t\tOops...\nDory forgot how to read(")
    noise = cv2.medianBlur(gray, 5)

    thresh = cv2.threshold(noise, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    try:
        reader = easyocr.Reader([language])
        result = reader.readtext(gray)
        TextFromImg = (pd.DataFrame(result))[1]
    except: 
        dpg.set_value("ans", "")
        dpg.set_value("img", data1)
        dpg.set_value("status", "\t\t\t\tOops...\nDory forgot how to read(")
    str_res = ''
    for i in TextFromImg:
        str_res += str(i) + '\n'

    dpg.set_value("img", data2)
    dpg.set_value("status", "\t\t\t\tYay!\nAn experienced detective worked well and recognized text on the photo.")    
    dpg.set_value("ans", str_res)


with dpg.file_dialog(directory_selector=False, height=300, width=600, show=False, callback=callback, tag="file_dialog_id", file_count=1):
    dpg.add_file_extension(".*")


with dpg.texture_registry(show=False):
    dpg.add_dynamic_texture(width=width2, height=height2, default_value = def_data, tag="img") 


def myfunc(sender):
    index = results.index(dpg.get_value(sender))
    cv2.imshow(f"{dpg.get_value(sender)}", drawed[index])
    cv2.waitKey(0)     


with dpg.theme() as new_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (238,136,204,255)) #(r,g,b,a) pink
        dpg.add_theme_color(dpg.mvThemeCol_Text, (21,21,21,255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (223,223,223,255))
        dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (223,223,223,255))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (223,223,223,255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (141,249,217,255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (141,249,217,255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (141,249,217,255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (249,141,174,255))
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (254,178,201,255))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (254,178,201,255))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)


with dpg.window(label="TextConverter", width=800, height=450, tag="primary"):
    dpg.add_button(label="File Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_text(tag="selected", default_value="Selected file: None")
    dpg.add_listbox(tag="LangSelector", items=Langs, num_items=2, callback=selectLanguage)
    dpg.add_image(texture_tag="img", width=80, height=80)
    dpg.add_text(tag="status")
    dpg.add_button(label="Convert to text", callback=lambda: proc(selected_file, selected_lang))
    dpg.add_text(tag="ans")


dpg.bind_theme(new_theme)
dpg.create_viewport(title='Window1', height=450, width=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary", True)
dpg.start_dearpygui()
dpg.destroy_context()