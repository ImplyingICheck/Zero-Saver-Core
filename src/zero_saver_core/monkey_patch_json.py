# Copyright 2023 The Zero Saver Authors. All Rights Reserved.
#
# This file is part of Zero Saver.
#
# Zero Saver is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Zero Saver is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Zero Saver. If not, see <https://www.gnu.org/licenses/>.
"""Monkey patches the python module to used Decimals over floats. Additionally,
white space formatting is changed as follows, with priority in order of writing:
If empty "{}" or "[]" write "{ }" or "[ ]" respectively.
Insert a space after every "{" and "[".
Insert a space before every "}" and "}"."""
from __future__ import annotations

import cmath
import decimal
import importlib
import json.encoder
import re
from collections.abc import Generator
from importlib.resources import Package
from typing import Any, Callable, Mapping, TypeVar

# pylint: skip-file
# pyright: ignore
# pyright: ignore[reportGeneralTypeIssues]
# pyright: ignore[reportUnboundVariable]
# Check if c implementation is available. Should be None to ensure the patch is
# used.
c_make_encoder: Package | None = None
# __format_spec passed to builtins.format() for decimals near 0 (but not 0.0)
ZERO_SIEVERT_FLOAT_PRECISION = 'e'
# Absolute tolerance value for when to write a decimal using
# ZERO_SIEVERT_FLOAT_PRECISION defined style
ABS_TOL = 9e-05


def format_with_two_digits_after_e(
    value: decimal.Decimal,
    format_str: str = ZERO_SIEVERT_FLOAT_PRECISION,
) -> str:
  formatted_decimal = format(value, format_str)
  mantissa, exponent = formatted_decimal.split('e')
  return f'{mantissa}e{int(exponent):+03}'


def is_almost_zero(o: decimal.Decimal) -> bool:
  return (
      cmath.isclose(
          o,
          0,
          rel_tol=0,
          abs_tol=ABS_TOL,
      )
      and str(o) != '0.0'
  )


class _JsonDecimal(float):
  """Wraps a decimal.Decimal in a float.

  Used to monkey patch the json module.
  DO NOT USE OUTSIDE OF monkey_patch_json.py"""

  def __init__(self, decimal_value: decimal.Decimal):
    self._disguised_decimal = decimal_value

  def __repr__(self) -> str:
    try:
      if is_almost_zero(self._disguised_decimal):
        return format_with_two_digits_after_e(self._disguised_decimal)
      else:
        return self._disguised_decimal.__str__()
    except ValueError:
      return super().__repr__()


"""!!!!!!!!!START SOURCE CODE FROM PYTHON!!!!!!!!!!!"""


class MonkeyPatchedJsonEncoder(json.JSONEncoder):

  def iterencode(
      self, o: Any, _one_shot: bool = False
  ) -> Generator[str | Generator[str, Any, None], Any, Any]:
    """Encode the given object and yield each string
    representation as available.

    For example::

        for chunk in JSONEncoder().iterencode(bigobject):
            mysocket.write(chunk)

    """
    # pylint: disable=[invalid-name]
    if self.check_circular:
      markers = {}
    else:
      markers = None
    if self.ensure_ascii:
      _encoder = (
          json.encoder.encode_basestring_ascii
      )  # pyright: ignore[reportGeneralTypeIssues]
    else:
      _encoder = (
          json.encoder.encode_basestring
      )  # pyright: ignore[reportGeneralTypeIssues]

    def floatstr(
        o,
        allow_nan=self.allow_nan,
        _repr=_JsonDecimal.__repr__,  # line modified
        _inf=json.encoder.INFINITY,
        _neginf=-json.encoder.INFINITY,
    ):
      # pylint: disable=[invalid-name]
      # Check for specials.  Note that this type of test is processor
      # and/or platform-specific, so do tests which don't depend on the
      # internals.

      if o != o:  # pylint: disable=[comparison-with-itself]
        text = 'NaN'
      elif o == _inf:
        text = 'Infinity'
      elif o == _neginf:
        text = '-Infinity'
      else:
        return _repr(o)

      if not allow_nan:
        raise ValueError(
            'Out of range float values are not JSON compliant: ' + repr(o)
        )

      return text

    if _one_shot and c_make_encoder is not None and self.indent is None:
      _iterencode = c_make_encoder(
          markers,
          self.default,
          _encoder,
          self.indent,
          self.key_separator,
          self.item_separator,
          self.sort_keys,
          self.skipkeys,
          self.allow_nan,
      )
    else:
      _iterencode = _make_iterencode(  # pylint: disable=[protected-access] # pyright: ignore[reportGeneralTypeIssues]
          markers,
          self.default,
          _encoder,
          self.indent,
          floatstr,
          self.key_separator,
          self.item_separator,
          self.sort_keys,
          self.skipkeys,
          _one_shot,
      )
    return _iterencode(o, 0)


