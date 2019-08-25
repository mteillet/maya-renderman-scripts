import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMaya as OM

####    This scripts reloads the alembic files with a relative path     ####

# Variables

n = 0
repathCount = 0
currentWorkspace = cmds.workspace( q=True, rd=True)


#Select All objects and saves it to a list
cmds.select(all = True)
AllScene = cmds.ls(selection =True)
print(AllScene)
oldAlembicNodes = []


#Loop checking if item in selection have Alembic attribute
for i in AllScene:
    objType = cmds.objectType(AllScene[n])

    #This can print all the object types on the scene selection:

    #print (objType)

    # Loop getting the alembic file path if i is an Alembic node
    # Abc file name attribute = u'abc_File'
    if "AlembicNode" in (objType):
        print("FOUND ALEMBIC NODE:")
        print(AllScene[n])

        

        #Finds the current Alembic path
        currentAbcPath = cmds.getAttr(AllScene[n] + ".abc_File")
        print("CURRENT ALEMBIC PATH IS :")
        print(currentAbcPath)


        #Check if cache/alembic is in the current Alembic path
        if "cache/alembic" in currentAbcPath:
            print("cache/alembic is in the current Alembic Path")

            #Stores the current alembic node into a list in order do delete it at the end of the script
            #Therefore avoiding duplicates with the new alembic nodes with the project path 
            oldAlembicNodes.append(AllScene[n])


            #Find where cache/alembic is
            PathIndex = currentAbcPath.find("cache/alembic")

            #Removes everything before cache/alembic
            NewAbcPath = (currentAbcPath[PathIndex:])

            #Adds the current workspace to the newAbcPath
            NewAbcPath = (currentWorkspace) + (NewAbcPath)

            print (NewAbcPath)

            #Clear selection before merging the Alembic nodes
            cmds.select(clear = True)

            #Re - imports the Alembic as a merge
            abcImportCommand = ('AbcImport -mode import -connect "/" ') + ('"') + (NewAbcPath) + ('"')
            print(abcImportCommand)

            # Execute the python abcImportCommand as mel
            mel.eval(abcImportCommand)

            repathCount += 1
    
         
    
    n += 1

print("---- DONE ----")
print((repathCount)," alembic paths were reloaded as relative to your current scene project.")

cmds.delete(oldAlembicNodes)
print("These old Alembic nodes were deleted:")
print(oldAlembicNodes)
