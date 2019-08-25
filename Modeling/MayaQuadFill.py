import maya.cmds as cmds
import maya.mel as mel

####    This script fills the selected edge loop with quads     ####


#   Selected Variables
#Edges
edgesSelected = cmds.ls(selection = True, shortNames = True)
#Object
curentObject = cmds.ls(selection = True, objectsOnly = True, shortNames = True)
#Get the number of selected edges
edgesNumber = cmds.polyEvaluate(edgeComponent = True)


print(curentObject)
print(edgesSelected)
print(edgesNumber)


#Deselecting the specified edges

