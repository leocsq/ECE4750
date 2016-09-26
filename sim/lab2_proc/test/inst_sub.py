#=========================================================================
# sub
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
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sub x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 1
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
# gen_basic_test
#-------------------------------------------------------------------------
def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "sub",   1,  1,  0 ),
    gen_rr_dest_dep_test( 4, "sub",   2, -1,  3 ),
    gen_rr_dest_dep_test( 3, "sub",  -3,  1, -4 ),
    gen_rr_dest_dep_test( 2, "sub",  -4, -1, -3 ),
    gen_rr_dest_dep_test( 1, "sub",   5,  1,  4 ),
    gen_rr_dest_dep_test( 0, "sub",   6,  1,  5 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sub",   7,  1,   6 ),
    gen_rr_src0_dep_test( 4, "sub",   8, -1,   9 ),
    gen_rr_src0_dep_test( 3, "sub",  -9,  1,  -10),
    gen_rr_src0_dep_test( 2, "sub", -10, -1,  -9 ),
    gen_rr_src0_dep_test( 1, "sub",  11,  1,  10 ),
    gen_rr_src0_dep_test( 0, "sub",  12,  1,  11 ),
  ]
  
#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sub",  13,  1,  12 ),
    gen_rr_src1_dep_test( 4, "sub",  14, -1,  15 ),
    gen_rr_src1_dep_test( 3, "sub", -15,  1, -16 ),
    gen_rr_src1_dep_test( 2, "sub", -16, -1, -15 ),
    gen_rr_src1_dep_test( 1, "sub",  17,  1,  16 ),
    gen_rr_src1_dep_test( 0, "sub",  18,  1,  17 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sub",  19,  1,  18 ),
    gen_rr_srcs_dep_test( 4, "sub",  20, -1,  21 ),
    gen_rr_srcs_dep_test( 3, "sub", -21,  1, -22 ),
    gen_rr_srcs_dep_test( 2, "sub", -22, -1, -21 ),
    gen_rr_srcs_dep_test( 1, "sub",  23,  1,  22 ),
    gen_rr_srcs_dep_test( 0, "sub",  24,  1,  23 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sub", 25, 1, 24 ),
    gen_rr_src1_eq_dest_test( "sub", 26, 1, 25 ),
    gen_rr_src0_eq_src1_test( "sub", 27, 0 ),
    gen_rr_srcs_eq_dest_test( "sub", 28, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "sub", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "sub", 0x00000001, 0x00000002, 0xffffffff ),
    gen_rr_value_test( "sub", 0x00004000, 0x00003f50, 0x000000B0 ),
    gen_rr_value_test( "sub", 0x00800000, 0x007ff111, 0x00000eef ),    
    gen_rr_value_test( "sub", 0x7fff0000, 0x4fff0000, 0x30000000 ),
    gen_rr_value_test( "sub", 0xffffffff, 0xffff0000, 0x0000ffff ),
    gen_rr_value_test( "sub", 0xffff8000, 0xffff0800, 0x00007800 ),
  ]
  
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------  
def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = src0 - src1
    asm_code.append( gen_rr_value_test( "sub", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
