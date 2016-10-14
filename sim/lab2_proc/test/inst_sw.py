#=========================================================================
# sw
# - Summary   : Store word into memory
# - Assembly  : sw rs2, imm(rs1)
# - Semantics : M_4B[ R[rs1] + sext(imm) ] = R[rs2]
# - Format    : S-type, S-immediate
#=========================================================================

import random

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

  #  gen_sd_dest_dep_test( 5, "sw", 0x2000, 0x00010203, 0x00010203 ),
  #  gen_sd_dest_dep_test( 4, "sw", 0x2004, 0x04050607, 0x04050607 ),
  #  gen_sd_dest_dep_test( 3, "sw", 0x2008, 0x08090a0b, 0x08090a0b ),
  #  gen_sd_dest_dep_test( 2, "sw", 0x200c, 0x0c0d0e0f, 0x0c0d0e0f ),
  #  gen_sd_dest_dep_test( 1, "sw", 0x2010, 0x10111213, 0x10111213 ),
    gen_sd_dest_dep_test( 0, "sw", 0x2014, 0x14151617, 0x14151617 ),

    gen_word_data([
      0x00010202,
      0x04050688,
      0x08090adb,
      0x0c0d0eef,
      0x10111543,
      0x14127937,
    ])

  ]
#-------------------------------------------------------------------------
# gen_sword_dep_test
#-------------------------------------------------------------------------

def gen_sword_dep_test():
  return [

    gen_sd_sword_dep_test( 5, "sw", 0x2000, 0x00010203, 0x00010203 ),
    gen_sd_sword_dep_test( 4, "sw", 0x2004, 0x04050607, 0x04050607 ),
    gen_sd_sword_dep_test( 3, "sw", 0x2008, 0x08090a0b, 0x08090a0b ),
    gen_sd_sword_dep_test( 2, "sw", 0x200c, 0x0c0d0e0f, 0x0c0d0e0f ),
    gen_sd_sword_dep_test( 1, "sw", 0x2010, 0x10111213, 0x10111213 ),
    gen_sd_sword_dep_test( 0, "sw", 0x2014, 0x14151617, 0x14151617 ),

    gen_word_data([
      0x00010203,
      0x040d0607,
      0x08390a0b,
      0x0ccd0e0f,
      0x12111213,
      0x10051617,
    ])

  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_sd_sword_eq_dest_test( "sw", 0x2000, 0x01020304, 0x01020304 ),
    gen_word_data([ 0x01029304 ])
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    # Test positive offsets

    gen_sd_value_test( "sw",   0, 0x00002000, 0xdeadbeef, 0xdeadbeef ),
    gen_sd_value_test( "sw",   4, 0x00002000, 0x00010203, 0x00010203 ),
    gen_sd_value_test( "sw",   8, 0x00002000, 0x04050607, 0x04050607 ),
    gen_sd_value_test( "sw",  12, 0x00002000, 0x08090a0b, 0x08090a0b ),
    gen_sd_value_test( "sw",  16, 0x00002000, 0x0c0d0e0f, 0x0c0d0e0f ),
    gen_sd_value_test( "sw",  20, 0x00002000, 0xcafecafe, 0xcafecafe ),

    # Test negative offsets

    gen_sd_value_test( "sw", -20, 0x00002014, 0xdeadbeef, 0xdeadbeef ),
    gen_sd_value_test( "sw", -16, 0x00002014, 0x00010203, 0x00010203 ),
    gen_sd_value_test( "sw", -12, 0x00002014, 0x04050607, 0x04050607 ),
    gen_sd_value_test( "sw",  -8, 0x00002014, 0x08090a0b, 0x08090a0b ),
    gen_sd_value_test( "sw",  -4, 0x00002014, 0x0c0d0e0f, 0x0c0d0e0f ),
    gen_sd_value_test( "sw",   0, 0x00002014, 0xcafecafe, 0xcafecafe ),

    # Test positive offset with unaligned base

    gen_sd_value_test( "sw",   1, 0x00001fff, 0xdeadbeef, 0xdeadbeef ),
    gen_sd_value_test( "sw",   5, 0x00001fff, 0x00010203, 0x00010203 ),
    gen_sd_value_test( "sw",   9, 0x00001fff, 0x04050607, 0x04050607 ),
    gen_sd_value_test( "sw",  13, 0x00001fff, 0x08090a0b, 0x08090a0b ),
    gen_sd_value_test( "sw",  17, 0x00001fff, 0x0c0d0e0f, 0x0c0d0e0f ),
    gen_sd_value_test( "sw",  21, 0x00001fff, 0xcafecafe, 0xcafecafe ),

    # Test negative offset with unaligned base

    gen_sd_value_test( "sw", -21, 0x00002015, 0xdeadbeef, 0xdeadbeef ),
    gen_sd_value_test( "sw", -17, 0x00002015, 0x00010203, 0x00010203 ),
    gen_sd_value_test( "sw", -13, 0x00002015, 0x04050607, 0x04050607 ),
    gen_sd_value_test( "sw",  -9, 0x00002015, 0x08090a0b, 0x08090a0b ),
    gen_sd_value_test( "sw",  -5, 0x00002015, 0x0c0d0e0f, 0x0c0d0e0f ),
    gen_sd_value_test( "sw",  -1, 0x00002015, 0xcafecafe, 0xcafecafe ),

    gen_word_data([
      0xdeedbeef,
      0xfff10203,
      0xfdf50607,
      0x12090a0b,
      0x000d0e0f,
      0x99fecafe,
    ])

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():

  # Generate some random data

  data = []
  for i in xrange(128):
    data.append( random.randint(0,0xffffffff) )
  # Generate random accesses to this data

  asm_code = []
  for i in xrange(100):

    a = random.randint(0,127)
    b = random.randint(0,127)
    	
    base   = Bits( 32, 0x2000 + (4*b) )
    offset = Bits( 16, (4*(a - b)) )    
    sword  = Bits( 32, random.randint(0,0xffffffff))
    result = sword.uint()

    asm_code.append( gen_sd_value_test( "sw", offset.int(), base.uint(), sword.uint(), result ) )

  # Add the data to the end of the assembly code

  asm_code.append( gen_word_data( data ) )
  return asm_code

