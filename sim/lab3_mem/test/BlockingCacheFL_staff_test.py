#=========================================================================
# BlockingCacheFL_staff_test.py
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
# Test Case: read hit path
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
    req( 'wr', 0x1, 0x00000080, 0, 0x00c0ffee ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'rd', 0x2, 0x00000000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x3, 0x00000080, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x00c0ffee ),
  ]

#-------------------------------------------------------------------------
# Test Case: write hit path
#-------------------------------------------------------------------------

def write_hit_1word_clean( base_addr ):
  return [
    #    type  opq   addr      len data               type  opq   test len data
    req( 'in', 0x00, base_addr, 0, 0x0a0b0c0d ), resp('in', 0x00, 0,   0,  0          ), # write word  0x00000000
    req( 'wr', 0x01, base_addr, 0, 0xbeefbeeb ), resp('wr', 0x01, 1,   0,  0          ), # write word  0x00000000
    req( 'rd', 0x02, base_addr, 0, 0          ), resp('rd', 0x02, 1,   0,  0xbeefbeeb ), # read  word  0x00000000
  ]

#-------------------------------------------------------------------------
# Test Case: read miss path
#-------------------------------------------------------------------------

def read_miss_1word_msg( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
  ]

# Data to be loaded into memory before running the test

def read_miss_1word_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
  ]

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Add more test cases
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

#-------------------------------------------------------------------------
# Test cases: more on read-hit path
#-------------------------------------------------------------------------

def read_hit_1word_dirty( base_addr ):
  return [
    #    type  opq  addr      len data                type  opq  test len data
    req( 'in', 0x0, base_addr, 0, 0xdeadbeef ), resp( 'in', 0x0, 0, 0, 0          ),
    req( 'wr', 0x1, base_addr, 0, 0xbabababa ), resp( 'wr', 0x1, 1, 0, 0          ),
    req( 'rd', 0x2, base_addr, 0, 0          ), resp( 'rd', 0x2, 1, 0, 0xbabababa ),
  ]

def read_hit_1line_clean( base_addr ):
  return [
    req( 'in', 0x0, base_addr,    0, 0xdeadbeef ), resp( 'in', 0x0, 0, 0, 0          ),
    req( 'rd', 0x4, base_addr,    0, 0          ), resp( 'rd', 0x4, 1, 0, 0xdeadbeef ),
    req( 'rd', 0x5, base_addr+4,  0, 0          ), resp( 'rd', 0x5, 1, 0, 0          ),
    req( 'rd', 0x6, base_addr+8,  0, 0          ), resp( 'rd', 0x6, 1, 0, 0          ),
    req( 'rd', 0x7, base_addr+12, 0, 0          ), resp( 'rd', 0x7, 1, 0, 0          ),
  ]

#-------------------------------------------------------------------------
# Test cases: more on write-hit path
#-------------------------------------------------------------------------

def write_hit_1word_dirty( base_addr ):
  return [
    #    type  opq   addr      len data               type  opq   test len data
    req( 'in', 0x00, base_addr, 0, 0x0a0b0c0d ), resp('in', 0x00, 0,   0,  0          ), # write word  0x00000000
    req( 'wr', 0x01, base_addr, 0, 0xbeefbeeb ), resp('wr', 0x01, 1,   0,  0          ), # write word  0x00000000
    req( 'wr', 0x02, base_addr, 0, 0xc0ffeebb ), resp('wr', 0x02, 1,   0,  0          ), # write word  0x00000000
    req( 'rd', 0x03, base_addr, 0, 0          ), resp('rd', 0x03, 1,   0,  0xc0ffeebb ), # read  word  0x00000000
  ]

#----------------------------------------------------------------------
# Test Case: random
#----------------------------------------------------------------------

def random_msgs( base_addr ):

  vmem = [ random.randint(0,0xffffffff) for _ in range(20) ]
  msgs = []

  for i in range(20):
    msgs.extend([
      req( 'wr', i, base_addr+4*i, 0, vmem[i] ), resp( 'wr', i, 2, 0, 0 ),
    ])

  for i in range(20):
    idx = random.randint(0,19)

    if random.randint(0,1):

      correct_data = vmem[idx]
      msgs.extend([
        req( 'rd', i, base_addr+4*idx, 0, 0 ), resp( 'rd', i, 2, 0, correct_data ),
      ])

    else:

      new_data = random.randint(0,0xffffffff)
      vmem[idx] = new_data
      msgs.extend([
        req( 'wr', i, base_addr+4*idx, 0, new_data ), resp( 'wr', i, 2, 0, 0 ),
      ])

  return msgs

#----------------------------------------------------------------------
# Test Case: stream
#----------------------------------------------------------------------

def stream_msgs( base_addr ):
  msgs = []
  for i in range(20):
    msgs.extend([
      req( 'wr', i, base_addr+4*i, 0, i ), resp( 'wr', i, 2, 0, 0 ),
      req( 'rd', i, base_addr+4*i, 0, 0 ), resp( 'rd', i, 2, 0, i ),
    ])

  return msgs

#-------------------------------------------------------------------------
# Test Case: write miss path
#-------------------------------------------------------------------------

