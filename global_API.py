# this is for communication between Server & UserEquipment
import Server.API
import UserEquipment.API
from multiprocessing import Process
import json
from bch_fuzzy_extractor.fuzzyExtractor import FE
from bch_fuzzy_extractor.converting import converting
import numpy as np
import random
import re
from threading import Thread
from queue import Queue
import queue
import base64
from Crypto.PublicKey import RSA
import Crypto.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5  # 用于签名/验签
from Crypto.Cipher import PKCS1_v1_5, PKCS1_OAEP  # 用于加密
from Crypto import Random
from Crypto.Hash import MD5


UE_id_list = [0, 1, 2, 3, 4, 5]
Server_id_list = [0, 1, 2, 3]

class challenge_respond:
    def __init__(self, R):
        self.private_key, self.public_key = self.keys_gen(R)

    def keys_gen(self, R):
        random_gen = random.Random()
        random_gen.seed(R)
        rsa = RSA.generate(2048, lambda n: random_gen.getrandbits(n * 8).to_bytes(n, 'little'))
        private_key = rsa.exportKey()
        public_key = rsa.publickey().export_key()
        return private_key, public_key



def padding(text):
    print('before padding', len(text))
    while len(text) %128 != 0:
        text += b' '
    return text


class UE_database:
    def __init__(self):
        self.data = {}

    def add(self, server_id, public_key):
        server = {'server_id': str(server_id), 'public_key': str(public_key)}
        self.data[server_id] = server

    def delete(self, server_id):
        del self.data[server_id]

    def load(self):
        with open('UserEquipment/client_database.json') as f:
            self.data = json.load(f)

    def dump(self):
        with open('UserEquipment/client_database.json', 'w') as f:
            json.dump(self.data, f, indent=4)

class UEProcess(Thread):
    def __init__(self, UE_id, Server_list, name=None):
        super(UEProcess, self).__init__()
        self.UE_id = UE_id
        self.Server_list = Server_list
        self.connection_list = []
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

    def warning(self, type: str, info: str):
        print('UE'+str(self.UE_id), ': ', type, '(', info, ')')

    def logMsg(self, Sent: bool, Msg):
        if Msg is None:
            return
        if Sent:
            head = 'Send: '
        else:
            head = 'Get: '
        log = head + Msg
        self.Msglog.append(log)

    def sendMsg(self, Server_id, msg):
        if msg == '':
            return
        self.Server_list[Server_id].queue.put(msg)
        self.logMsg(True, msg)

    def getMsg(self, block, timeout=None):
        request_msg = self.queue.get(block=block, timeout=timeout)
        self.logMsg(False, request_msg)
        return request_msg

    def build_connection(self, Server_id):
        self.connection_list.append(Server_id)

    def w_generator(self):
        rawData = np.load("UserEquipment/UE_feature_rawData/feature_clf1.npy")
        row = self.UE_id*200 + random.randint(0, 199)
        theMedian = np.median(rawData)
        w = converting(rawData[row], theMedian)
        return w

    def register_request(self, Server_id):
        tag = 'register_request'
        w = self.w_generator()
        registerMsg = tag+' '+str(self.UE_id) + ' ' + w
        return registerMsg


    def register(self, Server_id: int):
        Msg = self.register_request(Server_id)
        self.sendMsg(Server_id, Msg)

        try:
            respond_msg = self.getMsg(True, timeout=5)
        except queue.Empty:
            respond_msg = None
        if respond_msg:
            if re.match('register_respond', respond_msg):
                tag, public_key = re.split('\S+', respond_msg, maxsplit=1)
                self.database.add(Server_id, public_key)
            else:
                self.warning('register_failure', 'tag unmatch')
        else:
            self.warning('register_failure', 'time out')

    def call_register(self, Server_id):
        self.warning('starting register', 'to '+str(Server_id))
        t = Thread(target=self.register, args=[Server_id])
        t.start()

    def authentication_request(self, Server_id, Nonce):
        tag = 'authentication_request'
        w = self.w_generator()
        from_id = self.UE_id
        to_id = Server_id
        challenge = str(Nonce)+' '+str(from_id)
        public_key = RSA.import_key(eval(self.database.data[Server_id]['public_key']))
        cipher = PKCS1_OAEP.new(public_key)
        cipher_text = base64.b64encode(cipher.encrypt(challenge.encode('utf-8')))
        Msg = tag+' '+str(from_id)+' '+str(to_id)+' '+str(cipher_text)+' ' + w

        return Msg

    def authentication(self, Server_id: int):
        if Server_id not in self.database.data.keys():
            self.warning('authentication failure', 'has not registered to Server')
            return

        Nonce = random.randint(1, 10000)
        Msg = self.authentication_request(Server_id, Nonce)
        self.sendMsg(Server_id, Msg)

        try:
            respond_msg = self.getMsg(True, timeout=5)
        except queue.Empty:
            respond_msg = None
        if respond_msg:
            if re.match('authentication_respond', respond_msg):
                tag, Server_id_, signature = re.split('\S+', respond_msg, 2)
                public_key = RSA.import_key(eval(self.database.data[Server_id]['public_key']))
                signature = eval(signature)
                ch_respond = str(Nonce+1) + ' ' + str(self.UE_id)
                digest = MD5.new(ch_respond.encode('utf-8'))
                if sign_PKCS1_v1_5.new(public_key).verify(digest, signature):
                    self.build_connection(Server_id)
                else:
                    self.warning('authentication_failure', 'challenge-respond failure')
            else:
                self.warning('authentication_failure', 'tag unmatch')
        else:
            self.warning('authentication_failure', 'time out')


    def call_authentication(self, Server_id: int):
        self.warning('starting authentication', 'to Server'+str(Server_id))
        t = Thread(target=self.authentication, args=[Server_id])
        t.start()


    def get_respond(self):
        respond_msg = self.queue.get(block=True, timeout=2)
        return respond_msg


