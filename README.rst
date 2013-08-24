======================================
Redmine/Chiliproject ticket statistics
======================================

Visualize ticket statistics of redmine_ or chiliproject_ in munin_. This plugin provides 4 different graphs:

- Tracker

  - Tickets by tracker
  - Open Tickets by tracker

- User

  - Tickets by user
  - Open Tickets by user


Example
=======

.. image::  https://raw.github.com/saily/redmine_stats/master/example.png


Configuration
=============

First checkout and symlink your plugins into munin plugins directory using::

    $ git clone https://github.com/saily/redmine_stats.git /opt/redmine_stats
    $ ln -s /opt/redmine_stats /etc/munin/plugins/redmine_stats_tracker
    $ ln -s /opt/redmine_stats /etc/munin/plugins/redmine_stats_tracker_open
    $ ln -s /opt/redmine_stats /etc/munin/plugins/redmine_stats_user
    $ ln -s /opt/redmine_stats /etc/munin/plugins/redmine_stats_user_open

Open ``/etc/munin/plugin-conf.d/munin-node`` and add following lines::

    [redmine_*]
    env.host = <mysql_hostname>
    env.username = <mysql_username>
    env.password = <mysql_password>
    env.port = <mysql_port>

If you omit environment variable for hostname ``127.0.0.1`` is used by default,
if you omit environment variable for port ``3306`` is used by default.

Don't forget to restart ``munin-node`` after adding the new plugin.


Todo
====

- Implement limitation when having many users and/or trackers.
- Add more graphs


Changes
=======

1.0 - 2012.11.10
----------------

- First implementation
  [saily]


Author
======

`Daniel Widerin`_ [saily]


.. _chiliproject: http://www.chiliproject.org
.. _redmine: http://www.redmine.org
.. _munin: http://munin-monitoring.org/
.. _`Daniel Widerin`: http://www.widerin.org
