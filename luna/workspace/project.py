import os
from collections import deque
from datetime import datetime

from luna import Logger
import luna
try:
    import luna.utils.fileFn as fileFn
    from luna import Config
    from luna import ProjectVars
    from luna.interface.hud import LunaHUD
except Exception:
    Logger.exception("Failed to import modules")


class Project(object):
    """
    Base project class. Represents rigging project
    """
    TAG_FILE = "luna.proj"
    _INSTANCE = None  # type: Project

    def __repr__(self):
        return "{0}({1}): {2}".format(self.name, self.path, self.meta_data)

    def __init__(self, path):
        self.path = path  # type: str

    @property
    def name(self):
        name = os.path.basename(self.path)  # type:str
        return name

    @property
    def tag_path(self):
        p = os.path.join(self.path, self.TAG_FILE)  # type:str
        return p

    @property
    def meta_path(self):
        p = os.path.join(self.path, self.name + ".meta")  # type:str
        return p

    @property
    def meta_data(self):
        meta_dict = {}
        if os.path.isfile(self.meta_path):
            meta_dict = fileFn.load_json(self.meta_path)

        for category in os.listdir(self.path):
            category_path = os.path.join(self.path, category)
            if os.path.isdir(category_path):
                asset_dirs = filter(os.path.isdir, [os.path.join(category_path, item) for item in os.listdir(category_path)])
                meta_dict[category] = [os.path.basename(asset) for asset in asset_dirs]
        return meta_dict

    def __on_creation(self):
        Config.set(ProjectVars.previous_project, self.path)
        self.add_to_recent()
        LunaHUD.refresh()

    def set_data(self, key, value):
        data_dict = self.meta_data
        data_dict[key] = value
        fileFn.write_json(self.meta_path, data_dict, sort_keys=True)

    def update_meta(self):
        fileFn.write_json(self.meta_path, data=self.meta_data)

    def add_to_recent(self):
        max_recent = Config.get(ProjectVars.recent_max, default=3)
        project_queue = Config.get(ProjectVars.recent_projects, default=deque(maxlen=max_recent))
        if not isinstance(project_queue, deque):
            project_queue = deque(project_queue, maxlen=max_recent)

        entry = [self.name, self.path]
        if entry in project_queue:
            return

        project_queue.appendleft(entry)
        Config.set(ProjectVars.recent_projects, list(project_queue))

    @classmethod
    def create(cls, path, silent=False):
        if cls.is_project(path):
            Logger.error("Already a project: {0}".format(path))
            return

        new_project = cls(path)
        # Create missing meta and tag files
        fileFn.create_missing_dir(new_project.path)
        fileFn.create_file(path=new_project.tag_path)
        creation_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        new_project.set_data("created", creation_date)

        # Set enviroment variables and refresh HUD
        cls._INSTANCE = new_project
        luna.workspace.Asset._INSTANCE = None
        if not silent:
            new_project.__on_creation()
        return new_project

    @classmethod
    def is_project(cls, path):
        search_file = os.path.join(path, cls.TAG_FILE)
        Logger.debug("isProject check ({0}) - {1}".format(os.path.isfile(search_file), path))
        return os.path.isfile(search_file)

    @classmethod
    def set(cls, path, silent=False):
        if not cls.is_project(path):
            Logger.error("Not a project: {0}".format(path))
            return

        project_instance = cls(path)
        project_instance.update_meta()
        # Set enviroment variables and refresh HUD
        cls._INSTANCE = project_instance
        luna.workspace.Asset._INSTANCE = None
        if not silent:
            project_instance.__on_creation()
        return project_instance

    @classmethod
    def get(cls):
        return cls._INSTANCE

    @classmethod
    def exit(cls):
        cls._INSTANCE = None
        luna.workspace.Asset._INSTANCE = None
        LunaHUD.refresh()

    @staticmethod
    def refresh_recent():
        recent_projects = Config.get(ProjectVars.recent_projects)
        existing_projects = []
        for prj in recent_projects:
            if os.path.isdir(prj[1]):
                existing_projects.append(prj)
        Config.set(ProjectVars.recent_projects, existing_projects)
