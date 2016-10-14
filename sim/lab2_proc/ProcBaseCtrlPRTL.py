#=========================================================================
# ProcBaseCtrlPRTL.py
#=========================================================================

from pymtl        import *

from TinyRV2InstPRTL import *

class ProcBaseCtrlPRTL( Model ):

  def __init__( s ):

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    # imem ports

    s.imemreq_val     = OutPort( 1 )
    s.imemreq_rdy     = InPort ( 1 )

    s.imemresp_val    = InPort ( 1 )
    s.imemresp_rdy    = OutPort( 1 )

    s.imemresp_drop   = OutPort( 1 )

    # dmem ports

    s.dmemreq_val     = OutPort( 1 )
    s.dmemreq_rdy     = InPort ( 1 )

    s.dmemresp_val    = InPort ( 1 )
    s.dmemresp_rdy    = OutPort( 1 )

    # mngr ports

    s.mngr2proc_val   = InPort ( 1 )
    s.mngr2proc_rdy   = OutPort( 1 )

    s.proc2mngr_val   = OutPort( 1 )
    s.proc2mngr_rdy   = InPort ( 1 )

    # Control signals (ctrl->dpath)

    s.reg_en_F        = OutPort( 1 )
    s.pc_sel_F        = OutPort( 2 )

    s.reg_en_D        = OutPort( 1 )
    s.op2_sel_D       = OutPort( 2 )
    s.csrr_sel_D      = OutPort( 2 )
    s.imm_type_D      = OutPort( 3 )

    s.reg_en_X        = OutPort( 1 )
    s.alu_fn_X        = OutPort( 4 )

    s.reg_en_M        = OutPort( 1 )
    s.wb_result_sel_M = OutPort( 1 )

    s.reg_en_W        = OutPort( 1 )
    s.rf_waddr_W      = OutPort( 5 )
    s.rf_wen_W        = OutPort( 1 )

    # Status signals (dpath->ctrl)

    s.inst_D          = InPort ( 32 )
    s.br_cond_eq_X    = InPort ( 1 )

    # Output val_W for counting

    s.commit_inst     = OutPort( 1 )

    s.stats_en_wen_W  = OutPort( 1 )

    #-----------------------------------------------------------------------
    # Control unit logic
    #-----------------------------------------------------------------------
    # We follow this principle to organize code for each pipeline stage in
    # the control unit.  Register enable logics should always at the
    # beginning. It followed by pipeline registers. Then logic that is not
    # dependent on stall or squash signals. Then logic that is dependent on
    # stall or squash signals. At the end there should be signals meant to
    # be passed to the next stage in the pipeline.

    #---------------------------------------------------------------------
    # Valid, stall, and squash signals
    #---------------------------------------------------------------------
    # We use valid signal to indicate if the instruction is valid.  An
    # instruction can become invalid because of being squashed or
    # stalled. Notice that invalid instructions are microarchitectural
    # events, they are different from archtectural no-ops. We must be
    # careful about control signals that might change the state of the
    # processor. We should always AND outgoing control signals with valid
    # signal.

    s.val_F = Wire( 1 )
    s.val_D = Wire( 1 )
    s.val_X = Wire( 1 )
    s.val_M = Wire( 1 )
    s.val_W = Wire( 1 )

    # Managing the stall and squash signals is one of the most important,
    # yet also one of the most complex, aspects of designing a pipelined
    # processor. We will carefully use four signals per stage to manage
    # stalling and squashing: ostall_A, osquash_A, stall_A, and squash_A.

    # We denote the stall signals _originating_ from stage A as
    # ostall_A. For example, if stage A can stall due to a pipeline
    # harzard, then ostall_A would need to factor in the stalling
    # condition for this pipeline harzard.

    s.ostall_F = Wire( 1 )  # can ostall due to imemresp_val
    s.ostall_D = Wire( 1 )  # can ostall due to mngr2proc_val or other hazards
    s.ostall_X = Wire( 1 )  # can ostall due to dmemreq_rdy
    s.ostall_M = Wire( 1 )  # can ostall due to dmemresp_val
    s.ostall_W = Wire( 1 )  # can ostall due to proc2mngr_rdy

    # The stall_A signal should be used to indicate when stage A is indeed
    # stalling. stall_A will be a function of ostall_A and all the ostall
    # signals of stages in front of it in the pipeline.

    s.stall_F = Wire( 1 )
    s.stall_D = Wire( 1 )
    s.stall_X = Wire( 1 )
    s.stall_M = Wire( 1 )
    s.stall_W = Wire( 1 )

    # We denote the squash signals _originating_ from stage A as
    # osquash_A. For example, if stage A needs to squash the stages behind
    # A in the pipeline, then osquash_A would need to factor in this
    # squash condition.

    s.osquash_D = Wire( 1 ) # can osquash due to unconditional jumps
    s.osquash_X = Wire( 1 ) # can osquash due to taken branches

    # The squash_A signal should be used to indicate when stage A is being
    # squashed. squash_A will _not_ be a function of osquash_A, since
    # osquash_A means to squash the stages _behind_ A in the pipeline, but
    # not to squash A itself.

    s.squash_F = Wire( 1 )
    s.squash_D = Wire( 1 )

    #---------------------------------------------------------------------
    # F stage
    #---------------------------------------------------------------------

    @s.combinational
    def comb_reg_en_F():
      s.reg_en_F.value = ~s.stall_F | s.squash_F

    @s.posedge_clk
    def reg_F():
      if s.reset:
        s.val_F.next = 0
      elif s.reg_en_F:
        s.val_F.next = 1

    # forward declaration of branch logic

    s.pc_redirect_X = Wire( 1 )
    s.pc_sel_X      = Wire( 2 )

    # pc sel logic

    @s.combinational
    def comb_PC_sel_F():
      if s.pc_redirect_X:
        s.pc_sel_F.value = 1 # use branch target (if taken)
      else:
        s.pc_sel_F.value = 0 # use pc+4

    s.next_val_F = Wire( 1 )

    @s.combinational
    def comb_F():
      # ostall due to imemresp

      s.ostall_F.value      = s.val_F & ~s.imemresp_val

      # stall and squash in F stage

      s.stall_F.value       = s.val_F & ( s.ostall_F  | s.ostall_D |
                                          s.ostall_X  | s.ostall_M |
                                          s.ostall_W                 )
      s.squash_F.value      = s.val_F & ( s.osquash_D | s.osquash_X  )

      # imem req is special, it actually be sent out _before_ the F
      # stage, we need to send memreq everytime we are getting squashed
      # because we need to redirect the PC. We also need to factor in
      # reset. When we are resetting we shouldn't send out imem req.

      s.imemreq_val.value   =  ~s.reset & (~s.stall_F | s.squash_F)
      s.imemresp_rdy.value  =  ~s.stall_F | s.squash_F

      # We drop the mem response when we are getting squashed

      s.imemresp_drop.value = s.squash_F

      s.next_val_F.value    = s.val_F & ~s.stall_F & ~s.squash_F

    #---------------------------------------------------------------------
    # D stage
    #---------------------------------------------------------------------

    @s.combinational
    def comb_reg_en_D():
      s.reg_en_D.value = ~s.stall_D | s.squash_D

    @s.posedge_clk
    def reg_D():
      if s.reset:
        s.val_D.next = 0
      elif s.reg_en_D:
        s.val_D.next = s.next_val_F

    # Decoder, translate 32-bit instructions to symbols

    s.inst_type_decoder_D = m = DecodeInstType()

    s.connect( m.in_, s.inst_D )

    # Signals generated by control signal table

    s.inst_val_D            = Wire( 1 )
    s.br_type_D             = Wire( 3 )
    s.rs1_en_D              = Wire( 1 )
    s.rs2_en_D              = Wire( 1 )
    s.alu_fn_D              = Wire( 4 )
    s.dmemreq_type_D        = Wire( 2 )
    s.wb_result_sel_D       = Wire( 1 )
    s.rf_wen_pending_D      = Wire( 1 )
    s.rf_waddr_sel_D        = Wire( 3 )
    s.csrw_D                = Wire( 1 )
    s.csrr_D                = Wire( 1 )
    s.proc2mngr_val_D       = Wire( 1 )
    s.mngr2proc_rdy_D       = Wire( 1 )
    s.stats_en_wen_D        = Wire( 1 )

    # actual waddr, selected base on rf_waddr_sel_D

    s.rf_waddr_D = Wire( 5 )

    # Control signal table

    # Y/N parameters

    n = Bits( 1, 0 )
    y = Bits( 1, 1 )

    # Branch type

    br_x    = Bits( 3, 0 ) # don't care
    br_na   = Bits( 3, 0 ) # N/A, not branch
    br_bne  = Bits( 3, 1 ) # branch not equal

    # Op2 mux select

    bm_x   = Bits( 2, 0 ) # don't care
    bm_rf  = Bits( 2, 0 ) # use data from RF
    bm_imm = Bits( 2, 1 ) # use imm
    bm_csr = Bits( 2, 2 ) # use mngr2proc/numcores/coreid based on csrnum

    # ALU func

    alu_x   = Bits( 4, 0  )
    alu_add = Bits( 4, 0  )
    alu_sub = Bits( 4, 1  )
    alu_cp0 = Bits( 4, 11 )
    alu_cp1 = Bits( 4, 12 )

    # IMM type

    imm_x = Bits( 3, 0 ) # don't care
    imm_i = Bits( 3, 0 ) # I-imm
    imm_s = Bits( 3, 1 ) # S-imm
    imm_b = Bits( 3, 2 ) # B-imm
    imm_u = Bits( 3, 3 ) # U-imm
    imm_j = Bits( 3, 4 ) # J-imm

    # Memory request type

    nr = Bits( 2, 0 )
    ld = Bits( 2, 1 )
    st = Bits( 2, 2 )

    # Write-back mux select

    wm_x = Bits( 1, 0 )
    wm_a = Bits( 1, 0 )
    wm_m = Bits( 1, 1 )

    # helper function to assign control signal table

    def cs (
        cs_inst_val,
        cs_br_type,
        cs_imm_type,
        cs_rs1_en,
        cs_op2_sel,
        cs_rs2_en,
        cs_alu_fn,
        cs_dmemreq_type,
        cs_wb_result_sel,
        cs_rf_wen_pending,
        cs_csrr,
        cs_csrw
    ):
      s.inst_val_D.value       = cs_inst_val
      s.br_type_D.value        = cs_br_type
      s.imm_type_D.value       = cs_imm_type
      s.rs1_en_D.value         = cs_rs1_en
      s.op2_sel_D.value        = cs_op2_sel
      s.rs2_en_D.value         = cs_rs2_en
      s.alu_fn_D.value         = cs_alu_fn
      s.dmemreq_type_D.value   = cs_dmemreq_type
      s.wb_result_sel_D.value  = cs_wb_result_sel
      s.rf_wen_pending_D.value = cs_rf_wen_pending
      s.csrr_D.value           = cs_csrr
      s.csrw_D.value           = cs_csrw

    # control signal table

    @s.combinational
    def comb_control_table_D():
      inst = s.inst_type_decoder_D.out.value
      #                          br      imm  rs1  op2    rs2 alu      dmm wbmux rf  
      #                      val type    type  en  muxsel  en fn       typ sel   wen csrr csrw
      if   inst == NOP  : cs( y, br_na,  imm_x, n, bm_x,   n, alu_x,   nr, wm_a, n,  n,   n    )
      elif inst == ADD  : cs( y, br_na,  imm_x, y, bm_rf,  y, alu_add, nr, wm_a, y,  n,   n    )
      elif inst == LW   : cs( y, br_na,  imm_i, y, bm_imm, n, alu_add, ld, wm_m, y,  n,   n    )
      elif inst == BNE  : cs( y, br_bne, imm_b, y, bm_rf,  y, alu_x,   nr, wm_a, n,  n,   n    )
      elif inst == CSRR : cs( y, br_na,  imm_i, n, bm_csr, n, alu_cp1, nr, wm_a, y,  y,   n    )
      elif inst == CSRW : cs( y, br_na,  imm_i, y, bm_rf,  n, alu_cp0, nr, wm_a, n,  n,   y    )

      #''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
      # Add More instructions to the control signal table
      #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

      else:               cs( n,  br_x,  imm_x, n, bm_x,   n, alu_x,   nr, wm_x, n,  n,   n    )

      # setting the actual write address
      
      s.rf_waddr_D.value = s.inst_D[RD]

      # csrr/csrw logic

      s.proc2mngr_val_D.value = s.csrw_D & ( s.inst_D[CSRNUM] == CSR_PROC2MNGR )
      s.mngr2proc_rdy_D.value = s.csrr_D & ( s.inst_D[CSRNUM] == CSR_MNGR2PROC )
      s.stats_en_wen_D.value  = s.csrw_D & ( s.inst_D[CSRNUM] == CSR_STATS_EN  )
      
      s.csrr_sel_D.value = 0
      if s.csrr_D:
        if   s.inst_D[CSRNUM] == CSR_NUMCORES:
          s.csrr_sel_D.value = 1
        elif s.inst_D[CSRNUM] == CSR_COREID:
          s.csrr_sel_D.value = 2

    # forward wire declaration for hazard checking

    s.rf_waddr_X      = Wire( 5 )
    s.rf_waddr_M      = Wire( 5 )

    # ostall due to hazards

    s.ostall_waddr_X_rs1_D = Wire( 1 )
    s.ostall_waddr_M_rs1_D = Wire( 1 )
    s.ostall_waddr_W_rs1_D = Wire( 1 )
    s.ostall_waddr_X_rs2_D = Wire( 1 )
    s.ostall_waddr_M_rs2_D = Wire( 1 )
    s.ostall_waddr_W_rs2_D = Wire( 1 )

    s.ostall_hazard_D     = Wire( 1 )

    # ostall due to mngr2proc

    s.ostall_mngr_D       = Wire( 1 )

    # hazards checking logic

    @s.combinational
    def comb_hazard_D():
      s.ostall_waddr_X_rs1_D.value = ( s.rs1_en_D & s.val_X & s.rf_wen_pending_X &
                                       ( s.inst_D[ RS1 ] == s.rf_waddr_X ) &
                                       ( s.rf_waddr_X != 0 )                      )
      s.ostall_waddr_M_rs1_D.value = ( s.rs1_en_D & s.val_M & s.rf_wen_pending_M &
                                       ( s.inst_D[ RS1 ] == s.rf_waddr_M ) &
                                       ( s.rf_waddr_M != 0 )                      )
      s.ostall_waddr_W_rs1_D.value = ( s.rs1_en_D & s.val_W & s.rf_wen_pending_W &
                                       ( s.inst_D[ RS1 ] == s.rf_waddr_W ) &
                                       ( s.rf_waddr_W != 0 )                      )
      s.ostall_waddr_X_rs2_D.value = ( s.rs2_en_D & s.val_X & s.rf_wen_pending_X &
                                       ( s.inst_D[ RS2 ] == s.rf_waddr_X ) &
                                       ( s.rf_waddr_X != 0 )                      )
      s.ostall_waddr_M_rs2_D.value = ( s.rs2_en_D & s.val_M & s.rf_wen_pending_M &
                                       ( s.inst_D[ RS2 ] == s.rf_waddr_M ) &
                                       ( s.rf_waddr_M != 0 )                      )
      s.ostall_waddr_W_rs2_D.value = ( s.rs2_en_D & s.val_W & s.rf_wen_pending_W &
                                       ( s.inst_D[ RS2 ] == s.rf_waddr_W ) &
                                       ( s.rf_waddr_W != 0 )                      )

      s.ostall_hazard_D.value      = ( s.ostall_waddr_X_rs1_D | s.ostall_waddr_M_rs1_D |
                                       s.ostall_waddr_W_rs1_D | s.ostall_waddr_X_rs2_D |
                                       s.ostall_waddr_M_rs2_D | s.ostall_waddr_W_rs2_D   )

    s.next_val_D = Wire( 1 )

    @s.combinational
    def comb_D():

      # ostall due to mngr2proc

      s.ostall_mngr_D.value = s.mngr2proc_rdy_D & ~s.mngr2proc_val

      # put together all ostall conditions

      s.ostall_D.value      = s.val_D & ( s.ostall_mngr_D | s.ostall_hazard_D );

      # stall in D stage
      # Note that, in the same combinational block, we have to calculate
      # s.stall_D first then use it in mngr2proc_rdy and next_val_D.
      # Several people stuck here just because they calculate them before stall_D!

      s.stall_D.value       = s.val_D & ( s.ostall_D | s.ostall_X |
                                          s.ostall_M | s.ostall_W   )

      # osquash due to jumps, not implemented yet

      s.osquash_D.value     = 0

      # squash in D stage

      s.squash_D.value      = s.val_D & s.osquash_X

      # mngr2proc port

      s.mngr2proc_rdy.value = s.val_D & ~s.stall_D & s.mngr2proc_rdy_D

      # next valid bit

      s.next_val_D.value    = s.val_D & ~s.stall_D & ~s.squash_D

    #---------------------------------------------------------------------
    # X stage
    #---------------------------------------------------------------------

    @s.combinational
    def comb_reg_en_X():
      s.reg_en_X.value  = ~s.stall_X

    s.inst_type_X      = Wire( 8 )
    s.rf_wen_pending_X = Wire( 1 )
    s.proc2mngr_val_X  = Wire( 1 )
    s.dmemreq_type_X   = Wire( 2 )
    s.wb_result_sel_X  = Wire( 1 )
    s.stats_en_wen_X   = Wire( 1 )
    s.br_type_X        = Wire( 3 )

    @s.posedge_clk
    def reg_X():
      if s.reset:
        s.val_X.next            = 0
        s.stats_en_wen_X.next   = 0
      elif s.reg_en_X:
        s.val_X.next            = s.next_val_D
        s.rf_wen_pending_X.next = s.rf_wen_pending_D
        s.inst_type_X.next      = s.inst_type_decoder_D.out
        s.alu_fn_X.next         = s.alu_fn_D
        s.rf_waddr_X.next       = s.rf_waddr_D
        s.proc2mngr_val_X.next  = s.proc2mngr_val_D
        s.dmemreq_type_X.next   = s.dmemreq_type_D
        s.wb_result_sel_X.next  = s.wb_result_sel_D
        s.stats_en_wen_X.next   = s.stats_en_wen_D
        s.br_type_X.next        = s.br_type_D

    # Branch logic

    @s.combinational
    def comb_br_X():
      if s.val_X and ( s.br_type_X == br_bne ):
        s.pc_redirect_X.value = ~s.br_cond_eq_X
      else:
        s.pc_redirect_X.value = 0

    s.next_val_X = Wire( 1 )

    @s.combinational
    def comb_X():
      # ostall due to dmemreq

      s.ostall_X.value    = s.val_X & ( s.dmemreq_type_X != nr ) & ~s.dmemreq_rdy

      # stall in X stage

      s.stall_X.value     = s.val_X & ( s.ostall_X | s.ostall_M | s.ostall_W )

      # osquash due to taken branches
      # Note that, in the same combinational block, we have to calculate
      # s.stall_X first then use it in osquash_X. Several people have
      # stuck here just because they calculate osquash_X before stall_X!

      s.osquash_X.value   = s.val_X & ~s.stall_X & s.pc_redirect_X

      # send dmemreq if not stalling

      s.dmemreq_val.value = s.val_X & ~s.stall_X & ( s.dmemreq_type_X != nr )

      # next valid bit

      s.next_val_X.value  = s.val_X & ~s.stall_X

    #---------------------------------------------------------------------
    # M stage
    #---------------------------------------------------------------------

    @s.combinational
    def comb_reg_en_M():
      s.reg_en_M.value = ~s.stall_M

    s.inst_type_M      = Wire( 8 )
    s.rf_wen_pending_M = Wire( 1 )
    s.proc2mngr_val_M  = Wire( 1 )
    s.dmemreq_type_M   = Wire( 2 )
    s.stats_en_wen_M   = Wire( 1 )

    @s.posedge_clk
    def reg_M():
      if s.reset:
        s.val_M.next            = 0
        s.stats_en_wen_M.next   = 0
      elif s.reg_en_M:
        s.val_M.next            = s.next_val_X
        s.rf_wen_pending_M.next = s.rf_wen_pending_X
        s.inst_type_M.next      = s.inst_type_X
        s.rf_waddr_M.next       = s.rf_waddr_X
        s.proc2mngr_val_M.next  = s.proc2mngr_val_X
        s.dmemreq_type_M.next   = s.dmemreq_type_X
        s.wb_result_sel_M.next  = s.wb_result_sel_X
        s.stats_en_wen_M.next   = s.stats_en_wen_X

    s.next_val_M = Wire( 1 )

    @s.combinational
    def comb_M():
      # ostall due to dmem resp

      s.ostall_M.value     = s.val_M & ( s.dmemreq_type_M != nr ) & ~s.dmemresp_val

      # stall in M stage

      s.stall_M.value      = s.val_M & ( s.ostall_M | s.ostall_W )

      # set dmemresp ready if not stalling

      s.dmemresp_rdy.value = s.val_M & ~s.stall_M & ( s.dmemreq_type_M != nr )

      # next valid bit

      s.next_val_M.value   = s.val_M & ~s.stall_M

    #---------------------------------------------------------------------
    # W stage
    #---------------------------------------------------------------------

    @s.combinational
    def comb_W():
      s.reg_en_W.value = ~s.stall_W

    s.inst_type_W            = Wire( 8 )
    s.proc2mngr_val_W        = Wire( 1 )
    s.rf_wen_pending_W       = Wire( 1 )
    s.stats_en_wen_pending_W = Wire( 1 )

    @s.posedge_clk
    def reg_W():

      if s.reset:
        s.val_W.next            = 0
        s.stats_en_wen_W.next   = 0
      elif s.reg_en_W:
        s.val_W.next                  = s.next_val_M
        s.rf_wen_pending_W.next       = s.rf_wen_pending_M
        s.inst_type_W.next            = s.inst_type_M
        s.rf_waddr_W.next             = s.rf_waddr_M
        s.proc2mngr_val_W.next        = s.proc2mngr_val_M
        s.stats_en_wen_pending_W.next = s.stats_en_wen_M

    s.ostall_proc2mngr_W = Wire( 1 )

    @s.combinational
    def comb_W():
      # set RF write enable if valid

      s.rf_wen_W.value       = s.val_W & s.rf_wen_pending_W
      s.stats_en_wen_W.value = s.val_W & s.stats_en_wen_pending_W

      # ostall due to proc2mngr

      s.ostall_W.value      = s.val_W & s.proc2mngr_val_W & ~s.proc2mngr_rdy

      # stall in W stage

      s.stall_W.value       = s.val_W & s.ostall_W

      # set proc2mngr val if not stalling

      s.proc2mngr_val.value = s.val_W & ~s.stall_W & s.proc2mngr_val_W

      s.commit_inst.value   = s.val_W & ~s.stall_W
