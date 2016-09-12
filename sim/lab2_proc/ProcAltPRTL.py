#=========================================================================
# ProcAltPRTL.py
#=========================================================================

from pymtl             import *
from pclib.ifcs        import InValRdyBundle, OutValRdyBundle
from pclib.ifcs        import MemReqMsg4B, MemRespMsg4B
from pclib.rtl         import SingleElementBypassQueue, TwoElementBypassQueue
from tinyrv2_encoding  import disassemble_inst
from TinyRV2InstPRTL   import inst_dict

#''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Connect components here
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class ProcAltPRTL( Model ):

  def __init__( s, num_cores = 1 ):

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    # Starting F16 we turn core_id into input ports to
    # enable module reusability. In the past it was passed as arguments.

    s.core_id   = InPort( 32 )
    
    # Proc/Mngr Interface

    s.mngr2proc = InValRdyBundle ( 32 )
    s.proc2mngr = OutValRdyBundle( 32 )

    # Instruction Memory Request/Response Interface

    s.imemreq   = OutValRdyBundle( MemReqMsg4B  )
    s.imemresp  = InValRdyBundle ( MemRespMsg4B )

    # Data Memory Request/Response Interface

    s.dmemreq   = OutValRdyBundle( MemReqMsg4B  )
    s.dmemresp  = InValRdyBundle ( MemRespMsg4B )

    # val_W port used for counting commited insts.

    s.commit_inst = OutPort( 1 )

    # stats_en

    s.stats_en    = OutPort( 1 )

    #''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Connect components here
    #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
