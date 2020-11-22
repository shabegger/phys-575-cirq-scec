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
    circuit = deutsch.create(unitary)
    results = sim.simulate(circuit)
    print(circuit)
    print(results)
