#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  editMP3.py
#
#  Copyright 2016 ulric <ulric@ulric-pc>
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

from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
from mutagen.mp4 import MP4, MP4Cover


class EditTags:
    """

	"""

    def __init__(self, filefolder):
        """

		"""
        self.filefolder = filefolder
        self.tracks = []

    def editMP3(self, genre="Genre", album="Album", artist="Artist", date="2016"):
        """

		"""
        for root, dirs, files in os.walk(self.filefolder):
            for f in files:
                if f.endswith(".mp3"):
                    fullpath = root + os.sep + f
                    self.tracks.append(fullpath)
        for track in self.tracks:
            print(track)
            audio = EasyID3(track)
            print(audio)
            audio["genre"] = "Englist"
            audio["album"] = "TOEFL-iBT"
            audio["artist"] = "Dr.ZHY"
            audio.save()
            print(audio)
            print()

    def editMP4(self, genre="Genre", album="Album", artist="Artist", date="2016"):
        """

		"""
        for root, dirs, files in os.walk(self.filefolder):
            for f in files:
                if f.endswith(".m4a"):
                    fullpath = root + os.sep + f
                    self.tracks.append(fullpath)
        for track in self.tracks:
            print(track)
            audio = EasyMP4(track)
            print(audio)
            audio["genre"] = genre
            audio["album"] = album
            audio["artist"] = artist
            audio["albumartist"] = artist
            audio["artistsort"] = artist
            audio.save()
            print(audio)
            print()


class EditTitle:
    """
	
	"""

    def __init__(self, filefolder):
        """
		
		"""
        self.filefolder = filefolder
        self.tracks = []

    def reNum(self):
        """

		"""
        for root, dirs, files in os.walk(self.filefolder):
            for f in files:
                if f.endswith(".m4a"):
                    fullpath = root + os.sep + f
                    self.tracks.append(fullpath)
        for track in self.tracks:
            print(track)
            audio = EasyMP4(track)
            tname = audio["title"]
            tnum = audio["tracknumber"][0].split("/")[0]
            if len(tnum) < 2:
                tnum = "0" + tnum
            newname = tnum + " " + tname[0] + ".m4a"
            newname = self.filefolder + os.sep + newname
            print(newname)
            os.rename(track, newname)
            print()


def songEditTags():
    """

	"""
    folderpath = "/home/ulric/workspace/script/py/editSongTags/Robyn - [[ Body Talk ]]/Pt1"
    theGenre = "Pop"
    theAlbum = "Body Talk (Pt1)"
    theArtist = "Robyn"
    theDate = "2008"
    EditTags(folderpath).editMP4(genre=theGenre, album=theAlbum, artist=theArtist, date=theDate)


def songEditTitle():
    """

	"""
    folderpath = "/home/ulric/yr/workspace/py/AACNamer/music/album/Sara Bareilles - [[ What's Inside_ Songs from Waitress ]]"
    EditTitle(folderpath).reNum()


def main(args):
    songEditTags()
    # songEditTitle()
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
