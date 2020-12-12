# Surface Code Error Correction Using Cirq

Stephen Habegger

Phys 575

University of Washington - Autumn 2020

## Installation

To install the required packages, run:

```bash
$ pip install -r requirements.txt
```

If you prefer to try installing the latest releases, there are only two direct dependencies:

```bash
$ pip install cirq
$ pip install more-itertools
```

## Background

The surface code is a quantum computing error correcting and stabilizing code. It is based on the toric code, which was originally developed by Kitaev[1].

In the surface code, qubits can be conceived of as existing on a 2 dimensional lattice and interacting with each of their 4 nearest neighbors (or 2 or 3 neighbors on the boundary), though this is not necessarily a physical requirement of the system. However, the code is well suited to architectures that do adhere to this geometry, such as many superconducting processors.

Here, we implement a surface code on a grid, placing qubits at vertices, as in the below figure.

![D=3 Qubit Grid](./d_3_background.svg)

Here the white qubits represent data qubits. Together, these qubits represent the state of a single logical qubit. The green and blue qubits represent X and Z measurement qubits, respectively. The large colored blocks represent stabilizer groups. They are removed in the following image to make clear the qubit connectivity.

![D=3 Qubit Grid](./d_3.svg)

The code is implemented to support an arbitrary distance D, where the logical qubit is composed of DxD data qubits. A surface code must contain N = D^2 data qubits and N - 1 = D^2 - 1 measurement qubits. The measurement qubits are measured periodically, stabilizing the qubit by projecting onto a particular state. Furthermore, these measurements are used to determine and address an error syndrome. Due to these measurements, the logical qubit must contain one more data qubit than measurement qubits to maintain the necessary 2 degrees of freedom required by a logical qubit.

While this code does support arbitrary distance D, the built-in Cirq simulator was capable of running the circuit with no more than distance D = 2 on my home computer, so this is what was used for testing and demonstration.

![D=2 Qubit Grid](./d_2_background.svg)

![D=2 Qubit Grid](./d_2.svg)

## References

[1] Fowler, Austin G, Mariantoni, Matteo, Martinis, John M, & Cleland, Andrew N. (2012). Surface codes: Towards practical large-scale quantum computation. Physical Review. A, Atomic, Molecular, and Optical Physics, 86(3), Physical review. A, Atomic, molecular, and optical physics, 2012-09-18, Vol.86 (3).

[2] Criger, Ben, & Ashraf, Imran. (2018). Multi-path Summation for Decoding 2D Topological Codes. Quantum, 2, 102.

[3] Roffe, J. (2019). Quantum error correction: An introductory guide. Contemporary Physics, 60(3), 226-245.
