#=========================================================================
# ProcBaseRTL_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness import *
from lab2_proc.ProcBaseRTL import ProcBaseRTL

#-------------------------------------------------------------------------
# jal
#-------------------------------------------------------------------------

import inst_jal

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_jal.gen_basic_test        ) ,
  asm_test( inst_jal.gen_nops_dep_taken_test),
  asm_test( inst_jal.gen_random_test),
])
def test_jal( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# jalr
#-------------------------------------------------------------------------

import inst_jalr

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_jalr.gen_basic_test  ),
  asm_test( inst_jalr.gen_nops_dep_taken_test),
  asm_test( inst_jalr.gen_random_test),
])
def test_jalr( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )
