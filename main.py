from iqoptionapi.stable_api import IQ_Option
import PySimpleGUI as sg
from datetime import datetime
import time, threading

global contador

class TelaLogin:
    def __init__(self):
        layout = [
                  [sg.Text('Login'), sg.Input()],      
                  [sg.Text('Senha'), sg.Input(password_char = "*")],      
                  [sg.Submit("logar")]
                 ] 

        window = sg.Window("iqOption Bot").layout(layout)
        self.window = window
        self.button, self.values = window.Read()

        while self.values[0] == "" or self.values[1] == "":
            layout = [
                      [sg.Text('COLOCA O LOGIN E A SENHA ANIMAL')],
                      [sg.Text('Login'), sg.Input()],      
                      [sg.Text('Senha'), sg.Input(password_char = "*")],      
                      [sg.Submit("logar")]
                     ]
            window = sg.Window("iqOption Bot").layout(layout)
            self.window = window
            self.button, self.values = window.Read()


class Tela:
    def __init__(self):
        symbols = ["EURUSD", "EURJPY", "EURNZD", "EURAUD", "USDJPY", "AUDUSD", "AUDJPY", "NZDUSD", "EURUSD-OTC"]
        tempo = ["1 min", "5 min", "15 min"]
        opt = ["call", "put"]
        layout = [
                  [sg.Text('Valor'), sg.Input("5", key = "value-input")],
                  [sg.Checkbox('Definir horário?', key = "hour"), sg.Input("example: 01:23, 02:00, 14:30, 23:01", key = "hour-input")],
                  [sg.Checkbox('Conta Real', key = "account")],
                  [sg.OptionMenu(values = symbols, key = "symbol"), sg.OptionMenu(values = tempo, key = "time"), sg.OptionMenu(values = opt, key = "opt")],
                  [sg.Output(size = (60,5), echo_stdout_stderr = True)],
                  [sg.Submit("Operar")]
                 ] 

        window = sg.Window("iqOption Bot").layout(layout)
        self.window = window
        self.button, self.values = window.Read()

def Buy(quantity, symbol, opt, expireTime):
    check, id = api.buy(quantity, symbol, opt, expireTime)
    if check:
        print("Lucro/preju: %.2f" % api.check_win_v3(id))
        return
    else:
        print("Operação falhou :(")
        return

telaLogin = TelaLogin()
#api = IQ_Option(str(telaLogin.values[0]), str(telaLogin.values[1]))
api = IQ_Option("alexandrealen03@gmail.com","alexandrealen03@gmail.com")
api.connect()
telaLogin.window.close()

while api.check_connect() == False:
    layout = [
        [sg.Text('Login falhou, verifique se colocou o email/senha corretos')],
        [sg.Text('Login'), sg.Input()],      
        [sg.Text('Senha'), sg.Input(password_char = "*")],      
        [sg.Submit("logar")]
    ]
    telaLogin.window = sg.Window("iqOption Bot").layout(layout)
    telaLogin.button, telaLogin.values = telaLogin.window.Read()
    api = IQ_Option(str(telaLogin.values[0]), str(telaLogin.values[1]))
    api.connect()
    telaLogin.window.close()

tela = Tela()

if tela.values["account"]:
    conta = "REAL"
else:
    conta = "PRACTICE"
api.change_balance(conta)

if tela.values["time"] == "1 min":
    tela.values["time"] = 1
elif tela.values["time"] == "5 min":
    tela.values["time"] = 5
else:
    tela.values["time"] = 15  

contador = 0  
    

if tela.values["hour"]:
    print("Horário definido para " + str(tela.values["hour-input"]))
    value = float(tela.values["value-input"])
    symbol = tela.values["symbol"]
    opt = tela.values["opt"]
    expireTime = tela.values["time"]
    while True:
        if str(tela.values["hour-input"]) == str(datetime.now().strftime("%H:%M")) and contador == 0:
            print("Deu o horário menó, iniciando a operação")
            contador = 1
            threading.Thread(target = Buy, args = (value, symbol, opt, expireTime, )).start()
            tela.window.Read()
        else:
            time.sleep(0.9)