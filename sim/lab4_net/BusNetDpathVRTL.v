`ifndef LAB4_NET_BUS_NET_DPATH_V
`define LAB4_NET_BUS_NET_DPATH_V

`include "vc/net-msgs.v"
`include "vc/queues.v"
`include "vc/buses.v"

module lab4_net_BusNetDpathVRTL
#(
  parameter p_payload_nbits = 32
)
(
  input  logic                                         clk,
  input  logic                                         reset,

  input  logic     [c_nports-1:0]                      in_val,
  output logic     [c_nports-1:0]                      in_rdy,
  input  net_hdr_t [c_nports-1:0]                      in_msg_hdr,
  input  logic     [c_nports-1:0][p_payload_nbits-1:0] in_msg_payload,

  output net_hdr_t [c_nports-1:0]                      out_msg_hdr,
  output logic     [c_nports-1:0][p_payload_nbits-1:0] out_msg_payload, 
  
  // control signals (ctrl->dpath)
  input  logic     [1:0]                               bus_sel,
  input  logic     [c_nports-1:0]                      inq_rdy,

  // status signals  (dpath->ctrl)
  output logic     [1:0]                               inq_dest0,
  output logic     [1:0]                               inq_dest1,
  output logic     [1:0]                               inq_dest2,
  output logic     [1:0]                               inq_dest3,
  output logic     [c_nports-1:0]                      inq_val

);

  // c_nports included for convenience to avoid having magic numbers, but 
  // your design does not need to support other values of c_nports.
  localparam c_nports = 4;
  
  logic     [c_nports-1:0][11+p_payload_nbits:0]  in_total_msg;
  logic     [c_nports-1:0][11+p_payload_nbits:0]  deq_total_msg;
  logic     [c_nports-1:0][11+p_payload_nbits:0]  out_total_msg;
  
  assign in_total_msg[0]        = {in_msg_hdr[0].dest,in_msg_hdr[0].src,in_msg_hdr[0].opaque,in_msg_payload[0]};
  assign in_total_msg[1]        = {in_msg_hdr[1].dest,in_msg_hdr[1].src,in_msg_hdr[1].opaque,in_msg_payload[1]};
  assign in_total_msg[2]        = {in_msg_hdr[2].dest,in_msg_hdr[2].src,in_msg_hdr[2].opaque,in_msg_payload[2]};
  assign in_total_msg[3]        = {in_msg_hdr[3].dest,in_msg_hdr[3].src,in_msg_hdr[3].opaque,in_msg_payload[3]};
   
  assign out_msg_hdr[0].dest    = out_total_msg[0][11+p_payload_nbits:10+p_payload_nbits];
  assign out_msg_hdr[0].src     = out_total_msg[0][9+p_payload_nbits:8+p_payload_nbits];
  assign out_msg_hdr[0].opaque  = out_total_msg[0][7+p_payload_nbits:p_payload_nbits];
  assign out_msg_payload[0]     = out_total_msg[0][p_payload_nbits-1:0 ];

  assign out_msg_hdr[1].dest    = out_total_msg[1][11+p_payload_nbits:10+p_payload_nbits];
  assign out_msg_hdr[1].src     = out_total_msg[1][9+p_payload_nbits:8+p_payload_nbits];
  assign out_msg_hdr[1].opaque  = out_total_msg[1][7+p_payload_nbits:p_payload_nbits];
  assign out_msg_payload[1]     = out_total_msg[1][p_payload_nbits-1:0 ];

  assign out_msg_hdr[2].dest    = out_total_msg[2][11+p_payload_nbits:10+p_payload_nbits];
  assign out_msg_hdr[2].src     = out_total_msg[2][9+p_payload_nbits:8+p_payload_nbits];
  assign out_msg_hdr[2].opaque  = out_total_msg[2][7+p_payload_nbits:p_payload_nbits];
  assign out_msg_payload[2]     = out_total_msg[2][p_payload_nbits-1:0 ];

  assign out_msg_hdr[3].dest    = out_total_msg[1][11+p_payload_nbits:10+p_payload_nbits];
  assign out_msg_hdr[3].src     = out_total_msg[1][9+p_payload_nbits:8+p_payload_nbits];
  assign out_msg_hdr[3].opaque  = out_total_msg[1][7+p_payload_nbits:p_payload_nbits];
  assign out_msg_payload[3]     = out_total_msg[1][p_payload_nbits-1:0 ];
  
  
  assign  inq_dest0 = deq_total_msg[0][11+p_payload_nbits:10+p_payload_nbits];
  assign  inq_dest1 = deq_total_msg[1][11+p_payload_nbits:10+p_payload_nbits];
  assign  inq_dest2 = deq_total_msg[2][11+p_payload_nbits:10+p_payload_nbits];
  assign  inq_dest3 = deq_total_msg[3][11+p_payload_nbits:10+p_payload_nbits];
 
  // input terminal 0
  vc_Queue #(`VC_QUEUE_NORMAL, 12+p_payload_nbits, 2, 1) Q0
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (in_val[0]),
   .enq_rdy                  (in_rdy[0]),
   .enq_msg                  (in_total_msg[0]),
   .deq_val                  (inq_val[0]),
   .deq_rdy                  (inq_rdy[0]),
   .deq_msg                  (deq_total_msg[0]),
   .num_free_entries         ()
  );
  
  // input terminal 1
  vc_Queue #(`VC_QUEUE_NORMAL, 12+p_payload_nbits, 2, 1) Q1
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (in_val[1]),
   .enq_rdy                  (in_rdy[1]),
   .enq_msg                  (in_total_msg[1]),
   .deq_val                  (inq_val[1]),
   .deq_rdy                  (inq_rdy[1]),
   .deq_msg                  (deq_total_msg[1]),
   .num_free_entries         ()
  );
  
  // input terminal 2
  vc_Queue #(`VC_QUEUE_NORMAL, 12+p_payload_nbits, 2, 1) Q2
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (in_val[2]),
   .enq_rdy                  (in_rdy[2]),
   .enq_msg                  (in_total_msg[2]),
   .deq_val                  (inq_val[2]),
   .deq_rdy                  (inq_rdy[2]),
   .deq_msg                  (deq_total_msg[2]),
   .num_free_entries         ()
  );
  
  // input terminal 3
  vc_Queue #(`VC_QUEUE_NORMAL, 12+p_payload_nbits, 2, 1) Q3
  (
   .clk                      (clk),
   .reset                    (reset),
   .enq_val                  (in_val[3]),
   .enq_rdy                  (in_rdy[3]),
   .enq_msg                  (in_total_msg[3]),
   .deq_val                  (inq_val[3]),
   .deq_rdy                  (inq_rdy[3]),
   .deq_msg                  (deq_total_msg[3]),
   .num_free_entries         ()
  );
  
  // bus 
  vc_Bus #(12+p_payload_nbits,4) Bus
  (
   .sel                      (bus_sel),
   .in_                      (deq_total_msg),
   .out                      (out_total_msg)
  );


endmodule

`endif /* LAB4_NET_BUS_NET_DPATH_V */
