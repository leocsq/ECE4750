#=========================================================================
# jalr
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0           # 0x0200
                              #
    lui x1,      %hi[label_a] # 0x0204
    addi x1, x1, %lo[label_a] # 0x0208
                              #
    nop                       # 0x020c
    nop                       # 0x0210
    nop                       # 0x0214
    nop                       # 0x0218
    nop                       # 0x021c
    nop                       # 0x0220
    nop                       # 0x0224
    nop                       # 0x0228
                              #
    jalr  x31, x1, 0          # 0x022c
    addi  x3, x3, 0b01        # 0x0230

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
    csrw  proc2mngr, x31 > 0x0230

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3  > 0b10

  """

#-------------------------------------------------------------------------
# gen_nops_dep_taken_test
#-------------------------------------------------------------------------
def gen_nops_dep_taken_test():
  return [
   gen_jalr_dest_dep_test( 0, 0, "jalr", 0x224 ),
   gen_jalr_dest_dep_test( 1, 0, "jalr", 0x26c ),
   gen_jalr_dest_dep_test( 1, 1, "jalr", 0x2b8 ),
   gen_jalr_dest_dep_test( 2, 1, "jalr", 0x308 ),
   gen_jalr_dest_dep_test( 2, 2, "jalr", 0x35c ),
  ]

def gen_random_test():
  asm_code = []
  for i in xrange(21):
    #src0  = Bits( 5, ra28ndom.randint(0,0b11111))
    op = 548+i*72
    #result = src0
    asm_code.append( gen_jalr_value_test("jalr", op) )
  return asm_code
