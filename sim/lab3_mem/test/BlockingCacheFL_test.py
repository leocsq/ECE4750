#=========================================================================
# BlockingCacheFL_test.py
#=========================================================================

from __future__ import print_function

import pytest
import random
import struct
import math

random.seed(0xa4e28cc2)

from pymtl      import *
from pclib.test import mk_test_case_table, run_sim
from pclib.test import TestSource
from pclib.test import TestMemory

from pclib.ifcs import MemMsg,    MemReqMsg,    MemRespMsg
from pclib.ifcs import MemMsg4B,  MemReqMsg4B,  MemRespMsg4B
from pclib.ifcs import MemMsg16B, MemReqMsg16B, MemRespMsg16B

from TestCacheSink   import TestCacheSink
from lab3_mem.BlockingCacheFL import BlockingCacheFL

# We define all test cases here. They will be used to test _both_ FL and
# RTL models.
#
# Notice the difference between the TestHarness instances in FL and RTL.
#
# class TestHarness( Model ):
#   def __init__( s, src_msgs, sink_msgs, stall_prob, latency,
#                 src_delay, sink_delay, CacheModel, check_test, dump_vcd )
#
# The last parameter of TestHarness, check_test is whether or not we
# check the test field in the cacheresp. In FL model we don't care about
# test field and we set cehck_test to be False because FL model is just
# passing through cachereq to mem, so all cachereq sent to the FL model
# will be misses, whereas in RTL model we must set check_test to be True
# so that the test sink will know if we hit the cache properly.

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Model ):

  def __init__( s, src_msgs, sink_msgs, stall_prob, latency,
                src_delay, sink_delay, 
                CacheModel, num_banks, check_test, dump_vcd ):

    # Messge type

    cache_msgs = MemMsg4B()
    mem_msgs   = MemMsg16B()

    # Instantiate models

    s.src   = TestSource   ( cache_msgs.req,  src_msgs,  src_delay  )
    s.cache = CacheModel   ( num_banks = num_banks )
    s.mem   = TestMemory   ( mem_msgs, 1, stall_prob, latency )
    s.sink  = TestCacheSink( cache_msgs.resp, sink_msgs, sink_delay, check_test )

    # Dump VCD

    if dump_vcd:
      s.cache.vcd_file = dump_vcd

    # Connect

    s.connect( s.src.out,       s.cache.cachereq  )
    s.connect( s.sink.in_,      s.cache.cacheresp )

    s.connect( s.cache.memreq,  s.mem.reqs[0]     )
    s.connect( s.cache.memresp, s.mem.resps[0]    )

  def load( s, addrs, data_ints ):
    for addr, data_int in zip( addrs, data_ints ):
      data_bytes_a = bytearray()
      data_bytes_a.extend( struct.pack("<I",data_int) )
      s.mem.write_mem( addr, data_bytes_a )

  def done( s ):
    return s.src.done and s.sink.done

  def line_trace( s ):
    return s.src.line_trace() + " " + s.cache.line_trace() + " " \
         + s.mem.line_trace() + " " + s.sink.line_trace()

#-------------------------------------------------------------------------
# make messages
#-------------------------------------------------------------------------

def req( type_, opaque, addr, len, data ):
  msg = MemReqMsg4B()

  if   type_ == 'rd': msg.type_ = MemReqMsg.TYPE_READ
  elif type_ == 'wr': msg.type_ = MemReqMsg.TYPE_WRITE
  elif type_ == 'in': msg.type_ = MemReqMsg.TYPE_WRITE_INIT

  msg.addr   = addr
  msg.opaque = opaque
  msg.len    = len
  msg.data   = data
  return msg

def resp( type_, opaque, test, len, data ):
  msg = MemRespMsg4B()

  if   type_ == 'rd': msg.type_ = MemRespMsg.TYPE_READ
  elif type_ == 'wr': msg.type_ = MemRespMsg.TYPE_WRITE
  elif type_ == 'in': msg.type_ = MemRespMsg.TYPE_WRITE_INIT

  msg.opaque = opaque
  msg.len    = len
  msg.test   = test
  msg.data   = data
  return msg

#----------------------------------------------------------------------
# Test Case: read hit path clean
#----------------------------------------------------------------------
# The test field in the response message: 0 == MISS, 1 == HIT

def read_hit_1word_clean( base_addr ):
  return [
    #    type  opq  addr      len data                type  opq  test len data
    req( 'in', 0x0, base_addr, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, base_addr, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xdeadbeef ),
  ]

#----------------------------------------------------------------------
# Test Case: read hit path -- for set-associative cache
#----------------------------------------------------------------------
# This set of tests designed only for alternative design
# The test field in the response message: 0 == MISS, 1 == HIT

def read_hit_asso( base_addr ):
  return [
    #    type  opq  addr       len data                type  opq  test len data
    req( 'wr', 0x0, 0x00000000, 0, 0xdeadbeef ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x00001000, 0, 0x00c0ffee ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'rd', 0x2, 0x00000000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x3, 0x00001000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x00c0ffee ),
    
  ]

  
