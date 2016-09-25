#=========================================================================
# srl
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
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srl x3, x1, x2
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
#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "srl",   1,  1,  0 ),
    gen_rr_dest_dep_test( 4, "srl",   2,  1,  1 ),
    gen_rr_dest_dep_test( 3, "srl",  -3,  1, -2 ),
    gen_rr_dest_dep_test( 2, "srl",  -4,  2, -1 ),
    gen_rr_dest_dep_test( 1, "srl",   5,  2,  1 ),
    gen_rr_dest_dep_test( 0, "srl",  -6,  2, -2 ),
  ]
#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "srl",   7,  1,   3 ),
    gen_rr_src0_dep_test( 4, "srl",   8,  2,   2 ),
    gen_rr_src0_dep_test( 3, "srl",   9,  3,   1 ),
    gen_rr_src0_dep_test( 2, "srl", -10, 20,   4095 ),
    gen_rr_src0_dep_test( 1, "srl", -11, 24,   255 ),
    gen_rr_src0_dep_test( 0, "srl", -12, 26,   63 ),
  ]
#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "srl",  13,  1,   6 ),
    gen_rr_src1_dep_test( 4, "srl",  14,  2,   3 ),
    gen_rr_src1_dep_test( 3, "srl",  15,  3,   1),
    gen_rr_src1_dep_test( 2, "srl", -16,  1,   2147483640 ),
    gen_rr_src1_dep_test( 1, "srl", -17, 20,   4095 ),
    gen_rr_src1_dep_test( 0, "srl", -18, 26,   63 ),
  ]
#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "srl",  19,  1,   9 ),
    gen_rr_srcs_dep_test( 4, "srl",  20,  2,   5 ),
    gen_rr_srcs_dep_test( 3, "srl",  21,  3,   2 ),
    gen_rr_srcs_dep_test( 2, "srl", -22,  1,   2147483637 ),
    gen_rr_srcs_dep_test( 1, "srl", -23,  3,   536870909 ),
    gen_rr_srcs_dep_test( 0, "srl", -24,  5,   134217727 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "srl",  25, 1, 12 ),
    gen_rr_src1_eq_dest_test( "srl", -26, 3, 536870908),
    gen_rr_src0_eq_src1_test( "srl", 27, 0 ),
    gen_rr_srcs_eq_dest_test( "srl", 28, 0 ),
  ]
#-------------------------------------------------------------------------
# gen_value_test // imcomplete
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "srl", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "srl", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_value_test( "srl", 0x00000007, 0x00000003, 0x00000000 ),
    
    gen_rr_value_test( "srl", 0x00010000, 0x00000004, 0x00001000 ),
    gen_rr_value_test( "srl", 0x80000000, 0x00000005, 0x04000000 ),
    gen_rr_value_test( "srl", 0x89000000, 0x00000007, 0x01120000 ),

    gen_rr_value_test( "srl", 0x00000000, 0x00007fff, 0x00000000 ),
    gen_rr_value_test( "srl", 0x00007fff, 0x0000000b, 0x0000000f ),
    gen_rr_value_test( "srl", 0x7fffffff, 0x0000000a, 0x001fffff ),

    gen_rr_value_test( "srl", 0x80000000, 0x00007fff, 0x00000001 ),
    gen_rr_value_test( "srl", 0x7fffffff, 0x0000000d, 0x0003ffff ), 
       
   # gen_rr_value_test( "srl", 0x00000000, 0xffffffff, 0x00000000 ),
    gen_rr_value_test( "srl", 0xfffffffb, 0x00000001, 0x7ffffffd ),
    gen_rr_value_test( "srl", 0xffffffff, 0x0000000f, 0x0001ffff ),    
  ]
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = random.randint(0,4294967295)
    src1 = random.randint(0,4294967295)   
    dest = src0 >> src1
    asm_code.append( gen_rr_value_test( "srl", src0, src1, dest) )
  return asm_code