def _make_iterencode(
    markers,
    _default,
    _encoder,
    _indent,
    _floatstr,
    _key_separator,
    _item_separator,
    _sort_keys,
    _skipkeys,
    _one_shot,
    ## HACK: hand-optimized bytecode; turn globals into locals
    ValueError=ValueError,
    dict=dict,
    float=float,
    id=id,
    int=int,
    isinstance=isinstance,
    list=list,
    str=str,
    tuple=tuple,
    _intstr=int.__repr__,
):
  # pylint: disable=[redefined-builtin, invalid-name]
  if _indent is not None and not isinstance(_indent, str):
    _indent = ' ' * _indent

  def _iterencode_list(lst, _current_indent_level):
    if not lst:
      yield '[ ]'  # line modified
      return
    if markers is not None:
      markerid = id(lst)
      if markerid in markers:
        raise ValueError('Circular reference detected')
      markers[markerid] = lst
    else:
      markerid = None
    buf = '[ '  # line modified
    if _indent is not None:
      _current_indent_level += 1
      newline_indent = '\n' + _indent * _current_indent_level
      separator = _item_separator + newline_indent
      buf += newline_indent
    else:
      newline_indent = None
      separator = _item_separator
    first = True
    for value in lst:
      if first:
        first = False
      else:
        buf = separator
      if isinstance(value, str):
        yield buf + _encoder(value)
      elif value is None:
        yield buf + 'null'
      elif value is True:
        yield buf + 'true'
      elif value is False:
        yield buf + 'false'
      elif isinstance(value, int):
        # Subclasses of int/float may override __repr__, but we still
        # want to encode them as integers/floats in JSON. One example
        # within the standard library is IntEnum.
        yield buf + _intstr(value)
      elif isinstance(value, float):
        # see comment above for int
        yield buf + _floatstr(value)
      else:
        yield buf
        if isinstance(value, (list, tuple)):
          chunks = _iterencode_list(value, _current_indent_level)
        elif isinstance(value, dict):
          chunks = _iterencode_dict(value, _current_indent_level)
        else:
          chunks = _iterencode(value, _current_indent_level)
        yield from chunks
    if newline_indent is not None:
      _current_indent_level -= 1
      yield '\n' + _indent * _current_indent_level
    yield ' ]'  # line modified
    if markers is not None:
      del markers[markerid]

  def _iterencode_dict(dct, _current_indent_level):
    if not dct:
      yield '{}'
      return
    if markers is not None:
      markerid = id(dct)
      if markerid in markers:
        raise ValueError('Circular reference detected')
      markers[markerid] = dct
    else:
      markerid = None
    yield '{ '  # line modified
    if _indent is not None:
      _current_indent_level += 1
      newline_indent = '\n' + _indent * _current_indent_level
      item_separator = _item_separator + newline_indent
      yield newline_indent
    else:
      newline_indent = None
      item_separator = _item_separator
    first = True
    if _sort_keys:
      items = sorted(dct.items())
    else:
      items = dct.items()
    for key, value in items:
      if isinstance(key, str):
        pass
      # JavaScript is weakly typed for these, so it makes sense to
      # also allow them.  Many encoders seem to do something like this.
      elif isinstance(key, float):
        # see comment for int/float in _make_iterencode
        key = _floatstr(key)
      elif key is True:
        key = 'true'
      elif key is False:
        key = 'false'
      elif key is None:
        key = 'null'
      elif isinstance(key, int):
        # see comment for int/float in _make_iterencode
        key = _intstr(key)
      elif _skipkeys:
        continue
      else:
        raise TypeError(
            f'keys must be str, int, float, bool or None, '
            f'not {key.__class__.__name__}'
        )
      if first:
        first = False
      else:
        yield item_separator
      yield _encoder(key)
      yield _key_separator
      if isinstance(value, str):
        yield _encoder(value)
      elif value is None:
        yield 'null'
      elif value is True:
        yield 'true'
      elif value is False:
        yield 'false'
      elif isinstance(value, int):
        # see comment for int/float in _make_iterencode
        yield _intstr(value)
      elif isinstance(value, float):
        # see comment for int/float in _make_iterencode
        yield _floatstr(value)
      else:
        if isinstance(value, (list, tuple)):
          chunks = _iterencode_list(value, _current_indent_level)
        elif isinstance(value, dict):
          chunks = _iterencode_dict(value, _current_indent_level)
        else:
          chunks = _iterencode(value, _current_indent_level)
        yield from chunks
    if newline_indent is not None:
      _current_indent_level -= 1
      yield '\n' + _indent * _current_indent_level
    yield ' }'  # line modified
    if markers is not None:
      del markers[markerid]  # pyright: ignore[reportUnboundVariable

  def _iterencode(o, _current_indent_level):
    if isinstance(o, str):
      yield _encoder(o)
    elif o is None:
      yield 'null'
    elif o is True:
      yield 'true'
    elif o is False:
      yield 'false'
    elif isinstance(o, int):
      # see comment for int/float in _make_iterencode
      yield _intstr(o)
    elif isinstance(o, float):
      # see comment for int/float in _make_iterencode
      yield _floatstr(o)
    elif isinstance(o, (list, tuple)):
      yield from _iterencode_list(o, _current_indent_level)
    elif isinstance(o, dict):
      yield from _iterencode_dict(o, _current_indent_level)
    else:
      if markers is not None:
        markerid = id(o)
        if markerid in markers:
          raise ValueError('Circular reference detected')
        markers[markerid] = o
      else:
        markerid = None
      o = _default(o)
      yield from _iterencode(o, _current_indent_level)
      if markers is not None:
        del markers[markerid]  # pyright: ignore[reportUnboundVariable

  return _iterencode


