import cirq

from math import ceil, floor
from more_itertools import roundrobin

D = 3

size = 2 * D + 1

controlSuffix = 1
def nextControlQubitName():
    global controlSuffix

    name = 'Control{}'.format(controlSuffix)
    controlSuffix = controlSuffix + 1

    return name

qubits = [[None for i in range(size)] for j in range(size)]
for i in range(1, size - 1):
    for j in range(1, size - 1):
        if ((floor(i / 2) + ceil(j / 2) > (D - 1) / 2) and
            (ceil(j / 2) - ceil(i / 2) < (D + 1) / 2) and
            (floor(i / 2) - floor(j / 2) < (D + 1) / 2) and
            (ceil(i / 2) + floor(j / 2) < (3 * D + 1) / 2)):
            qubits[j][i] = cirq.GridQubit(i, j)

def translateDataQubitCoords(x, y):
    return (x + y + 1, D + y - x)

def translateMeasureQubitCoords(x, y):
    return (x + y, D + y - x)

def stabilizeZ(x, y, for_print = False):
    if ((x + y) % 2 == 1):
        raise Exception('({}, {}) is not a valid Z measure qubit'.format(x, y))

    translated = translateMeasureQubitCoords(x, y)
    i = translated[0]
    j = translated[1]

    measureQubit = qubits[j][i]
    if measureQubit is None:
        return

    yield cirq.I(measureQubit)

    dataQubit = qubits[j][i - 1]
    if dataQubit is None:
        yield cirq.I(measureQubit)
    else:
        yield cirq.CNOT(dataQubit, measureQubit)
    
    dataQubit = qubits[j - 1][i]
    if dataQubit is None:
        yield cirq.I(measureQubit)
    else:
        yield cirq.CNOT(dataQubit, measureQubit)

    dataQubit = qubits[j + 1][i]
    if dataQubit is None:
        yield cirq.I(measureQubit)
    else:
        yield cirq.CNOT(dataQubit, measureQubit)

    dataQubit = qubits[j][i + 1]
    if dataQubit is None:
        yield cirq.I(measureQubit)
    else:
        yield cirq.CNOT(dataQubit, measureQubit)

    yield cirq.I(measureQubit)
    yield cirq.measure(measureQubit)

    if not for_print:
        controlQubit = cirq.NamedQubit(nextControlQubitName())
        yield cirq.SWAP(measureQubit, controlQubit)

def stabilizeX(x, y, for_print = False):
    if ((x + y) % 2 == 0):
        raise Exception('({}, {}) is not a valid X measure qubit'.format(x, y))

    translated = translateMeasureQubitCoords(x, y)
    i = translated[0]
    j = translated[1]

    measureQubit = qubits[j][i]
    if measureQubit is None:
        return

    yield cirq.H(measureQubit)

    dataQubit = qubits[j][i - 1]
    if dataQubit is None:
        yield cirq.I(measureQubit)
    else:
        yield cirq.CNOT(measureQubit, dataQubit)
    
    dataQubit = qubits[j + 1][i]
    if dataQubit is None:
        yield cirq.I(measureQubit)
    else:
        yield cirq.CNOT(measureQubit, dataQubit)

    dataQubit = qubits[j - 1][i]
    if dataQubit is None:
        yield cirq.I(measureQubit)
    else:
        yield cirq.CNOT(measureQubit, dataQubit)

    dataQubit = qubits[j][i + 1]
    if dataQubit is None:
        yield cirq.I(measureQubit)
    else:
        yield cirq.CNOT(measureQubit, dataQubit)

    yield cirq.H(measureQubit)
    yield cirq.measure(measureQubit)

    if not for_print:
        controlQubit = cirq.NamedQubit(nextControlQubitName())
        yield cirq.SWAP(measureQubit, controlQubit)

operations = []
for y in range(D + 1):
    for x in range(D + 1):
        if ((x + y) % 2 == 0):
            operations.append(stabilizeZ(x, y, True))
        else:
            operations.append(stabilizeX(x, y, True))

circuit = cirq.Circuit()
circuit.append(roundrobin(*operations))

print(circuit)
