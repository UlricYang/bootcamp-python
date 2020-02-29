#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#  camRename.py
#
#  Copyright 2017 Ulric Yang <ryang_nudt@163.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os

import arrow
import exifread


class CamRename(object):
    """
    """

    def __init__(self, camdir):
        """
        """
        self.camdir = camdir

    def getPhotos(self):
        """
        """
        photos = []
        for root, dirs, files in os.walk(self.camdir):
            for f in files:
                if f.endswith(".jpg"):
                    photos.append(root + os.sep + f)

        return photos

    def photoRename(self, photopath):
        """
        """
        with open(photopath, "rb") as f:
            tags = exifread.process_file(f)

        try:
            ptime = tags["EXIF DateTimeOriginal"]
            t = arrow.get(str(ptime), "YYYY:MM:DD HH:mm:ss").format("YYYYMMDDHHmmss")
            nname = "CAMERA-" + t + ".jpg"
            newname = os.path.dirname(photopath) + os.sep + nname
            os.rename(photopath, newname)
        except Exception as identifier:
            print("{i}-->{e}".format(i=identifier, e=photopath))

    def batch(self):
        """
        """
        oldnames = self.getPhotos()
        for oldname in oldnames:
            self.photoRename(oldname)


def main(args):

    pdir = "/home/ulric/Pictures/pic/newones"
    cr = CamRename(pdir)
    cr.batch()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
