#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vidRename.py
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


class VidRename(object):
    """
	"""

    def __init__(self, viddir):
        """
		"""
        self.viddir = viddir

    def getVideos(self):
        """
		"""
        videos = []
        for root, dirs, files in os.walk(self.viddir):
            for f in files:
                if f.endswith(".mp4"):
                    videos.append(root + os.sep + f)
                    # print(photos)
        return videos

    def videoRename(self, videopath):
        """
		"""
        oldname = os.path.basename(videopath)
        dirpath = os.path.dirname(videopath)
        vv = oldname.split("_")
        vv[0] = "VIDEO-"
        newname = dirpath + os.sep + "".join(vv)
        os.rename(videopath, newname)

    def batch(self):
        """
		"""
        oldnames = self.getVideos()
        for oldname in oldnames:
            self.videoRename(oldname)


def main(args):

    vdir = "/home/ulric/Videos"
    vr = VidRename(vdir)
    vr.batch()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