"""!!!!!!!!!END SOURCE CODE FROM PYTHON!!!!!!!!!!!"""


class ZeroSievertJsonEncoder(MonkeyPatchedJsonEncoder):

  def default(self, o: Any) -> Any:
    if isinstance(o, decimal.Decimal):
      return _JsonDecimal(o)
    elif isinstance(o, type):
      return str(o)
    super().default(o)


_VT_co = TypeVar('_VT_co', covariant=True)
ClassConstructor = Callable[[Any], Any]


def get_class(qualifier_path: str) -> ClassConstructor:
  """

  Args:
    qualifier_path: A str consisting of the way the class would be referenced in
      global name space (i.e. decimal.Decimal or int). Attempts to import
      missing modules.

  Returns:

  Raises:
    ModuleNotFoundError: If the module searched for does not exist.
    AttributionError: If the expected class does not exist in the module. This
    can be caused by the class name not being capitalized.
  """
  parts = qualifier_path.split('.')
  class_name = parts[-1]
  if len(parts) == 1:
    if class_name in globals():
      return globals()[class_name]
    elif class_name == 'NoneType':
      module_path = 'types'
    else:
      module_path = 'builtins'
  else:
    module_path = ''.join(parts[:-1])
  module = importlib.import_module(module_path)
  return getattr(module, class_name)


def parse_type_hints(
    dictionary: Mapping[str, _VT_co],
) -> ClassConstructor | Mapping[str, _VT_co]:
  if type_string := dictionary.get('__type__'):
    if isinstance(type_string, str):
      pattern = re.escape("'") + '(.*?)' + re.escape("'")
      expected_class = re.search(pattern, type_string)
      if not expected_class:
        raise ValueError(f'Type value expected but no type found: {dictionary}')
      else:
        return get_class(expected_class.group(1))
    else:
      raise ValueError(
          f'Invalid type specified (type: {type_string}): ' f'{dictionary}'
      )
  return dictionary
