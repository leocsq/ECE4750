#=========================================================================
# srli
#=========================================================================

import random

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
    srli x3, x1, 0x03
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
    gen_rimm_dest_dep_test( 5, "srli",   1,  1,  0 ),
    gen_rimm_dest_dep_test( 4, "srli",   2,  1,  1 ),
    gen_rimm_dest_dep_test( 3, "srli",   3,  1,  1 ),
    gen_rimm_dest_dep_test( 2, "srli",   4,  2,  1 ),
    gen_rimm_dest_dep_test( 1, "srli",   5,  2,  1 ),
    gen_rimm_dest_dep_test( 0, "srli",   6,  2,  1 ),
  ]
#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srli",   7,  1,   3 ),
    gen_rimm_src_dep_test( 4, "srli",   8,  2,   2 ),
    gen_rimm_src_dep_test( 3, "srli",   9,  3,   1 ),
    gen_rimm_src_dep_test( 2, "srli", -10, 20,4095 ),
    gen_rimm_src_dep_test( 1, "srli", -11, 24, 255 ),
    gen_rimm_src_dep_test( 0, "srli", -12, 26,  63 ),
  ]
#-------------------------------------------------------------------------
# gen_src_eq_dest_test
#-------------------------------------------------------------------------
def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test(  "srli",  25,  1,  12 ),
    gen_rimm_src_eq_dest_test(  "srli", -26,  3,  536870908 ),
    ##gen_rimm_src_eq_dest_test(  "srli", -15,  1,  -8 ),
    ##gen_rimm_src_eq_dest_test(  "srai", -16,  2,  -4 ),
    ##gen_rimm_src_eq_dest_test(  "srai",  17,  2,   4 ),
    ##gen_rimm_src_eq_dest_test(  "srai", -18,  2,  -5 ),
  ]
#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rimm_value_test( "srli", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rimm_value_test( "srli", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rimm_value_test( "srli", 0x00000007, 0x00000002, 0x00000001 ),
    
    gen_rimm_value_test( "srli", 0x000f0f0f, 0x00000004, 0x0000f0f0 ),
    gen_rimm_value_test( "srli", 0x000f0f0f, 0x00000010, 0x0000000f ),
    gen_rimm_value_test( "srli", 0x000f0f0f, 0x00000011, 0x00000007 ),
    
  ]
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src = Bits( 32, random.randint(0,0xffffffff) )
    imm = Bits( 5,  random.randint(0,0b11111) )
    dest = src>>imm
    asm_code.append( gen_rimm_value_test( "srli", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code
