import cirq

from more_itertools import roundrobin

class GridPoint:

    def __init__(self, i, j):
        self.i = i
        self.j = j

class LogicalQubit:

    def __init__(self, d: int, p: float = 0, forPrint: bool = False):
        self._d = d
        self._p = p
        self._forPrint = forPrint
        self._circuit = cirq.Circuit()

        self._controlSuffix = 1
        self._step = 1

        size = 2 * d + 1

        self._qubits = [[None for i in range(size)] for j in range(size)]

        for x in range(d):
            for y in range(d):
                coords = self._translateDataQubitCoords(x, y)
                self._qubits[coords.j][coords.i] = cirq.GridQubit(coords.i, coords.j)

        for x in range(1, d):
            for y in range(1, d):
                coords = self._translateMeasureQubitCoords(x, y)
                self._qubits[coords.j][coords.i] = cirq.GridQubit(coords.i, coords.j)

        needsMeasureQubit = True
        for y in range(1, d):
            coords = self._translateMeasureQubitCoords(0, y)

            if needsMeasureQubit:
                self._qubits[coords.j][coords.i] = cirq.GridQubit(coords.i, coords.j)
            needsMeasureQubit = not needsMeasureQubit
        for x in range(1, d):
            coords = self._translateMeasureQubitCoords(x, d)

            if needsMeasureQubit:
                self._qubits[coords.j][coords.i] = cirq.GridQubit(coords.i, coords.j)
            needsMeasureQubit = not needsMeasureQubit
        for y in range(d - 1, 0, -1):
            coords = self._translateMeasureQubitCoords(d, y)

            if needsMeasureQubit:
                self._qubits[coords.j][coords.i] = cirq.GridQubit(coords.i, coords.j)
            needsMeasureQubit = not needsMeasureQubit
        for x in range(d - 1, 0, -1):
            coords = self._translateMeasureQubitCoords(x, 0)

            if needsMeasureQubit:
                self._qubits[coords.j][coords.i] = cirq.GridQubit(coords.i, coords.j)
            needsMeasureQubit = not needsMeasureQubit
    
    def _nextControlQubitName(self):
        name = 'Control{}'.format(self._controlSuffix)
        self._controlSuffix = self._controlSuffix + 1

        return name

    def _translateDataQubitCoords(self, x: int, y: int):
        return GridPoint(x + y + 1, self._d + y - x)

    def _translateMeasureQubitCoords(self, x: int, y: int):
        return GridPoint(x + y, self._d + y - x)

    def _stabilizeZ(self, x: int, y: int):
        if ((x + y) % 2 == 0):
            raise Exception('({}, {}) is not a valid Z measure qubit'.format(x, y))

        coords = self._translateMeasureQubitCoords(x, y)

        measureQubit = self._qubits[coords.j][coords.i]
        if measureQubit is None:
            return

        yield cirq.H(measureQubit)

        dataQubit = self._qubits[coords.j][coords.i - 1]
        if dataQubit is None:
            yield cirq.I(measureQubit)
        else:
            yield cirq.CZ(measureQubit, dataQubit)
        
        dataQubit = self._qubits[coords.j - 1][coords.i]
        if dataQubit is None:
            yield cirq.I(measureQubit)
        else:
            yield cirq.CZ(measureQubit, dataQubit)

        dataQubit = self._qubits[coords.j + 1][coords.i]
        if dataQubit is None:
            yield cirq.I(measureQubit)
        else:
            yield cirq.CZ(measureQubit, dataQubit)

        dataQubit = self._qubits[coords.j][coords.i + 1]
        if dataQubit is None:
            yield cirq.I(measureQubit)
        else:
            yield cirq.CZ(measureQubit, dataQubit)

        yield cirq.H(measureQubit)
        yield cirq.measure(measureQubit,
            key='MZ_({}, {})_{}'.format(x, y, self._step))

        if not self._forPrint:
            controlQubit = cirq.NamedQubit(self._nextControlQubitName())
            yield cirq.SWAP(measureQubit, controlQubit)

    def _stabilizeX(self, x: int, y: int):
        if ((x + y) % 2 == 1):
            raise Exception('({}, {}) is not a valid X measure qubit'.format(x, y))

        coords = self._translateMeasureQubitCoords(x, y)

        measureQubit = self._qubits[coords.j][coords.i]
        if measureQubit is None:
            return

        yield cirq.H(measureQubit)

        dataQubit = self._qubits[coords.j][coords.i - 1]
        if dataQubit is None:
            yield cirq.I(measureQubit)
        else:
            yield cirq.CNOT(measureQubit, dataQubit)
        
        dataQubit = self._qubits[coords.j + 1][coords.i]
        if dataQubit is None:
            yield cirq.I(measureQubit)
        else:
            yield cirq.CNOT(measureQubit, dataQubit)

        dataQubit = self._qubits[coords.j - 1][coords.i]
        if dataQubit is None:
            yield cirq.I(measureQubit)
        else:
            yield cirq.CNOT(measureQubit, dataQubit)

        dataQubit = self._qubits[coords.j][coords.i + 1]
        if dataQubit is None:
            yield cirq.I(measureQubit)
        else:
            yield cirq.CNOT(measureQubit, dataQubit)

        yield cirq.measure(measureQubit,
            key='MX_({}, {})_{}'.format(x, y, self._step))

        if not self._forPrint:
            controlQubit = cirq.NamedQubit(self._nextControlQubitName())
            yield cirq.SWAP(measureQubit, controlQubit)

    def _insertErrors(self):
        depolarize = cirq.depolarize(self._p)

        for y in range(self._d):
            for x in range(self._d):
                coords = self._translateDataQubitCoords(x, y)
                dataQubit = self._qubits[coords.j][coords.i]

                yield depolarize(dataQubit)

    def _stabilize(self):
        if not self._forPrint:
            self._circuit.append(self._insertErrors(),
                cirq.InsertStrategy.NEW_THEN_INLINE)

        zStabilizers = []
        xStabilizers = []
        for y in range(self._d + 1):
            for x in range(self._d + 1):
                if ((x + y) % 2 == 0):
                    xStabilizers.append(self._stabilizeX(x, y))
                else:
                    zStabilizers.append(self._stabilizeZ(x, y))

        self._circuit.append(roundrobin(*zStabilizers),
            cirq.InsertStrategy.NEW_THEN_INLINE)
        self._circuit.append(roundrobin(*xStabilizers),
            cirq.InsertStrategy.NEW_THEN_INLINE)
        
        self._step = self._step + 1

    def applyX(self):
        xOperations = []
        for y in range(self._d):
            coords = self._translateDataQubitCoords(0, y)
            dataQubit = self._qubits[coords.j][coords.i]

            xOperations.append(cirq.X(dataQubit))
        self._circuit.append(xOperations, cirq.InsertStrategy.NEW_THEN_INLINE)

        self._stabilize()

    def applyZ(self):
        zOperations = []
        for x in range(self._d):
            coords = self._translateDataQubitCoords(x, 0)
            dataQubit = self._qubits[coords.j][coords.i]

            zOperations.append(cirq.Z(dataQubit))
        self._circuit.append(zOperations, cirq.InsertStrategy.NEW_THEN_INLINE)

        self._stabilize()

    def run(self, repetitions: int = 1):
        measurements = []
        for x in range(self._d):
            for y in range(self._d):
                coords = self._translateDataQubitCoords(x, y)
                dataQubit = self._qubits[coords.j][coords.i]
                
                measurements.append(cirq.measure(dataQubit,
                    key='D_({}, {})'.format(x, y)))

        self._circuit.append(measurements, cirq.InsertStrategy.NEW_THEN_INLINE)

        sim = cirq.Simulator()
        return sim.run(self._circuit, repetitions=repetitions)

    def print(self):
        print(self._circuit)
