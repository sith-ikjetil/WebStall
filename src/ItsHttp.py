import socket
import httplib2

class ItsHttp():
    def CreateHttpSocket(self):
        return socket.socket()
    
    def ConnectHttpSocket(self, sock, address):
        return sock.connect((address.encode('ascii'),80))
    
    def SendHttpSocket(self, sock, payload):
        return sock.send(payload.encode('ascii'))

    def ReceiveHttpSocket(self, sock, count):
        return sock.recv(count)

    def CloseHttpSocket(self, sock):
        return sock.close()

    def ExecuteHttpGet(self, url):
        h = httplib2.Http()
        (content,response) = h.request(url)
        return (content,response)

