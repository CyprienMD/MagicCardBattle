from Tkinter import *
import pickle
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

from tkMessageBox import showinfo

from functools import partial
import glob
import Card
#os.chdir('C:\Users\test\Documents\Programmation\MCB2')
def getCards(file_):
    all_cards={}
    #print "load cards in ",file_
    d = pickle.load( open(file_, "rb" ))
    all_cards.update(d)
    return all_cards

all_cards={}
for f in glob.glob("CardFiles/*_monsters.sav"):    
    #print "load cards in ",f
    try :
        d = pickle.load( open(f, "rb" ))
    except :
        print "#### ERROR with ",f
    all_cards.update(d)

all_deks={}
for f in glob.glob("Decks/*.dek"):    
    #print "load cards in ",f
    d = pickle.load( open(f, "r" ))
    all_deks.update(d)

#print "all_cards = ",all_cards
#print "all_deks = ",all_deks
blocked_decks = Card.get_blocked_decks()
get_blocked_decks = Card. get_blocked_decks
#all_cards = pickle.load( open( "all_monsters.sav", "rb" ))
#all_decks=pickle.load( open( "all_decks.sav", "rb" ))

from PIL import Image, ImageTk


class DeckCreator():
    def __init__(self,fenetre):
        
        self.galeries = []
        
        self.all_cards_open = getCards("CardFiles/unknown_monsters.sav")
        self.refreshCardSelector(fenetre)
        
        self.deck={}
        self.ima=[]
        self.fenetre1=Toplevel(master=fenetre)
        self.fenetre1.title("Clic to remove a card from deck")
        self.deck_widg=PanedWindow(master=self.fenetre1, orient=VERTICAL)
        
        self.name = StringVar()
        self.firstline=PanedWindow(master=self.fenetre1, orient=HORIZONTAL)
        self.name_wid=Entry(master=self.firstline, width=30,textvariable=self.name)
        
        self.name.set("default")   
        self.deck_stars=Label(master=self.firstline, text="0")
        self.firstline.add(self.deck_stars)
        self.firstline.add( self.name_wid)
        self.firstline.pack()
        self.loadDeck("Decks\\default") 
       # def choose():
         #   canvas.create_image(b,0 , anchor=NW, image = p)
        #canvas = Canvas(fenetre, width=189, height=277)
    def refreshCardSelector(self,fenetre):
        self.fenetre = fenetre
        self.im=[]
        nb_Carte_p_ligne=-1
        self.ligne=1
        #galerie2=None
        galerie1=PanedWindow(fenetre, orient=HORIZONTAL)
        self.stars=[]
        print self.all_cards_open
        for a in self.all_cards_open.keys():
            nb_Carte_p_ligne+=1
            if nb_Carte_p_ligne>10:
                nb_Carte_p_ligne=0
             #   a='galerie'                                           
              #  self.ligne+=1
                self.galeries.append(galerie1)
                galerie1=PanedWindow(fenetre, orient=HORIZONTAL)
            self.stars.append(a)
            self.all_cards_open[a].getCost()
            self.stars.append(self.all_cards_open[a].getStars())
            self.filename=a.replace(" ","_")+'.png'
            print self.filename
            image = Image.open("Cards/"+self.filename).resize((120,180))
            print image,"   ", type(image)==type(Image.open("Cards/"+self.filename))
            p  = ImageTk.PhotoImage(image)
            #print p
            self.im.append(p)
            #print a
            galerie1.pack()
           # galerie_utilisee='galerie'+self.ligne
           # if self.ligne==1:
            #print 'galerie'+str(self.ligne)
            #'galerie'+str(self.ligne).add(Button(str(a+self.ligne,  command=partial(self.addCard,a),image =p)))
            galerie1.add(Button(galerie1,  command=partial(self.addCard,a),image =p))
            #if self.ligne==2:              
              # if not galerie2:
               #    galerie2=PanedWindow(fenetre, orient=HORIZONTAL)
           #    galerie2.add(Button(galerie2,command=partial(self.addCard,a),image =p))
        #galerie2.pack()
        #str(a+self.ligne).pack()
        print "stars :",self.stars
        self.galerie1 = galerie1
        self.galeries.append(galerie1)
        
        #self.canvas = Canvas(fenetre1, width=189, height=277)
        galerie1.pack()
    def addCard(self,card_name) :
        print "addCard",card_name
        # print self.deck
        if card_name not in self.deck: 
            self.deck[card_name]=1
        else:
            self.deck[card_name]+=1
        self.showDeck()
    def removeCard(self,card_name) :
        print "removeCard",card_name
        self.deck[card_name]-=1
        if self.deck[card_name]<1:
            del self.deck[card_name]
        self.showDeck()
    def save(self):
        if self.stars > 15:
                showinfo("Careful...","Your deck have too much stars to be used in the Campaign (limit is 15)")
        name=self.name.get().strip().replace(" ","_")+".dek"
        if name[:6]!="Decks/" and name[:6]!="Decks\\" :
                print "deck put in Decks/"
                name="Decks/"+name
        print "save in",name
        import os.path
        if self.loaded and self.loaded!=name and self.loaded.replace('\\','/')!=name.replace('\\','/') and os.path.isfile(name) or (not(self.loaded) and os.path.isfile(name)):
                print "loaded ",self.loaded,"  cannot overwrite",name," !"
                showinfo("Impossible","You cannot overwrite an existing deck")
                return
            #name=self.name_wid.get()
        pickle.dump(self.deck , open( name, "wb" ) )
        print self.deck," saved"
        self.deck={} ; self.name.set("") ; self.loaded=None
        self.showDeck()        
