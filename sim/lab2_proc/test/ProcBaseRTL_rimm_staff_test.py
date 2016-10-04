#=========================================================================
# ProcBaseRTL_alu_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness_staff import *
from lab2_proc.ProcBaseRTL import ProcBaseRTL

#-------------------------------------------------------------------------
# addi
#-------------------------------------------------------------------------

import inst_staff_addi

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_addi.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_addi.gen_dest_dep_test  ) ,
  asm_test( inst_staff_addi.gen_src_dep_test   ) ,
  asm_test( inst_staff_addi.gen_srcs_dest_test ) ,
  asm_test( inst_staff_addi.gen_value_test     ) ,
  asm_test( inst_staff_addi.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_addi( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_addi_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_addi.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# andi
#-------------------------------------------------------------------------

import inst_staff_andi

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_andi.gen_basic_test     ) ,
  asm_test( inst_staff_andi.gen_dest_dep_test  ) ,
  asm_test( inst_staff_andi.gen_src_dep_test   ) ,
  asm_test( inst_staff_andi.gen_srcs_dest_test ) ,
  asm_test( inst_staff_andi.gen_value_test     ) ,
  asm_test( inst_staff_andi.gen_random_test    ) ,
])
def test_andi( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_andi_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_andi.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# ori
#-------------------------------------------------------------------------

import inst_staff_ori

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_ori.gen_basic_test     ) ,
  asm_test( inst_staff_ori.gen_dest_dep_test  ) ,
  asm_test( inst_staff_ori.gen_src_dep_test   ) ,
  asm_test( inst_staff_ori.gen_srcs_dest_test ) ,
  asm_test( inst_staff_ori.gen_value_test     ) ,
  asm_test( inst_staff_ori.gen_random_test    ) ,
])
def test_ori( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_ori_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_ori.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# xori
#-------------------------------------------------------------------------

import inst_staff_xori

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_xori.gen_basic_test     ) ,
  asm_test( inst_staff_xori.gen_dest_dep_test  ) ,
  asm_test( inst_staff_xori.gen_src_dep_test   ) ,
  asm_test( inst_staff_xori.gen_srcs_dest_test ) ,
  asm_test( inst_staff_xori.gen_value_test     ) ,
  asm_test( inst_staff_xori.gen_random_test    ) ,
])
def test_xori( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_xori_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_xori.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# slti
#-------------------------------------------------------------------------

import inst_staff_slti

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_slti.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_slti.gen_dest_dep_test  ) ,
  asm_test( inst_staff_slti.gen_src_dep_test   ) ,
  asm_test( inst_staff_slti.gen_srcs_dest_test ) ,
  asm_test( inst_staff_slti.gen_value_test     ) ,
  asm_test( inst_staff_slti.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_slti( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_slti_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_slti.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# sltiu
#-------------------------------------------------------------------------

import inst_staff_sltiu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_sltiu.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_sltiu.gen_dest_dep_test  ) ,
  asm_test( inst_staff_sltiu.gen_src_dep_test   ) ,
  asm_test( inst_staff_sltiu.gen_srcs_dest_test ) ,
  asm_test( inst_staff_sltiu.gen_value_test     ) ,
  asm_test( inst_staff_sltiu.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_sltiu( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )
 
def test_sltiu_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_sltiu.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# srai
#-------------------------------------------------------------------------

import inst_staff_srai

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_srai.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_srai.gen_dest_dep_test  ) ,
  asm_test( inst_staff_srai.gen_src_dep_test   ) ,
  asm_test( inst_staff_srai.gen_srcs_dest_test ) ,
  asm_test( inst_staff_srai.gen_value_test     ) ,
  asm_test( inst_staff_srai.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_srai( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_srai_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_srai.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# srli
#-------------------------------------------------------------------------

import inst_staff_srli

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_srli.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_srli.gen_dest_dep_test  ) ,
  asm_test( inst_staff_srli.gen_src_dep_test   ) ,
  asm_test( inst_staff_srli.gen_srcs_dest_test ) ,
  asm_test( inst_staff_srli.gen_value_test     ) ,
  asm_test( inst_staff_srli.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_srli( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_srli_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_srli.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# slli
#-------------------------------------------------------------------------

import inst_staff_slli

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_slli.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_slli.gen_dest_dep_test  ) ,
  asm_test( inst_staff_slli.gen_src_dep_test   ) ,
  asm_test( inst_staff_slli.gen_srcs_dest_test ) ,
  asm_test( inst_staff_slli.gen_value_test     ) ,
  asm_test( inst_staff_slli.gen_random_test    ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_slli( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_slli_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_slli.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# lui
#-------------------------------------------------------------------------

import inst_staff_lui

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_lui.gen_basic_test    ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_lui.gen_dest_dep_test ) ,
  asm_test( inst_staff_lui.gen_value_test    ) ,
  asm_test( inst_staff_lui.gen_random_test   ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_lui( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_lui_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_lui.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# auipc
#-------------------------------------------------------------------------

import inst_staff_auipc

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_auipc.gen_basic_test    ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_auipc.gen_dest_dep_test ) ,
  asm_test( inst_staff_auipc.gen_value_test    ) ,
  asm_test( inst_staff_auipc.gen_random_test   ) ,
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_auipc( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_auipc_rand_delays( dump_vcd ):
  run_test( ProcBaseRTL, inst_staff_auipc.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )
