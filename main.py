import cirq

from d2decode import decode
from qubit import LogicalQubit

def printSimpleX():
    qubit = cirq.NamedQubit('Simple Qubit')

    circuit = cirq.Circuit()
    circuit.append([cirq.X(qubit), cirq.measure(qubit)])

    print(circuit)

def printX():
    logicalQubit = LogicalQubit(2, forPrint=True)
    logicalQubit.applyX()

    logicalQubit.print()

def simulateSimpleX():
    qubit = cirq.NamedQubit('Simple Qubit')

    circuit = cirq.Circuit()
    circuit.append([cirq.X(qubit), cirq.measure(qubit)])

    sim = cirq.Simulator()
    results = sim.run(circuit)
    print(results)

def simulateXNoErrors():
    logicalQubit = LogicalQubit(2)
    logicalQubit.applyX()

    results = logicalQubit.run()
    print(results)

def simulateXWithErrors():
    repetitions = 100

    logicalQubit = LogicalQubit(2, 0.05)
    logicalQubit.applyX()

    results = logicalQubit.run(repetitions)
    
    totalErrors = 0
    totalMeasurements = 0
    totalCorrectMeasurements = 0
    for i in range(repetitions):
        decoded = decode(results.measurements['D_(0, 0)'][i][0],
                         results.measurements['D_(0, 1)'][i][0],
                         results.measurements['D_(1, 0)'][i][0],
                         results.measurements['D_(1, 1)'][i][0],
                         results.measurements['MZ_(0, 1)_1'][i][0],
                         results.measurements['MZ_(2, 1)_1'][i][0])

        if decoded.errorCount > 0:
            totalErrors = totalErrors + 1
        else:
            if decoded.result is not None:
                totalMeasurements = totalMeasurements + 1
            if decoded.result == 1:
                totalCorrectMeasurements = totalCorrectMeasurements + 1

    print('Errors: {}'.format(totalErrors))
    print('Measurements: {}'.format(totalMeasurements))
    print('Correct Measurements: {}'.format(totalCorrectMeasurements))

printSimpleX()
printX()

simulateSimpleX()
simulateXNoErrors()
simulateXWithErrors()
