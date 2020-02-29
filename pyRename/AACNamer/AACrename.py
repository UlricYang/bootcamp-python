#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  AACrename.py
#
#  Copyright 2015 Ulric <Ulric@DESKTOP-MJ2I8ON>
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
import os.path
import re
from collections import Counter
from pprint import pprint
from shutil import move
from time import ctime

from mutagen.easymp4 import EasyMP4


class MyClassification:
    """

    """

    def __init__(self, filefolder):
        """
        sort things in "filefolder" into file or dir
        """
        self.filefolder = filefolder
        self.solos = []
        self.group = []
        for root, dirs, files in os.walk(self.filefolder):
            for f in files:
                self.solos.append(root + os.sep + f)
            break
        for root, dirs, files in os.walk(self.filefolder):
            for d in dirs:
                self.group.append(root + os.sep + d)
            break
        # print(self.group)

    def classify(self, folderpath):
        """

        """

        for w in os.walk(folderpath):
            files = [w[0] + os.sep + x for x in w[2] if x.endswith(".m4a")]
            break

        # artists = [AACInfo(f).getInfo('artist') for f in files]
        # albums  = [AACInfo(f).getInfo('album')  for f in files]
        artists_set = set([AACInfo(f).getInfo("artist") for f in files])
        albums_set = set([AACInfo(f).getInfo("album") for f in files])
        artists_sorted = sorted(list(artists_set), key=lambda x: len(x))
        albums_sorted = sorted(list(albums_set))

        myartist = artists_sorted[0]
        for a in artists_sorted + albums_sorted:
            if myartist in str(a):
                pass
            else:
                myartist = "None"

        cnt = len(files)

        logo = ""
        if myartist != "None":
            if len(albums_sorted) == 1:
                if cnt < 7:
                    logo = "EP"
                elif cnt < 20:
                    logo = "Album"
                else:
                    logo = "Collection"
            else:
                logo = "Collection"
        elif len(albums_sorted) == 1:
            logo = "Collection"
        else:
            logo = "chaos"

        return logo

    def sortation(self, folders):
        """

        """
        for s in self.solos:
            try:
                move(s, folders["singleFolder"])
            except Exception as e:
                print(e)

        for g in self.group:
            flag = self.classify(g) + "Folder"
            try:
                move(g, folders[flag])
            except Exception as e:
                print(e)


class AACInfo:
    """

    """

    flag = True

    def __init__(self, aacfilepath):
        """

        """
        self.songpath = aacfilepath
        try:
            self.audio = EasyMP4(self.songpath)
        except:
            # print(self.songpath)
            flag = False
            try:
                with open("failures.txt", "a+") as f:
                    f.writelines(str(self.songpath))
                    f.write("\n")
            except:
                pass

    def getInfo(self, tag):
        """

        """
        if self.flag:
            if tag in ["artist", "album", "title", "genre"]:
                taginfo = self.audio.tags[tag]
                return str(taginfo[0])
            elif tag == "tracknumber":
                tracknumber = audio.tags["tracknumber"][0].split("/")[0]
                return str(tracknumber)
        else:
            return self.flag


