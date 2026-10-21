# coding=utf8
"""jobject

jobject: A dictionary replacement that gives additional access to data using C
struct notation, just like JavaScript Objects
"""
from __future__ import annotations

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-24"

# Python imports
import sys
from typing import Iterable, Mapping

class jobject(dict):
	"""jobject

	Class that represents the dict

	jobject()
		new empty object

	jobject(mapping)
		new object initialized from a mapping object's (key, value) pairs

	jobject(iterable)
		new object initialized as if via:
			d = {} for k, v in iterable:
				d[k] = v

	jobject(**kwargs)
		new object initialized with the name=value pairs in the keyword
		argument list. For example: jobject(one=1, two=2)

	Extends:
		dict
	"""

	def __init__(self, *args: Mapping | Iterable[tuple], **kwargs: any):
		"""Constructor

		Arguments
			*args (Mapping | Iterable[tuple]): One or more mappings or iterables
				of (key, value) pairs to initialize the jobject with. Processed
				in order
			**kwargs (any): Additional name/value pairs to set as keys on the
				jobject

		Returns:
			jobject
		"""
		self.update(*args, **kwargs)

	def __delattr__(self, name: str) -> any:
		"""Delete Attribute

		Implements Python magic method __delattr__ to give object notation
		access to dictionaries

		Arguments:
			name (str): The dict key to delete

		Raises:
			AttributeError

		Returns:
			any
		"""
		try:
			return self.__delitem__(name)
		except KeyError:
			raise AttributeError(name)

	def __getattr__(self, name: str) -> any:
		"""Get Attribute

		Implements Python magic method __getattr__ to give object notation
		access to dictionaries

		Arguments:
			name (str): The dict key to get

		Raises:
			AttributeError

		Returns:
			any
		"""
		try:
			return self.__getitem__(name)
		except KeyError:
			raise AttributeError(name)

	def __ior__(self, other: dict | jobject) -> jobject:
		"""In Place Bitwise operator

		Handles merging a new dict with this instance.

		Arguments:
			other (jobject | dict): The other data to merge in
		"""

		# Update with the other Mapping
		self.update(other)

		# Return itself
		return self

	def __setattr__(self, name: str, value: any) -> None:
		"""Set Attribute

		Implements Python magic method __setattr__ to give object notation
		access to dictionaries

		Arguments:
			name (str): The key in the dict to set
			value (any): The value to set on the key
		"""
		super().__setitem__(name, self.convert(value))

	def __setitem__(self, key: any, value: any) -> None:
		"""Set Item

		Implements Python magic method __setitem__ in order to override the
		base setting of items on the instances. We want to make sure anything
		passed to this that has a dict is converted to a jobject

		Arguments:
			key (any): The key to store the value under
			value (any): The value to set

		Returns:
			None
		"""
		super().__setitem__(key, self.convert(value))

	def copy(self) -> jobject:
		"""Copy

		Makes sure to return a copy of jobject and not dict

		Returns:
			jobject
		"""
		return self.__class__(self)

	@classmethod
	def convert(cls, value: any) -> any:
		"""Convert

		Takes a value and makes sure it, or any children within it, that are
		dict instances, are turned into jobject instances instead

		Arguments:
			value (any): The value to convert

		Returns:
			jobject | any
		"""

		# If we got a jobject, return it as is
		if isinstance(value, cls):
			return value

		# If we got a dict, convert it to a jobject
		if isinstance(value, dict):
			return cls(value)

		# If we got a list
		if isinstance(value, list):
			return [ cls.convert(v) for v in value ]

		# If we got a tuple
		if isinstance(value, tuple):
			return tuple( cls.convert(v) for v in value )

		# Whatever we have, return it as is
		return value

	@classmethod
	def fromkeys(cls, iterable: Iterable, value: any = None):
		"""From Keys

		Creates a new jobject with all keys set to value.

		Arguments:
			iterable (Iterable): The list of keys
			value (any): Optional value to set, or None

		Returns:
			jobject
		"""

		# Convert the value once
		v = cls.convert(value)

		# Create a new jobect
		o = cls()

		# Set each key
		for k in iterable:
			o[k] = v

		# Return the new instance
		return o

	@classmethod
	def revert(cls, value: any) -> any:
		"""Revert

		Does the opposite of convert

		Arguments
			value (any): A value to revert

		Returns:
			any
		"""

		# If we got a jobject, return it as is
		if isinstance(value, cls):
			return value.to_dict()

		# Defensive: in case of dict C-level issues
		if isinstance(value, dict):
			return { k: cls.revert(v) for k,v in value.items() }

		# If we got a list, create a new one from reverted values
		if isinstance(value, list):
			return [ cls.revert(v) for v in value ]

		# If we got a tuple
		if isinstance(value, tuple):
			return tuple( cls.revert(v) for v in value )

		# Whatever we have, return it as is
		return value

	def setdefault(self, key, default = None) -> any:
		"""Set Default

		Returns a key whether it exists or not, returning the default if it
		does not.

		Arguments:
			key (str): The name of the key to get/set
			default (any): The default value to set if the key does not exist

		Returns:
			any
		"""
		if key not in self:
			super().__setitem__(key, self.convert(default))
		return self[key]

	def to_dict(self) -> dict:
		"""To Dict

		Returns the underlining dict of the instance

		Returns:
			dict
		"""

		# Init a new dict
		return { k: self.revert(self[k]) for k in self }

	def update(self, *args: Mapping | Iterable[tuple], **kwargs: any):
		"""Update

		Handles multiple keys changed.

		Arguments
			*args (Mapping | Iterable[tuple]): One or more mappings or iterables
				of (key, value) pairs to initialize the jobject with. Processed
				in order
			**kwargs (any): Additional name/value pairs to set as keys on the
				jobject
		"""
		for k, v in dict(*args, **kwargs).items():
			self[k] = v

# Allow use of import jobject instead of from jobject import jobject
if sys.modules[__name__] is jobject:
	pass
else:
	sys.modules[__name__] = jobject
	sys.modules[__name__].jobject = jobject