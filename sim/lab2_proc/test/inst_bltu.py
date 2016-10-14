#=========================================================================
# bltu
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    # Use x3 to track the control flow pattern
    addi  x3, x0, 0

    csrr  x1, mngr2proc < 2
    csrr  x2, mngr2proc < 1

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # This branch should be taken
    bltu   x2, x1, label_a
    addi  x3, x3, 0b01

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

  label_a:
    addi  x3, x3, 0b10

    # Only the second bit should be set if branch was taken
    csrw proc2mngr, x3 > 0b10

  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# gen_src0_dep_taken_test
#-------------------------------------------------------------------------

def gen_src0_dep_taken_test():
  return [
    gen_br2_src0_dep_test( 5, "bltu", 1, 2, True ),
    gen_br2_src0_dep_test( 4, "bltu", 2, 3, True ),
    gen_br2_src0_dep_test( 3, "bltu", 3, 4, True ),
    gen_br2_src0_dep_test( 2, "bltu", 4, 5, True ),
    gen_br2_src0_dep_test( 1, "bltu", 5, 6, True ),
    gen_br2_src0_dep_test( 0, "bltu", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "bltu", 1, 1, False ),
    gen_br2_src0_dep_test( 4, "bltu", 2, 2, False ),
    gen_br2_src0_dep_test( 3, "bltu", 3, 3, False ),
    gen_br2_src0_dep_test( 2, "bltu", 4, 4, False ),
    gen_br2_src0_dep_test( 1, "bltu", 5, 5, False ),
    gen_br2_src0_dep_test( 0, "bltu", 6, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu", 1, 2, True ),
    gen_br2_src1_dep_test( 4, "bltu", 2, 3, True ),
    gen_br2_src1_dep_test( 3, "bltu", 3, 4, True ),
    gen_br2_src1_dep_test( 2, "bltu", 4, 5, True ),
    gen_br2_src1_dep_test( 1, "bltu", 5, 6, True ),
    gen_br2_src1_dep_test( 0, "bltu", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu", 1, 1, False ),
    gen_br2_src1_dep_test( 4, "bltu", 2, 2, False ),
    gen_br2_src1_dep_test( 3, "bltu", 3, 3, False ),
    gen_br2_src1_dep_test( 2, "bltu", 4, 4, False ),
    gen_br2_src1_dep_test( 1, "bltu", 5, 5, False ),
    gen_br2_src1_dep_test( 0, "bltu", 6, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu", 1, 2, True ),
    gen_br2_srcs_dep_test( 4, "bltu", 2, 3, True ),
    gen_br2_srcs_dep_test( 3, "bltu", 3, 4, True ),
    gen_br2_srcs_dep_test( 2, "bltu", 4, 5, True ),
    gen_br2_srcs_dep_test( 1, "bltu", 5, 6, True ),
    gen_br2_srcs_dep_test( 0, "bltu", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu", 1, 1, False ),
    gen_br2_srcs_dep_test( 4, "bltu", 2, 2, False ),
    gen_br2_srcs_dep_test( 3, "bltu", 3, 3, False ),
    gen_br2_srcs_dep_test( 2, "bltu", 4, 4, False ),
    gen_br2_srcs_dep_test( 1, "bltu", 5, 5, False ),
    gen_br2_srcs_dep_test( 0, "bltu", 6, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "bltu", 1, False ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_br2_value_test( "bltu", -1, -1, False ),
    gen_br2_value_test( "bltu", -1,  0, False  ),
    gen_br2_value_test( "bltu", -1,  1, False  ),

    gen_br2_value_test( "bltu",  0, -1, True  ),
    gen_br2_value_test( "bltu",  0,  0, False ),
    gen_br2_value_test( "bltu",  0,  1, True  ),

    gen_br2_value_test( "bltu",  1, -1, True  ),
    gen_br2_value_test( "bltu",  1,  0, False ),
    gen_br2_value_test( "bltu",  1,  1, False ),

    gen_br2_value_test( "bltu", 0xfffffff7, 0xfffffff7, False ),
    gen_br2_value_test( "bltu", 0x7fff000e, 0x7fff000f, True  ),
    gen_br2_value_test( "bltu", 0xfffffffe, 0xfffffff7, False ),
    gen_br2_value_test( "bltu", 0xfffffff7, 0x7fffffff, False ),
    gen_br2_value_test( "bltu", 0x7fffffff, 0xfffffff7, True  ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(25):
    src0  = Bits( 32, random.randint(0,0xffffffff) )
    src1  = Bits( 32, random.randint(0,0xffffffff) )
    taken = (src0<src1)
    asm_code.append( gen_br2_value_test( "bltu", src0.uint(), src1.uint(), taken ) )
  return asm_code
