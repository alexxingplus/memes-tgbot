from key import firstpass, secondpass

def addStringLine(id, tags, photoID):
    tags = tags.replace("\n", " ")
    readFile = open("memes.txt")
    string_list = readFile.readlines()
    readFile.close()
    writeFile = open("memes.txt", "w")
    newFileContents = "".join(string_list)
    newFileContents += "{}{} {} {}{}\n".format(id, firstpass, tags, secondpass, photoID)
    writeFile.write(newFileContents)
    writeFile.close()

def getPhotoIDs(string):
    string = string.replace(";", ",")
    string = string.replace(".", ",")
    string = string.replace(",", " ")
    string = string.upper()
    tags = []
    ids = []
    while (" " in string):
        index = string.index(" ")
        tags.append(string[:index])
        string = string[index+1:]
    tags.append(string)
    
    readFile = open("memes.txt")
    string_list = readFile.readlines()
    readFile.close()
    for i in range(0, len(string_list)):
        memeDescripiton = string_list[i].upper().replace(",", " ")
        memeDescripiton = memeDescripiton.replace(";"," ")
        memeDescripiton = memeDescripiton.replace(".", " ")
        for j in range (0, len(tags)):
            if " {} ".format(tags[j]) in memeDescripiton:
                index = string_list[i].index(secondpass)
                ids.append(string_list[i][index + 10:].replace("\n", ""))
                break
    return ids

def addAdmin(id):
    readFile = open("admins.txt")
    string_list = readFile.readlines()
    readFile.close()
    writeFile = open("admins.txt", "w")
    newFileContents = "".join(string_list)
    newFileContents += "{}\n".format(id)
    writeFile.write(newFileContents)
    writeFile.close()

def deleteAdmin(id):
    input = str(id) + "\n"
    readFile = open("admins.txt")
    string_list = readFile.readlines()
    readFile.close()
    for i in range(0, len(string_list)):
        if (string_list[i] == input):
            string_list[i] = ""
    writeFile = open("admins.txt", "w")
    newFileContents = "".join(string_list)
    writeFile.write(newFileContents)
    writeFile.close()
    

def getAdminList():
    readFile = open("admins.txt")
    string_list = readFile.readlines()
    readFile.close()
    return string_list






