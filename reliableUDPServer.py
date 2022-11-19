#Connor Short
#server to recieve reliable UDP messages
#using python3 as well as some libraries
#importing socket for the UDP connections
#importing optparse for the commandline parameters
#for execution i opened an idle and ran the file prior to running the client

from socket import *
import socket
from optparse import OptionParser
import random

#options for command line parameters, use -h to get the help statements to show up
parser = OptionParser()
parser.add_option("-p",
                  action = "store", type="int", dest="serverPort", default = 99999,
                  help = "choose port for connection, must be same as on client")

(options, args) = parser.parse_args()

if options.serverPort == 99999:
    print ("please be sure to use the commandline parameters provided")
    print ("Use the -p serverPort command to set the port for the server (where serverPort is the port number)")
    exit()

if options.serverPort < 0 or options.serverPort > 65535:
    print ("You have entered an invalid port number")

serverSocket = socket.socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',options.serverPort))
print ("The server is ready to recieve")

wholeMessage = ''

while True: #while loop to keep the server open and redy to recieve
    message, clientAddress = serverSocket.recvfrom(2048) #recieving the message and the address from the client
    message = message.decode()
    protocol, length, destPort, randomNumber, flag, recSeqNum, checkSum, data = message.split()
    if data not in wholeMessage:
        wholeMessage = wholeMessage + data
    
    #check to ensure that multiple acks are not sent back
    checkBit = 0

    #recalculating checksum
    computedCheckSum = ord(protocol) ^ int(length) ^ int(destPort) ^ int(randomNumber) ^ ord(flag) ^ int(recSeqNum) ^ (ord(data[0]) + ord(data[1]))

    while int(computedCheckSum) != int(checkSum) and protocol == 'u':
        #creating the nack response to send back indicating a bad packet was recieved
        wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'n' + ' ' + recSeqNum + ' ' + checkSum
        serverSocket.sendto(wholeSegment.encode(), clientAddress)

        #this recieves the new packet
        message, clientAddress = serverSocket.recvfrom(2048)
        message = message.decode()
        protocol, length, destPort, randomNumber, flag, recSeqNum, checkSum, data = message.split()
        if data not in wholeMessage:
            wholeMessage = wholeMessage + data

        #recalculating the checksum
        computedCheckSum = ord(protocol) ^ int(length) ^ int(destPort) ^ int(randomNumber) ^ ord(flag) ^ int(recSeqNum) ^ (ord(data[0]) + ord(data[1]))

        #if case to send back an ack
        if int(computedCheckSum) == int(checkSum) and protocol == 'u':
            #if segment is not corrupt, print data
            #print (data, end = '')
            checkBit = 1
            badPacket = random.randint(1,10)
            print(badPacket)
            #two separate if cases to flip between sequence numbers 0 and 1
            if (int(recSeqNum) == 1 and badPacket != 5):
                wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'a' + ' ' + recSeqNum + ' ' + checkSum
                serverSocket.sendto(wholeSegment.encode(), clientAddress)
                
            if (int(recSeqNum) == 0 and badPacket != 5):
                wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'a' + ' ' + recSeqNum + ' ' + checkSum
                serverSocket.sendto(wholeSegment.encode(), clientAddress)
    
    if (int(computedCheckSum) == int(checkSum) and checkBit != 1) and protocol == 'u':
        #if segment is not corrupt, print data
        #print (data, end = '')
        badPacket = random.randint(1,10)
        print(badPacket)
        #two separate if cases to flip between sequence numbers 0 and 1
        if (int(recSeqNum) == 1 and badPacket != 5):
            wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'a' + ' ' + recSeqNum + ' ' + checkSum
            serverSocket.sendto(wholeSegment.encode(), clientAddress)
            
        if (int(recSeqNum) == 0 and badPacket != 5):
            wholeSegment = protocol + ' ' + length + ' ' + destPort + ' ' + randomNumber + ' ' + 'a' + ' ' + recSeqNum + ' ' + checkSum
            serverSocket.sendto(wholeSegment.encode(), clientAddress)
    print (wholeMessage)
