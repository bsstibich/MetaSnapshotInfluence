import requests
import json
import tkinter as tk
from PIL import Image, ImageTk
import os

#webscraping api keys/tokens
API_KEY = "tMvgxviE2H6Q"
PROJECT_TOKEN_TS = "tdyj0ztiT9xd"
RUN_TOKEN_TS = "tTdcu05Tr6rE"

PROJECT_TOKEN_HSR = "tiZY0SRs8Sh0"
RUN_TOKEN_HSR = "t_CrEFKSATdD"
dirname = os.path.dirname(__file__)

#class for all tempostorm data
class TempoStorm:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    #download and manipulate data from parsehub
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        data = json.loads(response.text)
        decks = data['decks']
        temp = self.label_class(decks)
        outp = {i: 99 for i in temp}
        return data, outp


    #label classes of each deck based on the title of said deck
    def label_class(self, decks):
        i = 0
        outp = []
        for deck in decks:
            deck['title'] = deck['title'][0:-40]
            outp.append(deck['title'])
            outp.insert(i, (deck['title']))
            i += 1
            if "Demon Hunter" in deck['title']:
                deck['class'] = "demon hunter"

            if "Druid" in deck['title']:
                deck['class']= "druid"

            if "Hunter" in deck['title']:
                deck['class'] = "hunter"

            if "Mage" in deck['title']:
                deck['class'] = "mage"

            if "Paladin" in deck['title']:
                deck['class'] = "paladin"

            if "Priest" in deck['title']:
                deck['class'] = "priest"

            if "Rogue" in deck['title']:
                deck['class'] = "rogue"

            if "Shaman" in deck['title']:
                deck['class'] = "shaman"

            if "Warlock" in deck['title']:
                deck['class'] = "warlock"

            if "Warrior" in deck['title']:
                deck['class'] = "warrior"
            else:
                deck['class'] = "warlock"
            
        return outp
#class for all hsreplay data
class HSReplay:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    #download and manipulate data from parsehub
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        data = json.loads(response.text)

        decks = data['deck']
        decks = self.label_class(decks)
        self.floatify(decks)

        decksOld = data['deckOld']
        decksOld = self.label_class(decksOld)
        self.floatify(decksOld)
        self.label_class(data['deckList'])
        return data

    #turns popularity data into a float
    def floatify(self, decks):
        for deck in decks:
            deck['pop'] = deck['pop'][:-1]
            deck['pop'] = float(deck['pop'])
        return decks

    # Scans the title of each deck and applies a class to it
    def label_class(self, decks):
        for deck in decks:
            if "Demon Hunter" in deck['title']:
                deck['class'] = "demon hunter"

            if "Druid" in deck['title']:
                deck['class']= "druid"

            if "Hunter" in deck['title'] and "Demon" not in deck['title']:
                deck['class'] = "hunter"

            if "Mage" in deck['title']:
                deck['class'] = "mage"

            if "Paladin" in deck['title']:
                deck['Class'] = "Paladin"

            if "Priest" in deck['title']:
                deck['class'] = "priest"

            if "Rogue" in deck['title']:
                deck['class'] = "rogue"

            if "Shaman" in deck['title']:
                deck['class'] = "shaman"

            if "Warlock" in deck['title']:
                deck['class'] = "warlock"

            if "Warrior" in deck['title']:
                deck['class'] = "warrior"
            else:
                deck['class'] = "warlock"
        return decks

#gets the difference in popularity percentage for each deck, if the deck title is not the same it uses the card_match function to find which deck closest matchs
def differences(ts_decks, hs_decks, final):
    rin = -1
    for deckts in ts_decks['decks']:
        rin += 1
        for deckhs in hs_decks['deck']:

            for deckold in hs_decks['deckOld']:

                if deckold['title'] == deckhs['title']:
                    final[deckhs['title']] = round(deckhs['pop'] - deckold['pop'], 4)

                else:
                    if rin < 15:
                        title = card_match(hs_decks, ts_decks['decks'][rin])['title']
                        if deckold['title'] == title:
                            for deckhs1 in hs_decks['deck']:
                                for deckold1 in hs_decks['deckOld']:
                                    if deckold1['title'] == title and deckhs1['title'] ==  title:
                                        final[deckts['title']] = round(deckhs1['pop'] - deckold1['pop'], 4)
            
#goes through each hsreplay deck and compares them to the tempostorm decks and returns the closest matching deck
def card_match(hs_decks, checkdeck):
    outp = {'title':'',
            'match': 0}
    for deckHS in hs_decks['deckList']:
        if not 'class' in deckHS:
            deckHS['class'] = 'reee'
        if deckHS['class'] == checkdeck['class']:
            rin = 0
            for cardHS in deckHS['cards']:
                for cardTS in checkdeck['cards']:
                    if cardHS['name'] == cardTS['name']:
                        rin += 1
                if outp['match'] < rin:
                    outp['match'] = rin
                    outp['title'] = deckHS['title']
    return outp

