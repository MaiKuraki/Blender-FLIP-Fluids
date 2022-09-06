# Blender FLIP Fluids Add-on
# Copyright (C) 2022 Ryan L. Guy
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.props import (
        FloatProperty,
        FloatVectorProperty,
        StringProperty,
        BoolProperty,
        EnumProperty,
        IntProperty,
        PointerProperty
        )

from . import preset_properties
from .. import types
from ..utils import version_compatibility_utils as vcu


class FlipFluidFluidProperties(bpy.types.PropertyGroup):
    conv = vcu.convert_attribute_to_28
    
    initial_velocity = FloatVectorProperty(
            name="Initial Velocity",
            description="Initial velocity of fluid (m/s)",
            default =(0.0, 0.0, 0.0),
            size=3,
            precision=3,
            subtype='VELOCITY',
            ); exec(conv("initial_velocity"))
    append_object_velocity = BoolProperty(
            name="Add Object Velocity to Fluid",
            description="Add the velocity of the object to the initial velocity"
                " of the fluid. Object mesh must be rigid (non-deformable)",
            default=False,
            ); exec(conv("append_object_velocity"))
    append_object_velocity_influence = FloatProperty(
            name="Influence",
            description="Amount of velocity that is added to the fluid."
                " A value of 1.0 is normal, less than 1.0 will dampen the"
                " velocity, greater than 1.0 will exaggerate the velocity,"
                " negative values will reverse velocity direction",
            subtype='FACTOR',
            soft_min=0.0, soft_max=1.0,
            default=1.0,
            precision=2,
            ); exec(conv("append_object_velocity_influence"))
    priority = IntProperty(
            name="Priority",
            description="Priority that this fluid object is added to the simulation"
                " during a frame. If multiple fluid/inflow objects are adding fluid"
                " to the simulation during a frame, the object with the higher priority"
                " value will be added first. Use to control which fluid attributes are"
                " prioritized and set first such as with intersecting objects or nested"
                " objects",
            min=-1000000, max=1000000,
            default=0,
            ); exec(conv("priority"))
    use_initial_velocity_target = BoolProperty(
            name ="Set towards target",
            description="Set initial velocity towards a target object",
            default=False,
            options={'HIDDEN'}
            ); exec(conv("use_initial_velocity_target"))
    fluid_velocity_mode = EnumProperty(
            name="Velocity Mode",
            description="Set how the inital fluid velocity is calculated",
            items=types.fluid_velocity_modes,
            default='FLUID_VELOCITY_MANUAL',
            options={'HIDDEN'},
            ); exec(conv("fluid_velocity_mode"))
    initial_speed = bpy.props.FloatProperty(
            name="Speed",
            description="Initial speed of fluid towards target (m/s)",
            default=0.0,
            precision=3,
            options={'HIDDEN'},
            ); exec(conv("initial_speed"))
    fluid_axis_mode = EnumProperty(
            name="Local Axis",
            description="Set local axis direction of fluid",
            items=types.local_axis_directions,
            default='LOCAL_AXIS_POS_X',
            ); exec(conv("fluid_axis_mode"))
    target_object = PointerProperty(
            name="Target Object", 
            type=bpy.types.Object
            ); exec(conv("target_object"))
    source_id = IntProperty(
            name="Source ID Attribute",
            description="Assign this identifier value to the fluid generated by this object. After"
                " baking, the source ID attribute values can be accessed in a Cycles Attribute Node"
                " with the name 'flip_source_id' from the Fac output. This can be used to create"
                " basic multiple material liquid effects. Enable this feature in the Domain FLIP"
                " Fluid Surface panel",
            min=0, soft_max=16,
            default=0,
            options={'HIDDEN'},
            ); exec(conv("source_id"))
    viscosity = FloatProperty(
            name="Viscosity Attribute",
            description="Assign this viscosity value to the fluid generated by this object. After"
                " baking, the viscosity attribute values can be accessed in a Cycles Attribute Node"
                " with the name 'flip_viscosity' from the Fac output. This feature can be used to create"
                " variable viscosity liquid effects. Enable this viscosity feature in the Domain FLIP"
                " Fluid World panel",
            min=0.0,
            default=0.0,
            ); exec(conv("viscosity"))
    color = FloatVectorProperty(
            name="Color Attribute",
            description="Assign this color to the fluid generated by this object. After"
                " baking, the color attribute values can be accessed in a Cycles Attribute Node"
                " with the name 'flip_color' from the Color output. This can be used to create"
                " basic varying color liquid effects. Enable this feature in the Domain FLIP"
                " Fluid Surface panel",
            default=(1.0, 1.0, 1.0),
            min=0.0, max=1.0,
            size=3,
            precision=3,
            subtype='COLOR',
            ); exec(conv("color"))
    export_animated_target = BoolProperty(
            name="Export Animated Target",
            description="Export this target as an animated one (slower, only"
                " use if really necessary [e.g. armatures or parented objects],"
                " animated pos/rot/scale F-curves do not require it",
            default=False,
            options={'HIDDEN'},
            ); exec(conv("export_animated_target"))
    export_animated_mesh = BoolProperty(
            name="Export Animated Mesh",
            description="Export this mesh as an animated one (slower, only use"
                " if really necessary [e.g. armatures or parented objects],"
                " animated pos/rot/scale F-curves do not require it",
            default=False,
            options={'HIDDEN'},
            ); exec(conv("export_animated_mesh"))
    skip_reexport = BoolProperty(
            name="Skip Mesh Re-Export",
            description="Skip re-exporting this mesh when starting or resuming"
                " a bake. If this mesh has not been exported or is missing files,"
                " the addon will automatically export the required files",
            default=False,
            options={'HIDDEN'},
            ); exec(conv("skip_reexport"))
    force_reexport_on_next_bake = BoolProperty(
            name="Force Re-Export On Next Bake",
            description="Override the 'Skip Re-Export' option and force this mesh to be"
                " re-exported and updated on the next time a simulation start/resumes"
                " baking. Afting starting/resuming the baking process, this option"
                " will automatically be disabled once the object has been fully exported."
                " This option is only applicable if 'Skip Re-Export' is enabled",
            default=False,
            options={'HIDDEN'},
            ); exec(conv("force_reexport_on_next_bake"))
    frame_offset_type = EnumProperty(
            name="Trigger Type",
            description="When to trigger fluid object",
            items=types.frame_offset_types,
            default='OFFSET_TYPE_FRAME',
            options={'HIDDEN'},
            ); exec(conv("frame_offset_type"))
    frame_offset = IntProperty(
            name="",
            description="Frame offset from start of simulation to add fluid object"
                " to domain",
            min=0,
            default=0,
            options={'HIDDEN'},
            ); exec(conv("frame_offset"))
    timeline_offset = bpy.props.IntProperty(
            name="",
            description="Timeline frame to add fluid object to domain",
            min=0,
            default=0,
            options={'HIDDEN'},
            ); exec(conv("timeline_offset"))
    property_registry = PointerProperty(
            name="Fluid Property Registry",
            description="",
            type=preset_properties.PresetRegistry,
            ); exec(conv("property_registry"))


    def initialize(self):
        self.property_registry.clear()
        add = self.property_registry.add_property
        add("fluid.initial_velocity", "")
        add("fluid.append_object_velocity", "")
        add("fluid.append_object_velocity_influence", "")
        add("fluid.priority", "")
        add("fluid.fluid_velocity_mode", "")
        add("fluid.initial_speed", "")
        add("fluid.fluid_axis_mode", "")
        add("fluid.source_id", "")
        add("fluid.viscosity", "")
        add("fluid.color", "")
        add("fluid.export_animated_target", "")
        add("fluid.export_animated_mesh", "")
        add("fluid.skip_reexport", "")
        add("fluid.force_reexport_on_next_bake", "")
        add("fluid.frame_offset_type", "")
        add("fluid.frame_offset", "")
        add("fluid.timeline_offset", "")
        self._validate_property_registry()


    def _validate_property_registry(self):
        for p in self.property_registry.properties:
            path = p.path
            base, identifier = path.split('.', 1)
            if not hasattr(self, identifier):
                print("Property Registry Error: Unknown Identifier <" + identifier + ", " + path + ">")


    def get_target_object(self):
        obj = None
        try:
            all_objects = vcu.get_all_scene_objects()
            obj = self.target_object
            obj = all_objects.get(obj.name)
        except:
            pass
        return obj


    def is_target_valid(self):
        return (self.fluid_velocity_mode == 'FLUID_VELOCITY_TARGET' and 
                self.get_target_object() is not None)


    def load_post(self):
        self.initialize()


def load_post():
    fluid_objects = bpy.context.scene.flip_fluid.get_fluid_objects()
    for fluid in fluid_objects:
        fluid.flip_fluid.fluid.load_post()


def register():
    bpy.utils.register_class(FlipFluidFluidProperties)


def unregister():
    bpy.utils.unregister_class(FlipFluidFluidProperties)