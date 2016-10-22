//=========================================================================
// Baseline Blocking Cache Control
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_BASE_CTRL_V
`define LAB3_MEM_BLOCKING_CACHE_BASE_CTRL_V

`include "vc/mem-msgs.v"
`include "vc/assert.v"
`include "vc/regs.v"
`include "vc/arithmetic.v"
`include "vc/regfiles.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab3_mem_BlockingCacheBaseCtrlVRTL
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

  output  logic        cachereq_en,
  output  logic        memresp_en,
  output  logic        write_data_mux_sel,
  output  logic        tag_array_ren,
  output  logic        tag_array_wen,
  output  logic        data_array_ren,
  output  logic        data_array_wen,
  output  logic [15:0] data_array_wben,
  output  logic        read_data_reg_en,  
  output  logic        evict_addr_reg_en,
  output  logic [1:0]  read_word_mux_sel,
  output  logic        memreq_addr_mux_sel,
  output  logic [2:0]  cacheresp_type,
  output  logic [1:0]  hit,
  output  logic [2:0]  memreq_type,

  // status signals (dpath->ctrl)

  input logic  [2:0]  cachereq_type,
  input logic [31:0]  cachereq_addr,
  input logic         tag_match


 );
  //----------------------------------------------------------------------
  // State Defions
  //----------------------------------------------------------------------
  localparam STATE_IDLE                 = 2'd0;
  localparam STATE_TAG_CHECK            = 2'd1;
  localparam STATE_INIT_DATA_ACCESS     = 2'd2;
  localparam STATE_READ_DATA_ACCESS     = 2'd3;
  localparam STATE_WRITE_DATA_ACCESS    = 2'd4;
  localparam STATE_EVICT_PREPARE        = 2'd5;
  localparam STATE_EVICT_REQUEST        = 2'd6;
  localparam STATE_EVICT_WAIT           = 2'd7;
  localparam STATE_REFILL_REQUEST       = 2'd8;
  localparam STATE_REFILL_WAIT          = 2'd9;
  localparam STATE_EVICT_UPDATE         = 2'd10;
  localparam STATE_WAIT                 = 2'd11;
  
  // local parameters not meant to be set from outside
  localparam size = 256;             // Cache size in bytes
  localparam dbw  = 32;              // Short name for data bitwidth
  localparam abw  = 32;              // Short name for addr bitwidth
  localparam o    = 8;               // Short name for opaque bitwidth
  localparam clw  = 128;             // Short name for cacheline bitwidth
  localparam nbl  = size*8/clw;      // Number of blocks in the cache
  localparam nby  = nbl;             // Number of blocks per way
  localparam idw  = $clog2(nby);     // Short name for index bitwidth
  localparam ofw  = $clog2(clw/8);   // Short name for the offset bitwidth
  // In this lab, to simplify things, we always use all bits except for the
  // offset in the tag, rather than storing the "normal" 24 bits. This way,
  // when implementing a multi-banked cache, we don't need to worry about
  // re-inserting the bank id into the address of a cacheline.
  localparam tgw  = abw - ofw;       // Short name for the tag bitwidth

  logic [1:0] cache_state;
  logic [1:0] cache_state_update;
  
  // state reg
  vc_Regfile_1r1w #(2, 16, 4) state_reg
  (
  .clk    (clk),
  .reset  (reset),

  // Read port (combinational read)

  .read_addr (cachereq_addr[3:0]),
  .read_data (cache_state),

  // Write port (sampled on the rising clock edge)

  .write_en (data_array_wen),
  .write_addr (cachereq_addr[3:0]),
  .write_data (cache_state_update)
);

  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------

  logic [1:0] state_curr;
  logic [1:0] state_next;

 always @(posedge clk) begin    //always_ff @( posedge clk ) begin
    if ( reset ) begin
      state_curr <= STATE_IDLE;
    end
    else begin
      state_curr <= state_next;    
    end
end
                      
  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------

  logic idle_go;
  logic tc_goto_in;
  logic tc_goto_rd;
  logic wait_go;
  /*
  logic tc_goto_wd;
  logic tc_goto_rr;
  logic rr_goto_rw;
  logic rw_goto_ru;
  logic ru_goto_rd;
  logic ru_goto_wd;*/

  
  assign idle_go = cachereq_val && cachereq_rdy;
  assign tc_goto_in = (cachereq_type == 3'd2);
  assign wait_go =  cacheresp_rdy;
  
  //type = read, test = hit
  assign tc_goto_rd = (cachereq_type == 3'd0 && tag_match == 1 );
/*
  //type = write, test = hit
  assign tc_goto_wd = (cacheresp_type == 3'd1 && cacheresp[35:34]==2'b1);
  //type = 3'dx, test = miss
  assign tc_goto_rr = (cacheresp[35:34] == 2'b0 && cache_state == 2'b10 );
  assign rr_goto_rw = (memreq_val && memreq_rdy);
  assign rw_goto_ru = (memresp_val && memresp_rdy);
  assign ru_goto_rd = (cacheresp_type == 3'd0);
  assign ru_goto_wd = (cacheresp_type == 3'd1);*/
  
  
  always @ (*) begin          //always_comb begin 

    case (state_curr)
      
      STATE_IDLE: if( idle_go )    state_next = STATE_TAG_CHECK;
      
      STATE_TAG_CHECK:          
      if( tc_goto_in )         state_next = STATE_INIT_DATA_ACCESS;
      
      else if ( tc_goto_rd )   state_next = STATE_READ_DATA_ACCESS;
 /*     else if ( tc_goto_wd )   state_next = STATE_WRITE_DATA_ACCESS; 
      else if ( tc_goto_rr )   state_next = STATE_REFILL_REQUEST;*/   
      
      STATE_INIT_DATA_ACCESS:   state_next = STATE_WAIT;
    //  STATE_READ_DATA_ACCESS:   state_next = STATE_WAIT; 
    /*  STATE_REFILL_REQUEST: if (rr_goto_rw) state_next = STATE_REFILL_WAIT;
      STATE_REFILL_WAITL:   if (rw_goto_ru) state_next = STATE_UPDATE;
      
      STATE_UPDATE: if(ru_goto_rd) state_next = STATE_READ_DATA_ACCESS;
                    else if (ru_goto_wd) state_next = STATE_WRITE_DATA_ACCESS;
     */ 
      
      STATE_WAIT: if( wait_go )  state_next = STATE_IDLE;
    endcase

  end
  //----------------------------------------------------------------------
  // State Outputs
  //----------------------------------------------------------------------
  localparam write_x   = 1'dx;  
  localparam write_rp  = 1'd0;
  localparam write_mem = 1'd1;

  localparam read_x  = 2'bxx;
  localparam read_w3 = 2'b11;
  localparam read_w2 = 2'b10;
  localparam read_w1 = 2'b01;
  localparam read_w0 = 2'b00;

  localparam mem_x  = 1'dx;
  localparam mem_ev = 1'd1;
  localparam mem_cl = 1'd0; 
 
  task cs
  ( 
    logic        cs_cachereq_rdy,
    logic        cs_cacheresp_val,
    logic        cs_memreq_val,
    logic        cs_memresp_rdy,

    logic        cs_cachereq_en,
    logic        cs_memresp_en,
    
    logic        cs_write_data_mux_sel, 
   
    logic        cs_tag_array_ren,
    logic        cs_tag_array_wen,
 
    logic        cs_data_array_ren,
    logic        cs_data_array_wen,
    logic [15:0] cs_data_array_wben,
    
    logic        cs_read_data_reg_en,
    logic        cs_evict_addr_reg_en,

    logic [1:0]  cs_read_word_mux_sel,
    logic        cs_memreq_addr_mux_sel,

    logic [2:0]  cs_cacheresp_type,
    logic [1:0]  cs_hit,
    logic [2:0]  cs_memreq_type    

  );
  begin
    cachereq_rdy          = cs_cachereq_rdy;
    cacheresp_val         = cs_cacheresp_val;

    memresp_rdy           = cs_memresp_rdy;
    memreq_val            = cs_memreq_val;

    cachereq_en           = cs_cachereq_en;
    memresp_en            = cs_memresp_en;

    write_data_mux_sel    = cs_write_data_mux_sel;

    tag_array_ren         = cs_tag_array_ren;
    tag_array_wen         = cs_tag_array_wen;
  
    data_array_ren        = cs_data_array_ren;
    data_array_wen        = cs_data_array_wen;
    data_array_wben       = cs_data_array_wben;

    read_data_reg_en      = cs_read_data_reg_en;
    evict_addr_reg_en     = cs_evict_addr_reg_en;

    read_word_mux_sel     = cs_read_word_mux_sel;
    memreq_addr_mux_sel   = cs_memreq_addr_mux_sel;

    cacheresp_type        = cs_cacheresp_type;
    hit                   = cs_hit;
    memreq_type           = cs_memreq_type;


    
  end
  endtask
  // Set outputs using a control signal "table"

  always @(*) begin //always_comb begin

    cs( 0, 0, 0, 0, 0, 0, write_x, 1'dx,  1'd0,  1'dx,  1'd0,  16'dx, 0, 0, read_x,  mem_x, 3'dx, 2'dx, 3'dx );
    case ( state_curr )
      //                             cachereq cacheresp memresp memreq   cachereq  memresp  write    tag    tag    data   data   data       read   evict  read    memreq  cacheresp  hit        memreq
      //                                                                                    data     array  array  array  array  array      data   addr           addr       
      //                             rdy      val       rdy     val      en        en       mux      ren    wen    ren    wen    wben       regen  regen  mux     mux     type                  type
      STATE_IDLE:                 cs( 1,      0,        0,      0,       1,        0,       write_x, 1'dx,  1'dx,  1'dx,  1'dx,  16'dx,     0,     0,     read_x,  mem_x,  3'dx,      2'dx,     3'dx );
      STATE_TAG_CHECK:            cs( 0,      0,        0,      0,       1,        0,       write_x, 0,     1,     0,     0,     16'dx,     0,     0,     read_x,  mem_x,  0,         0,        0    );
      STATE_INIT_DATA_ACCESS:     cs( 0,      0,        0,      0,       1,        0,       write_rp,0,     1,     1,     1,     16'd65535, 0,     0,     read_x,  mem_x,  3'd2,      2'd0,     3'dx );
      STATE_WAIT:                 cs( 0,      1,        0,      0,       0,        0,       write_x, 0,     0,     0,     0,     0,         0,     0,     read_x,  mem_x,  3'd2,      0,        3'dx );
      default                     cs( 1'dx,   1'dx,     1'dx,   1'dx,    1'dx,     0,       write_x, 0,     0,     0,     1'dx,  0,         0,     0,     read_x,  mem_x,  3'dx,      2'dx,     3'dx );

    endcase

  end
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement control unit
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

endmodule

`endif
