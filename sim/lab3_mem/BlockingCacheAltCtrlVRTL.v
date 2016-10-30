//=========================================================================
// Alternative Blocking Cache Control Unit
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_ALT_CTRL_V
`define LAB3_MEM_BLOCKING_CACHE_ALT_CTRL_V

`include "vc/mem-msgs.v"
`include "vc/assert.v"

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

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Add control signals
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
  // LAB TASK: Implement Control Unit
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

endmodule

`endif
