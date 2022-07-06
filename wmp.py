#*******************************************************************************
# content = Wraps motion paths to a single geometry.
#
# version      = 0.0.1
# date         = 2022-06-29
# how to       => Source wmp_launch.py
#
# dependencies = Maya
#
# author = Grae Revell <grae.revell@gmail.com>
#*******************************************************************************

import maya.cmds as cmds
#*******************************************************************************
# CLASS

class StoreInfo:
    def __init__(self):
        self.paths = []
        self.geo = ""

#*******************************************************************************
# COLLECT

    def get_paths(self):
        return cmds.ls(selection=True)

    def get_geo(self):
        return cmds.ls(selection=True)

#*******************************************************************************
# PROCESS

    # def wrap_path(self):
    #     for path in self.paths:
    #         cmds.select(path)
    #         path_shape = cmds.pickWalk(path, direction = 'down')[0]
    #         motion_path = cmds.listConnections(path_shape, type='motionPath')[0]
    #         cmds.disconnectAttr(path_shape + '.worldSpace[0]', str(motion_path) + '.geometryPath')
    #         #cmds.select(self.geo)
    #         #cmds.deformer(path, type='shrinkWrap')
    #         shrinkWrapNode = pm.deformer(path, type='shrinkWrap')[0]
    #         pm.PyNode(self.geo[0]).worldMesh[0] >> shrinkWrapNode.targetGeom
    #         shrinkWrapNode.closestIfNoIntersection.set(True)
    #         cmds.delete(path, constructionHistory=True)
    #         cmds.connectAttr(path_shape + '.worldSpace[0]', str(motion_path) + '.geometryPath')

    def disconnect_mp(self):
        cmds.select(path)
        path_shape = cmds.pickWalk(path, direction='down')[0]
        cmds.disconnectAttr(path_shape + '.worldSpace[0]', str(motion_path) + '.geometryPath')


    def create_shrink_wrap(self, mesh, target, **kwargs):
        """
        Check available kwargs with parameters below.
        """
        print('-----------------------------------------')
        print('')
        for path in self.paths:
            cmds.select(path)
            path_shape = cmds.pickWalk(path, direction = 'down')[0]
            motion_paths = cmds.listConnections(path_shape, type='motionPath')
            print('Found ' + str(len(motion_paths)) + ' motion paths connected to ' + path + '.')
            for mp in motion_paths:
                cmds.disconnectAttr(path_shape + '.worldSpace[0]', str(mp) + '.geometryPath')

            parameters = [
                ("projection", 4),
                ("closestIfNoIntersection", 1),
                ("reverse", 0),
                ("bidirectional", 1),
                ("boundingBoxCenter", 1),
                ("axisReference", 1),
                ("alongX", 0),
                ("alongY", 0),
                ("alongZ", 1),
                ("offset", 0),
                ("targetInflation", 0),
                ("targetSmoothLevel", 0),
                ("falloff", 0),
                ("falloffIterations", 1),
                ("shapePreservationEnable", 0),
                ("shapePreservationSteps", 1)
            ]

            target_shapes = cmds.listRelatives(target, f=True, shapes=True, type="mesh", ni=True)
            if not target_shapes:
                raise ValueError("The target supplied is not a mesh")
            target_shape = target_shapes[0]

            shrink_wrap = cmds.deformer(mesh, type="shrinkWrap")[0]

            for parameter, default in parameters:
                cmds.setAttr(
                    shrink_wrap + "." + parameter,
                    kwargs.get(parameter, default))

            connections = [
                ("worldMesh", "targetGeom"),
                ("continuity", "continuity"),
                ("smoothUVs", "smoothUVs"),
                ("keepBorder", "keepBorder"),
                ("boundaryRule", "boundaryRule"),
                ("keepHardEdge", "keepHardEdge"),
                ("propagateEdgeHardness", "propagateEdgeHardness"),
                ("keepMapBorders", "keepMapBorders")
            ]

            for out_plug, in_plug in connections:
                cmds.connectAttr(
                    target_shape + "." + out_plug,
                    shrink_wrap + "." + in_plug)

            cmds.delete(path, constructionHistory=True)
            for mp in motion_paths:
                cmds.connectAttr(path_shape + '.worldSpace[0]', str(mp) + '.geometryPath')
            print(path + ': shrinkwrap done.')
        print('That\'s a wrap! Have yourself the best day ever!' )
        print('-----------------------------------------')
        print('')
        return shrink_wrap