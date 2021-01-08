import os,glob
folder_path = os.getcwd()


for filename in glob.glob(os.path.join(folder_path, '*.eaf')):
    with open(filename) as file: #open file
        data = file.read()
        x = data.find("Attention") #find Attention sub
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
        finallist = [] #our last output with the body parts
        for index, items in enumerate(hitlist): #for all entries in our hitlist
            current = hitlist[index][hitlist[index].find("(")+1:hitlist[index].find(")")]
            if (current != prev): #if a new entry is found
                #print(hitlist[index][hitlist[index].find("(")+1:hitlist[index].find(")")])
                finallist.append(items.split("(")[0]) #add body part to list
            prev = current
        hitlist[:] = []
        print(finallist)
        test = open(filename.rstrip(".eaf")+".txt","w+")
        for items in finallist:
            test.write(items + "\n")
        file.close()

        finallist[:] = []

        