#=========================================================================
# BusNetPRTL.py
#=========================================================================
# This model implements 4-port (configurable) simple crossbar network.

from pymtl         import *
from pclib.ifcs    import InValRdyBundle, OutValRdyBundle
from pclib.ifcs    import NetMsg

from BusNetCtrlPRTL  import BusNetCtrlPRTL
from BusNetDpathPRTL import BusNetDpathPRTL

class BusNetPRTL( Model ):

  #-----------------------------------------------------------------------
  # Constructor
  #-----------------------------------------------------------------------

  def __init__( s, payload_nbits = 32 ):

    # Parameters
    # Your design does not need to support other values

    num_ports    = 4
    opaque_nbits = 8

    # Interface

    msg_type = NetMsg( num_ports, 2**opaque_nbits, payload_nbits )

    s.in_    = InValRdyBundle [num_ports]( msg_type )
    s.out    = OutValRdyBundle[num_ports]( msg_type )

    # Components

    s.dpath = BusNetDpathPRTL( payload_nbits )
    s.ctrl  = BusNetCtrlPRTL ()

    s.connect_auto( s.ctrl, s.dpath )

    for i in xrange( num_ports ):
      s.connect_pairs(
        s.in_[i], s.dpath.in_[i],

        s.out[i].msg, s.dpath.out_msg[i],
        s.out[i].val, s.ctrl. out_val[i],
        s.out[i].rdy, s.ctrl. out_rdy[i],
      )

  def line_trace( s ):

    traces = []
    for i in xrange( len(s.in_) ):
      in_ = s.in_[ i ]
      out = s.out[ i ]
      in_str  = in_.to_str( "%02s:%1s>%1s" % ( in_.msg.opaque, in_.msg.src, in_.msg.dest ) )
      out_str = out.to_str( "%02s:%1s>%1s" % ( out.msg.opaque, out.msg.src, out.msg.dest ) )
      traces += [ '({}|{})'.format( in_str, out_str ) ]

    return ''.join( traces )

