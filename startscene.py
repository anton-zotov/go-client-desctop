from tkinter import *
from scene import Scene


class StartScene(Scene):
    def __init__(self, client):
        super(StartScene, self).__init__(client.master)
        self.client = client
        self.invite = StringVar()
        font = "Helvetica 20"

        self.new_game_button = Button(self.frame, text="New game", command=self.new_game,
                                      background="#2196F3", activebackground="#1976D2",
                                      foreground="#FFF", activeforeground="#FFF")
        self.logout_button = Button(self.frame, text="Logout", command=self.client.logout)
        self.invite_label = Label(self.frame, text="Invite code: ", font=font)
        self.invite_entry = Entry(self.frame, textvariable=self.invite, font=font, justify="center")
        self.join_invite_button = Button(self.frame, text="Join invite", command=self.join_invite,
                                         background="#2196F3", activebackground="#1976D2",
                                         foreground="#FFF", activeforeground="#FFF")
        self.active_games_list = Listbox(self.frame)
        self.join_game_button = Button(self.frame, text="Join game", command=self.join_game,
                                       background="#2196F3", activebackground="#1976D2",
                                       foreground="#FFF", activeforeground="#FFF")

        self.update_active_games()
        self.frame.bind("<Configure>", self.configure)
        self.configure(None)

    def new_game(self):
        self.client.new_game(9)

    def join_invite(self):
        if self.invite.get():
            self.client.join_invite(self.invite.get())

    def join_game(self):
        if self.active_games_list.curselection():
            sel_n = self.active_games_list.curselection()[0]
            self.client.join_game(self.active_games[sel_n]['id'])

    def update_active_games(self):
        self.active_games = self.client.get_active_games()
        self.active_games_list.delete(0, END)
        for game in self.active_games:
            self.active_games_list.insert(END, "  " + str(game['name']))

    def configure(self, event):
        width = self.frame.winfo_width()
        height = self.frame.winfo_height()
        self.logout_button.place(x=width - 110, y=10, width=100, height=36)
        self.new_game_button.place(x=width / 4, y=100, width=width / 4 - 10, height=36)
        self.invite_label.place(x=width / 3 - 200, y=160, width=200, height=36)
        self.invite_entry.place(x=width / 3, y=160, width=width / 3, height=36)
        self.join_invite_button.place(x=width * 2 / 3 + 10, y=160, width=width / 3 - 30, height=36)
        self.active_games_list.place(x=20, y=220, width=width / 2 - 40, height=height - 286)
        self.join_game_button.place(x=20, y=height - 56, width=width / 2 - 40, height=36)
