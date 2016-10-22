//========================================================================
// net-msgs : Network Messages
//========================================================================
// Payload field width (payload_nbits), opaque filed width (opaque_nbits)
// source and destination field widths (p_srcdest_nbits) are adjustable
// via parameterized macro definitions.
//
// Example message format for payload_nbits = 32, srcdest_nbits = 3,
// opaque_nbits = 4
//
// 41   39 38  36 35    32 31                            0
// +------+------+--------+-------------------------------+
// | dest | src  | opaque | payload                       |
// +------+------+--------+-------------------------------+
//

`ifndef VC_NET_MSGS_V
`define VC_NET_MSGS_V

`include "vc/trace.v"

//-------------------------------------------------------------------------
// Message defines
//-------------------------------------------------------------------------

typedef struct packed {
  logic [1:0] dest;
  logic [1:0] src;
  logic [7:0] opaque;
} net_hdr_t;

//------------------------------------------------------------------------
// Trace message
//------------------------------------------------------------------------

module vc_NetMsgTrace
(
  input  logic     clk,
  input  logic     reset,
  input  logic     val,
  input  logic     rdy,
  input  net_hdr_t msg
);

  // Extract fields

  logic [1:0]    dest;
  logic [1:0]    src;
  logic [7:0]    opaque;

  // Line tracing

  logic [`VC_TRACE_NBITS-1:0] str;

  `VC_TRACE_BEGIN
  begin

    $sformat( str, "%x>%x:%x", src, dest, opaque );

    // Trace with val/rdy signals

    vc_trace.append_val_rdy_str( trace_str, val, rdy, str );

  end
  `VC_TRACE_END

endmodule

`endif /* VC_NET_MSGS_V */