def write_miss_1word_msg( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0x0e5ca18d ), # read  word 0x00000000
    req( 'rd', 0x01, 0x00000000, 0, 0          ), resp('rd', 0x01, 1, 0, 0x0e5ca18d ), # read  word 0x00000000
    req( 'rd', 0x02, 0x00000004, 0, 0          ), resp('rd', 0x02, 1, 0, 0x00ba11ad ), # read  word 0x00000004
    req( 'wr', 0x03, 0x00000100, 0, 0x00e1de57 ), resp('wr', 0x03, 0, 0, 0          ), # write word 0x00000100
    req( 'rd', 0x04, 0x00000100, 0, 0          ), resp('rd', 0x04, 1, 0, 0x00e1de57 ), # read  word 0x00000100
  ]

# Data to be loaded into memory before running the test

def write_miss_1word_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0x0e5ca18d,
    0x00000004, 0x00ba11ad,
  ]

#-------------------------------------------------------------------------
# Test Case: force eviction
#-------------------------------------------------------------------------

def evict_msg( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0x0a0b0c0d ), resp('wr', 0x00, 0, 0, 0          ), # write word  0x00000000
    req( 'wr', 0x01, 0x00000004, 0, 0x0e0f0102 ), resp('wr', 0x01, 1, 0, 0          ), # write word  0x00000004
    req( 'rd', 0x02, 0x00000000, 0, 0          ), resp('rd', 0x02, 1, 0, 0x0a0b0c0d ), # read  word  0x00000000
    req( 'rd', 0x03, 0x00000004, 0, 0          ), resp('rd', 0x03, 1, 0, 0x0e0f0102 ), # read  word  0x00000004

    # try forcing some conflict misses to force evictions

    req( 'wr', 0x04, 0x00004000, 0, 0xcafecafe ), resp('wr', 0x04, 0, 0, 0x0        ), # write word  0x00004000
    req( 'wr', 0x05, 0x00004004, 0, 0xebabefac ), resp('wr', 0x05, 1, 0, 0x0        ), # write word  0x00004004
    req( 'rd', 0x06, 0x00004000, 0, 0          ), resp('rd', 0x06, 1, 0, 0xcafecafe ), # read  word  0x00004000
    req( 'rd', 0x07, 0x00004004, 0, 0          ), resp('rd', 0x07, 1, 0, 0xebabefac ), # read  word  0x00004004

    req( 'wr', 0x00, 0x00008000, 0, 0xaaaeeaed ), resp('wr', 0x00, 0, 0, 0x0        ), # write word  0x00008000
    req( 'wr', 0x01, 0x00008004, 0, 0x0e0f0102 ), resp('wr', 0x01, 1, 0, 0x0        ), # write word  0x00008004
    req( 'rd', 0x03, 0x00008004, 0, 0          ), resp('rd', 0x03, 1, 0, 0x0e0f0102 ), # read  word  0x00008004
    req( 'rd', 0x02, 0x00008000, 0, 0          ), resp('rd', 0x02, 1, 0, 0xaaaeeaed ), # read  word  0x00008000

    req( 'wr', 0x04, 0x0000c000, 0, 0xcacafefe ), resp('wr', 0x04, 0, 0, 0x0        ), # write word  0x0000c000
    req( 'wr', 0x05, 0x0000c004, 0, 0xbeefbeef ), resp('wr', 0x05, 1, 0, 0x0        ), # write word  0x0000c004
    req( 'rd', 0x06, 0x0000c000, 0, 0          ), resp('rd', 0x06, 1, 0, 0xcacafefe ), # read  word  0x0000c000
    req( 'rd', 0x07, 0x0000c004, 0, 0          ), resp('rd', 0x07, 1, 0, 0xbeefbeef ), # read  word  0x0000c004

    req( 'wr', 0xf5, 0x0000c004, 0, 0xdeadbeef ), resp('wr', 0xf5, 1, 0, 0x0        ), # write word  0x0000c004
    req( 'wr', 0xd5, 0x0000d004, 0, 0xbeefbeef ), resp('wr', 0xd5, 0, 0, 0x0        ), # write word  0x0000d004
    req( 'wr', 0xe5, 0x0000e004, 0, 0xbeefbeef ), resp('wr', 0xe5, 0, 0, 0x0        ), # write word  0x0000e004
    req( 'wr', 0xc5, 0x0000f004, 0, 0xbeefbeef ), resp('wr', 0xc5, 0, 0, 0x0        ), # write word  0x0000f004

    # now refill those same cache lines to make sure we wrote to the
    # memory earlier and make sure we can read from memory

    req( 'rd', 0x06, 0x00004000, 0, 0          ), resp('rd', 0x06, 0, 0, 0xcafecafe ), # read  word  0x00004000
    req( 'rd', 0x07, 0x00004004, 0, 0          ), resp('rd', 0x07, 1, 0, 0xebabefac ), # read  word  0x00004004
    req( 'rd', 0x02, 0x00000000, 0, 0          ), resp('rd', 0x02, 0, 0, 0x0a0b0c0d ), # read  word  0x00000000
    req( 'rd', 0x03, 0x00000004, 0, 0          ), resp('rd', 0x03, 1, 0, 0x0e0f0102 ), # read  word  0x00000004
    req( 'rd', 0x03, 0x00008004, 0, 0          ), resp('rd', 0x03, 0, 0, 0x0e0f0102 ), # read  word  0x00008004
    req( 'rd', 0x02, 0x00008000, 0, 0          ), resp('rd', 0x02, 1, 0, 0xaaaeeaed ), # read  word  0x00008000
    req( 'rd', 0x06, 0x0000c000, 0, 0          ), resp('rd', 0x06, 0, 0, 0xcacafefe ), # read  word  0x0000c000
    req( 'rd', 0x07, 0x0000c004, 0, 0          ), resp('rd', 0x07, 1, 0, 0xdeadbeef ), # read  word  0x0000c004
    req( 'rd', 0x07, 0x0000d004, 0, 0          ), resp('rd', 0x07, 0, 0, 0xbeefbeef ), # read  word  0x0000d004
    req( 'rd', 0x08, 0x0000e004, 0, 0          ), resp('rd', 0x08, 0, 0, 0xbeefbeef ), # read  word  0x0000e004
    req( 'rd', 0x09, 0x0000f004, 0, 0          ), resp('rd', 0x09, 0, 0, 0xbeefbeef ), # read  word  0x0000f004
  ]

