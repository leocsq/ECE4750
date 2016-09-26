#=========================================================================
# sll

# - Summary   : Shift left logical by register value (append zeroes)
# - Assembly  : sll rd, rs1, rs2
# - Semantics : R[rd] = R[rs1] << R[rs2][4:0]
# - Format    : R-type
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
    csrr x1, mngr2proc < 0x80008000
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sll x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00040000
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
    gen_rr_dest_dep_test( 5, "sll",   1,  1,  2 ),
    gen_rr_dest_dep_test( 4, "sll",   2,  1,  4 ),
    gen_rr_dest_dep_test( 3, "sll",  -3,  1, -6 ),
    gen_rr_dest_dep_test( 2, "sll",  -4,  2,-16 ),
    gen_rr_dest_dep_test( 1, "sll",   5,  3,  0 ),
    gen_rr_dest_dep_test( 0, "sll",  -6,  3,-48 ),
  ]
#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sll",   7,  1,  14 ),
    gen_rr_src0_dep_test( 4, "sll",   8,  2,  32 ),
    gen_rr_src0_dep_test( 3, "sll",   9,  3,  72 ),
    gen_rr_src0_dep_test( 2, "sll", -10,  1, -20 ),
    gen_rr_src0_dep_test( 1, "sll", -11,  2, -44 ),
    gen_rr_src0_dep_test( 0, "sll", -12,  3, -96 ),
  ]
#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [ 
    gen_rr_src1_dep_test( 5, "sll",  13,  1,   26 ),
    gen_rr_src1_dep_test( 4, "sll",  14,  2,   56 ),
    gen_rr_src1_dep_test( 3, "sll",  15,  3,  120 ),
    gen_rr_src1_dep_test( 2, "sll", -16,  1,  -32 ),
    gen_rr_src1_dep_test( 1, "sll", -17,  2,  -68 ),
    gen_rr_src1_dep_test( 0, "sll", -18,  3, -144 ),
  ]
#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sll",  19,  1,   38 ),
    gen_rr_srcs_dep_test( 4, "sll",  20,  2,   80 ),
    gen_rr_srcs_dep_test( 3, "sll",  21,  3,  168 ),
    gen_rr_srcs_dep_test( 2, "sll", -22,  1,  -44 ),
    gen_rr_srcs_dep_test( 1, "sll", -23,  3, -184 ),
    gen_rr_srcs_dep_test( 0, "sll", -24,  5, -768 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sll",  25, 1,   50 ),
    gen_rr_src1_eq_dest_test( "sll", -26, 3, -208 ),
    gen_rr_src0_eq_src1_test( "sll", 27, 0xd8000000 ),
    gen_rr_srcs_eq_dest_test( "sll", 28, 0xc0000000 ),
  ]
#-------------------------------------------------------------------------
# gen_value_test 
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "sll", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "sll", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rr_value_test( "sll", 0x00000f07, 0x00000003, 0x00007838 ),
    
    gen_rr_value_test( "sll", 0x00000f07, 0x00000010, 0x0f070000 ),
    gen_rr_value_test( "sll", 0x00000f07, 0x00000013, 0x78380000 ),
    gen_rr_value_test( "sll", 0x00000f07, 0x00000020, 0x00000f07 ),
    gen_rr_value_test( "sll", 0x00000f07, 0x00000021, 0x00001e0e ),
    gen_rr_value_test( "sll", 0x00000f07, 0xffffff21, 0x00001e0e ),
            
    gen_rr_value_test( "sll", 0x89000000, 0x00000005, 0x20000000 ),
    gen_rr_value_test( "sll", 0xf0f0f0f0, 0x00000015, 0x1e000000 ),
    gen_rr_value_test( "sll", 0xf0f0f0f0, 0x00000025, 0x1e1e1e00 ),       
    gen_rr_value_test( "sll", 0x89000000, 0xffff0005, 0x20000000 ),
    gen_rr_value_test( "sll", 0xf0f0f0f0, 0xffffff15, 0x1e000000 ),
    gen_rr_value_test( "sll", 0xf0f0f0f0, 0xffff0025, 0x1e1e1e00 ),  
  ]
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = src0 << src1[0:5]
    asm_code.append( gen_rr_value_test( "sll", src0.uint(), src1.uint(), dest.uint()) )
  return asm_code