print("Loading...")
print("Please note that recent balance changes may influence usage statistics.")
dataTS = TempoStorm(API_KEY, PROJECT_TOKEN_TS)
ts_decks = dataTS.get_data()[0]
final = dataTS.get_data()[1]

dataHSR = HSReplay(API_KEY, PROJECT_TOKEN_HSR)
hsdecks = dataHSR.get_data()
differences(ts_decks, hsdecks, final)


#start of gui

#gives each deck the proper icon, same script as label class in previous section
def class_icons(title, label):
    if "Demon Hunter" in title:
        label['image'] = demonrender

    if "Druid" in title:
        label['image'] = druidrender

    if "Hunter" in title and "Demon" not in title:
        label['image'] = hunterrender

    if "Mage" in title:
        label['image'] = magerender

    if "Paladin" in title:
        label['image'] = pallyrender

    if "Priest" in title:
        label['image'] = priestrender

    if "Rogue" in title:
        label['image'] = roguerender

    if "Shaman" in title:
        label['image'] = shamanrender

    if "Warlock" in title:
        label['image'] = lockrender

    if "Warrior" in title:
        label['image'] = warriorrender

#checks to see if the percent is ><= 0 and changes visuals
def number_manip(percent, label): #add + if positive and do red/green
    if percent > 0:
        label['text'] = "+{}%".format(percent)
        label['fg'] = 'green'
    elif percent < 0:
        label['text'] = "{}%".format(percent)
        label['fg'] = '#eb2a3a'
    else:
        label['text'] = " {}%".format(percent)

#button fucntion that distributes all the data into the gui
def buttonf(final):
    decks = list(final.keys())
    percents = list(final.values())

    decklabel1['text'] = decks[0]
    poplabel1['text'] = percents[0]
    class_icons(decks[0], classlabel1)
    number_manip(percents[0],poplabel1)

    decklabel2['text'] = decks[1]
    poplabel2['text'] = percents[1]
    class_icons(decks[1], classlabel2)
    number_manip(percents[1],poplabel2)

    decklabel3['text'] = decks[2]
    poplabel3['text'] = percents[2]
    class_icons(decks[2], classlabel3)
    number_manip(percents[2],poplabel3)

    decklabel4['text'] = decks[3]
    poplabel4['text'] = percents[3]
    class_icons(decks[3], classlabel4)
    number_manip(percents[3], poplabel4)

    decklabel5['text'] = decks[4]
    poplabel5['text'] = percents[4]
    class_icons(decks[4], classlabel5)
    number_manip(percents[4],poplabel5)

    decklabel6['text'] = decks[5]
    poplabel6['text'] = percents[5]
    class_icons(decks[5], classlabel6)
    number_manip(percents[5],poplabel6)

    decklabel7['text'] = decks[6]
    poplabel7['text'] = percents[6]
    class_icons(decks[6], classlabel7)
    number_manip(percents[6],poplabel7)

#gui building
HEIGHT = 800
WIDTH = 800
bgbrown = '#2e2918'
labeltan = '#b98220'
textwhite = '#f2f0da'

#base
root = tk.Tk()
root.title("Meta Snapshot Influence")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
frame = tk.Frame(root, bg= bgbrown,)
frame.place(relx=0.5, rely=0, relheight=1, relwidth=1, anchor="n")

button = tk.Button(frame,text="Calculate Meta Influence",font=('ariel',18), bg=labeltan,fg=textwhite,command=lambda: buttonf(final))
button.place(relx=0.25,rely=0.820, relheight=0.150, relwidth=0.49)

#labels for both deck title and influence percentage
titlelabel = tk.Label(frame,font=('ariel',18),bg=bgbrown,fg=textwhite, anchor='w', justify='left',bd=20, text = "Deck Title\t\t\t\t      Influence")
titlelabel.place(relx=0.1,rely=0.01, anchor='nw',relwidth=0.87,relheight=0.07)

decklabel1 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
decklabel1.place(relx=0.1,rely=0.1, anchor='nw',relwidth=0.70,relheight=0.07)

decklabel2 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
decklabel2.place(relx=0.10,rely=0.2, anchor='nw',relwidth=0.70,relheight=0.07)

decklabel3 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
decklabel3.place(relx=0.1,rely=0.3, anchor='nw',relwidth=0.70,relheight=0.07)

decklabel4 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
decklabel4.place(relx=0.1,rely=0.4, anchor='nw',relwidth=0.70,relheight=0.07)

decklabel5 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
decklabel5.place(relx=0.1,rely=0.5, anchor='nw',relwidth=0.70,relheight=0.07)