#-------------------------------------------------------------------------
# Test Case: test set associtivity
#-------------------------------------------------------------------------
# Test cases designed for two-way set-associative cache. We should set
# check_test to False if we use it to test set-associative cache.

def set_assoc_msg0( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    # Write to cacheline 0 way 0
    req( 'wr', 0x00, 0x00000000, 0, 0xffffff00), resp( 'wr', 0x00, 0, 0, 0          ),
    req( 'wr', 0x01, 0x00000004, 0, 0xffffff01), resp( 'wr', 0x01, 1, 0, 0          ),
    req( 'wr', 0x02, 0x00000008, 0, 0xffffff02), resp( 'wr', 0x02, 1, 0, 0          ),
    req( 'wr', 0x03, 0x0000000c, 0, 0xffffff03), resp( 'wr', 0x03, 1, 0, 0          ), # LRU:1
    # Write to cacheline 0 way 1
    req( 'wr', 0x04, 0x00001000, 0, 0xffffff04), resp( 'wr', 0x04, 0, 0, 0          ),
    req( 'wr', 0x05, 0x00001004, 0, 0xffffff05), resp( 'wr', 0x05, 1, 0, 0          ),
    req( 'wr', 0x06, 0x00001008, 0, 0xffffff06), resp( 'wr', 0x06, 1, 0, 0          ),
    req( 'wr', 0x07, 0x0000100c, 0, 0xffffff07), resp( 'wr', 0x07, 1, 0, 0          ), # LRU:0
    # Evict way 0
    req( 'rd', 0x08, 0x00002000, 0, 0         ), resp( 'rd', 0x08, 0, 0, 0x00facade ), # LRU:1
    # Read again from same cacheline to see if cache hit properly
    req( 'rd', 0x09, 0x00002004, 0, 0         ), resp( 'rd', 0x09, 1, 0, 0x05ca1ded ), # LRU:1
    # Read from cacheline 0 way 1 to see if cache hits properly,
    req( 'rd', 0x0a, 0x00001004, 0, 0         ), resp( 'rd', 0x0a, 1, 0, 0xffffff05 ), # LRU:0
    # Write to cacheline 0 way 1 to see if cache hits properly
    req( 'wr', 0x0b, 0x0000100c, 0, 0xffffff09), resp( 'wr', 0x0b, 1, 0, 0          ), # LRU:0
    # Read that back
    req( 'rd', 0x0c, 0x0000100c, 0, 0         ), resp( 'rd', 0x0c, 1, 0, 0xffffff09 ), # LRU:0
    # Evict way 0 again
    req( 'rd', 0x0d, 0x00000000, 0, 0         ), resp( 'rd', 0x0d, 0, 0, 0xffffff00 ), # LRU:1
    # Testing cacheline 7 now
    # Write to cacheline 7 way 0
    req( 'wr', 0x10, 0x00000070, 0, 0xffffff00), resp( 'wr', 0x10, 0, 0, 0          ),
    req( 'wr', 0x11, 0x00000074, 0, 0xffffff01), resp( 'wr', 0x11, 1, 0, 0          ),
    req( 'wr', 0x12, 0x00000078, 0, 0xffffff02), resp( 'wr', 0x12, 1, 0, 0          ),
    req( 'wr', 0x13, 0x0000007c, 0, 0xffffff03), resp( 'wr', 0x13, 1, 0, 0          ), # LRU:1
    # Write to cacheline 7 way 1
    req( 'wr', 0x14, 0x00001070, 0, 0xffffff04), resp( 'wr', 0x14, 0, 0, 0          ),
    req( 'wr', 0x15, 0x00001074, 0, 0xffffff05), resp( 'wr', 0x15, 1, 0, 0          ),
    req( 'wr', 0x16, 0x00001078, 0, 0xffffff06), resp( 'wr', 0x16, 1, 0, 0          ),
    req( 'wr', 0x17, 0x0000107c, 0, 0xffffff07), resp( 'wr', 0x17, 1, 0, 0          ), # LRU:0
    # Evict way 0
    req( 'rd', 0x18, 0x00002070, 0, 0         ), resp( 'rd', 0x18, 0, 0, 0x70facade ), # LRU:1
    # Read again from same cacheline to see if cache hits properly
    req( 'rd', 0x19, 0x00002074, 0, 0         ), resp( 'rd', 0x19, 1, 0, 0x75ca1ded ), # LRU:1
    # Read from cacheline 7 way 1 to see if cache hits properly
    req( 'rd', 0x1a, 0x00001074, 0, 0         ), resp( 'rd', 0x1a, 1, 0, 0xffffff05 ), # LRU:0
    # Write to cacheline 7 way 1 to see if cache hits properly
    req( 'wr', 0x1b, 0x0000107c, 0, 0xffffff09), resp( 'wr', 0x1b, 1, 0, 0          ), # LRU:0
    # Read that back
    req( 'rd', 0x1c, 0x0000107c, 0, 0         ), resp( 'rd', 0x1c, 1, 0, 0xffffff09 ), # LRU:0
    # Evict way 0 again
    req( 'rd', 0x1d, 0x00000070, 0, 0         ), resp( 'rd', 0x1d, 0, 0, 0xffffff00 ), # LRU:1
  ]

