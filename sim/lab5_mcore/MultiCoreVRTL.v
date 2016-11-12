//========================================================================
// 1-Core Processor-Cache-Network
//========================================================================

`ifndef LAB5_MCORE_MULTI_CORE_V
`define LAB5_MCORE_MULTI_CORE_V

`include "vc/mem-msgs.v"
`include "vc/trace.v"


//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include components
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab5_mcore_MultiCoreVRTL
(
  input  logic                       clk,
  input  logic                       reset,

  input  logic [c_num_cores-1:0][31:0] mngr2proc_msg,
  input  logic [c_num_cores-1:0]       mngr2proc_val,
  output logic [c_num_cores-1:0]       mngr2proc_rdy,

  output logic [c_num_cores-1:0][31:0] proc2mngr_msg,
  output logic [c_num_cores-1:0]       proc2mngr_val,
  input  logic [c_num_cores-1:0]       proc2mngr_rdy,

  output mem_req_16B_t                 imemreq_msg,
  output logic                         imemreq_val,
  input  logic                         imemreq_rdy,

  input  mem_resp_16B_t                imemresp_msg,
  input  logic                         imemresp_val,
  output logic                         imemresp_rdy,

  output mem_req_16B_t                 dmemreq_msg,
  output logic                         dmemreq_val,
  input  logic                         dmemreq_rdy,

  input  mem_resp_16B_t                dmemresp_msg,
  input  logic                         dmemresp_val,
  output logic                         dmemresp_rdy,

  //  Only takes Core 0's stats_en to the interface
  output logic                         stats_en,
  output logic [c_num_cores-1:0]       commit_inst,
  output logic [c_num_cores-1:0]       icache_miss,
  output logic [c_num_cores-1:0]       icache_access,
  output logic [c_num_cores-1:0]       dcache_miss,
  output logic [c_num_cores-1:0]       dcache_access
);

  localparam c_num_cores = 4;

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK:
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  `VC_TRACE_BEGIN
  begin

    // This is staffs' line trace, which assume the processors and icaches
    // are instantiated in using generate statement, and the data cache
    // system is instantiated with the name dcache. You can add net to the
    // line trace.
    // Feel free to revamp it or redo it based on your need.

    CORES_CACHES[0].icache.line_trace( trace_str );
    CORES_CACHES[0].proc.line_trace( trace_str );
    CORES_CACHES[1].icache.line_trace( trace_str );
    CORES_CACHES[1].proc.line_trace( trace_str );
    CORES_CACHES[2].icache.line_trace( trace_str );
    CORES_CACHES[2].proc.line_trace( trace_str );
    CORES_CACHES[3].icache.line_trace( trace_str );
    CORES_CACHES[3].proc.line_trace( trace_str );

    dcache.line_trace( trace_str );
  end
  `VC_TRACE_END

endmodule

`endif /* LAB5_MCORE_MULTI_CORE_V */
