#=========================================================================
# BusNetDpathPRTL.py
#=========================================================================
# This model implements 4-port (configurable) simple bus network.

from pymtl         import *
from pclib.ifcs    import NetMsg, InValRdyBundle

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Include components
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class BusNetDpathPRTL( Model ):

  #-----------------------------------------------------------------------
  # Constructor
  #-----------------------------------------------------------------------

  def __init__( s, payload_nbits ):

    # Parameters
    # Your design does not need to support other values

    num_ports    = 4
    opaque_nbits = 8

    # Interface

    msg_type = NetMsg( num_ports, 2**opaque_nbits, payload_nbits )

    s.in_    = InValRdyBundle[num_ports]( msg_type )

    s.out_msg  = OutPort[num_ports]( msg_type )

    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK:
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
