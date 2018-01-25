from tkinter import *
import requests
import hashlib
import json
import time
from gamescene import GameScene
from loginscene import LoginScene
from startscene import StartScene

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_MIN_WIDTH = 600
SCREEN_MIN_HEIGHT = 600


class GoClient():
    server, port = '127.0.0.1', '61366'

    def __init__(self):
        self.server_url = 'http://' + self.server + ':' + self.port + '/'
        self.token = False
        self.master = Tk()
        self.master.geometry('{}x{}'.format(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.master.minsize(SCREEN_MIN_WIDTH, SCREEN_MIN_HEIGHT)
        # self.scene = StartScene(self)
        self.scene = LoginScene(self)
        # self.scene = GameScene(self)

    def __change_scene(self, SceneClass):
        self.scene.destroy()
        self.scene = SceneClass(self)

    def __on_credentials_response(self, response):
        print(response)
        if (response['success']):
            self.token = response['token']
            self.__change_scene(StartScene)

    def __on_game_start_response(self, response):
        print(response)
        if (response['success']):
            self.id_game = response['id_game']
            self.__change_scene(GameScene)

    def register(self, login, password):
        r = requests.post(self.server_url + 'register', json={'login': login, 'password': hashlib.sha1(password.encode('utf-8')).hexdigest()})
        response = json.loads(r.text)
        self.__on_credentials_response(response)

    def login(self, login, password):
        r = requests.post(self.server_url + 'login', json={'login': login, 'password': hashlib.sha1(password.encode('utf-8')).hexdigest()})
        response = json.loads(r.text)
        self.__on_credentials_response(response)

    def logout(self):
        requests.post(self.server_url + 'logout', json={'token': self.token})
        self.__change_scene(LoginScene)

    def new_game(self, field_size):
        print("new_game", field_size)
        r = requests.post(self.server_url + 'newgame', json={'token': self.token, 'field_size': field_size})
        response = json.loads(r.text)
        self.__on_game_start_response(response)

    def join_invite(self, invite):
        print("join_invite", invite)
        r = requests.post(self.server_url + 'joininvite', json={'token': self.token, 'invite': invite})
        response = json.loads(r.text)
        self.__on_game_start_response(response)

    def get_active_games(self):
        print("get_active_games")
        r = requests.post(self.server_url + 'activegames', json={'token': self.token})
        response = json.loads(r.text)
        if response['success']:
            return response['games']
        return []

    def join_game(self, id_game):
        print('join_game', id_game)
        self.id_game = id_game
        self.__change_scene(GameScene)

    def get_game_data(self):
        r = requests.post(self.server_url + 'gamedata', json={'token': self.token, 'id_game': self.id_game})
        response = json.loads(r.text)
        if response['success']:
            self.last_update = response['timestamp']
            return response['game_data']
        self.__change_scene(StartScene)

    def put_stone(self, x, y):
        r = requests.post(self.server_url + 'putstone',
                          json={'token': self.token, 'id_game': self.id_game, 'x': x, 'y': y})
        response = json.loads(r.text)
        return response['success']

    def get_game_update(self, callback, context):
        try:
            print(time.time(), "--requests--")
            r = requests.post(self.server_url + 'gameupdate',
                              json={'token': self.token, 'id_game': self.id_game, 'last_update': self.last_update},
                              timeout=10)
            response = json.loads(r.text)
        except:
            response = {'success': False}
        if response['success']:
            self.last_update = response['timestamp']
            callback(response['events'])

    def skip_turn(self):
        r = requests.post(self.server_url + 'pass',
                          json={'token': self.token, 'id_game': self.id_game})


def main():
    GoClient()
    mainloop()


if __name__ == '__main__':
    main()
