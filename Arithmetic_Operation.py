### ALL IMPORTS
import numpy as np
import qiskit
from qiskit import(
  QuantumCircuit,
  QuantumRegister,
  execute,
  ClassicalRegister,
  Aer,
  BasicAer)
from qiskit.visualization import plot_histogram, circuit_drawer
print("Done Importing...")

### Now classical addition in computers works using bits, say: 101011 and 100010 --+--> 1001101
[print() for i in range(5)]
print("Binary Addition Example:")
print(101011, int('101011', 2))
print(100010, int('100010', 2))
print(1001101, int('101011', 2)+int('100010', 2), int('1001101', 2))

### Simulates the circuit, shots number of times, here = 2048
def simulator(circuit, shots):
	simulator = Aer.get_backend('qasm_simulator')
	job = execute(circuit, simulator, shots=shots)
	result = job.result()
	counts = result.get_counts(circuit)        # Gets count of the output of the circuit for 2048 times
	return counts

### From this we can clearly see that: with c(0):
###                             c(0) + 0 + 0 = 0 + c(0)            carry:0
###                             c(0) + 1 + 0 = 0 + 1 = 1 + c(0)	   carry:0
###                             c(0) + 1 + 1 = 0 + c(1)			   carry:1
### Now taking c(1) in all these conditons
###                             c(1) + 0 + 0 = 1 + c(0)			   carry:0
###                             c(1) + 1 + 0 = 0 + 1 = 0 + c(1)	   carry:1
###                             c(1) + 1 + 1 = 1 + c(1)			   carry:1

### So we can clearly see that addition takes into account 3 qubits: where, 
### (0,0,0) --ADD--> (0,0)
### (1,0,0) --ADD--> (1,0)
### (0,1,0) --ADD--> (1,0)
### (0,0,1) --ADD--> (1,0)
### (1,1,0) --ADD--> (0,1)
### (1,0,1) --ADD--> (0,1)
### (0,1,1) --ADD--> (0,1)
### (1,1,1) --ADD--> (1,1)

### Now number of elements input = elements output using a quantum gate, here however 3 qubits give 2 outputs so, the final gate is a double-qubit gate.

### Lets try the sum without carrier qubit as input but carrier qubit as output, i.e. number of inputs = number of outputs
### (0,0) --ADD--> (0,0)
### (1,0) --ADD--> (1,0)
### (0,1) --ADD--> (1,0)
### (1,1) --ADD--> (0,1)

### Now as we can see the first output is given by Ex-Or and the second one is an AND gate.
### A common quantum gate for Ex-Or can be: cx-gate given by (a,b) --cx--> (a,a^b)
### An AND gate gives 1 only if the first two qubits is 1, there is only CCNOT Gate which has a semblence close to AND gate where the third qubit is NOTted only when the first two are 1
### AND gate output is 1 for only 1 and 1, so the third qubit must 0, so that CCNOT gate becomes an AND gate, on the third qubit while retaining the two initial qubit values

def and_gate(a_in, b_in):
	a = QuantumRegister(1)
	b = QuantumRegister(1)
	c = QuantumRegister(2)
	out = ClassicalRegister(1)
	circuit = QuantumCircuit(a, b, c, out)
	if a_in == 1:
		circuit.x(a)		#Flip the qubit from 0 to 1
	if b_in == 1:
		circuit.x(b)		#Flip the qubit from 0 to 1
	circuit.ccx(a, b, c[1])
	circuit.measure(c[1], out)
	counts = simulator(circuit, 2048)
	print('output:',counts)
	print(circuit_drawer(circuit))

[print() for i in range(5)]
print("AND Gate Using CCNOT Gate")
and_gate(0,0)
and_gate(1,0)
and_gate(0,1)
and_gate(1,1)



def addition_of_two_bits(a_in, b_in):  #Half-Adder Implementation
	# Now ADDITION is given by, Ex-Or followed by And Gate
	a = QuantumRegister(1)
	b = QuantumRegister(1)
	c = QuantumRegister(1)
	out = ClassicalRegister(2)
	circuit = QuantumCircuit(a, b, c, out)
	if a_in == 1:
		circuit.x(a)		#Flip the qubit from 0 to 1
	if b_in == 1:
		circuit.x(b)		#Flip the qubit from 0 to 1
	circuit.ccx(a, b, c)
	circuit.cx(a, b)
	circuit.measure(b, out[0])    #Doubt: Why does value of 
	circuit.measure(c, out[1])
	counts = simulator(circuit, 2048)
	print('output:',counts)
	print(circuit_drawer(circuit))

[print() for i in range(5)]
addition_of_two_bits(0,0)   #Output: 0,0
addition_of_two_bits(1,0)   #Output: 0,1
addition_of_two_bits(0,1)	#Output: 0,1
addition_of_two_bits(1,1)	#Output: 1,0

def half_adder(circuit, i, a, b, g, k):
	circuit.ccx(a[i],b[i],g[k])
	circuit.cx(a[i],b[i])
	return circuit

def or_gate()

def addition_of_two_4_byte(a_in, b_in):
	n = 3
	a = QuantumRegister(n)
	b = QuantumRegister(n)
	c = QuantumRegister(n)
	g = QuantumRegister(n*2)
	out = ClassicalRegister(n+1)
	circuit = QuantumCircuit(a, b, c, g, out)
	for i in range(n):
		if a_in[i] == 1:
			circuit.x(a[i])		#Flip the qubit from 0 to 1
	for i in range(n):
		if b_in[i] == 1:
			circuit.x(b[i])		#Flip the qubit from 0 to 1

	for i in range(n):
		circuit = half_adder(circuit, i, a, b, g, 2*i)
		circuit = half_adder(circuit, i, b, c, g, 2*i+1)


