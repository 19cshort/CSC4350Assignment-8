#Connor Short
#server to listen on port 8000 and handle various requests sent by a client

from socket import *
import socket
from optparse import OptionParser

#options for command line parameters, use -h to get the help statements to show up
parser = OptionParser()
parser.add_option("-p",
                  action = "store", type="int", dest="serverPort", default = 8000,
                  help = "choose port for connection, must be same as on client")

(options, args) = parser.parse_args()

serverSocket = socket.socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',options.serverPort))
print ("The server is ready to recieve")

while True: #while loop to keep the server open and redy to recieve
    message, clientAddress = serverSocket.recvfrom(2048) #recieving the message and the address from the client
    message = message.decode()
    #print (message)
    protocol, length, destPort, randomNumber, flag, seqNum, checkSum, data = message.split()
    checkBit = 0

    #recalculating checksum
    computedCheckSum = ord(protocol) ^ int(length) ^ int(destPort) ^ int(randomNumber) ^ ord(flag) ^ int(seqNum) ^ (ord(data[0]) + ord(data[1]))
    #print (str(computedCheckSum))
    #if int(computedCheckSum) != int(checkSum):
    while int(computedCheckSum) != int(checkSum):
        print ("")
        wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'n' + ' ' + seqNum + ' ' + checkSum
        serverSocket.sendto(wholeSegment.encode(), clientAddress)
        message, clientAddress = serverSocket.recvfrom(2048)
        message = message.decode()
        protocol, length, destPort, randomNumber, flag, seqNum, checkSum, data = message.split()
        computedCheckSum = ord(protocol) ^ int(length) ^ int(destPort) ^ int(randomNumber) ^ ord(flag) ^ int(seqNum) ^ (ord(data[0]) + ord(data[1]))
        if int(computedCheckSum) == int(checkSum):
            #if segment is not corrupt, print data
            print (data, end = '')
            checkBit = 1
            #two separate if cases to flip between sequence numbers 0 and 1
            if int(seqNum) == 1:
                wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'a' + ' ' + seqNum + ' ' + checkSum
                serverSocket.sendto(wholeSegment.encode(), clientAddress)
            if int(seqNum) == 0:
                wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'a' + ' ' + seqNum + ' ' + checkSum
                serverSocket.sendto(wholeSegment.encode(), clientAddress)
    if (int(computedCheckSum) == int(checkSum) and checkBit != 1):
        #if segment is not corrupt, print data
        print (data, end = '')
        #two separate if cases to flip between sequence numbers 0 and 1
        if int(seqNum) == 1:
            wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'a' + ' ' + seqNum + ' ' + checkSum
            serverSocket.sendto(wholeSegment.encode(), clientAddress)
        if int(seqNum) == 0:
            wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'a' + ' ' + seqNum + ' ' + checkSum
            serverSocket.sendto(wholeSegment.encode(), clientAddress)
