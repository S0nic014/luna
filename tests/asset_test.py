import os
import unittest
from luna.workspace.asset import Asset
from luna.workspace.project import Project
from luna.static import directories
from luna.test import TestCase


class AssetTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super(AssetTests, cls).tearDownClass()
        Project.exit()

    def test_asset_ctor(self):
        asset_type = "character"

        creation_path = AssetTests.get_temp_dirname("testProject")
        test_project = Project.create(creation_path, silent=True)
        test_asset = Asset(test_project, "testAsset", typ=asset_type)
        dummy_model_path = os.path.join(directories.LUNA_ROOT_PATH, "tests", "util_files", "mannequin_model.ma")
        test_asset.set_data("model", dummy_model_path)

        # Base Assertions
        self.assertTrue(os.path.isdir(test_asset.path))  # Asset folder created
        self.assertTrue(os.path.isfile(test_asset.meta_path))  # Meta data file created
        self.assertEqual(test_asset.name, "testAsset")  # Asset name is stored
        self.assertTrue(os.path.isdir(os.path.join(test_project.path, asset_type + "s")))  # Asset category folder is created
        # Check asset folders creations
        self.assertTrue(os.path.isdir(test_asset.controls))
        self.assertTrue(os.path.isdir(test_asset.skeleton))
        self.assertTrue(os.path.isdir(test_asset.rig))
        self.assertTrue(os.path.isdir(test_asset.settings))
        self.assertTrue(os.path.isdir(test_asset.weights.blendshape))
        self.assertTrue(os.path.isdir(test_asset.weights.delta_mush))
        self.assertTrue(os.path.isdir(test_asset.weights.dsAttract))
        self.assertTrue(os.path.isdir(test_asset.weights.ffd))
        self.assertTrue(os.path.isdir(test_asset.weights.ncloth))
        self.assertTrue(os.path.isdir(test_asset.weights.ng_layers))
        self.assertTrue(os.path.isdir(test_asset.weights.ng_layers2))
        self.assertTrue(os.path.isdir(test_asset.weights.nonlinear))
        self.assertTrue(os.path.isdir(test_asset.weights.skin))
        self.assertTrue(os.path.isdir(test_asset.weights.soft_mod))
        self.assertTrue(os.path.isdir(test_asset.weights.tension))
        self.assertTrue(os.path.isdir(test_asset.data.blendshapes))
        self.assertTrue(os.path.isdir(test_asset.data.mocap))
        self.assertTrue(os.path.isdir(test_asset.data.driven_poses))
        self.assertTrue(os.path.isdir(test_asset.data.xgen))
        self.assertTrue(os.path.isdir(test_asset.data.sdk_correctives))
        self.assertTrue(os.path.isdir(test_asset.data.psd))

        # Template files creation
        self.assertTrue(os.path.isfile(os.path.join(test_asset.skeleton, "{0}_skeleton.0000.ma".format(test_asset.name))))
        self.assertTrue(os.path.isfile(os.path.join(test_asset.rig, "{0}_rig.0000.ma".format(test_asset.name))))


if __name__ == "__main__":
    unittest.main(exit=False)
