#=========================================================================
# lui
# load upper immediate
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
    lui x1, 0x0001
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 0x00001000
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
    gen_imm_dest_dep_test( 5, "lui",   0x00000003,  0x00003000),
    gen_imm_dest_dep_test( 4, "lui",   0x00003000,  0x03000000),
    gen_imm_dest_dep_test( 3, "lui",   0x00001234,  0x01234000),
    gen_imm_dest_dep_test( 2, "lui",   0x00034000,  0x34000000),
    gen_imm_dest_dep_test( 1, "lui",   0x00044321,  0x44321000),
    gen_imm_dest_dep_test( 0, "lui",   0x00021000,  0x21000000),
  ]

def gen_value_test():
  return [

    gen_imm_value_test( "lui", 0x00000101, 0x00101000 ),
    gen_imm_value_test( "lui", 0x00000001, 0x00001000 ),
    gen_imm_value_test( "lui", 0x00000003, 0x00003000 ),
    
    gen_imm_value_test( "lui", 0x00000010, 0x00010000 ),
    gen_imm_value_test( "lui", 0x00000013, 0x00013000 ),
    gen_imm_value_test( "lui", 0x00000020, 0x00020000 ),
    gen_imm_value_test( "lui", 0x00000021, 0x00021000 ),
    gen_imm_value_test( "lui", 0x000fff21, 0xfff21000 ),
            
    gen_imm_value_test( "lui", 0x00000005, 0x00005000 ),
    gen_imm_value_test( "lui", 0x00000015, 0x00015000 ),
    gen_imm_value_test( "lui", 0x00000025, 0x00025000 ),       
    gen_imm_value_test( "lui", 0x000f0005, 0xf0005000 ),
    gen_imm_value_test( "lui", 0x000fff15, 0xfff15000 ),
    gen_imm_value_test( "lui", 0x000f0025, 0xf0025000 ),  
  ]
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    imm = Bits( 20, random.randint(0,0xfffff) )
    dest = imm<<12
    asm_code.append( gen_imm_value_test( "lui", imm.uint(), dest.uint() ) )
  return asm_code
