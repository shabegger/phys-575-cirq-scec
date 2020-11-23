import cirq
import deutsch

sim = cirq.Simulator()

unitaries = [
    deutsch.Constant0, 
    deutsch.Constant1,
    deutsch.BalancedI,
    deutsch.BalancedX,
]

for unitary in unitaries:
    circuit = deutsch.create(unitary, 0.05)
    result = sim.run(circuit, repetitions=100)
    print(circuit)
    print(result.histogram(key='result'))