def set_assoc_mem0( base_addr ):
  return [
    # addr      # data (in int)
    0x00002000, 0x00facade,
    0x00002004, 0x05ca1ded,
    0x00002070, 0x70facade,
    0x00002074, 0x75ca1ded,
  ]

#-------------------------------------------------------------------------
# Test Case: test direct-mapped
#-------------------------------------------------------------------------
# Test cases designed for direct-mapped cache. We should set check_test
# to False if we use it to test set-associative cache.

def dir_mapped_long0_msg( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    # Write to cacheline 0
    req( 'wr', 0x00, 0x00000000, 0, 0xffffff00), resp( 'wr', 0x00, 0, 0, 0          ),
    req( 'wr', 0x01, 0x00000004, 0, 0xffffff01), resp( 'wr', 0x01, 1, 0, 0          ),
    req( 'wr', 0x02, 0x00000008, 0, 0xffffff02), resp( 'wr', 0x02, 1, 0, 0          ),
    req( 'wr', 0x03, 0x0000000c, 0, 0xffffff03), resp( 'wr', 0x03, 1, 0, 0          ),
    # Write to cacheline 0
    req( 'wr', 0x04, 0x00001000, 0, 0xffffff04), resp( 'wr', 0x04, 0, 0, 0          ),
    req( 'wr', 0x05, 0x00001004, 0, 0xffffff05), resp( 'wr', 0x05, 1, 0, 0          ),
    req( 'wr', 0x06, 0x00001008, 0, 0xffffff06), resp( 'wr', 0x06, 1, 0, 0          ),
    req( 'wr', 0x07, 0x0000100c, 0, 0xffffff07), resp( 'wr', 0x07, 1, 0, 0          ),
    # Evict cache 0
    req( 'rd', 0x08, 0x00002000, 0, 0         ), resp( 'rd', 0x08, 0, 0, 0x00facade ),
    # Read again from same cacheline
    req( 'rd', 0x09, 0x00002004, 0, 0         ), resp( 'rd', 0x09, 1, 0, 0x05ca1ded ),
    # Read from cacheline 0
    req( 'rd', 0x0a, 0x00001004, 0, 0         ), resp( 'rd', 0x0a, 0, 0, 0xffffff05 ),
    # Write to cacheline 0
    req( 'wr', 0x0b, 0x0000100c, 0, 0xffffff09), resp( 'wr', 0x0b, 1, 0, 0          ),
    # Read that back
    req( 'rd', 0x0c, 0x0000100c, 0, 0         ), resp( 'rd', 0x0c, 1, 0, 0xffffff09 ),
    # Evict cache 0 again
    req( 'rd', 0x0d, 0x00000000, 0, 0         ), resp( 'rd', 0x0d, 0, 0, 0xffffff00 ),
    # Testing cacheline 7 now
    # Write to cacheline 7
    req( 'wr', 0x10, 0x00000070, 0, 0xffffff00), resp( 'wr', 0x10, 0, 0, 0          ),
    req( 'wr', 0x11, 0x00000074, 0, 0xffffff01), resp( 'wr', 0x11, 1, 0, 0          ),
    req( 'wr', 0x12, 0x00000078, 0, 0xffffff02), resp( 'wr', 0x12, 1, 0, 0          ),
    req( 'wr', 0x13, 0x0000007c, 0, 0xffffff03), resp( 'wr', 0x13, 1, 0, 0          ),
    # Write to cacheline 7
    req( 'wr', 0x14, 0x00001070, 0, 0xffffff04), resp( 'wr', 0x14, 0, 0, 0          ),
    req( 'wr', 0x15, 0x00001074, 0, 0xffffff05), resp( 'wr', 0x15, 1, 0, 0          ),
    req( 'wr', 0x16, 0x00001078, 0, 0xffffff06), resp( 'wr', 0x16, 1, 0, 0          ),
    req( 'wr', 0x17, 0x0000107c, 0, 0xffffff07), resp( 'wr', 0x17, 1, 0, 0          ),
    # Evict cacheline 7
    req( 'rd', 0x18, 0x00002070, 0, 0         ), resp( 'rd', 0x18, 0, 0, 0x70facade ),
    # Read again from same cacheline
    req( 'rd', 0x19, 0x00002074, 0, 0         ), resp( 'rd', 0x19, 1, 0, 0x75ca1ded ),
    # Read from cacheline 7
    req( 'rd', 0x1a, 0x00001074, 0, 0         ), resp( 'rd', 0x1a, 0, 0, 0xffffff05 ),
    # Write to cacheline 7 way 1 to see if cache hits properly
    req( 'wr', 0x1b, 0x0000107c, 0, 0xffffff09), resp( 'wr', 0x1b, 1, 0, 0          ),
    # Read that back
    req( 'rd', 0x1c, 0x0000107c, 0, 0         ), resp( 'rd', 0x1c, 1, 0, 0xffffff09 ),
    # Evict cacheline 0 again
    req( 'rd', 0x1d, 0x00000070, 0, 0         ), resp( 'rd', 0x1d, 0, 0, 0xffffff00 ),
  ]

