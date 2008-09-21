#
#   SearchBox - Epiphany Extension
#   Copyright (C) 2006  Eric Butler <eric@extremeboredom.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import os.path

def data_dir():
	# XXX: Replace all this with a call to epiphany.ephy_dot_dir(),
	# (not currently exposed - might need to re-implement in python!)

	home_dir = os.environ['HOME']
	dir = os.path.join(home_dir, '.gnome2', 'epiphany')
	dir = os.path.join(dir, "extensions", "data", "searchbox")
	return dir

def epiphany_dir():
	# XXX: Replace all this with a call to epiphany.ephy_dot_dir(),
	# (not currently exposed - might need to re-implement in python!)

	home_dir = os.environ['HOME']
	dir = os.path.join(home_dir, '.gnome2', 'epiphany')
	return dir
