#=========================================================================
# slli
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 0x80008000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slli x3, x1, 0x03
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
    gen_rimm_dest_dep_test( 5, "slli",   1,  1,  2 ),
    gen_rimm_dest_dep_test( 4, "slli",   2,  1,  4 ),
    gen_rimm_dest_dep_test( 3, "slli",  -3,  1, -6 ),
    gen_rimm_dest_dep_test( 2, "slli",  -4,  2,-16 ),
    gen_rimm_dest_dep_test( 1, "slli",   5,  3, 40 ),
    gen_rimm_dest_dep_test( 0, "slli",  -6,  3,-48 ),
  ]
#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slli",   7,  1,  14 ),
    gen_rimm_src_dep_test( 4, "slli",   8,  2,  32 ),
    gen_rimm_src_dep_test( 3, "slli",   9,  3,  72 ),
    gen_rimm_src_dep_test( 2, "slli", -10,  1, -20 ),
    gen_rimm_src_dep_test( 1, "slli", -11,  2, -44 ),
    gen_rimm_src_dep_test( 0, "slli", -12,  3, -96 ),
  ]
#-------------------------------------------------------------------------
# gen_src_eq_dest_test
#-------------------------------------------------------------------------
def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test(  "slli",  25, 1,   50 ),
    gen_rimm_src_eq_dest_test(  "slli", -26, 3, -208 ),
    gen_rimm_src_eq_dest_test(  "srli", -15,  1,  2147483640 ),
    gen_rimm_src_eq_dest_test(  "srli", -16,  2,  1073741820 ),
    gen_rimm_src_eq_dest_test(  "srli",  17,  2,  4 ),
    gen_rimm_src_eq_dest_test(  "srli", -18,  2,  1073741819 ),
  ]
#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rimm_value_test( "slli", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rimm_value_test( "slli", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rimm_value_test( "slli", 0x00000f07, 0x00000003, 0x00007838 ),
    gen_rimm_value_test( "slli", 0x00000f07, 0x00000010, 0x0f070000 ),
    gen_rimm_value_test( "slli", 0x00000f07, 0x00000013, 0x78380000 ),
  ]
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src = Bits( 32, random.randint(0,0xffffffff) )
    imm = Bits( 5,  random.randint(0,0b11111) )
    dest = src<<imm
    asm_code.append( gen_rimm_value_test( "slli", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code
