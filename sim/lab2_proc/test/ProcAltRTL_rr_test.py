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
# add
#-------------------------------------------------------------------------

import inst_add

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_add.gen_basic_test     ) ,
  asm_test( inst_add.gen_dest_dep_test  ) ,
  asm_test( inst_add.gen_src0_dep_test  ) ,
  asm_test( inst_add.gen_src1_dep_test  ) ,
  asm_test( inst_add.gen_srcs_dep_test  ) ,
  asm_test( inst_add.gen_srcs_dest_test ) ,
  asm_test( inst_add.gen_value_test     ) ,
  asm_test( inst_add.gen_random_test    ) ,
])
def test_add( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )
 
#-------------------------------------------------------------------------
# sub
#-------------------------------------------------------------------------

import inst_sub

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sub.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_sub( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# mul
#-------------------------------------------------------------------------

import inst_mul

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_mul.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_mul( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# and
#-------------------------------------------------------------------------

import inst_and

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_and.gen_basic_test     ) ,
  asm_test( inst_and.gen_dest_dep_test  ) ,
  asm_test( inst_and.gen_src0_dep_test  ) ,
  asm_test( inst_and.gen_src1_dep_test  ) ,
  asm_test( inst_and.gen_srcs_dep_test  ) ,
  asm_test( inst_and.gen_srcs_dest_test ) ,
  asm_test( inst_and.gen_value_test     ) ,
  asm_test( inst_and.gen_random_test    ) ,
])
def test_and( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# or
#-------------------------------------------------------------------------

import inst_or

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_or.gen_basic_test     ) ,
  asm_test( inst_or.gen_dest_dep_test  ) ,
  asm_test( inst_or.gen_src0_dep_test  ) ,
  asm_test( inst_or.gen_src1_dep_test  ) ,
  asm_test( inst_or.gen_srcs_dep_test  ) ,
  asm_test( inst_or.gen_srcs_dest_test ) ,
  asm_test( inst_or.gen_value_test     ) ,
  asm_test( inst_or.gen_random_test    ) ,
])
def test_or( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# xor
#-------------------------------------------------------------------------

import inst_xor

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_xor.gen_basic_test     ) ,
  asm_test( inst_xor.gen_dest_dep_test  ) ,
  asm_test( inst_xor.gen_src0_dep_test  ) ,
  asm_test( inst_xor.gen_src1_dep_test  ) ,
  asm_test( inst_xor.gen_srcs_dep_test  ) ,
  asm_test( inst_xor.gen_srcs_dest_test ) ,
  asm_test( inst_xor.gen_value_test     ) ,
  asm_test( inst_xor.gen_random_test    ) ,
])
def test_xor( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# slt
#-------------------------------------------------------------------------

import inst_slt

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_slt.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_slt( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# sltu
#-------------------------------------------------------------------------

import inst_sltu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sltu.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_sltu( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# sra
#-------------------------------------------------------------------------

import inst_sra

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sra.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_sra( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# srl
#-------------------------------------------------------------------------

import inst_srl

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_srl.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_srl( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# sll
#-------------------------------------------------------------------------

import inst_sll

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sll.gen_basic_test     ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_sll( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )


         