#----------------------------------------------------------------------
# Test Case: read hit path -- for direct-mapped cache
#----------------------------------------------------------------------
# This set of tests designed only for baseline design

def read_hit_dmap( base_addr ):
  return [
    #    type  opq  addr       len data                type  opq  test len data
    req( 'wr', 0x0, 0x00000000, 0, 0xdeadbeef ), resp( 'wr', 0x0, 0,   0,  0          ), 
    req( 'wr', 0x1, 0x00001000, 0, 0x00c0ffee ), resp( 'wr', 0x1, 0,   0,  0          ), 
    req( 'rd', 0x2, 0x00000000, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xdeadbeef ), 
    req( 'rd', 0x3, 0x00001000, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0x00c0ffee ), 
    req( 'wr', 0x4, 0x00001004, 0, 0xbeefdead ), resp( 'wr', 0x4, 1,   0,  0          ), 
    req( 'rd', 0x5, 0x00001004, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xbeefdead ), 
    
  ]

  
#-------------------------------------------------------------------------
# Test Case: write hit path clean
#-------------------------------------------------------------------------

def write_hit_1word_clean( base_addr ):
  return [
    #    type  opq   addr      len data               type  opq   test len data
    req( 'in', 0x00, base_addr, 0, 0x0a0b0c0d ), resp('in', 0x00, 0,   0,  0          ), 
    req( 'wr', 0x01, base_addr, 0, 0xbeefbeeb ), resp('wr', 0x01, 1,   0,  0          ), 
    req( 'rd', 0x02, base_addr, 0, 0          ), resp('rd', 0x02, 1,   0,  0xbeefbeeb ), 
  ]

  
#-------------------------------------------------------------------------
# Test Case: read hit path dirty
#-------------------------------------------------------------------------

def read_hit_1word_dirty( base_addr ):
  return [
    #    type  opq   addr      len data               type  opq   test len data
    req( 'wr', 0x00, base_addr, 0, 0xbeefbeeb ), resp('wr', 0x00, 0,   0,  0          ), 
    req( 'rd', 0x01, base_addr, 0, 0          ), resp('rd', 0x01, 1,   0,  0xbeefbeeb ), 
  ]

#-------------------------------------------------------------------------
# Test Case: write hit path dirty
#-------------------------------------------------------------------------

def write_hit_1word_dirty( base_addr ):
  return [
    #    type  opq   addr      len data               type  opq   test len data
    req( 'wr', 0x00, base_addr, 0, 0x0a0b0c0d ), resp('in', 0x00, 0,   0,  0          ), 
    req( 'wr', 0x01, base_addr, 0, 0xbeefbeeb ), resp('wr', 0x01, 1,   0,  0          ), 
    req( 'rd', 0x02, base_addr, 0, 0          ), resp('rd', 0x02, 1,   0,  0xbeefbeeb ), 
  ]
#-------------------------------------------------------------------------
# Test Case: read miss with refill and no eviction
#-------------------------------------------------------------------------

def read_miss_1word_refill_noecvt( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), 
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), 
    
  ]
#-------------------------------------------------------------------------
# Test Case: write miss with refill and no eviction
#-------------------------------------------------------------------------

def write_miss_1word_refill_noecvt( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0            ), 
    req( 'rd', 0x01, 0x00000000, 0, 0          ), resp('rd', 0x01, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x02, 0x00000004, 0, 0          ), resp('rd', 0x02, 1, 0,   0x03334444   ),
  ]

#-------------------------------------------------------------------------
# Test Case: read miss with refill and eviction--asso
#-------------------------------------------------------------------------
# This set of tests designed only for alternative design

def read_miss_refill_ecvt_asso( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0          ),
    req( 'wr', 0x01, 0x00000200, 0, 0xbeefdead ), resp('wr', 0x01, 0, 0,   0          ),
    req( 'rd', 0x02, 0x00000300, 0, 0          ), resp('rd', 0x02, 0, 0,   0x77585241 ), 
    req( 'rd', 0x03, 0x00000400, 0, 0          ), resp('rd', 0x03, 0, 0,   0x00074110 ), 
    
  ]

#-------------------------------------------------------------------------
# Test Case: read miss with refill and eviction--dmap
#-------------------------------------------------------------------------
# This set of tests designed only for baseline design

def read_miss_refill_ecvt_dmap( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0          ),
    req( 'rd', 0x01, 0x00000200, 0, 0          ), resp('rd', 0x01, 0, 0,   0xbeefdead ),
    req( 'rd', 0x02, 0x00000204, 0, 0          ), resp('rd', 0x02, 1, 0,   0x00c0ffee ), 
    
  ]

#-------------------------------------------------------------------------
# Test Case: write miss with refill and eviction--asso
#-------------------------------------------------------------------------
# This set of tests designed only for alternative design

def write_miss_refill_ecvt_asso( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0            ),
    req( 'wr', 0x01, 0x00000100, 0, 0xabababab ), resp('wr', 0x01, 0, 0,   0            ),
    req( 'wr', 0x02, 0x00000200, 0, 0xcdcdcdcd ), resp('wr', 0x02, 0, 0,   0            ), 
    req( 'rd', 0x03, 0x00000100, 0, 0          ), resp('rd', 0x03, 1, 0,   0xabababab   ), 
    req( 'rd', 0x04, 0x00000204, 0, 0          ), resp('rd', 0x04, 1, 0,   0x00c0ffee   ),
  ]