def dir_mapped_long0_mem( base_addr ):
  return [
    # addr      # data (in int)
    0x00002000, 0x00facade,
    0x00002004, 0x05ca1ded,
    0x00002070, 0x70facade,
    0x00002074, 0x75ca1ded,
  ]

#----------------------------------------------------------------------
# Enhanced random tests
#----------------------------------------------------------------------
# This set of random tests uses a cache model that properly tracks
# hits and misses, and should completely accurately model eviction
# behavior. The model is split up into a hit/miss tracker, and a
# transaction generator, so that the hit/miss tracker can be reused
# in an FL model

class HitMissTracker:
  def __init__(self, size, nways, nbanks, linesize):
    # Compute various sizes
    self.nways = nways
    self.linesize = linesize
    self.nlines = int(size / linesize)
    self.nsets = int(self.nlines / self.nways)
    self.nbanks = nbanks

    # Compute how the address is sliced
    self.offset_start = 0
    self.offset_end = self.offset_start + int(math.log(linesize, 2))
    self.bank_start = self.offset_end
    if nbanks > 0:
      self.bank_end = self.bank_start + int(math.log(nbanks, 2))
    else:
      self.bank_end = self.bank_start
    self.idx_start = self.bank_end
    self.idx_end = self.idx_start + int(math.log(self.nsets, 2))
    self.tag_start = self.idx_end
    self.tag_end = 32

    # Initialize the tag and valid array
    # Both arrays are of the form line[idx][way]
    # Note that line[idx] is a one-element array for
    # a direct-mapped cache
    self.line = []
    self.valid = []
    for n in xrange(self.nlines):
      self.line.insert(n, [Bits(32, 0) for x in xrange(nways)])
      self.valid.insert(n, [False for x in xrange(nways)])

    # Initialize the lru array
    # Implemented as an array for each set index
    # lru[idx][0] is the most recently used
    # lru[idx][-1] is the least recently used
    self.lru = []
    for n in xrange(self.nsets):
      self.lru.insert(n, [x for x in range(nways)])

  # Generate the components of an address
  # Ignores the bank bits, since they don't affect the behavior
  # (and may not even exist)
  def split_address(self, addr):
    addr = Bits(32, addr)
    offset = addr[self.offset_start:self.offset_end]
    idx = addr[self.idx_start:self.idx_end]
    tag = addr[self.tag_start:self.tag_end]
    return (tag, idx, offset)

  # Update the LRU status, given that a hit just occurred
  def lru_hit(self, idx, way):
    self.lru[idx].remove(way)
    self.lru[idx].insert(0, way)

  # Get the least recently used way for an index
  # The LRU is always the last element in the list
  def lru_get(self, idx):
    return self.lru[idx][-1]

  # Perform a tag check, and update lru if a hit occurs
  def tag_check(self, tag, idx):
    for way in range(self.nways):
      if self.valid[idx][way] and self.line[idx][way] == tag:
        # Whenever tag check hits, update the set's lru array
        self.lru_hit(idx, way)
        return True
    return False

  # Update the tag array due to a value getting fetched from memory
  def refill(self, tag, idx):
    victim = self.lru_get(idx)
    self.line[idx][victim] = tag
    self.valid[idx][victim] = True
    self.lru_hit(idx, victim)

  # Simulate accessing an address. Returns True if a hit occurred,
  # False on miss
  def access_address(self, addr):
    (tag, idx, offset) = self.split_address(addr)
    hit = self.tag_check(tag, idx)
    if not hit:
      self.refill(tag, idx)

    return hit

class ModelCache:
  def __init__(self, size, nways, nbanks, linesize, mem=None):
    # The hit/miss tracker
    self.tracker = HitMissTracker(size, nways, nbanks, linesize)

    self.mem = {}

    # Unpack any initial values of memory into a dict (has easier lookup)
    #
    # zip is used here to convert the mem array into an array of
    # (addr, value) pairs (which it really should be in the first
    # place)
    if mem:
      for addr, value in zip(mem[::2], mem[1::2]):
        self.mem[addr] = Bits(32, value)

    # The transactions list contains the requests and responses for
    # the stream of read/write calls on this model
    self.transactions = []

  def check_hit(self, addr):
    # Tracker returns boolean, need to convert to 1 or 0 to use
    # in the "test" field of the response
    if self.tracker.access_address(addr):
      return 1
    else:
      return 0

  def read(self, addr):
    hit = self.check_hit(addr)

    if addr.int() in self.mem:
      value = self.mem[addr.int()]
    else:
      value = Bits(32, 0)

    opaque = random.randint(0,255)
    self.transactions.append(req('rd', opaque, addr, 0, 0))
    self.transactions.append(resp('rd', opaque, hit, 0, value))

  def write(self, addr, value):
    value = Bits(32, value)
    hit = self.check_hit(addr)

    self.mem[addr.int()] = value

    opaque = random.randint(0,255)
    self.transactions.append(req('wr', opaque, addr, 0, value))
    self.transactions.append(resp('wr', opaque, hit, 0, 0))
    
  def get_transactions(self):
    return self.transactions

