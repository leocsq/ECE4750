#=========================================================================
# RouterPRTL.py
#=========================================================================

from pymtl      import *
from pclib.ifcs import NetMsg
from pclib.ifcs import InValRdyBundle, OutValRdyBundle

from RouterDpathPRTL import RouterDpathPRTL
from RouterCtrlPRTL  import RouterCtrlPRTL

#-------------------------------------------------------------------------
# Top-level module
#-------------------------------------------------------------------------

class RouterPRTL( Model ):

  #-----------------------------------------------------------------------
  # Constructor
  #-----------------------------------------------------------------------

  def __init__( s, payload_nbits = 32 ):

    # Parameters
    # Your design does not need to support other values

    nrouters     = 4
    opaque_nbits = 8 

    srcdest_nbits = clog2( nrouters )

    # Interface

    s.router_id = InPort( srcdest_nbits )

    msg_type = NetMsg(nrouters, 2**opaque_nbits, payload_nbits)

    s.in0  = InValRdyBundle ( msg_type )
    s.in1  = InValRdyBundle ( msg_type )
    s.in2  = InValRdyBundle ( msg_type )

    s.out0 = OutValRdyBundle( msg_type )
    s.out1 = OutValRdyBundle( msg_type )
    s.out2 = OutValRdyBundle( msg_type )

    # Components

    s.dpath = RouterDpathPRTL( payload_nbits )
    s.ctrl  = RouterCtrlPRTL ()

    s.connect( s.ctrl.router_id, s.router_id )

    s.connect_auto( s.dpath, s.ctrl )

    s.connect_pairs(
      s.in0,      s.dpath.in0,
      s.in1,      s.dpath.in1,
      s.in2,      s.dpath.in2,

      s.out0.msg, s.dpath.out0_msg,
      s.out0.val, s.ctrl. out0_val,
      s.out0.rdy, s.ctrl. out0_rdy,

      s.out1.msg, s.dpath.out1_msg,
      s.out1.val, s.ctrl. out1_val,
      s.out1.rdy, s.ctrl. out1_rdy,

      s.out2.msg, s.dpath.out2_msg,
      s.out2.val, s.ctrl. out2_val,
      s.out2.rdy, s.ctrl. out2_rdy,
    )

  #-----------------------------------------------------------------------
  # Line-trace
  #-----------------------------------------------------------------------

  def line_trace( s ):
    
    in0_str = s.in0.to_str( "%02s:%1s>%1s" % ( s.in0.msg.opaque, s.in0.msg.src, s.in0.msg.dest ) )
    in1_str = s.in1.to_str( "%02s:%1s>%1s" % ( s.in1.msg.opaque, s.in1.msg.src, s.in1.msg.dest ) )
    in2_str = s.in2.to_str( "%02s:%1s>%1s" % ( s.in2.msg.opaque, s.in2.msg.src, s.in2.msg.dest ) )

    return "({}|{}|{})".format( in0_str, in1_str, in2_str )