#-------------------------------------------------------------------------
# Test Case: write miss with refill and eviction--dmap
#-------------------------------------------------------------------------
# This set of tests designed only for baseline design

def write_miss_refill_ecvt_dmap( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0            ), 
    req( 'wr', 0x01, 0x00000100, 0, 0xabababab ), resp('wr', 0x01, 0, 0,   0            ),
    req( 'rd', 0x02, 0x00000100, 0, 0          ), resp('rd', 0x02, 1, 0,   0xabababab   ),
    req( 'rd', 0x03, 0x00000104, 0, 0          ), resp('rd', 0x03, 1, 0,   0x00c0ffee   ),
  ]

#-------------------------------------------------------------------------
# Test Case: fully used all cache lines--asso
#-------------------------------------------------------------------------
# This set of tests designed only for alternative design

def fully_used_all_cache_lines_asso( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0            ), 
    req( 'wr', 0x01, 0x00000010, 0, 0xdeadbeef ), resp('wr', 0x01, 0, 0,   0            ), 
    req( 'wr', 0x02, 0x00000020, 0, 0xdeadbeef ), resp('wr', 0x02, 0, 0,   0            ), 
    req( 'wr', 0x03, 0x00000030, 0, 0xdeadbeef ), resp('wr', 0x03, 0, 0,   0            ), 
    req( 'wr', 0x04, 0x00000040, 0, 0xdeadbeef ), resp('wr', 0x04, 0, 0,   0            ), 
    req( 'wr', 0x05, 0x00000050, 0, 0xdeadbeef ), resp('wr', 0x05, 0, 0,   0            ), 
    req( 'wr', 0x06, 0x00000060, 0, 0xdeadbeef ), resp('wr', 0x06, 0, 0,   0            ), 
    req( 'wr', 0x07, 0x00000070, 0, 0xdeadbeef ), resp('wr', 0x07, 0, 0,   0            ), 
    req( 'wr', 0x08, 0x00000080, 0, 0xdeadbeef ), resp('wr', 0x08, 0, 0,   0            ), 
    req( 'wr', 0x09, 0x00000090, 0, 0xdeadbeef ), resp('wr', 0x09, 0, 0,   0            ), 
    req( 'wr', 0x0a, 0x000000a0, 0, 0xdeadbeef ), resp('wr', 0x0a, 0, 0,   0            ), 
    req( 'wr', 0x0b, 0x000000b0, 0, 0xdeadbeef ), resp('wr', 0x0b, 0, 0,   0            ), 
    req( 'wr', 0x0c, 0x000000c0, 0, 0xdeadbeef ), resp('wr', 0x0c, 0, 0,   0            ), 
    req( 'wr', 0x0d, 0x000000d0, 0, 0xdeadbeef ), resp('wr', 0x0d, 0, 0,   0            ), 
    req( 'wr', 0x0e, 0x000000e0, 0, 0xdeadbeef ), resp('wr', 0x0e, 0, 0,   0            ),
    req( 'wr', 0x0f, 0x000000f0, 0, 0xdeadbeef ), resp('wr', 0x0f, 0, 0,   0            ), 
    req( 'rd', 0x10, 0x00000000, 0, 0          ), resp('rd', 0x10, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x11, 0x00000004, 0, 0          ), resp('rd', 0x11, 1, 0,   0x03334444   ),
    req( 'rd', 0x12, 0x00000010, 0, 0          ), resp('rd', 0x12, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x13, 0x00000014, 0, 0          ), resp('rd', 0x13, 1, 0,   0x13334444   ),
    req( 'rd', 0x14, 0x00000020, 0, 0          ), resp('rd', 0x14, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x15, 0x00000024, 0, 0          ), resp('rd', 0x15, 1, 0,   0x23334444   ), 
    req( 'rd', 0x16, 0x00000030, 0, 0          ), resp('rd', 0x16, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x17, 0x00000034, 0, 0          ), resp('rd', 0x17, 1, 0,   0x33334444   ), 
    req( 'rd', 0x18, 0x00000040, 0, 0          ), resp('rd', 0x18, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x19, 0x00000044, 0, 0          ), resp('rd', 0x19, 1, 0,   0x43334444   ), 
    req( 'rd', 0x1a, 0x00000050, 0, 0          ), resp('rd', 0x1a, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x1b, 0x00000054, 0, 0          ), resp('rd', 0x1b, 1, 0,   0x53334444   ), 
    req( 'rd', 0x1c, 0x00000060, 0, 0          ), resp('rd', 0x1c, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x1d, 0x00000064, 0, 0          ), resp('rd', 0x1d, 1, 0,   0x63334444   ), 
    req( 'rd', 0x1e, 0x00000070, 0, 0          ), resp('rd', 0x1e, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x1f, 0x00000074, 0, 0          ), resp('rd', 0x20, 1, 0,   0x73334444   ), 
    req( 'rd', 0x20, 0x00000080, 0, 0          ), resp('rd', 0x21, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x21, 0x00000084, 0, 0          ), resp('rd', 0x22, 1, 0,   0x83334444   ), 
    req( 'rd', 0x22, 0x00000090, 0, 0          ), resp('rd', 0x23, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x23, 0x00000094, 0, 0          ), resp('rd', 0x24, 1, 0,   0x93334444   ), 
    req( 'rd', 0x24, 0x000000a0, 0, 0          ), resp('rd', 0x25, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x25, 0x000000a4, 0, 0          ), resp('rd', 0x26, 1, 0,   0xa3334444   ), 
    req( 'rd', 0x26, 0x000000b0, 0, 0          ), resp('rd', 0x27, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x27, 0x000000b4, 0, 0          ), resp('rd', 0x28, 1, 0,   0xb3334444   ), 
    req( 'rd', 0x28, 0x000000c0, 0, 0          ), resp('rd', 0x29, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x29, 0x000000c4, 0, 0          ), resp('rd', 0x2a, 1, 0,   0xc3334444   ), 
    req( 'rd', 0x2a, 0x000000d0, 0, 0          ), resp('rd', 0x2b, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x2b, 0x000000d4, 0, 0          ), resp('rd', 0x2c, 1, 0,   0xd3334444   ), 
    req( 'rd', 0x2c, 0x000000e0, 0, 0          ), resp('rd', 0x2d, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x2d, 0x000000e4, 0, 0          ), resp('rd', 0x2e, 1, 0,   0xe3334444   ), 
    req( 'rd', 0x2e, 0x000000f0, 0, 0          ), resp('rd', 0x2f, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x2f, 0x000000f4, 0, 0          ), resp('rd', 0x30, 1, 0,   0xf3334444   ), 
    
    
  ]

