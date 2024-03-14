"""Custom build script for hatch backend"""
import os

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomHook(BuildHookInterface):
    """A custom build hook for nbconvert."""

    def initialize(self, version, build_data):
        """Initialize the hook."""
        if self.target_name not in ["sdist"]:
            return

        build_dir = os.getcwd()
        os.chdir('hardpy/hardpy_panel/frontend')
        os.system('yarn')
        os.system('yarn build')
        os.chdir(build_dir)
