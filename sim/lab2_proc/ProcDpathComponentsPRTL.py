#=========================================================================
# ProcDpathComponentsPRTL.py
#=========================================================================

from pymtl            import *
from TinyRV2InstPRTL  import *
from pclib.rtl        import arith

#-------------------------------------------------------------------------
# Generate intermediate (imm) based on type
#-------------------------------------------------------------------------

class ImmGenPRTL( Model ):

  # Interface

  def __init__( s ):

    s.imm_type = InPort( 3 )
    s.inst     = InPort( 32 )
    s.imm      = OutPort( 32 )

    @s.combinational
    def comb_logic():
      # Always sext!

      if   s.imm_type == 0: # I-type

        s.imm.value = concat( sext( s.inst[ I_IMM ], 32 ) )

      elif s.imm_type == 2: # B-type

        s.imm.value = concat( sext( s.inst[ B_IMM3 ], 20 ),
                                    s.inst[ B_IMM2 ],
                                    s.inst[ B_IMM1 ],
                                    s.inst[ B_IMM0 ],
                                    Bits( 1, 0 ) )

      #''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
      # Add more immediate types
      #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

      else:
        s.imm.value = 0

#-------------------------------------------------------------------------
# ALU
#-------------------------------------------------------------------------

class AluPRTL( Model ):

  # Interface

  def __init__( s ):

    s.in0      = InPort ( 32 )
    s.in1      = InPort ( 32 )
    s.fn       = InPort ( 4 )

    s.out      = OutPort( 32 )
    s.ops_eq   = OutPort( 1 )
    s.ops_lt   = OutPort( 1 )
    s.ops_ltu  = OutPort( 1 )

  # Combinational Logic

    s.tmp_a = Wire( 33 )
    s.tmp_b = Wire( 64 )

    @s.combinational
    def comb_logic():

      s.tmp_a.value = 0
      s.tmp_b.value = 0

      if   s.fn ==  0: s.out.value = s.in0 + s.in1       # ADD
      elif s.fn == 11: s.out.value = s.in0               # CP OP0
      elif s.fn == 12: s.out.value = s.in1               # CP OP1

      #''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
      # Add more ALU functions
      #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

      else:            s.out.value = 0                   # Unknown

      s.ops_eq.value = ( s.in0 == s.in1 )

      #''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''
      # Add more ALU functions
      # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
