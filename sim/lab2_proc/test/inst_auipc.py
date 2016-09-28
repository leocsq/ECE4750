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
#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------
def gen_dest_dep_test():
  return [
    gen_imm_dest_dep_test( 5, "auipc",   0x00000003,  0x00003000 + 0x200 + 0*4 ),
    gen_imm_dest_dep_test( 4, "auipc",   0x00003000,  0x03000000 + 0x200 + 7*4 ),
    gen_imm_dest_dep_test( 3, "auipc",   0x00001234,  0x01234000 + 0x200 + 13*4 ),
    gen_imm_dest_dep_test( 2, "auipc",   0x00034000,  0x34000000 + 0x200 + 18*4 ),
    gen_imm_dest_dep_test( 1, "auipc",   0x00044321,  0x44321000 + 0x200 + 22*4 ),
    gen_imm_dest_dep_test( 0, "auipc",   0x00021000,  0x21000000 + 0x200 + 25*4 ),
  ]

def gen_value_test():
  return [

    gen_imm_value_test( "auipc", 0x00000101, 0x00101000 + 0x200 + 0*4 ),
    gen_imm_value_test( "auipc", 0x00000001, 0x00001000 + 0x200 + 2*4 ),
    gen_imm_value_test( "auipc", 0x00000003, 0x00003000 + 0x200 + 4*4 ),
    
    gen_imm_value_test( "auipc", 0x00000010, 0x00010000 + 0x200 + 6*4 ),
    gen_imm_value_test( "auipc", 0x00000013, 0x00013000 + 0x200 + 8*4 ),
    gen_imm_value_test( "auipc", 0x00000020, 0x00020000 + 0x200 + 10*4 ),
    gen_imm_value_test( "auipc", 0x00000021, 0x00021000 + 0x200 + 12*4 ),
    gen_imm_value_test( "auipc", 0x000fff21, 0xfff21000 + 0x200 + 14*4 ),
            
    gen_imm_value_test( "auipc", 0x00000005, 0x00005000 + 0x200 + 16*4 ),
    gen_imm_value_test( "auipc", 0x00000015, 0x00015000 + 0x200 + 18*4 ),
    gen_imm_value_test( "auipc", 0x00000025, 0x00025000 + 0x200 + 20*4 ),       
    gen_imm_value_test( "auipc", 0x000f0005, 0xf0005000 + 0x200 + 22*4 ),
    gen_imm_value_test( "auipc", 0x000fff15, 0xfff15000 + 0x200 + 24*4 ),
    gen_imm_value_test( "auipc", 0x000f0025, 0xf0025000 + 0x200 + 26*4 ),  
  ]
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    imm = Bits( 20, random.randint(0,0xfffff) )
    dest = ((sext(imm, 32)<<12) + 0x200)
  asm_code.append( gen_imm_value_test( "auipc", imm.uint(), dest.uint() ) )
  return asm_code