class Server_database:
    def __init__(self):
        self.data = {}
        self.load()

    def add(self, UE_id, s, x):
        # print('UE_id', type(UE_id), UE_id)
        # print('s', type(s), s)
        # print('x', type(x), x)

        UE = {'UE_id': str(UE_id), 's': str(s), 'x': str(x)}
        self.data[UE_id] = UE

    def delete(self, server_id):
        del self.data[server_id]

    def load(self):
        with open('Server/server_database.json') as f:
            self.data = json.load(f)

    def dump(self):
        with open('Server/server_database.json', 'w') as f:
            json.dump(self.data, f, indent=4)


class ServerProcess(Thread):
    def __init__(self, server_id, UE_list, name=None):
        super(ServerProcess, self).__init__()
        self.server_id = server_id
        self.queue = Queue()
        self.UE_list = UE_list
        self.FE = FE(511, 200)
        self.database = Server_database()
        self.connection_list = []
        self.Msglog = []
        if name is None:
            self.name = 'Server'+str(server_id)
        else:
            self.name = name

    def run(self):
        # server process, use p.start() to run
        self.warning('initializing', 'thread start')
        while True:
            self.respond()

    def warning(self, type: str, info: str):
        print('Server'+str(self.server_id), ': ', type, '(', info, ')')


    def logMsg(self, Sent: bool, Msg):
        if Sent:
            head = 'Send: '
        else:
            head = 'Get: '
        log = head + Msg
        self.Msglog.append(log)

    def sendMsg(self, UE_id, msg):
        self.UE_list[UE_id].queue.put(msg)
        self.logMsg(True, msg)

    def getMsg(self, block, timeout=None):
        request_msg = self.queue.get(block=block, timeout=timeout)
        self.logMsg(False, request_msg)
        return request_msg

    def build_connection(self, UE_id):
        self.connection_list.append(UE_id)


    def register_respond(self, request_msg):
        tag = 'register_respond'
        register_tag, UE_id_str, w1 = re.split('\W+', request_msg)
        UE_id = int(UE_id_str)
        R1, s, x = self.FE.generate(w1)
        # self.warning('R1', str(R1))
        R1_sum = R1.sum()
        R1_sum = R1_sum.item()
        self.warning('R1_sum', str(R1_sum))
        self.database.add(UE_id, s, x)
        random_gen = random.Random()
        random_gen.seed(R1_sum)
        rsa = RSA.generate(2048, lambda n: random_gen.getrandbits(n * 8).to_bytes(n, 'little'))
        private_key = rsa.exportKey()
        public_key = rsa.publickey().export_key()
        print('1', public_key)
        self.sendMsg(UE_id, tag+' '+str(public_key))

    def authentication_respond(self, request_msg):
        tag = 'authentication_respond'
        get_tag, UE_id_str, Server_id_str, cipher_text, w2 = re.split('\s+', request_msg, maxsplit=5)
        UE_id = int(UE_id_str)
        cipher_text = eval(cipher_text)
        s = eval(self.database.data[UE_id]['s'])
        x = eval(self.database.data[UE_id]['x'])
        R2 = self.FE.reproduce(w2, s, x)
        # self.warning('R2', str(R2))
        R2_sum = R2.sum()
        R2_sum = R2_sum.item()
        self.warning('R2_sum', str(R2_sum))
        random_gen = random.Random()
        random_gen.seed(R2_sum)
        rsa = RSA.generate(2048, lambda n: random_gen.getrandbits(n * 8).to_bytes(n, 'little'))
        private_key = rsa.exportKey()
        public_key = rsa.publickey().export_key()
        private_key = RSA.import_key(private_key)
        print('2', public_key)
        cipher = PKCS1_OAEP.new(private_key)
        try:
            challenge = cipher.decrypt(base64.b64decode(cipher_text)).decode('utf-8')
        except ValueError:
            self.warning('authentication failure', 'from UE'+UE_id_str)
            return
        self.warning('decrypted challenge', challenge)
        # 对挑战进行应答
        print(re.findall('\d+', challenge))
        Nounce, from_id = re.findall('\d+', challenge)
        print('nounce', Nounce)
        print('id', from_id)
        Nounce = int(Nounce)+1
        ch_respond = str(Nounce)+' '+str(from_id)
        digest = MD5.new(ch_respond.encode('utf-8'))
        signature = sign_PKCS1_v1_5.new(private_key).sign(digest)
        Msg = tag+' '+str(self.server_id)+' '+str(signature)
        self.sendMsg(UE_id, Msg)
        self.build_connection(UE_id)







        # cipher = Cipher_pkcs1_v1_5.new(rsakey)
        # text = cipher.decrypt(base64.b64decode(encrypt_text), random_generator)

    def respond(self):
        request_msg = self.getMsg(True)
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
        process.start()

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