class AACRename:
    """

    """

    def __init__(self, pth):
        """

        """

        self.pth = pth

    def renameFile(self, filepath):
        """

        """

        aac = AACInfo(filepath)
        artist = aac.getInfo("artist")
        title = aac.getInfo("title")
        newname = os.path.split(filepath)[0] + os.sep + artist + " - " + title + ".m4a"
        oldname = filepath
        os.rename(oldname.encode("utf-8"), newname.encode("utf-8"))

    def renameFolder(self, folderpath, tag):
        """

        """

        artists = []
        albums = []
        for root, dirs, files in os.walk(folderpath):
            for fl in files:
                song = root + os.sep + fl
                if song.endswith(".m4a"):
                    artist = AACInfo(song).getInfo("artist")
                    album = AACInfo(song).getInfo("album")
                    artists.append(artist)
                    albums.append(album)
            break
        theArtist = Counter(artists).most_common(1)[0][0]
        theAlbum = Counter(albums).most_common(1)[0][0]

        oldname = folderpath

        try:
            if tag == "Album":
                newname = self.pth + os.sep + str(theArtist) + " - [[ " + str(theAlbum) + " ]]"
                os.rename(oldname.encode("utf-8"), newname.encode("utf-8"))
            if tag == "EP":
                newname = self.pth + os.sep + str(theArtist) + " - [[ " + str(theAlbum)
                newname = newname.replace("- EP", "]] - EP")
                os.rename(oldname.encode("utf-8"), newname.encode("utf-8"))
            if tag == "Collection":
                myartists = sorted(artists, key=lambda z: len(z))
                myartist = myartists[0]
                for m in myartists:
                    if myartist in m:
                        pass
                    else:
                        myartist = "None"
                if myartist != "None":
                    if len(set(albums)) == 1:
                        newname = "Collection - " + myartist + " - [[ " + theAlbum + " ]]"
                    else:
                        newname = "Collection - " + myartist
                else:
                    if len(set(albums)) == 1:
                        newname = "Collection - [[ " + theAlbum + " ]]"
                    else:
                        newname = os.path.split(oldname)[1]
                        print(oldname + "\nPlease do it manually\n\n")
                newname = self.pth + os.sep + newname
                os.rename(oldname.encode("utf-8"), newname.encode("utf-8"))
        except Exception as e:
            print(e)

    def renameAlbum(self):
        """

        """
        pattern = re.compile(r"[^\s][^\-\[\]]+ - \[\[ [^\-\[\]]+ \]\]")
        for root, dirs, files in os.walk(self.pth):
            for d in dirs:
                if pattern.match(d):
                    pass
                else:
                    albumpth = root + os.sep + d
                    albumpth.encode("utf-8")
                    # print(albumpth)
                    try:
                        if self.countFile(albumpth) == "Album":
                            self.renameFolder(albumpth, "Album")
                    except:
                        with open("failures.txt", "a+", encoding="utf-8") as f:
                            f.writelines(ctime() + "\n")
                            f.writelines(albumpth)
                            f.write("\n\n\n")

    def renameSingle(self):
        """

        """
        for root, dirs, files in os.walk(self.pth):
            for fl in files:
                singlepth = root + os.sep + fl
                # print(singlepth)
                singlepth.encode("utf-8")
                try:
                    self.renameFile(singlepth)
                except:
                    with open("failures.txt", "a+", encoding="utf-8") as f:
                        f.writelines(ctime() + "\n")
                        f.writelines(singlepth)
                        f.write("\n\n\n")

    def renameEP(self):
        """

        """
        pattern = re.compile(r"[^\s][^\-\[\]]+ - \[\[ [^\-\[\]]+ \]\] - EP")
        for root, dirs, files in os.walk(self.pth):
            for d in dirs:
                if pattern.match(d):
                    pass
                else:
                    eppth = root + os.sep + d
                    eppth.encode("utf-8")
                    try:
                        if self.countFile(eppth) == "EP":
                            self.renameFolder(eppth, "EP")
                    except:
                        with open("failures.txt", "a+") as f:
                            f.writelines(ctime() + "\n")
                            f.writelines(eppth)
                            f.write("\n\n\n")

    def renameCollection(self):
        """

        """
        for w in os.walk(self.pth):
            for d in w[1]:
                collectionpth = w[0] + os.sep + d
                collectionpth.encode("utf-8")
                try:
                    # if self.countFile(collectionpth)=='Collection':
                    self.renameFolder(collectionpth, "Collection")
                except:
                    with open("failures.txt", "a+") as f:
                        f.writelines(ctime() + "\n")
                        f.writelines(collectionpth)
                        f.write("\n\n\n")


class MyFilter:
    """

    """

    def __init__(self, pth):
        """

        """
        self.pth = pth

    def filterSingle(self, despath="E:\MyFun\Joy\Music\XYZ"):
        """

        """
        singlepattern = r"([^\-])+ - ([^\-])+.m4a\Z"
        mypattern = re.compile(singlepattern)
        for root, dirs, files in os.walk(self.pth):
            for f in files:
                try:
                    if mypattern.match(f):
                        pass
                    else:
                        if f.endswith(".m4a"):
                            print(root + os.sep + fl)
                            move(root + os.sep + f, despath)
                except:
                    pass

    def filterAlbum(self, despath="E:\MyFun\Joy\Music\XYZ"):
        """

        """
        albumpattern = r"([^\-])+ - (\[\[ )([^\-\[\]])+( \]\])\Z"
        mypattern = re.compile(albumpattern)
        for root, dirs, files in os.walk(self.pth):
            for d in dirs:
                try:
                    if mypattern.match(d):
                        pass
                    else:
                        move(root + os.sep + d, despath)
                        # print(d)
                except:
                    pass


def main(args):

    musicfolders = {
        "AlbumFolder": "/home/ulric/workspace/codes/py/AACNamer/music/album/",
        "EPFolder": "/home/ulric/workspace/codes/py/AACNamer/music/ep/",
        "singleFolder": "/home/ulric/workspace/codes/py/AACNamer/music/single",
        "CollectionFolder": "/home/ulric/workspace/codes/py/AACNamer/music/collection",
    }
    messFolder = "/home/ulric/workspace/script/py/AACNamer/music/xyz"

    Classification = MyClassification(messFolder).sortation(musicfolders)

    albums = AACRename(musicfolders["AlbumFolder"]).renameAlbum()
    eps = AACRename(musicfolders["EPFolder"]).renameEP()
    singles = AACRename(musicfolders["singleFolder"]).renameSingle()
    collections = AACRename(musicfolders["CollectionFolder"]).renameCollection()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