decklabel6 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
decklabel6.place(relx=0.1,rely=0.6, anchor='nw',relwidth=0.70,relheight=0.07)

decklabel7 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
decklabel7.place(relx=0.1,rely=0.7, anchor='nw',relwidth=0.70,relheight=0.07)

poplabel1 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
poplabel1.place(relx=0.82,rely=0.1, anchor='nw',relwidth=0.15,relheight=0.07)

poplabel2 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
poplabel2.place(relx=0.82,rely=0.2, anchor='nw',relwidth=0.15,relheight=0.07)

poplabel3 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
poplabel3.place(relx=0.82,rely=0.3, anchor='nw',relwidth=0.15,relheight=0.07)

poplabel4 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
poplabel4.place(relx=0.82,rely=0.4, anchor='nw',relwidth=0.15,relheight=0.07)

poplabel5 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
poplabel5.place(relx=0.82,rely=0.5, anchor='nw',relwidth=0.15,relheight=0.07)

poplabel6 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
poplabel6.place(relx=0.82,rely=0.6, anchor='nw',relwidth=0.15,relheight=0.07)

poplabel7 = tk.Label(frame,font=('ariel',18),bg=labeltan,fg=textwhite, anchor='nw', justify='left',bd=20)
poplabel7.place(relx=0.82,rely=0.7, anchor='nw',relwidth=0.15,relheight=0.07)

#class images
lockload = Image.open(os.path.join(dirname, 'class icons','warlock.gif'))
lockrender = ImageTk.PhotoImage(lockload)

shamanload = Image.open(os.path.join(dirname, 'class icons','shaman.gif'))
shamanrender = ImageTk.PhotoImage(shamanload)

demonload = Image.open(os.path.join(dirname, 'class icons','demonhunter.gif'))
demonrender = ImageTk.PhotoImage(demonload)

druidload = Image.open(os.path.join(dirname, 'class icons','druid.gif'))
druidrender = ImageTk.PhotoImage(druidload)

hunterload = Image.open(os.path.join(dirname, 'class icons','hunter.gif'))
hunterrender = ImageTk.PhotoImage(hunterload)

mageload = Image.open(os.path.join(dirname, 'class icons','mage.gif'))
magerender = ImageTk.PhotoImage(mageload)

pallyload = Image.open(os.path.join(dirname, 'class icons','pally.gif'))
pallyrender = ImageTk.PhotoImage(pallyload)

priestload = Image.open(os.path.join(dirname, 'class icons','priest.gif'))
priestrender = ImageTk.PhotoImage(priestload)

rogueload = Image.open(os.path.join(dirname, 'class icons','rogue.gif'))
roguerender = ImageTk.PhotoImage(rogueload)

warriorload = Image.open(os.path.join(dirname, 'class icons','warrior.gif'))
warriorrender = ImageTk.PhotoImage(warriorload)


classlabel1 = tk.Label(frame,bg=bgbrown,fg=textwhite, anchor='center', justify='center',bd=20, image = lockrender)
classlabel1.place(relx=0.015,rely=0.1, anchor='nw',relwidth=0.07,relheight=0.07)

classlabel2 = tk.Label(frame,bg=bgbrown,fg=textwhite, anchor='center', justify='center',bd=20, image = warriorrender)
classlabel2.place(relx=0.015,rely=0.2, anchor='nw',relwidth=0.07,relheight=0.07)

classlabel3 = tk.Label(frame,bg=bgbrown,fg=textwhite, anchor='center', justify='center',bd=20, image = shamanrender)
classlabel3.place(relx=0.015,rely=0.3, anchor='nw',relwidth=0.07,relheight=0.07)

classlabel4 = tk.Label(frame,bg=bgbrown,fg=textwhite, anchor='center', justify='center',bd=20, image = demonrender)
classlabel4.place(relx=0.015,rely=0.4, anchor='nw',relwidth=0.07,relheight=0.07)

classlabel5 = tk.Label(frame,bg=bgbrown,fg=textwhite, anchor='center', justify='center',bd=20, image = druidrender)
classlabel5.place(relx=0.015,rely=0.5, anchor='nw',relwidth=0.07,relheight=0.07)

classlabel6 = tk.Label(frame,bg=bgbrown,fg=textwhite, anchor='center', justify='center',bd=20, image = hunterrender)
classlabel6.place(relx=0.015,rely=0.6, anchor='nw',relwidth=0.07,relheight=0.07)

classlabel7 = tk.Label(frame,bg=bgbrown,fg=textwhite, anchor='center', justify='center',bd=20, image = priestrender)
classlabel7.place(relx=0.015,rely=0.7, anchor='nw',relwidth=0.07,relheight=0.07)

root.mainloop()



