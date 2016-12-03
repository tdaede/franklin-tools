Franklin Ace 1000/1200 Tools
============================

The Franklin Ace series predates the Apple Super Serial Card, so it includes its own implementation of a serial card: the Franklin Dual Interface Card. It's based on the 2661 UART. This UART is pretty mediocre, only supporting up to 19.2k and having a weird alternating register scheme in order to save 1 address pin.

The firmware on the card is totally bonkers. When activating it as an input (IN#2) the firmware forwards characters directly, with the high bit unset, which prevents bootstrapping ADT and makes the characters flash on screen. The built in mini-terminal correctly sets the bit, but is useless for bootstrapping.

Repository contents
===================

- franklin_term.py - Simple program to echo keyboard commands to the Ace.
- franklin_bootstrap.py - Like terminal, but reads a file and echoes it over the serial port instead.
- franklin_binary.py - Transfers a binary program into memory, such as ADT.
- franklin_adt/ - A hacked copy of the original DOS ADT client.

Configuring the serial card
===========================

All of the programs in here assume 9600 baud. It's probably possible to use 19200 baud too but I haven't tried.

Transferring ADT
================

  IN#2

  ./franklin_binary.py --raw franklin_adt/adt

  803G
  
Then hit C for configure, then arrow down to COMMS DEVICE, select GENERIC SLOT 2 (really Dual Interface), and then RETURN.

