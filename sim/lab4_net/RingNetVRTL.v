//=========================================================================
// Ring-based network
//=========================================================================

`ifndef LAB4_NET_RING_NET_V
`define LAB4_NET_RING_NET_V

`include "vc/net-msgs.v"
`include "lab4_net/RouterVRTL.v"
`include "vc/queues.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

// Helper macros to calculate previous and next router ids

`define PREV(i_) ( ( i_ + c_num_ports - 1 ) % c_num_ports )
`define NEXT(i_) i_

module lab4_net_RingNetVRTL
#(
  parameter p_payload_nbits = 32
)
(
  input logic clk,
  input logic reset,

  input  net_hdr_t [c_nports-1:0]                      in_msg_hdr,
  input  logic     [c_nports-1:0][p_payload_nbits-1:0] in_msg_payload,
  input  logic     [c_nports-1:0]                      in_val,
  output logic     [c_nports-1:0]                      in_rdy,

  output net_hdr_t [c_nports-1:0]                      out_msg_hdr,
  output logic     [c_nports-1:0][p_payload_nbits-1:0] out_msg_payload,
  output logic     [c_nports-1:0]                      out_val,
  input  logic     [c_nports-1:0]                      out_rdy
);
  // c_nports included for convenience to avoid having magic numbers, but 
  // your design does not need to support other values of c_nports.
  localparam c_nports = 4;
    
  logic [3:0]             in0_val;
  logic [3:0]             in0_rdy;
  
  logic [3:0]             in1_val;
  logic [3:0]             in1_rdy;
  
  logic [3:0]             in2_val;
  logic [3:0]             in2_rdy;
  
  logic [3:0]             out0_val;
  logic [3:0]             out0_rdy;
    
  logic [3:0]             out1_val;
  logic [3:0]             out1_rdy;
  
  logic [3:0]             out2_val;
  logic [3:0]             out2_rdy;
  
  logic [3:0][11:0]   out0_msg_hdr;
  logic [3:0][31:0]   out0_msg_payload;
  
  logic [3:0][11:0]   out2_msg_hdr;
  logic [3:0][31:0]   out2_msg_payload;
  
  
  
  logic [43:0]        inqE0_total_msg;
  logic [43:0]        inqE1_total_msg;
  logic [43:0]        inqE2_total_msg;
  logic [43:0]        inqE3_total_msg;  
  
  logic [43:0]        inqW0_total_msg;
  logic [43:0]        inqW1_total_msg;
  logic [43:0]        inqW2_total_msg;
  logic [43:0]        inqW3_total_msg;
  
  logic [43:0]        deqE0_total_msg;
  logic [43:0]        deqE1_total_msg;
  logic [43:0]        deqE2_total_msg;
  logic [43:0]        deqE3_total_msg;  
  
  logic [43:0]        deqW0_total_msg;
  logic [43:0]        deqW1_total_msg;
  logic [43:0]        deqW2_total_msg;
  logic [43:0]        deqW3_total_msg;
  
  
  lab4_net_RouterVRTL #(32) ROUTER0
  (
   .clk               (clk),
   .reset             (reset),
   
   .router_id         (0),
   .in0_msg_hdr       (deqE3_total_msg[43:32]),
   .in0_msg_payload   (deqE3_total_msg[31:0]),
   .in0_val           (in0_val[0]),
   .in0_rdy           (in0_rdy[0]),
   
   .out0_msg_hdr      (out0_msg_hdr[0]),
   .out0_msg_payload  (out0_msg_payload[0]),
   .out0_val          (out0_val[0]),
   .out0_rdy          (out0_rdy[0]),
   
   .in1_msg_hdr       (in_msg_hdr[0]),
   .in1_msg_payload   (in_msg_payload[0]),
   .in1_val           (in_val[0]),
   .in1_rdy           (in_rdy[0]),
   
   .out1_msg_hdr      (out_msg_hdr[0]),
   .out1_msg_payload  (out_msg_payload[0]),
   .out1_val          (out_val[0]),
   .out1_rdy          (out_rdy[0]),
   
   .in2_msg_hdr       (deqW0_total_msg[43:32]),
   .in2_msg_payload   (deqW0_total_msg[31:0]),
   .in2_val           (in2_val[0]),
   .in2_rdy           (in2_rdy[0]),
   
   .out2_msg_hdr      (out2_msg_hdr[0]),
   .out2_msg_payload  (out2_msg_payload[0]),
   .out2_val          (out2_val[0]),
   .out2_rdy          (out2_rdy[0])
  );
  
  assign inqE0_total_msg = {out2_msg_hdr[0],out2_msg_payload[0]};
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) EQ0
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out2_val[0]),
   .enq_rdy                  (out2_rdy[0]),
   .enq_msg                  (inqE0_total_msg),
   .deq_val                  (in0_val[1]),
   .deq_rdy                  (in0_rdy[1]),
   .deq_msg                  (deqE0_total_msg),
   .num_free_entries         ()
  );
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) WQ0
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out0_val[1]),
   .enq_rdy                  (out0_rdy[1]),
   .enq_msg                  (inqW0_total_msg),
   .deq_val                  (in2_val[0]),
   .deq_rdy                  (in2_rdy[0]),
   .deq_msg                  (deqW0_total_msg),
   .num_free_entries         ()
  );
  
  assign inqW0_total_msg = {out0_msg_hdr[1],out0_msg_payload[1]};
   
  lab4_net_RouterVRTL #(32) ROUTER1
  (
   .clk               (clk),
   .reset             (reset),
   
   .router_id         (1),
   .in0_msg_hdr       (deqE0_total_msg[43:32]),
   .in0_msg_payload   (deqE0_total_msg[31:0]),
   .in0_val           (in0_val[1]),
   .in0_rdy           (in0_rdy[1]),
   
   .out0_msg_hdr      (out0_msg_hdr[1]),
   .out0_msg_payload  (out0_msg_payload[1]),
   .out0_val          (out0_val[1]),
   .out0_rdy          (out0_rdy[1]),
   
   .in1_msg_hdr       (in_msg_hdr[1]),
   .in1_msg_payload   (in_msg_payload[1]),
   .in1_val           (in_val[1]),
   .in1_rdy           (in_rdy[1]),
   
   .out1_msg_hdr      (out_msg_hdr[1]),
   .out1_msg_payload  (out_msg_payload[1]),
   .out1_val          (out_val[1]),
   .out1_rdy          (out_rdy[1]),
   
   .in2_msg_hdr       (deqW1_total_msg[43:32]),
   .in2_msg_payload   (deqW1_total_msg[31:0]),
   .in2_val           (in2_val[1]),
   .in2_rdy           (in2_rdy[1]),
   
   .out2_msg_hdr      (out2_msg_hdr[1]),
   .out2_msg_payload  (out2_msg_payload[1]),
   .out2_val          (out2_val[1]),
   .out2_rdy          (out2_rdy[1])
  );
  
  assign inqE1_total_msg = {out2_msg_hdr[1],out2_msg_payload[1]};
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) EQ1
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out2_val[1]),
   .enq_rdy                  (out2_rdy[1]),
   .enq_msg                  (inqE1_total_msg),
   .deq_val                  (in0_val[2]),
   .deq_rdy                  (in0_rdy[2]),
   .deq_msg                  (deqE1_total_msg),
   .num_free_entries         ()
  );
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) WQ1
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out0_val[2]),
   .enq_rdy                  (out0_rdy[2]),
   .enq_msg                  (inqW1_total_msg),
   .deq_val                  (in2_val[1]),
   .deq_rdy                  (in2_rdy[1]),
   .deq_msg                  (deqW1_total_msg),
   .num_free_entries         ()
  );
  
   assign inqW1_total_msg = {out0_msg_hdr[2],out0_msg_payload[2]};
   
  lab4_net_RouterVRTL #(32) ROUTER2
  (
   .clk               (clk),
   .reset             (reset),
   
   .router_id         (2),
   .in0_msg_hdr       (deqE1_total_msg[43:32]),
   .in0_msg_payload   (deqE1_total_msg[31:0]),
   .in0_val           (in0_val[2]),
   .in0_rdy           (in0_rdy[2]),
   
   .out0_msg_hdr      (out0_msg_hdr[2]),
   .out0_msg_payload  (out_msg_payload[2]),
   .out0_val          (out0_val[2]),
   .out0_rdy          (out0_rdy[2]),
   
   .in1_msg_hdr       (in_msg_hdr[2]),
   .in1_msg_payload   (in_msg_payload[2]),
   .in1_val           (in_val[2]),
   .in1_rdy           (in_rdy[2]),
   
   .out1_msg_hdr      (out_msg_hdr[2]),
   .out1_msg_payload  (out_msg_payload[2]),
   .out1_val          (out_val[2]),
   .out1_rdy          (out_rdy[2]),
   
   .in2_msg_hdr       (deqW2_total_msg[43:32]),
   .in2_msg_payload   (deqW2_total_msg[31:0]),
   .in2_val           (in2_val[2]),
   .in2_rdy           (in2_rdy[2]),
   
   .out2_msg_hdr      (out2_msg_hdr[2]),
   .out2_msg_payload  (out2_msg_payload[2]),
   .out2_val          (out2_val[2]),
   .out2_rdy          (out2_rdy[2])
  );
  
  assign inqE2_total_msg = {out2_msg_hdr[2],out2_msg_payload[2]};
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) EQ2
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out2_val[2]),
   .enq_rdy                  (out2_rdy[2]),
   .enq_msg                  (inqE2_total_msg),
   .deq_val                  (in0_val[3]),
   .deq_rdy                  (in0_rdy[3]),
   .deq_msg                  (deqE2_total_msg),
   .num_free_entries         ()
  );
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) WQ2
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out0_val[3]),
   .enq_rdy                  (out0_rdy[3]),
   .enq_msg                  (inqW2_total_msg),
   .deq_val                  (in2_val[2]),
   .deq_rdy                  (in2_rdy[2]),
   .deq_msg                  (deqW2_total_msg),
   .num_free_entries         ()
  );
  
  assign inqW2_total_msg = {out0_msg_hdr[3],out0_msg_payload[3]};
   
  lab4_net_RouterVRTL #(32) ROUTER3
  (
   .clk               (clk),
   .reset             (reset),
   
   .router_id         (3),
   .in0_msg_hdr       (deqE0_total_msg[43:32]),
   .in0_msg_payload   (deqE0_total_msg[31:0]),
   .in0_val           (in0_val[3]),
   .in0_rdy           (in0_rdy[3]),
   
   .out0_msg_hdr      (out0_msg_hdr[3]),
   .out0_msg_payload  (out0_msg_payload[3]),
   .out0_val          (out0_val[3]),
   .out0_rdy          (out0_rdy[3]),
   
   .in1_msg_hdr       (in_msg_hdr[3]),
   .in1_msg_payload   (in_msg_payload[3]),
   .in1_val           (in_val[3]),
   .in1_rdy           (in_rdy[3]),
   
   .out1_msg_hdr      (out_msg_hdr[3]),
   .out1_msg_payload  (out_msg_payload[3]),
   .out1_val          (out_val[3]),
   .out1_rdy          (out_rdy[3]),
   
   .in2_msg_hdr       (deqW3_total_msg[43:32]),
   .in2_msg_payload   (deqW3_total_msg[31:0]),
   .in2_val           (in2_val[3]),
   .in2_rdy           (in2_rdy[3]),
   
   .out2_msg_hdr      (out2_msg_hdr[3]),
   .out2_msg_payload  (out2_msg_payload[3]),
   .out2_val          (out2_val[3]),
   .out2_rdy          (out2_rdy[3])
  );
  
  assign inqE3_total_msg = {out2_msg_hdr[3],out2_msg_payload[3]};
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) EQ3
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out2_val[3]),
   .enq_rdy                  (out2_rdy[3]),
   .enq_msg                  (inqE3_total_msg),
   .deq_val                  (in0_val[0]),
   .deq_rdy                  (in0_rdy[0]),
   .deq_msg                  (deqE3_total_msg),
   .num_free_entries         ()
  );
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) WQ3
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out0_val[0]),
   .enq_rdy                  (out0_rdy[0]),
   .enq_msg                  (inqW3_total_msg),
   .deq_val                  (in2_val[3]),
   .deq_rdy                  (in2_rdy[3]),
   .deq_msg                  (deqW3_total_msg),
   .num_free_entries         ()
  );
  
  assign inqW3_total_msg = {out0_msg_hdr[0],out0_msg_payload[0]};
  
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Compose ring network
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  //----------------------------------------------------------------------
  // Line tracing
  //----------------------------------------------------------------------
  genvar i;
  generate
  for (i = 0; i < c_nports; i = i + 1) begin: HEADER
    vc_NetHdrTrace in_hdr_trace
    (
      .clk   (clk),
      .reset (reset),
      .val   (in_val[i]),
      .rdy   (in_rdy[i]),
      .hdr   (in_msg_hdr[i])
    );

    vc_NetHdrTrace out_hdr_trace
    (
      .clk   (clk),
      .reset (reset),
      .val   (out_val[i]),
      .rdy   (out_rdy[i]),
      .hdr   (out_msg_hdr[i])
    );
  end
  endgenerate

  logic [6*8-1:0] in0_str;
  logic [6*8-1:0] in1_str;
  logic [6*8-1:0] in2_str;

  `VC_TRACE_BEGIN
  begin
    for (integer i = 0; i < c_nports; i = i + 1) begin
      $sformat( in0_str, "%x:%x>%x", in0_msg_hdr[i].opaque, in0_msg_hdr[i].src, in0_msg_hdr[i].dest );
      $sformat( in1_str, "%x:%x>%x", in1_msg_hdr[i].opaque, in1_msg_hdr[i].src, in1_msg_hdr[i].dest );
      $sformat( in2_str, "%x:%x>%x", in2_msg_hdr[i].opaque, in2_msg_hdr[i].src, in2_msg_hdr[i].dest );
      vc_trace.append_str( trace_str, "(" );
      vc_trace.append_val_rdy_str( trace_str, in0_val[i], in0_rdy[i], {{4048{1'b0}}, in0_str} );
      vc_trace.append_str( trace_str, "|" );
      vc_trace.append_val_rdy_str( trace_str, in1_val[i], in1_rdy[i], {{4048{1'b0}}, in1_str} );
      vc_trace.append_str( trace_str, "|" );
      vc_trace.append_val_rdy_str( trace_str, in2_val[i], in2_rdy[i], {{4048{1'b0}}, in2_str} );
      vc_trace.append_str( trace_str, ")" );
    end
  end
  `VC_TRACE_END

endmodule

`endif /* LAB4_NET_RING_NET_V */
