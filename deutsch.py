import cirq
import numpy as np

def create(unitary):
    circuit = cirq.Circuit()

    qIn = cirq.NamedQubit('input')
    qOut = cirq.NamedQubit('output')

    circuit.append(cirq.X(qOut))
    circuit.append([cirq.H(qIn), cirq.H(qOut)],
                   strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
    circuit.append(unitary().on(qIn, qOut))
    circuit.append(cirq.H(qIn))
    circuit.append(cirq.measure(qIn, key='result'))

    return circuit

class Constant0(cirq.MatrixGate):
    def __init__(self):
        cirq.MatrixGate.__init__(self, np.array([[1, 0, 0, 0],
                                                 [0, 1, 0, 0],
                                                 [0, 0, 1, 0],
                                                 [0, 0, 0, 1]]))

    def __str__(self):
        return 'C0'

    def __repr__(self):
        return 'Constant0'

    def _circuit_diagram_info_(self, args):
        return ('C0(In)', 'C0(Out)')

class Constant1(cirq.MatrixGate):
    def __init__(self):
        cirq.MatrixGate.__init__(self, np.array([[0, 1, 0, 0],
                                                 [1, 0, 0, 0],
                                                 [0, 0, 0, 1],
                                                 [0, 0, 1, 0]]))

    def __str__(self):
        return 'C1'

    def __repr__(self):
        return 'Constant1'

    def _circuit_diagram_info_(self, args):
        return ('C1(In)', 'C1(Out)')

class BalancedI(cirq.MatrixGate):
    def __init__(self):
        cirq.MatrixGate.__init__(self, np.array([[1, 0, 0, 0],
                                                 [0, 1, 0, 0],
                                                 [0, 0, 0, 1],
                                                 [0, 0, 1, 0]]))

    def __str__(self):
        return 'BI'

    def __repr__(self):
        return 'BalancedI'

    def _circuit_diagram_info_(self, args):
        return ('BI(In)', 'BI(Out)')

class BalancedX(cirq.MatrixGate):
    def __init__(self):
        cirq.MatrixGate.__init__(self, np.array([[0, 1, 0, 0],
                                                 [1, 0, 0, 0],
                                                 [0, 0, 1, 0],
                                                 [0, 0, 0, 1]]))

    def __str__(self):
        return 'BX'

    def __repr__(self):
        return 'BalancedX'

    def _circuit_diagram_info_(self, args):
        return ('BX(In)', 'BX(Out)')
