"""Script to program a bitstream to a chip"""
import argparse
from nirram import NIRRAM

# Get arguments
parser = argparse.ArgumentParser(description="Program a bitstream to a chip.")
parser.add_argument("chipname", help="chip name for logging")
parser.add_argument("bitstream", help="bitstream file name")
parser.add_argument("--start-addr", type=int, default=0, help="start addr")
parser.add_argument("--end-addr", type=int, default=65536, help="end addr")
parser.add_argument("--step-addr", type=int, default=1, help="addr step")
parser.add_argument("--iterations", type=int, default=3, help="number of programming iterations")
args = parser.parse_args()

# Initialize NI system
nisys = NIRRAM(args.chipname)

# Read bitstream
bitstream = open(args.bitstream).readlines()

# Do operation across cells
for i in range(args.iterations):
    for addr, bit in zip(range(args.start_addr, args.end_addr, args.step_addr), bitstream):
        nisys.set_addr(addr)
        bit = int(bit.strip())
        if bit == 0:
            target = nisys.target(9e3, 11e3)
        if bit == 1:
            target = nisys.target(100e3, 1e9)
        print(f"Iteration {i}, Address {addr}: {target}")

# Shutdown
nisys.close()
