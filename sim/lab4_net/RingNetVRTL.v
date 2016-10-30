//=========================================================================
// Ring-based network
//=========================================================================

`ifndef LAB4_NET_RING_NET_V
`define LAB4_NET_RING_NET_V

`include "vc/net-msgs.v"
`include "lab4_net/RouterVRTL.v"

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

  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Compose ring network
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  //----------------------------------------------------------------------
  // Line tracing
  //----------------------------------------------------------------------
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

  logic [6*8-1:0] in_str;
  logic [6*8-1:0] out_str;

  `VC_TRACE_BEGIN
  begin
    ROUTER[0].router.line_trace( trace_str );
    ROUTER[1].router.line_trace( trace_str );
    ROUTER[2].router.line_trace( trace_str );
    ROUTER[3].router.line_trace( trace_str );
  end
  `VC_TRACE_END

endmodule

`endif /* LAB4_NET_RING_NET_V */
