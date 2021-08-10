class LunaVars:
    logging_level = "logging.level"
    command_port = "python.commandPort"
    callback_licence = "callback.license"
    marking_menu_mode = "markingMenu.mode"
    asset_types = "assetTypes"


class HudVars:
    block = "hud.block"
    section = "hud.section"


class TestVars:
    delete_files = "tests.deleteFiles"
    delete_dirs = "tests.deleteDirs"
    temp_dir = "tests.tempDir"
    buffer_output = "tests.bufferOutput"
    new_file = "tests.newFile"


class ProjectVars:
    # TODO: Remove previous project and just use recent list
    recent_projects = "project.recent"
    previous_project = "project.previous"
    recent_max = "project.maxRecent"


class BuilderVars:
    title_font = "builder.titleFont"
    socket_font = "builder.socketFont"
    history_enabled = "builder.historyEnabled"
    history_size = "builder.historySize"


class UnrealVars:
    project = "unreal.project"


class NamingVars:
    templates_dict = "naming.templates"
    current_template = "naming.profile.template"
    index_padding = "naming.profile.indexPadding"
    start_index = "naming.profile.startIndex"


class RigVars:
    skin_export_format = "rig.io.skin.fileFormat"
    nglayers_export_format = "rig.io.nglayers.fileFormat"
    line_width = "rig.display.lineWidth"


class ToolVars:
    locator_match_orient = "tool.locator.orient"
    locator_match_position = "tool.locator.position"
