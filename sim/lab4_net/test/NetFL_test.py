#=========================================================================
# NetFL_test.py
#=========================================================================

from __future__     import print_function

import pytest
import random

random.seed(0xdeadbeef)

from pymtl          import *
from pclib.test     import TestSource, TestNetSink, mk_test_case_table
from pclib.ifcs     import NetMsg
from lab4_net.NetFL import NetFL

#-------------------------------------------------------------------------
# Helper functions
#-------------------------------------------------------------------------

def mk_msg( src, dest, opaque, payload,
            payload_nbits=32, opaque_nbits=8, num_ports=4 ):
  """Utility function to create a NetMsg object."""

  msg         = NetMsg( num_ports, 2**opaque_nbits, payload_nbits )
  msg.src     = src
  msg.dest    = dest
  msg.opaque  = opaque
  msg.payload = payload

  return msg

def mk_net_msgs( nports, msg_list ):
  """Utility function to create the msgs from a list of msg parameters."""

  src_msgs  = [ [] for x in xrange(nports) ]
  sink_msgs = [ [] for x in xrange(nports) ]

  for x in msg_list:
    src, dest, opaque, payload = x[0], x[1], x[2], x[3]

    msg = mk_msg( src, dest, opaque, payload, num_ports=nports )
    src_msgs [src ].append( msg )
    sink_msgs[dest].append( msg )

  return [ src_msgs, sink_msgs ]

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Model ):

  # Constructor

  def __init__( s, NetModel, src_msgs, sink_msgs, src_delay, sink_delay,
                num_ports, opaque_nbits, payload_nbits,
                dump_vcd=False, test_verilog=False ):

    s.src_msgs   = src_msgs
    s.sink_msgs  = sink_msgs
    s.src_delay  = src_delay
    s.sink_delay = sink_delay
    s.num_ports  = num_ports

    msg_type = NetMsg( num_ports, 2**opaque_nbits, payload_nbits )

    s.src  = [ TestSource ( msg_type, s.src_msgs[x],  s.src_delay  ) for x in xrange(num_ports) ]
    s.net  = NetModel
    s.sink = [ TestNetSink( msg_type, s.sink_msgs[x], s.sink_delay ) for x in xrange(num_ports) ]

    # Dump VCD

    if dump_vcd:
      s.net.vcd_file = dump_vcd
      if hasattr(s.net, 'inner'):
        s.net.inner.vcd_file = dump_vcd

    # Translation

    if test_verilog:
      s.net = TranslationTool( s.net )

    # Connect

    for i in xrange(num_ports):
      s.connect( s.net.in_[i], s.src[i].out  )
      s.connect( s.net.out[i], s.sink[i].in_ )

  # Done

  def done( s ):
    done_flag = 1
    for i in xrange(s.num_ports):
      done_flag &= s.src[i].done and s.sink[i].done
    return done_flag

  # Line-trace

  def line_trace( s ):
    in_ = '|'.join( [ x.out.to_str( "%02s:%1s>%1s" % (  x.out.msg[32:40],
                                                        x.out.msg[40:40+clog2(s.num_ports)],
                                                        x.out.msg[40+clog2(s.num_ports):40+clog2(s.num_ports)*2] ) )
                                        for x in s.src  ] )
    out = '|'.join( [ x.in_.to_str( "%02s:%1s>%1s" % (  x.in_.msg[32:40],
                                                        x.in_.msg[40:40+clog2(s.num_ports)],
                                                        x.in_.msg[40+clog2(s.num_ports):40+clog2(s.num_ports)*2] ) )
                                        for x in s.sink ] )
    return in_ + ' >>> ' + s.net.line_trace() + ' >>> ' + out

#-------------------------------------------------------------------------
# run_net_test
#-------------------------------------------------------------------------

def run_net_test( NetModel, src_delay, sink_delay, test_msgs,
                  dump_vcd = False, test_verilog = False,
                  num_ports = 4, opaque_nbits = 8, payload_nbits = 32 ):

  # src/sink msgs

  src_msgs  = test_msgs[0]
  sink_msgs = test_msgs[1]

  # Instantiate and elaborate the model

  model = TestHarness( NetModel, src_msgs, sink_msgs, src_delay, sink_delay,
                       num_ports, opaque_nbits, payload_nbits,
                       dump_vcd, test_verilog )

  model.vcd_file     = dump_vcd
  model.test_verilog = test_verilog
  model.elaborate()

  # Create a simulator using the simulation tool

  sim = SimulationTool( model )

  # Run the simulation

  print()

  sim.reset()
  while not model.done() and sim.ncycles < 50000:
    sim.print_line_trace()
    sim.cycle()

  # Add a couple extra ticks so that the VCD dump is nicer

  sim.cycle()
  sim.cycle()
  sim.cycle()

  # Check for success

  if not model.done():
    raise AssertionError( "Simulation did not complete!" )

#-------------------------------------------------------------------------
# Test case: one pkt
#-------------------------------------------------------------------------

def one_pkt_msgs():

  nports = 4

  return mk_net_msgs( nports,
#       src dest opaque payload
    [ ( 0,  2,  0x00,  0xab ),
    ]
  )

#-------------------------------------------------------------------------
# Test case: every source to every destination
#-------------------------------------------------------------------------

