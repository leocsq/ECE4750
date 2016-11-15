#=========================================================================
# net_sim_eval
#=========================================================================
# Run the evaluations on the baseline and alternative design.

import os

from subprocess import check_output, CalledProcessError

impls  = [ "bus", "ring" ]
inputs = [ "urandom", "partition2", "opposite", "neighbor", "complement" ]

eval_runs = []

for impl in impls:
  for input_ in inputs:
    eval_runs.append([ impl, input_ ])

# Get path to simulator script

sim_dir = os.path.dirname( os.path.abspath( __file__ ) )
sim     = sim_dir + os.path.sep + 'net-sim-staff'

# Print header

print ""
print " Results from running simulator ( injection rate = 10 ) "
print ""
print "    {:<5} {:<10} {:>9}".format( "Impl", "Pattern", "Avg. Latency" )
print "    " + "-" * 29

# Run the simulator

for eval_run in eval_runs:

  # Command

  impl   = eval_run[0]
  input_ = eval_run[1]

  cmd = [ sim, "--impl", impl, "--pattern", input_, "--stats", "--injection-rate", "10" ]

  try:
    result = check_output( cmd ).strip()
  except CalledProcessError as e:
    raise Exception( "Error running simulator!\n\n"
                     "Simulator command line: {cmd}\n\n"
                     "Simulator output:\n {output}"
                     .format( cmd=' '.join(e.cmd), output=e.output ) )

  # Find result

  lat = None
  for line in result.splitlines():
    if line.startswith('Average Latency'):
      lat = line.split('=')[1].strip()

  # Display result

  print "  - {:<5} {:<10} {:>9}".format( impl, input_, lat )

print ""

print ""
print " Results from running simulator ( injection rate = 60 ) "
print ""
print "    {:<5} {:<10} {:>9}".format( "Impl", "Pattern", "Avg. Latency" )
print "    " + "-" * 29

# Run the simulator

for eval_run in eval_runs:

  # Command

  impl   = eval_run[0]
  input_ = eval_run[1]

  cmd = [ sim, "--impl", impl, "--pattern", input_, "--stats", "--injection-rate", "60" ]

  try:
    result = check_output( cmd ).strip()
  except CalledProcessError as e:
    raise Exception( "Error running simulator!\n\n"
                     "Simulator command line: {cmd}\n\n"
                     "Simulator output:\n {output}"
                     .format( cmd=' '.join(e.cmd), output=e.output ) )

  # Find result

  lat = None
  for line in result.splitlines():
    if line.startswith('Average Latency'):
      lat = line.split('=')[1].strip()

  # Display result

  print "  - {:<5} {:<10} {:>9}".format( impl, input_, lat )

print ""
