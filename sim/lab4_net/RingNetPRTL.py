#=========================================================================
# RingNetPRTL.py
#=========================================================================

from pymtl        import *
from pclib.ifcs   import InValRdyBundle, OutValRdyBundle, ValRdyBundle
from pclib.ifcs   import NetMsg
from pclib.rtl    import NormalQueue

from RouterPRTL import RouterPRTL

class RingNetPRTL( Model ):

  def __init__( s, payload_nbits = 32 ):

    # Parameters
    # Your design does not need to support other values

    num_ports    = 4
    opaque_nbits = 8 

    srcdest_nbits = clog2( num_ports )

    msg_type = NetMsg(num_ports, 2**opaque_nbits, payload_nbits)

    # Interface

    s.in_ = InValRdyBundle [num_ports]( msg_type )
    s.out = OutValRdyBundle[num_ports]( msg_type )

    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Compose ring network
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  def line_trace( s ):

    return "".join( [ x.line_trace() for x in s.routers] )
