#=========================================================================
# sltiu
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
    sltiu x3, x1, 6
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
    gen_rimm_dest_dep_test( 5, "sltiu",   1,  1,  0 ),
    gen_rimm_dest_dep_test( 4, "sltiu",   2, -1,  0 ),
    gen_rimm_dest_dep_test( 3, "sltiu",  -3,  1,  1 ),
    gen_rimm_dest_dep_test( 2, "sltiu",  -4, -1,  1 ),
    gen_rimm_dest_dep_test( 1, "sltiu",   5,  1,  0 ),
    gen_rimm_dest_dep_test( 0, "sltiu",   1,  5,  1 ),
  ]
#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "sltiu",   7,  1,   0 ),
    gen_rimm_src_dep_test( 4, "sltiu",   8, -1,   0 ),
    gen_rimm_src_dep_test( 3, "sltiu",  -9,  1,   1 ),
    gen_rimm_src_dep_test( 2, "sltiu", -10, -1,   1 ),
    gen_rimm_src_dep_test( 1, "sltiu",  11,  1,   0 ),
    gen_rimm_src_dep_test( 0, "sltiu",  12,  1,   0 ),
  ]
#-------------------------------------------------------------------------
# gen_src_eq_dest_test
#-------------------------------------------------------------------------
def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test(  "sltiu",   7,  1,   0 ),
    gen_rimm_src_eq_dest_test(  "sltiu",   8, -1,   0 ),
    gen_rimm_src_eq_dest_test(  "sltiu",  -9,  1,   1 ),
    gen_rimm_src_eq_dest_test(  "sltiu", -10, -1,   1 ),
    gen_rimm_src_eq_dest_test(  "sltiu",  11,  1,   0 ),
    gen_rimm_src_eq_dest_test(  "sltiu",  12,  1,   0 ),
  ]
#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rimm_value_test( "sltiu", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0x00000003, 0x00000007, 0x00000001 ),

    gen_rimm_value_test( "sltiu", 0x00000000, 0xffff8000, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0x80000000, 0x00000000, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0x80000000, 0xffff8000, 0x00000000 ),

    gen_rimm_value_test( "sltiu", 0x00000000, 0x00007fff, 0x00000001 ),
    gen_rimm_value_test( "sltiu", 0x7fffffff, 0x00000000, 0x7fffffff ),
    gen_rimm_value_test( "sltiu", 0x7fffffff, 0x00007fff, 0x80007ffe ),

    gen_rimm_value_test( "sltiu", 0x80000000, 0x00007fff, 0x80007fff ),
    gen_rimm_value_test( "sltiu", 0x7fffffff, 0xffff8000, 0x7fff7fff ),

    gen_rimm_value_test( "sltiu", 0x00000000, 0xffffffff, 0xffffffff ),
    gen_rimm_value_test( "sltiu", 0xffffffff, 0x00000001, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0xffffffff, 0xffffffff, 0xfffffffe ),

  ]
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src = Bits( 32, random.randint(0,0xffffffff) )
    imm = Bits( 32, random.randint(0,0xffffffff) )
    if src<imm:
     dest = Bits( 32, 1 )
    else:
     dest = Bits( 32, 0 )
    asm_code.append( gen_rimm_value_test( "sltiu", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code