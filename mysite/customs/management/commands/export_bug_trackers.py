# This file is part of OpenHatch.
# Copyright (C) 2012 OpenHatch, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import yaml
from django.core.management.base import BaseCommand
import mysite.customs.models

CLASS_NAME2SIMPLE_NAME = {
    mysite.customs.models.GitHubTrackerModel: 'github',
    mysite.customs.models.GoogleTrackerModel: 'google',
    mysite.customs.models.RoundupTrackerModel: 'roundup',
    mysite.customs.models.TracTrackerModel: 'trac',
    }
class Command(BaseCommand):
    help = "Print a YAML file with configuration all Trac-based trackers"

    def handle(self, *args, **options):
        as_dicts = []
        for tracker in mysite.customs.models.TracTrackerModel.objects.select_subclasses():
            # Annotate it with a oh-bugimporter-compatible name
            # If no such annotation is possible, then skip the export.
            if tracker.__class__ not in CLASS_NAME2SIMPLE_NAME:
                continue
            as_dict = tracker.as_dict()
            as_dict['bugimporter'] = CLASS_NAME2SIMPLE_NAME[tracker.__class__]
            as_dicts.append(as_dict)

        print yaml.safe_dump(as_dicts)