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
#
# generated by datamodel-codegen:
#   filename:  key_structure_0.31_production_clean_types.json
#   timestamp: 2023-08-15T21:41:59+00:00
"""This file reflects the values lexed from a deserialized "ZERO Sievert" save
in JSON format. It is not equivalent to expected fields nor types in zero_saver
objects.
"""
# pylint: disable=[invalid-name, missing-class-docstring]
from __future__ import annotations

import decimal
from typing import Any, Dict, List

from typing_extensions import NotRequired, TypedDict

ZeroSievertJsonValue = str | decimal.Decimal | None
ZeroSievertLexedItem = dict[str, ZeroSievertJsonValue]
ZeroSievertParsedValue = ZeroSievertJsonValue | bool | dict[str, str] | int
ZeroSievertParsedItem = dict[str, ZeroSievertParsedValue]

Base = TypedDict(
    'Base',
    {
        '0': decimal.Decimal,
        '11': decimal.Decimal,
        '4': decimal.Decimal,
        '12': decimal.Decimal,
        '3': decimal.Decimal,
        '1': decimal.Decimal,
        '13': decimal.Decimal,
        '7': decimal.Decimal,
        '5': decimal.Decimal,
        '9': decimal.Decimal,
        '2': decimal.Decimal,
        '10': decimal.Decimal,
        '6': decimal.Decimal,
        '8': decimal.Decimal,
    },
)


class Exp(TypedDict):
  Livello: decimal.Decimal
  Amount: decimal.Decimal


class Item(TypedDict):
  item: str
  x: decimal.Decimal
  quantity: decimal.Decimal
  y: decimal.Decimal
  min_level: decimal.Decimal
  rotation: decimal.Decimal
  page: decimal.Decimal
  ammo_id: NotRequired[str]
  ammo_quantity: NotRequired[decimal.Decimal]
  weapon_fire_mode: NotRequired[str]
  mods: NotRequired[None]


class TraderFaction1Trader(TypedDict):
  items: List[Item]
  money: decimal.Decimal