#-------------------------------------------------------------------------
# Test Case: fully used all cache lines--dmap
#-------------------------------------------------------------------------
# This set of tests designed only for baseline design

def fully_used_all_cache_lines_dmap( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0            ), 
    req( 'wr', 0x01, 0x00000010, 0, 0xdeadbeef ), resp('wr', 0x01, 0, 0,   0            ), 
    req( 'wr', 0x02, 0x00000020, 0, 0xdeadbeef ), resp('wr', 0x02, 0, 0,   0            ), 
    req( 'wr', 0x03, 0x00000030, 0, 0xdeadbeef ), resp('wr', 0x03, 0, 0,   0            ), 
    req( 'wr', 0x04, 0x00000040, 0, 0xdeadbeef ), resp('wr', 0x04, 0, 0,   0            ), 
    req( 'wr', 0x05, 0x00000050, 0, 0xdeadbeef ), resp('wr', 0x05, 0, 0,   0            ), 
    req( 'wr', 0x06, 0x00000060, 0, 0xdeadbeef ), resp('wr', 0x06, 0, 0,   0            ), 
    req( 'wr', 0x07, 0x00000070, 0, 0xdeadbeef ), resp('wr', 0x07, 0, 0,   0            ), 
    req( 'wr', 0x08, 0x00000080, 0, 0xdeadbeef ), resp('wr', 0x08, 0, 0,   0            ), 
    req( 'wr', 0x09, 0x00000090, 0, 0xdeadbeef ), resp('wr', 0x09, 0, 0,   0            ), 
    req( 'wr', 0x0a, 0x000000a0, 0, 0xdeadbeef ), resp('wr', 0x0a, 0, 0,   0            ), 
    req( 'wr', 0x0b, 0x000000b0, 0, 0xdeadbeef ), resp('wr', 0x0b, 0, 0,   0            ), 
    req( 'wr', 0x0c, 0x000000c0, 0, 0xdeadbeef ), resp('wr', 0x0c, 0, 0,   0            ), 
    req( 'wr', 0x0d, 0x000000d0, 0, 0xdeadbeef ), resp('wr', 0x0d, 0, 0,   0            ), 
    req( 'wr', 0x0e, 0x000000e0, 0, 0xdeadbeef ), resp('wr', 0x0e, 0, 0,   0            ), 
    req( 'wr', 0x0f, 0x000000f0, 0, 0xdeadbeef ), resp('wr', 0x0f, 0, 0,   0            ), 
    req( 'rd', 0x10, 0x00000000, 0, 0          ), resp('rd', 0x10, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x11, 0x00000004, 0, 0          ), resp('rd', 0x11, 1, 0,   0x03334444   ),
    req( 'rd', 0x12, 0x00000010, 0, 0          ), resp('rd', 0x12, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x13, 0x00000014, 0, 0          ), resp('rd', 0x13, 1, 0,   0x13334444   ),
    req( 'rd', 0x14, 0x00000020, 0, 0          ), resp('rd', 0x14, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x15, 0x00000024, 0, 0          ), resp('rd', 0x15, 1, 0,   0x23334444   ), 
    req( 'rd', 0x16, 0x00000030, 0, 0          ), resp('rd', 0x16, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x17, 0x00000034, 0, 0          ), resp('rd', 0x17, 1, 0,   0x33334444   ), 
    req( 'rd', 0x18, 0x00000040, 0, 0          ), resp('rd', 0x18, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x19, 0x00000044, 0, 0          ), resp('rd', 0x19, 1, 0,   0x43334444   ), 
    req( 'rd', 0x1a, 0x00000050, 0, 0          ), resp('rd', 0x1a, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x1b, 0x00000054, 0, 0          ), resp('rd', 0x1b, 1, 0,   0x53334444   ), 
    req( 'rd', 0x1c, 0x00000060, 0, 0          ), resp('rd', 0x1c, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x1d, 0x00000064, 0, 0          ), resp('rd', 0x1d, 1, 0,   0x63334444   ), 
    req( 'rd', 0x1e, 0x00000070, 0, 0          ), resp('rd', 0x1e, 1, 0,   0xdeadbeef   ),
    req( 'rd', 0x1f, 0x00000074, 0, 0          ), resp('rd', 0x1f, 1, 0,   0x73334444   ),
    req( 'rd', 0x20, 0x00000080, 0, 0          ), resp('rd', 0x20, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x21, 0x00000084, 0, 0          ), resp('rd', 0x21, 1, 0,   0x83334444   ),
    req( 'rd', 0x22, 0x00000090, 0, 0          ), resp('rd', 0x22, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x23, 0x00000094, 0, 0          ), resp('rd', 0x23, 1, 0,   0x93334444   ),
    req( 'rd', 0x24, 0x000000a0, 0, 0          ), resp('rd', 0x24, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x25, 0x000000a4, 0, 0          ), resp('rd', 0x25, 1, 0,   0xa3334444   ),
    req( 'rd', 0x26, 0x000000b0, 0, 0          ), resp('rd', 0x26, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x27, 0x000000b4, 0, 0          ), resp('rd', 0x27, 1, 0,   0xb3334444   ),
    req( 'rd', 0x28, 0x000000c0, 0, 0          ), resp('rd', 0x28, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x29, 0x000000c4, 0, 0          ), resp('rd', 0x29, 1, 0,   0xc3334444   ),
    req( 'rd', 0x2a, 0x000000d0, 0, 0          ), resp('rd', 0x2a, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x2b, 0x000000d4, 0, 0          ), resp('rd', 0x2b, 1, 0,   0xd3334444   ),
    req( 'rd', 0x2c, 0x000000e0, 0, 0          ), resp('rd', 0x2c, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x2d, 0x000000e4, 0, 0          ), resp('rd', 0x2d, 1, 0,   0xe3334444   ),
    req( 'rd', 0x2e, 0x000000f0, 0, 0          ), resp('rd', 0x2e, 1, 0,   0xdeadbeef   ), 
    req( 'rd', 0x2f, 0x000000f4, 0, 0          ), resp('rd', 0x2e, 1, 0,   0xf3334444   ), 
    
  ]
