//=========================================================================
// Alternative Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_ALT_DPATH_V
`define LAB3_MEM_BLOCKING_CACHE_ALT_DPATH_V

`include "vc/mem-msgs.v"
`include "vc/arithmetic.v"
`include "vc/muxes.v"
`include "vc/regs.v"
`include "vc/srams.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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

  input  logic        cachereq_en,
  input  logic        memresp_en,
  input  logic        write_data_mux_sel,
  input  logic        way0_tag_array_ren,
  input  logic        way0_tag_array_wen,
  input  logic        way1_tag_array_ren,
  input  logic        way1_tag_array_wen,
  input  logic        data_array_ren,
  input  logic        data_array_wen,
  input  logic [15:0] data_array_wben,
  input  logic        read_data_reg_en,  
  input  logic        evict_addr_reg_en,
  input  logic [1:0]  read_word_mux_sel,
  input  logic        memreq_addr_mux_sel,
  input  logic [2:0]  cacheresp_type,
  input  logic [1:0]  hit,
  input  logic [2:0]  memreq_type,

  // status signals (dpath->ctrl)

  output logic [2:0]   cachereq_type,
  output logic [31:0]  cachereq_addr,
  output logic         tag_match0,
  output logic         tag_match1,
  output logic         tag_match

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Add dpath signals
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement Dpath
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Cachereq_Opaque Register
   
   logic [o-1:0] cachereq_msg_opaque_in;
   logic [o-1:0] cachereq_msg_opaque_out;
   
   assign cachereq_msg_opaque_in = cachereq_msg [73:66];
   
   vc_EnResetReg #(o,0) Cachereq_Opaque_reg 
   (
      .clk    (clk),
      .reset  (reset),
      .d      (cachereq_msg_opaque_in),
      .q      (cachereq_msg_opaque_out),
      .en     (cachereq_en)
   );
   assign cacheresp_msg [43:36] = cachereq_msg_opaque_out;
   // Cachereq_Type Register
  
   //localparam type = 3;
   logic [2:0] cachereq_msg_type_in;
   logic [2:0] cachereq_msg_type_out;
   
   assign cachreq_msg_type_in = cachereq_msg [76:74];
   
   vc_EnResetReg #(3,0) Cachereq_Type_reg
   (
      .clk    (clk),
      .reset  (reset),
      .d      (cachereq_msg_type_in),
      .q      (cachereq_msg_type_out),
      .en     (cachereq_en)
   );
   
   // Cachereq_Addr Register
   
   logic [abw-1:0] cachereq_msg_addr_in;
   logic [abw-1:0] cachereq_msg_addr_out;
   
   assign cachreq_msg_addr_in = cachereq_msg [65:43];
   
   vc_EnResetReg #(abw,0) Cachereq_Addr_reg
   (
      .clk    (clk),
      .reset  (reset),
      .d      (cachereq_msg_addr_in),
      .q      (cachereq_msg_addr_out),
      .en     (cachereq_en)
   );
   
   // Cachereq_Data Register
   
   logic [dbw-1:0] cachereq_msg_data_in;
   logic [dbw-1:0] cachereq_msg_data_out;
   
   assign cachreq_msg_data_in = cachereq_data [31:0];
   
   vc_EnResetReg #(dbw,0) Cachereq_Data_reg
   (
     .clk     (clk),
     .reset   (reset),
     .d       (cachereq_msg_data_in),
     .q       (cachereq_msg_data_out),
     .en      (cachereq_en)
   );
   
   // Memresp_Data Register
   
   localparam mdata = 128;
   logic [mdata-1:0] memresp_msg_data_in;
   logic [mdata-1:0] memresp_msg_data_out; 
   
   assign memresp_msg_data_in = memresp_msg [127:0]; 
    
   vc_EnResetReg #(mdata,0) Memresp_Data_reg
   (
     .clk     (clk),
     .reset   (reset),
     .d       (memresp_msg_data_in),
     .q       (memresp_msg_data_out),
     .en      (memresp_en)
   );
   
   //Repl
   
   logic [mdata-1:0] write_data_out;
   vc_repl #(32,128) Repl
   (
    .in       (cachereq_msg_data_out),
    .out      (write_data_out)
   );
   
   // Write_Data Mux
   
   logic [mdata-1:0] write_data_out;
   vc_Mux2 #(mdata-1) Write_Data_mux
   (
    .sel   (write_data_mux_sel),
    .in0   (repl_data_out),
    .in1   (memresp_msg_data_out),
    .out   (write_data_out)
  );
  
   // Way0_Tag_Array_SRAM
  
   logic [27:0] way0_mem_tag [7:0];
   vc_CombinationalBitSRAM_1rw
   #(28, 8, 3) Way0_Tag_Array
   (
   .clk         (clk),
   .reset       (reset),
   .read_en     (way0_tag_array_ren),
   .read_addr   (cachereq_msg_addr_out[6:4]),
   .read_data   (way0_mem_tag),
   .write_en    (way0_tag_array_wen),
   .write_addr  (cachereq_msg_addr_out[6:4]),
   .write_data  (cachereq_msg_addr_out[31:4])
); 

   // Way1_Tag_Array_SRAM
  
   logic [27:0] way1_mem_tag [7:0];
   vc_CombinationalBitSRAM_1rw
   #(28, 8, 3) Way1_Tag_Array
   (
   .clk         (clk),
   .reset       (reset),
   .read_en     (way1_tag_array_ren),
   .read_addr   (cachereq_msg_addr_out[6:4]),
   .read_data   (way1_mem_tag),
   .write_en    (way1_tag_array_wen),
   .write_addr  (cachereq_msg_addr_out[6:4]),
   .write_data  (cachereq_msg_addr_out[31:4])
); 

   // Data_Array_SRAM
  
   logic [127:0] mem_data [15:0];
   vc_CombinationalSRAM_1rw
   #( 128, 16, 4, 16 ) Data_Array
   (
   .clk             (clk),
   .reset           (reset),
   .read_en         (data_array_ren),
   .read_addr       (cachereq_msg_addr_out[6:4]),
   .read_data       (mem_data),
   .write_en        (data_array_wen),
   .write_byte_en   (data_array_wben),
   .write_data      (write_data_out),
   .write_addr      (cachereq_msg_addr_out[6:4])
);

   // Comparator_1
 
   vc_EqComparator
   #( 28 ) Cmp_1
   (
   .in0            (way0_mem_tag),
   .in1            (cachereq_msg_addr_out[31:4]),
   .out            (tag_match0)
 );
   
   // Comparator_2
 
   vc_EqComparator
   #( 28 ) Cmp_2
   (
   .in0            (way1_mem_tag),
   .in1            (cachereq_msg_addr_out[31:4]),
   .out            (tag_match1),
 );
 
   // Read_Data_Way_Select Mux
   
   logic [27:0] selected_tag;
   vc_Mux2 #(mdata-1) Read_Data_Way_Select_Mux
   (
    .sel   (tag_match1),
    .in0   (way0_mem_tag),
    .in1   (way1_mem_tag),
    .out   (selected_tag)
  );
   
   //mkaddr1
 
   logic [31:0]    new_address1;
   vc_mkaddr
   #( 28, 32 ) mkaddr1
   (
   .in             (selected_tag),
   .out            (new_address1)
 );
 
   //mkaddr2
 
   logic [31:0]    new_address2;
   vc_mkaddr
   #( 28, 32) mkaddr2
   (
   .in             (cachereq_msg_addr_out[31:4]).
   .out            (new_address2)
 );
 
   //Read_Data Register
 
   logic [127:0]     whole_line_data;
   vc_EnResetReg #(128,0) Read_Data_reg
   (
     .clk     (clk),
     .reset   (reset),
     .d       (mem_data),
     .q       (whole_line_data),
     .en      (read_data_reg_en_en)
 );
   assign memreq_msg [127:0] = whole_line_data; 
 
   //Read_Word Mux
 
   logic [31:0]      read_word_out;
   vc_Mux4
   #( 32 ) Read_Word_Mux
   (
   .in0            (whole_line_data[31:0]),
   .in1            (whole_line_data[63:32]),
   .in2            (whole_line_data[95:64]),
   .in3            (whole_line_data[127:96]),
   .sel            (read_word_mux_sel),
   .out            (read_word_out)
 );
   
   assign cacheresp_msg [31:0] = read_word_out;

   // Evict_Addr Register
 
   logic [31:0]    evicted_addr; 
   vc_EnResetReg #(32,0) Evict_Addr_reg
   (
      .clk    (clk),
      .reset  (reset),
      .d      (new_address1),
      .q      (evicted_addr),
      .en     (evict_addr_reg_en)
   );
   
   //Memreq_addr Mux
  
   logic [31:0]    memreq_addr;
   vc_Mux2
   #( 32 ) Memreq_addr_Mux
   (
    .sel   (memreq_addr_mux_sel),
    .in0   (evicted_addr),
    .in1   (new_address2),
    .out   (memreq_addr)
   );
  
   assign cacheresp_msg [35:34] = hit;
   assign cacheresp_msg [33:32] = 2'b00;
   assign cacheresp_msg [46:44] = cacheresp_type;
   
   assign memreq_msg  [163:132] = memreq_addr;
   assign memreq_msg  [131:128] = 4'b0000;
   assign memreq_msg  [171:164] = 8'b00000000;
   assign memreq_msg  [174:172] = memreq_type;
endmodule

`endif

module vc_repl
#(
  parameter p_in_nbits  = 32,
  parameter p_out_nbits = 128
)(
  input  logic [p_in_nbits-1:0]  in,
  output logic [p_out_nbits-1:0] out
);

  assign out = {4{in[31:0]}};

endmodule

module vc_mkaddr
#(
   parameter p_in_nbits  = 28,
   parameter p_out_nbits = 32
)(
  input  logic [p_in_nbits-1:0]  in,
  output logic [p_out_nbits-1:0] out
);

  assign out = {in,{4'b0000}};

endmodule
                                                                                                                                                                                                                                                                                                                                                                                                                  
