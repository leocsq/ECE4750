#=========================================================================
# add
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
    add x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 9
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "add",   1,  1,  2 ),
    gen_rr_dest_dep_test( 4, "add",   2, -1,  1 ),
    gen_rr_dest_dep_test( 3, "add",  -3,  1, -2 ),
    gen_rr_dest_dep_test( 2, "add",  -4, -1, -5 ),
    gen_rr_dest_dep_test( 1, "add",   5,  1,  6 ),
    gen_rr_dest_dep_test( 0, "add",   6,  1,  7 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "add",   7,  1,   8 ),
    gen_rr_src0_dep_test( 4, "add",   8, -1,   7 ),
    gen_rr_src0_dep_test( 3, "add",  -9,  1,  -8),
    gen_rr_src0_dep_test( 2, "add", -10, -1, -11 ),
    gen_rr_src0_dep_test( 1, "add",  11,  1,  12 ),
    gen_rr_src0_dep_test( 0, "add",  12,  1,  13 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "add",  13,  1,  14 ),
    gen_rr_src1_dep_test( 4, "add",  14, -1,  13 ),
    gen_rr_src1_dep_test( 3, "add", -15,  1, -14 ),
    gen_rr_src1_dep_test( 2, "add", -16, -1, -17 ),
    gen_rr_src1_dep_test( 1, "add",  17,  1,  18 ),
    gen_rr_src1_dep_test( 0, "add",  18,  1,  19 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "add",  19,  1,  20 ),
    gen_rr_srcs_dep_test( 4, "add",  20, -1,  19 ),
    gen_rr_srcs_dep_test( 3, "add", -21,  1, -20 ),
    gen_rr_srcs_dep_test( 2, "add", -22, -1, -23 ),
    gen_rr_srcs_dep_test( 1, "add",  23,  1,  24 ),
    gen_rr_srcs_dep_test( 0, "add",  24,  1,  25 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "add", 25, 1, 26 ),
    gen_rr_src1_eq_dest_test( "add", 26, 1, 27 ),
    gen_rr_src0_eq_src1_test( "add", 27, 54 ),
    gen_rr_srcs_eq_dest_test( "add", 28, 56 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "add", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "add", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rr_value_test( "add", 0x00000003, 0x00000007, 0x0000000a ),

    gen_rr_value_test( "add", 0x00000000, 0xffff8000, 0xffff8000 ),
    gen_rr_value_test( "add", 0x80000000, 0x00000000, 0x80000000 ),
    gen_rr_value_test( "add", 0x80000000, 0xffff8000, 0x7fff8000 ),

    gen_rr_value_test( "add", 0x00000000, 0x00007fff, 0x00007fff ),
    gen_rr_value_test( "add", 0x7fffffff, 0x00000000, 0x7fffffff ),
    gen_rr_value_test( "add", 0x7fffffff, 0x00007fff, 0x80007ffe ),

    gen_rr_value_test( "add", 0x80000000, 0x00007fff, 0x80007fff ),
    gen_rr_value_test( "add", 0x7fffffff, 0xffff8000, 0x7fff7fff ),

    gen_rr_value_test( "add", 0x00000000, 0xffffffff, 0xffffffff ),
    gen_rr_value_test( "add", 0xffffffff, 0x00000001, 0x00000000 ),
    gen_rr_value_test( "add", 0xffffffff, 0xffffffff, 0xfffffffe ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = src0 + src1
    asm_code.append( gen_rr_value_test( "add", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code

