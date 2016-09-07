//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

`ifndef LAB1_IMUL_INT_MUL_BASE_V
`define LAB1_IMUL_INT_MUL_BASE_V

`include "vc/trace.v"
`include "vc/muxes.v"
`include "vc/regs.v"
`include "vc/arithmetic.v"

// ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// Define datapath and control unit here.
// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

//========================================================================
// IntMulBase Datapath
//========================================================================

module lab1_imul_IntMulBaseDpath
(
  input  logic        clk,
  input  logic        reset,

  // Data signals

  input  logic [63:0] req_msg,
  output logic [31:0] resp_msg,

  // Control signals

  input  logic        result_en,   // Enable for Result register
  input  logic        a_mux_sel,  // Sel for mux in front of A reg
  input  logic        b_mux_sel,  // sel for mux in front of B reg
  input  logic        result_mux_sel,  // Sel for mux in front of Result reg
  input  logic        add_mux_sel,  // sel for mux in back of Adder

  // Status signals

  output logic        b_lsb  // Lsb of B reg
);

  localparam c_nbits = 32;

  // Split out the a and b operands

  logic [c_nbits-1:0] req_msg_a = req_msg[63:32];
  logic [c_nbits-1:0] req_msg_b = req_msg[31:0 ];

  // A Mux

  logic [c_nbits-1:0] l_shift_out;
  logic [c_nbits-1:0] a_mux_out;

  vc_Mux2#(c_nbits) a_mux
  (
    .sel   (a_mux_sel),
    .in0   (l_shift_out),
    .in1   (req_msg_a),
    .out   (a_mux_out)
  );

  // A register

  logic [c_nbits-1:0] a_reg_out;

  vc_Reg#(c_nbits) a_reg
  (
    .clk   (clk),
    .d     (a_mux_out),
    .q     (a_reg_out)
  );
  
  // Left shifter
  
  //logic [2:0] shnum;
  
  vc_LeftLogicalShifter#(c_nbits,3) l_shift
  (
    .in    (a_reg_out),
    .shamt (3'd1),
    .out   (l_shift_out)
  );

  // B Mux

  logic [c_nbits-1:0] r_shift_out;
  logic [c_nbits-1:0] b_mux_out;

  vc_Mux2#(c_nbits) b_mux
  (
    .sel   (b_mux_sel),
    .in0   (r_shift_out),
    .in1   (req_msg_b),
    .out   (b_mux_out)
  );

  // B register

  logic [c_nbits-1:0] b_reg_out;
  
  vc_Reg#(c_nbits) b_reg
  (
    .clk   (clk),
    .d     (b_mux_out),
    .q     (b_reg_out)
  );
  
  // Right shifter
  
  vc_RightLogicalShifter#(c_nbits,3) r_shift
  (
    .in    (b_reg_out),
    .shamt (3'd1),
    .out   (r_shift_out)
  );

  // Result MUX
  
  logic [c_nbits-1:0] add_mux_out;
  logic [c_nbits-1:0] result_mux_out;
  
  vc_Mux2#(c_nbits) result_mux
  (
    .sel   (result_mux_sel),
    .in0   (add_mux_out),
    .in1   (0),
    .out   (result_mux_out)
  );
  
  // Result register
  
  logic [c_nbits-1:0] result_reg_out;
  
  vc_EnReg#(c_nbits) result_reg
  (
    .clk   (clk),
	.reset (reset),
    .d     (result_mux_out),
    .q     (result_reg_out),
	.en    (result_en)
  );
  
  // Adder
  
  logic [c_nbits-1:0] adder_out;
  
  vc_SimpleAdder#(c_nbits) adder
  (
    .in0   (a_reg_out),
    .in1   (result_reg_out),
    .out   (adder_out)
  );

  // Add MUX
  
  vc_Mux2#(c_nbits) add_mux
  (
    .sel   (add_mux_sel),
    .in0   (adder_out),
    .in1   (result_reg_out),
    .out   (add_mux_out)
  );
  
  // Connect to output port

  assign resp_msg = result_reg_out;
  assign b_lsb = b_reg_out[0]; 
  //assign shnum = b_reg_out[1]? 3'd1 : (b_reg_out[2]? 3'd2 : (b_reg_out[3]? 3'd3 : 3'd4));

endmodule

//========================================================================
// IntMulBase Control
//========================================================================

module lab1_imul_IntMulBaseCtrl
(
  input  logic        clk,
  input  logic        reset,

  // Dataflow signals

  input  logic        req_val,
  output logic        req_rdy,
  output logic        resp_val,
  input  logic        resp_rdy,

  // Control signals

  output logic        result_en,      // Enable for Result register
  output logic        a_mux_sel,      // Sel for mux in front of A reg
  output logic        b_mux_sel,      // sel for mux in front of B reg
  output logic        result_mux_sel, // sel for mux in front of Result reg
  output logic        add_mux_sel,    // sel for mux in back of Adder

  // Data signals

  input  logic        b_lsb  // Lsb of B reg

);

  //----------------------------------------------------------------------
  // State Definitions
  //----------------------------------------------------------------------

  localparam STATE_IDLE = 2'd0;
  localparam STATE_CALC = 2'd1;
  localparam STATE_DONE = 2'd2;

  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------

  logic [1:0] state_reg;
  logic [1:0] state_next;
  logic [5:0] counter;
  logic count_done;

  always @(posedge clk) begin    //always_ff @( posedge clk ) begin
    if ( reset ) begin
      state_reg <= STATE_IDLE;
		counter <= 0;
		count_done <= 0;
    end
    else begin
      state_reg <= state_next;
		if ( state_reg == STATE_CALC ) begin
		  if ( counter == 6'd32 ) begin
		    counter <= 0;
			 count_done <= 1;
		  end
		  else begin
		    counter <= counter + 1; 
		  end
		end
		else begin
		  count_done <= 0;  
		end
    end
  end

  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------

  logic req_go;
  logic resp_go;
  logic is_calc_done;

  assign req_go       = req_val  && req_rdy;
  assign resp_go      = resp_val && resp_rdy;
  assign is_calc_done = count_done;

  always @ (*) begin          //always_comb begin

    state_next = state_reg;

    case ( state_reg )

      STATE_IDLE: if ( req_go    )    state_next = STATE_CALC;
      STATE_CALC: if ( is_calc_done ) state_next = STATE_DONE;
      STATE_DONE: if ( resp_go   )    state_next = STATE_IDLE;
      default:    state_next = 2'dx;

    endcase

  end

  //----------------------------------------------------------------------
  // State Outputs
  //----------------------------------------------------------------------

  localparam a_x   = 1'dx;
  localparam a_ld  = 1'd1;
  localparam a_ls  = 1'd0;

  localparam b_x   = 1'dx;
  localparam b_ld  = 1'd1;
  localparam b_rs  = 1'd0;

  localparam r_x   = 1'dx;
  localparam r_o   = 1'd1;
  localparam r_a   = 1'd0;
  
  localparam ad_x  = 1'dx;
  localparam ad_n  = 1'd1;
  localparam ad_y  = 1'd0;
  
  task cs
  (
    input logic       cs_req_rdy,
    input logic       cs_resp_val,
	input logic       cs_result_en,
    input logic       cs_a_mux_sel,
    input logic       cs_b_mux_sel,
    input logic       cs_result_mux_sel,
    input logic       cs_add_mux_sel
  );
  begin
    req_rdy        = cs_req_rdy;
    resp_val       = cs_resp_val;
    result_en      = cs_result_en;
    a_mux_sel      = cs_a_mux_sel;
    b_mux_sel      = cs_b_mux_sel;
	result_mux_sel = cs_result_mux_sel;
	add_mux_sel    = cs_add_mux_sel;
  end
  endtask

  // Labels for Mealy transistions

  logic do_shift;
  logic do_addshift;

  assign do_shift = !b_lsb;
  assign do_addshift = b_lsb;

  // Set outputs using a control signal "table"

  always @(*) begin //always_comb begin

    cs( 0, 0, 0, a_x, b_x, r_x, ad_x );
    case ( state_reg )
      //                             req resp result a mux b mux result add mux	
      //                             rdy val  en     sel   sel   sel    sel
      STATE_IDLE:                 cs( 1,  0,   1,    a_ld, b_ld, r_o,   ad_n );
      STATE_CALC: if (do_shift)   cs( 0,  0,   1,    a_ls, b_rs, r_a,   ad_n );
             else if (do_addshift)cs( 0,  0,   1,    a_ls, b_rs, r_a,   ad_y );
      STATE_DONE:                 cs( 0,  1,   0,    a_x,  b_x,  r_x,   ad_x );
      default                     cs(1'dx,1'dx,1'dx, a_x,  b_x,  r_x,   ad_x );

    endcase

  end

endmodule

//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

module lab1_imul_IntMulBaseVRTL
(
  input  logic        clk,
  input  logic        reset,

  input  logic        req_val,
  output logic        req_rdy,
  input  logic [63:0] req_msg,

  output logic        resp_val,
  input  logic        resp_rdy,
  output logic [31:0] resp_msg
);

  // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Instantiate datapath and control models here and then connect them
  // together.
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  // Control signals

  logic        result_en;
  logic        a_mux_sel;
  logic        b_mux_sel;
  logic        result_mux_sel;
  logic        add_mux_sel;

  // Data signals

  logic        b_lsb;

  // Datapath

  lab1_imul_IntMulBaseDpath dpath
  (
    .clk(clk),
    .reset(reset),
	.req_msg(req_msg),
    .resp_msg(resp_msg),
    .result_en(result_en),   
    .a_mux_sel(a_mux_sel),  
    .b_mux_sel(b_mux_sel),  
    .result_mux_sel(result_mux_sel),  
    .add_mux_sel(add_mux_sel),  
    .b_lsb(b_lsb) 
  );

  // Control unit

  lab1_imul_IntMulBaseCtrl ctrl
  (
    .clk(clk),
    .reset(reset),
	.req_val(req_val),
    .req_rdy(req_rdy),
    .resp_val(resp_val),
    .resp_rdy(resp_rdy),
    .result_en(result_en),   
    .a_mux_sel(a_mux_sel),  
    .b_mux_sel(b_mux_sel),  
    .result_mux_sel(result_mux_sel),  
    .add_mux_sel(add_mux_sel),  
    .b_lsb(b_lsb) 
  );
  
  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    $sformat( str, "%x", req_msg );
    vc_trace.append_val_rdy_str( trace_str, req_val, req_rdy, str );

    vc_trace.append_str( trace_str, "(" );

    // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Add additional line tracing using the helper tasks for
    // internal state including the current FSM state.
    // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    vc_trace.append_str( trace_str, ")" );

    $sformat( str, "%x", resp_msg );
    vc_trace.append_val_rdy_str( trace_str, resp_val, resp_rdy, str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */   
                                
endmodule

`endif /* LAB1_IMUL_INT_MUL_BASE_V */

