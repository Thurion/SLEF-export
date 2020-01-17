"""
SLEF-export a plugin for EDMC
Copyright (C) 2020 Sebastian Bauer

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import sys
import json
from collections import OrderedDict

try:
    # Python 2
    import Tkinter as tk
    import ttk
except ModuleNotFoundError:
    # Python 3
    import tkinter as tk
    import tkinter.ttk as ttk


this = sys.modules[__name__]  # For holding module globals
this.state = None
this.button = None
this.frame = None  # type: tk.Frame


this.VERSION = "1.0"
this.NAME = "SLEF Export"


def plugin_start(plugin_dir):
    return this.NAME


def plugin_start3(plugin_dir):
    plugin_start(plugin_dir)


def plugin_stop():
    # nothing to do here.
    pass


def plugin_prefs(parent, cmdr, is_beta):
    # no prefs
    return None


def button_callback():
    # code copied from monitor class
    # https://github.com/Marginal/EDMarketConnector/blob/master/monitor.py
    standard_order = ["ShipCockpit", "CargoHatch", "Armour", "PowerPlant", "MainEngines", "FrameShiftDrive", "LifeSupport", "PowerDistributor", "Radar", "FuelTank"]

    d = OrderedDict()
    d["Ship"] = this.state["ShipType"]
    d["ShipID"] = this.state["ShipID"]
    if this.state["ShipName"]:
        d["ShipName"] = this.state["ShipName"]
    if this.state["ShipIdent"]:
        d["ShipIdent"] = this.state["ShipIdent"]
    # sort modules by slot - hardpoints, standard, internal
    d["Modules"] = []
    for slot in sorted(this.state["Modules"], key=lambda x: ("Hardpoint" not in x, x not in standard_order and len(standard_order) or standard_order.index(x), "Slot" not in x, x)):
        module = dict(this.state["Modules"][slot])
        module.pop("Health", None)
        module.pop("Value", None)
        d["Modules"].append(module)

    slef = {"header": {"appName": this.NAME,
                       "appVersion": this.VERSION,
                       "appURL": "https://github.com"},
            "data": d}

    this.frame.clipboard_clear()
    this.frame.clipboard_append(json.dumps(slef, indent=2))


def plugin_app(parent):
    this.frame = tk.Frame(parent)
    this.button = tk.Button(this.frame, text="Copy SLEF to clipboard", command=button_callback)
    this.button.config(state=tk.DISABLED)
    this.button.pack(side=tk.LEFT)
    return this.frame


def journal_entry(cmdr, is_beta, system, station, entry, state):
    if state["Modules"]:
        this.state = state
        this.button.config(state=tk.NORMAL)
