#=========================================================================
# ProcAltRTL_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness import *
from lab2_proc.ProcAltRTL import ProcAltRTL

#-------------------------------------------------------------------------
# jal
#-------------------------------------------------------------------------

import inst_jal

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_jal.gen_basic_test        ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_jal( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

#-------------------------------------------------------------------------
# jalr
#-------------------------------------------------------------------------

import inst_jalr

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_jalr.gen_basic_test ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])
def test_jalr( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )