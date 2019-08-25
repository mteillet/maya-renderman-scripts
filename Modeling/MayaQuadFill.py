import maya.cmds as cmds
import maya.mel as mel

####    This script fills the selected edge loop with quads     ####


#   Selected Variables
#Edges
edgeSelect = cmds.polySelect(edgeLoop = True)
#Object
curentObject = cmds.ls(selection = True, objectsOnly = True, shortNames = True)

print(curentObject)
print(edgeSelect)

# select the other edge loops to close the loop

selectEdgeLoop = "select -add "+ str(curentObject) + ".e" + str(edgeSelect)
print(selectEdgeLoop)

mel.eval(selectEdgeLoop)

"""
for i in edgeSelect:
    cmds.select((curentObject) + ".e" + str(i))
    select -add pSphere1.e[320:339] ;
"""


