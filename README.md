Franklin Ace 1000/1200 Tools
============================

The Franklin Ace series predates the Apple Super Serial Card, so it includes its own implementation of a serial card: the Franklin Dual Interface Card. It's based on the 2661 UART. This UART is pretty mediocre, only supporting up to 19.2k and having a weird alternating register scheme in order to save 1 address pin.

The firmware on the card is totally bonkers. When activating it as an input (IN#2) the firmware forwards characters directly, with the high bit unset, which prevents bootstrapping ADT and makes the characters flash on screen. The built in mini-terminal correctly sets the bit, but is useless for bootstrapping.

Repository contents
===================

- franklin_term.py - Simple program to echo keyboard commands to the Ace.
- franklin_bootstrap.py - Like terminal, but reads a file and echoes it over the serial port instead.
- franklin_binary.py - Transfers a binary program into memory, such as ADT.
- hacked_adt/ - A hacked copy of the original DOS ADT client.

Cable
=====
If you do not have a null-modem cable (or your Dual Interface Card does not have a cable), these are the connections that must be made:

| 9-pin serial pin # | Dual Interface Card pin # |
| :---------------:  | :----------------------:  |
|         2 (RX)   | 2 (TX) |
|         3 (TX)   | 3 (RX) |
|         5 (GND)  | 7 (GND) |


Configuring the serial card
===========================
The following examples assume the Ace Dual Interface card is pysically inserted into Slot 1, with the serial card functions "ghosted" to slot 2. See Franklin Dual Interface Reference Manual for more details.


Switch block S1 tells the Dual Interface Card firmware where the "virtual" serial slot should be. For some bizarre reason, Franklin numbered the switch and PCB differently. The PCB numbers are correct. Set these to:

| Switch | Position | Function |
| :----: | :------: | :------: |
| 1 | OFF | slot 7 |
| 2 | OFF | slot 6 | 
| 3 | OFF | slot 5 |
| 4 | OFF | slot 4 |
| 5 | OFF | slot 3 |
| 6 | ON  | slot 2 |
| 7 | OFF | slot 1 |


Switch block S2 defines format and baud rate. It should be set to: 

| Switch | Position | Function |
| :----: | :------: | :------: |
|  1 | ON |
|  2 | ON |
|  3 | OFF | 1-3 set card to 8-bits with no parity
|  4 | OFF |
|  5 | OFF |
|  6 | ON |
|  7 | OFF | 5-7 set card to 9600 baud
  
  
Switch block S3 connects the UART to the serial connector (J2). These settings worked with the other settings listed here:

| Switch | Position | Function |
| :----: | :------: | :------: |
| 1 | OFF | disconnects serial card DTR from host computer
|  2 | OFF | disconnects DTR-CTS loopback
|  3 | OFF | disconnects host computer CTS from serial card
|  4 | ON  | connects serial card RTS to serial card CTS
|  5 | ON  | connects serial card RX to host TX
|  6 | OFF |
|  7 | OFF |
|  8 | ON  | connects serial card TX to host RX
  
All of the programs in here assume 9600 baud. It's probably possible to use 19200 baud too but I haven't tried.

Transferring ADT
================

  On the destination machine with Franklin card, enter `IN#2`

  In a shell on the host machine `./franklin_binary.py --raw hacked_adt/adt`
  
  The ADT program will be transferred from host to destination, taking several minutes. When finished, enter

  `803G` on the destination machine to launch ADT.
  
  In ADT, enter `C` for configure, then arrow down to COMMS DEVICE, select GENERIC SLOT 2 (really Dual Interface), and then RETURN.

