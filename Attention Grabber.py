import os,glob
import PySimpleGUI as sg
import time
folder_path = os.getcwd()

def parserchar(location):
    fulllist = [] #our full list
    for filename in glob.glob(os.path.join(location, '*.eaf')):
        with open(filename) as file: #open file
            data = file.read()
            keyword = "Attention"
            before_keyword, keyword, after_keyword = data.partition(keyword)
            tier = after_keyword.split("\n") #Split into lines 
            hitlist = []
            for lines in tier:
                keyword = "<ANNOTATION_VALUE>"
                if keyword in lines:
                    temp = lines.split("<ANNOTATION_VALUE>") #removes <ANNOTATION_VALUE> from string
                    new = temp[1].rstrip("</ANNOTATION_VALUE>") #removes </ANNOTATION_VALUE> from string
                    hitlist.append(new)

            prev = ""
            current = ""
            for index, items in enumerate(hitlist): #for all entries in our hitlist
                current = hitlist[index][hitlist[index].find("(")+1:hitlist[index].find(")")]
                if (current != prev): #if a new entry is found
                    #print(hitlist[index][hitlist[index].find("(")+1:hitlist[index].find(")")])
                    fulllist.append(items.split("(")[0]) #add body part to list
                prev = current
            hitlist[:] = []
        file.close()
    return fulllist

def writerchar(outputname, fulllist):
    test = open(outputname+"_character.txt","w+")
    for items in fulllist:
        test.write(items + "\n")

def parserfull(location):
    hitlist = []
    for filename in glob.glob(os.path.join(location, '*.eaf')):
        with open(filename) as file: #open file
            data = file.read()
            keyword = "Attention"
            before_keyword, keyword, after_keyword = data.partition(keyword)
            tier = after_keyword.split("\n") #Split into lines
            for lines in tier:
                keyword = "<ANNOTATION_VALUE>"
                if keyword in lines:
                    temp = lines.split("<ANNOTATION_VALUE>") #removes <ANNOTATION_VALUE> from string
                    new = temp[1].rstrip("</ANNOTATION_VALUE>") #removes </ANNOTATION_VALUE> from string
                    hitlist.append(new.split("(")[0])
        file.close()
    return hitlist

def writerfull(outputname, tier):
    test = open(outputname+"_full.txt","w+")
    for items in tier:
        test.write(items + "\n")

def driver(task, location,outputname):
    if task == "New character":
        t = parserchar(location)
        writerchar(outputname, t)
    elif task == "Full attention":
        t = parserfull(location)
        writerfull(outputname, t)

def gui():
    sg.theme("Reddit")
    layout = [[sg.InputCombo(('New character', 'Full attention'), size=(20, 1))],[sg.Button("Submit")]] #creates combobox for values
    window = sg.Window('Attention grabber', layout, size=(300,100))

    while True:
        event, task = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            break
        elif event == "Submit":
            location = sg.popup_get_folder("Please input your desired folder.", title="Attention grabber")
            outputname = sg.popup_get_text("Please input the name of the output.", title="Attention grabber") 
            try:
                driver(task[0], location,outputname)
                sg.popup_timed("Success",auto_close_duration=1) 
            except:
                sg.popup_timed("Error",auto_close_duration=2) 
                pass

gui()