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
#while loop
whileLoop = 0
n = 0


print(curentObject)
print(edgesSelected)
print(edgesNumber)

#### Need to store the quarters as separate list in order to refer to individual edges at the extermities of the list in an easier way
#### Should also allow to implement the rotate a lot more easier

#Check if number is even
if edgesNumber % 2 == 0:
    #Calculates the number of half edges
    edgesHalf = edgesNumber / 2
    #Calculates the number of quarter edges
    edgesQuarter = edgesHalf / 2
    print(edgesHalf, edgesQuarter)
else :
    #Calculates the number of half edges
    edgesHalf = (edgesNumber - 1)/2
    #Calculates the number of quarter edges
    edgesQuarter = edgesHalf / 2
    print("Edge loop is an odd number of edges")
    print(edgesHalf, edgesQuarter)



#While loop deselect quarters of edges
while whileLoop <= edgesQuarter:
    print ("N is:")
    print(n)
    #Deselect the first quarter of the loop
    cmds.select(((edgesSelected[n])), toggle = True)
    print(edgesSelected[n])

    #Deselect the opposite quarter of the loop
    m = n + edgesHalf
    cmds.select((str(edgesSelected[m])), toggle = True)

    #increments
    n += 1
    whileLoop += 1




#Get the number of remaining edges
remainingEdges = edgesNumber - edgesHalf 
#Calculates the number of divisions needed for the first bridge
divisionNeeded = remainingEdges - 7

# Bridge the opposing loop quarters
# Get selection first
firstQuarters = cmds.ls(selection = True, shortNames = True)
cmds.polyBridgeEdge(firstQuarters, divisions = (divisionNeeded))