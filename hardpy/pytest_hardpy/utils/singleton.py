# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class SingletonMeta(type, Generic[T]):  # noqa: D101
    _instances: dict[SingletonMeta[T], T] = {}  # noqa: RUF012

    def __call__(cls, *args, **kwargs) -> T:  # noqa: ANN002, ANN003
        """Magic method to create an instance of the class.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        Returns:
            object: An instance of the class
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(
                *args,
                **kwargs,
            )
        return cls._instances[cls]

    def __instancecheck__(cls, instance: object) -> bool:
        return cls.__subclasscheck__(type(instance))
