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
  
  logic [3:0][11:0]   in0_msg_hdr;
  logic [3:0][31:0]   in0_msg_payload;
  
  logic [3:0][11:0]   out0_msg_hdr;
  logic [3:0][31:0]   out0_msg_payload;
  
  logic [3:0][11:0]   in1_msg_hdr;
  logic [3:0][31:0]   in1_msg_payload;
  
  logic [3:0][11:0]   out1_msg_hdr;
  logic [3:0][31:0]   out1_msg_payload;
  
  logic [3:0][11:0]   in2_msg_hdr;
  logic [3:0][31:0]   in2_msg_payload;
  
  logic [3:0][11:0]   out2_msg_hdr;
  logic [3:0][31:0]   out2_msg_payload;
      
  logic [43:0]        deqE0_total_msg;
  logic [43:0]        deqE1_total_msg;
  logic [43:0]        deqE2_total_msg;
  logic [43:0]        deqE3_total_msg;  
  
  logic [43:0]        deqW0_total_msg;
  logic [43:0]        deqW1_total_msg;
  logic [43:0]        deqW2_total_msg;
  logic [43:0]        deqW3_total_msg;
  
  assign in1_msg_hdr[0] = in_msg_hdr[0];
  assign in1_msg_hdr[1] = in_msg_hdr[1];
  assign in1_msg_hdr[2] = in_msg_hdr[2];
  assign in1_msg_hdr[3] = in_msg_hdr[3];
  
  assign in1_msg_payload[0] = in_msg_payload[0];
  assign in1_msg_payload[1] = in_msg_payload[1];
  assign in1_msg_payload[2] = in_msg_payload[2];
  assign in1_msg_payload[3] = in_msg_payload[3];
  
  assign out_msg_hdr[0] = out1_msg_hdr[0];
  assign out_msg_hdr[1] = out1_msg_hdr[1];
  assign out_msg_hdr[2] = out1_msg_hdr[2];
  assign out_msg_hdr[3] = out1_msg_hdr[3];
  
  assign out_msg_payload[0] = out1_msg_payload[0];
  assign out_msg_payload[1] = out1_msg_payload[1];
  assign out_msg_payload[2] = out1_msg_payload[2];
  assign out_msg_payload[3] = out1_msg_payload[3];
  
    
  lab4_net_RouterVRTL #(32) Router0
  (
   .clk               (clk),
   .reset             (reset),
   
   .router_id         (0),
   .in0_msg_hdr       (in0_msg_hdr[0]),
   .in0_msg_payload   (in0_msg_payload[0]),
   .in0_val           (in0_val[0]),
   .in0_rdy           (in0_rdy[0]),
   
   .out0_msg_hdr      (out0_msg_hdr[0]),
   .out0_msg_payload  (out0_msg_payload[0]),
   .out0_val          (out0_val[0]),
   .out0_rdy          (out0_rdy[0]),
   
   .in1_msg_hdr       (in1_msg_hdr[0]),
   .in1_msg_payload   (in1_msg_payload[0]),
   .in1_val           (in_val[0]),
   .in1_rdy           (in_rdy[0]),
   
   .out1_msg_hdr      (out1_msg_hdr[0]),
   .out1_msg_payload  (out1_msg_payload[0]),
   .out1_val          (out_val[0]),
   .out1_rdy          (out_rdy[0]),
   
   .in2_msg_hdr       (in2_msg_hdr[0]),
   .in2_msg_payload   (in2_msg_payload[0]),
   .in2_val           (in2_val[0]),
   .in2_rdy           (in2_rdy[0]),
   
   .out2_msg_hdr      (out2_msg_hdr[0]),
   .out2_msg_payload  (out2_msg_payload[0]),
   .out2_val          (out2_val[0]),
   .out2_rdy          (out2_rdy[0])
  );
  
    
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) EQ0
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out2_val[0]),
   .enq_rdy                  (out2_rdy[0]),
   .enq_msg                  ({out2_msg_hdr[0],out2_msg_payload[0]}),
   .deq_val                  (in0_val[1]),
   .deq_rdy                  (in0_rdy[1]),
   .deq_msg                  (deqE0_total_msg),
   .num_free_entries         ()
  );
  
  assign in0_msg_hdr[1]     = deqE0_total_msg[43:32];
  assign in0_msg_payload[1] = deqE0_total_msg[31:0];
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) WQ0
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out0_val[1]),
   .enq_rdy                  (out0_rdy[1]),
   .enq_msg                  ({out0_msg_hdr[1],out0_msg_payload[1]}),
   .deq_val                  (in2_val[0]),
   .deq_rdy                  (in2_rdy[0]),
   .deq_msg                  (deqW0_total_msg),
   .num_free_entries         ()
  );
  
  assign in2_msg_hdr[0]     = deqW0_total_msg[43:32];
  assign in2_msg_payload[0] = deqW0_total_msg[31:0];
   
  lab4_net_RouterVRTL #(32) Router1
  (
   .clk               (clk),
   .reset             (reset),
   
   .router_id         (1),
   .in0_msg_hdr       (in0_msg_hdr[1]),
   .in0_msg_payload   (in0_msg_payload[1]),
   .in0_val           (in0_val[1]),
   .in0_rdy           (in0_rdy[1]),
   
   .out0_msg_hdr      (out0_msg_hdr[1]),
   .out0_msg_payload  (out0_msg_payload[1]),
   .out0_val          (out0_val[1]),
   .out0_rdy          (out0_rdy[1]),
   
   .in1_msg_hdr       (in1_msg_hdr[1]),
   .in1_msg_payload   (in1_msg_payload[1]),
   .in1_val           (in_val[1]),
   .in1_rdy           (in_rdy[1]),
   
   .out1_msg_hdr      (out1_msg_hdr[1]),
   .out1_msg_payload  (out1_msg_payload[1]),
   .out1_val          (out_val[1]),
   .out1_rdy          (out_rdy[1]),
   
   .in2_msg_hdr       (in2_msg_hdr[1]),
   .in2_msg_payload   (in2_msg_payload[1]),
   .in2_val           (in2_val[1]),
   .in2_rdy           (in2_rdy[1]),
   
   .out2_msg_hdr      (out2_msg_hdr[1]),
   .out2_msg_payload  (out2_msg_payload[1]),
   .out2_val          (out2_val[1]),
   .out2_rdy          (out2_rdy[1])
  );
  
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) EQ1
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out2_val[1]),
   .enq_rdy                  (out2_rdy[1]),
   .enq_msg                  ({out2_msg_hdr[1],out2_msg_payload[1]}),
   .deq_val                  (in0_val[2]),
   .deq_rdy                  (in0_rdy[2]),
   .deq_msg                  (deqE1_total_msg),
   .num_free_entries         ()
  );
  
  assign in0_msg_hdr[2]     = deqE1_total_msg[43:32];
  assign in0_msg_payload[2] = deqE1_total_msg[31:0];
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) WQ1
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out0_val[2]),
   .enq_rdy                  (out0_rdy[2]),
   .enq_msg                  ({out0_msg_hdr[2],out0_msg_payload[2]}),
   .deq_val                  (in2_val[1]),
   .deq_rdy                  (in2_rdy[1]),
   .deq_msg                  (deqW1_total_msg),
   .num_free_entries         ()
  );
  
  assign in2_msg_hdr[1]     = deqW1_total_msg[43:32];
  assign in2_msg_payload[1] = deqW1_total_msg[31:0];
   
  lab4_net_RouterVRTL #(32) Router2
  (
   .clk               (clk),
   .reset             (reset),
   
   .router_id         (2),
   .in0_msg_hdr       (in0_msg_hdr[2]),
   .in0_msg_payload   (in0_msg_payload[2]),
   .in0_val           (in0_val[2]),
   .in0_rdy           (in0_rdy[2]),
   
   .out0_msg_hdr      (out0_msg_hdr[2]),
   .out0_msg_payload  (out0_msg_payload[2]),
   .out0_val          (out0_val[2]),
   .out0_rdy          (out0_rdy[2]),
   
   .in1_msg_hdr       (in1_msg_hdr[2]),
   .in1_msg_payload   (in1_msg_payload[2]),
   .in1_val           (in_val[2]),
   .in1_rdy           (in_rdy[2]),
   
   .out1_msg_hdr      (out1_msg_hdr[2]),
   .out1_msg_payload  (out1_msg_payload[2]),
   .out1_val          (out_val[2]),
   .out1_rdy          (out_rdy[2]),
   
   .in2_msg_hdr       (in2_msg_hdr[2]),
   .in2_msg_payload   (in2_msg_payload[2]),
   .in2_val           (in2_val[2]),
   .in2_rdy           (in2_rdy[2]),
   
   .out2_msg_hdr      (out2_msg_hdr[2]),
   .out2_msg_payload  (out2_msg_payload[2]),
   .out2_val          (out2_val[2]),
   .out2_rdy          (out2_rdy[2])
  );
  
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) EQ2
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out2_val[2]),
   .enq_rdy                  (out2_rdy[2]),
   .enq_msg                  ({out2_msg_hdr[2],out2_msg_payload[2]}),
   .deq_val                  (in0_val[3]),
   .deq_rdy                  (in0_rdy[3]),
   .deq_msg                  (deqE2_total_msg),
   .num_free_entries         ()
  );
  
  assign in0_msg_hdr[3]     = deqE2_total_msg[43:32];
  assign in0_msg_payload[3] = deqE2_total_msg[31:0];
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) WQ2
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out0_val[3]),
   .enq_rdy                  (out0_rdy[3]),
   .enq_msg                  ({out0_msg_hdr[3],out0_msg_payload[3]}),
   .deq_val                  (in2_val[2]),
   .deq_rdy                  (in2_rdy[2]),
   .deq_msg                  (deqW2_total_msg),
   .num_free_entries         ()
  );
  
  assign in2_msg_hdr[2]     = deqW2_total_msg[43:32];
  assign in2_msg_payload[2] = deqW2_total_msg[31:0];  
   
  lab4_net_RouterVRTL #(32) Router3
  (
   .clk               (clk),
   .reset             (reset),
   
   .router_id         (3),
   .in0_msg_hdr       (in0_msg_hdr[3]),
   .in0_msg_payload   (in0_msg_payload[3]),
   .in0_val           (in0_val[3]),
   .in0_rdy           (in0_rdy[3]),
   
   .out0_msg_hdr      (out0_msg_hdr[3]),
   .out0_msg_payload  (out0_msg_payload[3]),
   .out0_val          (out0_val[3]),
   .out0_rdy          (out0_rdy[3]),
   
   .in1_msg_hdr       (in1_msg_hdr[3]),
   .in1_msg_payload   (in1_msg_payload[3]),
   .in1_val           (in_val[3]),
   .in1_rdy           (in_rdy[3]),
   
   .out1_msg_hdr      (out1_msg_hdr[3]),
   .out1_msg_payload  (out1_msg_payload[3]),
   .out1_val          (out_val[3]),
   .out1_rdy          (out_rdy[3]),
   
   .in2_msg_hdr       (in2_msg_hdr[3]),
   .in2_msg_payload   (in2_msg_payload[3]),
   .in2_val           (in2_val[3]),
   .in2_rdy           (in2_rdy[3]),
   
   .out2_msg_hdr      (out2_msg_hdr[3]),
   .out2_msg_payload  (out2_msg_payload[3]),
   .out2_val          (out2_val[3]),
   .out2_rdy          (out2_rdy[3])
  );
  
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) EQ3
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out2_val[3]),
   .enq_rdy                  (out2_rdy[3]),
   .enq_msg                  ({out2_msg_hdr[3],out2_msg_payload[3]}),
   .deq_val                  (in0_val[0]),
   .deq_rdy                  (in0_rdy[0]),
   .deq_msg                  (deqE3_total_msg),
   .num_free_entries         ()
  );
  
  assign in0_msg_hdr[0]     = deqE3_total_msg[43:32];
  assign in0_msg_payload[0] = deqE3_total_msg[31:0];
  
      vc_Queue #(`VC_QUEUE_NORMAL, 44, 2, 1) WQ3
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (out0_val[0]),
   .enq_rdy                  (out0_rdy[0]),
   .enq_msg                  ({out0_msg_hdr[0],out0_msg_payload[0]}),
   .deq_val                  (in2_val[3]),
   .deq_rdy                  (in2_rdy[3]),
   .deq_msg                  (deqW3_total_msg),
   .num_free_entries         ()
  );
  
  assign in2_msg_hdr[3]     = deqW3_total_msg[43:32];
  assign in2_msg_payload[3] = deqW3_total_msg[31:0]; 
  
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

  logic [3:0][6*8-1:0] in_str;
  logic [3:0][6*8-1:0] out_str;

  `VC_TRACE_BEGIN
  begin
    $sformat( in_str[0],  "%x:%x>%x",  in_msg_hdr[0].opaque,  in_msg_hdr[0].src,  in_msg_hdr[0].dest );
    $sformat( out_str[0], "%x:%x>%x", out_msg_hdr[0].opaque, out_msg_hdr[0].src, out_msg_hdr[0].dest );
    $sformat( in_str[1],  "%x:%x>%x",  in_msg_hdr[1].opaque,  in_msg_hdr[1].src,  in_msg_hdr[1].dest );
    $sformat( out_str[1], "%x:%x>%x", out_msg_hdr[1].opaque, out_msg_hdr[1].src, out_msg_hdr[1].dest );
    $sformat( in_str[2],  "%x:%x>%x",  in_msg_hdr[2].opaque,  in_msg_hdr[2].src,  in_msg_hdr[2].dest );
    $sformat( out_str[2], "%x:%x>%x", out_msg_hdr[2].opaque, out_msg_hdr[2].src, out_msg_hdr[2].dest );
    $sformat( in_str[3],  "%x:%x>%x",  in_msg_hdr[3].opaque,  in_msg_hdr[3].src,  in_msg_hdr[3].dest );
    $sformat( out_str[3], "%x:%x>%x", out_msg_hdr[3].opaque, out_msg_hdr[3].src, out_msg_hdr[3].dest );
    vc_trace.append_str( trace_str, "(" );
    vc_trace.append_val_rdy_str( trace_str, in_val[0], in_rdy[0], {{4048{1'b0}}, in_str[0]} );
    vc_trace.append_str( trace_str, "|" );
    vc_trace.append_val_rdy_str( trace_str, in_val[1], in_rdy[1], {{4048{1'b0}}, in_str[1]} );
    vc_trace.append_str( trace_str, "|" );
    vc_trace.append_val_rdy_str( trace_str, in_val[2], in_rdy[2], {{4048{1'b0}}, in_str[2]} );
    vc_trace.append_str( trace_str, "|" );
    vc_trace.append_val_rdy_str( trace_str, in_val[3], in_rdy[3], {{4048{1'b0}}, in_str[3]} );
    vc_trace.append_str( trace_str, ")" );
  end
  `VC_TRACE_END

endmodule

`endif /* LAB4_NET_RING_NET_V */
