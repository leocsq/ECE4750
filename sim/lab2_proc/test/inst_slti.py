#=========================================================================
# slti
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slti x3, x1, 6
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
# gen_dest_dep_test
#-------------------------------------------------------------------------
def gen_dest_dep_test():
  return [
    gen_rimm_dest_dep_test( 5, "slti",   1,  1,  0 ),
    gen_rimm_dest_dep_test( 4, "slti",   2, -1,  0 ),
    gen_rimm_dest_dep_test( 3, "slti",  -3,  1,  1 ),
    gen_rimm_dest_dep_test( 2, "slti",  -4, -1,  1 ),
    gen_rimm_dest_dep_test( 1, "slti",   5,  1,  0 ),
    gen_rimm_dest_dep_test( 0, "slti",   1,  5,  1 ),
  ]
#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slti",   7,  1,   0 ),
    gen_rimm_src_dep_test( 4, "slti",   8, -1,   0 ),
    gen_rimm_src_dep_test( 3, "slti",  -9,  1,   1 ),
    gen_rimm_src_dep_test( 2, "slti", -10, -1,   1 ),
    gen_rimm_src_dep_test( 1, "slti",  11,  1,   0 ),
    gen_rimm_src_dep_test( 0, "slti",  12,  1,   0 ),
  ]
#-------------------------------------------------------------------------
# gen_src_eq_dest_test
#-------------------------------------------------------------------------
def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test(  "slti",   7,  1,   0 ),
    gen_rimm_src_eq_dest_test(  "slti",   8, -1,   0 ),
    gen_rimm_src_eq_dest_test(  "slti",  -9,  1,   1 ),
    gen_rimm_src_eq_dest_test(  "slti", -10, -1,   1 ),
    gen_rimm_src_eq_dest_test(  "slti",  11,  1,   0 ),
    gen_rimm_src_eq_dest_test(  "slti",  12,  1,   0 ),
  ]
#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rimm_value_test( "slti", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rimm_value_test( "slti", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rimm_value_test( "slti", 0x00000003, 0x00000007, 0x00000001 ),

    gen_rimm_value_test( "slti", 0x00000000, 0xffff8000, 0x00000000 ),
    gen_rimm_value_test( "slti", 0x80000000, 0x00000000, 0x00000000 ),
    gen_rimm_value_test( "slti", 0x80000000, 0xffff8000, 0x00000000 ),

    gen_rimm_value_test( "slti", 0x00000000, 0x00007fff, 0x00000001 ),
    gen_rimm_value_test( "slti", 0x7fffffff, 0x00000000, 0x7fffffff ),
    gen_rimm_value_test( "slti", 0x7fffffff, 0x00007fff, 0x80007ffe ),

    gen_rimm_value_test( "slti", 0x80000000, 0x00007fff, 0x80007fff ),
    gen_rimm_value_test( "slti", 0x7fffffff, 0xffff8000, 0x7fff7fff ),

    gen_rimm_value_test( "slti", 0x00000000, 0xffffffff, 0xffffffff ),
    gen_rimm_value_test( "slti", 0xffffffff, 0x00000001, 0x00000000 ),
    gen_rimm_value_test( "slti", 0xffffffff, 0xffffffff, 0xfffffffe ),

  ]
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src = Bits( 32, random.randint(0,0xffffffff) )
    imm = Bits( 32, random.randint(0,0xffffffff) )
    temp = src[31]^~sext(imm,32) 
    if (temp>0):
      if (src<imm):
        dest = Bits( 32, 1 )
      else:
       dest = Bits( 32, 0 )
    else:
     if (src[31]>0):
      dest = Bits( 32, 1 )
    else:
      dest = Bits( 32, 0 )
    asm_code.append( gen_rimm_value_test( "slti", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code
