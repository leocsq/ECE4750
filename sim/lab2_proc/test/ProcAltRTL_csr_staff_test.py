#=========================================================================
# ProcAltRTL_csr_test.py
#=========================================================================

import pytest
import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl   import *
from harness_staff import *
from lab2_proc.ProcAltRTL import ProcAltRTL

#-------------------------------------------------------------------------
# csr
#-------------------------------------------------------------------------

import inst_staff_csr

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_staff_csr.gen_basic_test      ),
  asm_test( inst_staff_csr.gen_bypass_test     ),
  asm_test( inst_staff_csr.gen_value_test      ),
  asm_test( inst_staff_csr.gen_random_test     ),
  asm_test( inst_staff_csr.gen_core_stats_test ),
])
def test_csr( name, test, dump_vcd ):
  run_test( ProcAltRTL, test, dump_vcd )

def test_csr_rand_delays( dump_vcd ):
  run_test( ProcAltRTL, inst_staff_csr.gen_random_test, dump_vcd,
            src_delay=3, sink_delay=10, mem_stall_prob=0.5, mem_latency=3)
