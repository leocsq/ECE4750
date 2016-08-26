#=========================================================================
# IntMulFL_test
#=========================================================================

import pytest
import random

random.seed(0xdeadbeef)

from pymtl      import *
from pclib.test import mk_test_case_table, run_sim
from pclib.test import TestSource, TestSink

from lab1_imul.IntMulFL   import IntMulFL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness (Model):

  def __init__( s, imul, src_msgs, sink_msgs,
                src_delay, sink_delay,
                dump_vcd=False, test_verilog=False ):

    # Instantiate models

    s.src  = TestSource ( Bits(64), src_msgs,  src_delay  )
    s.imul = imul
    s.sink = TestSink   ( Bits(32), sink_msgs, sink_delay )

    # Dump VCD

    if dump_vcd:
      s.imul.vcd_file = dump_vcd

    # Translation

    if test_verilog:
      s.imul = TranslationTool( s.imul )

    # Connect

    s.connect( s.src.out,  s.imul.req  )
    s.connect( s.imul.resp, s.sink.in_ )

  def done( s ):
    return s.src.done and s.sink.done

  def line_trace( s ):
    return s.src.line_trace()  + " > " + \
           s.imul.line_trace()  + " > " + \
           s.sink.line_trace()

#-------------------------------------------------------------------------
# mk_req_msg
#-------------------------------------------------------------------------

def req( a, b ):
  msg = Bits( 64 )
  msg[32:64] = Bits( 32, a, trunc=True )
  msg[ 0:32] = Bits( 32, b, trunc=True )
  return msg

def resp( a ):
  return Bits( 32, a, trunc=True )

#----------------------------------------------------------------------
# Test Case: small positive * positive
#----------------------------------------------------------------------

small_pos_pos_msgs = [
  req(  2,  3 ), resp(   6 ),
  req(  4,  5 ), resp(  20 ),
  req(  3,  4 ), resp(  12 ),
  req( 10, 13 ), resp( 130 ),
  req(  8,  7 ), resp(  56 ),
]

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional lists of request/response messages to create
# additional directed and random test cases.
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                      "msgs                 src_delay sink_delay"),
  [ "small_pos_pos",     small_pos_pos_msgs,   0,        0          ],

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to leverage the additional lists
  # of request/response messages defined above, but also to test
  # different source/sink random delays.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

#-------------------------------------------------------------------------
# Test cases
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, dump_vcd ):
  run_sim( TestHarness( IntMulFL(),
                        test_params.msgs[::2], test_params.msgs[1::2],
                        test_params.src_delay, test_params.sink_delay ),
           dump_vcd )

