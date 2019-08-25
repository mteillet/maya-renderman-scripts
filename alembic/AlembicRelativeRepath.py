import maya.cmds as cmds
import maya.mel as mel

####    This scripts reloads the alembic files with a relative path     ####

# Variables

n = 0
currentWorkspace = cmds.workspace( q=True, rd=True)


#Select All objects and saves it to a list
cmds.select(all = True)
AllScene = cmds.ls(selection =True)
print(AllScene)


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
        
        #Re - imports the Alembic as a merge
        abcImportCommand = ('AbcImport -mode import -connect ') + ('"ObjectNeeded"') + " " + (currentAbcPath)
        print(abcImportCommand)
    
         
    
    n += 1


