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

def or_gate(circuit, i, j, a, b, o):
	circuit.x(a[i])
	circuit.x(b[j])
	circuit.ccx(a[i], b[j], o[i//2])
	circuit.x(o[i//2])
	return circuit

def unit_full_adder(a_in, b_in, c_in):
	q = QuantumRegister(5)
	c = ClassicalRegister(2)
	circuit = QuantumCircuit(q,c)
	if a_in == '1':
		circuit.x(q[0])		#Flip the qubit from 0 to 1
	if b_in == '1':
		circuit.x(q[1])		#Flip the qubit from 0 to 1
	if c_in == '1':
		circuit.x(q[2])		#Flip the qubit from 0 to 1
	circuit.cx(q[0],q[3])
	circuit.cx(q[1],q[3])
	circuit.cx(q[2],q[3])
	circuit.ccx(q[0],q[1],q[4])
	circuit.ccx(q[0],q[2],q[4])
	circuit.ccx(q[1],q[2],q[4])
	circuit.measure(q[3],c[0])
	circuit.measure(q[4],c[1])
	counts = simulator(circuit, 2048)
	print('output:',counts)
	print(circuit_drawer(circuit))

[print() for i in range(5)]
unit_full_adder('0', '0', '0')
unit_full_adder('1', '0', '0')
unit_full_adder('0', '1', '0')
unit_full_adder('0', '0', '1')
unit_full_adder('1', '1', '0')
unit_full_adder('0', '1', '1')
unit_full_adder('1', '0', '1')
unit_full_adder('1', '1', '1')


def addition_of_two_4_byte(a_in, b_in, n):
	a_in = a_in[::-1]
	b_in = b_in[::-1]
	
	a = QuantumRegister(n)
	b = QuantumRegister(n)
	c = QuantumRegister(n+1)
	s = QuantumRegister(n)
	out = ClassicalRegister(n)
	out_c = ClassicalRegister(1)
	circuit = QuantumCircuit(a, b, c, s, out, out_c)

	for i in range(n):
		if a_in[i] == '1':
			circuit.x(a[i])		#Flip the qubit from 0 to 1
	for i in range(n):
		if b_in[i] == '1':
			circuit.x(b[i])		#Flip the qubit from 0 to 1

	for i in range(n):
		circuit.cx(a[i],s[i])
		circuit.cx(b[i],s[i])
		circuit.cx(c[i],s[i])
		circuit.ccx(a[i],b[i],c[i+1])
		circuit.ccx(a[i],c[i],c[i+1])
		circuit.ccx(b[i],c[i],c[i+1])

	circuit.measure(s, out)
	circuit.measure(c[i+1], out_c)
	counts = simulator(circuit, 2048)
	print('output:',counts)
	print(circuit_drawer(circuit))

[print() for i in range(5)]
print("000, 000 = 0 000")
addition_of_two_4_byte('000','000', 3)
print("000, 001 = 0 001")
addition_of_two_4_byte('000','001', 3)
print("001, 000 = 0 001")
addition_of_two_4_byte('001','000', 3)
print("000, 010 = 0 010")
addition_of_two_4_byte('000','010', 3)
print("010, 000 = 0 010")
addition_of_two_4_byte('010','000', 3)
print("100, 100 = 1 000")
addition_of_two_4_byte('100','100', 3)
print("111, 110 = 1 101")
addition_of_two_4_byte('111','110', 3)
print("111, 101 = 1 100")
addition_of_two_4_byte('111','101', 3)

[print() for i in range(5)]
print("(12 = 1100) + (10 = 1010)")
addition_of_two_4_byte('1100', '1010', 4)