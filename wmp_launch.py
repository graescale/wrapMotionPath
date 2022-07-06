#*******************************************************************************
# content = Launches UI for wrap_motion_path.
#
# version      = 0.0.1
# date         = 2022-06-29
#
# dependencies = Maya, Qt
#
# author = Grae Revell <grae.revell@gmail.com>
#*******************************************************************************



# Qt
from Qt import QtWidgets, QtGui, QtCore, QtCompat
import os
import sys

CURRENT_PATH = '/mnt/rodeo/dropbox/grevell/rdoenv/wrap_motion_path/'
sys.path.append(CURRENT_PATH)
#TITLE = os.path.splitext(os.path.basename(__file__))[0]

#from wmp import *
import wmp as wp
reload(wp)
#*******************************************************************************
# VARIABLES


#*******************************************************************************
# UI

class WrapPath:
    def __init__(self):
        path_ui = CURRENT_PATH + "/" + "wrap_motion_path" + ".ui"
        self.wgWrapMotionPath = QtCompat.loadUi(path_ui)
        self.objects = wp.StoreInfo()

        self.wgWrapMotionPath.btnAddPath.clicked.connect(self.press_btnAddPath)
        self.wgWrapMotionPath.btnAddGeo.clicked.connect(self.press_btnAddGeo)
        self.wgWrapMotionPath.btnWrap.clicked.connect(self.press_btnWrap)
        self.wgWrapMotionPath.show()

        # PRESS

    def press_btnAddPath(self):
        if len(cmds.ls(sl=True)) > 0:
            self.objects.paths = self.objects.get_paths()
            self.wgWrapMotionPath.wgPathList.clear()
            self.wgWrapMotionPath.wgPathList.addItems(self.objects.paths)
            self.wgWrapMotionPath.lblStatus.setText("Motion path(s) added. Please add geometry")


    def press_btnAddGeo(self):
        if len(cmds.ls(sl=True)) > 0:
            self.objects.geo = self.objects.get_geo()
            self.wgWrapMotionPath.wgGeoList.clear()
            self.wgWrapMotionPath.wgGeoList.addItems(self.objects.geo)
            self.wgWrapMotionPath.lblStatus.setText("Geometry added. Please click Wrap Path(s)")
    def press_btnWrap(self):
        self.objects.create_shrink_wrap(self.objects.paths, self.objects.geo)
        self.wgWrapMotionPath.lblStatus.setText("Done. Please see script editor for messages.")

#*******************************************************************
# START
if __name__ == "__main__":
    wrap_motion_path_UI = WrapPath()