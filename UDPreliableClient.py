#Connor Short
#client to send reliable UDP
#ADD CASE FOR IF THE CHUNK BEING SENT IS ONLY 1 LONG (CHECKSUM PURPOSES)


from socket import *
from optparse import OptionParser
import sys
import random
import math

#options for command line parameters, do a -h to get the help statements to appear
parser = OptionParser()
parser.add_option("-p",
                  action = "store", type="int", dest="serverPort", default = 8000,
                  help = "choose port for connection, must be same as on server")
parser.add_option("-i",
                  action = "store", type="str", dest="serverName", default = '127.0.0.1',
                  help = "choose address for connection, ex. 127.0.0.1")
parser.add_option("-m",
                  action = "store", type="str", dest="message", default = "helloworldhowareyoudoingtodayinthisfineworldweliveinkkkkk",
                  help = "Enter the message you wish to send")

(options, args) = parser.parse_args()


clientSocket = socket(AF_INET, SOCK_DGRAM)

numberOfPackets = math.ceil(len(options.message)/8)

#splitting the message into 8 character chunks that are stored in a list and number of chunks is number of packets to be sent
n = 8
chunks = [options.message[i:i+n] for i in range(0, len(options.message), n)]
print(chunks)

#setting some of the header values
protocol = 'u'
flag = 's'
seqNum = 0
randomNumber = random.randint(0,65535)

wholeSegment = protocol + ' ' + str(options.serverPort) + ' ' + str(randomNumber) + ' ' + flag + ' ' + str(0)
length = sys.getsizeof(chunks[0]) + sys.getsizeof(wholeSegment) - 49 - 49 - 4 #subtracting 49 twice because they are both strings and 3 because of whitespace

#calculating the checksum by XORing all items in header
if (len(chunks[0]) < 2):
    chunks[0] = chunks[0] + '0'
checkSum = ord(protocol) ^ int(length) ^ int(options.serverPort) ^ int(randomNumber) ^ ord(flag) ^ int(seqNum) ^ (ord(chunks[0][0]) + ord(chunks[0][1]))

#creating whole segment to be sent
wholeSegment = protocol + ' ' + str(length) + ' ' + str(options.serverPort) + ' ' + str(randomNumber) + ' ' + flag + ' ' + str(seqNum) + ' ' + str(checkSum) + ' ' + chunks[0]

print (wholeSegment)
print (numberOfPackets)
clientSocket.sendto(wholeSegment.encode(), (options.serverName, options.serverPort))

counter = 1 #counter at 1 because 1 packet has already been sent

while counter != numberOfPackets:
    #recieving the response from server and splitting items
    message, serverAddress = clientSocket.recvfrom(2048)
    message = message.decode()
    print (message)
    protocol, length, destPort, randomNumber, flag, serverSeqNum, checkSum = message.split()

    #if a nack is recieved the previous segment gets resent
    if (flag == 'n'):
        wholeSegment = protocol + ' ' + str(length) + ' ' + str(options.serverPort) + ' ' + str(randomNumber) + ' ' + 's' + ' ' + str(seqNum) + ' ' + str(checkSum) + ' ' + chunks[counter-1]
        clientSocket.sendto(wholeSegment.encode(), (options.serverName, options.serverPort))
    #two separate if cases to flip between 0 and 1 sequence numbers
    if (int(serverSeqNum) == 1 and flag == 'a'):
        #setting header values
        seqNum = 0
        randomNumber = random.randint(0,65535)
        wholeSegment = protocol + ' ' + str(options.serverPort) + ' ' + str(randomNumber) + ' ' + 's' + ' ' + str(0)
        #calculating a random number to send bad packets
        badPacket = random.randint(1,5)
        length = sys.getsizeof(chunks[counter]) + sys.getsizeof(wholeSegment) - 49 - 49 - 4
        #calculating the checksum and adding a case to pad on a 0 if data is less than 2 in length
        if (len(chunks[counter]) < 2):
            chunks[counter] = chunks[counter] + '0'
        checkSum = ord(protocol) ^ int(length) ^ int(options.serverPort) ^ int(randomNumber) ^ ord('s') ^ int(seqNum) ^ (ord(chunks[counter][0]) + ord(chunks[counter][1]))
        #creating the whole segment to be sent
        wholeSegment = protocol + ' ' + str(length) + ' ' + str(options.serverPort) + ' ' + str(randomNumber) + ' ' + 's' + ' ' + str(seqNum) + ' ' + str(checkSum) + ' ' + chunks[counter]
        if (badPacket == 2):
            wholeSegment = protocol + ' ' + str(length) + ' ' + str(options.serverPort) + ' ' + str(randomNumber) + ' ' + 'z' + ' ' + str(seqNum) + ' ' + str(checkSum) + ' ' + chunks[counter]
        clientSocket.sendto(wholeSegment.encode(), (options.serverName, options.serverPort))
        #incrementing the counter indicating that a new packet has been sent
        counter = counter + 1
    if (int(serverSeqNum) == 0 and flag == 'a'):
        #setting header values
        seqNum = 1
        randomNumber = random.randint(0,65535)
        wholeSegment == protocol + ' ' + str(options.serverPort) + ' ' + str(randomNumber) + ' ' + 's' + ' ' + str(0)
        #calculating a random number to send bad packets
        badPacket = random.randint(1,5)
        length = sys.getsizeof(chunks[counter]) + sys.getsizeof(wholeSegment) - 49 - 49 - 4
        #calculating checksum and adding a case to pad on a 0 if data is less than 2 in length
        if (len(chunks[counter]) < 2):
            chunks[counter] = chunks[counter] + '0'
        checkSum = ord(protocol) ^ int(length) ^ int(options.serverPort) ^ int(randomNumber) ^ ord('s') ^ int(seqNum) ^ (ord(chunks[counter][0]) + ord(chunks[counter][1]))
        #creating whole segment to be sent
        wholeSegment = protocol + ' ' + str(length) + ' ' + str(options.serverPort) + ' ' + str(randomNumber) + ' ' + 's' + ' ' + str(seqNum) + ' ' + str(checkSum) + ' ' + chunks[counter]
        if (badPacket == 2):
             wholeSegment = protocol + ' ' + str(length) + ' ' + str(options.serverPort) + ' ' + str(randomNumber) + ' ' + 'z' + ' ' + str(seqNum) + ' ' + str(checkSum) + ' ' + chunks[counter]
        clientSocket.sendto(wholeSegment.encode(), (options.serverName, options.serverPort))
        #incrementing the counter indicating that a new packet has been sent
        counter = counter + 1
clientSocket.close()
        
        
