#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains constant definitions for tpDccLib
"""

from __future__ import print_function, division, absolute_import

from tpPyUtils import enum

# =================== PROJECTS
PROJECTS_NAME = 'project.json'
CODE_FOLDER = '__code__'
DATA_FOLDER = '__data__'
BACKUP_FOLDER = '__backup__'
VERSIONS_FOLDER = '__versions__'
MANIFEST_FILE = 'manifest.data'
DATA_FILE = 'data.json'


# =================== TOOLTIPS
DELETE_PROJECT_TOOLTIP = 'Delete selected project'
OPEN_PROJECT_IN_EXPLORER_TOOLTIP = 'Open Project Folder in Explorer'
SET_PROJECT_IMAGE_TOOLTIP = 'Set the Image used for the Project'


# =================== TYPES
class PointerTypes(enum.EnumGroup):
    Shape = enum.Enum()
    Transform = enum.Enum()
    Pointer = enum.Enum()


class ObjectTypes(enum.EnumGroup):
    Generic = enum.Enum()
    Sphere = enum.Enum()
    Box = enum.Enum()
    Cylinder = enum.Enum()
    Capsule = enum.Enum()
    Geometry = enum.Enum()
    Model = enum.Enum()
    PolyMesh = enum.Enum()
    NurbsSurface = enum.Enum()
    Curve = enum.Enum()
    Light = enum.Enum()
    Camera = enum.Enum()
    Group = enum.Enum()
    Null = enum.Enum()
    Bone = enum.Enum()
    Particle = enum.Enum()
    Network = enum.Enum()
    Circle = enum.Enum()
    Biped = enum.Enum()


class UnitSystem(enum.EnumGroup):
    Inches = enum.Enum()
    Feet = enum.Enum()
    Millimeters = enum.Enum()
    Centimeters = enum.Enum()
    Meters = enum.Enum()
    Kilometers = enum.Enum()
    Yards = enum.Enum()
    Miles = enum.Enum()


class MaterialAttributeTypes(enum.EnumGroup):
    Int = enum.Enum()
    Float = enum.Enum()
    String = enum.Enum()
    Path = enum.Enum()
    Color = enum.Enum()
    Bool = enum.Enum()


class MaterialTypes(enum.EnumGroup):
    Standard = enum.Enum()