#-------------------------------------------------------------------------
# Test Case: Conflict misses--asso
#-------------------------------------------------------------------------
# This set of tests designed only for alternative design

def Conflict_misses_asso( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0          ),
    req( 'wr', 0x01, 0x00000200, 0, 0xbeefdead ), resp('wr', 0x01, 0, 0,   0          ),
    req( 'wr', 0x02, 0x00000300, 0, 0xabababab ), resp('wr', 0x02, 0, 0,   0          ), 
    req( 'rd', 0x03, 0x00000000, 0, 0          ), resp('rd', 0x03, 0, 0,   0xdeadbeef ), 
    
  ]

#-------------------------------------------------------------------------
# Test Case: Conflict misses--dmap
#-------------------------------------------------------------------------
# This set of tests designed only for baseline design

def Conflict_misses_dmap( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0          ),
    req( 'wr', 0x01, 0x00000200, 0, 0xbeefdead ), resp('wr', 0x01, 0, 0,   0          ),
    req( 'rd', 0x02, 0x00000000, 0, 0          ), resp('rd', 0x02, 0, 0,   0xdeadbeef ), 
    req( 'rd', 0x03, 0x00000200, 0, 0          ), resp('rd', 0x03, 0, 0,   0xbeefdead ), 
    
  ]
  
  
#-------------------------------------------------------------------------
# Test Case: Capacity misses--asso
#-------------------------------------------------------------------------
# This set of tests designed only for alternative design

