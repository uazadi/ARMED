import tkinter as tk
from tkinter import *
import webbrowser
from tkinter import font
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import os
from analogy_engine import apply_analogy
from add_new_dish import add_new_dish
LARGE_FONT = ("Verdana", 15)

from tkinter import *
from PIL import ImageTk, Image


def callback(event, url):
    webbrowser.open_new(url)


offset=0

class SeaofBTCapp(tk.Tk):
    frames = {}


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        for F in (StartPage, ShowResult, AddDish):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):
    def applyAnalogy(self,controller,tkvar2,dict):
        origin_cuisine=self.tkvar.get()
        origin_dish=self.tkvar3.get()
        destination_cuisine=tkvar2.get()
        vector=[]
        for key in dict:
            if dict[key].get():
                vector.append(key)


        results = apply_analogy(origin_cuisine=origin_cuisine,
                            origin_dish=origin_dish,
                            destination_cuisine=destination_cuisine,
                            num_of_suggestion=3,
                            filters=vector)


        app.frames[ShowResult].text1.configure(text=results[0][0])
        app.frames[ShowResult].text2.bind("<Button-1>", lambda a: webbrowser.open_new(results[0][3]))
        app.frames[ShowResult].text2.configure(text=results[1][0])
        app.frames[ShowResult].text2.bind("<Button-1>", lambda a: webbrowser.open_new(results[1][3]))
        app.frames[ShowResult].text3.configure(text=results[2][0])
        app.frames[ShowResult].text3.bind("<Button-1>", lambda a: webbrowser.open_new(results[2][3]))

        app.frames[ShowResult].conf1.configure(text="(with confidence: " + str(results[0][1]) + ")")
        app.frames[ShowResult].conf2.configure(text="(with confidence: " + str(results[1][1]) + ")")
        app.frames[ShowResult].conf3.configure(text="(with confidence: " + str(results[2][1]) + ")")

        i = Image.open(results[0][2])
        half = 0.3
        out = i.resize([int(half * s) for s in i.size])
        app.frames[ShowResult].img1 = ImageTk.PhotoImage(out)
        app.frames[ShowResult].panel1.configure(image=app.frames[ShowResult].img1)

        i = Image.open(results[1][2])
        half = 0.3
        out = i.resize([int(half * s) for s in i.size])
        app.frames[ShowResult].img2 = ImageTk.PhotoImage(out)
        app.frames[ShowResult].panel2.configure(image=app.frames[ShowResult].img2)

        i = Image.open(results[2][2])
        half = 0.3
        out = i.resize([int(half * s) for s in i.size])
        app.frames[ShowResult].img3 = ImageTk.PhotoImage(out)
        app.frames[ShowResult].panel3.configure(image=app.frames[ShowResult].img3)

        controller.show_frame(ShowResult)



    def dropDownCreator(self,a,b,c):
        self.tkvar3 = tk.StringVar(self)
        self.tkvar3.set("Select your dish")  # set the default option

        string = "./data/embeddings/" + str(self.tkvar.get()) + ".csv"
        array = []
        with open(string) as csv_file:
            # csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_file:
                array.append(row.strip().split(';')[0])
        dishes = array

        self.DropDown3 = tk.OptionMenu(self, self.tkvar3, *dishes)
        self.DropDown3.place(relx=0.244, rely=0.214, relheight=0.043, relwidth=0.134)
        self.DropDown3.configure(background="white")
        self.DropDown3.configure(text="Select your dish")
        self.DropDown3.configure(disabledforeground="#a3a3a3")
        self.DropDown3.configure(font="TkFixedFont")
        self.DropDown3.configure(foreground="#000000")
        self.DropDown3.configure(width=154)
        # tkvar3.trace("w", ret_dropdown)

    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)

        ingredient = []
        with open('./data/Ingredients.txt') as inputfile:
            for line in inputfile:
                ingredient.append(line.strip().split(' '))
        lista = [item for sublist in ingredient for item in sublist]


        _bgcolor = '#01d4b4'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        self.Label1 = tk.Label(self)
        self.Label1.place(relx=0.052, rely=0.112, height=46, width=262)
        self.Label1.configure(activebackground="#24ef1d")
        self.Label1.configure(activeforeground="#000000")
        self.Label1.configure(background="#5daf65")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Seleziona un piatto di tuo gradimento''')
        self.Label1.configure(width=262)


        self.tkvar = tk.StringVar(self)
        self.tkvar.set('italian')  # set the default option
        choices = {"african", "american", "british", "caribbean", "chinese", "east_european",
                   "french", "greek", "indian", "irish", "italian", "japanese", "korean", "mexican",
                   "nordic", "north_african", "pakistani", "portuguese", "south_american", "spanish",
                   "thai_and_south-east_asian", "turkish_and_middle_eastern"}



        self.DropDown = tk.OptionMenu(self, self.tkvar, *choices)
        self.DropDown.place(relx=0.052, rely=0.202, relheight=0.043, relwidth=0.134)
        self.DropDown.configure(background="white")
        self.DropDown.configure(disabledforeground="#a3a3a3")
        self.DropDown.configure(font="TkFixedFont")
        self.DropDown.configure(foreground="#000000")
        self.DropDown.configure(width=154)
        self.tkvar.trace("w",self.dropDownCreator)


        self.tkvar3 = tk.StringVar(self)
        self.tkvar3.set("Select your dish")  # set the default option

        string = "./data/embeddings/" + str(self.tkvar.get()) + ".csv"
        array = []
        with open(string) as csv_file:
            # csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_file:
                array.append(row.strip().split(';')[0])
        dishes = array


        self.DropDown3 = tk.OptionMenu(self, self.tkvar3, *dishes)
        self.DropDown3.place(relx=0.244, rely=0.214, relheight=0.043, relwidth=0.134)
        self.DropDown3.configure(background="white")
        #self.DropDown3.configure(text="Select your dish")
        self.DropDown3.configure(disabledforeground="#a3a3a3")
        self.DropDown3.configure(font="TkFixedFont")
        self.DropDown3.configure(foreground="#000000")
        self.DropDown3.configure(width=154)



        self.Label2 = tk.Label(self)
        self.Label2.place(relx=0.052, rely=0.315, height=46, width=292)
        self.Label2.configure(background="#5daf65")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Seleziona ora la cucina di destinazione''')
        self.Label2.configure(width=292)


        tkvar2 = tk.StringVar(self)

        def change_dropdown2(*args):
            print(tkvar2.get())

        tkvar2.set('Cuisine')  # set the default option
        self.DropDown2 = tk.OptionMenu(self, tkvar2, *choices)
        self.DropDown2.place(relx=0.061, rely=0.439, relheight=0.043, relwidth=0.134)
        self.DropDown2.configure(background="white")
        self.DropDown2.configure(disabledforeground="#a3a3a3")
        self.DropDown2.configure(font="TkFixedFont")
        self.DropDown2.configure(foreground="#000000")
        self.DropDown2.configure(width=154)
        #page1_AI_support.change_dropdown(tkvar2.get())
        tkvar2.trace("w", change_dropdown2)

        self.Label3 = tk.Label(self)
        self.Label3.place(relx=0.061, rely=0.517, height=96, width=332)
        self.Label3.configure(background="#5daf65")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Se lo desideri puoi aggiungere i seguenti filtri''')
        self.Label3.configure(width=332)

        filters = []
        with open('./data/filtri.txt') as inputfile:
            for line in inputfile:
                filters.append(line.strip().split(' '))
        filtri = [item for sublist in filters for item in sublist]

        DairyFree = tk.BooleanVar(self)
        EggFree = tk.BooleanVar(self)
        Vegan = tk.BooleanVar(self)
        Vegetarian = tk.BooleanVar(self)
        GlutenFree = tk.BooleanVar(self)
        NutFree = tk.BooleanVar(self)
        LowGlycemicIndex = tk.BooleanVar(self)
        PregnancyFriendly = tk.BooleanVar(self)
        LowCalories = tk.BooleanVar(self)


        self.Checkbutton1 = tk.Checkbutton(self)
        self.Checkbutton1.place(relx=0.061, rely=0.664, relheight=0.035, relwidth=0.084)
        self.Checkbutton1.configure(activebackground="#ececec")
        self.Checkbutton1.configure(activeforeground="#000000")
        self.Checkbutton1.configure(background="#5daf65")
        self.Checkbutton1.configure(command=lambda: print(DairyFree.get()))
        self.Checkbutton1.configure(disabledforeground="#a3a3a3")
        self.Checkbutton1.configure(foreground="#000000")
        self.Checkbutton1.configure(highlightbackground="#d9d9d9")
        self.Checkbutton1.configure(highlightcolor="black")
        self.Checkbutton1.configure(justify='left')
        self.Checkbutton1.configure(text='''Dairy Free''')
        #self.Checkbutton1.configure(variable=page1_AI_support.che56)
        self.Checkbutton1.configure(variable=DairyFree)
        #DairyFree.trace("w", var_states)


        self.Checkbutton2 = tk.Checkbutton(self)
        self.Checkbutton2.setvar(value='0')
        self.Checkbutton2.place(relx=0.166, rely=0.664, relheight=0.035, relwidth=0.076)
        self.Checkbutton2.configure(activebackground="#ececec")
        self.Checkbutton2.configure(activeforeground="#000000")
        self.Checkbutton2.configure(background="#5daf65")
        self.Checkbutton2.configure(disabledforeground="#a3a3a3")
        self.Checkbutton2.configure(foreground="#000000")
        self.Checkbutton2.configure(highlightbackground="#d9d9d9")
        self.Checkbutton2.configure(highlightcolor="black")
        self.Checkbutton2.configure(justify='left')
        self.Checkbutton2.configure(text='''Egg Free''')
        #self.Checkbutton2.configure(variable=page1_AI_support.che57)
        self.Checkbutton2.configure(variable=EggFree)
        self.Checkbutton2.configure(command=lambda: print(EggFree.get()))


        self.Checkbutton3 = tk.Checkbutton(self)
        self.Checkbutton3.place(relx=0.061, rely=0.72, relheight=0.035, relwidth=0.062)
        self.Checkbutton3.configure(activebackground="#ececec")
        self.Checkbutton3.configure(activeforeground="#000000")
        self.Checkbutton3.configure(background="#5daf65")
        self.Checkbutton3.configure(disabledforeground="#a3a3a3")
        self.Checkbutton3.configure(foreground="#000000")
        self.Checkbutton3.configure(highlightbackground="#d9d9d9")
        self.Checkbutton3.configure(highlightcolor="black")
        self.Checkbutton3.configure(justify='left')
        self.Checkbutton3.configure(text='''Vegan''')
        #self.Checkbutton3.configure(variable=page1_AI_support.che58)
        self.Checkbutton3.configure(variable=Vegan)


        self.Checkbutton4 = tk.Checkbutton(self)
        self.Checkbutton4.place(relx=0.061, rely=0.776, relheight=0.035, relwidth=0.088)
        self.Checkbutton4.configure(activebackground="#ececec")
        self.Checkbutton4.configure(activeforeground="#000000")
        self.Checkbutton4.configure(background="#5daf65")
        self.Checkbutton4.configure(disabledforeground="#a3a3a3")
        self.Checkbutton4.configure(foreground="#000000")
        self.Checkbutton4.configure(highlightbackground="#d9d9d9")
        self.Checkbutton4.configure(highlightcolor="black")
        self.Checkbutton4.configure(justify='left')
        self.Checkbutton4.configure(text='''Vegetarian''')
        #self.Checkbutton4.configure(variable=page1_AI_support.che59)
        self.Checkbutton4.configure(variable=Vegetarian)


        self.Checkbutton5 = tk.Checkbutton(self)
        self.Checkbutton5.place(relx=0.166, rely=0.72, relheight=0.035, relwidth=0.091)
        self.Checkbutton5.configure(activebackground="#ececec")
        self.Checkbutton5.configure(activeforeground="#000000")
        self.Checkbutton5.configure(background="#5daf65")
        self.Checkbutton5.configure(disabledforeground="#a3a3a3")
        self.Checkbutton5.configure(foreground="#000000")
        self.Checkbutton5.configure(highlightbackground="#d9d9d9")
        self.Checkbutton5.configure(highlightcolor="black")
        self.Checkbutton5.configure(justify='left')
        self.Checkbutton5.configure(text='''Gluten Free''')
        #self.Checkbutton5.configure(variable=page1_AI_support.che60)
        self.Checkbutton5.configure(variable=GlutenFree)


        self.Checkbutton6 = tk.Checkbutton(self)
        self.Checkbutton6.place(relx=0.166, rely=0.776, relheight=0.035, relwidth=0.074)
        self.Checkbutton6.configure(activebackground="#ececec")
        self.Checkbutton6.configure(activeforeground="#000000")
        self.Checkbutton6.configure(background="#5daf65")
        self.Checkbutton6.configure(disabledforeground="#a3a3a3")
        self.Checkbutton6.configure(foreground="#000000")
        self.Checkbutton6.configure(highlightbackground="#d9d9d9")
        self.Checkbutton6.configure(highlightcolor="black")
        self.Checkbutton6.configure(justify='left')
        self.Checkbutton6.configure(text='''Nut Free''')
        #self.Checkbutton6.configure(variable=page1_AI_support.che61)
        self.Checkbutton6.configure(variable=NutFree)


        self.Checkbutton7 = tk.Checkbutton(self)
        self.Checkbutton7.place(relx=0.279, rely=0.664, relheight=0.035, relwidth=0.139)
        self.Checkbutton7.configure(activebackground="#ececec")
        self.Checkbutton7.configure(activeforeground="#000000")
        self.Checkbutton7.configure(background="#5daf65")
        self.Checkbutton7.configure(disabledforeground="#a3a3a3")
        self.Checkbutton7.configure(foreground="#000000")
        self.Checkbutton7.configure(highlightbackground="#d9d9d9")
        self.Checkbutton7.configure(highlightcolor="black")
        self.Checkbutton7.configure(justify='left')
        self.Checkbutton7.configure(text='''Low Glycemic Index''')
        #self.Checkbutton7.configure(variable=page1_AI_support.che62)
        self.Checkbutton7.configure(variable=LowGlycemicIndex)


        self.Checkbutton8 = tk.Checkbutton(self)
        self.Checkbutton8.place(relx=0.279, rely=0.72, relheight=0.035, relwidth=0.133)
        self.Checkbutton8.configure(activebackground="#ececec")
        self.Checkbutton8.configure(activeforeground="#000000")
        self.Checkbutton8.configure(background="#5daf65")
        self.Checkbutton8.configure(disabledforeground="#a3a3a3")
        self.Checkbutton8.configure(foreground="#000000")
        self.Checkbutton8.configure(highlightbackground="#d9d9d9")
        self.Checkbutton8.configure(highlightcolor="black")
        self.Checkbutton8.configure(justify='left')
        self.Checkbutton8.configure(text='''Pregnancy Friendly''')
        #self.Checkbutton8.configure(variable=page1_AI_support.che63)
        self.Checkbutton8.configure(variable=PregnancyFriendly)


        self.Checkbutton9 = tk.Checkbutton(self)
        self.Checkbutton9.place(relx=0.279, rely=0.776, relheight=0.035, relwidth=0.099)
        self.Checkbutton9.configure(activebackground="#ececec")
        self.Checkbutton9.configure(activeforeground="#000000")
        self.Checkbutton9.configure(background="#5daf65")
        self.Checkbutton9.configure(disabledforeground="#a3a3a3")
        self.Checkbutton9.configure(foreground="#000000")
        self.Checkbutton9.configure(highlightbackground="#d9d9d9")
        self.Checkbutton9.configure(highlightcolor="black")
        self.Checkbutton9.configure(justify='left')
        self.Checkbutton9.configure(text='''Low Calories''')
        #self.Checkbutton9.configure(variable=page1_AI_support.che64)
        self.Checkbutton9.configure(variable=LowCalories)
        #print(LowCalories.get())



        dict={"dairy_free": DairyFree, "egg_free":EggFree, "vegan":Vegan, "vegetarian": Vegetarian,
              "gluten_free": GlutenFree, "nut_free": NutFree, "low_glycemic_index": LowGlycemicIndex,
              "pregnancy_friendly": PregnancyFriendly, "low_calories": LowCalories}
        self.Button1 = tk.Button(self)
        self.Button1.place(relx=0.654, rely=0.202, height=103, width=226)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#5daf65")
        self.Button1.configure(command=lambda: self.applyAnalogy(controller,tkvar2,dict))
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Avanti''')
        self.Button1.configure(width=226)

        self.Button2 = tk.Button(self)
        self.Button2.place(relx=0.793, rely=0.787, height=33, width=22)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#5daf65")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(command=lambda: controller.show_frame(AddDish))
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''+''')

        self.Label4 = tk.Label(self)
        self.Label4.place(relx=0.654, rely=0.664, height=56, width=312)
        self.Label4.configure(background="#5daf65")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Non hai trovato il tuo piatto? Aggiungilo!''')
        self.Label4.configure(width=312)