class Field15(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field4(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field12(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field17(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field1(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field16(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field18(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field13(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field27(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field5(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field9(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field26(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field6(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field21(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field14(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field0(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field11(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field24(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field3(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field28(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field19(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field29(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field7(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field23(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field2(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field10(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field22(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field25(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field20(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


class Field8(TypedDict):
  id: str
  amount_now: List[decimal.Decimal]
  state: str
  notifica_sub: List[decimal.Decimal]
  notifica: decimal.Decimal
  giver: str


Quest = TypedDict(
    'Quest',
    {
        '15': Field15,
        '4': Field4,
        '12': Field12,
        '17': Field17,
        '1': Field1,
        '16': Field16,
        '18': Field18,
        '13': Field13,
        '27': Field27,
        '5': Field5,
        '9': Field9,
        '26': Field26,
        '6': Field6,
        '21': Field21,
        'daily generated': decimal.Decimal,
        '14': Field14,
        '0': Field0,
        '11': Field11,
        '24': Field24,
        '3': Field3,
        '28': Field28,
        '19': Field19,
        '29': Field29,
        '7': Field7,
        '23': Field23,
        '2': Field2,
        '10': Field10,
        '22': Field22,
        '25': Field25,
        '20': Field20,
        '8': Field8,
    },
)


class Item1(TypedDict):
  item: str
  x: decimal.Decimal
  quantity: decimal.Decimal
  y: decimal.Decimal
  min_level: decimal.Decimal
  rotation: decimal.Decimal
  page: decimal.Decimal


class MedicTrader(TypedDict):
  items: List[Item1]
  money: decimal.Decimal


class QuestNextItem(TypedDict):
  id: str
  npc_id: str


class RewardItem(TypedDict):
  item: str
  amount: decimal.Decimal


class ObjectiveItem(TypedDict):
  object: NotRequired[decimal.Decimal]
  map: NotRequired[decimal.Decimal]
  amount_max: decimal.Decimal
  text: str
  object_name: NotRequired[str]
  already_created: NotRequired[decimal.Decimal]
  marker_radius: decimal.Decimal
  type: str
  faction: NotRequired[str]
  array_kill: NotRequired[List[str]]
  exp_amount: NotRequired[decimal.Decimal]
  item: NotRequired[str]
  marker_object: NotRequired[decimal.Decimal]
  money_amount: NotRequired[decimal.Decimal]
  distance: NotRequired[decimal.Decimal]
  text_if_no_item: NotRequired[decimal.Decimal]
  item_id: NotRequired[str]
  text_prompt: NotRequired[str]
  text_if_item: NotRequired[decimal.Decimal]
  anomaly_generator_id: NotRequired[decimal.Decimal]
  chest_obj: NotRequired[decimal.Decimal]


class InitialItemItem(TypedDict):
  item: str
  amount: decimal.Decimal


class GeneratedItem(TypedDict):
  id: str
  quest_next: List[QuestNextItem]
  text: str
  faction: str
  name: str
  reputation: decimal.Decimal
  daily: decimal.Decimal
  rep_min: decimal.Decimal
  removable: decimal.Decimal
  reward: List[RewardItem]
  experience: decimal.Decimal
  objective: List[ObjectiveItem]
  money: decimal.Decimal
  initial_item: List[InitialItemItem]


class DailyQuests(TypedDict):
  generated: List[GeneratedItem]


class GameTimePlayed(TypedDict):
  seconds: decimal.Decimal


BaseSlot = TypedDict(
    'BaseSlot',
    {
        '0': decimal.Decimal,
        '5': decimal.Decimal,
        '4': decimal.Decimal,
        '2': decimal.Decimal,
        '3': decimal.Decimal,
        '6': decimal.Decimal,
        '1': decimal.Decimal,
    },
)


class Factions(TypedDict):
  joined: str
  relationships: List[List[decimal.Decimal]]


class Data1(TypedDict):
  bandit: decimal.Decimal
  cabinet: decimal.Decimal
  electronic: decimal.Decimal
  survival_streak_now: decimal.Decimal
  big: decimal.Decimal
  medication: decimal.Decimal
  boss_orel: decimal.Decimal
  attachment_box: decimal.Decimal
  green_army: decimal.Decimal
  most_exp_raid: decimal.Decimal
  wolf: decimal.Decimal
  survival_rate: decimal.Decimal
  rat: decimal.Decimal
  ghoul: decimal.Decimal
  boss_lazar: decimal.Decimal
  hidden_stash: decimal.Decimal
  loner: decimal.Decimal
  tot_money: decimal.Decimal
  blink: decimal.Decimal
  boss_killa: decimal.Decimal
  tot_hunt: decimal.Decimal
  vending_machine: decimal.Decimal
  crimson: decimal.Decimal
  tot_human: decimal.Decimal
  spider: decimal.Decimal
  bag: decimal.Decimal
  tot_chest: decimal.Decimal
  survival_streak_max: decimal.Decimal
  safe: decimal.Decimal
  boss_arman: decimal.Decimal
  weapon_box: decimal.Decimal
  scientist: decimal.Decimal
  most_roubles_raid: decimal.Decimal
  tool_box: decimal.Decimal
  boar: decimal.Decimal
  tot_mutant: decimal.Decimal
  tot_hunt_survived: decimal.Decimal
  rabbit: decimal.Decimal
  crystal: decimal.Decimal
  air_drop: decimal.Decimal
  wood_box: decimal.Decimal


class Statistics(TypedDict):
  data: Data1


BaseSlotOccupato = TypedDict(
    'BaseSlotOccupato',
    {
        '0': decimal.Decimal,
        '5': decimal.Decimal,
        '4': decimal.Decimal,
        '2': decimal.Decimal,
        '3': decimal.Decimal,
        '6': decimal.Decimal,
        '1': decimal.Decimal,
    },
)


class QuestLine(TypedDict):
  completed: Dict[str, Any]


class Item2(TypedDict):
  item: str
  x: decimal.Decimal
  quantity: decimal.Decimal
  y: decimal.Decimal
  min_level: decimal.Decimal
  rotation: decimal.Decimal
  page: decimal.Decimal
  ammo_id: NotRequired[str]
  ammo_quantity: NotRequired[decimal.Decimal]
  weapon_fire_mode: NotRequired[str]
  mods: NotRequired[None]


class BarmanTrader(TypedDict):
  items: List[Item2]
  money: decimal.Decimal


SkillLastLevel = TypedDict(
    'SkillLastLevel',
    {
        '15': decimal.Decimal,
        '4': decimal.Decimal,
        '12': decimal.Decimal,
        '17': decimal.Decimal,
        '1': decimal.Decimal,
        '16': decimal.Decimal,
        '18': decimal.Decimal,
        '13': decimal.Decimal,
        '5': decimal.Decimal,
        '9': decimal.Decimal,
        '6': decimal.Decimal,
        '21': decimal.Decimal,
        '14': decimal.Decimal,
        '0': decimal.Decimal,
        '11': decimal.Decimal,
        '24': decimal.Decimal,
        '3': decimal.Decimal,
        '19': decimal.Decimal,
        '7': decimal.Decimal,
        '23': decimal.Decimal,
        '2': decimal.Decimal,
        '10': decimal.Decimal,
        '22': decimal.Decimal,
        '20': decimal.Decimal,
        '8': decimal.Decimal,
    },
)


class RealTimePlayed(TypedDict):
  seconds: decimal.Decimal


Skill = TypedDict(
    'Skill',
    {
        '15': decimal.Decimal,
        '4': decimal.Decimal,
        '12': decimal.Decimal,
        '17': decimal.Decimal,
        '1': decimal.Decimal,
        '16': decimal.Decimal,
        '18': decimal.Decimal,
        '13': decimal.Decimal,
        '5': decimal.Decimal,
        '9': decimal.Decimal,
        '6': decimal.Decimal,
        '21': decimal.Decimal,
        '14': decimal.Decimal,
        '0': decimal.Decimal,
        '11': decimal.Decimal,
        '24': decimal.Decimal,
        '3': decimal.Decimal,
        '19': decimal.Decimal,
        '7': decimal.Decimal,
        '23': decimal.Decimal,
        '2': decimal.Decimal,
        '10': decimal.Decimal,
        '22': decimal.Decimal,
        '20': decimal.Decimal,
        '8': decimal.Decimal,
    },
)

General = TypedDict(
    'General',
    {
        'Base': Base,
        'Exp': Exp,
        'trader_faction1_trader': TraderFaction1Trader,
        'quest': Quest,
        'medic_trader': MedicTrader,
        'daily quests': DailyQuests,
        'Game time played': GameTimePlayed,
        'Base slot': BaseSlot,
        'factions': Factions,
        'Statistics': Statistics,
        'Base slot occupato': BaseSlotOccupato,
        'quest line': QuestLine,
        'barman_trader': BarmanTrader,
        'skill last level': SkillLastLevel,
        'Real time played': RealTimePlayed,
        'skill': Skill,
    },
)


class Chest(TypedDict):
  chest_0: NotRequired[List[ZeroSievertLexedItem]]
  chest_1: NotRequired[List[ZeroSievertLexedItem]]
  chest_2: NotRequired[List[ZeroSievertLexedItem]]
  chest_3: NotRequired[List[ZeroSievertLexedItem]]
  chest_4: NotRequired[List[ZeroSievertLexedItem]]
  chest_5: NotRequired[List[ZeroSievertLexedItem]]
  chest_6: NotRequired[List[ZeroSievertLexedItem]]
  chest_7: NotRequired[List[ZeroSievertLexedItem]]
  chest_8: NotRequired[List[ZeroSievertLexedItem]]
  chest_9: NotRequired[List[ZeroSievertLexedItem]]
  chest_10: NotRequired[List[ZeroSievertLexedItem]]
  chest_11: NotRequired[List[ZeroSievertLexedItem]]
  chest_12: NotRequired[List[ZeroSievertLexedItem]]
  chest_13: NotRequired[List[ZeroSievertLexedItem]]


class NPC(TypedDict):
  leader_faction1_quest: List[str]
  daily_quest_giver_quest: List[str]
  barman_quest: List[str]


class Stats(TypedDict):
  money: decimal.Decimal


class Loadout(TypedDict):
  id: str


class Player(TypedDict):
  energy: decimal.Decimal
  radiation: decimal.Decimal
  x: decimal.Decimal
  y: decimal.Decimal
  fatigue: decimal.Decimal
  hp_max: decimal.Decimal
  stamina_max: decimal.Decimal
  wound: decimal.Decimal
  hp: decimal.Decimal
  thirst: decimal.Decimal


class Inventory(TypedDict):
  items: List[ZeroSievertLexedItem] | List[ZeroSievertParsedItem]


class PreRaid(TypedDict):
  NPC: NPC
  stats: Stats
  loadout: Loadout
  player: Player
  Inventory: Inventory


class Difficulty(TypedDict):
  pro_player_health: decimal.Decimal
  pro_min_carry_weight: decimal.Decimal
  loot_npc_drop_armor: decimal.Decimal
  trade_trader_money: decimal.Decimal
  trade_price_medication: decimal.Decimal
  hardcore_lose_other: decimal.Decimal
  pro_quest_money: decimal.Decimal
  trade_item_amount: decimal.Decimal
  loot_item_amount: decimal.Decimal
  pro_quest_rep: decimal.Decimal
  pro_service_price: decimal.Decimal
  trade_price_weapon: decimal.Decimal
  pro_hunger_thirst_rate: decimal.Decimal
  trade_price_ammo: decimal.Decimal
  loot_weapon_dur_max: decimal.Decimal
  hardcore_lose_medication: decimal.Decimal
  loot_weapon_dur_min: decimal.Decimal
  hardcore_lose_keys: decimal.Decimal
  hardcore_lose_ammo: decimal.Decimal
  loot_amount_single_item: decimal.Decimal
  trade_price_armor: decimal.Decimal
  pro_exp_multiplier: decimal.Decimal
  loot_npc_drop_ammo: decimal.Decimal
  trade_sell_mult: decimal.Decimal
  enemy_human_hp: decimal.Decimal
  pro_quest_item: decimal.Decimal
  hardcore_lose_consumable: decimal.Decimal
  enemy_mutant_hp: decimal.Decimal
  trade_price_backpack: decimal.Decimal
  enemy_human_damage: decimal.Decimal
  pro_reputation_multiplier: decimal.Decimal
  hardcore_perma_death: decimal.Decimal
  hardcore_lose_equipment: decimal.Decimal
  enemy_mutant_damage: decimal.Decimal


class Data(TypedDict):
  general: General
  chest: Chest
  pre_raid: PreRaid
  difficulty: Difficulty


class Model(TypedDict):
  save_version: str
  data: Data
  format: str
  timestamp: str
