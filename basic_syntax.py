### ALL IMPORTS
import numpy as np
import qiskit
from qiskit import(
  QuantumCircuit,
  execute,
  Aer,
  BasicAer)
from qiskit.visualization import plot_histogram, circuit_drawer
print("Done Importing...")

### Initializing new circuit as QuantumCircuit(int, int), where: first int represents n qubits and m classical bits.
circuit = QuantumCircuit(2, 2)

### Basic Circuit
def circuit_construction(circuit):
	circuit.h(0)                      #Hadamard Gate
	circuit.cx(0, 1)                  #CNOT Gate
	circuit.measure([0,1], [0,1])     #Sends the qubit value to the classical bit
	return circuit

circuit = circuit_construction(circuit)

### Circuit Representation
print(circuit_drawer(circuit))

### Simulates the circuit, shots number of times, here = 2048
def simulator(circuit, shots):
	simulator = Aer.get_backend('qasm_simulator')
	job = execute(circuit, simulator, shots=shots)
	result = job.result()
	counts = result.get_counts(circuit)        # Gets count of the output of the circuit for 2048 times
	return counts

counts = simulator(circuit, 2048)
print('output:',counts)

plot_histogram(counts)                         # Draws a Histogram with the results from the simulation

### Now why is the result 00 or 11 with equal probabilities i.e, 50:50
### We start with |0> --H--> (|0> + |1>)/(2)^0.5, i.e. a measurement has equal probability to be a |0> or |1>, i.e. 50:50
### Now Cx gate for (|0> + |1>)/(2)^0.5 , |0> will give us, either |00> --cx--> |00> as the first qubit is 0
###                                                        whereas |10> --cx--> |11> as the first qubit is 1, so it will NOT the second qubit making that |0> --NOT--> |1>
### Now both of these will be executed with equal probabilities, which is the reason the result has equal probability of being 00 or 11.