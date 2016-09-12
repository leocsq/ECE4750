#=========================================================================
# ProcBasePRTL.py
#=========================================================================

from pymtl               import *
from pclib.ifcs          import InValRdyBundle, OutValRdyBundle
from pclib.ifcs          import MemReqMsg4B, MemRespMsg4B
from pclib.rtl           import SingleElementBypassQueue, TwoElementBypassQueue
from tinyrv2_encoding    import disassemble_inst
from TinyRV2InstPRTL     import inst_dict

from ProcBaseDpathPRTL import ProcBaseDpathPRTL
from ProcBaseCtrlPRTL  import ProcBaseCtrlPRTL
from DropUnitPRTL        import DropUnitPRTL

class ProcBasePRTL( Model ):

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

    # Output val_W from control unit for counting num_inst

    s.commit_inst = OutPort( 1 )

    # stats_en

    s.stats_en    = OutPort( 1 )

    #---------------------------------------------------------------------
    # Structural composition
    #---------------------------------------------------------------------

    s.ctrl  = ProcBaseCtrlPRTL()
    s.dpath = ProcBaseDpathPRTL( num_cores )

    # Connect parameters

    s.connect( s.core_id, s.dpath.core_id )

    # Bypass queues

    s.imemreq_queue   = TwoElementBypassQueue( MemReqMsg4B )
    s.dmemreq_queue   = SingleElementBypassQueue( MemReqMsg4B )
    s.proc2mngr_queue = SingleElementBypassQueue( 32 )

    s.connect_pairs(
      s.imemreq_queue.deq,   s.imemreq,
      s.dmemreq_queue.deq,   s.dmemreq,
      s.proc2mngr_queue.deq, s.proc2mngr
    )

    # imem drop unit

    s.imemresp_drop = Wire( 1 )

    s.imemresp_drop_unit = m = DropUnitPRTL( 32 )

    s.connect_pairs(
      m.drop,    s.imemresp_drop,
      m.in_.val, s.imemresp.val,
      m.in_.rdy, s.imemresp.rdy,
      m.in_.msg, s.imemresp.msg.data,
    )

    # Control

    s.connect_pairs(

      # imem ports

      s.ctrl.imemreq_val,   s.imemreq_queue.enq.val,
      s.ctrl.imemreq_rdy,   s.imemreq_queue.enq.rdy,

      s.ctrl.imemresp_val,  s.imemresp_drop_unit.out.val,
      s.ctrl.imemresp_rdy,  s.imemresp_drop_unit.out.rdy,

      # to drop unit

      s.ctrl.imemresp_drop, s.imemresp_drop,

      # dmem port

      s.ctrl.dmemreq_val,   s.dmemreq_queue.enq.val,
      s.ctrl.dmemreq_rdy,   s.dmemreq_queue.enq.rdy,

      s.ctrl.dmemresp_val,  s.dmemresp.val,
      s.ctrl.dmemresp_rdy,  s.dmemresp.rdy,

      # proc2mngr and mngr2proc

      s.ctrl.proc2mngr_val, s.proc2mngr_queue.enq.val,
      s.ctrl.proc2mngr_rdy, s.proc2mngr_queue.enq.rdy,

      s.ctrl.mngr2proc_val, s.mngr2proc.val,
      s.ctrl.mngr2proc_rdy, s.mngr2proc.rdy,

      s.ctrl.commit_inst,   s.commit_inst

    )

    # Dpath

    s.connect_pairs(

      # imem ports

      s.dpath.imemreq_msg,       s.imemreq_queue.enq.msg,
      s.dpath.imemresp_msg_data, s.imemresp_drop_unit.out.msg,

      # dmem ports

      s.dpath.dmemreq_msg_addr,  s.dmemreq_queue.enq.msg.addr,
      s.dpath.dmemresp_msg_data, s.dmemresp.msg.data,

      # mngr

      s.dpath.mngr2proc_data,    s.mngr2proc.msg,
      s.dpath.proc2mngr_data,    s.proc2mngr_queue.enq.msg,

      # stats_en

      s.dpath.stats_en,          s.stats_en
    )

    # Ctrl <-> Dpath

    s.connect_auto( s.ctrl, s.dpath )

  #-----------------------------------------------------------------------
  # Line tracing
  #-----------------------------------------------------------------------

  def line_trace( s ):

    # F stage

    if not s.ctrl.val_F.value:
      F_str = "{:<8s}".format( ' ' )
    elif s.ctrl.squash_F.value:
      F_str = "{:<8s}".format( '~' )
    elif s.ctrl.stall_F.value:
      F_str = "{:<8s}".format( '#' )
    else:
      F_str = "{:08x}".format( s.dpath.pc_reg_F.out.value.uint() )

    # D stage

    if not s.ctrl.val_D.value:
      D_str = "{:<23s}".format( ' ' )
    elif s.ctrl.squash_D.value:
      D_str = "{:<23s}".format( '~' )
    elif s.ctrl.stall_D.value:
      D_str = "{:<23s}".format( '#' )
    else:
      D_str = "{:<23s}".format( disassemble_inst(s.ctrl.inst_D.value) )

    # X stage

    if not s.ctrl.val_X.value:
      X_str = "{:<5s}".format( ' ' )
    elif s.ctrl.stall_X.value:
      X_str = "{:<5s}".format( '#' )
    else:
      X_str = "{:<5s}".format( inst_dict[s.ctrl.inst_type_X.value.uint()] )

    # M stage

    if not s.ctrl.val_M.value:
      M_str = "{:<5s}".format( ' ' )
    elif s.ctrl.stall_M.value:
      M_str = "{:<5s}".format( '#' )
    else:
      M_str = "{:<5s}".format( inst_dict[s.ctrl.inst_type_M.value.uint()] )

    # W stage

    if not s.ctrl.val_W.value:
      W_str = "{:<5s}".format( ' ' )
    elif s.ctrl.stall_W.value:
      W_str = "{:<5s}".format( '#' )
    else:
      W_str = "{:<5s}".format( inst_dict[s.ctrl.inst_type_W.value.uint()] )

    pipeline_str = ( F_str + "|" + D_str + "|" + X_str + "|" + M_str + "|" + W_str )

    return pipeline_str
