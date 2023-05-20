bl_info = {
    "name": "RenderBuzz",
    "author": "metarex21",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Properties > Render",
    "description": "Plays an alert tone when rendering is complete",
    "warning": "",
    "wiki_url": "",
    "category": "Render",
}

import bpy
import os
import platform

def get_alert_tone_path():
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Specify the alert tone file name
    alert_tone_file = "alert_tone.wav"

    # Construct the path to the alert tone file based on the platform
    if platform.system() == "Windows":
        alert_tone_path = os.path.join(script_directory, alert_tone_file)
    elif platform.system() == "Darwin":
        alert_tone_path = os.path.join(script_directory, "alert_tone.wav")
    else:  # Linux
        alert_tone_path = os.path.join(script_directory, "alert_tone.wav")

    return alert_tone_path

def play_alert_tone():
    alert_tone_path = get_alert_tone_path()
    
    if platform.system() == "Windows":
        import winsound
        winsound.PlaySound(alert_tone_path, winsound.SND_FILENAME)
    elif platform.system() == "Linux":
        os.system(f"aplay {alert_tone_path}")
    elif platform.system() == "Darwin":
        os.system(f"afplay {alert_tone_path}")

def render_complete_handler(scene):
    if scene.frame_current == scene.frame_end:
        play_alert_tone()

class RenderBuzzOperator(bpy.types.Operator):
    bl_idname = "render_buzz.activate"
    bl_label = "Activate Render Buzz"
    bl_description = "Activate the Render Buzz add-on"
    
    def execute(self, context):
        bpy.app.handlers.render_complete.append(render_complete_handler)
        self.report({'INFO'}, "Render Buzz activated")
        return {'FINISHED'}

class RenderBuzzPanel(bpy.types.Panel):
    bl_idname = "RENDER_BUZZ_PT_panel"
    bl_label = "Render Buzz"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("render_buzz.activate")

classes = (RenderBuzzOperator, RenderBuzzPanel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
