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
    [ ( 0,  2,   0x00,  0xab ),
    ]
  )

#-------------------------------------------------------------------------
# Test case: single destination
#-------------------------------------------------------------------------

def single_dest_msgs():

  nports = 4

  return mk_net_msgs( nports,
#       src dest opaque payload
    [ ( 0,  0,   0x00,  0xce ),
      ( 1,  0,   0x01,  0xff ),
      ( 2,  0,   0x02,  0x80 ),
      ( 3,  0,   0x03,  0xc0 ),
    ]
  )

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Add new test cases
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                      "msgs                 src_delay sink_delay"),
  [ "one_pkt",            one_pkt_msgs(),      0,        0          ],
  [ "single_dest",        single_dest_msgs(),  0,        0          ],

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to leverage the additional lists
  # of request/response messages defined above, but also to test
  # different source/sink random delays.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

#-------------------------------------------------------------------------
# Run tests
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, dump_vcd, test_verilog ):
  run_net_test( NetFL(), test_params.src_delay, test_params.sink_delay,
                test_params.msgs, dump_vcd, test_verilog )
