from tkinter import messagebox
from firebase import firebase
from threading import Thread
from app import Content
from tkinter import *
import PIL.ImageTk
import PIL.Image
import re
#commemt

class Netflix:
    def __init__(self):
        self.screen = Tk()
        self.database = firebase.FirebaseApplication("https://netflix-8c648-default-rtdb.firebaseio.com/", None)
        self.content = Content()

        self.screenWidth = self.screen.winfo_screenwidth()
        self.screenHeight = self.screen.winfo_screenheight()

        self.screen.geometry(f"{self.screenWidth}x{self.screenHeight}")
        self.screen.title("Netflix")
        self.screen.resizable(True, True)
        self.screen.iconbitmap("icon.ico")
        self.screen.attributes("-alpha", 1)
        self.screen.protocol("WM_DELETE_WINDOW", self.closeScreen)

        self.regexEmail = "^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"
        self.patternPassword = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$"

        self.patternEmail = re.compile(self.regexEmail)
        self.patternPassword = re.compile(self.patternPassword)

        self.email = StringVar()
        self.signInEmail = StringVar()
        self.signInPassword = StringVar()
        self.signInCheck = BooleanVar()
        self.signUpEmail = StringVar()
        self.signUpPassword = StringVar()
        self.needHelpEmail = StringVar()

        self.backgroundImage = PIL.Image.open("img/bg.png")
        self.backgroundImage = self.backgroundImage.resize((self.screenWidth, self.screenHeight))
        self.backgroundImage = PIL.ImageTk.PhotoImage(self.backgroundImage)

        self.logoImage = PIL.Image.open("img/logo.png")
        self.logoImage = self.logoImage.resize((200, 50))
        self.logoImage = PIL.ImageTk.PhotoImage(self.logoImage)

        self.show_1_Image = PIL.Image.open("img/show_1.jpg")
        self.show_1_Image = self.show_1_Image.resize((288, 200))
        self.show_1_Image = PIL.ImageTk.PhotoImage(self.show_1_Image)

        self.backgroundImageLabel = Label(self.screen, image=self.backgroundImage)
        self.backgroundImageLabel.pack()

        self.logoImageLabel = Label(self.screen, image=self.logoImage, bg='black')
        self.logoImageLabel.place(x=50, y=30)

        self.screenManager()
        self.screen.mainloop()

    def screenManager(self):
        self.signInFrame = Frame(self.screen, width=430, height=650, bg="#191919")
        self.signUpFrame = Frame(self.screen, width=430, height=650, bg="#191919")
        self.needHelpFrame = Frame(self.screen, width=430, height=550, bg="#191919")

        self.homeScreen()

    def homeScreen(self):
        self.signInButton = Button(self.screen, text="Sign In", font=("Netflix Sans", 16, "bold"), bd=0, bg="red", fg="white", command=self.signInScreen)
        self.signInButton.place(x=1400, y=30)

        self.homeScreenEmailButton = Button(self.screen, width=10, text="Email", font=("Netflix Sans", 19, "bold"), bd=0, bg="red", fg="white", state="disable")
        self.homeScreenEmailButton.place(x=324, y=400)

        self.emailEntry = Entry(self.screen, textvariable=self.email, width=25, font=("Netflix Sans", 30))
        self.emailEntry.place(x=480, y=400)

        self.getStartedButton = Button(self.screen, text="Get Started", font=("Netflix Sans", 19, "bold"), bd=0, bg="red", fg="white", command=self.validateEmail)
        self.getStartedButton.place(x=1034, y=400)

        self.emailEntry.focus()

    def signInScreen(self, event=None):
        self.signInButton.destroy()
        self.homeScreenEmailButton.destroy()
        self.emailEntry.destroy()
        self.getStartedButton.destroy()

        self.signInFrame = Frame(self.screen, width=430, height=650, bg="#191919")
        self.signInFrame.place(x=550, y=100)

        self.signInFrameLabel = Label(self.signInFrame, text="Sign In", font=("Netflix Sans", 26, "bold"), bg="#191919", fg="white")
        self.signInFrameLabel.place(x=55, y=50)

        self.signInFrameEmailLabel = Label(self.signInFrame, text="Email", font=("Netflix Sans", 16, "bold"), bg="#191919", fg="white")
        self.signInFrameEmailLabel.place(x=55, y=130)

        self.signInFrameEmailEntry = Entry(self.signInFrame, textvariable=self.signInEmail, width=20, font=("Netflix Sans", 20))
        self.signInFrameEmailEntry.place(x=55, y=180)

        self.signInFramePasswordLabel = Label(self.signInFrame, text="Password", font=("Netflix Sans", 16, "bold"), bg="#191919", fg="white")
        self.signInFramePasswordLabel.place(x=55, y=230)

        self.signInFramePasswordEntry = Entry(self.signInFrame, textvariable=self.signInPassword, width=20, font=("Netflix Sans", 20))
        self.signInFramePasswordEntry.place(x=55, y=280)

        self.signInFrameButton = Button(self.signInFrame, text="Sign In", width=20, font=("Netflix Sans", 19, "bold"), bd=0, bg="red", fg="white", command=self.login)
        self.signInFrameButton.place(x=55, y=370)

        self.signInFrameCheckButton = Checkbutton(self.signInFrame, text="Remember me", font=("Netflix Sans", 12), fg="white", bg="#191919", variable=self.signInCheck)
        self.signInFrameCheckButton.place(x=50, y=440)

        self.signInFrameHelplabel = Label(self.signInFrame, text="Need help?", font=("Netflix Sans", 12), bg="#191919", fg="white")
        self.signInFrameHelplabel.place(x=280, y=440)

        self.signInFrameNewlabel = Label(self.signInFrame, text="New to Netflix?", font=("Netflix Sans", 12), bg="#191919", fg="white")
        self.signInFrameNewlabel.place(x=55, y=571)

        self.signInFrameSignUplabel = Label(self.signInFrame, text="Sign up now.", font=("Netflix Sans", 12), bg="#191919", fg="white")
        self.signInFrameSignUplabel.place(x=170, y=571)

        self.signInFrameEmailEntry.focus()

        email = self.email.get()
        self.signInFrameEmailEntry.insert(0, email)

        self.signInFrameSignUplabel.bind("<Button-1>", self.signUpScreen)
        self.signInFrameHelplabel.bind("<Button-1>", self.needHelpScreen)

    def signUpScreen(self, event=None):
        self.signInFrame.destroy()

        self.signUpFrame = Frame(self.screen, width=430, height=650, bg="#191919")
        self.signUpFrame.place(x=550, y=100)

        self.signUpFrameLabel = Label(self.signUpFrame, text="Sign Up", font=("Netflix Sans", 26, "bold"), bg="#191919", fg="white")
        self.signUpFrameLabel.place(x=55, y=50)

        self.signUpFrameEmailLabel = Label(self.signUpFrame, text="Email", font=("Netflix Sans", 16, "bold"), bg="#191919", fg="white")
        self.signUpFrameEmailLabel.place(x=55, y=130)

        self.signUpFrameEmailEntry = Entry(self.signUpFrame, textvariable=self.signUpEmail, width=20, font=("Netflix Sans", 20))
        self.signUpFrameEmailEntry.place(x=55, y=180)

        self.signUpFramePasswordLabel = Label(self.signUpFrame, text="Password", font=("Netflix Sans", 16, "bold"), bg="#191919", fg="white")
        self.signUpFramePasswordLabel.place(x=55, y=230)

        self.signUpFramePasswordEntry = Entry(self.signUpFrame, textvariable=self.signUpPassword, width=20, font=("Netflix Sans", 20), show="*")
        self.signUpFramePasswordEntry.place(x=55, y=280)

        self.signUpFrameButton = Button(self.signUpFrame, text="Sign Up", width=20, font=("Netflix Sans", 19, "bold"), bd=0, bg="red", fg="white", command=self.register)
        self.signUpFrameButton.place(x=55, y=370)

        self.signUpFrameNewlabel = Label(self.signUpFrame, text="Already a user?", font=("Netflix Sans", 12), bg="#191919", fg="white")
        self.signUpFrameNewlabel.place(x=55, y=571)

        self.signUpFrameSignInlabel = Label(self.signUpFrame, text="Sign in now.", font=("Netflix Sans", 12), bg="#191919", fg="white")
        self.signUpFrameSignInlabel.place(x=170, y=571)

        self.signUpFrameEmailEntry.focus()
        self.signUpFrameSignInlabel.bind("<Button-1>", self.signInScreen)

    def needHelpScreen(self, event=None):
        self.signInFrame.destroy()
        self.signUpFrame.destroy()

        self.needHelpFrame = Frame(self.screen, width=430, height=550, bg="#191919")
        self.needHelpFrame.place(x=550, y=170)

        self.needHelpFrameLabel = Label(self.needHelpFrame, text="Forgot Password", font=("Netflix Sans", 26, "bold"), bg="#191919", fg="white")
        self.needHelpFrameLabel.place(x=55, y=50)

        self.needHelpFrameLabel_1 = Label(self.needHelpFrame, text="We will send you an email with instructions", font=("Netflix Sans", 12), bg="#191919", fg="white")
        self.needHelpFrameLabel_1.place(x=55, y=130)

        self.needHelpFrameLabel_2 = Label(self.needHelpFrame, text="on how to reset your password.", font=("Netflix Sans", 12), bg="#191919", fg="white")
        self.needHelpFrameLabel_2.place(x=55, y=160)

        self.needHelpFrameEmailLabel = Label(self.needHelpFrame, text="Email", font=("Netflix Sans", 16, "bold"), bg="#191919", fg="white")
        self.needHelpFrameEmailLabel.place(x=55, y=210)

        self.needHelpFrameEmailEntry = Entry(self.needHelpFrame, textvariable=self.needHelpEmail, width=21, font=("Netflix Sans", 20))
        self.needHelpFrameEmailEntry.place(x=55, y=260)

        self.needHelpFrameButton = Button(self.needHelpFrame, text="Email Me", width=21, font=("Netflix Sans", 19, "bold"), bd=0, bg="red", fg="white", command=self.forgotPassword)
        self.needHelpFrameButton.place(x=55, y=360)

        self.needHelpFrameEmailEntry.focus()

    def showCardsScreen(self):
        self.signInFrame.destroy()
        self.signUpFrame.destroy()

        movies = self.content.latest_movies(3)
        tv_shows = self.content.latest_tv_shows(3)

        movie_title = movies['title'].to_list()
        tv_show_title = tv_shows['title'].to_list()

        # Showing latest movies -

        x = 190

        for i in range(3):
            self.showCard = Frame(self.screen, width=300, height=265, bg="#191919", bd=4)
            self.showCard.place(x=x, y=150)

            self.showCardImagelabel = Label(self.showCard, image=self.show_1_Image, bg='#191919')
            self.showCardImagelabel.place(x=0, y=0)

            self.showCardTitlelabel = Label(self.showCard, text=movie_title[i], width=22, font=("Netflix Sans", 16, "bold"), fg="white", bg='red', height=2)
            self.showCardTitlelabel.place(x=0, y=203)

            x += 400

        # Showing latest tv shows -

        x = 190

        for i in range(3):
            self.showCard = Frame(self.screen, width=300, height=265, bg="#191919", bd=4)
            self.showCard.place(x=x, y=550)

            self.showCardImagelabel = Label(self.showCard, image=self.show_1_Image, bg='#191919')
            self.showCardImagelabel.place(x=0, y=0)

            self.showCardTitlelabel = Label(self.showCard, text=tv_show_title[i], width=22, font=("Netflix Sans", 16, "bold"), fg="white", bg='red', height=2)
            self.showCardTitlelabel.place(x=0, y=203)

            x += 400

    def showRecommendations(self):
        self.signInFrame.destroy()
        self.signUpFrame.destroy()

        watched_movies = {
            'director': ['Toshiya Shinohara', 'Hajime Kamegaki'],
            'cast': ['Kofi Ghanaba', 'Johny Lever']
        }

        watched_tv_shows = {
            'director': ['Cecilia Peck', 'Stuart Orme'],
            'cast': ['Linor Abargil', 'Linor Abargil']
        }

        movies = self.content.recommended_movies(watched_movies, 3)
        tv_shows = self.content.recommended_tv_shows(watched_tv_shows, 3)

        # Showing latest movies -

        x = 190

        for i in range(3):
            self.showCard = Frame(self.screen, width=300, height=265, bg="#191919", bd=4)
            self.showCard.place(x=x, y=150)

            self.showCardImagelabel = Label(self.showCard, image=self.show_1_Image, bg='#191919')
            self.showCardImagelabel.place(x=0, y=0)

            self.showCardTitlelabel = Label(self.showCard, text=movies[i], width=22, font=("Netflix Sans", 16, "bold"), fg="white", bg='red', height=2)
            self.showCardTitlelabel.place(x=0, y=203)

            x += 400

        # Showing latest tv shows -

        x = 190

        for i in range(3):
            self.showCard = Frame(self.screen, width=300, height=265, bg="#191919", bd=4)
            self.showCard.place(x=x, y=550)

            self.showCardImagelabel = Label(self.showCard, image=self.show_1_Image, bg='#191919')
            self.showCardImagelabel.place(x=0, y=0)

            self.showCardTitlelabel = Label(self.showCard, text=tv_shows[i], width=22, font=("Netflix Sans", 16, "bold"), fg="white", bg='red', height=2)
            self.showCardTitlelabel.place(x=0, y=203)

            x += 400

    def validateEmail(self):
        email = self.email.get()

        if email:
            if re.search(self.patternEmail, email):
                self.signInScreen()
            else:
                messagebox.showwarning("Warning", "Invalid email!")
        else:
            messagebox.showwarning("Warning", "This field is required!")

    def login(self, event=None):
        email = self.signInEmail.get()
        password = self.signInPassword.get()

        if email:
            if password:
                if re.search(self.patternEmail, email):
                    if re.search(self.patternPassword, password):
                        self.userData = self.database.get(f"/{password}", None)

                        if self.userData is not None:
                            self.userDataValue = list(self.userData.values())[0]

                            if self.userDataValue.get("password") == password:
                                if messagebox.showinfo("Success", "You are now logged in!"):
                                    Thread(target=self.showRecommendations).start()
                                    # Thread(target=self.showCardsScreen).start()
                                    # self.showCardsScreen()
                            else:
                                messagebox.showwarning("Warning", "Incorrect password!")
                        else:
                            messagebox.showwarning("Warning", "User not found!")
                    else:
                        messagebox.showwarning("Warning", "Invalid password!")
                else:
                    messagebox.showwarning("Warning", "Invalid email!")
            else:
                messagebox.showwarning("Warning", "Password missing!")
        else:
            messagebox.showwarning("Warning", "Email missing!")

    def register(self, event=None):
        email = self.signUpEmail.get()
        password = self.signUpPassword.get()

        if email:
            if password:
                if re.search(self.patternEmail, email):
                    if re.search(self.patternPassword, password):

                        userData = {
                            'email': email,
                            'password': password
                        }

                        if self.database.post(f"/{password}", userData) is not None:
                            if messagebox.showinfo("Success", "You are now registered!"):
                                self.signInScreen()
                        else:
                            messagebox.showinfo("Failure", "Something wrong!")
                    else:
                        messagebox.showwarning("Warning", "Invalid password!")
                else:
                    messagebox.showwarning("Warning", "Invalid email!")
            else:
                messagebox.showwarning("Warning", "Password missing!")
        else:
            messagebox.showwarning("Warning", "Email missing!")

    def forgotPassword(self, event=None):
        email = self.needHelpEmail.get()

        if email:
            if re.search(self.patternEmail, email):
                if messagebox.showinfo("Success", "You can now log in again!"):
                    self.signInScreen()
            else:
                messagebox.showwarning("Warning", "Invalid email!")
        else:
            messagebox.showwarning("Warning", "Email missing!")

    def closeScreen(self):
        if messagebox.askyesnocancel("Close", "Do you want to close?"):
            self.screen.destroy()


if __name__ == '__main__':
    netflix = Netflix()
