# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from .network import HTTPXClient
from .object_factory import ObjectFactory


class DictField:
    """Data descriptor class for Dict data.

    Data descriptor that provides a shortcut for
    getting/setting a specific key on a ``UserDict``
    data attribute.
    """

    def __get__(self, obj, objtype=None):
        """Get the key value."""
        if obj is None:
            return self
        return self.get_key(obj)

    def __set__(self, obj, value):
        """Set the key value."""
        self.set_field(obj, value)

    def __init__(self, key, default=None, create_if_missing=True):
        """Initializer

        Args:
            key (str): Path where data will be stored in the
                       object data (dot notation by ``pydash``).

            default (object): Default value used when the field is
                              not defined.
        """
        self._key = key
        self._default = default

        self._create_if_missing = create_if_missing

    def get_key(self, obj):
        """Access data field."""
        if not py_.has(obj.data, self._key) and self._create_if_missing:
            self.set_field(obj, self._default)

        return py_.get(obj.data, self._key, self._default)

    def set_field(self, obj, value):
        """Set data field value"""
        return py_.set_(obj.data, self._key, value)


class ObjectField(DictField):
    """Object data field.

    Data descriptor that provides a shortcut for
    getting/setting a specific key on a ``UserDict``
    data attribute. The retrieved values are
    mutated in a ``User-Defined Class`` type.

    Note:
        Since this class uses the ``ObjectFactory``
        all classes used in this field must be
        registered in the factory object.
    """

    def __get__(self, obj, objtype=None):
        """Get the key value."""
        objdata = super().__get__(obj)
        return self.resolve_class(objdata)

    def __init__(self, key, class_name, default=None):
        """Initializer"""
        super(ObjectField, self).__init__(key, default)
        self._class_name = class_name

    def resolve_class(self, obj):
        """Resolve a data dictionary in a ``valid class``."""
        return ObjectFactory.resolve(self._class_name, obj)


class ObjectCollectionField(ObjectField):
    """Object Collection data field.

    Collection of objects with same type.
    """

    def __get__(self, obj, objtype=None):
        """Get the key value."""
        objdata = self.get_key(obj)
        return py_.map(objdata, lambda data: self.resolve_class(data))


class LinkField(ObjectField):
    """Link data field.

    Data descriptor that resolve a link
    in a ``User-Defined class`` object.
    """

    def resolve_link(self, model: "BaseModel", http_method="GET"):
        """Resolve a link."""
        model.has_field(self._key)

        response = HTTPXClient.request(http_method, model.get_field(self._key)).json()
        if py_.has(response, "hits.hits"):  # for the `version` attribute
            return [
                ObjectFactory.resolve(self._class_name, r)
                for r in py_.get(response, "hits.hits")
            ]

        return ObjectFactory.resolve(self._class_name, response)

    def __get__(self, obj, objtype=None):
        """Get the key value."""
        return self.resolve_link(obj)
