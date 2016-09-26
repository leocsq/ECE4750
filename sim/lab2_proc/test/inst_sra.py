#=========================================================================
# sra
# - Summary   : Shift right arithmetic by register value (sign-extend)
# - Assembly  : sra rd, rs1, rs2
# - Semantics : R[rd] = R[rs1] >>> R[rs2][4:0]
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
    sra x3, x1, x2
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
    gen_rr_dest_dep_test( 5, "sra",   1,  1,  0 ),
    gen_rr_dest_dep_test( 4, "sra",   2,  1,  1 ),
    gen_rr_dest_dep_test( 3, "sra",  -3,  1, -2 ),
    gen_rr_dest_dep_test( 2, "sra",  -4,  2, -1 ),
    gen_rr_dest_dep_test( 1, "sra",   5,  2,  1 ),
    gen_rr_dest_dep_test( 0, "sra",  -6,  2, -2 ),
  ]
#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sra",   7,  1,   3 ),
    gen_rr_src0_dep_test( 4, "sra",   8,  1,   4 ),
    gen_rr_src0_dep_test( 3, "sra",  -9,  1,  -5 ),
    gen_rr_src0_dep_test( 2, "sra", -10,  2,  -3 ),
    gen_rr_src0_dep_test( 1, "sra",  11,  2,   2 ),
    gen_rr_src0_dep_test( 0, "sra", -12,  2,  -3 ),
  ]
#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sra",  13,  1,   6 ),
    gen_rr_src1_dep_test( 4, "sra",  14,  1,   7 ),
    gen_rr_src1_dep_test( 3, "sra", -15,  1,  -8 ),
    gen_rr_src1_dep_test( 2, "sra", -16,  2,  -4 ),
    gen_rr_src1_dep_test( 1, "sra",  17,  2,   4 ),
    gen_rr_src1_dep_test( 0, "sra", -18,  2,  -5 ),
  ]
#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sra",  19,  1,   9 ),
    gen_rr_srcs_dep_test( 4, "sra",  20,  1,  10 ),
    gen_rr_srcs_dep_test( 3, "sra", -21,  1, -11 ),
    gen_rr_srcs_dep_test( 2, "sra", -22,  2,  -6 ),
    gen_rr_srcs_dep_test( 1, "sra",  23,  2,   5 ),
    gen_rr_srcs_dep_test( 0, "sra", -24,  2,  -6 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sra",  25, 1, 12 ),
    gen_rr_src1_eq_dest_test( "sra", -26, 1,-13 ),
    gen_rr_src0_eq_src1_test( "sra", 27, 0 ),
    gen_rr_srcs_eq_dest_test( "sra", 28, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test // imcomplete
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "sra", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rr_value_test( "sra", 0x00000001, 0x00004001, 0x00000000 ),
    gen_rr_value_test( "sra", 0x00000007, 0x00000003, 0x00000000 ),
    
    gen_rr_value_test( "sra", 0x00010000, 0x00000004, 0x00001000 ),
    gen_rr_value_test( "sra", 0x80000000, 0x00000005, 0xfc000000 ),
    gen_rr_value_test( "sra", 0x89000000, 0x00000038, 0xffffff89 ),

    gen_rr_value_test( "sra", 0x80000000, 0x00007fff, 0xffffffff ),
    gen_rr_value_test( "sra", 0x7fffffff, 0xffff8000, 0x7fffffff ), 
       
    gen_rr_value_test( "sra", 0x00000000, 0xffffffff, 0x00000000 ),
    gen_rr_value_test( "sra", 0xfffffffb, 0x00000021, 0xfffffffd ),
    gen_rr_value_test( "sra", 0xffffffff, 0xffffffff, 0xffffffff ),    
  ]

#-------------------------------------------------------------------------
# gen_random_test//***
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0b11111) ) 
    stemp = src1
    if src0[31]==0:
      dest = src0>>stemp
    else:
      temp = src0>>stemp
      temp1 = ~temp
      temp2 = temp1 + temp
      temp1 = temp1>>stemp
      dest = temp2-temp1
    asm_code.append( gen_rr_value_test( "sra", src0.uint(), src1.uint(), dest.uint()) )
  return asm_code

