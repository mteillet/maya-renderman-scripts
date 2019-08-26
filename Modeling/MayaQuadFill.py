import maya.cmds as cmds
import maya.mel as mel

####    This script fills the selected edge loop with quads     ####


#   Selected Variables
#Edges
edgesSelected = cmds.ls(selection = True, shortNames = True, flatten = True)
#Object
curentObject = cmds.ls(selection = True, objectsOnly = True, shortNames = True)
#Get the number of selected edges
edgesNumber = cmds.polyEvaluate(edgeComponent = True)
#Quartes of the edge loop
firstQuarter = []
secondQuarter = []
thirdQuarter = []
fourthQuarter = []
#while loop
quarterLoop = 0
whileLoop = 0
n = 0


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
# if not an even number, error
else :
    print("ERROR")


#Deselect second and fourth quarters 
cmds.select((secondQuarter), toggle = True)
cmds.select((fourthQuarter), toggle = True)

#Finds the number of divisions needed based on the quarter size
divisionsNeeded = quarterSize - 3
currentSelection = cmds.ls(selection = True, shortNames = True)
cmds.polyBridgeEdge(currentSelection, divisions = (divisionsNeeded))

print (divisionsNeeded)


# Need to find a way to connect the quarters second and fourth to the new creater faces on the bridge
# Possible to remove first and last edges in the indexes of quarters second and fourth in order to bridge correctly
# Try to select edge loops connected to the quarters, and then remove the first and last index of the quarter before bridging

# Would be even better if one loop was taken away from every quarter list in order to be able to find the division needed in a more natural way
# Would also allow to spin the quarters in a much easier manner

# Need to make the script work on A mutiplier of 2 (currently only of 4)
# Should be fixed by rewriting the way quarters are defined
    # First split edge loop in halves, and then split each half into two quarters