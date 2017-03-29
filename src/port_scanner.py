#!/usr/bin/env python
# Simple port scanner in python
# Carpe Noctem
import threading, socket
from optparse import OptionParser
op = OptionParser(usage='usage: %prog [options] hostname low_port [high_port]\n\nScan port range (low_port - high_port) on hostname.')
op.add_option('-t','--timeout', dest='timeout', default=0.2, type='float', metavar='SECS', help='connection timeout, in seconds. default 0.2')
op.add_option('-n','--threads', dest='threads', default=1, type='int', help='number of threads to use. default 1.')
op.add_option('-v','--verbose', dest='verbose', default=0, action='count', help='increase verbosity.')
(options, args) = op.parse_args()
if len(args) < 2:
  op.error('hostname and low_port are required')
try:
  low_port = int(args[1])
except:
  op.error('low_port must be an integer')
high_port = low_port
if len(args) > 2:
  try:
    high_port = int(args[2])
  except:
    op.error('high_port must be an integer')
  if high_port < low_port:
    op.error('high_port should be higher than low_port')
total_ports_to_scan = len(xrange(low_port,high_port +1))
if options.threads > (total_ports_to_scan / 10) + 1:
  op.error('number of threads is overkill for the number of ports we\'re scanning...')
host = socket.getaddrinfo(args[0],80)[0][4][0]
threads = options.threads
timeout = options.timeout
verbose = options.verbose

open_ports = []
child_msgs = []
scanned = 0
ports_per_thread = total_ports_to_scan / threads

class Child(threading.Thread):
  def __init__(self,prange=(80,80)):
    self.prange = prange
    threading.Thread.__init__(self)
  def run(self):
    global host,open_ports,timeout,verbose,scanned,child_msgs
    self.h = host
    self.t = timeout
    self.v = verbose
    self.o = []
    self.s = 0
    for port in xrange(self.prange[0],self.prange[-1] + 1):
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.settimeout(self.t)
      try:
        client.connect((self.h,port))
        self.o.append(port)
        child_msgs.append('scanning port ' + str(port) + ': ' + 'OPEN')
        client.close()
      except socket.error:
        child_msgs.append('scanning port ' + str(port) + ': ' + 'closed')
        client.close()
      self.s += 1
    open_ports.extend(self.o)
    scanned += self.s

try:
  print('Scanning...')
  for i in xrange(threads):
    low = (i * ports_per_thread) + low_port
    high = (low + ports_per_thread - 1)
    if i+1 >= threads and high_port - high < ports_per_thread:
      high = high_port
    Child((low,high)).start()

  last_active = threading.active_count()
  active = last_active
  if verbose > 0:
    print( 'Waiting for ' + str(active - 1) + ' threads to finish...')
  while active > 1:
    if verbose > 1:
        while (len(child_msgs) > 0):
            print( child_msgs.pop() #yes, we're not printing in the order the child messages were created,
                                   #but this is quicker and order doesn't necessarily matter when multi-threadded..
    if active != last_active:
      last_active = active
      if verbose > 0:
        print( 'Waiting for ' + str(active - 1) + ' threads to finish...')
    active = threading.active_count()

  open_ports.sort()
  print( '\nFinished scan for ' + host + '.\nTotal ports scanned: ' + str(scanned) + '\nOpen ports:\n' + str(open_ports))
except Exception:
  print( '\nExiting.')
  from sys import exit
exit(1)