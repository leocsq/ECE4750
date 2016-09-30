#=========================================================================
# jal
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

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     # 0x0200
                        #
    nop                 # 0x0204
    nop                 # 0x0208
    nop                 # 0x020c
    nop                 # 0x0210
    nop                 # 0x0214
    nop                 # 0x0218
    nop                 # 0x021c
    nop                 # 0x0220
                        #
    jal   x1, label_a   # 0x0224
    addi  x3, x3, 0b01  # 0x0228

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

    # Check the link address
    csrw  proc2mngr, x1 > 0x0228 

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b10

  """
#-------------------------------------------------------------------------
# gen_nops_dep_taken_test
#-------------------------------------------------------------------------
def gen_nops_dep_taken_test():
  return [
   gen_jal_dest_dep_test( 0, 0, "jal", 0x0214),
   gen_jal_dest_dep_test( 1, 0, "jal", 0x0244),
   gen_jal_dest_dep_test( 1, 1, "jal", 0x0278),
   gen_jal_dest_dep_test( 2, 1, "jal", 0x02b0),
   gen_jal_dest_dep_test( 2, 2, "jal", 0x02ec),
   gen_jal_dest_dep_test( 3, 3, "jal", 0x032c),
  ]
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------


def gen_random_test():
  asm_code = []
  for i in xrange(25):
    src0  = Bits( 5, random.randint(0,0b11111))
    op = 532+i*48
    result = src0
    asm_code.append( gen_jal_value_test("jal", op ) )
  return asm_code

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def gen_src0_dep_taken_test():
  return [
   gen_jal_dest_dep_test( 8, "jal", 2, 0x0228, 0b10, 0b10),

  ]

