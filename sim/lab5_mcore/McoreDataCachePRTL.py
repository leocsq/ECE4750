#=========================================================================
# McoreDataCachePRTL.py
#=========================================================================

from pymtl               import *
from pclib.ifcs          import InValRdyBundle, OutValRdyBundle
from pclib.ifcs          import MemReqMsg, MemRespMsg

from lab3_mem   import BlockingCacheAltRTL

from lab5_mcore.CacheNetRTL import CacheNetRTL
from lab5_mcore.MemNetRTL   import MemNetRTL

class McoreDataCachePRTL( Model ):

  def __init__( s ):

    num_cores     = 4
    nopaque_nbits = 8
    icache_nbytes = 256
    dcache_nbytes = 256
    mopaque_nbits = 8
    addr_nbits    = 32
    data_nbits    = 32
    cacheline_nbits = 128

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    s.procreq  = InValRdyBundle [num_cores]( MemReqMsg(mopaque_nbits, addr_nbits, data_nbits) )
    s.procresp = OutValRdyBundle[num_cores]( MemRespMsg(mopaque_nbits, data_nbits) )

    s.mainmemreq  = OutValRdyBundle( MemReqMsg(mopaque_nbits, addr_nbits, cacheline_nbits) )
    s.mainmemresp = InValRdyBundle ( MemRespMsg(mopaque_nbits, cacheline_nbits) )

    # bring these statistics to upper level since the interfaces of this
    # module is hooked up to the networks, not the cache banks

    s.dcache_miss   = OutPort( 4 )
    s.dcache_access = OutPort( 4 )

    #---------------------------------------------------------------------
    # Components
    #---------------------------------------------------------------------

    s.proc_dcache_net   = CacheNetRTL()
    s.dcache            = BlockingCacheAltRTL[num_cores]( num_banks=num_cores )
    s.dcache_refill_net = MemNetRTL()

    #---------------------------------------------------------------------
    # Connections
    #---------------------------------------------------------------------

    for i in xrange( num_cores ):

      # proc <-> proc_dcache_net
      s.connect( s.procreq[i],  s.proc_dcache_net.procreq[i]  )
      s.connect( s.procresp[i], s.proc_dcache_net.procresp[i] )

      # proc_dcache_net <-> dcache bank
      s.connect( s.proc_dcache_net.cachereq[i],  s.dcache[i].cachereq )
      s.connect( s.proc_dcache_net.cacheresp[i], s.dcache[i].cacheresp )

      # dcache bank <-> dcache_refill_net
      s.connect( s.dcache[i].memreq,  s.dcache_refill_net.memreq[i]  )
      s.connect( s.dcache[i].memresp, s.dcache_refill_net.memresp[i] )

    # dcache_refill_net <-> dmemport
    s.connect( s.dcache_refill_net.mainmemreq[0],  s.mainmemreq  )
    s.connect( s.dcache_refill_net.mainmemresp[0], s.mainmemresp )

    # statistics

    @s.combinational
    def collect_cache_statistics():
      s.dcache_miss.value   = concat( s.dcache[3].cacheresp.rdy & s.dcache[3].cacheresp.val & \
                                        (~s.dcache[3].cacheresp.msg.test[0]),
                                      s.dcache[2].cacheresp.rdy & s.dcache[2].cacheresp.val & \
                                        (~s.dcache[2].cacheresp.msg.test[0]),
                                      s.dcache[1].cacheresp.rdy & s.dcache[1].cacheresp.val & \
                                        (~s.dcache[1].cacheresp.msg.test[0]),
                                      s.dcache[0].cacheresp.rdy & s.dcache[0].cacheresp.val & \
                                        (~s.dcache[0].cacheresp.msg.test[0]), )

      s.dcache_access.value = concat( s.dcache[3].cachereq.rdy & s.dcache[3].cachereq.val,
                                      s.dcache[2].cachereq.rdy & s.dcache[2].cachereq.val,
                                      s.dcache[1].cachereq.rdy & s.dcache[1].cachereq.val,
                                      s.dcache[0].cachereq.rdy & s.dcache[0].cachereq.val )

  #-----------------------------------------------------------------------
  # Line tracing
  #-----------------------------------------------------------------------

  def line_trace( s ):
    # cachenet_trace = s.proc_dcache_net.line_trace()
    # dcache_trace = "".join( [x.line_trace() for x in s.dcache] )
    # memnet_trace = s.dcache_refill_net.line_trace()
    # return cachenet_trace + "|" + dcache_trace + "|" + memnet_trace
    return "".join( [x.line_trace() for x in s.dcache] )
