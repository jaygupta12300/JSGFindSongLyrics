from tkinter import *
import urllib
import re
import lxml.html
import unicodedata
import os


class Song(object):
    def __init__(self, artist, title):
        self.artist = self.__format_str(artist)
        self.title = self.__format_str(title)
        self.url = None
        self.lyric = None

    def __format_str(self, s):
        # remove paranthesis and contents
        s = s.strip()
        try:
            # strip accent
            s = ''.join(c for c in unicodedata.normalize('NFD', s)
                        if unicodedata.category(c) != 'Mn')
        except:
            pass
        s = s.title()
        return s

    def __quote(self, s):
        return urllib.parse.quote(s.replace(' ', '_'))

    def __make_url(self):
        artist = self.__quote(self.artist)
        title = self.__quote(self.title)
        artist_title = '%s:%s' % (artist, title)
        url = 'http://lyrics.wikia.com/' + artist_title
        self.url = url

    def update(self, artist=None, title=None):
        if artist:
            self.artist = self.__format_str(artist)
        if title:
            self.title = self.__format_str(title)

    def lyricwikia(self):
        self.__make_url()
        try:
            doc = lxml.html.parse(self.url)
            lyricbox = doc.getroot().cssselect('.lyricbox')[0]
        except IOError:
            self.lyric = ''
            return
        lyrics = []
        for node in lyricbox:
            if node.tag == 'br':
                lyrics.append('\n')
            if node.tail is not None:
                lyrics.append(node.tail)
        self.lyric = "".join(lyrics).strip()
        return self.lyric


if __name__ == '__main__':
    myGUI = Tk()
    songname = StringVar()
    singername = StringVar()
    def printLyrics():
        song = Song(artist=str(singername.get()), title=str(songname.get()))
        lyr = song.lyricwikia()
        root = Tk()
        root.title(songname.get()+" Lyrics Finder")
        S = Scrollbar(root)
        T = Text(root, height=30, width=50,font=20)
        S.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(INSERT, lyr)
        root.mainloop()

    myGUI.title("JSG Lyrics Finder")
    myGUI.geometry("500x200+500+150")
    myLabel = Label(text="Find Your Songs Lyrics", fg='red', bg='white', font=20).pack()
    mySong = Label(text="Song's Name", fg='red', bg='white', font=10).place(x=40, y=40)
    mySinger = Label(text="Singer's Name", fg='red', bg='white', font=10).place(x=40, y=80)
    textSong = Entry(textvariable=songname).place(x=220, y=40)
    textSinger = Entry(textvariable=singername).place(x=220, y=80)
    findlyrics = Button(text="Find Lyrics", bg='white', font=20, command=printLyrics).place(x=200, y=120)
    myGUI.mainloop()