def Capacity_misses_asso( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xabababab ), resp('wr', 0x00, 0, 0,   0          ),
    req( 'wr', 0x01, 0x00000010, 0, 0xdeadbeef ), resp('wr', 0x01, 0, 0,   0          ),
    req( 'wr', 0x02, 0x00000020, 0, 0xdeadbeef ), resp('wr', 0x02, 0, 0,   0          ), 
    req( 'wr', 0x03, 0x00000030, 0, 0xdeadbeef ), resp('wr', 0x03, 0, 0,   0          ), 
    req( 'wr', 0x04, 0x00000040, 0, 0xdeadbeef ), resp('wr', 0x04, 0, 0,   0          ), 
    req( 'wr', 0x05, 0x00000050, 0, 0xdeadbeef ), resp('wr', 0x05, 0, 0,   0          ), 
    req( 'wr', 0x06, 0x00000060, 0, 0xdeadbeef ), resp('wr', 0x06, 0, 0,   0          ), 
    req( 'wr', 0x07, 0x00000070, 0, 0xdeadbeef ), resp('wr', 0x07, 0, 0,   0          ), 
    req( 'wr', 0x08, 0x00000080, 0, 0xdeadbeef ), resp('wr', 0x08, 0, 0,   0          ), 
    req( 'wr', 0x09, 0x00000090, 0, 0xdeadbeef ), resp('wr', 0x09, 0, 0,   0          ), 
    req( 'wr', 0x0a, 0x000000a0, 0, 0xdeadbeef ), resp('wr', 0x0a, 0, 0,   0          ), 
    req( 'wr', 0x0b, 0x000000b0, 0, 0xdeadbeef ), resp('wr', 0x0b, 0, 0,   0          ), 
    req( 'wr', 0x0c, 0x000000c0, 0, 0xdeadbeef ), resp('wr', 0x0c, 0, 0,   0          ), 
    req( 'wr', 0x0d, 0x000000d0, 0, 0xdeadbeef ), resp('wr', 0x0d, 0, 0,   0          ), 
    req( 'wr', 0x0e, 0x000000e0, 0, 0xdeadbeef ), resp('wr', 0x0e, 0, 0,   0          ), 
    req( 'wr', 0x0f, 0x000000f0, 0, 0xdeadbeef ), resp('wr', 0x0f, 0, 0,   0          ), 
    req( 'rd', 0x10, 0x00000100, 0, 0          ), resp('rd', 0x10, 0, 0,   0xdeadbeef ),
    req( 'rd', 0x11, 0x00000000, 0, 0          ), resp('rd', 0x11, 0, 0,   0xabababab ), 
    
  ]

#-------------------------------------------------------------------------
# Test Case: Capacity misses--dmap
#-------------------------------------------------------------------------
# This set of tests designed only for baseline design

def Capacity_misses_dmap( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xabababab ), resp('wr', 0x00, 0, 0,   0          ),
    req( 'wr', 0x01, 0x00000010, 0, 0xdeadbeef ), resp('wr', 0x01, 0, 0,   0          ),
    req( 'wr', 0x02, 0x00000020, 0, 0xdeadbeef ), resp('wr', 0x02, 0, 0,   0          ), 
    req( 'wr', 0x03, 0x00000030, 0, 0xdeadbeef ), resp('wr', 0x03, 0, 0,   0          ), 
    req( 'wr', 0x04, 0x00000040, 0, 0xdeadbeef ), resp('wr', 0x04, 0, 0,   0          ), 
    req( 'wr', 0x05, 0x00000050, 0, 0xdeadbeef ), resp('wr', 0x05, 0, 0,   0          ), 
    req( 'wr', 0x06, 0x00000060, 0, 0xdeadbeef ), resp('wr', 0x06, 0, 0,   0          ), 
    req( 'wr', 0x07, 0x00000070, 0, 0xdeadbeef ), resp('wr', 0x07, 0, 0,   0          ), 
    req( 'wr', 0x08, 0x00000080, 0, 0xdeadbeef ), resp('wr', 0x08, 0, 0,   0          ), 
    req( 'wr', 0x09, 0x00000090, 0, 0xdeadbeef ), resp('wr', 0x09, 0, 0,   0          ), 
    req( 'wr', 0x0a, 0x000000a0, 0, 0xdeadbeef ), resp('wr', 0x0a, 0, 0,   0          ), 
    req( 'wr', 0x0b, 0x000000b0, 0, 0xdeadbeef ), resp('wr', 0x0b, 0, 0,   0          ), 
    req( 'wr', 0x0c, 0x000000c0, 0, 0xdeadbeef ), resp('wr', 0x0c, 0, 0,   0          ), 
    req( 'wr', 0x0d, 0x000000d0, 0, 0xdeadbeef ), resp('wr', 0x0d, 0, 0,   0          ), 
    req( 'wr', 0x0e, 0x000000e0, 0, 0xdeadbeef ), resp('wr', 0x0e, 0, 0,   0          ), 
    req( 'wr', 0x0f, 0x000000f0, 0, 0xdeadbeef ), resp('wr', 0x0f, 0, 0,   0          ), 
    req( 'rd', 0x10, 0x00000100, 0, 0          ), resp('rd', 0x10, 0, 0,   0xdeadbeef ),
    req( 'rd', 0x11, 0x00000000, 0, 0          ), resp('rd', 0x11, 0, 0,   0xabababab ), 
    
  ]


# Data to be loaded into memory before running the test

def read_miss_1word_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    ]
      
# Data to be loaded into memory before running the test

