SearchBox for Epiphany 
======================

A toolbar search box similar to the one in Firefox.

Created By
----------

Eric Butler <eric@extremeboredom.net>  
[http://eric.extremeboredom.net](http://eric.extremeboredom.net)

License
-------

GPLv3 or later, see COPYING.

Requirements
------------

Epiphany-SearchBox has been tested on Ubuntu Edgy, it is known to not work on
Ubuntu Dapper.

To install
----------

* You need to have the epiphany-extensions package installed first, or else you
  will not have a *Tools* menu.

		$ sudo apt-get install epiphany-extensions

* Copy files into *~/.gnome2/epiphany/extensions/*:

		$ cp searchbox.ephy-extension ~/.gnome2/epiphany/extensions/
		$ cp -r searchbox ~/.gnome2/epiphany/extensions/

* Activate from *Tools -> Extensions* after restarting epiphany

* Right-click on an empty part of the toolbar and select *Customize Toolbars*, 
  then drag the *Search Box* icon to the toolbar wherever you would like.
