# CSC4350Assignment-8
Short description of the project and the implemented methods

This project simulates reliable transport over UDP. The reliability comes in by adding in a protocol header
that has the following:
1-byte protocol identifier 
1-byte length (header length + payload length)
2-byte destination port (this should be the same as what was used to send the UDP packet)
2-byte random number
1-byte SND/ACK/NACK field
1-byte Sequence Number
2-byte checksum

these are all sent before the message and the checksum is calculated by XORing all of the header fields
and the first two bytes of the data being sent.

The client will first split the message up into parts no longer than 8 bytes. these chunks of the message will then be sent in the correct order
using sequence number 0 or 1 and will alternate between the two. The Server will recieve the header along with the message and will then
compute its own checksum and ensure that the packet was recieved correctly. If the packet was not recieved correctly, the server will send back a header
with a nack in the SND/ACK/NACK field and the client will retransmit the illrecieved packet. If the packet is recieved correctly, the server will send
back a header with an ack in the SND/ACK/NACK field. Upon recieveing the ack the client will switch to the other sequence number and move onto 
the next packet to be sent. This process will continue untill all packets are sent. In order to simulate errors, a method was added to intentionally
corrupt ~1 in every 10 packets

Instructions for executing the program, including command-line flag options

I opened up an IDLE environment for the server and the client respectivly and ran the server first and then the client.

Server side commandline: 
  the -p will allow the user to input a port number for the server to open a connection on
  the -h will provide a help statement to the user
Client side commandline:
  the -p will allow the user to input a port number for the client to connect to
  the -i will allow the user to input the name of the server (127.0.0.1)
  the -m will allow the user to input the message they would like to send to the server (no spaces)
  
 Notes. Include:
  - Any requirements not fully implemented or functioning as expected
  
  not quite sure how to accurately get the length of the segment in bytes (maybe just misunderstanding directions)
  
  - Areas of your code you feel are not optimal and need to be improved or refactored
  
  should probably add something to not print the last padded on 0 in the case of a message segment being less than 2 bytes long
  should change the code to allow for spaces in the message (this was causing split issues which is why i state to not put spaces in the message)
  The connection currently gets killed on the client side without the server knowing anything; should add something to disconnect more gracefully
