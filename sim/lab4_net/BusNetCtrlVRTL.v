`ifndef LAB4_NET_BUS_NET_CTRL_V
`define LAB4_NET_BUS_NET_CTRL_V

`include "vc/arbiters.v"

module lab4_net_BusNetCtrlVRTL
(
  input  logic                                 clk,
  input  logic                                 reset,

  output logic [c_nports-1:0]                  out_val,
  input  logic [c_nports-1:0]                  out_rdy,
  // ctrl -> dpath
  output logic [1:0]                           bus_sel,
  output logic [c_nports-1:0]                  inq_rdy,
  // dpath -> ctrl
  input  logic [c_nports-1:0]                  inq_val,
  input  logic [1:0]                           inq_dest0,
  input  logic [1:0]                           inq_dest1,
  input  logic [1:0]                           inq_dest2,
  input  logic [1:0]                           inq_dest3


);
  // c_nports included for convenience to avoid having magic numbers, but 
  // your design does not need to support other values of c_nports.
  localparam c_nports = 4;
  
  logic            arbiter_en;
  logic [3:0]      grants;

  vc_RoundRobinArbEn #(4) RoundRobin_Arbiter
  (
   .clk        (clk),
   .reset      (reset),
   .en         (arbiter_en),
   .reqs       (inq_val),
   .grants     (grants)
  );

  //Cloud A
  always @(*) begin
    case(grants)
      4'b1000: bus_sel = 2'd3;
      4'b0100: bus_sel = 2'd2;
      4'b0010: bus_sel = 2'd1;
      4'b0001: bus_sel = 2'd0;
      default: bus_sel = 2'dx;
    endcase
  end


  // Cloud B
  logic [1:0]   cloud_b_out; // decide which destination to be selected
  always @(*) begin
    case(grants)
      4'b1000: begin 
               cloud_b_out = inq_dest3;
               out_val = (4'd1 << cloud_b_out);
               end
      4'b0100: begin
               cloud_b_out = inq_dest2; 
               out_val = (4'd1 << cloud_b_out);
               end
      4'b0010: begin 
               cloud_b_out = inq_dest1; 
               out_val = (4'd1 << cloud_b_out);
               end
      4'b0001: begin 
               cloud_b_out = inq_dest0; 
               out_val = (4'd1 << cloud_b_out);
               end
      default: begin 
               cloud_b_out = 2'dx; 
               out_val = 4'd0;
               end     
    endcase
    
  end


  //Cloud_C 
  always @(*) begin
    if (out_rdy[cloud_b_out]==1 ) 
      arbiter_en = 1;
    else
      arbiter_en = 0; 
  end

  //Cloud_D
  always @(*) begin
    if( arbiter_en )
     inq_rdy = grants;
    else
     inq_rdy = 4'd0;
  end

endmodule

`endif /* LAB4_NET_BUS_NET_CTRL_V */
