import numpy as np

from qiskit import QuantumCircuit


class QwalkerGridCircuit():


    def __init__(self, dim1, dim2, graph, dynamic=False):

        self.graph = graph
        self.dynamic = dynamic

        self.vreg_len, self.ereg_len = self.num_qubits()
        self.reg_len = self.vreg_len + self.ereg_len

        self.N = int(np.ceil(np.log2(dim1)))
        self.M = int(np.ceil(np.log2(dim2)))

        self.circuit = QuantumCircuit(self.reg_len, self.reg_len)


    def num_qubits(self):
        return [int(x) for x in np.ceil( 
            np.log2([self.graph.number_of_nodes(), 4]))]


    def flip_flop(self):

        circuit = QuantumCircuit(self.reg_len)
        start = 0
        end = self.N

        for i in range(start, end - 1):
            target_qubit = i
            control_qubits = np.arange(i + 1, end, dtype=int).tolist()
            circuit.mcx(
                control_qubits + [self.vreg_len, self.vreg_len + 1],
                target_qubit)
        circuit.toffoli(self.vreg_len, self.vreg_len + 1, end - 1)
        circuit.barrier()

        for i in range(start, end - 1):
            target_qubit = i
            control_qubits = np.arange(i + 1, end, dtype=int).tolist()

            for qubit in control_qubits:
                circuit.x(qubit)

            circuit.x(self.vreg_len + 1)
            circuit.mcx(
                control_qubits + [self.vreg_len, self.vreg_len + 1],
                target_qubit)

            for qubit in control_qubits:
                circuit.x(qubit)
        circuit.toffoli(self.vreg_len, self.vreg_len + 1, end - 1)
        circuit.barrier()

        start = self.N
        end = self.N + self.M

        for i in range(start, end - 1):
            target_qubit = i
            control_qubits = np.arange(i + 1, end, dtype=int).tolist()

            for qubit in control_qubits:
                circuit.x(qubit)

            circuit.x(self.vreg_len)
            circuit.mcx(
                control_qubits + [self.vreg_len, self.vreg_len + 1],
                target_qubit)
            
            for qubit in control_qubits:
                circuit.x(qubit)
        circuit.toffoli(self.vreg_len, self.vreg_len + 1, end - 1)
        circuit.barrier()

        for i in range(start, end - 1):
            target_qubit = i
            control_qubits = np.arange(i + 1, end, dtype=int).tolist()
            circuit.x(self.vreg_len + 1)
            circuit.mcx(
                control_qubits + [self.vreg_len, self.vreg_len + 1],
                target_qubit)
        circuit.toffoli(self.vreg_len, self.vreg_len + 1, end - 1)
        circuit.barrier()

        circuit.x(self.vreg_len)
        circuit.x(self.vreg_len + 1)

        return circuit



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