#=========================================================================
# ProcBaseRTL_branch_test.py
#=========================================================================

import pytest
import random

from pymtl   import *
from harness import *
from lab2_proc.ProcBaseRTL import ProcBaseRTL

#-------------------------------------------------------------------------
# beq
#-------------------------------------------------------------------------

import inst_beq

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_beq.gen_basic_test ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_beq( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# bne
#-------------------------------------------------------------------------

import inst_bne

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bne.gen_basic_test             ),
  asm_test( inst_bne.gen_src0_dep_taken_test    ),
  asm_test( inst_bne.gen_src0_dep_nottaken_test ),
  asm_test( inst_bne.gen_src1_dep_taken_test    ),
  asm_test( inst_bne.gen_src1_dep_nottaken_test ),
  asm_test( inst_bne.gen_srcs_dep_taken_test    ),
  asm_test( inst_bne.gen_srcs_dep_nottaken_test ),
  asm_test( inst_bne.gen_src0_eq_src1_test      ),
  asm_test( inst_bne.gen_value_test             ),
  asm_test( inst_bne.gen_random_test            ),
])
def test_bne( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_bne_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_bne.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3)

#-------------------------------------------------------------------------
# bge
#-------------------------------------------------------------------------

import inst_bge

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bge.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_bge( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# bgeu
#-------------------------------------------------------------------------

import inst_bgeu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bgeu.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_bgeu( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# blt
#-------------------------------------------------------------------------

import inst_blt

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_blt.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_blt( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#-------------------------------------------------------------------------
# bltu
#-------------------------------------------------------------------------

import inst_bltu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bltu.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_bltu( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

# ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# random stall and delay
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
