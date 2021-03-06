#=========================================================================
# BusNetCtrlPRTL.py
#=========================================================================
# This model implements 4-port (configurable) simple bus network.

from pymtl     import *

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Include components
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class BusNetCtrlPRTL( Model ):

  #-----------------------------------------------------------------------
  # Constructor
  #-----------------------------------------------------------------------

  def __init__( s ):

    # Parameters
    # Your design does not need to support other values

    num_ports = 4

    # Interface

    s.out_val  = OutPort[num_ports]( 1 )
    s.out_rdy  = InPort [num_ports]( 1 )

    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # LAB TASK:
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