def bigdata_preload( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0x01112222,
    0x00000004, 0x03334444,
    0x00000008, 0x05556666,
    0x0000000c, 0x07778888,
    0x00000010, 0x11112222,
    0x00000014, 0x13334444,
    0x00000018, 0x15556666,
    0x0000001c, 0x17778888,
    0x00000020, 0x21112222,
    0x00000024, 0x23334444,
    0x00000028, 0x25556666,
    0x0000002c, 0x27778888,
    0x00000030, 0x31112222,
    0x00000034, 0x33334444,
    0x00000038, 0x35556666,
    0x0000003c, 0x37778888,
    0x00000040, 0x41112222,
    0x00000044, 0x43334444,
    0x00000048, 0x45556666,
    0x0000004c, 0x47778888,
    0x00000050, 0x51112222,
    0x00000054, 0x53334444,
    0x00000058, 0x55556666,
    0x0000005c, 0x57778888,
    0x00000060, 0x61112222,
    0x00000064, 0x63334444,
    0x00000068, 0x65556666,
    0x0000006c, 0x67778888,
    0x00000070, 0x71112222,
    0x00000074, 0x73334444,
    0x00000078, 0x75556666,
    0x0000007c, 0x77778888,
    0x00000080, 0x81112222,
    0x00000084, 0x83334444,
    0x00000088, 0x85556666,
    0x0000008c, 0x87778888,
    0x00000090, 0x91112222,
    0x00000094, 0x93334444,
    0x00000098, 0x95556666,
    0x0000009c, 0x97778888,
    0x000000a0, 0xa1112222,
    0x000000a4, 0xa3334444,
    0x000000a8, 0xa5556666,
    0x000000ac, 0xa7778888,
    0x000000b0, 0xb1112222,
    0x000000b4, 0xb3334444,
    0x000000b8, 0xb5556666,
    0x000000bc, 0xb7778888,
    0x000000c0, 0xc1112222,
    0x000000c4, 0xc3334444,
    0x000000c8, 0xc5556666,
    0x000000cc, 0xc7778888,
    0x000000d0, 0xd1112222,
    0x000000d4, 0xd3334444,
    0x000000d8, 0xd5556666,
    0x000000dc, 0xd7778888,
    0x000000e0, 0xe1112222,
    0x000000e4, 0xe3334444,
    0x000000e8, 0xe5556666,
    0x000000ec, 0xe7778888,
    0x000000f0, 0xf1112222,
    0x000000f4, 0xf3334444,
    0x000000f8, 0xf5556666,
    0x000000fc, 0xf7778888,
    
    0x00000100, 0xdeadbeef,  
    0x00000104, 0x00c0ffee,  
    0x00000108, 0xabcddcba,  
    0x0000010c, 0xdcbaabcd,  
    0x00000114, 0x00000004,
    0x00000118, 0x00000008,
    0x000001c0, 0x12344321,
    0x000001c4, 0x12340000,
    0x00000140, 0x12344321,
    0x00000200, 0xbeefdead,  
    0x00000204, 0x00c0ffee,  
    0x00000208, 0xabcddcba,  
    0x0000020c, 0xdcbaabcd,  
    0x00000210, 0xaaaabbbb,  
    0x00000214, 0xdcccdddd,  
    0x00000218, 0xeeeeffff,  
    0x0000021c, 0x11112222,  
    0x000002C0, 0x12344321,
    0x00000240, 0x12344321,
    0x00000244, 0x12340000,
    0x00000300, 0x77585241,
    0x00000400, 0x00074110,
    
  ]

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Add more test cases
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#----------------------------------------------------------------------
# Banked cache test
#----------------------------------------------------------------------
# The test field in the response message: 0 == MISS, 1 == HIT

# This test case is to test if the bank offset is implemented correctly.
#
# The idea behind this test case is to differentiate between a cache
# with no bank bits and a design has one/two bank bits by looking at cache
# request hit/miss status.

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK:
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# Test table for generic test
#-------------------------------------------------------------------------