#    def openDeck(self) :
#        from tkFileDialog import askopenfilename
#        #Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
#        filename = askopenfilename(defaultextension=".dek",filetypes=[('Deck file','*.dek')]) # show an "Open" dialog box and return the path to the selected file
#        self.name.set(filename[0:-3].replace("_"," "))
#        self.load()

    def openDeck(self,*args) :
        name = self.opening.get()
        if ("\\" in name and name[name.index("\\")+1:] in blocked_decks) or " (not available)" in name:
            lv = int(open("progression","r").read())
            print "La campagne est au niveau ",lv," /7"
            if lv >= 7:
                self.loadDeck(name)
            else:
                print "Deck is not accessible"
            """
            def validate(*args):
                if entree.get() == "Gandalf":
                    name=self.opening.get()
                    self.loadDeck(name)
                else:
                    #self.opening.set("Open another deck")
                    #self.opening.trace("w",self.openDeck)
                    pass
                new_fenetre.destroy()
                
                    
            new_fenetre = Tk()
            value = StringVar() 
            value.set("texte par defaut")
            label = Label(new_fenetre, text="Password (vous l'obtenez a la fin de la campagne):")
            label.pack()
            entree = Entry(new_fenetre, textvariable="string", width=45)
            entree.pack()
            button = Button(new_fenetre, text="Ok", command=validate,width=40)
            button.pack()
            """
        else:
            name=self.opening.get()
            self.loadDeck(name)
        #self.opening.set("open another deck")
    
    def changeFile(self,*args):
        
        name = self.files.get()
        self.all_cards_open = getCards(name)
        for galerie in self.galeries:
            galerie.pack_forget()
        self.galeries = []
        self.refreshCardSelector(self.fenetre)
    
    def changeAvatar(self,*args):
        name = self.avatars.get()
        self.deck["AvatarImage"]=name
        print "avatar image is now ",self.deck["AvatarImage"]
        self.showDeck()
        
    def loadDeck(self,name) :
        print "load",name
        self.name.set(name)
        name=name.replace(" ","_")+".dek"   
        self.loaded=name
        print " load ",name
        try :
            deck=pickle.load( open(name))
            print "deck is",deck
        except :
            deck={}
        self.deck=deck
        try:
            self.showDeck()
        except:
            print "error with showDeck"
            self.verifyDeck()
    def verifyDeck(self) :
        pass
        #print "verify deck"
        #for y in all_decks[self.opening.get()].keys():
        #    try:
        #        self.deck[y]
        #    except:
        #        pass
    def showDeck(self) :
        print "showDeck"
        if hasattr(self,"deck_widg") :
            self.deck_widg.pack_forget()
        self.deck_widg=PanedWindow(master=self.fenetre1, orient=VERTICAL)
        self.galerie_deck=PanedWindow(master=self.deck_widg, orient=VERTICAL)
        galerie1=PanedWindow(master=self.galerie_deck, orient=HORIZONTAL)
        galerie1.pack()
        galerie2=PanedWindow(master=self.galerie_deck, orient=HORIZONTAL)
        self.nb_card=0
        self.firstline.pack_forget()
        self.firstline=PanedWindow(master=self.fenetre1, orient=HORIZONTAL)
        print "name",self.name.get()
        self.name_wid=Entry(master=self.firstline, width=30,textvariable=self.name)
        self.stars=0
        DE=dict([(d.upper(),d) for d in self.deck])
        modify=[]
        for creature in self.deck :
            if (creature not in all_cards) and creature!="AvatarImage":
                if creature.upper() in DE :
                    self.deck[DE[creature.upper()]]=self.deck[creature]
                    modify.append(creature)
                else :
                    print "ERROR : Missing :",creature
        for c in modify :
            print "modified ",c
            del self.deck[c]
            try:
                print self.deck[DE[c.upper()]]
            except:
                print "error when capitalize card ",c
        for s,n in self.deck.items():
            if s != "AvatarImage":
                try:
                    all_cards[s].getCost()
                    self.stars+=all_cards[s].getStars()*n
                except:
                    del self.deck[s]
                    print "error with ",s
        print"stars",self.stars
        self.deck_stars=Label(master=self.firstline, text=self.stars)
        self.firstline.add(self.deck_stars)
        self.firstline.add( self.name_wid)
        self.firstline.pack()
        nb_card_in_line=0
        actual_zone=galerie1
        #self.ligne=1
        for c,n in self.deck.items():
            if c != "AvatarImage":
                nb_card_in_line+=1
                if nb_card_in_line==10:
                    actual_zone=galerie2
                    galerie2.pack()
              #     self.ligne+=1
                #print "list deck",c
                self.filename=c.replace(" ","_")+'.png'
                p = ImageTk.PhotoImage(Image.open("Cards/"+self.filename).resize((120,180)))
                self.ima.append(p)
                card_zone = PanedWindow(master=actual_zone, orient=VERTICAL)
                #nb_zone = PanedWindow(master=self.galerie_deck, orient=VERTICAL)
                card_zone.add(Button(master=card_zone,  command=partial(self.removeCard,c),image =p))
                card_zone.add(Button(width=17,master=card_zone,  command= partial(self.removeCard,c) ,text=str(n)))
                self.nb_card+=n
                actual_zone.add(card_zone)
            #self.galerie_deck.add(nb_zone)
        self.deck_widg.add(self.galerie_deck)
        #self.deck_widg.add(self.nb_monstres)
        self.deck_widg.add(Button(master=self.deck_widg,  command= None ,text=self.nb_card))
        self.opening = StringVar(self.deck_widg)
        self.opening.set("Open another deck")
        choice = [fname[0:-4].replace("_"," ") for fname in glob.glob("Decks/*.dek")]
        if choice :
            lv = int(open("progression","r").read())
            if lv<8:
              choice=[name+" (not available)"*(name[name.index("\\")+1:] in blocked_decks) for name in choice]
            open_wid = OptionMenu(self.deck_widg, self.opening,*choice)
            open_wid.pack()
            self.deck_widg.add(open_wid)
        self.opening.trace('w', self.openDeck)
        
        self.files = StringVar(self.deck_widg)
        self.files.set("Take Monsters from Files")        
        file_wid = OptionMenu(self.deck_widg, self.files,*glob.glob("CardFiles/*_monsters.sav"))
        file_wid.pack()
        self.files.trace('w', self.changeFile)
        self.deck_widg.add(file_wid)
        
        self.avatars = StringVar(self.deck_widg)
        try:
            print "avatar=",self.deck["AvatarImage"]
            self.avatars.set(self.deck["AvatarImage"])      
        except:
            self.avatars.set("Avatars/Chevalier_noir#.png ")
            self.deck["AvatarImage"] = "Avatars/Chevalier_noir#.png "
            print "no atribute avatarimage"
        avatar_wid = OptionMenu(self.deck_widg, self.avatars,*glob.glob("Avatars/*#.png"))
        avatar_wid.pack()
        self.avatars.trace('w', self.changeAvatar)
        self.deck_widg.add(avatar_wid)
        
        
        if self.nb_card>29:
            if self.stars <= 15:
                self.deck_widg.add(Button(master=self.deck_widg,  command= self.save ,text='save deck'))
            else:
                self.deck_widg.add(Button(master=self.deck_widg,  command= self.save ,text='save deck (but beware there is too much stars)'))
        else :
           self.deck_widg.add(Button(master=self.deck_widg,  command= None ,text='30 cards and 15 stars needed to save deck')) 
        print "fin show"
        self.deck_widg.pack()
        self.firstline.pack()

