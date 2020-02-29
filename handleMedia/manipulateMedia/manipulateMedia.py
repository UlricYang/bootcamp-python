#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  manipulateMedia.py
#
#  Copyright 2016 Unknown <ulric@ulric-pc>
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
from collections import deque
from pprint import pprint
from subprocess import call

import pydub
from pydub import AudioSegment

import pysrt


class SubtitleProcess(object):
    """

	"""

    def __init__(self, subtitlefile):
        """

		"""

        super(SubtitleProcess, self).__init__()
        self.subtitlefile = subtitlefile

    def getPieces(self):
        """

		"""

        subs = pysrt.open(self.subtitlefile, encoding="utf-8")
        subsinfo1 = []
        subsinfo2 = []

        for i in range(len(subs)):
            sub = subs[i]
            if "\n" in sub.text:
                x = sub.index
                s = sub.start
                e = sub.end
                t = sub.text.split("\n")
                ss = ".".join([str(s.minutes), str(s.seconds), str(int(s.milliseconds) % 100)])
                ee = ".".join([str(e.minutes), str(e.seconds), str(int(e.milliseconds) % 100)])
                subsinfo1.append((x, ss, ee, t))
                sss = s.milliseconds + s.seconds * 1000 + s.minutes * 1000 * 60
                eee = e.milliseconds + e.seconds * 1000 + e.minutes * 1000 * 60
                subsinfo2.append((x, sss, eee, t))

        subsinfo = sorted(subsinfo1, key=lambda info: len(info[3][1]), reverse=True)
        # return(subsinfo[:howmany])
        return subsinfo1


class VideoProcess(object):
    """

	"""

    def __init__(self, videofile):
        """

		"""

        super(VideoProcess, self).__init__()
        self.videofile = videofile

    def extractAudio(self, theformat=".m4a"):
        """

		"""

        outfile = os.path.splitext(self.videofile)[0] + theformat
        theCommand = ["ffmpeg", "-i", self.videofile, "-vn", "-acodec", "copy", outfile]

        if os.path.exists(outfile):
            pass
        else:
            call(theCommand)

        m4a_file = os.path.splitext(self.videofile)[0] + ".m4a"
        mp3_file = os.path.splitext(self.videofile)[0] + ".mp3"
        newCommand = ["ffmpeg", "-i", m4a_file, "-acodec", "libmp3lame", "-ab", "192k", mp3_file]

        if os.path.exists(mp3_file):
            pass
        else:
            call(newCommand)

        return mp3_file


class AudioProcess(object):
    """
	
	"""

    def __init__(self, audiofile):
        """

		"""

        super(AudioProcess, self).__init__()
        self.audiofile = audiofile

    def periodCut(self, flag, starttime, endtime):
        """

		"""

        dirpath = os.path.dirname(self.audiofile)
        theformat = os.path.splitext(self.audiofile)[1]
        theformat = theformat.split(".")[1]

        track = AudioSegment.from_file(self.audiofile, theformat)
        mp3name = dirpath + os.sep + flag + ".mp3"
        song = track[starttime:endtime]
        song.export(mp3name, format="mp3", bitrate="192k")

    def mp3spltCut(self, flag, starttime, endtime):
        """
		
		"""

        if len(flag) < 3:
            flag = "0" * (3 - len(flag)) + flag
        mp3name = "./splits" + os.sep + "group-" + flag

        call(["mp3splt", self.audiofile, starttime, endtime, "-o", mp3name])

    def intervalCut(self, subinfo, interval):
        """

		"""

        q = deque()
        periods = []

        for i in subinfo:
            if len(q) < interval:
                q.append(i)
            else:
                b = q.popleft()[1]
                f = q.pop()[2]
                periods.append((b, f))
                q.clear()

        for p in periods:
            flag = str(periods.index(p))
            if len(flag) < 3:
                flag = "0" * (3 - len(flag)) + flag
            mp3name = "./splits" + os.sep + "group-" + flag
            call(["mp3splt", self.audiofile, p[0], p[1], "-o", mp3name])


def main(args):

    basedir = "/home/ulric/yr/workspace/py/manipulateMedia/media"
    mysubtitle = basedir + os.sep + "DeviousMaidsS04E08.srt"
    myvideo = basedir + os.sep + "DeviousMaidsS04E08.mkv"
    interval = 5

    mysubtitleinfo = SubtitleProcess(mysubtitle).getPieces()

    vp = VideoProcess(myvideo).extractAudio()

    ap = AudioProcess(vp).intervalCut(mysubtitleinfo, interval)

    """
	for i in range(len(mysubtitleinfo)):
		logo   = mysubtitleinfo[i][0]
		begin  = mysubtitleinfo[i][1]
		finish = mysubtitleinfo[i][2]
		ap.mp3spltCut(str(logo), begin, finish)
	"""

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