test_case_table_generic = mk_test_case_table([
  (                                            "msg_func                        mem_data_func        nbank stall lat src sink"),
  [ "read_hit_1word_clean",                    read_hit_1word_clean,            None,                 0,    0.0,  0,  0,  0    ],
  [ "read_miss_1word_refill_noecvt",           read_miss_1word_refill_noecvt,   read_miss_1word_mem,  0,    0.0,  0,  0,  0    ],
  [ "read_hit_1word_4bank",                    read_hit_1word_clean,            None,                 4,    0.0,  0,  0,  0    ],
  [ "write_hit_1word_clean",                   write_hit_1word_clean,           None,                 0,    0.0,  0,  0,  0    ],
  [ "read_hit_1word_dirty",                    read_hit_1word_dirty,            None,                 0,    0.0,  0,  0,  0    ],
  [ "write_hit_1word_dirty",                   write_hit_1word_dirty,           None,                 0,    0.0,  0,  0,  0    ],
  [ "read_miss_1word_refill_noecvt",           read_miss_1word_refill_noecvt,   read_miss_1word_mem,  0,    0.0,  0,  0,  0    ],
  [ "write_miss_1word_refill_noecvt",          write_miss_1word_refill_noecvt,  bigdata_preload,      0,    0.0,  0,  0,  0    ],
  [ "read_hit_1word_clean_delay",              read_hit_1word_clean,            None,                 0,    0.5,  5,  5,  5    ],
  [ "read_miss_1word_refill_noecvt_delay",     read_miss_1word_refill_noecvt,   read_miss_1word_mem,  0,    0.5,  5,  5,  5    ],
  [ "read_hit_1word_4bank_delay",              read_hit_1word_clean,            None,                 4,    0.5,  5,  5,  5    ],
  [ "write_hit_1word_clean_delay",             write_hit_1word_clean,           None,                 0,    0.8,  6,  7,  8    ],
  [ "read_hit_1word_dirty_delay",              read_hit_1word_dirty,            None,                 0,    0.2,  5,  3,  2    ],
  [ "write_hit_1word_dirty_delay",             write_hit_1word_dirty,           None,                 0,    0.7,  4,  6,  8    ],
  [ "read_miss_1word_refill_noecvt_delay",     read_miss_1word_refill_noecvt,   read_miss_1word_mem,  0,    0.0,  6,  3,  2    ],
  [ "write_miss_1word_refill_noecvt_delay",    write_miss_1word_refill_noecvt,  bigdata_preload,      0,    0.6,  7,  4,  6    ],
  
  
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheFL, test_params.nbank,
                         False, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )

#-------------------------------------------------------------------------
# Test table for set-associative cache (alternative design)
#-------------------------------------------------------------------------

test_case_table_set_assoc = mk_test_case_table([
  (                                           "msg_func                         mem_data_func          nbank stall lat src sink"),
  [ "read_hit_asso",                          read_hit_asso,                    None,                  0,    0.0,  0,  0,  0    ],
  [ "read_miss_refill_ecvt_asso",             read_miss_refill_ecvt_asso,       bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "write_miss_refill_ecvt_asso",            write_miss_refill_ecvt_asso,      bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "fully_used_all_cache_lines_asso",        write_miss_refill_ecvt_asso,      bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "Conflict_misses_asso",                   Conflict_misses_asso,             bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "Capacity_misses_asso",                   Capacity_misses_asso,             bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "read_hit_dmap_delay",                    read_hit_asso,                    None,                  0,    0.6,  5,  7,  8    ],
  [ "read_miss_refill_ecvt_asso_delay",       read_miss_refill_ecvt_asso,       bigdata_preload,       0,    0.5,  7,  3,  2    ],
  [ "write_miss_refill_ecvt_asso_delay",      write_miss_refill_ecvt_asso,      bigdata_preload,       0,    0.8,  4,  6,  7    ],
  [ "fully_used_all_cache_lines_asso_delay",  write_miss_refill_ecvt_asso,      bigdata_preload,       0,    0.6,  8,  9,  2    ],
  [ "Conflict_misses_asso_delay",             Conflict_misses_asso,             bigdata_preload,       0,    0.7,  5,  7,  2    ],
  [ "Capacity_misses_asso_delay",             Capacity_misses_asso,             bigdata_preload,       0,    0.6,  3,  5,  1    ],
  
  
  

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

@pytest.mark.parametrize( **test_case_table_set_assoc )
def test_set_assoc( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem  = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheFL, test_params.nbank,
                         False, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )


#-------------------------------------------------------------------------
# Test table for direct-mapped cache (baseline design)
#-------------------------------------------------------------------------

test_case_table_dir_mapped = mk_test_case_table([
  (                                           "msg_func                         mem_data_func          nbank stall lat src sink"),
  [ "read_hit_dmap",                          read_hit_dmap,                    None,                  0,    0.0,  0,  0,  0    ],
  [ "read_miss_refill_ecvt_dmap",             read_miss_refill_ecvt_dmap,       bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "write_miss_refill_ecvt_damp",            write_miss_refill_ecvt_dmap,      bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "fully_used_all_cache_lines_dmap",        write_miss_refill_ecvt_dmap,      bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "Conflict_misses_dmap",                   Conflict_misses_dmap,             bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "Capacity_misses_dmap",                   Capacity_misses_dmap,             bigdata_preload,       0,    0.0,  0,  0,  0    ],
  [ "read_hit_dmap_delay",                    read_hit_dmap,                    None,                  0,    0.6,  5,  7,  8    ],
  [ "read_miss_refill_ecvt_dmap_delay",       read_miss_refill_ecvt_dmap,       bigdata_preload,       0,    0.5,  7,  3,  2    ],
  [ "write_miss_refill_ecvt_damp_delay",      write_miss_refill_ecvt_dmap,      bigdata_preload,       0,    0.8,  4,  6,  7    ],
  [ "fully_used_all_cache_lines_dmap_delay",  write_miss_refill_ecvt_dmap,      bigdata_preload,       0,    0.6,  8,  9,  2    ],
  [ "Conflict_misses_dmap_delay",             Conflict_misses_dmap,             bigdata_preload,       0,    0.7,  5,  7,  2    ],
  [ "Capacity_misses_dmap_delay",             Capacity_misses_dmap,             bigdata_preload,       0,    0.6,  3,  5,  1    ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

@pytest.mark.parametrize( **test_case_table_dir_mapped )
def test_dir_mapped( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem  = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheFL, test_params.nbank,
                         False, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )
