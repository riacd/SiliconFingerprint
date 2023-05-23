# this is for communication between Server & UserEquipment
import Server.API
import UserEquipment.API
from multiprocessing import Process, Queue
import re
import json
from bch_fuzzy_extractor.fuzzyExtractor import FE
from bch_fuzzy_extractor.converting import converting
import numpy as np
import random



UE_id_list = [0, 1, 2, 3, 4, 5]
Server_id_list = [0, 1, 2, 3]

class UE_database:
    def __init__(self):
        self.data = {}

    def add(self, server_id, server_name, public_key):
        server = {'server_id': server_id, 'server_name': server_name, 'public_key': public_key}
        self.data[server_id] = server

    def delete(self, server_id):
        del self.data[server_id]

    def load(self):
        with open('UserEquipment/client_database.json') as f:
            self.data = json.load(f)

    def dump(self):
        with open('UserEquipment/client_database.json', 'w') as f:
            json.dump(self.data, f, indent=4)

class UEProcess(Process):
    def __init__(self, UE_id, Server_list, name=None):
        super(UEProcess, self).__init__()
        self.UE_id = UE_id
        self.Server_list = Server_list
        self.queue = Queue()
        if name is None:
            self.name = 'UE'+str(UE_id)
        else:
            self.name = name
        self.database = UE_database()
        self.Msglog = []

    def run(self):
        # UE process, use p.start() to run, p.join() to wait for process to finish
        pass

    def sendMsg(self, Server_id, msg):
        self.Server_list[Server_id].queue.put(msg)

    def logMsg(self, Sent: bool, Msg):
        if Sent:
            head = 'Send: '
        else:
            head = 'Get: '
        log = head + Msg
        self.Msglog.append(log)

    def register(self, Server_id):
        Msg = self.register_request(Server_id)
        self.sendMsg(Server_id, Msg)
        self.logMsg(True, Msg)


    def register_request(self, Server_id):
        tag = 'register_request '
        rawData = np.load("UserEquipment/UE_feature_rawData/feature_clf1.npy")
        row = Server_id*200 + random.randint(0, 199)
        theMedian = np.median(rawData)
        w = converting(rawData[row], theMedian)
        registerMsg = tag + str(self.UE_id) + ' ' + w
        return registerMsg


    def authentication_request(self, Server_id):
        tag = 'authentication_request'
        rawData = np.load("UserEquipment/UE_feature_rawData/feature_clf1.npy")
        row = Server_id*200 + random.randint(0, 199)
        theMedian = np.median(rawData)
        w = converting(rawData[row], theMedian)
        from_id = self.UE_id
        to_id = Server_id
        Nonce = random.randint(1, 10000)
        challenge = str(Nonce)+' '+str(from_id)
        public_key = self.database.data[Server_id]['public_key']

        # cipher = Cipher_pkcs1_v1_5.new(public_key)
        # cipher_text = base64.b64encode(cipher.encrypt(challenge.encode('utf-8')))
        #
        registerMsg = tag+' '+from_id+' '+to_id+' '+ ' ' + w

        self.sendMsg(Server_id, registerMsg)

    def get_respond(self):
        respond_msg = self.queue.get(block=True, timeout=2)


class Server_database:
    def __init__(self):
        self.data = {}
        self.load()

    def add(self, UE_id, s, x):
        UE = {'UE_id': UE_id, 's': s, 'x': x}
        self.data[UE_id] = UE

    def delete(self, server_id):
        del self.data[server_id]

    def load(self):
        with open('Server/server_database.json') as f:
            self.data = json.load(f)

    def dump(self):
        with open('Server/server_database.json', 'w') as f:
            json.dump(self.data, f, indent=4)


class ServerProcess(Process):
    def __init__(self, server_id, UE_list, name=None):
        super(ServerProcess, self).__init__()
        self.server_id = server_id
        self.queue = Queue()
        self.UE_list = UE_list
        self.FE = FE(511, 15)
        self.database = Server_database()
        self.Msglog = []
        if name is None:
            self.name = 'Server'+str(server_id)
        else:
            self.name = name

    def run(self):
        # server process, use p.start() to run
        while True:
            self.respond()

    def sendMsg(self, UE_id, msg):
        self.UE_list[UE_id].queue.put(msg)

    def logMsg(self, Sent: bool, Msg):
        if Sent:
            head = 'Send: '
        else:
            head = 'Get: '
        log = head + Msg
        self.Msglog.append(log)

    def register_respond(self, request_msg):
        tag = 'register_respond '
        UE_id, w1 = re.split('[0123456789]+', request_msg)
        R1, s, x = self.FE.generate(w1)
        self.database.add(UE_id, s, x)
        # rsa = RSA.generate(2048, R1)
        # # private_key = rsa.exportKey()
        # public_key = rsa.publicKey().exportKey()
        #
        # self.sendMsg(UE_id, tag+public_key)

    def authentication_respond(self, request_msg):
        tag = 'authentication_respond '

        # cipher = Cipher_pkcs1_v1_5.new(rsakey)
        # text = cipher.decrypt(base64.b64decode(encrypt_text), random_generator)

    def respond(self):
        request_msg = self.queue.get(block=True)
        self.logMsg(False, request_msg)
        if re.match('register_request', request_msg):
            print('Server: processing register_request')
            self.register_respond(request_msg)
        if re.match('authentication_request', request_msg):
            print('Server: processing authentication_request')
            self.authentication_respond(request_msg)



class ProcessManagement:
    def __init__(self):
        self.UE_list = {}
        self.Server_list = {}
        for i in UE_id_list:
            self.addUE(i)
        for i in Server_id_list:
            self.addServer(i)

    def addServer(self, server_id):
        process = ServerProcess(server_id, self.UE_list)
        self.Server_list[server_id] = process
        # process.start()

    def addUE(self, UE_id):
        process = UEProcess(UE_id, self.Server_list)
        self.UE_list[UE_id] = process
        # process.start()

    def send2Server(self, msg: str):
        self.Server_MsgBox.append(msg)

    def send2UE(self, msg: str):
        self.UE_MsgBox.append(msg)

    def clearServer(self):
        self.Server_MsgBox = []

    def clearUE(self):
        self.UE_MsgBox = []

print("create Manager object")
Manager = ProcessManagement()

class Protocol:
    def __init__(self):
        pass

    @staticmethod
    def register_request():
        pass

    @staticmethod
    def register_respond():
        pass

    @staticmethod
    def authentication_request():
        pass

    @staticmethod
    def authentication_respond():
        pass

