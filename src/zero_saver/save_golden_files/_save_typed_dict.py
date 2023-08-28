#  Copyright 2023 The Zero Saver Authors. All Rights Reserved.
#
#  This file is part of Zero Saver.
#
#  Zero Saver is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Zero Saver is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Zero Saver. If not, see <https://www.gnu.org/licenses/>.
"""Type hints used across zero_saver when referencing save file data.

Types defined here are independent of save version and are robust for usage
within zero_saver.

These types should not be used externally. Instead, import the type directly
from the public API being used."""
from __future__ import annotations

import decimal

ZeroSievertAttachments = dict[str, str]
ZeroSievertJsonValue = str | decimal.Decimal | None | ZeroSievertAttachments
ZeroSievertLexedItem = dict[str, ZeroSievertJsonValue]
ZeroSievertParsedValue = ZeroSievertJsonValue | bool | dict[str, str] | int
ZeroSievertParsedItem = dict[str, ZeroSievertParsedValue]
