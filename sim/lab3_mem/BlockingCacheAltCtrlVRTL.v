//=========================================================================
// Baseline Blocking Cache Control
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_ALT_CTRL_V
`define LAB3_MEM_BLOCKING_CACHE_ALT_CTRL_V

`include "vc/mem-msgs.v"
`include "vc/assert.v"
`include "vc/regfiles.v"
`include "vc/regs.v"
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab3_mem_BlockingCacheAltCtrlVRTL
#(
  parameter p_idx_shamt    = 0
)
(
  input  logic                        clk,
  input  logic                        reset,

  // Cache Request
  input  logic                        cachereq_val,
  output logic                        cachereq_rdy,
  // Cache Response
  output logic                        cacheresp_val,
  input  logic                        cacheresp_rdy,
  // Memory Request
  output logic                        memreq_val,
  input  logic                        memreq_rdy,
  // Memory Response
  input  logic                        memresp_val,
  output logic                        memresp_rdy,

  // control signals (ctrl->dpath)
  
  output logic                        cachereq_en,
  output logic                        memresp_en,
  output logic                        write_data_mux_sel,
  output logic                        tag_array_ren,
  output logic                        tag_array0_wen,
  output logic                        tag_array1_wen,
  output logic                        data_array_ren,
  output logic                        data_array_wen,
  output logic [15:0]                 data_array_wben,
  output logic                        read_data_reg_en,
  output logic                        evict_addr_reg_en,
  output logic                        memreq_addr_mux_sel,
  output logic [2:0]                  read_word_mux_sel,
  output logic [2:0]                  cacheresp_type,
  output logic [2:0]                  memreq_type,
  output logic [1:0]                  hit,
  output logic                        victim,
  output logic                        match1,
  
  // status signals (dpath->ctrl)
  
  input  logic [2:0]                  cachereq_type,
  input  logic [31:0]                 cachereq_addr,
  input  logic                        tag_match0,
  input  logic                        tag_match1
 );

  // local parameters not meant to be set from outside
  localparam size = 256;             // Cache size in bytes
  localparam dbw  = 32;              // Short name for data bitwidth
  localparam abw  = 32;              // Short name for addr bitwidth
  localparam o    = 8;               // Short name for opaque bitwidth
  localparam clw  = 128;             // Short name for cacheline bitwidth
  localparam nbl  = size*8/clw;      // Number of blocks in the cache
  localparam nby  = nbl/2;           // Number of blocks per way
  localparam idw  = $clog2(nby);     // Short name for index bitwidth
  localparam ofw  = $clog2(clw/8);   // Short name for the offset bitwidth
  // In this lab, to simplify things, we always use all bits except for the
  // offset in the tag, rather than storing the "normal" 24 bits. This way,
  // when implementing a multi-banked cache, we don't need to worry about
  // re-inserting the bank id into the address of a cacheline.
  localparam tgw  = abw - ofw;       // Short name for the tag bitwidth
  
  localparam type_x  = 3'dx;
  localparam type_r  = 3'd0;
  localparam type_w  = 3'd1;
  localparam type_in = 3'd2;
  
  assign cacheresp_type = cachereq_type;

  
  
  //                                       1     0                                 
  // Track the state of each tag entry. |valid|dirty|
  
  logic [1:0] entry_state;
  logic [1:0] entry_state_in0;
  logic [1:0] entry_state_in1;
  logic [1:0] entry_state0;
  logic [1:0] entry_state1;
  logic [1:0] entry_state_update;
  logic  entry_state_ren;
  logic  entry_state_wen0;
  logic  entry_state_wen1;
  logic  use_state;
  logic  use_update;
  logic  use_wen;
  

  vc_ResetRegfile_1r1w #(2,nby,0) entry_state_regfile0
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr[6:4]),
    .read_data  (entry_state_in0),
    .write_en   (entry_state_wen0),
    .write_addr (cachereq_addr[6:4]),
    .write_data (entry_state_update)
  );
  
  vc_ResetRegfile_1r1w #(2,nby,0) entry_state_regfile1
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr[6:4]),
    .read_data  (entry_state_in1),
    .write_en   (entry_state_wen1),
    .write_addr (cachereq_addr[6:4]),
    .write_data (entry_state_update)
  );
  
  vc_EnReg #(2) entry_state_reg0
  (
    .clk        (clk),  
    .reset      (reset), 
    .q          (entry_state0),     
    .d          (entry_state_in0),     
    .en         (entry_state_ren)
  );
  
  vc_EnReg #(2) entry_state_reg1
  (
    .clk        (clk),  
    .reset      (reset), 
    .q          (entry_state1),     
    .d          (entry_state_in1),     
    .en         (entry_state_ren)
  );
  
  vc_Mux2 #(2) entry_state_mux
  (
    .sel    (victim),
    .in0    (entry_state0),
    .in1    (entry_state1),
    .out    (entry_state)
  );
  
  vc_ResetRegfile_1r1w #(1,nby,0) usebit_regfile
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr[6:4]),
    .read_data  (use_state),
    .write_en   (use_wen),
    .write_addr (cachereq_addr[6:4]),
    .write_data (use_update)
  );
  
  logic match;
  logic match1;
  logic dirty;
  
  
  assign match = (tag_match0 & entry_state0[1]) || (tag_match1 & entry_state1[1]);
  assign match1 =  tag_match1 & entry_state1[1];
  assign victim = match? match1 : use_state;
  assign dirty = entry_state[0];
  assign hit = {1'b0,match}; 
  
 
  //----------------------------------------------------------------------
  // State Definitions
  //----------------------------------------------------------------------

  localparam I     = 4'd0;
  localparam TC    = 4'd1;
  localparam IN    = 4'd2;
  localparam RD    = 4'd3;
  localparam WD    = 4'd4;
  localparam EP    = 4'd5;
  localparam ER    = 4'd6;
  localparam EW    = 4'd7;
  localparam RR    = 4'd8;
  localparam RW    = 4'd9;
  localparam RU    = 4'd10;
  localparam W     = 4'd11;
  
  //----------------------------------------------------------------------
  // State Update
  //----------------------------------------------------------------------

  logic [3:0] state_reg;
  logic [3:0] state_next;

  always @(posedge clk) begin    
    if ( reset ) state_reg <= I;
    else state_reg <= state_next;    
  end

  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------
  
  logic idle_go;
  logic wait_go;
  logic tc_goto_in;
  logic tc_goto_rd;
  logic tc_goto_wd;
  logic tc_goto_rr;
  logic rr_goto_rw;
  logic rw_goto_ru;
  logic ru_goto_rd;
  logic ru_goto_wd;
  logic tc_goto_ep;
  logic er_goto_ew;
  logic ew_goto_rr;
  
 
 
  
  assign idle_go    =  cachereq_val;
  assign wait_go    =  cacheresp_rdy;
  assign tc_goto_in = (cachereq_type == type_in);
  assign tc_goto_rd = (cachereq_type == type_r)&& match;
  assign tc_goto_wd = (cachereq_type == type_w)&& match;
  assign tc_goto_rr = !match && !dirty;
  assign rr_goto_rw =  memreq_rdy;
  assign rw_goto_ru =  memresp_val;
  assign ru_goto_rd = (cachereq_type == type_r);
  assign ru_goto_wd = (cachereq_type == type_w);
  assign tc_goto_ep = !match && dirty;
  assign er_goto_ew =  memreq_rdy;
  assign ew_goto_rr =  memresp_val;
  
  always @ (*) begin         

    state_next = state_reg;

    case ( state_reg )

      I : if ( idle_go )         state_next = TC;
      TC: if ( tc_goto_in )      state_next = IN;
		  else if ( tc_goto_rd ) state_next = RD;
		  else if ( tc_goto_wd ) state_next = WD;
		  else if ( tc_goto_rr ) state_next = RR;
		  else if ( tc_goto_ep ) state_next = EP;
	  IN:                        state_next = W ;
	  RD:                        state_next = W ;
	  WD:                        state_next = W ;
	  EP:                        state_next = ER;
	  ER: if ( er_goto_ew )      state_next = EW;
	  EW: if ( ew_goto_rr )      state_next = RR;
	  RR: if ( rr_goto_rw )      state_next = RW;
	  RW: if ( rw_goto_ru )      state_next = RU;
	  RU: if ( ru_goto_rd )      state_next = RD;
	      else if ( ru_goto_wd ) state_next = WD;
      W : if ( wait_go )         state_next = I;
      default:                   state_next = 4'dx;

    endcase

  end
  
  //----------------------------------------------------------------------
  // State Outputs
  //----------------------------------------------------------------------
  localparam n = 1'd0;
  localparam y = 1'd1;
  
  // Write Data Mux Select 
  
  localparam wd_x     = 1'bx; 
  localparam wd_cq    = 1'b0; 
  localparam wd_mp    = 1'b1;
  
  // Memreq Address Mux Select
  
  localparam ma_x     = 1'bx; 
  localparam ma_ev    = 1'b0; 
  localparam ma_rf    = 1'b1;
  
  // Read Word Mux Select
  
  localparam rw_n     = 3'd4; 
  
  // Data Array Wben
  
  localparam wb_n     = 16'd0;
  localparam wb_a     = 16'hFFFF;
  
  // Tag Entry State
  
  localparam es_x     = 2'dx;
  
  // Entry Wen
  
  localparam ew_n     = 1'b0;
  
  // Use Bit Update
  
  localparam use_x    = 1'bx;
  
  
  logic [2:0]  rw_y;
  logic [15:0] wb_y;
  logic [1:0]  es_v;
  logic [1:0]  es_d;
  logic [1:0]  es_c;
  logic ew_y;
  logic use_y;
  
  
  assign es_v  = entry_state | 2'b10;
  assign es_d  = entry_state | 2'b11;
  assign es_c  = entry_state & 2'b10;
  assign rw_y  = {1'b0,cachereq_addr[3:2]};
  assign ew_y  = victim;
  assign use_y = !victim;
  
  
  
  always @(*) begin 
    case ( cachereq_addr[3:2] )
	   
		2'd0:    wb_y = 16'h000F;
		2'd1:    wb_y = 16'h00F0;
		2'd2:    wb_y = 16'h0F00;
		2'd3:    wb_y = 16'hF000;
	   default:  wb_y = wb_n;
		
	 endcase
  end
  
  
  task cs
  (
    input logic        cs_cachereq_rdy,
    input logic        cs_cacheresp_val,
	input logic        cs_memreq_val,
    input logic        cs_memresp_rdy,
	 
    input logic        cs_cachereq_en,
    input logic        cs_memresp_en, 
    input logic        cs_write_data_mux_sel,
	input logic        cs_tag_array_ren,
    input logic        cs_tag_array0_wen,
    input logic        cs_tag_array1_wen,
    input logic        cs_data_array_ren,
    input logic        cs_data_array_wen,
    input logic [15:0] cs_data_array_wben,
    input logic        cs_read_data_reg_en,
    input logic        cs_evict_addr_reg_en,
    input logic        cs_memreq_addr_mux_sel,
    input logic [2:0]  cs_read_word_mux_sel,
    input logic [2:0]  cs_memreq_type,
	input logic        cs_entry_state_wen0,
	input logic        cs_entry_state_wen1,
	input logic [1:0]  cs_entry_state_update,
	input logic        cs_entry_state_ren,
	input logic        cs_use_update,
	input logic        cs_use_wen
  );
  begin
    cachereq_rdy        = cs_cachereq_rdy;
    cacheresp_val       = cs_cacheresp_val;
    memreq_val          = cs_memreq_val;
    memresp_rdy         = cs_memresp_rdy;
	 
    cachereq_en         = cs_cachereq_en;
    memresp_en          = cs_memresp_en;
    write_data_mux_sel  = cs_write_data_mux_sel;
    tag_array_ren       = cs_tag_array_ren;
    tag_array0_wen      = cs_tag_array0_wen;
    tag_array1_wen      = cs_tag_array1_wen;
    data_array_ren      = cs_data_array_ren;
    data_array_wen      = cs_data_array_wen;
    data_array_wben     = cs_data_array_wben;
    read_data_reg_en    = cs_read_data_reg_en;
    evict_addr_reg_en   = cs_evict_addr_reg_en;
    memreq_addr_mux_sel = cs_memreq_addr_mux_sel;
    read_word_mux_sel   = cs_read_word_mux_sel;
    memreq_type         = cs_memreq_type;
	entry_state_wen0    = cs_entry_state_wen0;
	entry_state_wen1    = cs_entry_state_wen1;
	entry_state_update  = cs_entry_state_update;
	entry_state_ren     = cs_entry_state_ren;
	use_update          = cs_use_update;
	use_wen             = cs_use_wen;
  end
  endtask
  

  always @(*) begin 

    case ( state_reg )
      //     c_req c_resp m_req m_resp c_req m_resp w_data tag tag0 tag1 data data data r_data e_addr mreq_addr readword m_req    entry entry  entry   entry use    use        	
      //     rdy   val    val   rdy    en    en     muxsel ren wen  wen  ren  wen  wben regen  regen  muxsel    muxsel   type     wen0  wen1   update  ren   update wen
      I : cs( y,    n,    n,    n,     y,    n,     wd_x,   n,  n,   n,   n,   n,  wb_n,   n,     n,   ma_x,     rw_n,   type_x,  ew_n, ew_n,  es_x,   y,   use_x,  n );
      TC: cs( n,    n,    n,    n,     n,    n,     wd_x,   y,  n,   n,   n,   n,  wb_n,   n,     n,   ma_x,     rw_n,   type_x,  ew_n, ew_n,  es_x,   y,   use_x,  n );
      IN: cs( n,    n,    n,    n,     n,    n,     wd_cq,  n,  n,   n,   n,   y,  wb_a,   n,     n,   ma_x,     rw_n,   type_x, !ew_y, ew_y,  es_v,   n,   use_x,  n );
      RD: cs( n,    n,    n,    n,     n,    n,     wd_x,   y,  n,   n,   y,   n,  wb_y,   y,     n,   ma_x,     rw_y,   type_x, !ew_y, ew_y,  es_v,   n,   use_x,  n ); 
      WD: cs( n,    n,    n,    n,     n,    n,     wd_cq,  y,  n,   n,   n,   y,  wb_y,   n,     n,   ma_x,     rw_n,   type_x, !ew_y, ew_y,  es_d,   n,   use_x,  n ); 
      EP: cs( n,    n,    n,    n,     n,    n,     wd_x,   y,  n,   n,   y,   n,  wb_n,   y,     y,   ma_ev,    rw_n,   type_w, !ew_y, ew_y,  es_c,   n,   use_x,  n );
      ER: cs( n,    n,    y,    n,     n,    y,     wd_x,   y,  n,   n,   n,   n,  wb_n,   n,     n,   ma_ev,    rw_n,   type_w,  ew_n, ew_n,  es_x,   n,   use_x,  n );
      EW: cs( n,    n,    n,    y,     n,    y,     wd_x,   y,  n,   n,   n,   n,  wb_n,   n,     n,   ma_ev,    rw_n,   type_w,  ew_n, ew_n,  es_x,   n,   use_x,  n );
      RR: cs( n,    n,    y,    n,     n,    y,     wd_mp,  y,  n,   n,   n,   y,  wb_a,   n,     n,   ma_rf,    rw_n,   type_r,  ew_n, ew_n,  es_x,   n,   use_x,  n );
      RW: cs( n,    n,    n,    y,     n,    y,     wd_mp,  y,  n,   n,   n,   y,  wb_a,   n,     n,   ma_rf,    rw_n,   type_r,  ew_n, ew_n,  es_x,   n,   use_x,  n );
      RU: cs( n,    n,    n,    n,     n,    n,     wd_mp,  y,  n,   n,   n,   y,  wb_a,   n,     n,   ma_rf,    rw_n,   type_x,  ew_n, ew_n,  es_x,   n,   use_x,  n ); 
      W : cs( n,    y,    n,    n,     n,    n,     wd_x,   y,!ew_y,ew_y, y,   n,  wb_n,   y,     n,   ma_x,     rw_y,   type_x,  ew_n, ew_n,  es_x,   n,   use_y,  y );
		
      default: 
	      cs( n,    n,    n,    n,     n,    n,     wd_x,   n,  n,   n,   n,   n,  wb_n,   n,     n,   ma_x,     rw_n,   type_x,  ew_n, ew_n,  es_x,   n,   use_x,  n );

    endcase
	 
  end
  
  
  
endmodule

`endif
