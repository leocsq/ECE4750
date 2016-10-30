#=========================================================================
# RouterPRTL.py
#=========================================================================

from pymtl      import *
from pclib.ifcs import NetMsg
from pclib.ifcs import InValRdyBundle, OutValRdyBundle
from pclib.rtl  import RoundRobinArbiterEn

class RouterCtrlPRTL( Model ):

  #-----------------------------------------------------------------------
  # Constructor
  #-----------------------------------------------------------------------

  def __init__( s ):

    # Parameters
    # Your design does not need to support other values

    nrouters = 4 

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    s.router_id = InPort( clog2(nrouters) )

    s.out0_val  = OutPort( 1 )
    s.out0_rdy  = InPort ( 1 )

    s.out1_val  = OutPort( 1 )
    s.out1_rdy  = InPort ( 1 )

    s.out2_val  = OutPort( 1 )
    s.out2_rdy  = InPort ( 1 )

    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK: Router control logic and other inports/outports
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
