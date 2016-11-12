#=========================================================================
# CacheNetPRTL.py
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
# This is the architecture of a general memory network. In CacheNet, the
# number of requesters and the number of requestees are both 4. Requesters
# are renamed to procreqs since the requesters are basically processors.
# Requestees are the caches.

from pymtl               import *
from pclib.ifcs          import InValRdyBundle, OutValRdyBundle
from pclib.ifcs          import MemMsg, MemReqMsg, MemRespMsg

from lab4_net import BusNetRTL, RingNetRTL

from MsgAdapters import UpstreamMsgAdapter as UpsAdapter
from MsgAdapters import DownstreamMsgAdapter as DownsAdapter

class CacheNetPRTL( Model ):

  def __init__( s ):

    # Parameters

    num_reqers    = 4 # 4 processors
    num_reqees    = 4 # 4 data caches
    num_ports     = max( num_reqers, num_reqees ) # We still have 4 ports

    nopaque_nbits = 8
    mopaque_nbits = 8
    addr_nbits    = 32
    data_nbits    = 32 # CacheNet only deals with 32 bit requests

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    s.procifc   = MemMsg( mopaque_nbits, addr_nbits, data_nbits )
    s.cacheifc  = MemMsg( mopaque_nbits, addr_nbits, data_nbits )

    s.procreq   = InValRdyBundle [num_ports]( s.procifc.req  )
    s.procresp  = OutValRdyBundle[num_ports]( s.procifc.resp )

    s.cachereq  = OutValRdyBundle[num_ports]( s.cacheifc.req  )
    s.cacheresp = InValRdyBundle [num_ports]( s.cacheifc.resp )

    #---------------------------------------------------------------------
    # Components
    #---------------------------------------------------------------------

    single_reqee = False # 4 caches so not single reqee
    single_reqer = False # 4 procs so not single reqer 

    s.u_adpt = UpsAdapter[num_ports]( single_reqee,
                                      mopaque_nbits, addr_nbits, data_nbits, # mem msg parameter
                                      nopaque_nbits, num_ports ) # net msg parameter

    # One can also use RingNetRTL

    s.reqnet  = BusNetRTL( s.procifc.req.nbits )
    s.respnet = BusNetRTL( s.procifc.resp.nbits )

    s.d_adpt = DownsAdapter[num_ports]( single_reqer,
                                        mopaque_nbits, addr_nbits, data_nbits, # mem msg parameter
                                        nopaque_nbits, num_ports ) # net msg parameter

    #---------------------------------------------------------------------
    # Connections
    #---------------------------------------------------------------------

    for i in xrange( num_ports ):
      s.connect( s.u_adpt[i].src_id, i )

      s.connect( s.procreq[i],        s.u_adpt[i].memreq  )
      s.connect( s.u_adpt[i].netreq,  s.reqnet.in_[i]  )

      s.connect( s.procresp[i],       s.u_adpt[i].memresp )
      s.connect( s.u_adpt[i].netresp, s.respnet.out[i] )

    for i in xrange( num_ports ):
      s.connect( s.d_adpt[i].src_id, i )

      s.connect( s.reqnet.out[i],  s.d_adpt[i].netreq  )
      s.connect( s.d_adpt[i].memreq,  s.cachereq[i]    )

      s.connect( s.respnet.in_[i], s.d_adpt[i].netresp )
      s.connect( s.d_adpt[i].memresp, s.cacheresp[i]   )

  def line_trace( s ):
    return s.reqnet.line_trace() + " >>> "+s.respnet.line_trace()
