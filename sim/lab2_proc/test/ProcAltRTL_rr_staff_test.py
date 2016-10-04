#=========================================================================
# ProcAltRTL_alu_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness_staff import *
from lab2_proc.ProcAltRTL import ProcAltRTL

#-------------------------------------------------------------------------
# add
#-------------------------------------------------------------------------

import inst_staff_add

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_add.gen_basic_test     ) ,
  asm_test( inst_staff_add.gen_dest_dep_test  ) ,
  asm_test( inst_staff_add.gen_src0_dep_test  ) ,
  asm_test( inst_staff_add.gen_src1_dep_test  ) ,
  asm_test( inst_staff_add.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_add.gen_srcs_dest_test ) ,
  asm_test( inst_staff_add.gen_value_test     ) ,
  asm_test( inst_staff_add.gen_random_test    ) ,
])
def test_add( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_add_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_add.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )
 
#-------------------------------------------------------------------------
# sub
#-------------------------------------------------------------------------

import inst_staff_sub

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_sub.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_sub.gen_dest_dep_test  ) ,
  asm_test( inst_staff_sub.gen_src0_dep_test  ) ,
  asm_test( inst_staff_sub.gen_src1_dep_test  ) ,
  asm_test( inst_staff_sub.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_sub.gen_srcs_dest_test ) ,
  asm_test( inst_staff_sub.gen_value_test     ) ,
  asm_test( inst_staff_sub.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_sub( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_sub_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_sub.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# mul
#-------------------------------------------------------------------------

import inst_staff_mul

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_mul.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_mul.gen_dest_dep_test  ) ,
  asm_test( inst_staff_mul.gen_src0_dep_test  ) ,
  asm_test( inst_staff_mul.gen_src1_dep_test  ) ,
  asm_test( inst_staff_mul.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_mul.gen_srcs_dest_test ) ,
  asm_test( inst_staff_mul.gen_value_test     ) ,
  asm_test( inst_staff_mul.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_mul( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_mul_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_mul.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# and
#-------------------------------------------------------------------------

import inst_staff_and

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_and.gen_basic_test     ) ,
  asm_test( inst_staff_and.gen_dest_dep_test  ) ,
  asm_test( inst_staff_and.gen_src0_dep_test  ) ,
  asm_test( inst_staff_and.gen_src1_dep_test  ) ,
  asm_test( inst_staff_and.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_and.gen_srcs_dest_test ) ,
  asm_test( inst_staff_and.gen_value_test     ) ,
  asm_test( inst_staff_and.gen_random_test    ) ,
])
def test_and( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_and_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_and.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# or
#-------------------------------------------------------------------------

import inst_staff_or

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_or.gen_basic_test     ) ,
  asm_test( inst_staff_or.gen_dest_dep_test  ) ,
  asm_test( inst_staff_or.gen_src0_dep_test  ) ,
  asm_test( inst_staff_or.gen_src1_dep_test  ) ,
  asm_test( inst_staff_or.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_or.gen_srcs_dest_test ) ,
  asm_test( inst_staff_or.gen_value_test     ) ,
  asm_test( inst_staff_or.gen_random_test    ) ,
])
def test_or( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_or_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_or.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# xor
#-------------------------------------------------------------------------

import inst_staff_xor

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_xor.gen_basic_test     ) ,
  asm_test( inst_staff_xor.gen_dest_dep_test  ) ,
  asm_test( inst_staff_xor.gen_src0_dep_test  ) ,
  asm_test( inst_staff_xor.gen_src1_dep_test  ) ,
  asm_test( inst_staff_xor.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_xor.gen_srcs_dest_test ) ,
  asm_test( inst_staff_xor.gen_value_test     ) ,
  asm_test( inst_staff_xor.gen_random_test    ) ,
])
def test_xor( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_xor_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_xor.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# slt
#-------------------------------------------------------------------------

import inst_staff_slt

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_slt.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_slt.gen_dest_dep_test  ) ,
  asm_test( inst_staff_slt.gen_src0_dep_test  ) ,
  asm_test( inst_staff_slt.gen_src1_dep_test  ) ,
  asm_test( inst_staff_slt.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_slt.gen_srcs_dest_test ) ,
  asm_test( inst_staff_slt.gen_value_test     ) ,
  asm_test( inst_staff_slt.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_slt( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_slt_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_slt.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# sltu
#-------------------------------------------------------------------------

import inst_staff_sltu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_sltu.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_sltu.gen_dest_dep_test  ) ,
  asm_test( inst_staff_sltu.gen_src0_dep_test  ) ,
  asm_test( inst_staff_sltu.gen_src1_dep_test  ) ,
  asm_test( inst_staff_sltu.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_sltu.gen_srcs_dest_test ) ,
  asm_test( inst_staff_sltu.gen_value_test     ) ,
  asm_test( inst_staff_sltu.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_sltu( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_sltu_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_sltu.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# sra
#-------------------------------------------------------------------------

import inst_staff_sra

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_sra.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_sra.gen_dest_dep_test  ) ,
  asm_test( inst_staff_sra.gen_src0_dep_test  ) ,
  asm_test( inst_staff_sra.gen_src1_dep_test  ) ,
  asm_test( inst_staff_sra.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_sra.gen_srcs_dest_test ) ,
  asm_test( inst_staff_sra.gen_value_test     ) ,
  asm_test( inst_staff_sra.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_sra( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_sra_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_sra.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# srl
#-------------------------------------------------------------------------

import inst_staff_srl

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_srl.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_srl.gen_dest_dep_test  ) ,
  asm_test( inst_staff_srl.gen_src0_dep_test  ) ,
  asm_test( inst_staff_srl.gen_src1_dep_test  ) ,
  asm_test( inst_staff_srl.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_srl.gen_srcs_dest_test ) ,
  asm_test( inst_staff_srl.gen_value_test     ) ,
  asm_test( inst_staff_srl.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_srl( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_srl_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_srl.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# sll
#-------------------------------------------------------------------------

import inst_staff_sll

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_sll.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_sll.gen_dest_dep_test  ) ,
  asm_test( inst_staff_sll.gen_src0_dep_test  ) ,
  asm_test( inst_staff_sll.gen_src1_dep_test  ) ,
  asm_test( inst_staff_sll.gen_srcs_dep_test  ) ,
  asm_test( inst_staff_sll.gen_srcs_dest_test ) ,
  asm_test( inst_staff_sll.gen_value_test     ) ,
  asm_test( inst_staff_sll.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_sll( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_sll_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_sll.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )
