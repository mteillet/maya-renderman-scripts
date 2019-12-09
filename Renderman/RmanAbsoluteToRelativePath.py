import maya.cmds as cmds

####    This script goes through all the pxrTexture nodes of a scene, checks if their filepath contains the project path and if so change it to <ws> (relative path) 

#selecting all dependency nodes in the scene
cmds.select(adn = True)

#Storing all nodes in a list and printing it
Allnodes = cmds.ls(selection = True)


# Variables for the loop
n = 0
modifiedTextures = 0
failCount = 0
PxrTextureList = []
PxrFailList = []
currentWorkspace = cmds.workspace( q=True, rd=True)

#Checking object type
for i in Allnodes:
    objType = cmds.objectType(Allnodes[n])    

    print (objType)

    # If object type is pixar texture, append it to a new list
    if objType == "PxrTexture":
        # Set the current attribute to ThePxrTexture.filename
        currentAttribute = Allnodes[n] + ".filename"

        # Adds this PxrTextureName to a list
        PxrTextureList.append(Allnodes[n])
        # Call and store the filename indicated on the PxrTexture
        checkAttribute = cmds.getAttr(currentAttribute)

        # Check if the filename contains the current Worskpace path
        if currentWorkspace in checkAttribute:
            print(checkAttribute)
            
            #Replace the workspace path by <ws>/ and stores it as a new string
            newAttribute = checkAttribute.replace(currentWorkspace, "<ws>/")
            print("changed to :")
            print(newAttribute)

            #Sets the filename attribute to the newAttribute
            cmds.setAttr(currentAttribute, newAttribute, type = "string")

            #Adds one to the modified textures counter
            modifiedTextures += 1

            #check if filenames were updated
            checkUpdate = cmds.getAttr(currentAttribute)
            if checkUpdate == checkAttribute:
                print("FAILED")
                failCount += 1
                #Add the current node to the fail list
                PxrFailList.append(Allnodes[n])
        

    
    n += 1

#List containing the PxrTexture Node Names
print("checked these PxrTexture nodes:")
print(PxrTextureList)

#Select the PxrTexture nodes
cmds.select(PxrTextureList)

#Prints the number of texture path changes
print ("---- DONE ----")
modifiedTextures -= failCount

print (str(modifiedTextures) + " texture paths were changed to relative(s).")
print (str(failCount) + " texture paths could not be changed.")

if failCount > 0 :
    print ("The filepaths of these might not have been changed because they are still set on your previous project location.  If not, try closing and reopening Maya.")
    print ("Filepath of the following nodes could not be changed:")
    print (PxrFailList)
