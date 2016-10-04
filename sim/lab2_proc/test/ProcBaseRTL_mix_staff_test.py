#=========================================================================
# ProcBaseRTL_mix_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness_staff import *
from lab2_proc.ProcBaseRTL import ProcBaseRTL

#-------------------------------------------------------------------------
# jal_beq
#-------------------------------------------------------------------------

import inst_staff_jal_beq

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_jal_beq.gen_basic_test     ) ,
])
def test_jal_beq( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )
 
#-------------------------------------------------------------------------
# mul_mem
#-------------------------------------------------------------------------

import inst_staff_mul_mem

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_mul_mem.gen_basic_test     ) ,
  asm_test( inst_staff_mul_mem.gen_more_test      ) ,
])
def test_mul_mem( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )
 
  
