import tkinter as tk
import logging


class Attributes():
    def __init__(self, attrs, default):
        """
        Base Attribute class that acts as an interface between the game controller
        and other components.

        `attrs`: dict with `key: value` pair for each attribute

        `default`: either "auto" or some value
        """
        if type(attrs) not in [dict, None]:
            raise TypeError
        if attrs is None:
            attrs = {}

        self.attrs = attrs
        self.default = default

    def _get_obj(self, key):
        if key in self.attrs:
            return self.attrs[key]
        else:
            return self._get_default(key)


class FuncAttributes(Attributes):
    def __init__(self, attrs: dict = None, default = "auto"):
        """
        Function Attributes class that contains functions to pass
        between components.
        """
        super().__init__(attrs, default)

    def get_func_obj(self, key):
        return self._get_obj(key)

    def exec(self, key, *args, **kwargs):
        func = self._get_obj(key)
        return func(*args, **kwargs)

    def _get_default(self, key):
        if self.default == "auto":
            def no_func(*args, **kwargs):
                logging.warn(f"{key} is not defined")
            self.default = no_func
        return self.default


class VarAttributes(Attributes):
    def __init__(self, attrs: dict = None, default = "auto"):
        """
        Variable Attributes class that contains variables to pass
        between components.
        """
        super().__init__(attrs, default)

    def get_var_obj(self, key):
        return self._get_obj(key)

    def get_value(self, key):
        val = self._get_obj(key)
        if issubclass(type(val), tk.Variable):
            val = val.get()
        return val

    def _get_default(self, key):
        if self.default == "auto":
            self.default = f"<{key} is not defined>"
        return self.default
