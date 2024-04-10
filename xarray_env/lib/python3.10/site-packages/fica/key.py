"""Configuration keys"""

from typing import Any, Callable, Optional, Tuple, Type, Union

from .config import Config
from .validators import _Validator


class _Empty:
    """
    A singleton object representing an empty value.
    """

    def __repr__(self) -> str:
        return "fica.EMPTY"


class _Subkeys():
    """
    A singleton object representing that a key's subkeys should be its default value.
    """

    def __repr__(self) -> str:
        return "fica.SUBKEYS"


EMPTY = _Empty()
SUBKEYS = _Subkeys()


class Key:
    """
    A class representing a key in a configuration.

    Keys have a default value, specified with the ``default`` argument.

    - If ``default`` is :py:data:`fica.EMPTY`, then the key is not included in the resulting
      configuration unless the user specifies a value.
    - If ``default`` is :py:data:`fica.SUBKEYS`, then the key is defaulted to a dictionary
      containing each subkey with its default unless the user specifies
      a value.
    - Otherwise, the key is mapped to the value of ``default``.

    If ``default`` is :py:data:`fica.EMPTY` and subkeys are provided, ``default`` is
    automatically set to :py:data:`fica.SUBKEYS`.

    To create a new default value for each key value, pass a 0-argument function to ``factory``.
    This function will be called each time a :py:class:`fica.Config` is created to set the value of
    the key if no value is specified by the user.

    Args:
        description (``str | None``): a description of the configuration for documentation
        default (``object``): the default value of the key
        type_ (``type | tuple[type]``): valid type(s) for the value of this configuration
        allow_none (``bool``): whether ``None`` is a valid value for the configuration
        validator (validator or ``None``): a validator for validating user-specified values
        subkey_container (subclass of :py:class:`fica.Config`): an (uninstantiated) config class
            containing the subkeys of this key
        enforce_subkeys (``bool``): whether to enforce the use of the subkey container if any
        name (``str | None``): a name to look for in the user config (if different from the
            attribute name on the :py:class:`fica.Config` object)
        factory (``callable[[], object] | None``): a factory used to create the default value of the key
    """

    description: Optional[str]
    """a description of the configuration for documentation"""

    default: Optional[Any]
    """the default value of the key"""

    type_: Optional[Union[Type, Tuple[Type]]]
    """valid type(s) for the value of this configuration"""

    allow_none: bool
    """whether ``None`` is a valid value for the configuration"""

    validator: Optional[_Validator]
    """a validator for user-specified values"""

    subkey_container: Optional[Type[Config]]
    """a config class containing the subkeys of this key"""

    enforce_subkeys: bool
    """whether to enforce the use of the subkey container if any"""

    name: Optional[str]
    """the name of this key in the user config (if different from the attribute name)"""

    factory: Optional[Callable[[], Any]]
    """a factory used to create the default value"""

    def __init__(
        self,
        description: Optional[str] = None,
        default: Optional[Any] = None,
        type_: Optional[Union[Type, Tuple[Type]]] = None,
        allow_none: bool = False,
        validator: Optional[_Validator] = None,
        subkey_container: Optional[Type[Config]] = None,
        enforce_subkeys: bool = False,
        name: Optional[str] = None,
        factory: Optional[Callable[[], Any]] = None,
    ) -> None:
        if type_ is not None:
            if not (isinstance(type_, Type) or (isinstance(type_, tuple) and \
                    all(isinstance(e, Type) for e in type_))):
                raise TypeError("type_ must be a single type or tuple of types")

            if default is not SUBKEYS and \
                    not (isinstance(default, type_) or (allow_none and default is None)):
                raise TypeError("The default value is not of the specified type(s)")

        if isinstance(default, dict):
            raise TypeError("The default value cannot be a dictionary; use subkeys instead")

        if validator is not None and not isinstance(validator, _Validator):
            raise TypeError("validator is not a valid validator")

        if subkey_container is not None and not issubclass(subkey_container, Config):
            raise TypeError("The provided subkey_container is not a subclass of fica.Config")

        if default is None and subkey_container is not None:
            default = SUBKEYS

        if default is SUBKEYS and subkey_container is None:
            raise ValueError("Cannot default to subkeys when no subkey_container is provided")

        if enforce_subkeys and subkey_container is None:
            raise ValueError("Cannot enforce subkeys when no subkey container is provided")

        if factory is not None and (default is not None or subkey_container is not None):
            raise ValueError("Cannot specify a factory with a default of subkey_container")

        self.description = description
        self.default = default
        self.type_ = type_
        self.allow_none = allow_none
        self.validator = validator
        self.subkey_container = subkey_container
        self.enforce_subkeys = enforce_subkeys
        self.name = name
        self.factory = factory

    def get_description(self) -> Optional[str]:
        """
        Get the description of the key.

        Returns:
            ``str | None``: the description of the key
        """
        return self.description

    def get_subkey_container(self) -> Optional[Type[Config]]:
        """
        Get the subkey container class.

        Returns:
            subclass of :py:class:`fica.Config`: the uninstantiated subkey container class
        """
        return self.subkey_container

    def get_name(self, attr_name: str) -> str:
        """
        Determine the name of this key in the user configuration.

        Args:
            attr_name (``str``): the name of the attribute of this key in the
                :py:class:`fica.Config` object

        Returns:
            ``str``: the name of the key
        """
        return self.name if self.name is not None else attr_name

    def use_default(self, user_value: Any = EMPTY) -> bool:
        """
        Determine whether the default value for this key will be used given the user-specified
        value.

        Args:
            user_value (``object``): the value specified by the user

        Returns:
            ``bool``: whether the default value will be used
        """
        return user_value is EMPTY

    def get_value(self, user_value: Any = EMPTY, require_valid_keys: bool = False) -> Any:
        """
        Get the value of this key taking into account the value specified by the user, if any.

        Args:
            user_value (``object``): the value specified by the user
            require_valid_keys (``bool``): whether to require that all keys in the user config are
                valid in the subkey container, if applicable

        Returns:
            ``object``: the value of the key, taking into account the user-specified value

        Raises:
            ``TypeError``: if the user-specified value is not of the correct type
            ``ValueError``: if the user-specified value fails validation
        """
        if self.use_default(user_value):
            if self.default is SUBKEYS:
                return self.subkey_container(require_valid_keys=require_valid_keys)

            elif self.factory:
                return self.factory()

            else:
                return self.default

        else:
            if not ((self.type_ is None or isinstance(user_value, self.type_)) or \
                    (self.allow_none and user_value is None)):
                raise TypeError("User-specified value is not of the correct type")

            # validate the value
            if self.validator is not None:
                err = self.validator.validate(user_value)
                if err is not None:
                    raise ValueError(f"User-specified value failed validation: {err}")

            # handle user-inputted dict w/ missing subkeys
            if self.subkey_container is not None:
                if isinstance(user_value, dict):
                    return self.subkey_container(user_value, require_valid_keys=require_valid_keys)

                elif self.enforce_subkeys:
                    raise ValueError("Cannot override subkeys for a key with enforced subkeys")

            return user_value

    def get_default(self) -> Any:
        """
        Get the default valu of this key.

        If the default is a subkey container instance or a factory function, it is
        re-instantiated/called, meaning that new instances/return values are returned for each call.

        Returns:
            ``object``: the default value of the key.
        """
        return self.get_value()

    def should_document_subkeys(self) -> bool:
        """
        Determine whether this key has subkeys that should be documented.

        Returns:
            ``bool``: whether this class has subkeys that should be documented
        """
        return self.subkey_container is not None