# Fills 1K of memory randomly
def rand_mem( base_addr ):
  random.seed(0x00c0ffee)

  # This double list comprehension looks really icky, but my prior comments seem to suggest
  # that it was written this way for efficiency, whatever that meant at the time. The first
  # for is the outer loop, generating the addresses of 1K worth of memory. The second for
  # takes a tuple of (address, value), and turns it into two separate array elements, so that
  # it can be loaded into a test memory. ModelCache will undo the effects of the second for
  # when it reads the array in
  return [val for n in xrange(1024/4) for val in (n*4, random.randint(0x00000000, 0xffffffff))]

RAND_LEN = 100 # Number of transactions per random test
ADDR_LEN = 20  # How many bits are allowed in a random address
#-------------------------------------------------------------------------
# Test: Write random data to random low addresses
#-------------------------------------------------------------------------
def rand_write_lowaddr( base_addr, size, nways, nbanks, linesize, mem=None ):
  random.seed(0xdeadbeef)
  model = ModelCache(size, nways, nbanks, linesize, mem)
  for i in xrange(RAND_LEN):
    addr = random.randint(0x00000000, 0x00000400)
    addr = addr & Bits(32, 0xfffffffc) # Align the address
    value = random.getrandbits(32)
    model.write(addr, value)
  return model.get_transactions()

#-------------------------------------------------------------------------
# Test: Read random data from random low addresses
#-------------------------------------------------------------------------
def rand_read_lowaddr( base_addr, size, nways, nbanks, linesize, mem=None ):
  random.seed(0xd00dd00d)
  model = ModelCache(size, nways, nbanks, linesize, mem)
  for i in xrange(RAND_LEN):
    addr = random.randint(0x00000000, 0x00000400)
    addr = addr & Bits(32, 0xfffffffc) # Align the address
    model.read(addr)
  return model.get_transactions()

#-------------------------------------------------------------------------
# Test: Randomly read or write random data from random low addresses
#-------------------------------------------------------------------------
def rand_rw_lowaddr( base_addr, size, nways, nbanks, linesize, mem=None ):
  random.seed(0xbaadf00d)
  model = ModelCache(size, nways, nbanks, linesize, mem)
  for i in xrange(RAND_LEN):
    addr = random.randint(0x00000000, 0x00000400)
    addr = addr & Bits(32, 0xfffffffc) # Align the address
    if random.randint(0,1):
      # Write something
      value = random.getrandbits(32)
      model.write(addr, value)
    else:
      # Read something
      model.read(addr)
  return model.get_transactions()

#-------------------------------------------------------------------------
# Test: Randomly read or write random data from random low addresses
#       Replaces with an operation on a small pool of addresses 60% of the time
#-------------------------------------------------------------------------
REPEAT_LEN = 10
REPEAT_CHANCE = 0.6
def rand_rw_repeat( base_addr, size, nways, nbanks, linesize, mem=None ):
  random.seed(0x12345678)
  model = ModelCache(size, nways, nbanks, linesize, mem)
  rep = [random.getrandbits(ADDR_LEN) for x in xrange(REPEAT_LEN)]
  for i in xrange(RAND_LEN):
    if random.random() < REPEAT_CHANCE:
      addr = rep[random.randint(0,REPEAT_LEN-1)]
    else:
      addr = random.getrandbits(ADDR_LEN)
    
    addr = addr & Bits(32, 0xfffffffc) # Align the address
    if random.randint(0,1):
      # Write something
      value = random.getrandbits(32)
      model.write(addr, value)
    else:
      # Read something
      model.read(addr)
  return model.get_transactions()

#-------------------------------------------------------------------------
# Test: Read/write random data to each address sequentially
#-------------------------------------------------------------------------
def rand_rw_stride( base_addr, size, nways, nbanks, linesize, mem=None ):
  random.seed(0xaaaaaaaa)
  model = ModelCache(size, nways, nbanks, linesize, mem)
  for i in xrange(RAND_LEN):
    addr = i * 4

    addr = addr & Bits(32, 0xfffffffc) # Align the address
    if random.randint(0,1):
      # Write something
      value = random.getrandbits(32)
      model.write(addr, value)
    else:
      # Read something
      model.read(addr)
  return model.get_transactions()

#-------------------------------------------------------------------------
# Test: Read/write random data to every 3rd address
#-------------------------------------------------------------------------
STRIDE_LEN = 3
def rand_rw_vstride( base_addr, size, nways, nbanks, linesize, mem=None ):
  random.seed(0xbbbbbbbb)
  model = ModelCache(size, nways, nbanks, linesize, mem)
  for i in xrange(RAND_LEN):
    addr = i * 4 * STRIDE_LEN

    addr = addr & Bits(32, 0xfffffffc) # Align the address
    if random.randint(0,1):
      # Write something
      value = random.getrandbits(32)
      model.write(addr, value)
    else:
      # Read something
      model.read(addr)
  return model.get_transactions()

