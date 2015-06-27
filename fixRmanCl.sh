#!/bin/bash

export  PIXAR_LICENSE_FILE=/opt/pixar/RenderManStudio-19.0-maya2014/rmantree/etc/pixar.license

RMANTREE=/opt/pixar/RenderManProServer-19.0
RSTUDIOTREE=/opt/pixar/RenderManStudio-19.0-maya2014

AW_LOCATION=/usr/autodesk
MAYA_LOCATION=$AW_LOCATION/maya
export AW_LOCATION MAYA_LOCATION

RMSTREE=/opt/pixar/RenderManStudio-19.0-maya2014
MAYA_PLUG_IN_PATH=$RMSTREE/plug-ins
MAYA_SCRIPT_PATH=$RMSTREE/scripts:$RSTUDIOTREE/scripts

XBMLANGPATH="$RMSTREE/icons/"

RMANFB=it
MAYA_PLUG_IN_PATH=$RSTUDIOTREE/plug-ins:~/plug-ins
XBMLANGPATH="$RSTUDIOTREE/lib/mtor/resources/%B"
XBMLANGPATH="$RSTUDIOTREE/icons/%B"
PATH=$PATH:$RSTUDIOTREE/bin:$RMANTREE/bin:/opt/Golaem/GolaemCrowd-3.4.2.1-Maya2014/bin
export RMANTREE RSTUDIOTREE RMANFB MAYA_SCRIPT_PATH XBMLANGPATH PATH MAYA_PLUG_IN_PATH RMSTREE

MI_CUSTOM_SHADER_PATH=$HOME/maya/mentalray/include
MI_LIBRARY_PATH=$HOME/maya/mentalray/lib
export MI_CUSTOM_SHADER_PATH MI_LIBRARY_PATH

LD_LIBRARY32_PATH="$MAYA_LOCATION/lib:$AW_LOCATION/COM/lib:$RSTUDIOTREE/bin:$RSTUDIOTREE/lib"
PYTHONPATH=/var/lib/python-support/python2.4:/usr/lib/python2.4/site-packages:$PYTHONPATH
export LD_LIBRARYN32_PATH PYTHONPATH

# Golaem Crowd
export golaem_LICENSE=2375@burton
export GLM_CROWD_HOME=/opt/Golaem/GolaemCrowd-3.4.2.1-Maya2014
export MAYA_MODULE_PATH=/opt/Golaem/GolaemCrowd-3.4.2.1-Maya2014:${MAYA_MODULE_PATH}
export LD_LIBRARY_PATH=/opt/Golaem/GolaemCrowd-3.4.2.1-Maya2014/lib:${LD_LIBRARY_PATH}
export MAYA_PLUG_IN_PATH=/opt/Golaem/GolaemCrowd-3.4.2.1-Maya2014:${MAYA_PLUG_IN_PATH}
export MAYA_SCRIPT_PATH=/opt/Golaem/GolaemCrowd-3.4.2.1-Maya2014/scripts:${MAYA_SCRIPT_PATH}
#Fix the cross mouse cursor
