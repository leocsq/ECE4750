#=========================================================================
# ProcAltRTL_alu_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness import *
from lab2_proc.ProcAltRTL import ProcAltRTL

#-------------------------------------------------------------------------
# addi
#-------------------------------------------------------------------------

import inst_addi

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_addi.gen_basic_test     ) ,
  asm_test( inst_addi.gen_dest_dep_test   ) ,
  asm_test( inst_addi.gen_src_dep_test    ) ,
  asm_test( inst_addi.gen_src_eq_dest_test) ,
  asm_test( inst_addi.gen_value_test      ) ,
  asm_test( inst_addi.gen_random_test     ) ,
])
def test_addi( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# andi
#-------------------------------------------------------------------------

import inst_andi

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_andi.gen_basic_test     ) ,
  asm_test( inst_andi.gen_dest_dep_test  ) ,
  asm_test( inst_andi.gen_src_dep_test   ) ,
  asm_test( inst_andi.gen_srcs_dest_test ) ,
  asm_test( inst_andi.gen_value_test     ) ,
  asm_test( inst_andi.gen_random_test    ) ,
])
def test_andi( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# ori
#-------------------------------------------------------------------------

import inst_ori

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_ori.gen_basic_test     ) ,
  asm_test( inst_ori.gen_dest_dep_test  ) ,
  asm_test( inst_ori.gen_src_dep_test   ) ,
  asm_test( inst_ori.gen_srcs_dest_test ) ,
  asm_test( inst_ori.gen_value_test     ) ,
  asm_test( inst_ori.gen_random_test    ) ,
])
def test_ori( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# xori
#-------------------------------------------------------------------------

import inst_xori

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_xori.gen_basic_test     ) ,
  asm_test( inst_xori.gen_dest_dep_test  ) ,
  asm_test( inst_xori.gen_src_dep_test   ) ,
  asm_test( inst_xori.gen_srcs_dest_test ) ,
  asm_test( inst_xori.gen_value_test     ) ,
  asm_test( inst_xori.gen_random_test    ) ,
])
def test_xori( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# slti
#-------------------------------------------------------------------------

import inst_slti

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_slti.gen_basic_test      ) ,
  asm_test( inst_slti.gen_dest_dep_test   ) ,
  asm_test( inst_slti.gen_src_dep_test    ) ,
  asm_test( inst_slti.gen_src_eq_dest_test) ,
  asm_test( inst_slti.gen_value_test      ) , 
  asm_test( inst_slti.gen_random_test     ) ,  

])
def test_slti( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# sltiu
#-------------------------------------------------------------------------

import inst_sltiu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sltiu.gen_basic_test       ) ,
  asm_test( inst_sltiu.gen_dest_dep_test    ) ,
  asm_test( inst_sltiu.gen_src_dep_test     ) ,
  asm_test( inst_sltiu.gen_src_eq_dest_test ) ,
  asm_test( inst_sltiu.gen_value_test       ) ,
  asm_test( inst_sltiu.gen_random_test      ) ,
])
def test_sltiu( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )
 
#-------------------------------------------------------------------------
# srai
#-------------------------------------------------------------------------

import inst_srai

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_srai.gen_basic_test       ) ,
  asm_test( inst_srai.gen_src_dep_test     ) ,
  asm_test( inst_srai.gen_src_eq_dest_test ) ,
  asm_test( inst_srai.gen_value_test       ) ,
  asm_test( inst_srai.gen_random_test      ) ,
])
def test_srai( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# srli
#-------------------------------------------------------------------------

import inst_srli

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_srli.gen_basic_test      ) ,
  asm_test( inst_srli.gen_dest_dep_test    ) ,
  asm_test( inst_srli.gen_src_dep_test     ) ,
  asm_test( inst_srli.gen_src_eq_dest_test ) ,
  asm_test( inst_srli.gen_value_test       ) ,
  asm_test( inst_srli.gen_random_test      ) ,
])
def test_srli( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# slli
#-------------------------------------------------------------------------

import inst_slli

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_slli.gen_basic_test       ) ,
  asm_test( inst_slli.gen_dest_dep_test    ) ,
  asm_test( inst_slli.gen_src_dep_test     ) ,
  asm_test( inst_slli.gen_src_eq_dest_test ) ,
  asm_test( inst_slli.gen_value_test       ) ,
  asm_test( inst_slli.gen_random_test      ) ,
])
def test_slli( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# lui
#-------------------------------------------------------------------------

import inst_lui

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_lui.gen_basic_test    ) ,
  asm_test( inst_lui.gen_dest_dep_test ) ,
  asm_test( inst_lui.gen_value_test    ) ,
])
def test_lui( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# auipc
#-------------------------------------------------------------------------

import inst_auipc

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_auipc.gen_basic_test    ) ,
  asm_test( inst_auipc.gen_dest_dep_test ) , 
  asm_test( inst_auipc.gen_value_test    ) , 
  asm_test( inst_auipc.gen_random_test   ) ,
])
def test_auipc( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )
  
