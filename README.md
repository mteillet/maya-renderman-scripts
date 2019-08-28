# maya-renderman-scripts

Scripts I made for Renderman and for Maya. 
All scripts are free to use and to share. 
For more informations, contact me.


# RmanAbsoluteToRelativePath.py
This script allows you to change all of your PxrTexture nodes filename from an absolute to a relative one. before you move a project from one location to another one.

Example : it would change "c:/usr/desktop/project/sourceimages/anytexture.tiff"
to "<ws>/sourceimages/anytexture.tiff"
  
  Remember to do this before moving the project into a new location. Otherwise the current workspace will be considered as your new project file path, and not the ancient you wanted to change.
  
# AlembicRelativeRepath.py
This scripts allow you to remerge the alembic broken links to the correct ones when you change your project location.

It selects all the alembic nodes from your scene containing the string "cache/alembic" and replaces the characters before that by the current set project path.

Then it remerges the alembic files and deletes the ancient Alembic nodes which had the broken paths.


# MayaQuadFill.py
This script allows you to fill a selection with only quads, trying to replicate the Blender Grid fill function. You can offset (rotate) the direction of the gridfill, you can use the increase/decrease in order to change the  way the corners of the edge loop are defined

Here is a demonstration :
![](Maya_GridFill_Demo.gif)

However, this script still has a few issues.

1st = The first loop selected will work only if the "cmds.ls(orderedSelection=True)" returns edges following each other. It sometime does not

2nd = The window created is not great. It would be much better if the GridFill operated a first time with the default indicated settings.
      It would also be much better to have a floating pannel (as it is the case for the Maya extrude tool for example).
      The user would modified the default inputs if needed from this pannel
      Everytime a value is modified, the gridfill should "undo" itself and reoperate again with the new user values

3rd = Currently, this script works only if the number of edges selected is a multiple of 4. It should also be possible to make it work with multiples of 2


# Thank you
If you have any ideas for tools, or how to improve the current one, do not hesitate to email me at : martin.teillet@hotmail.fr or to create a branch :)