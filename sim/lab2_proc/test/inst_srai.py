#=========================================================================
# srai
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 0x00008000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srai x3, x1, 0x03
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00001000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rimm_dest_dep_test( 5, "srai",   1,  1,  0 ),
    gen_rimm_dest_dep_test( 4, "srai",   2,  1,  1 ),
    gen_rimm_dest_dep_test( 3, "srai",  -3,  1, -2 ),
    gen_rimm_dest_dep_test( 2, "srai",  -4,  2, -1 ),
    gen_rimm_dest_dep_test( 1, "srai",   5,  2,  1 ),
    gen_rimm_dest_dep_test( 0, "srai",  -6,  2, -2 ),
  ]
#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srai",   7,  1,   3 ),
    gen_rimm_src_dep_test( 4, "srai",   8,  1,   4 ),
    gen_rimm_src_dep_test( 3, "srai",  -9,  1,  -5 ),
    gen_rimm_src_dep_test( 2, "srai", -10,  2,  -3 ),
    gen_rimm_src_dep_test( 1, "srai",  11,  2,   2 ),
    gen_rimm_src_dep_test( 0, "srai", -12,  2,  -3 ),
  ]
#-------------------------------------------------------------------------
# gen_src_eq_dest_test
#-------------------------------------------------------------------------
def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test(  "srai",  13,  1,   6 ),
    gen_rimm_src_eq_dest_test(  "srai",  14,  1,   7 ),
    gen_rimm_src_eq_dest_test(  "srai", -15,  1,  -8 ),
    gen_rimm_src_eq_dest_test(  "srai", -16,  2,  -4 ),
    gen_rimm_src_eq_dest_test(  "srai",  17,  2,   4 ),
    gen_rimm_src_eq_dest_test(  "srai", -18,  2,  -5 ),
  ]
#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rimm_value_test( "srai", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rimm_value_test( "srai", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rimm_value_test( "srai", 0x00000007, 0x00000002, 0x00000001 ),
    
    gen_rimm_value_test( "srai", 0x000f0f0f, 0x00000004, 0x0000f0f0 ),
    gen_rimm_value_test( "srai", 0x000f0f0f, 0x00000010, 0x0000000f ),
    gen_rimm_value_test( "srai", 0x000f0f0f, 0x00000011, 0x00000007 ),
    
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src = Bits( 32, random.randint(0,0xffffffff) )
    imm = Bits(  5, random.randint(0,0b11111) ) 
    stemp = sext(imm, 32)
    if src[31] == 0:
      dest = src>>imm
    else:
      temp1 = ~src
      temp2 = temp1>>imm
      dest= 0xffffffff-temp2
  asm_code.append( gen_rimm_value_test( "srai", src.uint(), imm.uint(), dest.uint()) )
  return asm_code
