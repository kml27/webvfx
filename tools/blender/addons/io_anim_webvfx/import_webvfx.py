# Copyright (c) 2011 Hewlett-Packard Development Company, L.P. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import bpy
from io_anim_webvfx import KeyframeGroup, CurveNames, CoordNames
import numbers
import json

def importAnimation(animObject, animation):
    animObject.animation_data_clear()
    animObject.animation_data_create()

    action = bpy.data.actions.new("%sAction" % animObject.name)
    action.groups.new(KeyframeGroup)

    # Restore camera FOV
    if animObject.type == 'CAMERA' and 'horizontalFOV' in animation:
        animObject.data.angle = animation['horizontalFOV']

    animRange = animation['range']

    for curve in CurveNames:
        for coord in range(3):
            fcurve = action.fcurves.new(curve, coord, KeyframeGroup)
            curveData = animation[CurveNames[curve] + CoordNames[coord]]
            # Constant value
            if isinstance(curveData, numbers.Real):
                fcurve.keyframe_points.insert(animRange[0], curveData)
            # Array of segment control point data
            else:
                for segment in curveData:
                    points = segment['bezierPoints']
                    keyframe = fcurve.keyframe_points.insert(points[0][0],
                                                             points[0][1])
                    keyframe.handle_right = points[1]
                    keyframe = fcurve.keyframe_points.insert(points[3][0],
                                                             points[3][1])
                    keyframe.handle_left = points[2]

    animObject.animation_data.action = action


def load(operator, context, filepath=""):
    with open(filepath, "r") as file:
        animation = json.load(file)
    importAnimation(context.object, animation)
    return {'FINISHED'}
