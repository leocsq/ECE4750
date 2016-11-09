`ifndef LAB4_NET_BUS_NET_DPATH_V
`define LAB4_NET_BUS_NET_DPATH_V

`include "vc/net-msgs.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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
  
  input  logic      [c_nports-1:0]                      inq_rdy,
  input  logic      [1:0]                               sel,
  
  // status signals (dpath->ctrl)
  
  output logic      [c_nports-1:0]                      inq_val,
  output logic      [1:0]                               inq_dest0,
  output logic      [1:0]                               inq_dest1,
  output logic      [1:0]                               inq_dest2,
  output logic      [1:0]                               inq_dest3,
);
  // c_nports included for convenience to avoid having magic numbers, but 
  // your design does not need to support other values of c_nports.
  localparam c_nports = 4;

  vc_Queue #(`VC_QUEUE_NORMAL,
  parameter p_type      = `VC_QUEUE_NORMAL,
  parameter p_msg_nbits = 1,
  parameter p_num_msgs  = 2,

  // parameters not meant to be set outside this module
  parameter c_addr_nbits = $clog2(p_num_msgs)
)(
  input  logic                   clk,
  input  logic                   reset,

  input  logic                   enq_val,
  output logic                   enq_rdy,
  input  logic [p_msg_nbits-1:0] enq_msg,

  output logic                   deq_val,
  input  logic                   deq_rdy,
  output logic [p_msg_nbits-1:0] deq_msg,

  output logic [c_addr_nbits:0]  num_free_entries
);
  

endmodule

`endif /* LAB4_NET_BUS_NET_DPATH_V */
