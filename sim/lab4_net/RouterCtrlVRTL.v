//=========================================================================
// Router Control Unit
//=========================================================================

`ifndef LAB4_NET_ROUTER_CTRL_V
`define LAB4_NET_ROUTER_CTRL_V

`include "vc/net-msgs.v"
`include "vc/arbiters.v"


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
   
  input  logic [2:0]     inq_val,
  output logic [2:0]     inq_rdy,
  
  input  logic [1:0]     inq_dest0,
  input  logic [1:0]     inq_dest1,
  input  logic [1:0]     inq_dest2, 
  
  output logic [1:0]     sel0,
  output logic [1:0]     sel1,
  output logic [1:0]     sel2
  
  
  
  

  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Define additional ports
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
);
  

  logic [2:0]        arbiter_en;
  logic [2:0][2:0]   grants;
  logic [2:0]        inq_val0;
  logic [2:0]        inq_val1;
  logic [2:0]        inq_val2;
  logic [1:0]        dest0;
  logic [1:0]        dest1;
  logic [1:0]        dest2;
  logic              isodd;
  
  assign isodd = router_id[0];
  
  always @(*) begin
    if (inq_dest0 == router_id)
      dest0 = 2'd1;
    else if ((inq_dest0 == router_id + 2'd2)||(inq_dest0 == router_id - 2'd2))
      begin 
      if (isodd) dest0 = 2'd2;  
      else dest0 = 2'd0;
      end
    else if (inq_dest0 == router_id + 2'd1) 
      dest0 = 2'd2;
    else if (inq_dest0 == router_id - 2'd1) 
      dest0 = 2'd0;
    else if (inq_dest1 == router_id + 2'd3) 
      dest0 = 2'd0;
    else if (inq_dest1 == router_id - 2'd3) 
      dest0 = 2'd2;
    else 
      dest0 = 2'dx;
  end
  
  always @(*) begin
    if (inq_dest1 == router_id)
      dest1 = 2'd1;
    else if ((inq_dest1 == router_id + 2'd2)||(inq_dest1 == router_id - 2'd2))
      begin 
      if (isodd) dest1 = 2'd2;  
      else dest1 = 2'd0;
      end
    else if (inq_dest1 == router_id + 2'd1) 
      dest1 = 2'd2;
    else if (inq_dest1 == router_id - 2'd1) 
      dest1 = 2'd0;
    else if (inq_dest1 == router_id + 2'd3) 
      dest1 = 2'd0;
    else if (inq_dest1 == router_id - 2'd3) 
      dest1 = 2'd2;
    else 
      dest1 = 2'dx;
  end
  
   always @(*) begin
    if (inq_dest2 == router_id)
      dest2 = 2'd1;
    else if ((inq_dest2 == router_id + 2'd2)||(inq_dest2 == router_id - 2'd2))
      begin 
      if (isodd) dest2 = 2'd2;  
      else dest2 = 2'd0;
      end
    else if (inq_dest2 == router_id + 2'd1) 
      dest2 = 2'd2;
    else if (inq_dest2 == router_id - 2'd1) 
      dest2 = 2'd0;
    else if (inq_dest1 == router_id + 2'd3) 
      dest2 = 2'd0;
    else if (inq_dest1 == router_id - 2'd3) 
      dest2 = 2'd2;
    else 
      dest2 = 2'dx;
  end
  
     
  
  assign inq_val0[0] = inq_val[0] && (dest0 == 2'd0);
  assign inq_val0[1] = inq_val[1] && (dest1 == 2'd0);
  assign inq_val0[2] = inq_val[2] && (dest2 == 2'd0);
  
  assign inq_val1[0] = inq_val[0] && (dest0 == 2'd1);
  assign inq_val1[1] = inq_val[1] && (dest1 == 2'd1);
  assign inq_val1[2] = inq_val[2] && (dest2 == 2'd1);
  
  assign inq_val2[0] = inq_val[0] && (dest0 == 2'd2);
  assign inq_val2[1] = inq_val[1] && (dest1 == 2'd2);
  assign inq_val2[2] = inq_val[2] && (dest2 == 2'd3);
  
 
    vc_RoundRobinArbEn #(3) Arbiter0
  (
   .clk        (clk),
   .reset      (reset),
   .en         (arbiter_en[0]),
   .reqs       (inq_val0),
   .grants     (grants[0])
  );
  
    vc_RoundRobinArbEn #(3) Arbiter1
  (
   .clk        (clk),
   .reset      (reset),
   .en         (arbiter_en[1]),
   .reqs       (inq_val1),
   .grants     (grants[1])
  );
  
    vc_RoundRobinArbEn #(3) Arbiter2
  (
   .clk        (clk),
   .reset      (reset),
   .en         (arbiter_en[2]),
   .reqs       (inq_val2),
   .grants     (grants[2])
  );
  
  
  always @(*) begin
    case(grants[0])
      3'b100: sel0 = 2'd2;
      3'b010: sel0 = 2'd1;
      3'b001: sel0 = 2'd0;
     default: sel0 = 2'dx;
    endcase
  end
  
  always @(*) begin
    case(grants[1])
      3'b100: sel1 = 2'd2;
      3'b010: sel1 = 2'd1;
      3'b001: sel1 = 2'd0;
     default: sel1 = 2'dx;
    endcase
  end
  
  always @(*) begin
    case(grants[2])
      3'b100: sel2 = 2'd2;
      3'b010: sel2 = 2'd1;
      3'b001: sel2 = 2'd0;
     default: sel2 = 2'dx;
    endcase
  end
  
  assign out0_val = |inq_val0;
  assign out1_val = |inq_val1;
  assign out2_val = |inq_val2;
 
  assign arbiter_en[0] = out0_rdy? 1 : 0; 
  assign arbiter_en[1] = out1_rdy? 1 : 0;
  assign arbiter_en[2] = out2_rdy? 1 : 0;
   
  assign inq_rdy[0] = grants[dest0][0] && arbiter_en[dest0];
  assign inq_rdy[1] = grants[dest1][1] && arbiter_en[dest1];
  assign inq_rdy[2] = grants[dest2][2] && arbiter_en[dest2];
    
  
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement control unit
  //'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

endmodule

`endif /* LAB4_NET_ROUTER_CTRL_V */
