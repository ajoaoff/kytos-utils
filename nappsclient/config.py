# This file is part of kytos-utils.
#
# Copyright (c) 2016 Kytos Team
#
# Authors:
#    Beraldo Leal <beraldo AT ncc DOT unesp DOT br>
#
# kytos-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kytos-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

from configparser import ConfigParser, NoOptionError
import os
import sys

class KytosConfig():
    def __init__(self):
        self.config_file = "~/.kytosrc"
        self.debug = False
        self.napps_uri = os.environ.get('NAPPS_API_URI')
        self.user = os.environ.get('NAPPS_USER')
        self.password = os.environ.get('NAPPS_PASSWORD')
        self.token = os.environ.get('NAPPS_TOKEN')

        self.config = ConfigParser()

        self.parse()

    def parse(self):
        try:
            self.config.readfp(open(os.path.expanduser(self.config_file)))
        except IOError as e:
            print("Config file not found.")
            print("Creating new config file.")
            print("For more information please run:")
            print(" $ kytos-napps --help")
            self.create()
            self.save_user(self.user)
            self.save_napps_uri(self.napps_uri)
            self.save_token(self.token)

        self.load_global()
        self.load_auth()

    def load_global(self):
        # Try to read global section
        try:
            self.debug = self.config.getboolean("global", "debug")
        except NoOptionError:
            pass

        try:
            self.napps_uri = self.config.get("global", "napps_uri")
        except NoOptionError:
            pass

    def load_auth(self):
        try:
            self.user = self.config.get("auth", "user")
        except NoOptionError:
            pass

        try:
            self.token = self.config.get("auth", "token")
        except NoOptionError:
            pass

    def save_napps_uri(self, napps_uri):
        self.napps_uri = napps_uri
        if self.napps_uri:
           self.config.set("global", "napps_uri", napps_uri)
           self.save()

    def save_user(self, user):
        self.user = user
        if self.user:
            self.config.set("auth", "user", user)
            self.save()

    def save_token(self, token):
        self.token = token
        if self.token:
            self.config.set("auth", "token", token)
            self.save()

    def create(self):
        """ Creates a empty config file."""
        self.config.add_section("global")
        self.config.add_section("auth")

    def save(self):
        filename = os.path.expanduser(self.config_file)
        with open(filename, 'w') as f:
            os.chmod(filename, 0o0600)
            self.config.write(f)
