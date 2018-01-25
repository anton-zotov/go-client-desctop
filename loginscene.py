from tkinter import *
from scene import Scene


class LoginScene(Scene):
    def __init__(self, client):
        super(LoginScene, self).__init__(client.master)
        self.client = client
        self.login = StringVar()
        self.login.set("test")
        self.password = StringVar()
        self.password.set("test")
        font = "Helvetica 20"

        self.login_label = Label(self.frame, text="Login: ", font=font)
        self.login_entry = Entry(self.frame, textvariable=self.login, font=font, justify="center")
        self.password_label = Label(self.frame, text="Password: ", font=font)
        self.password_entry = Entry(self.frame, textvariable=self.password, font=font, justify="center", show="*")
        self.register_button = Button(self.frame, text="Register", command=self.do_register)
        self.login_button = Button(self.frame, text="Login", command=self.do_login,
                                   background="#2196F3", activebackground="#1976D2",
                                   foreground="#FFF", activeforeground="#FFF")

        self.frame.bind("<Configure>", self.configure)
        self.configure(None)

    def do_register(self):
        self.client.register(self.login.get(), self.password.get())

    def do_login(self):
        self.client.login(self.login.get(), self.password.get())

    def configure(self, event):
        width = self.frame.winfo_width()
        height = self.frame.winfo_height()
        self.login_label.place(x=width / 4 - 150, y=height / 2 - 100, width=150, height=36)
        self.login_entry.place(x=width / 4, y=height / 2 - 100, width=width / 2, height=36)
        self.password_label.place(x=width / 4 - 150, y=height / 2 - 40, width=150, height=36)
        self.password_entry.place(x=width / 4, y=height / 2 - 40, width=width / 2, height=36)
        self.register_button.place(x=width / 4, y=height / 2 + 10, width=width / 4 - 10, height=36)
        self.login_button.place(x=width / 2 + 10, y=height / 2 + 10, width=width / 4 - 10, height=36)
