"""Advent of Code - Day 23, Year 2019
Solution Started: Mar 12, 2025
Puzzle Link: https://adventofcode.com/2019/day/23
Solution by: abbasmoosajee07
Brief: [Intcode Networks]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys
start_time = time.time()

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)
# from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D23_file = "Day23_input.txt"
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

# Read and sort input data into a grid
with open(D23_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_Networks:
    NETWORK_SIZE = 50  # Number of computers in the network

    def __init__(self, program):
        """
        Initialize a network of Intcode computers.
        Each computer starts with a unique ID and the provided Intcode program.
        """
        from Intcode_Computer import Intcode_CPU
        self.computers = {i: Intcode_CPU(program.copy(), [i])
                            for i in range(self.NETWORK_SIZE)}
        self.queues = {i: [] for i in range(self.NETWORK_SIZE)}
        self.nat_packet = None  # Store the last packet received by the NAT
        self.last_sent_y = None  # Track the last Y value sent to address 0
        self.y_sent = set()  # To track Y values sent to address 0

    def run_network(self, visualize: bool = False):
        """
        Run the network of computers continuously. Each computer processes its input,
        sends outputs to other computers, and checks for special 'destination 255' outputs.
        The network will terminate when a packet is sent to destination 255, returning its Y value.
        """
        queues = self.queues.copy()  # Shallow copy for efficiency
        computers = self.computers.copy()  # Use direct references; no need for deep copy

        while True:
            idle = True  # Assume idle until proven otherwise
            idle_computers = 0  # Count idle computers
            total_output = []  # Track outputs from computers for visualization

            for comp_no in range(self.NETWORK_SIZE):
                # Process the computer, either with its input queue or -1 if no input
                if queues[comp_no]:
                    computers[comp_no].process_program(queues[comp_no])
                    queues[comp_no].clear()  # Clear the input queue after processing
                    idle = False  # Activity detected, network is not idle
                else:
                    computers[comp_no].process_program([-1])  # No input, send -1

                # Clear paused state and get output from the computer
                computers[comp_no].paused = False
                output = computers[comp_no].get_result("output")
                computers[comp_no].output_list = []  # Clear output list after processing

                # Track the outputs for visualization
                total_output.extend(output)
                
                # Log each computer's output if visualize is True
                if visualize:
                    print(f"Computer {comp_no} -> Output: {output}")

                # Process output in chunks of three (dest, x, y)
                for pos in range(0, len(output), 3):
                    dest, x, y = output[pos:pos + 3]
                    if dest == 255:
                        return y  # Return the Y value if destination is 255
                    queues[dest].extend([x, y])  # Forward the packet to the correct queue
                    idle = False  # A packet was sent, network is not idle

            # Track idle computers
            idle_computers = sum(1 for queue in queues.values() if not queue)

            # If the network is idle (no packets sent or received), log the idle state and process NAT
            if idle:
                if visualize:
                    print(f"Network is idle. Idle computers: {idle_computers}/{self.NETWORK_SIZE}")
                    print(f"Total Output (last 10): {total_output[-10:]}")  # Show last 10 outputs for context

    def run_NAT(self, visualize: bool = False):
        """
        Run the network of computers continuously. Each computer processes its input,
        sends outputs to other computers, and checks for special 'destination 255' outputs.
        The network will terminate when a packet is sent to destination 255, returning its Y value.
        """
        queues = self.queues.copy()  # Shallow copy for efficiency
        computers = self.computers.copy()  # Use direct references; no need for deep copy

        while True:
            idle = True  # Assume idle until proven otherwise
            total_output = []  # Track outputs from computers for visualization

            for comp_no in range(self.NETWORK_SIZE):
                # Process the computer, either with its input queue or -1 if no input
                if queues[comp_no]:
                    computers[comp_no].process_program(queues[comp_no])
                    queues[comp_no].clear()  # Clear the input queue after processing
                    idle = False  # Activity detected, network is not idle
                else:
                    computers[comp_no].process_program([-1])  # No input, send -1

                # Clear paused state and get output from the computer
                computers[comp_no].paused = False
                output = computers[comp_no].get_result("output")
                computers[comp_no].output_list = []  # Clear output list after processing

                # Track the outputs for visualization
                total_output.extend(output)

                # Log each computer's output if visualize is True
                if visualize:
                    print(f"Computer {comp_no} -> Output: {output}")

                # Process output in chunks of three (dest, x, y)
                for pos in range(0, len(output), 3):
                    dest, x, y = output[pos:pos + 3]
                    if dest == 255:
                        self.nat_packet = (x, y)  # Store the packet in the NAT
                    else:
                        queues[dest].extend([x, y])  # Forward the packet to the correct queue
                    idle = False  # A packet was sent, network is not idle

            # If the network is idle (no packets sent or received), log the idle state and process NAT
            if idle:
                if visualize:
                    print(f"Network is idle. NAT is processing...")
                    print(f"Last NAT packet received: {self.nat_packet}")

                if self.nat_packet:
                    x, y = self.nat_packet
                    # Check if the Y value is the same as the last one sent to address 0
                    if y == self.last_sent_y:
                        if visualize:
                            print(f"NAT sent Y value {y} to address 0 twice in a row.")
                        return y  # Return the Y value if it's the same as the last sent value

                    # Send the NAT's packet to address 0 to wake up the network
                    self.queues[0].extend([x, y])
                    self.last_sent_y = y  # Update the last sent Y value
                    self.y_sent.add(y)  # Add the Y value to the set of sent Y values

                    if visualize:
                        print(f"NAT sent packet (x: {x}, y: {y}) to address 0.")
                # Show last few outputs from the computers for context
                if visualize:
                    print(f"Total Output (last 10): {total_output[-10:]}")  # Show last 10 outputs for context

# Run the networks
address_p1 = Intcode_Networks(input_program).run_network()
print("Part 1:", address_p1)

address_p2 = Intcode_Networks(input_program).run_NAT()
print("Part 2:", address_p2)

print(f"Execution Time = {time.time() - start_time:.5f}s")

