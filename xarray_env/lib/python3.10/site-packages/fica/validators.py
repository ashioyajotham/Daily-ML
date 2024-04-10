"""User-specified value validators"""

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional


class _Validator(ABC):
    """
    An abstract base class for validators of user-specified configuration values.
    """

    @abstractmethod
    def validate(self, value: Any) -> Optional[str]:
        """
        Validate the specified value.

        If the value is valid, this method returns ``None``. Otherwise, it returns a string with an
        error message that is displayed to the user.

        Args:
            value (``object``): the value to validate

        Returns:
            ``str | None``: whether the value is valid
        """
        raise NotImplementedError


class choice(_Validator):
    """
    A validator that asserts that a value is one of a pre-defined set of options.

    Args:
        choices (``list[object]``): the list of valid options

    Raises:
        ``TypeError``: if ``choices`` is not a ``list``
    """

    _choices: List[Any]
    """the list of valid options"""

    def __init__(self, choices: List[Any]) -> None:
        if not isinstance(choices, list):
            raise TypeError("choices is not a list")

        self._choices = choices

    def validate(self, value: Any) -> Optional[str]:
        if value not in self._choices:
            as_str = lambda v: "'" + v + "'" if isinstance(v, str) else str(v)
            choices = '{' + ', '.join(as_str(c) for c in self._choices) + '}'
            value = as_str(value)
            return f"{value} is not one of {choices}"


class validator(_Validator):
    """
    A decorator for custom validation functions.

    The decorated function should return ``None`` if the value passed to it is valid,
    otherwise it should return a string with an error message that will be displayed to the user. If
    the return type of the function is not ``str | None``, a ``TypeError`` is raised.

    Args:
        validation_func (``callable[[object], bool]``): the validation function
    """

    _func: Callable[[Any], bool]
    """the validation function"""

    def __init__(self, validation_func: Callable[[Any], bool]) -> None:
        self._func = validation_func

    def validate(self, value: Any) -> Optional[str]:
        ret = self._func(value)
        if ret is not None and not isinstance(ret, str):
            raise TypeError("The validation function did not return a string or None")

        return ret
