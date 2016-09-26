#=========================================================================
# sw
# - Summary   : Store word into memory
# - Assembly  : sw rs2, imm(rs1)
# - Semantics : M_4B[ R[rs1] + sext(imm) ] = R[rs2]
# - Format    : S-type, S-immediate
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
    csrr x1, mngr2proc < 0x00002000
    csrr x2, mngr2proc < 0xdeadbeef
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sw   x2, 0(x1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lw   x3, 0(x1)
    csrw proc2mngr, x3 > 0xdeadbeef

    .data
    .word 0x01020304
  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [

    #gen_ld_dest_dep_test( 5, "sw", 0x2000, 0x00010203,),
    gen_ld_dest_dep_test( 5, "sw", 0x00010203, 0x2000 ),
    #gen_ld_dest_dep_test( 4, "sw", 0x2004, 0x04050607 ),
    #gen_ld_dest_dep_test( 3, "sw", 0x2008, 0x08090a0b ),
    #gen_ld_dest_dep_test( 2, "sw", 0x200c, 0x0c0d0e0f ),
    #gen_ld_dest_dep_test( 1, "sw", 0x2010, 0x10111213 ),
    #gen_ld_dest_dep_test( 0, "sw", 0x2014, 0x14151617 ),

    gen_word_data([
      0x00010203
     # 0x04050607,
     # 0x08090a0b,
     # 0x0c0d0e0f,
     # 0x10111213,
     # 0x14151617,
    ])

  ]
