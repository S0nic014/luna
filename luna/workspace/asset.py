import os
from datetime import datetime
from luna import Logger
import luna.utils.fileFn as fileFn
from luna.interface.hud import LunaHUD


class Asset:

    _INSTANCE = None  # type: Asset

    @classmethod
    def get(cls):
        return cls._INSTANCE

    def __repr__(self):
        return "Asset: {0}({1}), Model: {2}".format(self.name, self.type, self.meta_data.get("model"))

    def __init__(self, project, name, typ):
        self.name = name
        self.type = typ.lower()
        self.current_project = project
        if not self.current_project:
            raise Exception("Project is not set!")

        # Define paths
        self.path = os.path.join(self.current_project.path, self.type.lower() + "s", self.name)  # type:str

        #  Create directories
        fileFn.create_missing_dir(self.path)
        self.controls = fileFn.create_missing_dir(os.path.join(self.path, "controls"))  # type:str
        self.skeleton = fileFn.create_missing_dir(os.path.join(self.path, "skeleton"))  # type:str
        self.build = fileFn.create_missing_dir(os.path.join(self.path, "build"))  # type:str
        self.rig = fileFn.create_missing_dir(os.path.join(self.path, "rig"))  # type:str
        self.settings = fileFn.create_missing_dir(os.path.join(self.path, "settings"))  # type:str
        self.weights = _weightsDirectorySctruct(self.path)
        self.data = _dataDirectoryStruct(self.path)
        self.mapping = _mappingFiles(self.data)

        # Copy empty scenes
        fileFn.copy_empty_scene(os.path.join(self.skeleton, "{0}_skeleton.0000.ma".format(self.name)))
        fileFn.copy_empty_scene(os.path.join(self.rig, "{0}_rig.0000.ma".format(self.name)))

        # Set env variables and update hud
        Asset._INSTANCE = self
        self.current_project.update_meta()
        self.update_meta()
        # Update hude
        LunaHUD.refresh()

    @property
    def meta_path(self):
        path = os.path.join(self.path, self.name + ".meta")  # type:str
        path = os.path.normpath(path)
        return path

    @property
    def meta_data(self):
        meta_dict = {}
        if os.path.isfile(self.meta_path):
            meta_dict = fileFn.load_json(self.meta_path)
        return meta_dict

    @property
    def latest_skeleton_path(self):
        path = fileFn.get_latest_file("{0}_skeleton".format(self.name), self.skeleton, extension="ma", full_path=True, split_char=".")  # type: str
        return path

    @property
    def new_skeleton_path(self):
        path = fileFn.get_new_versioned_file("{0}_skeleton".format(self.name), self.skeleton, extension="ma", full_path=True, split_char=".")  # type: str
        return path

    @property
    def latest_rig_path(self):
        path = fileFn.get_latest_file("{0}_rig".format(self.name), self.rig, extension="ma", full_path=True, split_char=".")  # type: str
        return path

    @property
    def new_rig_path(self):
        path = fileFn.get_new_versioned_file("{0}_rig".format(self.name), self.rig, extension="ma", full_path=True, split_char=".")  # type: str
        return path

    @property
    def latest_build_path(self):
        path = fileFn.get_latest_file(self.name, self.build, extension="rig", full_path=True, split_char=".")  # type: str
        return path

    @property
    def new_build_path(self):
        path = fileFn.get_new_versioned_file(self.name, self.build, extension="rig", full_path=True, split_char=".")  # type: str
        return path

    @property
    def model_path(self):
        path = self.meta_data.get("model", "")  # type:str
        return path

    def set_data(self, key, value):
        data = self.meta_data
        data[key] = value
        data["modified"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        fileFn.write_json(self.meta_path, data)

    def update_meta(self):
        meta_dict = self.meta_data
        meta_dict["name"] = self.name
        meta_dict["type"] = self.type
        meta_dict["modified"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        meta_dict["model"] = meta_dict.get("model", "")
        if not meta_dict.get("created", ""):
            meta_dict["created"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        fileFn.write_json(self.meta_path, meta_dict)


class _weightsDirectorySctruct:
    """Directory scruct with folder per weight type"""

    def __init__(self, root):
        self.blendshape = fileFn.create_missing_dir(os.path.join(root, "weights", "blendshape"))  # type:str
        self.delta_mush = fileFn.create_missing_dir(os.path.join(root, "weights", "delta_mush"))  # type:str
        self.ffd = fileFn.create_missing_dir(os.path.join(root, "weights", "ffd"))  # type:str
        self.ncloth = fileFn.create_missing_dir(os.path.join(root, "weights", "ncloth"))  # type:str
        self.skin = fileFn.create_missing_dir(os.path.join(root, "weights", "skin"))  # type:str
        self.nonlinear = fileFn.create_missing_dir(os.path.join(root, "weights", "nonlinear"))  # type:str
        self.tension = fileFn.create_missing_dir(os.path.join(root, "weights", "tension"))  # type:str
        self.soft_mod = fileFn.create_missing_dir(os.path.join(root, "weights", "soft_mod"))  # type:str
        self.dsAttract = fileFn.create_missing_dir(os.path.join(root, "weights", "dsAttract"))  # type:str
        self.ng_layers = fileFn.create_missing_dir(os.path.join(root, "weights", "ng_layers"))  # type:str
        self.ng_layers2 = fileFn.create_missing_dir(os.path.join(root, "weights", "ng_layers2"))  # type:str


class _dataDirectoryStruct:
    """Directory struct with folder per data type."""

    def __init__(self, root):
        self.blendshapes = fileFn.create_missing_dir(os.path.join(root, "data", "blendshapes"))  # type:str
        self.driven_poses = fileFn.create_missing_dir(os.path.join(root, "data", "driven_poses"))  # type:str
        self.sdk_correctives = fileFn.create_missing_dir(os.path.join(root, "data", "sdk_correctives"))  # type:str
        self.xgen = fileFn.create_missing_dir(os.path.join(root, "data", "xgen"))  # type:str
        self.mocap = fileFn.create_missing_dir(os.path.join(root, "data", "mocap"))  # type:str
        self.psd = fileFn.create_missing_dir(os.path.join(root, "data", "psd"))  # type:str


class _mappingFiles:
    def __init__(self, data_struct):
        self.blendshapes = fileFn.create_file(os.path.join(data_struct.blendshapes, "mapping.json"), data=r"{}")
