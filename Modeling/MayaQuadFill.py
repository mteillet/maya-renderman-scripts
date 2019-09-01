import maya.cmds as cmds
import maya.mel as mel
import math

####    This script fills the selected edge loop with quads     ####

####################################################
####                MAYA WINDOW                 ####
####################################################


####        Setting ordered selection as true in the preferences        ####

cmds.selectPref(trackSelectionOrder=True)


####        Getting the original selection          ####
originalSelection = (cmds.ls(selection = True, flatten = True))


####        User Inputs         ####
userOffset = 0
userDivision = len(originalSelection)/8

#####       Selection changes       #### 

i = 0
newSelection = []
selectionGrowList = []



mel.eval("invertSelection;")
invertedOriginal = (cmds.ls(selection = True, flatten = True))

cmds.select(clear = True)


# Get the first edge of the border selected
cmds.select(originalSelection[userOffset])

# Grow selection until the whole border is selected
while i < (len(originalSelection)/2):
    mel.eval('select `ls -sl`;PolySelectTraverse 1;select `ls -sl`;')
    selectionGrowList.append(cmds.ls(selection = True, flatten = True))
    i += 1

# Finding the middle of the list<
midHalf = (i/2)-1
midSubstract = (i/2)-2

# Reset i value
i = 0


####        Selecting the two opposite edges suites         ####


# Selecting the first two opposite edges
cmds.select(clear = True)
cmds.select(selectionGrowList[midHalf])
cmds.select(selectionGrowList[midSubstract], deselect = True)


# Growing the selection by the number of user divisions
while i < userDivision:
    cmds.polySelectConstraint( pp=1 )
    i += 1 
cmds.select(invertedOriginal, deselect = True)
# reset i
i = 0


####        Getting the number of division on the bridge           ####
firstBridge = cmds.ls(selection = True, flatten = True)
# The number of divisions needed is equal to the remaining edges on the original edge loop divided by 2 and minus 3
divisionsNeeded = (len(originalSelection) - len(firstBridge))/2 - 3

# Bridging the first loop and dividing it
cmds.polyBridgeEdge(divisions=divisionsNeeded)


# now need to find a way to select the remaining edge loops in order to bridge them
# The shrink selection around loop should work
# Should find indications in the cmds.polySelectConstraint( pp=1 ) documentation

# Get the first edge of the last two bridges
cmds.select(clear = True)
cmds.select(originalSelection)
cmds.select( firstBridge, deselect = True )

otherBridge = cmds.ls(selection = True, flatten = True)

# Minus border edges
mel.eval('select `ls -sl`;PolySelectTraverse 6; select `ls -sl`;')
actualBridge = cmds.ls(selection = True, flatten = True)


#Getting border edges to remove for the last two bridges
cmds.select(clear = True)
cmds.select(otherBridge)
cmds.select(actualBridge, deselect = True)
minusBridge = cmds.ls(selection = True, flatten = True)



#####        Selecting the remaining bridges           ####


cmds.select(clear = True)
cmds.select(otherBridge[0])
# Selecting the whole loop
cmds.polySelectSp(loop=True)
secondBridge = cmds.ls(selection = True, flatten = True)

# Deselect the minusBridge
cmds.select(minusBridge, deselect = True)

cmds.polyBridgeEdge(divisions=0)

#LastBridge
cmds.select(clear = True)
cmds.select(otherBridge)
cmds.select(secondBridge, deselect = True)

# Selecting the whole loop
cmds.polySelectSp(loop=True)

# Deselect the minusBridge
cmds.select(minusBridge, deselect = True)

cmds.polyBridgeEdge(divisions=0)

"""



#originalSelection = cmds.ls(orderedSelection=True, flatten=True)
originaldivision = len(originalSelection)/8
maxDiv = ((len(originalSelection)/4)-1)

GridFill = cmds.window( title="Grid Fill", iconName='Grid Fill', widthHeight=(140, 120), toolbox = True)
cmds.rowColumnLayout( numberOfColumns=2, columnWidth = [(1,75),(2,60)])
cmds.text( label="Offset" )
offset = cmds.intField(changeCommand = 'userInput()', value = 0)
cmds.text( label="Add/Reduce" )
divisions = cmds.intField(changeCommand = 'userInput()', value = originaldivision, minValue = 2, maxValue = maxDiv)
cmds.text( label="Relax" )
relaxChoice = cmds.optionMenu( label='', changeCommand='userInput()' )
cmds.menuItem( label='Yes' )
cmds.menuItem( label='No' )

cmds.separator(h=20, style = "none")
cmds.separator(h=20, style = "none")
cmds.separator(h=10, style = "none")
cmds.separator(h=10, style = "none")

cmds.button( label = "Grid Fill", command = 'gridFill()')

cmds.showWindow( GridFill )



####################################################
####               Grid fill code               ####
####################################################

def userInput():    
    #Get the inputs from offset and divisions
    edgeOffset = cmds.intField(offset, q=1, v=1)
    edgeDivision = cmds.intField(divisions, q=1, v=1)
    relax = cmds.optionMenu(relaxChoice, q=1, v=1)
    print("Edge offset is : " + str(edgeOffset))
    print("Bridge Division is : " + str(edgeDivision))
    print(relax)    
    return(edgeOffset)
    return(edgeDivision)


def gridFill():
    userOffset = cmds.intField(offset, q=1, v=1)
    userDivision = cmds.intField(divisions, q=1, v=1)
    relax = cmds.optionMenu(relaxChoice, q=1, v=1)
    
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
    
    
    ### Select all current vertices
    
    
    mel.eval("invertSelection;")
    cmds.polyListComponentConversion(fromEdge = True, toVertex = True)
    verticesForExclusion = cmds.polyListComponentConversion(fromEdge = True, toVertex = True)
    cmds.select(verticesForExclusion)
    

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
    


    ### FILLING THE FIRST TWO BRIDGES ####
    
    
    
    cmds.polyBridgeEdge(divisions = math.sqrt(pow(((2 * userDivision)-3), 2)))
    



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
    
    
    ####    Smooth the new created vertices with polyAverageVertex  ####
    if relax == "Yes":
        cmds.select(clear = True)
        mel.eval("setSelectMode components Components;")
        mel.eval("selectType -smp 0 -sme 0 -smf 0 -smu 0 -pv 1 -pe 0 -pf 0 -puv 0;")
        cmds.select(verticesForExclusion)
        mel.eval("invertSelection;")
        verticesForRelax = []
        verticesForRelax = cmds.ls(selection = True, flatten = True)
        cmds.polyAverageVertex( verticesForRelax, iterations = 100)
        mel.eval("selectType -smp 0 -sme 0 -smf 0 -smu 0 -pv 0 -pe 1 -pf 0 -puv 0;")
        
    cmds.select(clear = True)
    print("Gridd Fill Done")
    
    
# Still need to figure out how to get the original selection order right
# https://forums.cgsociety.org/t/return-selection-orderd-by-edge-loop-maya-api/1577329/3
# Could be a solution

"""