def select(deck_name):
    pass
    #all_cards = pickle.load( open( "all_monsters.sav", "rb" ))


#def utilisation_dict():
#        all_decks = pickle.load( open( "all_decks.sav", "rb" ))
#        print type(all_decks)
#        has_choosen=None
#        fenetre=Tk()
#        list_decks=PanedWindow(fenetre, orient=VERTICAL)
#        global i
#        for i in all_decks:
#            list_decks.add(Button(master=list_decks,command=partial(select,i),text=i))
#        list_decks.pack()


def change_to_list():
    all_decks = pickle.load( open( "all_decks.sav", "rb" ))
    all_cards = pickle.load( open( "all_monsters.sav", "rb" ))
    global a
    selected_deck=[]
    for d,c in all_decks[deck_name].items():
        k=all_cards[d]
        for v in range(c):
             selected_deck.append(k)
    a=selected_deck
    return selected_deck
    
#def utilisation_list(name=None):
#        all_cards = pickle.load( open( "all_monsters.sav", "rb" ))
#        print type(all_decks)
#        has_choosen=None
#        fenetre=Tk()
#        print '1 '
#        list_decks=PanedWindow(fenetre, orient=VERTICAL)
#        print '1 '
#        global i
#        print '1 '
#        for i in all_decks:
#            list_decks.add(Button(master=list_decks,command=partial(select,i),text=i))
#        list_decks.pack()
#        print '1 '
#        a=None
#        s=i
#        while s<10000000:
#            if a:
#                return a
#                fenetre.destroy()
#                break
#            s+=1
#        fenetre.destroy()

def run():
    fenetre = Tk()
    fenetre.title('Clic to add a monster to deck')
    a=DeckCreator(fenetre)
    fenetre.mainloop()

if __name__=='__main__':
    run()
    

        
        
        
        
        
        
        
        
        
        
