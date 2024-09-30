# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

class Singleton:
    """Singleton class.

    In the child class must be used constructor of type:

    def __init__(self):
        if not self._initialized:
            ...
            your code
            ...
            self._initialized = True
    """

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):  # noqa: D102
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
