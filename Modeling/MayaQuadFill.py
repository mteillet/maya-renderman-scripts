import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
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
    


####                    DEFINE THE OPTIMAL DIVISIONS AND THE MAX/MIN               ####
originaldivision = (((len(originalSelection) - OptimalFirstBridge - 4) / 2) - 1)
MaxOffset = (len(originalSelection) - 2)

# Defining the min and max values of divisions
if len(originalSelection) > 9:
    lessTenCheck = "True"
    if len(originalSelection) % 2 == 0:
        LoopStateCheck = "True"
        if len(originalSelection) < 12:
            minDiv = 1
            maxDiv = 2
            originaldivision = 1
        else:
            if len(originalSelection) < 16:
                minDiv = 2
                maxDiv = 3
                originaldivision = 2
            else:
                minDiv = 4
                if ((len(originalSelection) / 2) % 2) == 0:
                    maxDiv = (len(originalSelection) / 4) + 1
                    originaldivision = ((minDiv + maxDiv) // 2) + 1
                else:
                    maxDiv = (len(originalSelection) % 4) + 3
                    originaldivision = ((minDiv + maxDiv) // 2)               
    else:
        LoopStateCheck = "False"
else:
    lessTenCheck = "False"




####################################################
####               Grid fill code               ####
####################################################

def newValue():
    cmds.undo()
    print("newGridFill")
    userInput()
    gridFill()
    print("DONE")


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

#Check if there are 4 edges or more in the loop selection

if (len(originalSelection)) == 4:
    cmds.select(originalSelection)
    cmds.polyCloseBorder()
    
if (len(originalSelection)) == 6:
    cmds.select(originalSelection)
    cmds.polyCloseBorder()

if (len(originalSelection)) == 8:
    cmds.select(originalSelection)
    cmds.polyCloseBorder()
    
if lessTenCheck == "True":
    
    #Check if the number of edges in the loop is even
    if LoopStateCheck == "True":
    
        GridFill = cmds.window( title="Grid Fill", iconName='Grid Fill', widthHeight=(230, 110), toolbox = True)
        cmds.rowColumnLayout( numberOfColumns=4, columnWidth = [(1,80),(2,40),(3,45),(4,60)])
        cmds.text( label="Offset" )
        cmds.text( label="from 0", font ="smallFixedWidthFont" )
        offsetBox = cmds.intField(changeCommand = 'newValue()', value = 0, minValue = 0, maxValue = MaxOffset)
        cmds.text( label= "up to " + str(MaxOffset), font ="smallFixedWidthFont" )

        cmds.separator(h=20, style = "none")
        cmds.separator(h=20, style = "none")
        cmds.separator(h=20, style = "none")
        cmds.separator(h=20, style = "none")
        cmds.text( label=("Add/reduce ") )
        cmds.text( label= "from " + str(minDiv), font ="smallFixedWidthFont" )
        divisions = cmds.intField(changeCommand = 'newValue()', value = originaldivision, minValue = minDiv, maxValue = maxDiv)
        cmds.text( label= "up to " + str(maxDiv), font ="smallFixedWidthFont" )
        
        cmds.separator(h=20, style = "none")
        cmds.separator(h=20, style = "none")
        cmds.separator(h=20, style = "none")
        cmds.separator(h=20, style = "none")
        cmds.text( label="Relax" )
        cmds.separator(h=20, style = "none")
        relaxChoice = cmds.optionMenu( label='', changeCommand = 'newValue()' )
        cmds.menuItem( label='Yes' )
        cmds.menuItem( label='No' )

        cmds.showWindow( GridFill )

        userInput()
        gridFill()
        
    
        if len(originalSelection) < 16 :
            om.MGlobal.displayWarning("IMPOSSIBLE TO TWEAK DIVISION SETTINGS IF SELECTION WAS LESS THAN 16")
    
      
    else:
        cmds.error("ERROR : Selection must contain an even number of edges")
        
else:
    if len(originalSelection) < 10:
        
        if len(originalSelection) < 16:
            om.MGlobal.displayWarning("Can not tweak settings with less thant 16 edges")
        
        if len(originalSelection) % 2 != 0:
            cmds.error("ERROR : Selection must contain an even number of edges")
        
        if len(originalSelection) < 4:
            cmds.error("ERROR: Selection must containt 4 edges or more")
    
