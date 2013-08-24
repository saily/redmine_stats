#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Daniel Widerin  <daniel@widerin.net>
#
# v1.0 20/11/2012 - First basic implementation

import os
import sys
import MySQLdb


class RedmineBase(object):

    graph_category = "redmine"
    graph_args = "--base 1000 --lower-limit 0"
    graph_vlabel = "tickets"

    def __init__(self, database, username, password, hostname, port=3306):
        self.db = MySQLdb.connect(host=hostname,
                                  user=username,
                                  passwd=password,
                                  port=port,
                                  db=database,
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def config(self):
        for attr in dir(self):
            if attr.startswith('graph_'):
                print "%s %s" % (attr, getattr(self, attr))


class TicketsByTracker(RedmineBase):

    graph_title = "tickets by tracker"

    def _result(self, callback):
        self.cursor.execute("""\
            SELECT count(issues.id) as Amount, trackers.name, trackers.id
            FROM issues
            INNER JOIN trackers ON issues.tracker_id=trackers.id
            GROUP BY issues.tracker_id
            ORDER BY trackers.id ASC""")

        result = self.cursor.fetchall()
        for item in result:
            callback(item)

    def config(self):
        super(TicketsByTracker, self).config()

        def row(item):
            print "_v%s.label %s" % (item[2], item[1])
            print "_v%s.draw AREASTACK" % (item[2])

        self._result(row)

    def run(self):

        def row(item):
            print "_v%s.value %d" % (item[2], item[0])

        self._result(row)


class OpenTicketsByTracker(TicketsByTracker):

    graph_title = "open tickets by tracker"

    def _result(self, callback):
        self.cursor.execute("""\
            SELECT count(issues.id) as Amount, trackers.name, trackers.id
            FROM issues
            INNER JOIN trackers ON issues.tracker_id=trackers.id
            INNER JOIN issue_statuses ON issues.status_id=issue_statuses.id
            WHERE issue_statuses.is_closed=0
            GROUP BY issues.tracker_id
            ORDER BY trackers.id ASC""")

        result = self.cursor.fetchall()
        for item in result:
            callback(item)


class TicketsByOwner(RedmineBase):

    graph_title = "tickets by user"

    def _result(self, callback):
        self.cursor.execute("""\
            SELECT count(issues.id) as Amount, users.firstname, users.lastname,
                users.id
            FROM issues
            INNER JOIN users ON users.id=issues.assigned_to_id
            GROUP BY issues.assigned_to_id
            ORDER BY users.id ASC""")

        result = self.cursor.fetchall()
        for item in result:
            callback(item)

    def config(self):
        super(TicketsByOwner, self).config()

        def row(item):
            print "_v%s.label %s %s" % (item[3],
                                        unicode(item[1]).encode("utf-8"),
                                        unicode(item[2]).encode("utf-8"))
            print "_v%s.draw AREASTACK" % (item[3])

        self._result(row)

    def run(self):

        def row(item):
            print "_v%s.value %d" % (item[3], item[0])

        self._result(row)


class OpenTicketByOwner(TicketsByOwner):

    graph_title = "open tickets by user"

    def _result(self, callback):
        self.cursor.execute("""\
            SELECT count(issues.id) as Amount, users.firstname, users.lastname,
                users.id
            FROM issues
            INNER JOIN users ON users.id=issues.assigned_to_id
            INNER JOIN issue_statuses ON issues.status_id=issue_statuses.id
            WHERE issue_statuses.is_closed=0
            GROUP BY issues.assigned_to_id
            ORDER BY users.id ASC""")

        result = self.cursor.fetchall()
        for item in result:
            callback(item)

if __name__ == '__main__':

    host = os.environ.get("host", "127.0.0.1")
    username = os.environ.get("username")
    password = os.environ.get("password")
    database = os.environ.get("database")
    port = os.environ.get("port", 3306)

    if '_tracker' in sys.argv[0]:
        if '_open' in sys.argv[0]:
            r = OpenTicketsByTracker(database, username, password, host, port)
        else:
            r = TicketsByTracker(database, username, password, host, port)

    else:
        if '_open' in sys.argv[0]:
            r = OpenTicketByOwner(database, username, password, host, port)
        else:
            r = TicketsByOwner(database, username, password, host, port)

    if len(sys.argv) > 1 and sys.argv[1] == 'config':
        r.config()
    else:
        r.run()
