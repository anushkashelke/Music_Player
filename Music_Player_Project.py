# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 18:51:53 2021

@author: DELL
"""

import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer
from PIL import Image,ImageTk

class Player(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.pack()
        if os.path.getsize('songs.pickle')>0:
            with open('songs.pickle','rb') as f:
                self.playlist=pickle.load(f)
        else:
            self.playlist=[]
        self.current=0
        self.paused=True 
        self.played=False 
        mixer.init()
        self.create_frame()
        self.control_widgets()
        self.tracklist_widgets()
        self.track_widgets()
        self.playing_state=False
    def create_frame(self):   #Creation of frames
        #to display name of current song
        self.track=tk.LabelFrame(self,text="Song Track",            
                                 font=("times new roman",15,"bold"),
                                 bg="black",fg="white",bd=5,relief=tk.GROOVE)
        self.track.configure(width=410,height=300)

        self.track.grid(row=0,column=0,padx=10,pady=10)
        #to display current playlist
        self.tracklist=tk.LabelFrame(self,text=f"Playlist-{str(len(self.playlist))}",
                                 font=("times new roman",15,"bold"),
                                 bg="pink",fg="black",bd=5,relief=tk.GROOVE)
        self.tracklist.configure(width=200,height=400)
        self.tracklist.grid(row=0,column=1,rowspan=3,pady=5,padx=10)
        #Control Buttons
        self.controls=tk.LabelFrame(self,text="Controls",
                                 font=("times new roman",15,"bold"),
                                 bg="white",fg="purple",bd=5,relief=tk.GROOVE)
        self.controls.configure(width=410,height=80)
        self.controls.grid(row=2,column=0,padx=5,pady=5)
        
    def track_widgets(self): 
        self.canvas=tk.Label(self.track,image=music)
        self.canvas.configure(width=410,height=240)
        self.canvas.grid(row=0,column=0)
        
        self.songtrack=tk.Label(self.track,font=("times new roman",15,"bold"),
                             bg='white',fg='dark blue')
        self.songtrack['text']='Mp3 Player'
        self.songtrack.configure(width=30,height=1) 
        self.songtrack.grid(row=1,column=0)
    def tracklist_widgets(self):
        
        self.scrollbar=tk.Scrollbar(self.tracklist,orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=1,rowspan=5,sticky='ns')
        self.list=tk.Listbox(self.tracklist,selectmode=tk.SINGLE,
                             yscrollcommand=self.scrollbar.set,selectbackground='sky blue')
        self.list.config(height=22)
        self.list.bind('<Double-1>',self.play_song)
        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0,column=0,rowspan=5)
    def control_widgets(self):
        self.loadSongs=tk.Button(self.controls,bg='yellow',fg='red',font=10)
        self.loadSongs['text']='Load Songs'
        self.loadSongs['command']=self.retrieve_songs 
        self.loadSongs.grid(row=0,column=0,padx=2)
        
        self.prev=tk.Button(self.controls,image=back)
        self.prev['command']=self.prev_song
        self.prev.grid(row=0,column=2)
        
        self.play=tk.Button(self.controls,image=play)
        self.play['command']=self.pause_song
        self.play.grid(row=0,column=3)
        
        self.next=tk.Button(self.controls,image=forward)
        self.next['command']=self.next_song
        self.next.grid(row=0,column=4)
        
    def retrieve_songs(self):
        self.songlist=[]
        music_file=filedialog.askdirectory()
        print(music_file)
        for root_,dirs,files in os.walk(music_file):
            for file in files:
                if os.path.splitext(file)[1]=='.mp3':
                    print(file)
                    path=music_file+'/'+file
                    self.songlist.append(path)
        if os.path.getsize('songs.pickle')>0:
         with open('songs.pickle','wt') as f:
           pickle.dump(self.songlist.f)            
        self.playlist=self.songlist
        self.tracklist['text']=f"Playlist-{str(len(self.playlist))}"
        self.list.delete(0,tk.END)
        self.enumerate_songs()            
    
    def play_song(self,event=None):
        if event is not None:
            self.current=self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i,bg='white')
        mixer.music.load(self.playlist[self.current])
        self.play['image']=pause_img
        self.paused=False
        self.played=True
        self.songtrack['anchor']='w'
        self.songtrack['text']=os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current,bg='sky blue')
        mixer.music.play()
        
    def pause_song(self):
        if not self.paused:
            self.paused=True
            mixer.music.pause()
            self.play['image']=play
            
        else:
            if self.played==False:
                self.play_song()
            self.paused=False
            mixer.music.unpause()
            self.play['image']=pause_img
            
    def prev_song(self):
        if self.current>0:
            self.current-=1
        else:
             self.current=0
        self.list.itemconfigure(self.current+1,bg='white')
        self.play_song()
        
    def next_song(self):
        if self.current<len(self.playlist)-1:
            self.current+=1
        else:
             self.current=0
        self.list.itemconfigure(self.current-1,bg='white')
        self.play_song()
    def enumerate_songs(self):
        for index,song in enumerate(self.playlist):
            self.list.insert(index,os.path.basename(song))
root=tk.Tk()
root.geometry('700x500')
root.wm_title("Mini Music Player")
music=PhotoImage(file=r'C:\Users\DELL\.spyder-py3\images\music.png')
back=PhotoImage(file=r'C:\Users\DELL\.spyder-py3\images\back.png')
forward=PhotoImage(file=r'C:\Users\DELL\.spyder-py3\images\forward.png')
play=PhotoImage(file=r'C:\Users\DELL\.spyder-py3\images\play.png')
pause_img=PhotoImage(file=r'C:\Users\DELL\.spyder-py3\images\pause.png')
app=Player(master=root)
app.mainloop()