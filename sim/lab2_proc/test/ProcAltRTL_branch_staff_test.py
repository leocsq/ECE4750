#=========================================================================
# ProcAltRTL_branch_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness_staff import *
from lab2_proc.ProcAltRTL import ProcAltRTL

#-------------------------------------------------------------------------
# beq
#-------------------------------------------------------------------------

import inst_staff_beq

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_beq.gen_basic_test ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_beq.gen_src0_dep_taken_test    ) ,
  asm_test( inst_staff_beq.gen_src0_dep_nottaken_test ) ,
  asm_test( inst_staff_beq.gen_src1_dep_taken_test    ) ,
  asm_test( inst_staff_beq.gen_src1_dep_nottaken_test ) ,
  asm_test( inst_staff_beq.gen_srcs_dep_taken_test    ) ,
  asm_test( inst_staff_beq.gen_srcs_dep_nottaken_test ) ,
  asm_test( inst_staff_beq.gen_src0_eq_src1_test      ) ,
  asm_test( inst_staff_beq.gen_value_test             ) ,
  asm_test( inst_staff_beq.gen_random_test            ) ,

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_beq( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_beq_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_beq.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3)

#-------------------------------------------------------------------------
# bne
#-------------------------------------------------------------------------

import inst_staff_bne

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_bne.gen_basic_test             ),
  asm_test( inst_staff_bne.gen_src0_dep_taken_test    ),
  asm_test( inst_staff_bne.gen_src0_dep_nottaken_test ),
  asm_test( inst_staff_bne.gen_src1_dep_taken_test    ),
  asm_test( inst_staff_bne.gen_src1_dep_nottaken_test ),
  asm_test( inst_staff_bne.gen_srcs_dep_taken_test    ),
  asm_test( inst_staff_bne.gen_srcs_dep_nottaken_test ),
  asm_test( inst_staff_bne.gen_src0_eq_src1_test      ),
  asm_test( inst_staff_bne.gen_value_test             ),
  asm_test( inst_staff_bne.gen_random_test            ),
])
def test_bne( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_bne_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_bne.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3)

#-------------------------------------------------------------------------
# bge
#-------------------------------------------------------------------------

import inst_staff_bge

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_bge.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_bge.gen_src0_dep_taken_test    ),
  asm_test( inst_staff_bge.gen_src0_dep_nottaken_test ),
  asm_test( inst_staff_bge.gen_src1_dep_taken_test    ),
  asm_test( inst_staff_bge.gen_src1_dep_nottaken_test ),
  asm_test( inst_staff_bge.gen_srcs_dep_taken_test    ),
  asm_test( inst_staff_bge.gen_srcs_dep_nottaken_test ),
  asm_test( inst_staff_bge.gen_src0_eq_src1_test      ),
  asm_test( inst_staff_bge.gen_value_test             ),
  asm_test( inst_staff_bge.gen_random_test            ),

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_bge( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_bge_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_bge.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3)

#-------------------------------------------------------------------------
# bgeu
#-------------------------------------------------------------------------

import inst_staff_bgeu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_bgeu.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_bgeu.gen_src0_dep_taken_test    ),
  asm_test( inst_staff_bgeu.gen_src0_dep_nottaken_test ),
  asm_test( inst_staff_bgeu.gen_src1_dep_taken_test    ),
  asm_test( inst_staff_bgeu.gen_src1_dep_nottaken_test ),
  asm_test( inst_staff_bgeu.gen_srcs_dep_taken_test    ),
  asm_test( inst_staff_bgeu.gen_srcs_dep_nottaken_test ),
  asm_test( inst_staff_bgeu.gen_src0_eq_src1_test      ),
  asm_test( inst_staff_bgeu.gen_value_test             ),
  asm_test( inst_staff_bgeu.gen_random_test            ),

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_bgeu( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_bgeu_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_bgeu.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3)

#-------------------------------------------------------------------------
# blt
#-------------------------------------------------------------------------

import inst_staff_blt

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_blt.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_blt.gen_src0_dep_taken_test    ),
  asm_test( inst_staff_blt.gen_src0_dep_nottaken_test ),
  asm_test( inst_staff_blt.gen_src1_dep_taken_test    ),
  asm_test( inst_staff_blt.gen_src1_dep_nottaken_test ),
  asm_test( inst_staff_blt.gen_srcs_dep_taken_test    ),
  asm_test( inst_staff_blt.gen_srcs_dep_nottaken_test ),
  asm_test( inst_staff_blt.gen_src0_eq_src1_test      ),
  asm_test( inst_staff_blt.gen_value_test             ),
  asm_test( inst_staff_blt.gen_random_test            ),

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_blt( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_blt_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_blt.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3)

#-------------------------------------------------------------------------
# bltu
#-------------------------------------------------------------------------

import inst_staff_bltu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_bltu.gen_basic_test             ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_bltu.gen_src0_dep_taken_test    ),
  asm_test( inst_staff_bltu.gen_src0_dep_nottaken_test ),
  asm_test( inst_staff_bltu.gen_src1_dep_taken_test    ),
  asm_test( inst_staff_bltu.gen_src1_dep_nottaken_test ),
  asm_test( inst_staff_bltu.gen_srcs_dep_taken_test    ),
  asm_test( inst_staff_bltu.gen_srcs_dep_nottaken_test ),
  asm_test( inst_staff_bltu.gen_src0_eq_src1_test      ),
  asm_test( inst_staff_bltu.gen_value_test             ),
  asm_test( inst_staff_bltu.gen_random_test            ),

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_bltu( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_bltu_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_bltu.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3)
