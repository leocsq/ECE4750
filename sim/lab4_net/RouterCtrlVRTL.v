//=========================================================================
// Router Control Unit
//=========================================================================

`ifndef LAB4_NET_ROUTER_CTRL_V
`define LAB4_NET_ROUTER_CTRL_V

`include "vc/net-msgs.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab4_net_RouterCtrlVRTL
(
  input  logic       clk,
  input  logic       reset,
  
  input  logic [1:0] router_id,

  output logic       out0_val,
  input  logic       out0_rdy,

  output logic       out1_val,
  input  logic       out1_rdy,

  output logic       out2_val,
  input  logic       out2_rdy,

  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Define additional ports
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
);

  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement control unit
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

endmodule

`endif /* LAB4_NET_ROUTER_CTRL_V */
