#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wav2aac.py
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

"""
need to pre-install: mp4v2, shntool, ffmpeg
"""


import os
from subprocess import call

from pydub import AudioSegment

from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4


class Wav2Aac(object):
    """docstring for Wav2Aac"""

    def __init__(self, folderpath):

        super(Wav2Aac, self).__init__()

        self.folderpath = folderpath
        self.outputdir = self.folderpath + os.sep + "output"
        if os.path.exists(self.outputdir):
            pass
        else:
            os.makedirs(self.outputdir)

    def cutWav(self, cuename, audioname, filetype="wav"):

        cn = self.folderpath + os.sep + cuename
        an = self.folderpath + os.sep + audioname
        thecommand = [
            "shntool",
            "split",
            "-t",
            "%n %t",
            "-f",
            cn,
            "-o",
            filetype,
            an,
            "-d",
            self.outputdir,
        ]
        call(thecommand)

    def wavTOm4a(self):

        wavlist = []
        for root, dirs, files in os.walk(self.outputdir):
            for f in files:
                if f.endswith(".wav"):
                    wavlist.append(root + os.sep + f)

        for w in wavlist:
            try:
                thecommand = [
                    "ffmpeg",
                    "-i",
                    w,
                    "-strict",
                    "experimental",
                    "-c:a",
                    "aac",
                    "-b:a",
                    "320k",
                    w.replace(".wav", ".m4a"),
                ]
                call(thecommand)
            except Exception as e:
                print(e)
            finally:
                os.remove(w)

    def wavTOmp3(self):

        wavlist = []
        for root, dirs, files in os.walk(self.outputdir):
            for f in files:
                if f.endswith(".wav"):
                    wavlist.append(root + os.sep + f)

        for w in wavlist:
            try:
                thecommand = ["ffmpeg", "-i", w, "-ab", "320k", w.replace(".wav", ".mp3")]
                call(thecommand)
            except Exception as e:
                print(e)
            finally:
                os.remove(w)

    def editM4A(self, genre="Genre", album="Album", artist="Artist", date="2016"):

        m4alist = []
        for root, dirs, files in os.walk(self.outputdir):
            for f in files:
                if f.endswith(".m4a"):
                    m4alist.append(root + os.sep + f)

        for m in m4alist:
            audio = EasyMP4(m)
            audio["genre"] = genre
            audio["album"] = album
            audio["artist"] = artist
            audio["albumartist"] = artist
            audio["artistsort"] = artist
            audio["date"] = date
            audio.save()

    def editMP3(self, genre="Genre", album="Album", artist="Artist", date="2016"):

        mp3list = []
        for root, dirs, files in os.walk(self.outputdir):
            for f in files:
                if f.endswith(".mp3"):
                    mp3list.append(root + os.sep + f)

        for m in mp3list:
            audio = EasyID3(m)
            audio["genre"] = genre
            audio["album"] = album
            audio["artist"] = artist
            # audio['date'] = date
            audio.save()

    def changeCover(self, picname):

        m4alist = []
        for root, dirs, files in os.walk(self.outputdir):
            for f in files:
                if f.endswith(".m4a"):
                    m4alist.append(root + os.sep + f)

        cover = self.outputdir + os.sep + picname
        for m4 in m4alist:
            thecommand = ["mp4art", "--add", cover, m4]
            call(thecommand)

        mp3list = []
        for root, dirs, files in os.walk(self.outputdir):
            for f in files:
                if f.endswith(".mp3"):
                    m4alist.append(root + os.sep + f)

        cover = self.outputdir + os.sep + picname
        for m3 in mp3list:
            thecommand = [
                "ffmpeg -i",
                m3,
                "-i",
                cover,
                "-map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v",
                'title="Album cover" -metadata:s:v comment="Cover (Front)"',
                m3,
            ]
            call(thecommand)


def main(args):

    myfolder = "/home/ulric/workspace/codes/py/wav2aac/Cher - [[ The Very Best Of Cher ]]"
    wa = Wav2Aac(myfolder)
    # wa.cutWav('Cher - The Very Best Of Cher.cue', 'Cher - The Very Best Of Cher.wav')
    # wa.wavTOm4a()
    # wa.wavTOmp3()
    # wa.editM4A(genre='pop', album='The Very Best Of Cher', artist='Cher', date=2003)
    # wa.editMP3(genre='pop', album='The Very Best Of Cher', artist='Cher', date=2003)
    wa.changeCover("cover.jpg")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
