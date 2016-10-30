#=========================================================================
# RouterDpathPRTL.py
#=========================================================================
# This model implements a 3-port router

from pymtl         import *
from pclib.ifcs    import NetMsg, InValRdyBundle
from pclib.rtl     import NormalQueue, Crossbar

class RouterDpathPRTL( Model ):

  #-----------------------------------------------------------------------
  # Constructor
  #-----------------------------------------------------------------------

  def __init__( s, payload_nbits = 32 ):

    # Parameters
    # Your design does not need to support other values

    nrouters     = 4
    opaque_nbits = 8

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    msg_type = NetMsg( nrouters, 2**opaque_nbits, payload_nbits)

    s.in0 = InValRdyBundle( msg_type )
    s.in1 = InValRdyBundle( msg_type )
    s.in2 = InValRdyBundle( msg_type )

    s.out0_msg  = OutPort( msg_type )
    s.out1_msg  = OutPort( msg_type )
    s.out2_msg  = OutPort( msg_type )

    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Other interfaces between dpath and ctrl 
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    #---------------------------------------------------------------------
    # Components
    #---------------------------------------------------------------------

    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Dpath components
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
