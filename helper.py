import os
import Tkinter as tk
import time
import datetime
import tkMessageBox
import textwrap
import pickle
from bs4 import BeautifulSoup
from urllib2 import urlopen

#Created by: 	Kaspar Kriisk
#Contact: 		kasparkriisk@gmail.com
#				2017

#TODO: 	
#	Watched? functionality		


destination = "C:\TvHelper" + "\data_links"
try:
	with open(destination,"rb") as f:
		ShowList = pickle.load(f)
except:
	ShowList = []


def print_episode_releases(episode_link): #Scraping provided imdb link and returning episode nr, release date and description
	html = urlopen(episode_link).read()
	soup = BeautifulSoup(html, "lxml")
	airdate_x = soup.findAll("div", { "class" : "airdate" })
	description_x = soup.findAll("div", { "class" : "item_description" })
	
	list_names = []
	array_index = []
	array_description = []
	array_names = [[], [], []]
	i = 1;
	for airdate in airdate_x:
		airdate_text = ''.join(airdate.findAll(text=True)).rstrip() 				
		text = os.linesep.join([s for s in airdate_text.splitlines() if s]) 		#Remove empty lines
		text = text.strip()															#Remove unneccessary spaces from string
		
		list_names.append(str(text))
		array_index.append(i)
		i = i + 1 
		
	for item_description in description_x:
		description_text = ''.join(item_description.findAll(text=True)).rstrip() 				
		des_text = os.linesep.join([s for s in description_text.splitlines() if s]) 		#Remove empty lines
		des_text = des_text.strip()															#Remove unneccessary spaces from string
		
		array_description.append(des_text.encode('utf-8'))
	
	#print array_description
	array_names[0] = array_index
	array_names[1] = list_names
	array_names[2] = array_description
	return array_names


def download_show_information(list): #Downloading ll show info and saves them to file
	dest_folder = "C:\TvHelper"
	if not os.path.exists(dest_folder):
		os.makedirs(dest_folder)
		
	for (name, link) in list:
		destination = dest_folder + "\data_" + name.replace(" ", "_")
		
		with open(destination,"wb") as f:
			information_list = print_episode_releases(link)
			pickle.dump(information_list,f)

def load_show_information(self, name): #Loading up one show from file (insert name from ShowList)
	dest_folder = "C:\TvHelper"
	destination = dest_folder + "\data_" + name.replace(" ", "_")
	with open(destination,"rb") as f:
		temp = pickle.load(f)
		display_show(self,temp)

	
def display_episode_description(self, description): #Displaying episode description
	tk.Label(self, text = textwrap.fill(description, 40), anchor = "w").grid(row=0,column=5, rowspan = 7, sticky="wens")

def create_show_buttons(self, list): #Creating radiobuttons for the show names
	i = 1
	global which_series
	global deleting_list
	try:
		for object in deleting_list:
			object.grid_forget()
	except:
		pass
	deleting_list = []
	which_series = tk.IntVar()
	for (name, link) in list:
		
		showbutton = tk.Radiobutton(self, text = name, variable = which_series, value = i, width = 15, anchor = "w", command = lambda i=i:load_show_information(self, list[i-1][0]))
		showbutton.grid(sticky="w", row=i+1, column=0)
		deleting_list.append(showbutton)
		i += 1
	
	global down_button
	down_button = tk.Button(self, text = "Download new info", state = "disabled", command = lambda: download_info(self))
	down_button.grid(sticky="w",row=1,column=0)
	
	global enable_download
	global enable_down_button
	enable_download = tk.IntVar()
	try:
		enable_down_button.pack_forget()
	except:
		pass
	enable_down_button = tk.Checkbutton(root,text="Enable download", anchor="w", variable=enable_download, command = lambda:download_button_toggle(self))
	#enable_down_button.grid(sticky="w",row=i,column=0, pady=10)
	enable_down_button.pack(side="bottom", fill="both", padx=10, pady = 0, anchor="w")
	add_show_button = tk.Button(self,text="Show manager        ",command = lambda: create_window(self), anchor="w")
	add_show_button.grid(sticky="w", row=0, column=0)

	
def save_show_list(): #Retrieving the user input and saving that to a file
	global ShowList
	array_one = []
	array_two = []
	array_combined = [[],[]]
	for names in list_of_names:
		if not names.get() == "":
			array_one.append(names.get())
	for links in list_of_links:
		if not links.get() == "":
			array_two.append(links.get())
	array_combined[0]=array_one
	array_combined[1]=array_two
	ShowList = zip(*array_combined)
	

	destination = "C:\TvHelper" + "\data_links"
	with open(destination,"wb") as f:
		pickle.dump(ShowList,f)

def close_window(self,window): #Refreshing the show list after the "Show Manager" window is closed
	global ShowList
	create_show_buttons(self,ShowList)
	window.destroy()

def create_window(self): #Creating the "Show Manager" window
	global list_of_names
	global list_of_links
	global ShowList

	window = tk.Toplevel(root)
	window.protocol("WM_DELETE_WINDOW", lambda: close_window(self, window))
	tk.Label(window, text="Show").grid(sticky="w",row=0,column=1)
	tk.Label(window, text="Episode Guide link").grid(sticky="w",row=0,column=2)
	tk.Button(window, text="Save", width=8, command = save_show_list).grid(sticky="w",row=0,column=0)
	show_text = tk.StringVar()
	link_text = tk.StringVar()
	row = 1
	list_of_names = []
	list_of_links = []

	for (name, link) in ShowList:
		show_entry = tk.Entry(window, width = 20)
		link_entry = tk.Entry(window, width = 70)
		show_entry.grid(sticky="w",row=row,column=1)
		link_entry.grid(sticky="w",row=row, column=2)
		list_of_names.append(show_entry)
		list_of_links.append(link_entry)
		#show_entry.insert(0,name)
		#link_entry.insert(0,link)
		list_of_names[(row-1)].insert(0,name)
		list_of_links[(row-1)].insert(0,link)

		row = row+1
	while row < 11:
		show_entry = tk.Entry(window, width = 20)
		link_entry = tk.Entry(window, width = 70)
		show_entry.grid(sticky="w",row=row,column=1)
		link_entry.grid(sticky="w",row=row, column=2)
		list_of_names.append(show_entry)
		list_of_links.append(link_entry)
		row = row+1


def download_info(self): #After "Download new info" button is pressed, disables it again, also the enabling button. Calls the download function when done.
	down_button["state"]="disabled"
	enable_download = False
	enable_down_button.deselect()
	download_show_information(ShowList)
	
def download_button_toggle(self): #Disabling and enabling the "Download new info" button
	global enable_download	
	if enable_download.get():
		down_button["state"] = "normal"
	else:
		down_button["state"] = "disabled"
def display_show(self,a): #Deleting previous show's data from screen and displaying a new one
    row = 1
    global var
    var = tk.IntVar()
    data = zip(*a)

    global list_of_widgets
    try:
        for (widget) in list_of_widgets:
            widget.grid_forget()
    except:
        pass
    list_of_widgets = []
	
    for (nr, name, active) in data:
        nr_label = tk.Label(self, text=str(nr), anchor="w")
        name_label = tk.Label(self, text=name,  anchor="e")
        #action_button =tk.Checkbutton(self, onvalue=True, offvalue=False, command = lambda nr=nr:save_watched_mark(self,nr-1))
        active_cb = tk.Radiobutton(self, variable = var, value = row, command = lambda nr=nr:display_episode_description(self, data[nr-1][2]))
        #if watched:
        #    action_button.select()
        #else:	
        #    action_button.deselect()

        name_label.grid(row=row, column=2, sticky="ew")
        nr_label.grid(row=row, column=1, sticky="ew")
        active_cb.grid(row=row, column=3, sticky="ew")
        #action_button.grid(row=row, column=4, sticky="ew")
		
        list_of_widgets.append(name_label)
        list_of_widgets.append(nr_label)
        #list_of_widgets.append(action_button)		
        list_of_widgets.append(active_cb)

        row += 1
class Example(tk.LabelFrame): #More initializing stuff and stuff that only needs to be run once
    def __init__(self, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="Episode nr", anchor="w").grid(row=0, column=1, sticky="ew")
        tk.Label(self, text="Release date", anchor="w").grid(row=0, column=2, sticky="ew")
        tk.Label(self, text="Description", anchor="w").grid(row=0, column=3, sticky="ew")
        #tk.Label(self, text="Watched", anchor="w").grid(row=0, column=4, sticky="ew")
        create_show_buttons(self,ShowList)
if __name__ == "__main__": #Initializing the program
    root = tk.Tk()
    root.wm_title("Tv helper 3000")
    Example(root, text=datetime.datetime.now().strftime ("%d %b %Y")).pack(side="top", fill="both", expand=True, padx=10, pady=10)
    root.mainloop()
