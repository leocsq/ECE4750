//=========================================================================
// Router datapath
//=========================================================================

`ifndef LAB4_NET_ROUTER_DPATH_V
`define LAB4_NET_ROUTER_DPATH_V

`include "vc/net-msgs.v"
`include "vc/crossbars.v"
`include "vc/queues.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab4_net_RouterDpathVRTL
#(
  parameter p_payload_nbits = 32
)
(
  input  logic                           clk,
  input  logic                           reset,

  input  net_hdr_t                       in0_msg_hdr,
  input  logic     [p_payload_nbits-1:0] in0_msg_payload,
  input  logic                           in0_val,
  output logic                           in0_rdy,

  input  net_hdr_t                       in1_msg_hdr,
  input  logic     [p_payload_nbits-1:0] in1_msg_payload,
  input  logic                           in1_val,
  output logic                           in1_rdy,

  input  net_hdr_t                       in2_msg_hdr,
  input  logic     [p_payload_nbits-1:0] in2_msg_payload,
  input  logic                           in2_val,
  output logic                           in2_rdy,

  output net_hdr_t                       out0_msg_hdr,
  output logic     [p_payload_nbits-1:0] out0_msg_payload,

  output net_hdr_t                       out1_msg_hdr,
  output logic     [p_payload_nbits-1:0] out1_msg_payload,

  output net_hdr_t                       out2_msg_hdr,
  output logic     [p_payload_nbits-1:0] out2_msg_payload,
  
  input logic [1:0]                      sel0,
  input logic [1:0]                      sel1,
  input logic [1:0]                      sel2,
  
  input  logic [2:0]                     inq_rdy,
  output logic [2:0]                     inq_val,
  
  output logic [1:0]                     inq_dest0,
  output logic [1:0]                     inq_dest1,
  output logic [1:0]                     inq_dest2

  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Define additional ports
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
);

  logic [43:0]          in0_total_msg;
  logic [43:0]          in1_total_msg;
  logic [43:0]          in2_total_msg;
  
  assign in0_total_msg = {in0_msg_hdr.dest,in0_msg_hdr.src,in0_msg_hdr.opaque,in0_msg_payload};
  assign in1_total_msg = {in1_msg_hdr.dest,in1_msg_hdr.src,in1_msg_hdr.opaque,in1_msg_payload};
  assign in2_total_msg = {in2_msg_hdr.dest,in2_msg_hdr.src,in2_msg_hdr.opaque,in2_msg_payload};
  
  
  logic [43:0]          out0_total_msg;
  logic [43:0]          out1_total_msg;
  logic [43:0]          out2_total_msg;
  
  assign out0_msg_hdr.dest = out0_total_msg[43:42];
  assign out1_msg_hdr.dest = out1_total_msg[43:42];
  assign out2_msg_hdr.dest = out2_total_msg[43:42];
  
  assign out0_msg_hdr.src = out0_total_msg[41:40];
  assign out1_msg_hdr.src = out1_total_msg[41:40];
  assign out2_msg_hdr.src = out2_total_msg[41:40];
  
  assign out0_msg_hdr.opaque = out0_total_msg[39:32];
  assign out1_msg_hdr.opaque = out1_total_msg[39:32];
  assign out2_msg_hdr.opaque = out2_total_msg[39:32];
  
  assign out0_msg_payload = out0_total_msg[31:0];
  assign out1_msg_payload = out1_total_msg[31:0];
  assign out2_msg_payload = out2_total_msg[31:0];
  
  logic  [43:0]             deq0_total_msg;
  logic  [43:0]             deq1_total_msg;
  logic  [43:0]             deq2_total_msg;
  
  assign inq_dest0 = deq0_total_msg[43:42];
  assign inq_dest1 = deq1_total_msg[43:42];
  assign inq_dest2 = deq2_total_msg[43:42];
  
  
  
  
  
  vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) Q0
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (in0_val),
   .enq_rdy                  (in0_rdy),
   .enq_msg                  (in0_total_msg),
   .deq_val                  (inq_val[0]),
   .deq_rdy                  (inq_rdy[0]),
   .deq_msg                  (deq0_total_msg),
   .num_free_entries         ()
  );
  
  vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) Q1
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (in1_val),
   .enq_rdy                  (in1_rdy),
   .enq_msg                  (in1_total_msg),
   .deq_val                  (inq_val[1]),
   .deq_rdy                  (inq_rdy[1]),
   .deq_msg                  (deq1_total_msg),
   .num_free_entries         ()
  );
  
    vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) Q2
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (in2_val),
   .enq_rdy                  (in2_rdy),
   .enq_msg                  (in2_total_msg),
   .deq_val                  (inq_val[2]),
   .deq_rdy                  (inq_rdy[2]),
   .deq_msg                  (deq2_total_msg),
   .num_free_entries         ()
  );
  
    vc_Crossbar3 #(44) Crossbar
  (
   .in0      (deq0_total_msg),
   .in1      (deq1_total_msg),
   .in2      (deq2_total_msg),
   
   .sel0     (sel0),
   .sel1     (sel1),
   .sel2     (sel2),
   
   .out0     (out0_total_msg),
   .out1     (out1_total_msg),
   .out2     (out2_total_msg)
  );
  
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement datapath
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

endmodule

`endif /* LAB4_NET_ROUTER_DPATH_V */
