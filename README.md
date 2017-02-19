# TvHelper
Program to check if you favourite show released an episode this week.

You can enter up to 10 of your favourite shows to this program and it will display the show's Episode list with release dates and episode descriptions. You have to enter the show's only once and it will remember them the next time you run this program. You can update the show's information with just a click of a button!

Note: This program will create a directory C:\TvHelper to store all of it's data.
Note: Program tested only on Windows, there might be issues on other operating systems regarding library's used and data directory

# Installation

For this program to run properly, you need to install the following:

1. Python 2.x
2. Pickle - 
3. BeautifulSoup
4. lxml 


# How to use?

This program is fairly simple to use if all the correct library's are installed. Just run the script!

1. Press show manager
2. Fill in the information of the show's that you would like to be monitored. In the first column, enter the name of the show that you'd like to be displayed for you. In the second column add an imdb episode guide link. 
For instance: 
If I would like to monitor the show "Suits", I will type in "Suits in the first column and retrieve the episode guide link from www.imdb.com, which in this case is "http://www.imdb.com/title/tt1632701/episodes?ref_=tt_ov_epl"

3. Click "Save" and close the window from the corner (x)
4. Check "Enable download" from the bottom of the main menu
5. Click "Download new info" button on the same menu
6. Now the program will have all the show's info that you will need. Over couple of days/weeks this info might become outdated. Then just repeat steps 4-5.

# To do list:
1. Add "watched?" checkbox after each episode and save that data, so the next time you run the program you can see which of the episodes have you already watched.