#-------------------------------------------------------------------------
# Test: Read/write random data to every address in sequence
#       Replaces an operation with a query to a preselected
#       address 60% of the time
#-------------------------------------------------------------------------
def rand_rw_rstride( base_addr, size, nways, nbanks, linesize, mem=None ):
  random.seed(0xcccccccc)
  model = ModelCache(size, nways, nbanks, linesize, mem)
  rep = [random.getrandbits(ADDR_LEN) for x in xrange(REPEAT_LEN)]
  for i in xrange(RAND_LEN):
    if random.random() < REPEAT_CHANCE:
      addr = rep[random.randint(0,REPEAT_LEN-1)]
    else:
      addr = i * 4

    addr = addr & Bits(32, 0xfffffffc) # Align the address
    if random.randint(0,1):
      # Write something
      value = random.getrandbits(32)
      model.write(addr, value)
    else:
      # Read something
      model.read(addr)
  return model.get_transactions()

#-------------------------------------------------------------------------
# Test: Read/write random data to random addresses
#       Replaces an operation with a query to a previous
#       address 60% of the time
#-------------------------------------------------------------------------
HIST_LEN = 20
HIST_CHANCE = 0.6
def rand_rw_hist( base_addr, size, nways, nbanks, linesize, mem=None ):
  random.seed(0xbaadf00d)
  model = ModelCache(size, nways, nbanks, linesize, mem)
  hist = [random.getrandbits(ADDR_LEN) for x in xrange(HIST_LEN)]
  for i in xrange(RAND_LEN):
    if random.random() < HIST_CHANCE:
      addr = hist[random.randint(0,HIST_LEN-1)]
    else:
      addr = random.getrandbits(ADDR_LEN)
    
    # Update the address history
    hist.pop()
    hist.insert(0, addr)
    
    addr = addr & Bits(32, 0xfffffffc) # Align the address
    if random.randint(0,1):
      # Write something
      value = random.getrandbits(32)
      model.write(addr, value)
    else:
      # Read something
      model.read(addr)
  return model.get_transactions()

test_case_table_enhanced_random = mk_test_case_table([
  (                             "msg_func             mem_data_func  nbank stall lat src sink"),
  # No latency
  [ "rand_write_lowaddr",       rand_write_lowaddr,   None,          0,    0.0,  0,  0,  0    ],
  [ "rand_read_lowaddr",        rand_read_lowaddr,    rand_mem,      0,    0.0,  0,  0,  0    ],
  [ "rand_rw_lowaddr",          rand_rw_lowaddr,      rand_mem,      0,    0.0,  0,  0,  0    ],
  [ "rand_rw_repeat",           rand_rw_repeat,       rand_mem,      0,    0.0,  0,  0,  0    ],
  [ "rand_rw_stride",           rand_rw_stride,       rand_mem,      0,    0.0,  0,  0,  0    ],
  [ "rand_rw_vstride",          rand_rw_vstride,      rand_mem,      0,    0.0,  0,  0,  0    ],
  [ "rand_rw_rstride",          rand_rw_rstride,      rand_mem,      0,    0.0,  0,  0,  0    ],
  [ "rand_rw_hist",             rand_rw_hist,         rand_mem,      0,    0.0,  0,  0,  0    ],

  # With all latencies
  [ "rand_write_lowaddr_stall", rand_write_lowaddr,   None,          0,    0.3,  3,  4,  5    ],
  [ "rand_read_lowaddr_stall",  rand_read_lowaddr,    rand_mem,      0,    0.3,  3,  4,  5    ],
  [ "rand_rw_lowaddr_stall",    rand_rw_lowaddr,      rand_mem,      0,    0.3,  3,  4,  5    ],
  [ "rand_rw_repeat_stall",     rand_rw_repeat,       rand_mem,      0,    0.3,  3,  4,  5    ],
  [ "rand_rw_stride_stall",     rand_rw_stride,       rand_mem,      0,    0.3,  3,  4,  5    ],
  [ "rand_rw_vstride_stall",    rand_rw_vstride,      rand_mem,      0,    0.3,  3,  4,  5    ],
  [ "rand_rw_rstride_stall",    rand_rw_rstride,      rand_mem,      0,    0.3,  3,  4,  5    ],
  [ "rand_rw_hist_stall",       rand_rw_hist,         rand_mem,      0,    0.3,  3,  4,  5    ],

])

@pytest.mark.parametrize( **test_case_table_enhanced_random )
def test_enhanced_random( test_params, dump_vcd ):
  if test_params.mem_data_func != None:
    mem  = test_params.mem_data_func( 0 )
  else:
    mem = None

  msgs = test_params.msg_func( 0, 256, 1, test_params.nbank, 16, mem )
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

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

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
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

# Test case:  the last request should hit
#
# I first designed a test case for 2-way set-associative cache. The last
# request should hit only if students implement the correct index bit to
# be [6:9]. If they implement the index bit to be [4:7] or [5:8],
# the last request is a miss, which is wrong. See below for explanation.
#
# 2-way set-associative
#
# no bank(should fail):
#      idx
#  0 0 000 0000
#  1 0 000 0000
# 10 0 000 0000
# idx: 0, 0, 0 so the third one with tag 10 will evict the first one 00
#
# 2-bank(should fail):
#     idx bk
# 0 0 000 0 0000
# 0 1 000 0 0000
# 1 0 000 0 0000
# idx: 0, 0, 0 so the third one with tag 10 will evict the first one 00
#
# 4-bank(correct):
#   idx  bk
# 0 0 00 00 0000
# 0 1 00 00 0000
# 1 0 00 00 0000
# idx: 0, 4, 0 so the third one with tag 10 won't evict anything

