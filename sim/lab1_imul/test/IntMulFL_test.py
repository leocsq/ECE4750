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
#----------------------------------------------------------------------
# Test Case: small negative * positive
#----------------------------------------------------------------------

small_neg_pos_msgs = [
  req(  -2,  3 ), resp(   -6 ),
  req(  -4,  5 ), resp(  -20 ),
  req(  -3,  4 ), resp(  -12 ),
  req( -10, 13 ), resp( -130 ),
  req(  -8,  7 ), resp(  -56 ),
]

#----------------------------------------------------------------------
# Test Case: small positive * negative
#----------------------------------------------------------------------

small_pos_neg_msgs = [
  req(  2,  -3 ), resp(   -6 ),
  req(  4,  -5 ), resp(  -20 ),
  req(  3,  -4 ), resp(  -12 ),
  req( 10, -13 ), resp( -130 ),
  req(  8,  -7 ), resp(  -56 ),
]

#----------------------------------------------------------------------
# Test Case: small negative * negative
#----------------------------------------------------------------------

small_neg_neg_msgs = [
  req(  -2,  -3 ), resp(   6 ),
  req(  -4,  -5 ), resp(  20 ),
  req(  -3,  -4 ), resp(  12 ),
  req( -10, -13 ), resp( 130 ),
  req(  -8,  -7 ), resp(  56 ),
]

#----------------------------------------------------------------------
# Test Case: random small positive * positive
#----------------------------------------------------------------------

random.seed(0xdeadbeef)
random_small_pos_pos_msgs = []
for i in xrange(5):
    a = random.randint(0,255)
    b = random.randint(0,255)
    c = a*b
    random_small_pos_pos_msgs.extend([req(a,b),resp(c)])

#----------------------------------------------------------------------
# Test Case: random small positive * negative
#----------------------------------------------------------------------

random_small_pos_neg_msgs = []
for i in xrange(5):
    a = random.randint( 0,255)
    b = random.randint(-255,0)
    c = a*b
    random_small_pos_neg_msgs.extend([req(a,b),resp(c)])

#----------------------------------------------------------------------
# Test Case: random small negative * positive
#----------------------------------------------------------------------

random_small_neg_pos_msgs = []
for i in xrange(5):
    a = random.randint(-255,0)
    b = random.randint(0,255)
    c = a*b
    random_small_neg_pos_msgs.extend([req(a,b),resp(c)])

#----------------------------------------------------------------------
# Test Case: random small negative * negative
#----------------------------------------------------------------------
    
random_small_neg_neg_msgs = []
for i in xrange(5):
    a = random.randint(-255,0)
    b = random.randint(-255,0)
    c = a*b
    random_small_neg_pos_msgs.extend([req(a,b),resp(c)])

#----------------------------------------------------------------------
# Test Case:  large positive * positive
#----------------------------------------------------------------------

large_pos_pos_msgs = [
  req(  0x1abcd,  0x1dcba ), resp(  0x31CA7FEF2 ), 
  ##overflow result but still as exact trunc result as multiplier does
  req(  0xabcd,   0xdcba  ), resp(  0x9420FEF2  ),
]

#----------------------------------------------------------------------
# Test Case:  large negative * positive
#----------------------------------------------------------------------

large_neg_pos_msgs = [
  req(  0xFFFFD8F0, 0x2710), resp( 0xFA0A1F00),
]

#----------------------------------------------------------------------
# Test Case:  large positive * negative
#----------------------------------------------------------------------

large_pos_neg_msgs = [
  req(  0x2710, 0xFFFFD8F0), resp( 0xFA0A1F00),
]

#----------------------------------------------------------------------
# Test Case:  large negative * negative
#----------------------------------------------------------------------

large_neg_neg_msgs = [
  req( 0xFFFFB1E0, 0xFFFF8AD0), resp(0x23c34600),
]

#----------------------------------------------------------------------
# Test Case:  random large positive * positive
#----------------------------------------------------------------------

random_large_pos_pos_msgs = []
for i in xrange(5):
    a = random.randint(1024,65535)
    b = random.randint(1024,65535)
    c = a*b
    random_large_pos_pos_msgs.extend([req(a,b),resp(c)])

#----------------------------------------------------------------------
# Test Case:  random large negative * positive
#----------------------------------------------------------------------    
random_large_neg_pos_msgs = []
for i in xrange(5):
    a = random.randint(-65535,-1024)
    b = random.randint(1024,65535)
    c = a*b
    random_large_neg_pos_msgs.extend([req(a,b),resp(c)])

