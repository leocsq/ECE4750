//========================================================================
// Multi-Core Processor-Cache-Network
//========================================================================

`ifndef LAB5_MCORE_MULTI_CORE_V
`define LAB5_MCORE_MULTI_CORE_V

`include "vc/mem-msgs.v"
`include "vc/trace.v"
`include "lab2_proc/ProcAltVRTL.v"
`include "lab3_mem/BlockingCacheAltVRTL.v"
`include "lab5_mcore/MemNetVRTL.v"
`include "lab5_mcore/McoreDataCacheVRTL.v"


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
  
  mem_req_16B_t  [c_num_cores-1:0]     mainmemreq_refill_msg;
  logic          [c_num_cores-1:0]     mainmemreq_refill_val;
  logic          [c_num_cores-1:0]     mainmemreq_refill_rdy;

  mem_resp_16B_t [c_num_cores-1:0]     mainmemresp_refill_msg;
  logic          [c_num_cores-1:0]     mainmemresp_refill_val;
  logic          [c_num_cores-1:0]     mainmemresp_refill_rdy;
  
  mem_req_16B_t  [c_num_cores-1:0]     MemNet_req_msg;
  logic          [c_num_cores-1:0]     MemNet_req_val;
  logic          [c_num_cores-1:0]     MemNet_req_rdy;
  
  mem_resp_16B_t [c_num_cores-1:0]     MemNet_resp_msg;
  logic          [c_num_cores-1:0]     MemNet_resp_val;
  logic          [c_num_cores-1:0]     MemNet_resp_rdy;
  
  mem_req_4B_t   [c_num_cores-1:0]     ICache_req_msg;
  logic          [c_num_cores-1:0]     ICache_req_val;
  logic          [c_num_cores-1:0]     ICache_req_rdy;
  
  mem_resp_4B_t  [c_num_cores-1:0]     ICache_resp_msg;
  logic          [c_num_cores-1:0]     ICache_resp_val;
  logic          [c_num_cores-1:0]     ICache_resp_rdy;
  
  mem_req_4B_t   [c_num_cores-1:0]     DProc_req_msg;
  logic          [c_num_cores-1:0]     DProc_req_val;
  logic          [c_num_cores-1:0]     DProc_req_rdy;
  
  mem_resp_4B_t  [c_num_cores-1:0]     DProc_resp_msg;
  logic          [c_num_cores-1:0]     DProc_resp_val;
  logic          [c_num_cores-1:0]     DProc_resp_rdy;
  
  
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // MemNet
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  
  lab5_mcore_MemNetVRTL MemNet
  (
    .clk                   (clk),
    .reset                 (reset),
    
    .memreq_msg            (MemNet_req_msg),
    .memreq_val            (MemNet_req_val),
    .memreq_rdy            (MemNet_req_rdy),
    
    .memresp_msg           (MemNet_resp_msg),
    .memresp_val           (MemNet_resp_val),
    .memresp_rdy           (MemNet_resp_rdy),
    
    .mainmemreq_msg        (mainmemreq_refill_msg),
    .mainmemreq_val        (mainmemreq_refill_val),
    .mainmemreq_rdy        (mainmemreq_refill_rdy),
    
    .mainmemresp_msg       (mainmemresp_refill_msg),
    .mainmemresp_val       (mainmemresp_refill_val),
    .mainmemresp_rdy       (mainmemresp_refill_rdy)
  );
  
  assign imemreq_msg = mainmemreq_refill_msg[0];
  assign imemreq_val = mainmemreq_refill_val[0];
  assign mainmemreq_refill_rdy = { {c_num_cores-1{1'b0}}, imemreq_rdy };

  assign mainmemresp_refill_msg[0] = imemresp_msg;
  assign mainmemresp_refill_val = { {c_num_cores-1{1'b0}}, imemresp_val };
  assign imemresp_rdy = mainmemresp_refill_rdy[0];
  
  
  genvar i;
  generate
  for ( i = 0; i < c_num_cores; i = i + 1 ) begin: CORES_CACHES

    // instruction cache

    lab3_mem_BlockingCacheAltVRTL
    #(0) icache_i
    (
      .clk           (clk),
      .reset         (reset),

      .cachereq_msg  (ICache_req_msg[i]),
      .cachereq_val  (ICache_req_val[i]),
      .cachereq_rdy  (ICache_req_rdy[i]),

      .cacheresp_msg (ICache_resp_msg[i]),
      .cacheresp_val (ICache_resp_val[i]),
      .cacheresp_rdy (ICache_resp_rdy[i]),

      .memreq_msg    (MemNet_req_msg[i]),
      .memreq_val    (MemNet_req_val[i]),
      .memreq_rdy    (MemNet_req_rdy[i]),

      .memresp_msg   (MemNet_resp_msg[i]),
      .memresp_val   (MemNet_resp_val[i]),
      .memresp_rdy   (MemNet_resp_rdy[i])

    );
     assign icache_miss[i] = ICache_resp_rdy[i] & ICache_resp_val[i] & (! ICache_resp_msg[i].test[0] );
    assign icache_access[i] = ICache_req_rdy[i] & ICache_req_val[i];
    
  end
  endgenerate

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Proc 0
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  
  lab2_proc_ProcAltVRTL #(c_num_cores) proc_0
  (
    .clk           (clk),
    .reset         (reset),

    .core_id       (32'd0),

    .imemreq_msg   (ICache_req_msg[0]),
    .imemreq_val   (ICache_req_val[0]),
    .imemreq_rdy   (ICache_req_rdy[0]),

    .imemresp_msg  (ICache_resp_msg[0]),
    .imemresp_val  (ICache_resp_val[0]),
    .imemresp_rdy  (ICache_resp_rdy[0]),

    .dmemreq_msg   (DProc_req_msg[0]),
    .dmemreq_val   (DProc_req_val[0]),
    .dmemreq_rdy   (DProc_req_rdy[0]),

    .dmemresp_msg  (DProc_resp_msg[0]),
    .dmemresp_val  (DProc_resp_val[0]),
    .dmemresp_rdy  (DProc_resp_rdy[0]),

    .mngr2proc_msg (mngr2proc_msg[0]),
    .mngr2proc_val (mngr2proc_val[0]),
    .mngr2proc_rdy (mngr2proc_rdy[0]),

    .proc2mngr_msg (proc2mngr_msg[0]),
    .proc2mngr_val (proc2mngr_val[0]),
    .proc2mngr_rdy (proc2mngr_rdy[0]),

    .stats_en      (stats_en),
    .commit_inst   (commit_inst[0])
  );
  
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Proc 1
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  lab2_proc_ProcAltVRTL #(c_num_cores) proc_1
  (
    .clk           (clk),
    .reset         (reset),

    .core_id       (32'd1),

    .imemreq_msg   (ICache_req_msg[1]),
    .imemreq_val   (ICache_req_val[1]),
    .imemreq_rdy   (ICache_req_rdy[1]),

    .imemresp_msg  (ICache_resp_msg[1]),
    .imemresp_val  (ICache_resp_val[1]),
    .imemresp_rdy  (ICache_resp_rdy[1]),

    .dmemreq_msg   (DProc_req_msg[1]),
    .dmemreq_val   (DProc_req_val[1]),
    .dmemreq_rdy   (DProc_req_rdy[1]),

    .dmemresp_msg  (DProc_resp_msg[1]),
    .dmemresp_val  (DProc_resp_val[1]),
    .dmemresp_rdy  (DProc_resp_rdy[1]),

    .mngr2proc_msg (mngr2proc_msg[1]),
    .mngr2proc_val (mngr2proc_val[1]),
    .mngr2proc_rdy (mngr2proc_rdy[1]),

    .proc2mngr_msg (proc2mngr_msg[1]),
    .proc2mngr_val (proc2mngr_val[1]),
    .proc2mngr_rdy (proc2mngr_rdy[1]),

    .stats_en      (stats_en),
    .commit_inst   (commit_inst[1])
  );
  
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Proc 2
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  
  lab2_proc_ProcAltVRTL #(c_num_cores) proc_2
  (
    .clk           (clk),
    .reset         (reset),

    .core_id       (32'd2),

    .imemreq_msg   (ICache_req_msg[2]),
    .imemreq_val   (ICache_req_val[2]),
    .imemreq_rdy   (ICache_req_rdy[2]),

    .imemresp_msg  (ICache_resp_msg[2]),
    .imemresp_val  (ICache_resp_val[2]),
    .imemresp_rdy  (ICache_resp_rdy[2]),

    .dmemreq_msg   (DProc_req_msg[2]),
    .dmemreq_val   (DProc_req_val[2]),
    .dmemreq_rdy   (DProc_req_rdy[2]),

    .dmemresp_msg  (DProc_resp_msg[2]),
    .dmemresp_val  (DProc_resp_val[2]),
    .dmemresp_rdy  (DProc_resp_rdy[2]),

    .mngr2proc_msg (mngr2proc_msg[2]),
    .mngr2proc_val (mngr2proc_val[2]),
    .mngr2proc_rdy (mngr2proc_rdy[2]),

    .proc2mngr_msg (proc2mngr_msg[2]),
    .proc2mngr_val (proc2mngr_val[2]),
    .proc2mngr_rdy (proc2mngr_rdy[2]),

    .stats_en      (stats_en),
    .commit_inst   (commit_inst[2])
  );
  
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Proc 3
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  lab2_proc_ProcAltVRTL #(c_num_cores) proc_3
  (
    .clk           (clk),
    .reset         (reset),

    .core_id       (32'd3),

    .imemreq_msg   (ICache_req_msg[3]),
    .imemreq_val   (ICache_req_val[3]),
    .imemreq_rdy   (ICache_req_rdy[3]),

    .imemresp_msg  (ICache_resp_msg[3]),
    .imemresp_val  (ICache_resp_val[3]),
    .imemresp_rdy  (ICache_resp_rdy[3]),

    .dmemreq_msg   (DProc_req_msg[3]),
    .dmemreq_val   (DProc_req_val[3]),
    .dmemreq_rdy   (DProc_req_rdy[3]),

    .dmemresp_msg  (DProc_resp_msg[3]),
    .dmemresp_val  (DProc_resp_val[3]),
    .dmemresp_rdy  (DProc_resp_rdy[3]),

    .mngr2proc_msg (mngr2proc_msg[3]),
    .mngr2proc_val (mngr2proc_val[3]),
    .mngr2proc_rdy (mngr2proc_rdy[3]),

    .proc2mngr_msg (proc2mngr_msg[3]),
    .proc2mngr_val (proc2mngr_val[3]),
    .proc2mngr_rdy (proc2mngr_rdy[3]),

    .stats_en      (stats_en),
    .commit_inst   (commit_inst[3])
  );

  
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // McoreDataCache
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  lab5_mcore_McoreDataCacheVRTL McroDataCache
  (
    .clk                (clk),
    .reset              (reset),
    
    .procreq_msg        (DProc_req_msg),
    .procreq_val        (DProc_req_val),
    .procreq_rdy        (DProc_req_rdy),
    
    .procresp_msg       (DProc_resp_msg),
    .procresp_val       (DProc_resp_val),
    .procresp_rdy       (DProc_resp_rdy),
    
    .mainmemreq_msg     (dmemreq_msg),
    .mainmemreq_val     (dmemreq_val),
    .mainmemreq_rdy     (dmemreq_rdy),
    
    .mainmemresp_msg    (dmemresp_msg),
    .mainmemresp_val    (dmemresp_val),
    .mainmemresp_rdy    (dmemresp_rdy),
    
    .dcache_miss        (dcache_miss),
    .dcache_access      (dcache_access)
  );
  
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK:
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  `VC_TRACE_BEGIN
   /*begin

     /*This is staffs' line trace, which assume the processors and icaches
     are instantiated in using generate statement, and the data cache
     system is instantiated with the name dcache. You can add net to the
     line trace.
     Feel free to revamp it or redo it based on your need.

     CORES_CACHES[0].icache_0.line_trace( trace_str );
     CORES_CACHES[0].proc_0.line_trace( trace_str );
     CORES_CACHES[1].icache_1.line_trace( trace_str );
     CORES_CACHES[1].proc_1.line_trace( trace_str );
     CORES_CACHES[2].icache_2.line_trace( trace_str );
     CORES_CACHES[2].proc_2.line_trace( trace_str );
     CORES_CACHES[3].icache_3.line_trace( trace_str );
     CORES_CACHES[3].proc_3.line_trace( trace_str );
  end*/
  `VC_TRACE_END 
  

endmodule

`endif /* LAB5_MCORE_MULTI_CORE_V */
