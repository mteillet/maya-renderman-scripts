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
            else:
                pass
            current += 1
    print("Found a total of " + str(len(fileList)) + " matches")
    return(fileList)

def quietFiles(studentFiles):
    current = 0
    
    for i in studentFiles:
        fileToOpen = studentFiles[current]
        
        # Opening the file and storing the lines in a list
        f = open(fileToOpen, "r")
        lines = f.readlines()
        f.close
        
        # checking if the 13th line is student version
        checkMessage = ("Checking the file :" + str(fileToOpen))
        print(checkMessage)
        licenseMessage = 'fileInfo "license" "student";'
        subcurrent = 0
        for i in lines:
            if lines[subcurrent].startswith(licenseMessage):
                # Check the line
                print("StudentVersion detected")
                del lines[subcurrent] # Remove the line
                
                  
            else:
                pass
                
            subcurrent += 1
        
        # Reopen the file to write without the student line
        f = open(fileToOpen, "w")
        f.writelines(lines)
        f.close()
              
        
        current += 1
    

if __name__ == "__main__":
    main()