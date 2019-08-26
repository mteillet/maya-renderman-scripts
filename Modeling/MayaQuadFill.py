import maya.cmds as cmds
import maya.mel as mel

####    This script fills the selected edge loop with quads     ####


### Variables

####################################################
####                MAYA WINDOW                 ####
####################################################


GridFill = cmds.window( title="Grid Fill", iconName='Grid Fill', widthHeight=(140, 90), toolbox = True)
cmds.rowColumnLayout( numberOfColumns=2, columnWidth = [(1,75),(2,60)])
cmds.text( label="Offset" )
offset = cmds.intField(changeCommand = 'userInput()', value = 0)
cmds.text( label="Divisions" )
divisions = cmds.intField(changeCommand = 'userInput()', value = 1)

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



    #Ordering the number of edges
    orderedEdges = cmds.ls(orderedSelection=True, flatten=True)
    print(orderedEdges)
    
    #Reorder the selection based on the offset input by user
    ReorderedEdges = orderedEdges[userOffset:] + orderedEdges[:userOffset]
    print("This is the new edges order following the offset " + str(ReorderedEdges))
    
    #Splitting the list in 2
    FirstHalf = ReorderedEdges[:len(ReorderedEdges)//2]
    SecondHalf = ReorderedEdges[len(ReorderedEdges)//2:]
    
    print(FirstHalf)
    print(SecondHalf)


    """

    print(curentObject)
    print(edgesSelected)
    print(edgesNumber)

    #### Need to store the quarters as separate list in order to refer to individual edges at the extermities of the list in an easier way
    #### Should also allow to implement the rotate a lot more easier


    #Store the 4 quarters of the edgeloop
    #Find the quarter size
    if edgesNumber % 2 == 0:
        quarterSize = edgesNumber / 4
        print(quarterSize)



        #Sets the list of edges containing the four quarters
        while quarterLoop < quarterSize:
            firstQuarter.append(edgesSelected[quarterLoop])
            secondQuarter.append(edgesSelected[(quarterLoop) + (quarterSize)])
            thirdQuarter.append(edgesSelected[(quarterLoop) + ( (quarterSize) * 2 )])
            fourthQuarter.append(edgesSelected[(quarterLoop) + ( (quarterSize) * 3 )])

            quarterLoop += 1
        print(firstQuarter)
        print(secondQuarter)
        print(thirdQuarter)
        print(fourthQuarter)
        #Get rid of every first and last edges of indexes for bridges sides
        #The removed edges are still in the quarter lists
        firstBridgeSide = firstQuarter[:-1]
        secondBridgeSide = secondQuarter[:-1]
        thirdBridgeSide = thirdQuarter[:-1]
        fourthBridgeSide = fourthQuarter[:-1]
        

    # if not an even number, error
    else :
        print("ERROR")



    #Select first and third bride sides 
    cmds.select(clear = True)
    cmds.select((firstBridgeSide), toggle = True)
    cmds.select((thirdBridgeSide), toggle = True)




    #Finds the number of divisions needed based on the quarter size
    #Bridges the first two Bridges sides
    divisionsNeeded = quarterSize - 2
    currentSelection = cmds.ls(selection = True, shortNames = True)
    cmds.polyBridgeEdge(currentSelection, divisions = (divisionsNeeded))

    #Select the second Bridge edge 
    cmds.select(clear = True)
    cmds.select((secondBridgeSide), toggle = True)

    #select the new edge border next to the second bridge
    print(secondBridgeSide)
    secondEdgeBorder= str(secondBridgeSide[0])
    print(secondEdgeBorder)

    #cmds.polySelect(shortObject, edgeBorder=1316)


    # Need to find a way to connect the quarters second and fourth to the new creater faces on the bridge
    # Possible to remove first and last edges in the indexes of quarters second and fourth in order to bridge correctly
    # Try to select edge loops connected to the quarters, and then remove the first and last index of the quarter before bridging

    # Need to make the script work on A mutiplier of 2 (currently only of 4)
    # Should be fixed by rewriting the way quarters are defined
        # First split edge loop in halves, and then split each half into two quarters

    """


if __name__ == "__main__":
	main()