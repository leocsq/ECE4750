#=========================================================================
# BlockingCacheBasePRTL.py
#=========================================================================

from pymtl      import *
from pclib.ifcs import InValRdyBundle, OutValRdyBundle
from pclib.ifcs import MemMsg, MemReqMsg, MemRespMsg

from BlockingCacheBaseCtrlPRTL  import BlockingCacheBaseCtrlPRTL
from BlockingCacheBaseDpathPRTL import BlockingCacheBaseDpathPRTL

# Note on num_banks:
# In a multi-banked cache design, cache lines are interleaved to
# different cache banks, so that consecutive cache lines correspond to a
# different bank. The following is the addressing structure in our
# four-banked data caches:
#
# +--------------------------+--------------+--------+--------+--------+
# |        22b               |     4b       |   2b   |   2b   |   2b   |
# |        tag               |   index      |bank idx| offset | subwd  |
# +--------------------------+--------------+--------+--------+--------+
#
# We will compose four-banked cache in lab5 multi-core lab.

class BlockingCacheBasePRTL( Model ):

  def __init__( s, num_banks=0 ):

    # Parameters

    idx_shamt       = clog2( num_banks ) if num_banks > 0 else 0
    size            = 256  # 256 bytes
    opaque_nbits    = 8    # 8-bit opaque field
    addr_nbits      = 32   # 32-bit address
    data_nbits      = 32   # 32-bit data access
    cacheline_nbits = 128  # 128-bit cacheline

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    # Proc <-> Cache

    s.cachereq  = InValRdyBundle ( MemReqMsg(opaque_nbits, addr_nbits, data_nbits)  )
    s.cacheresp = OutValRdyBundle( MemRespMsg(opaque_nbits, data_nbits) )

    # Cache <-> Mem

    s.memreq    = OutValRdyBundle( MemReqMsg(opaque_nbits, addr_nbits, cacheline_nbits)  )
    s.memresp   = InValRdyBundle ( MemRespMsg(opaque_nbits, cacheline_nbits) )

    s.ctrl      = BlockingCacheBaseCtrlPRTL ( idx_shamt )
    s.dpath     = BlockingCacheBaseDpathPRTL( idx_shamt )

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Connect control unit and datapath
    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  def line_trace( s ):

    #: return ""

    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Create line tracing
    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
