#=========================================================================
# BlockingCacheBaseCtrlPRTL.py
#=========================================================================

from pymtl      import *

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Include necessary files
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class BlockingCacheBaseCtrlPRTL( Model ):

  def __init__( s, idx_shamt ):

    # Parameters

    abw = 32  # Short name for addr bitwidth
    dbw = 32  # Short name for data bitwidth
    clw = 128 # Short name for cacheline bitwidth
    nbl = 16  # Short name for number of cache blocks, 256*8/128 = 16
    idw = 4   # Short name for index width, clog2(16) = 4
    ofw = 4   # Short name for offset bit width, clog2(128/8) = 4
    nby = 16  # Short name for number of cache blocks per way, 16/1 = 16

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    # Cache request

    s.cachereq_val  = InPort ( 1 )
    s.cachereq_rdy  = OutPort( 1 )

    # Cache response

    s.cacheresp_val = OutPort( 1 )
    s.cacheresp_rdy = InPort ( 1 )

    # Memory request

    s.memreq_val    = OutPort( 1 )
    s.memreq_rdy    = InPort ( 1 )

    # Memory response

    s.memresp_val   = InPort ( 1 )
    s.memresp_rdy   = OutPort( 1 )

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Implement control unit
    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