class ShowResult(tk.Frame):



    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Top 3 Reccomandations", font=("Verdana", 24), foreground="red")
        self.label.pack()

        self.text1 = tk.Label(self, text="", font=("Arial", 20), fg="blue", cursor="hand2")
        self.text1.pack(side="top", fill="both", expand="yes")

        self.conf1 = tk.Label(self, text="", font=("Arial", 12))
        self.conf1.pack(side="top", fill="both", expand="yes")

        i = Image.open(
            "./data/DatasetImages/american/American-style blueberry pancakes.jpg")
        half = 0.3
        out = i.resize([int(half * s) for s in i.size])

        self.img1 = ImageTk.PhotoImage(out)
        self.panel1 = Label(self, image=self.img1)
        self.panel1.pack(side="top", fill="both", expand="yes")

        self.text2 = Label(self, text="", font=("Arial", 20), fg="blue", cursor="hand2")
        self.text2.pack(side="top", fill="both", expand="yes")

        self.conf2 = tk.Label(self, text="", font=("Arial", 12))
        self.conf2.pack(side="top", fill="both", expand="yes")

        self.img2 = ImageTk.PhotoImage(out)
        self.panel2 = Label(self, image=self.img2)
        self.panel2.pack(side="top", fill="both", expand="yes")

        self.text3 = Label(self, text="", font=("Arial", 20), fg="blue", cursor="hand2")
        self.text3.pack(side="top", fill="both", expand="yes")

        self.conf3 = tk.Label(self, text="", font=("Arial", 12))
        self.conf3.pack(side="top", fill="both", expand="yes")

        self.img3 = ImageTk.PhotoImage(out)
        self.panel3 = Label(self, image=self.img3)
        self.panel3.pack(side="top", fill="both", expand="yes")

        button1 = tk.Button(self, text="Fai una nuova ricerca",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(side="bottom")


class AddDish(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ingrList = []
        label = tk.Label(self, text="Aggiungi un nuovo piatto", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


        self.tkvar4 = tk.StringVar(self)
        self.tkvar4.set('italian')  # set the default option
        choices = {"african", "american", "british", "caribbean", "chinese", "east_european",
                   "french", "greek", "indian", "irish", "italian", "japanese", "korean", "mexican",
                   "nordic", "north_african", "pakistani", "portuguese", "south_american", "spanish",
                   "thai_and_south-east_asian", "turkish_and_middle_eastern"}

        def getResult(*args):
            self.newCuisine=str(self.tkvar4.get())
            print(self.tkvar4.get())

        self.newCuisine=""
        self.DropDown4 = tk.OptionMenu(self, self.tkvar4, *choices)
        self.DropDown4.place(relx=0.052, rely=0.202, relheight=0.043, relwidth=0.134)
        self.DropDown4.configure(background="white")
        self.DropDown4.configure(disabledforeground="#a3a3a3")
        self.DropDown4.configure(font="TkFixedFont")
        self.DropDown4.configure(foreground="#000000")
        self.DropDown4.configure(width=154)
        # variable=tkvar.trace("w", change_dropdown)
        self.tkvar4.trace("w", getResult)
        # print(variabile)

        button1 = tk.Button(self, text="Indietro",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Avvia",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()


        button3 = tk.Button(self, text="Sfoglia...", command=self.load_file, width=10)
        button3.pack()


        button3 = tk.Button(self, text="Aggiungi ingrediente", command=self.addIngredient, width=10)
        button3.pack()

        self.entry= tk.Entry(self)
        self.entry.pack()

        button4 = tk.Button(self, text="Inserisci nome piatto", command=self.dishName, width=10)
        button4.pack()
        self.nameDish=""
        self.imagePath=""

    def dishName(self):
        a=str(self.entry.get())
        self.nameDish=a
        print(a)

    def load_file(self):
        fname = askopenfilename(filetypes=(("Jpeg files", "*.jpeg;*.jpg;*.JPG;*.JPEG"),
                                           ("All files", "*.*")))
        fname = os.path.realpath(fname)
        try:
            print(fname)
            self.imagePath=fname
        except:
            showerror("Open Source File", "Errore di lettura del file\n'%s'" % fname)
        return
    #def addIngredient(self,ingrList,controller):

    def addIngredient(self):
        ingredient = []
        global ingrList
        ingrList=[]
        with open('./data/Ingredients.txt') as inputfile:
            for line in inputfile:
                ingredient.append(line.strip().split(' '))
        lista = [item for sublist in ingredient for item in sublist]
        self.tkvar5 = tk.StringVar(self)

        def listIngredient(a,b,c):
            print(self.tkvar5.get())
            ingrList.append(str(self.tkvar5.get()))

        self.DropDown5 = tk.OptionMenu(self, self.tkvar5, *lista)
        self.DropDown5.place(relx=0.061, rely=0.439, relheight=0.043, relwidth=0.134)
        self.tkvar5.trace("w", listIngredient)
        app.update()

    def addNewDish(self,controller):

        correct = str(";".join(ingrList))
        results= add_new_dish(name=self.nameDish,
                     cuisine=self.newCuisine,
                     ingredients=correct,
                     path_image=self.imagePath)

        controller.show_frame(StartPage)


app = SeaofBTCapp()
app.mainloop()


