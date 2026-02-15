bl_info = {
    "name": "Wii MTC",
    "author": "FireWolf",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar",
    "description": "Putting in red the objects that have more triangles that the estimated selected Wii game's limit.",
    "category": "Object",
}

import bpy

class TriangleColorProperties(bpy.types.PropertyGroup):
    active: bpy.props.BoolProperty(
        name="Enable Object coloration",
        description="Put the objects with too much triangles in red and the others in blue.",
        default=False
    )
    
    threshold: bpy.props.EnumProperty(
        name="Target Game",
        description="The Wii game you want to export to",
        items=[
            ('8500', "Super Mario Bros : Brawl (Character) [< 8500]", ""),
            ('8000', "Mario Kart Wii (Character) [< 8000]", "")
        ],
        default='8500'
    )

def color_triangles_handler(scene):
    props = bpy.context.scene.triangle_color_props
    if not props.active:
        return
    threshold = int(props.threshold)
    
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            if not obj.data.materials:
                mat = bpy.data.materials.new(name="Mat")
                obj.data.materials.append(mat)
            else:
                mat = obj.data.materials[0]

            tris = sum(len(p.vertices) - 2 for p in obj.data.polygons)
            if tris > threshold:
                mat.diffuse_color = (1,0,0,1)
            else:
                mat.diffuse_color = (0,0,1,1)

class VIEW3D_PT_triangle_color_panel(bpy.types.Panel):
    bl_label = "Wii MTC"
    bl_idname = "VIEW3D_PT_triangle_color_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Triangles"

    def draw(self, context):
        layout = self.layout
        props = context.scene.triangle_color_props
        layout.prop(props, "active")
        layout.prop(props, "threshold")

classes = (
    TriangleColorProperties,
    VIEW3D_PT_triangle_color_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.triangle_color_props = bpy.props.PointerProperty(type=TriangleColorProperties)
    bpy.app.handlers.depsgraph_update_post.append(color_triangles_handler)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.triangle_color_props
    bpy.app.handlers.depsgraph_update_post.remove(color_triangles_handler)

if __name__ == "__main__":
    register()