#----------------------------------------------------------------------
# Test Case:  random large positive * negative
#----------------------------------------------------------------------    
random_large_pos_neg_msgs = []
for i in xrange(5):
    a = random.randint(1024,65535)
    b = random.randint(-65535,-1024)
    c = a*b
    random_large_pos_neg_msgs.extend([req(a,b),resp(c)])

#----------------------------------------------------------------------
# Test Case:  random large negative * positive
#----------------------------------------------------------------------
random_large_neg_neg_msgs = []
for i in xrange(5):
    a = random.randint(-65535,-1024)
    b = random.randint(-65535,-1024)
    c = a*b
    random_large_neg_neg_msgs.extend([req(a,b),resp(c)])
#----------------------------------------------------------------------
# Test Case:  direct many ones
#----------------------------------------------------------------------
many_ones_msgs = [
  req(   0xFFFFF, 0xF   ), resp( 0xEFFFF1   ),
] 
#----------------------------------------------------------------------
# Test Case:  direct many zeros
#----------------------------------------------------------------------
many_zeros_msgs = [
  req(  0x8000, 0x10 ), resp( 0x80000 ),
]
#----------------------------------------------------------------------
# Test Case:  random  many zeros
#----------------------------------------------------------------------
random_manyzeros_msgs = []
for i in xrange(5):
    a = random.randint(0,0xFFFFFFFF)
    b = random.randint(0,0xFFFFFFFF)
    a = a&0xc0000003
    b = b&0xc0000003
    c = a*b
    random_manyzeros_msgs.extend([req(a,b),resp(c)])
#----------------------------------------------------------------------
# Test Case:  random  many ones
#----------------------------------------------------------------------
random_manyones_msgs = []
for i in xrange(5):
    a = random.randint(0,0xFFFFFFFF)
    b = random.randint(0,0xFFFFFFFF)
    a = a|0x00FFFF00
    b = b|0x00FFFF00
    c = a*b
    random_manyones_msgs.extend([req(a,b),resp(c)])



#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                      "msgs                 src_delay sink_delay"),
  [ "small_pos_pos",     small_pos_pos_msgs,    0,        0          ],
  [ "small_neg_pos",     small_neg_pos_msgs,    0,        0          ],
  [ "small_pos_neg",     small_pos_neg_msgs,    0,        0          ],
  [ "small_neg_neg",     small_neg_neg_msgs,    0,        0          ],
  [ "samll_pos_pos",     small_pos_pos_msgs,    0,        0          ],
  [ "large_pos_pos",     large_pos_pos_msgs,    0,        0          ],
  [ "large_neg_pos",     large_neg_pos_msgs,    0,        0          ],
  [ "large_pos_neg",     large_pos_neg_msgs,    0,        0          ],
  [ "large_neg_neg",     large_neg_neg_msgs,    0,        0          ],
  [ "many_ones",         many_ones_msgs,        0,        0          ],
  [ "many_zeros",        many_zeros_msgs,       0,        0          ],
  
  [ "random_small_pos_pos", random_small_pos_pos_msgs,      0,   0   ],
  [ "random_small_pos_neg", random_small_pos_neg_msgs,      0,   0   ],
  [ "random_small_neg_pos", random_small_neg_pos_msgs,      0,   0   ],
  [ "random_small_neg_neg", random_small_neg_neg_msgs,      0,   0   ],
  [ "random_large_pos_pos", random_large_pos_pos_msgs,      0,   0   ],
  [ "random_large_neg_pos", random_large_neg_pos_msgs,      0,   0   ],
  [ "random_large_pos_neg", random_large_pos_neg_msgs,      0,   0   ],
  [ "random_large_neg_neg", random_large_neg_neg_msgs,      0,   0   ],
  [ "random_manyones",      random_manyones_msgs,           0,   0   ],
  [ "random_manyzeros",     random_manyzeros_msgs,          0,   0   ],
  
  [ "random_delay_small_pos_pos", random_small_pos_pos_msgs, 5,   5   ],
  [ "random_delay_small_pos_neg", random_small_pos_neg_msgs, 5,   5   ],
  [ "random_delay_small_neg_pos", random_small_neg_pos_msgs, 5,   5   ],
  [ "random_delay_small_neg_neg", random_small_neg_neg_msgs, 5,   5   ],
  [ "random_delay_large_pos_pos", random_large_pos_pos_msgs, 5,   5   ],
  [ "random_delay_large_neg_pos", random_large_neg_pos_msgs, 5,   5   ],
  [ "random_delay_large_pos_neg", random_large_pos_neg_msgs, 5,   5   ],
  [ "random_delay_large_neg_neg", random_large_neg_neg_msgs, 5,   5   ],
  [ "random_delay_manyones",      random_manyones_msgs,      5,   5   ],
  [ "random_delay_manyzeros",     random_manyzeros_msgs,     5,   5   ]

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

