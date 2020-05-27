import maya.cmds as cmds
import os

####        The goal of this script is to remove all of the student messages from the references of a project       ####

def main():
    currentProj = getCurrentProject()
    studentFiles = checkMayaFiles(currentProj)
    quietFiles(studentFiles)
    

def getCurrentProject():
    currentProj = cmds.workspace( q=True, rootDirectory=True )
    return(currentProj)

def checkMayaFiles(currentProj):
    fileList = []
    print(currentProj)
    for r, d, f in os.walk(currentProj):
        current = 0
        for i in f:
            if f[current].endswith(".ma"):
                tempVar = str(r) + "/" + str(f[current])
                tempVar = tempVar.replace("\\", "/")
                fileList.append(tempVar)
                print("Match")
            else:
                pass
    print("Found a total of " + str(len(fileList)) + " matches")
    return(fileList)

def quietFiles(studentFiles):
    current = 0
    for i in studentFiles:
        with f as file 
        print("test")
    

if __name__ == "__main__":
    main()