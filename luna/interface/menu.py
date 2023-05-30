import pymel.core as pm
import imp
from functools import partial

from luna import Logger
DEBUG_MODE = Logger.get_level() == 10
try:
    import luna.tools
    from luna import Config
    from luna.static import directories
    from luna.interface.commands import tool_cmds
    from luna.interface.commands import help_cmds
    from luna.utils import devFn
    from luna.utils import fileFn
    from luna import TestVars
except Exception as e:
    Logger.exception("Failed to import modules", exc_info=e)

if DEBUG_MODE:
    try:
        imp.reload(tool_cmds)
        imp.reload(help_cmds)
        imp.reload(devFn)
        imp.reload(luna.tools)
        Logger.debug("Menu - reloaded command modules")
    except ImportError:
        Logger.exception("Failed to reload command modules")


def _null_command(*args):
    pass


class MenuUtil:
    @staticmethod
    def addMenuItem(parent=None,
                    label="",
                    command=_null_command,
                    icon="",
                    divider=False,
                    option_box=False,
                    check_box=False,
                    use_maya_icons=False,
                    var_name=None,
                    default_value=False):

        if icon and not use_maya_icons:
            icon = fileFn.get_icon_path(icon)

        if divider:
            return pm.menuItem(p=parent, dl=label, i=icon, d=divider)

        elif option_box:
            return pm.menuItem(p=parent, l=label, i=icon, ob=option_box, c=command)

        elif check_box:
            if not var_name:
                Logger.error(
                    "Menuitem: {0}::{1} is not connected to config!".format(parent, label))
                return

            checkBox_value = Config.get(var_name, default_value)
            checkBox = pm.menuItem(
                p=parent, l=label, i=icon, cb=checkBox_value, c=partial(Config.set, var_name))
            return checkBox

        else:
            return pm.menuItem(p=parent, l=label, i=icon, c=command)

    @staticmethod
    def addSubMenu(parent, label, tear_off=False, icon=None, use_maya_icons=False):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon and not use_maya_icons:
            icon = fileFn.get_icon_path(icon)

        return pm.menuItem(p=parent, l=label, i=icon, subMenu=True, to=tear_off)


class LunaMenu:
    MAIN_WINDOW = pm.melGlobals["gMainWindow"]
    MAIN_MENU_ID = "lunaMainMenu"
    MAIN_MENU_LABEL = "Luna"
    TOOLS_MENU_ID = "lunaToolsMenu"

    @classmethod
    def _delete_old(cls):
        try:
            pm.deleteUI(pm.menu(cls.MAIN_MENU_ID, e=1, deleteAllItems=1))
        except Exception:
            pass

    @classmethod
    def create(cls):
        # Build main menu
        cls._delete_old()
        Logger.info("Building menu...")
        pm.menu(cls.MAIN_MENU_ID, label=cls.MAIN_MENU_LABEL,
                parent=cls.MAIN_WINDOW, tearOff=1)
        MenuUtil.addMenuItem(cls.MAIN_MENU_ID, divider=1, label="Tools")

        # Tools
        MenuUtil.addMenuItem(cls.MAIN_MENU_ID,
                             label="Builder",
                             command=tool_cmds.luna_builder, icon="builder.svg")
        MenuUtil.addMenuItem(cls.MAIN_MENU_ID,
                             label="Transfer keyframes",
                             command=lambda *args: luna.tools.TransferKeyframesDialog.display())
        MenuUtil.addMenuItem(cls.MAIN_MENU_ID,
                             label="Animation baker",
                             command=lambda *args: luna.tools.AnimBakerDialog.display())
        MenuUtil.addMenuItem(cls.MAIN_MENU_ID,
                             label="Custom space tool",
                             command=lambda *args: luna.tools.CustomSpaceTool.display())
        cls._add_external_tools()

        # Developer tools
        cls._add_dev_menu()

        # Animation tools etc
        # MenuUtil.addMenuItem(cls.MAIN_MENU_ID, divider=1, label="Animation")

        # Help and config section
        MenuUtil.addMenuItem(cls.MAIN_MENU_ID, divider=1)
        MenuUtil.addMenuItem(cls.MAIN_MENU_ID, label="Configuration",
                             command=tool_cmds.luna_configer, icon="config.svg")
        cls._add_help_menu()

    @classmethod
    def _add_external_tools(cls):
        register = fileFn.load_json(directories.EXTERNAL_TOOLS_REGISTER)
        found = set(register).intersection(set(pm.moduleInfo(lm=1)))
        if not found:
            return

        tools_menu = MenuUtil.addSubMenu(
            cls.MAIN_MENU_ID, label="External", tear_off=1, icon="")
        for tool in found:
            MenuUtil.addMenuItem(tools_menu,
                                 label=register[tool].get("label"),
                                 command=register[tool].get("command"),
                                 icon=register[tool].get("icon"),
                                 use_maya_icons=register[tool].get("useMayaIcon"))
            Logger.info("Added {0} to luna >> Tools menu".format(tool))

    @classmethod
    def _add_help_menu(cls):
        help_menu = MenuUtil.addSubMenu(
            cls.MAIN_MENU_ID, label="Help", tear_off=1, icon="")
        MenuUtil.addMenuItem(help_menu, "About",
                             command=help_cmds.show_about_dialog)
        MenuUtil.addMenuItem(help_menu, "Documentation", icon="help.png",
                             command=help_cmds.open_docs, use_maya_icons=1)

    @classmethod
    def _add_dev_menu(cls):
        dev_menu = MenuUtil.addSubMenu(
            cls.MAIN_MENU_ID, label="Developer", tear_off=1, icon="")
        MenuUtil.addMenuItem(dev_menu, label="Testing", divider=1)
        MenuUtil.addMenuItem(dev_menu, label="Buffer output", check_box=1,
                             default_value=True, var_name=TestVars.buffer_output)
        MenuUtil.addMenuItem(dev_menu, label="Run all tests",
                             command=devFn.run_unit_tests, icon="checklist.svg")
        MenuUtil.addMenuItem(dev_menu, label="Unload", divider=1)
        MenuUtil.addMenuItem(dev_menu, label="Rig modules",
                             command=devFn.unload_rig_modules)
        MenuUtil.addMenuItem(dev_menu, label="Builder modules",
                             command=devFn.unload_builder_modules)
        MenuUtil.addMenuItem(dev_menu, label="Configer modules",
                             command=devFn.unload_configer_modules)


if __name__ == "__main__":
    LunaMenu.create()
