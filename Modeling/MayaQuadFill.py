import maya.cmds as cmds
import maya.mel as mel
import math

####    This script fills the selected edge loop with quads     ####




originalSelection = (cmds.ls(selection = True, flatten = True))

# Check if we can run grid fill
if len(originalSelection) % 2 != 0:
    print("Selected loop needs to contain an even edges number")
    
if len(originalSelection) < 4:
    print("Selected loop needs to contain at least 4 edges")
    
# Define the original first bridge optimal number
if len(originalSelection) % 2 == 0:
    OptimalFirstBridge = ((len(originalSelection)/2)-4)
else :
    OptimalFirstBridge = ((len(originalSelection)/2)-3)
    


####                    !!!!            NEED TO REDEFINE HOW THE DIVISION INPUT WORKS             !!!!               ####
originaldivision = (((len(originalSelection) - OptimalFirstBridge - 4) / 2) - 1)




####################################################
####               Grid fill code               ####
####################################################

def newValue():
    cmds.undo()
    print("newGridFill")
    userInput()
    gridFill()


def userInput():    
    #Get the inputs from offset and divisions
    userOffset = cmds.intField(offsetBox, q=1, v=1)
    userDivision = cmds.intField(divisions, q=1, v=1)
    relax = cmds.optionMenu(relaxChoice, q=1, v=1)
    print("Edge offset is : " + str(userOffset))
    print("Bridge Division is : " + str(userDivision))
    print(relax)    
    return(userOffset)
    return(userDivision)


def gridFill():
    ####        Setting ordered selection as true in the preferences        ####

    cmds.selectPref(trackSelectionOrder=True)
    userOffset = cmds.intField(offsetBox, q=1, v=1)
    userDivision = cmds.intField(divisions, q=1, v=1)
    relax = cmds.optionMenu(relaxChoice, q=1, v=1)

    
    ####        Getting the original selection          ####
    originalSelection = (cmds.ls(selection = True, flatten = True))
    # Storing the number of vertices in order to be able to relax the new created ones
    cmds.select(clear = True)
    mel.eval("invertSelection;")
    cmds.polyListComponentConversion(fromEdge = True, toVertex = True)
    verticesForExclusion = cmds.polyListComponentConversion(fromEdge = True, toVertex = True)
    cmds.select(verticesForExclusion)

    cmds.select(originalSelection)


    #####       Selection changes       #### 

    i = 0
    selectionGrowList = []



    mel.eval("invertSelection;")
    invertedOriginal = (cmds.ls(selection = True, flatten = True))

    cmds.select(clear = True)


    # Get the first edge of the border selected
    cmds.select(originalSelection[userOffset+1])
    if len(originalSelection) % 4 == 0:
        mel.eval('select `ls -sl`;PolySelectTraverse 1;select `ls -sl`;')
        cmds.select(invertedOriginal, deselect = True)
        originalOddSelection = (cmds.ls(selection = True, flatten = True))
        cmds.select(clear = True)
        cmds.select(originalOddSelection[0], originalOddSelection[1])
        

    # Grow selection until the whole border is selected
    while i < (len(originalSelection)/2-1):
        mel.eval('select `ls -sl`;PolySelectTraverse 1;select `ls -sl`;')
        selectionGrowList.append(cmds.ls(selection = True, flatten = True))
        i += 1

    # Finding the two middle edges of the list
    midHalf = (i/2)
    midSubstract = (i/2)-2
    
    # Reset i value
    i = 0


    ####        Selecting the two opposite edges suites         ####


    # Selecting the first two opposite edges
    cmds.select(clear = True)
    cmds.select(selectionGrowList[midHalf])
    cmds.select(selectionGrowList[midSubstract], deselect = True)
    cmds.select(invertedOriginal, deselect = True)
    



    # Growing the selection by the number of user divisions
    while i < userDivision-4:
        mel.eval('select `ls -sl`;PolySelectTraverse 1;select `ls -sl`;')
        i += 1
    cmds.select(invertedOriginal, deselect = True)
    # reset i
    i = 0



    ####        Getting the number of division on the bridge           ####
    firstBridge = cmds.ls(selection = True, flatten = True)

    # The number of divisions needed is equal to the remaining edges on the original edge loop divided by 2 and minus 3
    divisionsNeeded = (len(originalSelection) - len(firstBridge) - 4)/2 - 1
    
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
    #Selecting a single edge from this selection, otherwise the polySelectSp(loop=True) does not work
    cmds.select(secondBridge, deselect = True)
    lastBridge = cmds.ls(selection = True, flatten = True)

    cmds.select(clear = True)
    cmds.select(lastBridge[0])

    # Selecting the whole loop
    cmds.polySelectSp(loop=True)



    # Deselect the minusBridge
    cmds.select(minusBridge, deselect = True)

    cmds.polyBridgeEdge(divisions=0)


    ####        Relax the new vertices      ####
    cmds.select(clear = True)
    
    if relax == "Yes":
        mel.eval("setSelectMode components Components;")
        mel.eval("selectType -smp 0 -sme 0 -smf 0 -smu 0 -pv 1 -pe 0 -pf 0 -puv 0;")
        cmds.select(verticesForExclusion)
        mel.eval("invertSelection;")
        verticesForRelax = []
        verticesForRelax = cmds.ls(selection = True, flatten = True)
        cmds.polyAverageVertex( verticesForRelax, iterations = 100)
        mel.eval("selectType -smp 0 -sme 0 -smf 0 -smu 0 -pv 0 -pe 1 -pf 0 -puv 0;")
        cmds.select(clear = True)





####################################################
####                MAYA WINDOW                 ####
####################################################


GridFill = cmds.window( title="Grid Fill", iconName='Grid Fill', widthHeight=(220, 220), toolbox = True)
cmds.rowColumnLayout( numberOfColumns=2, columnWidth = [(1,155),(2,60)])
cmds.text( label="Offset" )
offsetBox = cmds.intField(changeCommand = 'newValue()', value = 0, minValue = 0)

cmds.separator(h=20, style = "none")
cmds.separator(h=20, style = "none")
cmds.text( label=("Add/reduce ") )
cmds.separator(h=20, style = "none")
cmds.text( label=("if the loop") )
divisions = cmds.intField(changeCommand = 'newValue()', value = originaldivision)
cmds.text( label=("is superior to") )
cmds.separator(h=20, style = "none")
cmds.text( label=("16 edges") )
cmds.separator(h=20, style = "none")
cmds.separator(h=20, style = "none")
cmds.separator(h=20, style = "none")
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

userInput()
gridFill()


