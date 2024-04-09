"""Config exporters for different formats"""

import json
import yaml

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Type

from .config import Config
from .key import Key


def infer_indentation(l: str) -> str:
    """
    Infer the indentation of a string by returning all of its leading whitespace.
    """
    for i in range(1, len(l)):
        if not l[:i].isspace():
            return l[:i-1]
    return l


@dataclass
class Description:
    """
    A container for a description line.
    """

    text: str
    """the text of the description"""

    is_default: Optional[bool] = None
    """whether this line is the default value of a subkey container"""


class ConfigExporter(ABC):
    """
    An abstract base class that converts a :py:class:`fica.Config` object into a documentation
    string.
    """

    @classmethod
    def recursively_populate_config_dict(cls, instc: Config, d: Dict[str, Tuple[str, Any]]) -> None:
        """
        Populate a dictionary with the values for each key in the provided :py:class:`fica.Config`
        instance, recursing into nested :py:class:`fica.Config` objects.

        Args:
            instc (:py:class:`fica.Config`): an instance of a :py:class:`fica.Config` subclass
            d (``dict[str, object]``): the dictionary to populate with the default values
        """
        for n, a in instc._get_names_to_attrs().items():
            v = getattr(instc, a)
            skc = getattr(type(instc), a).get_subkey_container()
            if skc:
                subd = {}
                cls.recursively_populate_config_dict(skc(documentation_mode=True), subd)
                v = subd
            d[a] = (n, v)

    @classmethod
    def config_to_dict(cls, config: Type[Config]) -> Dict[str, Tuple[str, Any]]:
        """
        Create a dictionary mapping each key attribute name to a tuple containing its name in the
        user config and its default value (or a dictionary of default values in the case of subkeys)
        for the provided :py:class:`fica.Config` subclass.

        Args:
            config (``type[Config]``): the :py:class:`fica.Config` subclass

        Returns:
            ``dict[str, tuple[str, object]]``: the generated dictionary
        """
        instc = config(documentation_mode=True)
        d = {}
        cls.recursively_populate_config_dict(instc, d)
        return d

    @property
    @abstractmethod
    def comment_char(self) -> str:
        """
        the character(s) used to delimit comments in the language represented by this exporter
        """
        raise NotImplementedError()

    def get_descriptions(self, config: Type[Config], config_dict: Dict[str, Tuple[str, Any]]) -> \
            List[Description]:
        """
        Get a list of description strings for each configuration in ``config_dict``.

        The list returned also includes descriptions for subkeys recursed into, and elements are
        added to it using the DFS iteration order of ``config_dict``.

        Args:
            config (:py:class:`fica.Config`): the config object being converted
            config_dict (``dict[str, tuple[str, object]]``): the dictionary of default
                configurations

        Returns:
            ``list[Description]``: the list of descriptions for each key and subkey in
                ``config_dict``
        """
        descriptions = []
        for a, (_, v) in config_dict.items():
            key: Key = getattr(config, a)
            descriptions.append(Description(key.get_description()))

            default = key.get_default()
            if key.get_subkey_container() and not isinstance(default, key.get_subkey_container()):
                descriptions.append(Description(f"Default value: {self.export_primitive(default)}", is_default=True))

            if key.should_document_subkeys():
                subkey_descriptions = \
                    self.get_descriptions(key.get_subkey_container(), v)
                descriptions.extend(subkey_descriptions)

        return descriptions

    def add_descriptions(self, lines: List[str], descriptions: List[Description]) -> List[str]:
        """
        Add descriptions to lines of configurations as comments.

        The strings in lines are all padded to the same length so that the comment characters on
        each line line up vertically. Descriptions are added after the comment characters.

        Args:
            lines (``list[str]``): the lines of code that descriptions should be added to
            descriptions (``list[Description]``): the list of descriptions for each line in
                ``lines``

        Returns:
            ``list[str]``: a list of each line with its description appended
        """
        pad_to = max(len(l) for l in lines) + 1
        pad_line = lambda l: l + " " * (pad_to - len(l))
        concat_line = lambda l, d: l if d is None else pad_line(l) + " " + self.comment_char + " " + d

        ret, iter_d = [], iter(descriptions)
        for l in lines:
            if self.should_add_description(l):
                d = next(iter_d)

                while d.is_default:
                    ret.append(infer_indentation(l) + self.comment_char + " " + d.text)
                    d = next(iter_d)

                l = concat_line(l, d.text)

            ret.append(l)

        return ret

    def should_add_description(self, line: str) -> bool:
        """
        Determine whether the provided line represents a key and should have a description appended
        to it.

        Args:
            line (``str``): the line to check

        Returns:
            ``bool``: whether a description should be appended to the line
        """
        return True

    @abstractmethod
    def export_primitive(self, value: Any) -> str:
        """
        Export a primitive value.
        """
        raise NotImplementedError()

    @abstractmethod
    def export(self, config: Type[Config]) -> str:
        """
        Export a :py:class:`fica.Config` subclass to a block of code with descriptions as comments.
        """
        raise NotImplementedError()

    @classmethod
    def config_dict_to_user_config(cls, config_dict: Dict[str, Tuple[str, Any]]) -> Dict[str, Any]:
        """
        Convert ``config_dict`` to a valid user config.
        """
        return {n: (cls.config_dict_to_user_config(v) if isinstance(v, dict) else v) for _, (n, v) \
            in config_dict.items()}


class JsonExporter(ConfigExporter):
    """
    A configuration exporter that displays its configurations as JSON.
    """

    comment_char = "//"

    def should_add_description(self, line: str) -> bool:
        return ":" in line

    def export_primitive(self, value: Any) -> str:
        return json.dumps(value)

    def export(self, config: Type[Config]) -> str:
        config_dict = self.config_to_dict(config)
        descriptions = self.get_descriptions(config, config_dict)
        conf_str = json.dumps(self.config_dict_to_user_config(config_dict), indent=2)
        lines = conf_str.split("\n")
        lines[1:-1] = self.add_descriptions(lines[1:-1], descriptions)
        return "\n".join(lines)


class YamlExporter(ConfigExporter):
    """
    A configuration exporter that displays its configurations as YAML.
    """

    comment_char = "#"

    def export_primitive(self, value: Any) -> str:
        out = yaml.dump(value)
        if out.endswith("\n...\n"):
            out = out[:-5]
        return out

    def export(self, config: Type[Config]) -> str:
        config_dict = self.config_to_dict(config)
        descriptions = self.get_descriptions(config, config_dict)
        conf_str = yaml.dump(
            self.config_dict_to_user_config(config_dict),
            indent=2,
            sort_keys=False,
        ).strip()
        return "\n".join(self.add_descriptions(conf_str.split("\n"), descriptions))


EXPORTER_CLASSES = {
    "json": JsonExporter,
    "yaml": YamlExporter,
}
"""a dictionary mapping exporter names to their classes"""


def create_exporter(exporter_type: str, **kwargs) -> ConfigExporter:
    """
    Create an instance of the specified exporter type.

    Args:
        exporter_type (``str``): the name of the exporter to create; should be a key in
            :py:obj:`EXPORTER_CLASSES`
        **kwargs: keyword arguments passed to the :py:class:`ConfigExporter` constructor

    Returns:
        :py:class:`ConfigExporter`: the instantiated exporter

    Raises:
        ``ValueError``: if there is no exporter of the specified type
    """
    if exporter_type not in EXPORTER_CLASSES:
        raise ValueError(f"There is no exporter of type {exporter_type}")

    return EXPORTER_CLASSES[exporter_type](**kwargs)