def single_dest_msgs():

  nports = 4

  return mk_net_msgs( nports,
#       src dest opaque payload
    [ ( 0,  0,   0x00,  0xce ),
      ( 1,  0,   0x01,  0xff ),
      ( 2,  0,   0x02,  0x80 ),
      ( 3,  0,   0x03,  0xc0 ),
      ( 0,  1,   0x04,  0xce ),
      ( 1,  1,   0x05,  0xff ),
      ( 2,  1,   0x06,  0x80 ),
      ( 3,  1,   0x07,  0xc0 ),
      ( 0,  2,   0x08,  0xce ),
      ( 1,  2,   0x09,  0xff ),
      ( 2,  2,   0x0a,  0x80 ), 
      ( 3,  2,   0x0b,  0xc0 ),
      ( 0,  3,   0x0c,  0xce ),
      ( 1,  3,   0x0d,  0xff ),
      ( 2,  3,   0x0e,  0x80 ),
      ( 3,  3,   0x0f,  0xc0 ),
    ]
  )

#-------------------------------------------------------------------------
# Test case: single source to every destination 
#-------------------------------------------------------------------------

def single_src_msgs():

  nports = 4

  return mk_net_msgs( nports,
#       src dest opaque payload
    [ ( 0,  0,   0x00,  0xce ),
      ( 0,  1,   0x01,  0xff ),
      ( 0,  2,   0x02,  0x80 ),
      ( 0,  3,   0x03,  0xc0 ),
      ( 1,  0,   0x04,  0xce ),
      ( 1,  1,   0x05,  0xff ),
      ( 1,  2,   0x06,  0x80 ),
      ( 1,  3,   0x07,  0xc0 ),
      ( 2,  0,   0x08,  0xce ),
      ( 2,  1,   0x09,  0xff ),
      ( 2,  2,   0x0a,  0x80 ), 
      ( 2,  3,   0x0b,  0xc0 ),
      ( 3,  0,   0x0c,  0xce ),
      ( 3,  1,   0x0d,  0xff ),
      ( 3,  2,   0x0e,  0x80 ),
      ( 3,  3,   0x0f,  0xc0 ),

    ]
  )

#-------------------------------------------------------------------------
# Test case: one pkt from each node to its neighbor
#-------------------------------------------------------------------------

def neighbor_msgs():

  nports = 4

  return mk_net_msgs( nports,
#       src dest opaque payload
    [ ( 0,  1,   0x00,  0xce ),
      ( 1,  2,   0x01,  0xff ),
      ( 2,  3,   0x02,  0x80 ),
      ( 3,  0,   0x03,  0xc0 ),
      ( 0,  2,   0x04,  0xce ),
      ( 2,  0,   0x05,  0xff ),
      ( 0,  3,   0x06,  0x80 ),
      ( 3,  2,   0x07,  0xc0 ),
      ( 2,  1,   0x08,  0xce ),
      ( 1,  0,   0x09,  0xff ),
    ]
  )

#-------------------------------------------------------------------------
# Test case: fully_random (random ports, random opaque, random message)
#-------------------------------------------------------------------------

def fully_random():

  nports = 4
  msgs = []
  ports = [0,1,2,3]
  for i in range(100):
#                src                   dest                  opaque payload
    msgs.append((random.choice(ports), random.choice(ports), i%16, i))

  return mk_net_msgs( nports,msgs)

#-------------------------------------------------------------------------
# Test case: hotspot_src, prolonged traffic to a single scource node 0
#-------------------------------------------------------------------------

def hotspot_src():

  nports = 4
  msgs = []
  ports = [0,1,2,3]
  for i in range(1000):
#                src dest                  opaque payload
    msgs.append((0,  random.choice(ports), i%16,  i))
    
  return mk_net_msgs( nports, msgs )

#-------------------------------------------------------------------------
# Test case: hotspot_dest, prolonged traffic to a single destination node 0
#-------------------------------------------------------------------------

def hotspot_dest():

  nports = 4
  msgs = []
  ports = [0,1,2,3]
  for i in range(1000):
#                src                   dest  opaque payload
    msgs.append((random.choice(ports), 0,    i%16,  i))
    
  return mk_net_msgs( nports, msgs )
#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

# list for random delay
delay_list = []
for i in range(25):
  delay_list.append(i)

test_case_table = mk_test_case_table([
  (                                   "msgs                     src_delay                    sink_delay"              ),
  [ "one_pkt",                        one_pkt_msgs(),           0,                           0                        ],
  [ "single_dest",                    single_dest_msgs(),       0,                           0                        ],
  [ "single_src",                     single_src_msgs(),        0,                           0                        ], 
  [ "neighbor",                       neighbor_msgs(),          0,                           0                        ], 
  [ "neighbor_scr_2delay",            neighbor_msgs(),          2,                           0                        ], # fixed delay
  [ "neighbor_dest_2delay",           neighbor_msgs(),          0,                           2                        ], # fixed delay
  [ "neighbor_delay",                 neighbor_msgs(),          random.choice(delay_list),   random.choice(delay_list)],   
  [ "fully_random",                   fully_random(),           0,                           0                        ], 
  [ "fully_random_randomdelay",       fully_random(),           random.choice(delay_list),   random.choice(delay_list)],   
  [ "hotspot_src",                    hotspot_src(),            0,                           0                        ],
  [ "hotspot_src_randomdelay",        hotspot_src(),            random.choice(delay_list),   random.choice(delay_list)],
  [ "hotspot_dest",                   hotspot_dest(),           0,                           0                        ],
  [ "hotspot_dest_randomdelay",       hotspot_dest(),           random.choice(delay_list),   random.choice(delay_list)],
])


#-------------------------------------------------------------------------
# Run tests
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, dump_vcd, test_verilog ):
  run_net_test( NetFL(), test_params.src_delay, test_params.sink_delay,
                test_params.msgs, dump_vcd, test_verilog )
