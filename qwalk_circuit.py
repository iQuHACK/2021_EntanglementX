import numpy as np

from qiskit import QuantumCircuit


class QwalkerGridCircuit():


    def __init__(self, dim1, dim2, graph, dynamic=False):

        self.graph = graph
        self.dynamic = dynamic

        self.N = int(np.ceil(np.log2(dim1)))
        self.M = int(np.ceil(np.log2(dim2)))

        self.vreg_len = self.N + self.M
        self.ereg_len = 2
        self.reg_len = self.vreg_len + self.ereg_len


        self.circuit = QuantumCircuit(self.reg_len, self.reg_len)


    # def num_qubits(self):
    #     return [int(x) for x in np.ceil( 
    #         np.log2([self.graph.number_of_nodes(), 4]))]


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


    def coin(self, vertex_coins=None):

        circuit = QuantumCircuit(self.reg_len)
        if vertex_coins is None:
            circuit.h(self.vreg_len)
            circuit.h(self.vreg_len + 1)
            circuit.barrier()

        else:
            for vertex in vertex_coins:

                vcoin = QuantumCircuit(self.ereg_len, name='HH')
                vcoin.x(range(self.ereg_len))
                cvcoin = vcoin.to_gate().control(
                    num_ctrl_qubits=self.vreg_len, ctrl_state=vertex)

                circuit.append(cvcoin, list(range(self.reg_len)))
                
            circuit.barrier()

        return circuit


    def counter(self, inc=1):
        start = 0
        end = self.N

        if inc == 1:
            ctrl_state = "1"
        else:
            ctrl_state = "0"

        for i in range(start, end - 1):

            target_qubit = i
            mcx_len = end - i
            num_control = mcx_len - 1
            mcx = QuantumCircuit(mcx_len)
            print(np.arange(i + 1, mcx_len, dtype=int))
            mcx.mcx(np.arange(i + 1, mcx_len, dtype=int), target_qubit)
            mcx.to_gate().control(
                num_ctrl_qubits=num_control,
                ctrl_state=num_control * ctrl_state)
        return mcx


    def simpler_flip_flop(self):

        flip_flop = QuantumCircuit(self.reg_len)
        
        # incrementer
        inc_x = QuantumCircuit(self.vreg_len)
        inc_x.append(self.counter(1), range(self.N))
        inc_x.to_gate().control(num_ctrl_qubits=2, ctrl_state="11")
        flip_flop.append(inc_x, [0, 1, 4, 5])
        flip_flop.barrier()

         # incrementer
        dec_x = QuantumCircuit(self.vreg_len)
        dec_x.append(self.counter(0), range(self.N))
        dec_x.to_gate().control(num_ctrl_qubits=2, ctrl_state="10")
        flip_flop.append(dec_x, [0, 1, 4, 5])
        flip_flop.barrier()

         # incrementer
        inc_y = QuantumCircuit(self.vreg_len)
        inc_y.append(self.counter(1), range(self.M))
        inc_y.to_gate().control(num_ctrl_qubits=2, ctrl_state="01")
        flip_flop.append(inc_y, [2, 3, 4, 5])
        flip_flop.barrier()

         # incrementer
        dec_y = QuantumCircuit(self.vreg_len)
        dec_y.append(self.counter(0), range(self.M))
        dec_y.to_gate().control(num_ctrl_qubits=2, ctrl_state="00")
        flip_flop.append(dec_y, [2, 3, 4, 5])
        flip_flop.barrier()

        return flip_flop



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