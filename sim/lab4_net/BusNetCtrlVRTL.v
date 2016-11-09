`ifndef LAB4_NET_BUS_NET_CTRL_V
`define LAB4_NET_BUS_NET_CTRL_V

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab4_net_BusNetCtrlVRTL
(
  input  logic                                          clk,
  input  logic                                          reset,

  output logic [c_nports-1:0]                           out_val,
  input  logic [c_nports-1:0]                           out_rdy,

  // control signals (ctrl->dpath)
  
  output logic      [c_nports-1:0]                      inq_rdy,
  output logic      [1:0]                               sel,
  
  // status signals (dpath->ctrl)
  
  input  logic      [c_nports-1:0]                      inq_val,
  input  logic      [1:0]                               inq_dest0,
  input  logic      [1:0]                               inq_dest1,
  input  logic      [1:0]                               inq_dest2,
  input  logic      [1:0]                               inq_dest3,
);
  // c_nports included for convenience to avoid having magic numbers, but 
  // your design does not need to support other values of c_nports.
  localparam c_nports = 4;

  // control signals (ctrl->dpath)
    
  // status signals (dpath->ctrl)

endmodule

`endif /* LAB4_NET_BUS_NET_CTRL_V */
