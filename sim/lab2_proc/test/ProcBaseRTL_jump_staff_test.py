#=========================================================================
# ProcBaseRTL_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness_staff import *
from lab2_proc.ProcBaseRTL import ProcBaseRTL

#-------------------------------------------------------------------------
# jal
#-------------------------------------------------------------------------

import inst_staff_jal

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_jal.gen_basic_test        ) ,

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  asm_test( inst_staff_jal.gen_link_dep_test     ) ,
  asm_test( inst_staff_jal.gen_jump_test         ) ,
  asm_test( inst_staff_jal.gen_back_to_back_test ) ,
  asm_test( inst_staff_jal.gen_value_test_0      ) ,
  asm_test( inst_staff_jal.gen_value_test_1      ) ,
  asm_test( inst_staff_jal.gen_value_test_2      ) ,
  asm_test( inst_staff_jal.gen_value_test_3      ) ,
  asm_test( inst_staff_jal.gen_jal_stall_test    ) ,
  
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])

def test_jal( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_jal_rand_delays(dump_vcd):
  run_test( ProcBaseRTL, inst_staff_jal.gen_jump_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=.5, mem_latency=3 )

#-------------------------------------------------------------------------
# jalr
#-------------------------------------------------------------------------

import inst_staff_jalr

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_jalr.gen_basic_test    ) ,
  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to test more complicated
  # scenarios.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/
  asm_test( inst_staff_jalr.gen_link_dep_test ),
  asm_test( inst_staff_jalr.gen_jump_test     ),
  asm_test( inst_staff_jalr.gen_lsb_test      ), 
  asm_test( inst_staff_jalr.gen_value_test_0  ),
  asm_test( inst_staff_jalr.gen_value_test_1  ),
  asm_test( inst_staff_jalr.gen_value_test_2  ),
  asm_test( inst_staff_jalr.gen_value_test_3  ),

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\
])
def test_jalr( name, test, dump_vcd ):
  run_test( ProcBaseRTL, test, dump_vcd )

def test_jalr_rand_delays(dump_vcd):
  run_test( ProcBaseRTL, inst_staff_jalr.gen_jump_test, dump_vcd,
            src_delay=3, sink_delay=5, mem_stall_prob=.5, mem_latency=3 )
