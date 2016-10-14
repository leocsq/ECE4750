#=========================================================================
# BlockingCacheAltDpathPRTL.py
#=========================================================================

from pymtl      import *
from pclib.ifcs import MemMsg, MemReqMsg, MemRespMsg

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Include necessary files
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class BlockingCacheAltDpathPRTL( Model ):

  def __init__( s, idx_shamt ):

    # Parameters

    o   = 8   # Short name for opaque bitwidth
    abw = 32  # Short name for addr bitwidth
    dbw = 32  # Short name for data bitwidth
    clw = 128 # Short name for cacheline bitwidth
    nbl = 16  # Short name for number of cache blocks, 256*8/128 = 16
    idw = 3   # Short name for index width, clog2(16)-1 = 3 (-1 for 2-way)
    ofw = 4   # Short name for offset bit width, clog2(128/8) = 4
    nby = 16  # Short name for number of cache blocks per way, 16/1 = 16
    # In the lab, to simplify things, we always use all bits except for
    # the offset bits to represent the tag instead of storing the 25-bit
    # tag and concatenate everytime with the index bits and even the bank
    # bits to get the address of a cacheline
    tgw = 28  # Short name for tag bit width, 32-4 = 28

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    # Cache request

    s.cachereq_msg  = InPort ( MemReqMsg(o, abw, dbw) )

    # Cache response

    s.cacheresp_msg = OutPort( MemRespMsg(o, dbw) )

    # Memory request

    s.memreq_msg    = OutPort( MemReqMsg(o, abw, clw) )

    # Memory response

    s.memresp_msg   = InPort ( MemRespMsg(o, clw) )

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Implement datapath
    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