#.........................................................................
# Then I accidentally found that, this test case also works for the
# baseline direct-mapped cache. Yay!
#.........................................................................
# Direct-mapped
#
# no bank(should fail):
#    idx
#  0 0000 0000
#  1 0000 0000
# 10 0000 0000
# idx: 0, 0, 0 so the third one with tag 10 will evict the first one 00
#
# 2-bank(should fail):
#    idx  bk
# 0 0 000 0 0000
# 0 1 000 0 0000
# 1 0 000 0 0000
# idx: 0, 8, 0 so the third one with tag 10 will evict the first one 00
#
# 4-bank(correct):
#  idx  bk
# 00 00 00 0000
# 01 00 00 0000
# 10 00 00 0000
# idx: 0, 4, 8 so the third one with tag 10 won't evict anything!

def bank_test( base_addr ):
  return [
    #    type  opq  addr       len data                type  opq  test len data
    req( 'rd', 0x0, 0x00000000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xdeadbeef ),
    req( 'rd', 0x1, 0x00000100, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x00c0ffee ),
    req( 'rd', 0x2, 0x00000200, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xffffffff ),
    req( 'rd', 0x3, 0x00000000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xdeadbeef ),
  ]

def bank_test_data( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000100, 0x00c0ffee,
    0x00000200, 0xffffffff,
  ]
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

#-------------------------------------------------------------------------
# Test table for generic test
#-------------------------------------------------------------------------

test_case_table_generic = mk_test_case_table([
  (                         "msg_func               mem_data_func         nbank stall lat src sink"),
  [ "read_hit_1word_clean",  read_hit_1word_clean,  None,                 0,    0.0,  0,  0,  0    ],
  [ "read_miss_1word",       read_miss_1word_msg,   read_miss_1word_mem,  0,    0.0,  0,  0,  0    ],
  [ "read_hit_1word_4bank",  read_hit_1word_clean,  None,                 4,    0.0,  0,  0,  0    ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  [ "read_hit_1word_dirty",  read_hit_1word_dirty,  None,                 0,    0.0,  0,  0,  0    ],
#  [ "read_hit_1line_clean",  read_hit_1line_clean,  None,                 0.0,  0,  0,  0    ],
  [ "write_hit_1word_clean", write_hit_1word_clean, None,                 0,    0.0,  0,  0,  0    ],
  [ "write_hit_1word_dirty", write_hit_1word_dirty, None,                 0,    0.0,  0,  0,  0    ],
  [ "random",                random_msgs,           None,                 0,    0.0,  0,  0,  0    ],
  [ "random_stall0.5_lat0",  random_msgs,           None,                 0,    0.5,  0,  0,  0    ],
  [ "random_stall0.0_lat4",  random_msgs,           None,                 0,    0.0,  4,  0,  0    ],
  [ "random_stall0.5_lat4",  random_msgs,           None,                 0,    0.5,  4,  0,  0    ],
  [ "stream",                stream_msgs,           None,                 0,    0.0,  0,  0,  0    ],
  [ "stream_stall0.5_lat0",  stream_msgs,           None,                 0,    0.5,  0,  0,  0    ],
  [ "stream_stall0.0_lat4",  stream_msgs,           None,                 0,    0.0,  4,  0,  0    ],
  [ "stream_stall0.5_lat4",  stream_msgs,           None,                 0,    0.5,  4,  0,  0    ],
  [ "write_miss_1word",      write_miss_1word_msg,  write_miss_1word_mem, 0,    0.0,  0,  0,  0    ],
  [ "evict",                 evict_msg,             None,                 0,    0.0,  0,  0,  0    ],
  [ "evict_stall0.5_lat0",   evict_msg,             None,                 0,    0.5,  0,  0,  0    ],
  [ "evict_stall0.0_lat4",   evict_msg,             None,                 0,    0.0,  4,  0,  0    ],
  [ "evict_stall0.5_lat4",   evict_msg,             None,                 0,    0.5,  4,  0,  0    ],
  [ "bank_test",             bank_test,             bank_test_data,       4,    0.0,  0,  0,  0    ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

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
  (                             "msg_func        mem_data_func    nbank stall lat src sink"),
  [ "read_hit_asso",             read_hit_asso,  None,            0,    0.0,  0,  0,  0    ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  [ "set_assoc_test0",           set_assoc_msg0, set_assoc_mem0,  0,    0.0,  0,  0,  0    ],
  [ "set_assoc_test0_lat4_3x14", set_assoc_msg0, set_assoc_mem0,  0,    0.5,  4,  3,  14   ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

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
  (                                  "msg_func              mem_data_func          nbank stall lat src sink"),
  [ "read_hit_dmap",                  read_hit_dmap,        None,                  0,    0.0,  0,  0,  0    ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\/

  [ "dir_maped_test_long0",           dir_mapped_long0_msg, dir_mapped_long0_mem,  0,    0.0,  0,  0,  0    ],
  [ "dir_maped_test_long0_lat4_3x14", dir_mapped_long0_msg, dir_mapped_long0_mem,  0,    0.5,  4,  3,  14   ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/\

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
