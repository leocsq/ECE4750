#=========================================================================
# auipc
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
    auipc x1, 0x00010                       # PC=0x200
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00010200
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
