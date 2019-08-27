import maya.cmds as cmds
import maya.mel as mel
import re

####    This script fills the selected edge loop with quads     ####

####################################################
####                MAYA WINDOW                 ####
####################################################

originalSelection = cmds.ls(orderedSelection=True, flatten=True)
originaldivision = len(originalSelection)/8


GridFill = cmds.window( title="Grid Fill", iconName='Grid Fill', widthHeight=(140, 90), toolbox = True)
cmds.rowColumnLayout( numberOfColumns=2, columnWidth = [(1,75),(2,60)])
cmds.text( label="Offset" )
offset = cmds.intField(changeCommand = 'userInput()', value = 0)
cmds.text( label="Divisions" )
divisions = cmds.intField(changeCommand = 'userInput()', value = originaldivision)

cmds.separator(h=20, style = "none")
cmds.separator(h=20, style = "none")
cmds.separator(h=10, style = "none")

cmds.button( label = "Grid Fill", command = 'gridFill()')

cmds.showWindow( window )



####################################################
####               Grid fill code               ####
####################################################

def userInput():    
    #Get the inputs from offset and divisions
    edgeOffset = cmds.intField(offset, q=1, v=1)
    edgeDivision = cmds.intField(divisions, q=1, v=1)
    print("Edge offset is : " + str(edgeOffset))
    print("Bridge Division is : " + str(edgeDivision))    
    return(edgeOffset)
    return(edgeDivision)


def gridFill():
    userOffset = cmds.intField(offset, q=1, v=1)
    userDivision = cmds.intField(divisions, q=1, v=1)
    
    print("Start")  

    #Object
    curentObject = cmds.ls(selection = True, objectsOnly = True, shortNames = True)

    #Get short name of current object for the polySelect fonction
    shortObject = str(curentObject).replace("Shape","").replace("u'","").replace("'","").replace("[","").replace("]","")
    firstBridgeBorder = []
    secondBridgeBorder = []
    i = 0


    #Ordering the number of edges
    orderedEdges = cmds.ls(orderedSelection=True, flatten=True)
    print(orderedEdges)
    
    #Reorder the selection based on the offset input by user
    ReorderedEdges = orderedEdges[userOffset:] + orderedEdges[:userOffset]
    print("This is the new edges order following the offset " + str(ReorderedEdges))
    
    #Splitting the list in 2
    firstHalf = ReorderedEdges[:len(ReorderedEdges)//2]
    secondHalf = ReorderedEdges[len(ReorderedEdges)//2:]
    
    print("firstHalf")
    print((firstHalf))
    print("firstBridgeBorder")
    
    firstBridgeBorder = firstHalf
    secondBridgeBorder = secondHalf
    thirdBridgeBorder = []
    fourthBridgeBorder = []

    # Removes from the bridges border the number of divisions needed from both bridge borders
    # Also resets i at the end of while loop

    while i < userDivision:
        #Get the last items which will be unselected in order to make the last bridges easier
        thirdBridgeBorder = [firstBridgeBorder[len(firstBridgeBorder)-1], firstBridgeBorder[0]]
        del firstBridgeBorder[len(firstBridgeBorder)-1]
        del firstBridgeBorder[0]
        i += 1

    i = 0

    while i < userDivision:
        #Get the last items which will be unselected in order to make the last bridges easier
        fourthBridgeBorder = [secondBridgeBorder[len(secondBridgeBorder)-1], secondBridgeBorder[0]]  
        del secondBridgeBorder[len(secondBridgeBorder)-1]
        del secondBridgeBorder[0]
        i += 1

    i = 0
    
    
    cmds.select(clear = True)
    cmds.select(firstBridgeBorder, secondBridgeBorder, add = True)
    
    if userDivision % 2 == 0:
        cmds.polyBridgeEdge(divisions = (userDivision+1))
        
    else:
        cmds.polyBridgeEdge(divisions = (userDivision+2))




    ##############################
    #Filling the last two bridges#
    ##############################
    
    cmds.select(clear = True)
    cmds.select(thirdBridgeBorder[0], add = True)
    
    cmds.polySelectSp(loop=True)
    
    cmds.select(thirdBridgeBorder[0], fourthBridgeBorder[1], add = True, toggle = True)
    
    cmds.polyBridgeEdge(divisions=0)
    
        
    cmds.select(clear = True)
    cmds.select(thirdBridgeBorder[1], add = True)
    
    cmds.polySelectSp(loop=True)
    
    cmds.select(thirdBridgeBorder[1], fourthBridgeBorder[0], add = True, toggle = True)
    
    cmds.polyBridgeEdge(divisions=0)
    
#### Need to redefine the way divisions are calculated (works well with 4 and 5, but not with 1, 2, 3, 6, 7, etc...)