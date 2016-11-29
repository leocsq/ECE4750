//=========================================================================
// 5-Stage Stalling Pipelined Processor Control
//=========================================================================

`ifndef LAB2_PROC_PIPELINED_PROC_ALT_CTRL_V
`define LAB2_PROC_PIPELINED_PROC_ALT_CTRL_V

`include "vc/trace.v"

`include "lab2_proc/TinyRV2InstVRTL.v"

module lab2_proc_ProcAltCtrlVRTL
(
  input  logic        clk,
  input  logic        reset,

  // Instruction Memory Port

  output logic        imemreq_val,
  input  logic        imemreq_rdy,

  input  logic        imemresp_val,
  output logic        imemresp_rdy,

  output logic        imemresp_drop,

  // Data Memory Port

  output logic        dmemreq_val,
  input  logic        dmemreq_rdy,

  input  logic        dmemresp_val,
  output logic        dmemresp_rdy,
  output logic [2:0]  dmemreq_type,

  // mngr communication port

  input  logic        mngr2proc_val,
  output logic        mngr2proc_rdy,

  output logic        proc2mngr_val,
  input  logic        proc2mngr_rdy,

  // control signals (ctrl->dpath)

  output logic        reg_en_F,
  output logic [1:0]  pc_sel_F,

  output logic        reg_en_D,
  output logic [1:0]  op1_byp_sel_D,
  output logic [1:0]  op2_byp_sel_D,
  output logic        op1_sel_D,
  output logic [1:0]  op2_sel_D,
  output logic [1:0]  csrr_sel_D,
  output logic [2:0]  imm_type_D,
  output logic        imul_req_val_D,

  output logic        reg_en_X,
  output logic [3:0]  alu_fn_X,
  output logic        imul_resp_rdy_X,
  output logic [1:0]  ex_result_sel_X,
  

  output logic        reg_en_M,
  output logic        wb_result_sel_M,

  output logic        reg_en_W,
  output logic [4:0]  rf_waddr_W,
  output logic        rf_wen_W,

  // status signals (dpath->ctrl)

  input  logic [31:0] inst_D,
  input  logic        imul_req_rdy_D,
  input  logic        br_cond_eq_X,
  input  logic        br_cond_lt_X,
  input  logic        br_cond_ltu_X,
  input  logic        imul_resp_val_X,

  output logic        stats_en_wen_W,

  output logic        commit_inst

);

  //----------------------------------------------------------------------
  // Notes
  //----------------------------------------------------------------------
  // We follow this principle to organize code for each pipeline stage in
  // the control unit.  Register enable logics should always at the
  // beginning. It followed by pipeline registers. Then logic that is not
  // dependent on stall or squash signals. Then logic that is dependent
  // on stall or squash signals. At the end there should be signals meant
  // to be passed to the next stage in the pipeline.

  //----------------------------------------------------------------------
  // Valid, stall, and squash signals
  // ----------------------------------------------------------------------
  // We use valid signal to indicate if the instruction is valid.  An
  // instruction can become invalid because of being squashed or
  // stalled. Notice that invalid instructions are microarchitectural
  // events, they are different from archtectural no-ops. We must be
  // careful about control signals that might change the state of the
  // processor. We should always AND outgoing control signals with valid
  // signal.

  logic val_F;
  logic val_D;
  logic val_X;
  logic val_M;
  logic val_W;

  // Managing the stall and squash signals is one of the most important,
  // yet also one of the most complex, aspects of designing a pipelined
  // processor. We will carefully use four signals per stage to manage
  // stalling and squashing: ostall_A, osquash_A, stall_A, and squash_A.
  //
  // We denote the stall signals _originating_ from stage A as
  // ostall_A. For example, if stage A can stall due to a pipeline
  // harzard, then ostall_A would need to factor in the stalling
  // condition for this pipeline harzard.

  logic ostall_F;  // can ostall due to imemresp_val
  logic ostall_D;  // can ostall due to mngr2proc_val or other hazards
  logic ostall_X;  // can ostall due to dmemreq_rdy
  logic ostall_M;  // can ostall due to dmemresp_val
  logic ostall_W;  // can ostall due to proc2mngr_rdy

  // The stall_A signal should be used to indicate when stage A is indeed
  // stalling. stall_A will be a function of ostall_A and all the ostall
  // signals of stages in front of it in the pipeline.

  logic stall_F;
  logic stall_D;
  logic stall_X;
  logic stall_M;
  logic stall_W;

  // We denote the squash signals _originating_ from stage A as
  // osquash_A. For example, if stage A needs to squash the stages behind
  // A in the pipeline, then osquash_A would need to factor in this
  // squash condition.

  logic osquash_D; // can osquash due to unconditional jumps
  logic osquash_X; // can osquash due to taken branches

  // The squash_A signal should be used to indicate when stage A is being
  // squashed. squash_A will _not_ be a function of osquash_A, since
  // osquash_A means to squash the stages _behind_ A in the pipeline, but
  // not to squash A itself.

  logic squash_F;
  logic squash_D;

  //----------------------------------------------------------------------
  // F stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_F = !stall_F || squash_F;

  // Pipeline registers

  always_ff @( posedge clk ) begin
    if ( reset )
      val_F <= 1'b0;
    else if ( reg_en_F )
      val_F <= 1'b1;
  end

  // forward declaration for PC sel

  logic       pc_redirect_X;
  logic       pc_redirect_D;
  logic [1:0] pc_sel_X;
  logic [1:0] pc_sel_D;

  // PC select logic

  always_comb begin
    if ( pc_redirect_X )       // If a branch is taken in X stage
      pc_sel_F = pc_sel_X;     // Use pc from X
    else if ( pc_redirect_D )  
      pc_sel_F = pc_sel_D;     // Use pc from D
    else
      pc_sel_F = 2'b0;         // Use pc+4
  end

  // ostall due to the imem response not valid.

  assign ostall_F = val_F && !imemresp_val;

  // stall and squash in F

  assign stall_F  = val_F && ( ostall_F  || ostall_D || ostall_X || ostall_M || ostall_W );
  assign squash_F = val_F && ( osquash_D || osquash_X );

  // We drop the mem response when we are getting squashed

  assign imemresp_drop = squash_F;

  // imem is very special. Actually imem requests are sent before the F
  // stage. Note that we need to factor in reset to the imemreq_val
  // signal because we don't want to send out imem request when we are
  // resetting.

  assign imemreq_val  = ( !stall_F || squash_F ) && !reset;
  assign imemresp_rdy = !stall_F || squash_F;

  // Valid signal for the next stage (stage D)

  logic  next_val_F;
  assign next_val_F = val_F && !stall_F && !squash_F;

  //----------------------------------------------------------------------
  // D stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_D = !stall_D || squash_D;

  // Pipline registers

  always_ff @( posedge clk ) begin
    if ( reset )
      val_D <= 1'b0;
    else if ( reg_en_D )
      val_D <= next_val_F;
  end

  // Parse instruction fields

  logic   [4:0] inst_rd_D;
  logic   [4:0] inst_rs1_D;
  logic   [4:0] inst_rs2_D;
  logic   [11:0] inst_csr_D;

  rv2isa_InstUnpack inst_unpack
  (
    .inst     (inst_D),
    .opcode   (),
    .rd       (inst_rd_D),
    .rs1      (inst_rs1_D),
    .rs2      (inst_rs2_D),
    .funct3   (),
    .funct7   (),
    .csr      (inst_csr_D)
  );

  // Generic Parameters -- yes or no

  localparam n = 1'd0;
  localparam y = 1'd1;

  // Register specifiers

  localparam rx = 5'bx;   // don't care
  localparam r0 = 5'd0;   // zero
  localparam rL = 5'd31;  // for jal
  
  // Jump type
  localparam jr_x     = 2'bx; // Don't care
  localparam jr_na    = 2'd0; // No jump
  localparam jr_jal   = 2'd1; // jal
  localparam jr_jalr  = 2'd2; // jalr

  // Branch type

  localparam br_x     = 3'bx; // Don't care
  localparam br_na    = 3'd0; // No branch
  localparam br_beq   = 3'd1; // beq
  localparam br_bne   = 3'd2; // bne
  localparam br_blt   = 3'd3; // blt
  localparam br_bge   = 3'd4; // bge
  localparam br_bltu  = 3'd5; // bltu
  localparam br_bgeu  = 3'd6; // bgeu

  // Operand 1 Mux Select

  localparam pm_x     = 1'bx; // Don't care
  localparam pm_pc    = 1'b0; // Use data from pc reg
  localparam pm_rf    = 1'b1; // Use data from register file


  // Operand 2 Mux Select

  localparam bm_x     = 2'bx; // Don't care
  localparam bm_rf    = 2'd0; // Use data from register file
  localparam bm_imm   = 2'd1; // Use sign-extended immediate
  localparam bm_csr   = 2'd2; // Use from mngr data

  // ALU Function

  localparam alu_x    = 4'bx;
  localparam alu_add  = 4'd0;
  localparam alu_sub  = 4'd1;
  localparam alu_and  = 4'd2;
  localparam alu_or   = 4'd3;
  localparam alu_xor  = 4'd4;
  localparam alu_slt  = 4'd5;
  localparam alu_sltu = 4'd6;
  localparam alu_sra  = 4'd7;
  localparam alu_srl  = 4'd8;
  localparam alu_sll  = 4'd9;
  localparam alu_jalr = 4'd10;
  localparam alu_cp0  = 4'd11;
  localparam alu_cp1  = 4'd12;

  // Immediate Type
  localparam imm_x    = 3'bx;
  localparam imm_i    = 3'd0;
  localparam imm_s    = 3'd1;
  localparam imm_b    = 3'd2;
  localparam imm_u    = 3'd3;
  localparam imm_j    = 3'd4;

  // Memory Request Type

  localparam nr       = 2'd0; // No request
  localparam ld       = 2'd1; // Load
  localparam st       = 2'd2; // Store

  // Writeback Mux Select

  localparam wm_x     = 1'bx; // Don't care
  localparam wm_a     = 1'b0; // Use ALU output
  localparam wm_m     = 1'b1; // Use data memory response

  // Result Mux Select
  
  localparam ex_x     = 2'bx; // Don't care
  localparam ex_pc    = 2'd0; // Use PC_incr output
  localparam ex_alu   = 2'd1; // Use ALU output
  localparam ex_mul   = 2'd2; // Use IMUL output
  
  
  // Instruction Decode

  logic       inst_val_D;
  logic [1:0] jr_type_D;
  logic [2:0] br_type_D;
  logic       rs1_en_D;
  logic       rs2_en_D;
  logic [3:0] alu_fn_D;
  logic [1:0] dmemreq_type_D;
  logic       wb_result_sel_D;
  logic       rf_wen_pending_D;
  logic       csrr_D;
  logic       csrw_D;
  logic       proc2mngr_val_D;
  logic       mngr2proc_rdy_D;
  logic       stats_en_wen_D;
  logic       imul_resp_rdy_D;
  logic [1:0] ex_result_sel_D;

  task cs
  (
    input logic       cs_inst_val,
    input logic [1:0] cs_jr_type, 
    input logic [2:0] cs_br_type,
    input logic [2:0] cs_imm_type,
    input logic       cs_rs1_en,
    input logic       cs_op1_sel,
    input logic [1:0] cs_op2_sel,
    input logic       cs_rs2_en,
    input logic [3:0] cs_alu_fn,
    input logic [1:0] cs_dmemreq_type,
    input logic       cs_wb_result_sel,
    input logic       cs_rf_wen_pending,
    input logic       cs_csrr,
    input logic       cs_csrw,
    input logic       cs_imul_req_val_D,
    input logic       cs_imul_resp_rdy_D,
    input logic [1:0] cs_ex_result_sel_D,
  
  );
  begin
    inst_val_D            = cs_inst_val;
    jr_type_D             = cs_jr_type;
    br_type_D             = cs_br_type;
    imm_type_D            = cs_imm_type;
    rs1_en_D              = cs_rs1_en;
    op1_sel_D             = cs_op1_sel;
    op2_sel_D             = cs_op2_sel;
    rs2_en_D              = cs_rs2_en;
    alu_fn_D              = cs_alu_fn;
    dmemreq_type_D        = cs_dmemreq_type;
    wb_result_sel_D       = cs_wb_result_sel;
    rf_wen_pending_D      = cs_rf_wen_pending;
    csrr_D                = cs_csrr;
    csrw_D                = cs_csrw;
    imul_req_val_D        = cs_imul_req_val_D;
    imul_resp_rdy_D       = cs_imul_resp_rdy_D;
    ex_result_sel_D       = cs_ex_result_sel_D;
  
    
  end
  endtask

  // Control signals table

  always_comb begin

    casez ( inst_D )

      //                           jr      br      imm  rs1  op1    op2    rs2 alu      dmm wbmux rf            imul imul result
      //                       val type    type    type  en  muxsel muxsel  en fn       typ sel   wen csrr csrw req  resp sel
      `RV2ISA_INST_NOP     :cs( y, jr_na,  br_na,  imm_x, n, pm_x,  bm_x,   n, alu_x   , nr, wm_a, n,  n,   n,   n,   n,   ex_x   );
      `RV2ISA_INST_CSRR    :cs( y, jr_na,  br_na,  imm_i, n, pm_rf, bm_csr, n, alu_cp1 , nr, wm_a, y,  y,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_CSRW    :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_rf,  n, alu_cp0 , nr, wm_a, n,  n,   y,   n,   n,   ex_alu );
      
      `RV2ISA_INST_ADD     :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_add , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SUB     :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_sub , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_AND     :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_and , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_OR      :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_or  , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_XOR     :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_xor , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SLT     :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_slt , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SLTU    :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_sltu, nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SRA     :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_sra , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SRL     :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_srl , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SLL     :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_sll , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_MUL     :cs( y, jr_na,  br_na,  imm_x, y, pm_rf, bm_rf,  y, alu_x   , nr, wm_a, y,  n,   n,   y,   y,   ex_mul );
        
      `RV2ISA_INST_ADDI    :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_add , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_ANDI    :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_and , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_ORI     :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_or  , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_XORI    :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_xor , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SLTI    :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_slt , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SLTIU   :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_sltu, nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SRAI    :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_sra , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SRLI    :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_srl , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SLLI    :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_sll , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_LUI     :cs( y, jr_na,  br_na,  imm_u, n, pm_rf, bm_imm, n, alu_cp1 , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_AUIPC   :cs( y, jr_na,  br_na,  imm_u, n, pm_pc, bm_imm, n, alu_add , nr, wm_a, y,  n,   n,   n,   n,   ex_alu );
      
      `RV2ISA_INST_LW      :cs( y, jr_na,  br_na,  imm_i, y, pm_rf, bm_imm, n, alu_add , ld, wm_m, y,  n,   n,   n,   n,   ex_alu );
      `RV2ISA_INST_SW      :cs( y, jr_na,  br_na,  imm_s, y, pm_rf, bm_imm, y, alu_add , st, wm_a, n,  n,   n,   n,   n,   ex_alu );
      
      `RV2ISA_INST_JAL     :cs( y, jr_jal, br_na,  imm_j, n, pm_rf, bm_rf,  n, alu_x   , nr, wm_a, y,  n,   n,   n,   n,   ex_pc  );
      `RV2ISA_INST_JALR    :cs( y, jr_jalr,br_na,  imm_i, y, pm_rf, bm_imm, n, alu_jalr, nr, wm_a, y,  n,   n,   n,   n,   ex_pc  );
      
      `RV2ISA_INST_BEQ     :cs( y, jr_na,  br_beq, imm_b, y, pm_rf, bm_rf,  y, alu_x   , nr, wm_a, n,  n,   n,   n,   n,   ex_x   );
      `RV2ISA_INST_BNE     :cs( y, jr_na,  br_bne, imm_b, y, pm_rf, bm_rf,  y, alu_x   , nr, wm_a, n,  n,   n,   n,   n,   ex_x   );
      `RV2ISA_INST_BLT     :cs( y, jr_na,  br_blt, imm_b, y, pm_rf, bm_rf,  y, alu_x   , nr, wm_a, n,  n,   n,   n,   n,   ex_x   );
      `RV2ISA_INST_BGE     :cs( y, jr_na,  br_bge, imm_b, y, pm_rf, bm_rf,  y, alu_x   , nr, wm_a, n,  n,   n,   n,   n,   ex_x   );
      `RV2ISA_INST_BLTU    :cs( y, jr_na,  br_bltu,imm_b, y, pm_rf, bm_rf,  y, alu_x   , nr, wm_a, n,  n,   n,   n,   n,   ex_x   );
      `RV2ISA_INST_BGEU    :cs( y, jr_na,  br_bgeu,imm_b, y, pm_rf, bm_rf,  y, alu_x   , nr, wm_a, n,  n,   n,   n,   n,   ex_x   );
      
      default              :cs( n, jr_x ,  br_x,   imm_x, n, pm_x,  bm_x,   n, alu_x   , nr, wm_x, n,  n,   n,   n,   n,   ex_x   );

    endcase
  end // always_comb

  logic [4:0] rf_waddr_D;
  assign rf_waddr_D = inst_rd_D;

  // csrr and csrw logic

  always_comb begin
    proc2mngr_val_D  = 1'b0;
    mngr2proc_rdy_D  = 1'b0;
    csrr_sel_D       = 2'h0;
    stats_en_wen_D   = 1'b0;

    if ( csrw_D && inst_csr_D == `RV2ISA_CPR_PROC2MNGR )
      proc2mngr_val_D    = 1'b1;
    if ( csrr_D && inst_csr_D == `RV2ISA_CPR_MNGR2PROC )
      mngr2proc_rdy_D  = 1'b1;
    if ( csrw_D && inst_csr_D == `RV2ISA_CPR_STATS_EN )
      stats_en_wen_D  = 1'b1;
    if ( csrr_D && inst_csr_D == `RV2ISA_CPR_NUMCORES )
      csrr_sel_D       = 2'h1;
    if ( csrr_D && inst_csr_D == `RV2ISA_CPR_COREID )
      csrr_sel_D       = 2'h2;
  end
  
  // jal logic, redirect PC in D 

  always_comb begin
    if ( val_D && ( jr_type_D == jr_jal ) ) begin
      pc_redirect_D = 1'b1;
      pc_sel_D      = 2'd2;          // use jal target
    end 
    else begin
      pc_redirect_D = 1'b0;
      pc_sel_D      = 2'b0;          // use pc+4
    end
  end

  // bypass logic
  
  logic  bypass_waddr_X_rs1_D;
  logic  bypass_waddr_X_rs2_D;
  logic  bypass_waddr_M_rs1_D;
  logic  bypass_waddr_M_rs2_D;
  logic  bypass_waddr_W_rs1_D;
  logic  bypass_waddr_W_rs2_D;
  
  always_comb begin
    if ( bypass_waddr_X_rs1_D ) begin
      op1_byp_sel_D = 2'd1;
    end else if ( bypass_waddr_M_rs1_D ) begin
      op1_byp_sel_D = 2'd2;
    end else if ( bypass_waddr_W_rs1_D ) begin
      op1_byp_sel_D = 2'd3; 
    end else begin
      op1_byp_sel_D = 2'd0;
    end
  end
  
  always_comb begin
    if ( bypass_waddr_X_rs2_D ) begin
      op2_byp_sel_D = 2'd1;
    end else if ( bypass_waddr_M_rs2_D ) begin
      op2_byp_sel_D = 2'd2;
    end else if ( bypass_waddr_W_rs2_D ) begin
      op2_byp_sel_D = 2'd3; 
    end else begin
      op2_byp_sel_D = 2'd0;
    end
  end
  
  assign bypass_waddr_X_rs1_D 
    = val_D && rs1_en_D && val_X && rf_wen_pending_X
      && ( inst_rs1_D == rf_waddr_X ) && ( rf_waddr_X != 5'd0 )
      && (dmemreq_type_X != ld);
  
  assign bypass_waddr_X_rs2_D 
    = val_D && rs2_en_D && val_X && rf_wen_pending_X
      && ( inst_rs2_D == rf_waddr_X ) && ( rf_waddr_X != 5'd0 )
      && (dmemreq_type_X != ld);
  
  assign bypass_waddr_M_rs1_D 
    = val_D && rs1_en_D && val_M && rf_wen_pending_M
      && ( inst_rs1_D == rf_waddr_M ) && ( rf_waddr_M != 5'd0 );
  
  assign bypass_waddr_M_rs2_D 
    = val_D && rs2_en_D && val_M && rf_wen_pending_M
      && ( inst_rs2_D == rf_waddr_M ) && ( rf_waddr_M != 5'd0 );
  
  assign bypass_waddr_W_rs1_D 
    = val_D && rs1_en_D && val_W && rf_wen_pending_W
      && ( inst_rs1_D == rf_waddr_W ) && ( rf_waddr_W != 5'd0 );
  
  assign bypass_waddr_W_rs2_D 
    = val_D && rs2_en_D && val_W && rf_wen_pending_W
      && ( inst_rs2_D == rf_waddr_W ) && ( rf_waddr_W != 5'd0 );
  
  // mngr2proc_rdy signal for csrr instruction

  assign mngr2proc_rdy  = val_D && !stall_D && mngr2proc_rdy_D;

  logic  ostall_mngr2proc_D;
  assign ostall_mngr2proc_D = val_D && mngr2proc_rdy_D && !mngr2proc_val;
  
  // ostall if imul request is not ready
  
  logic  ostall_imul_req_D;
  assign ostall_imul_req_D = val_D && !imul_req_rdy_D && !imul_req_val_D;

  // ostall if write address in X matches rs1 in D when load

  logic  ostall_load_use_X_rs1_D;
  assign ostall_load_use_X_rs1_D
    = rs1_en_D && val_X && rf_wen_pending_X
      && ( inst_rs1_D == rf_waddr_X ) && ( rf_waddr_X != 5'd0 )
      && (dmemreq_type_X == ld);
  
  // ostall if write address in X matches rs2 in D when load

  logic  ostall_load_use_X_rs2_D;
  assign ostall_load_use_X_rs2_D
    = rs2_en_D && val_X && rf_wen_pending_X
      && ( inst_rs2_D == rf_waddr_X ) && ( rf_waddr_X != 5'd0 )
      && (dmemreq_type_X == ld);

  // Put together ostall signal due to hazards

  logic  ostall_hazard_D;
  assign ostall_hazard_D =
      ostall_load_use_X_rs1_D || ostall_load_use_X_rs2_D ;

  // Final ostall signal

  assign ostall_D = val_D && ( ostall_mngr2proc_D || ostall_imul_req_D || ostall_hazard_D );

  // osquash due to jump instruction in D stage (not implemented yet)

  logic osquash_j_D;
  assign osquash_j_D = ( jr_type_D == jr_jal ) || ( jr_type_D == jr_jalr );

  assign osquash_D = val_D && !stall_D && osquash_j_D;

  // stall and squash in D

  assign stall_D  = val_D && ( ostall_D || ostall_X || ostall_M || ostall_W );
  assign squash_D = val_D && osquash_X;

  // Valid signal for the next stage

  logic  next_val_D;
  assign next_val_D = val_D && !stall_D && !squash_D;

  //----------------------------------------------------------------------
  // X stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_X = !stall_X;

  logic [31:0] inst_X;
  logic [1:0]  dmemreq_type_X;
  logic        wb_result_sel_X;
  logic        rf_wen_pending_X;
  logic [4:0]  rf_waddr_X;
  logic        proc2mngr_val_X;
  logic        stats_en_wen_X;
  logic [1:0]  jr_type_X;
  logic [2:0]  br_type_X;
  logic        imul_req_val_X;

  // Pipeline registers

  always_ff @( posedge clk )
    if (reset) begin
      val_X           <= 1'b0;
      stats_en_wen_X  <= 1'b0;
    end else if (reg_en_X) begin
      val_X           <= next_val_D;
      rf_wen_pending_X<= rf_wen_pending_D;
      inst_X          <= inst_D;
      alu_fn_X        <= alu_fn_D;
      rf_waddr_X      <= rf_waddr_D;
      proc2mngr_val_X <= proc2mngr_val_D;
      dmemreq_type_X  <= dmemreq_type_D;
      wb_result_sel_X <= wb_result_sel_D;
      stats_en_wen_X  <= stats_en_wen_D;
      jr_type_X       <= jr_type_D;
      br_type_X       <= br_type_D;
      imul_resp_rdy_X <= imul_resp_rdy_D;
      ex_result_sel_X <= ex_result_sel_D; 
      imul_req_val_X  <= imul_req_val_D;
      
      
    end
  
  // dmemreq type
  
  always_comb begin
    if ( val_X ) begin
      if( dmemreq_type_X == st) begin
        dmemreq_type = 3'd1;
      end else begin
        dmemreq_type = 3'd0; 
      end    
    end
  end

  // branch logic, redirect PC in F if branch is taken

  always_comb begin
    if ( val_X && ( br_type_X != br_na ) ) begin
      case ( br_type_X ) 
        
        br_beq  : pc_redirect_X =  br_cond_eq_X;
        br_bne  : pc_redirect_X = !br_cond_eq_X;
        br_blt  : pc_redirect_X =  br_cond_lt_X;
        br_bge  : pc_redirect_X = !br_cond_lt_X;
        br_bltu : pc_redirect_X =  br_cond_ltu_X;
        br_bgeu : pc_redirect_X = !br_cond_ltu_X;
      
        default : pc_redirect_X = 1'b0;
      endcase  
      pc_sel_X      = 2'd1;          // use branch target
    end else if ( val_X && ( jr_type_X == jr_jalr ) ) begin
      pc_redirect_X = 1'b1;
      pc_sel_X      = 2'd3;          // use jalr target
    end
    else begin
      pc_redirect_X = 1'b0;
      pc_sel_X      = 2'b0;          // use pc+4
    end
  end

  // ostall due to dmemreq not ready.
  logic  ostall_dmemreq_X; 
  assign ostall_dmemreq_X = val_X && ( dmemreq_type_X != nr ) && !dmemreq_rdy;
  
  // ostall if imul value is not ready
  logic  ostall_imul_resp_X;
  assign ostall_imul_resp_X = val_X && ( imul_req_val_X == 1 ) && !imul_resp_val_X;
  
  
  // Final ostall signal
  assign ostall_X = val_X &&  ( ostall_dmemreq_X  || ostall_imul_resp_X );
  
  
  
  
  // osquash due to taken branch, notice we can't osquash if current
  // stage stalls, otherwise we will send osquash twice.

  assign osquash_X = val_X && !stall_X && pc_redirect_X;

  // stall and squash used in X stage

  assign stall_X = val_X && ( ostall_X || ostall_M || ostall_W );

  // set dmemreq_val only if not stalling

  assign dmemreq_val = val_X && !stall_X && ( dmemreq_type_X != nr );

  // Valid signal for the next stage

  logic  next_val_X;
  assign next_val_X = val_X && !stall_X;

  //----------------------------------------------------------------------
  // M stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_M  = !stall_M;

  logic [31:0] inst_M;
  logic [1:0]  dmemreq_type_M;
  logic        rf_wen_pending_M;
  logic [4:0]  rf_waddr_M;
  logic        proc2mngr_val_M;
  logic        stats_en_wen_M;

  // Pipeline register

  always_ff @( posedge clk )
    if (reset) begin
      val_M            <= 1'b0;
      stats_en_wen_X   <= 1'b0;
    end else if (reg_en_M) begin
      val_M            <= next_val_X;
      rf_wen_pending_M <= rf_wen_pending_X;
      inst_M           <= inst_X;
      rf_waddr_M       <= rf_waddr_X;
      proc2mngr_val_M  <= proc2mngr_val_X;
      dmemreq_type_M   <= dmemreq_type_X;
      wb_result_sel_M  <= wb_result_sel_X;
      stats_en_wen_M   <= stats_en_wen_X;
    end

  // ostall due to dmemresp not valid

  assign ostall_M = val_M && ( dmemreq_type_M != nr ) && !dmemresp_val;

  // stall M

  assign stall_M = val_M && ( ostall_M || ostall_W );

  // Set dmemresp_rdy if valid and not stalling and this is a lw/sw

  assign dmemresp_rdy = val_M && !stall_M && ( dmemreq_type_M != nr );

  // Valid signal for the next stage

  logic  next_val_M;
  assign next_val_M = val_M && !stall_M;

  //----------------------------------------------------------------------
  // W stage
  //----------------------------------------------------------------------

  // Register enable logic

  assign reg_en_W = !stall_W;

  logic [31:0] inst_W;
  logic        proc2mngr_val_W;
  logic        rf_wen_pending_W;

  // Pipeline registers

  always_ff @( posedge clk ) begin
    if (reset) begin
      val_W            <= 1'b0;
      stats_en_wen_W   <= 1'b0;
    end else if (reg_en_W) begin
      val_W            <= next_val_M;
      rf_wen_pending_W <= rf_wen_pending_M;
      inst_W           <= inst_M;
      rf_waddr_W       <= rf_waddr_M;
      proc2mngr_val_W  <= proc2mngr_val_M;
      stats_en_wen_W   <= stats_en_wen_M;
    end
  end

  // write enable

  assign rf_wen_W = val_W && rf_wen_pending_W;

  // ostall due to proc2mngr

  assign ostall_W = val_W && proc2mngr_val_W && !proc2mngr_rdy;

  // stall and squash signal used in W stage

  assign stall_W = val_W && ostall_W;

  // proc2mngr port

  assign proc2mngr_val = val_W && !stall_W && proc2mngr_val_W;

  assign commit_inst = val_W && !stall_W;

endmodule

`endif

