#=========================================================================
# MemNetPRTL.py
#========================================================================= 
#
# num_reqers (n): num of requester ports, {1,2,..,n}
# num_reqees (m): num of requestee ports, {1,2,..,m}
#
# reqer_req:  the memory request port of the requesters  -- inport
# reqer_resp: the memory response port of the requesters -- outport
#
# reqee_req:  the memory request port of the requestees  -- outport
# reqee_resp: the memory response port of the requestees -- inport
#
# Because the request net receives requests from requesters and forward
# them to the requestees, the request port from requester is an inport
# for this module, and the request port to requestee is an outport.
# The response network is the other way around.
#
#                  +-----------------------------------+
#                  |            MemNet Module          |
#                  |            +---------+            |
#                  |            |         |            |
#                  |  +-----+   |         |            |
# reqer_req [ 0 ]--|M>|     |-N>|  req    |   +-----+  |
#                  |  |  U  |   |         |-N>|     |-M|->reqee_req [ 0 ]
# reqer_resp[ 0 ]<-|M-| [0] |<N-|         |   |  D  |  |
#                  |  +-----+   |  and    |<N-| [0] |<M|<-reqee_resp[ 0 ]
#                  |  +-----+   |         |   +-----+  |
# reqer_req [ 1 ]--|M>|     |-N>|         |            |
#                  |  |  U  |   |  resp   |            |
# reqer_resp[ 1 ]<-|M-| [1] |<N-|         |            |
#                  |  +-----+   |         |    .....   |
#                  |            | network |            |
#     ......       |   .....    |         |            |
#                  |            |   in    |   +-----+  |
#                  |  +-----+   |   the   |-N>|     |-M|->reqee_req [m-1]
# reqer_req [n-1]--|M>|     |-N>|   same  |   |  D  |  |
#                  |  |  U  |   |   box   |<N-| [0] |<M|<-reqee_resp[m-1]
# reqer_resp[n-1]<-|M-|[n-1]|<N-|         |   +-----+  |
#                  |  +-----+   |         |            |
#                  |            |         |            |
#                  |            +---------+            |
#                  |  M - memory, N - network          |
#                  +-----------------------------------+
#
# This is the architecture of a general memory network. In MemNet, there
# are 4 requesters and 1 requestee (memory port). However, we will let the
# network have 4 ports but only use one to unify the network message
# format.
# Requesters are renamed to cachereqs since the requesters are basically
# caches. The requestee is the memory port.

from pymtl               import *
from pclib.ifcs          import InValRdyBundle, OutValRdyBundle
from pclib.ifcs          import MemMsg, MemReqMsg, MemRespMsg

from lab4_net import BusNetRTL, RingNetRTL

from MsgAdapters import UpstreamMsgAdapter as UpsAdapter
from MsgAdapters import DownstreamMsgAdapter as DownsAdapter

class MemNetPRTL( Model ):

  def __init__( s ):

    # Parameters

    num_reqers    = 4 # 4 data caches
    num_reqees    = 1 # 1 memory port
    num_ports     = max( num_reqers, num_reqees ) # We still have 4 ports

    nopaque_nbits = 8
    mopaque_nbits = 8
    addr_nbits    = 32
    data_nbits    = 128 # MemNet deals with 128 bit refill requests

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    s.memifc      = MemMsg( mopaque_nbits, addr_nbits, data_nbits )
    s.mainmemifc  = MemMsg( mopaque_nbits, addr_nbits, data_nbits )

    s.memreq      = InValRdyBundle [num_ports]( s.memifc.req  )
    s.memresp     = OutValRdyBundle[num_ports]( s.memifc.resp )

    s.mainmemreq  = OutValRdyBundle[num_ports]( s.mainmemifc.req  )
    s.mainmemresp = InValRdyBundle [num_ports]( s.mainmemifc.resp )

    #---------------------------------------------------------------------
    # Components
    #---------------------------------------------------------------------

    single_reqee = True  # 1 memory port so single reqee
    single_reqer = False # 4 caches so not single reqer 

    s.u_adpt = UpsAdapter[num_ports]( single_reqee,
                                      mopaque_nbits, addr_nbits, data_nbits, # mem msg parameter
                                      nopaque_nbits, num_ports ) # net msg parameter

    # One can also use RingNetRTL

    s.reqnet  = BusNetRTL( s.memifc.req.nbits )
    s.respnet = BusNetRTL( s.memifc.resp.nbits )

    s.d_adpt = DownsAdapter[num_ports]( single_reqer,
                                        mopaque_nbits, addr_nbits, data_nbits, # mem msg parameter
                                        nopaque_nbits, num_ports ) # net msg parameter

    #---------------------------------------------------------------------
    # Connections
    #---------------------------------------------------------------------

    for i in xrange( num_ports ):
      s.connect( s.u_adpt[i].src_id, i )

      s.connect( s.memreq[i],         s.u_adpt[i].memreq  )
      s.connect( s.u_adpt[i].netreq,  s.reqnet.in_[i]  )

      s.connect( s.memresp[i],        s.u_adpt[i].memresp )
      s.connect( s.u_adpt[i].netresp, s.respnet.out[i] )

    for i in xrange( num_ports ):
      s.connect( s.d_adpt[i].src_id, i )

      s.connect( s.reqnet.out[i],     s.d_adpt[i].netreq  )
      s.connect( s.d_adpt[i].memreq,  s.mainmemreq[i]     )

      s.connect( s.respnet.in_[i],    s.d_adpt[i].netresp )
      s.connect( s.d_adpt[i].memresp, s.mainmemresp[i]    )

  def line_trace( s ):
    return s.reqnet.line_trace() + " >>> "+s.respnet.line_trace()
