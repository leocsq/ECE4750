#=========================================================================
# MultiCorePRTL.py
#=========================================================================

from pymtl               import *
from pclib.ifcs          import InValRdyBundle, OutValRdyBundle
from pclib.ifcs          import MemMsg

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Include components
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class MultiCorePRTL( Model ):

  def __init__( s ):

    # Parameters

    num_cores       = 4
    mopaque_nbits   = 8
    nopaque_nbits   = 8
    addr_nbits      = 32
    icache_nbytes   = 256
    dcache_nbytes   = 256
    data_nbits      = 32
    cacheline_nbits = 128

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    s.memifc = MemMsg( mopaque_nbits, addr_nbits, cacheline_nbits )

    s.mngr2proc = InValRdyBundle [num_cores]( 32 )
    s.proc2mngr = OutValRdyBundle[num_cores]( 32 )

    s.imemreq  = OutValRdyBundle( s.memifc.req )
    s.imemresp = InValRdyBundle ( s.memifc.resp )

    s.dmemreq  = OutValRdyBundle( s.memifc.req )
    s.dmemresp = InValRdyBundle ( s.memifc.resp )

    # These ports are for statistics. Basically we want to provide the
    # simulator with some useful signals to let the simulator calculate
    # cache miss rate.

    s.stats_en      = OutPort( 1 )
    s.commit_inst   = OutPort( 4 )

    s.icache_miss   = OutPort( 4 )
    s.icache_access = OutPort( 4 )
    s.dcache_miss   = OutPort( 4 )
    s.dcache_access = OutPort( 4 )

    #---------------------------------------------------------------------
    # Components
    #---------------------------------------------------------------------

    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Include components
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    #---------------------------------------------------------------------
    # Connections
    #---------------------------------------------------------------------

    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Connect other components
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    # statistics

    # core #0's stats_en is brought up to the top level
    
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK:  hook up statistics and add icache statistics
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  #-----------------------------------------------------------------------
  # Line tracing
  #-----------------------------------------------------------------------

  def line_trace( s ):

    # This is staffs' line trace, which assume the processors are
    # instantiated in s.proc[], icaches in s.icache[], and the data cache
    # system is instantiated with the name dcache. You can add net to the
    # line trace.
    # Feel free to revamp it based on your need.

    trace = ""
    for i in xrange(len(s.proc)):
      trace += s.icache[i].line_trace() + s.proc[i].line_trace()
    return trace + s.dcache.line_trace()
