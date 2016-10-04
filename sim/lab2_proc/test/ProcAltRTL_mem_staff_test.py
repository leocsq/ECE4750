#=========================================================================
# ProcAltRTL_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness_staff import *
from lab2_proc.ProcAltRTL import ProcAltRTL

#-------------------------------------------------------------------------
# lw
#-------------------------------------------------------------------------

import inst_staff_lw

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_lw.gen_basic_test     ) ,
  asm_test( inst_staff_lw.gen_dest_dep_test  ) ,
  asm_test( inst_staff_lw.gen_base_dep_test  ) ,
  asm_test( inst_staff_lw.gen_srcs_dest_test ) ,
  asm_test( inst_staff_lw.gen_value_test     ) ,
  asm_test( inst_staff_lw.gen_random_test    ) ,
])
def test_lw( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_lw_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_lw.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )

#-------------------------------------------------------------------------
# sw
#-------------------------------------------------------------------------

import inst_staff_sw

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_sw.gen_basic_test     ),

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_sw.gen_dest_dep_test  ),
  asm_test( inst_staff_sw.gen_base_dep_test  ),
  asm_test( inst_staff_sw.gen_src_dep_test   ),
  asm_test( inst_staff_sw.gen_srcs_dep_test  ),
  asm_test( inst_staff_sw.gen_srcs_dest_test ),
  asm_test( inst_staff_sw.gen_value_test     ),
  asm_test( inst_staff_sw.gen_random_test    ),

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_sw( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_sw_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_sw.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3 )
