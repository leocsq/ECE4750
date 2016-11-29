//=========================================================================
// Baseline Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_ALT_DPATH_V
`define LAB3_MEM_BLOCKING_CACHE_ALT_DPATH_V

`include "vc/mem-msgs.v"
`include "vc/arithmetic.v"
`include "vc/muxes.v"
`include "vc/regs.v"
`include "vc/srams.v"


module lab3_mem_BlockingCacheAltDpathVRTL
#(
  parameter p_idx_shamt    = 0
)
(
  input  logic                        clk,
  input  logic                        reset,

  // Cache Request
  input  mem_req_4B_t                 cachereq_msg,
  // Cache Response
  output mem_resp_4B_t                cacheresp_msg,
  // Memory Request
  output mem_req_16B_t                memreq_msg,
  // Memory Response
  input  mem_resp_16B_t               memresp_msg,
  
  // control signals (ctrl->dpath)
  
  input  logic                        cachereq_en,
  input  logic                        memresp_en,
  input  logic                        write_data_mux_sel,
  input  logic                        tag_array_ren,
  input  logic                        tag_array0_wen,
  input  logic                        tag_array1_wen,
  input  logic                        data_array_ren,
  input  logic                        data_array_wen,
  input  logic [15:0]                 data_array_wben,
  input  logic                        read_data_reg_en,
  input  logic                        evict_addr_reg_en,
  input  logic                        memreq_addr_mux_sel,
  input  logic [2:0]                  read_word_mux_sel,
  input  logic [2:0]                  cacheresp_type,
  input  logic [2:0]                  memreq_type,
  input  logic [1:0]                  hit,
  input  logic                        victim,
  input  logic                        match1,
 
  // status signals (dpath->ctrl)
  
  output logic [2:0]                  cachereq_type,
  output logic [31:0]                 cachereq_addr,
  output logic                        tag_match0,
  output logic                        tag_match1
  
);

  // local parameters not meant to be set from outside
  localparam size = 256;             // Cache size in bytes
  localparam dbw  = 32;              // Short name for data bitwidth
  localparam abw  = 32;              // Short name for addr bitwidth
  localparam o    = 8;               // Short name for opaque bitwidth
  localparam clw  = 128;             // Short name for cacheline bitwidth
  localparam nbl  = size*8/clw;      // Number of blocks in the cache
  localparam nby  = nbl/2;             // Number of blocks per way
  localparam idw  = $clog2(nby);     // Short name for index bitwidth
  localparam ofw  = $clog2(clw/8);   // Short name for the offset bitwidth
  // In this lab, to simplify things, we always use all bits except for the
  // offset in the tag, rather than storing the "normal" 24 bits. This way,
  // when implementing a multi-banked cache, we don't need to worry about
  // re-inserting the bank id into the address of a cacheline.
  localparam tgw  = abw - ofw;       // Short name for the tag bitwidth


  logic [o-1:0] cache_opaque;
  
  vc_EnResetReg #(o, 0) cachereq_opaque_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_en),
    .d      (cachereq_msg.opaque),
    .q      (cache_opaque)
  );
 
  vc_EnResetReg #(3, 0) cachereq_type_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_en),
    .d      (cachereq_msg.type_),
    .q      (cachereq_type)
  );
  
  vc_EnResetReg #(abw, 0) cachereq_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_en),
    .d      (cachereq_msg.addr),
    .q      (cachereq_addr)
  );

  logic [dbw-1:0] cachereq_data;
  
  vc_EnResetReg #(dbw, 0) cachereq_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_en),
    .d      (cachereq_msg.data),
    .q      (cachereq_data)
  );
  
  logic [clw-1:0] memresp_data;
  
  vc_EnResetReg #(clw, 0) memresp_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (memresp_en),
    .d      (memresp_msg.data),
    .q      (memresp_data)
  );
  
  logic [4*dbw-1:0] cachereq_data_repl;
  
  vc_repl #(dbw,4*dbw) Repl
  (
    .in     (cachereq_data),
    .out    (cachereq_data_repl)
  ); 
  
  logic [clw-1:0] write_data;
  
  vc_Mux2 #(clw) write_data_mux
  (
    .sel    (write_data_mux_sel),
    .in0    (cachereq_data_repl),
    .in1    (memresp_data),
    .out    (write_data)
  ); 
  
  // Tag Array0: FullWriteSRAM
  
  logic [tgw-1:0] cache_tag0;
  logic [idw-1:0] idx;
  
  assign idx = cachereq_addr[ofw+idw+p_idx_shamt-1:ofw+p_idx_shamt]; 
  
  vc_CombinationalBitSRAM_1rw
  #(tgw, nby) Tag_Array0
  (
    .clk          (clk),
    .reset        (reset),
    .read_en      (tag_array_ren),
    .read_addr    (idx),
    .read_data    (cache_tag0),
    .write_en     (tag_array0_wen),
    .write_addr   (idx),
    .write_data   (cachereq_addr[31:4])
  ); 
  
  // Tag Array1: FullWriteSRAM
  
  logic [tgw-1:0] cache_tag1; 
  
  vc_CombinationalBitSRAM_1rw
  #(tgw, nby) Tag_Array1
  (
    .clk          (clk),
    .reset        (reset),
    .read_en      (tag_array_ren),
    .read_addr    (idx),
    .read_data    (cache_tag1),
    .write_en     (tag_array1_wen),
    .write_addr   (idx),
    .write_data   (cachereq_addr[31:4])
  ); 
  
  // Data Array: ByteWriteSRAM
  
  logic [clw-1:0] read_data;
  
  vc_CombinationalSRAM_1rw
  #(clw, nbl) Data_Array
  (
    .clk           (clk),
    .reset         (reset),
    .read_en       (data_array_ren),
    .read_addr     ({victim,idx}),
    .read_data     (read_data),
    .write_en      (data_array_wen),
    .write_byte_en (data_array_wben),
	.write_addr    ({victim,idx}),
    .write_data    (write_data)
  );
 
  vc_EqComparator #(tgw) cmp0
  (
    .in0    (cachereq_addr[31:4]),
    .in1    (cache_tag0),
    .out    (tag_match0)
  );
  
  vc_EqComparator #(tgw) cmp1
  (
    .in0    (cachereq_addr[31:4]),
    .in1    (cache_tag1),
    .out    (tag_match1)
  );
  
  logic [tgw-1:0] cache_tag;
  
  vc_Mux2 #(tgw) cache_tag_mux
  (
    .sel    (victim),
    .in0    (cache_tag0),
    .in1    (cache_tag1),
    .out    (cache_tag)
  );
  
  logic [abw-1:0] evict_addr_pre;
  
  vc_mkaddr #(tgw,abw) mkaddr_ev
  (
    .in     (cache_tag),
    .out    (evict_addr_pre)
  );
  
  logic [abw-1:0] evict_addr;
  
  vc_EnResetReg #(abw, 0) evict_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (evict_addr_reg_en),
    .d      (evict_addr_pre),
    .q      (evict_addr)
  );
  
  logic [abw-1:0] refill_addr;
  
  vc_mkaddr #(tgw,abw) mkaddr_rf
  (
    .in     (cachereq_addr[31:4]),
    .out    (refill_addr)
  );

  logic [abw-1:0] memreq_msg_addr;
  
  vc_Mux2 #(abw) memreq_addr_mux
  (
    .sel    (memreq_addr_mux_sel),
    .in0    (evict_addr),
    .in1    (refill_addr),
    .out    (memreq_msg_addr)
  );
  
  logic [clw-1:0] cache_data;
  
  vc_EnResetReg #(clw, 0) read_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (read_data_reg_en),
    .d      (read_data),
    .q      (cache_data)
  );
  
  logic [dbw-1:0] cacheresp_msg_data;
  
  vc_Mux5 #(dbw) read_word_mux
  (
   .in0     (cache_data[31:0]),
   .in1     (cache_data[63:32]),
   .in2     (cache_data[95:64]),
   .in3     (cache_data[127:96]),
   .in4     (32'd0),
   .sel     (read_word_mux_sel),
   .out     (cacheresp_msg_data)
  );
  
  
  
  assign cacheresp_msg.type_  = cacheresp_type;
  assign cacheresp_msg.opaque = cache_opaque;
  assign cacheresp_msg.test   = hit;
  assign cacheresp_msg.len    = 2'd0;
  assign cacheresp_msg.data   = cacheresp_msg_data;
  
  assign memreq_msg.type_  = memreq_type;
  assign memreq_msg.opaque = 8'b0;
  assign memreq_msg.addr   = memreq_msg_addr;
  assign memreq_msg.len    = 4'd0;
  assign memreq_msg.data   = cache_data;
  
endmodule

`endif
