import numpy as np

from qiskit import QuantumCircuit


class QwalkerGridCircuit():


    def __init__(self, dim1, dim2, graph, dynamic=False):

        self.graph = graph
        self.dynamic = dynamic

        self.vreg_len, self.ereg_len = self.num_qubits()
        self.reg_len = self.vreg_len + self.ereg_len

        self.N = np.ceil(np.log2(dim1), dtype=int)
        self.M = np.ceil(np.log2(dim2), dtype=int)

        self.circuit = QuantumCircuit(reg_len, reg_len)


    def num_qubits(self):
        return np.ceil(
            np.log2([self.graph.vertices, self.graph.edges]), dtype=int)


    def counter(self, add=1):

        circuit = QuantumCircuit(self.reg_len)
        start = 0
        end = self.N

        for i in range(start, end - 1):
            target_qubit = i
            control_qubits = np.arange(i + 1, end, dtype=int).tolist()
            circuit.mcx(
                control_qubits + list(range(self.vreg_len, self.ereg_len)), target_qubit)
        circuit.x(end)

        for i in range(start, end - 1):
            target_qubit = i
            control_qubits = np.arange(i + 1, end, dtype=int).tolist()

            for qubit in control_qubits:
                circuit.x(qubit)

            circuit.x(self.vreg_len + 1)
            circuit.mcx(
                control_qubits + list(range(self.vreg_len, self.ereg_len)), target_qubit)

            for qubit in control_qubits:
                circuit.x(qubit)
        circuit.x(end)

        start = self.N
        end = self.N + self.M

        for i in range(start, end - 1):
            target_qubit = i
            control_qubits = np.arange(i + 1, end, dtype=int).tolist()

            for qubit in control_qubits:
                circuit.x(qubit)

            circuit.x(self.vreg_len)
            circuit.mcx(
                control_qubits + list(range(self.vreg_len, self.ereg_len)), target_qubit)

            for qubit in control_qubits:
                circuit.x(qubit)

        for i in range(start, end - 1):
            target_qubit = i
            control_qubits = np.arange(i + 1, end, dtype=int).tolist()
            circuit.x(self.vreg_len)
            circuit.x(self.vreg_len + 1)
            circuit.mcx(
                control_qubits + list(range(self.vreg_len, self.ereg_len)), target_qubit)
        circuit.x(end)
    
        return circuit


    # def cyclic_counter(self, bound=None):

    #     # treat boundary cases
    #     if bound is None:
    #         limit = [1 for i in range(self.vreg_len)]
    #     else:
    #         limit = bound
        
    #     # run counter

    #     # undo operations
        




    # def flip_flop_circuit(self):

    #     """ Create a flip-flop operator for any grid using a coordinate 
    #     system in qubits. As an example, a 5-by-5 grid has 6 vertex qubits and
    #     2 dof qubits, giving a state ket |x1x2x3,y1y2y3,c1c2>. The flip flop
    #     bit can be implemented with operators
    #     U = A_x |0><0|_c0 Iy + B_x |1><1|_c0 I_y
    #     U = A_y |0><0|_c1 Ix + B_y |1><1|_c1 I_x.
    #     """

        

    # def create_coin(coin_list):
    #     for