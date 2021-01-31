import random
import time
import numpy as np
from qiskit import QuantumCircuit, transpile


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
    

    def build_evolution_operator(self, vertex_coins):
        self.c = self.coin(vertex_coins=vertex_coins)
        self.c.name = "C"
        self.s = self.flip_flop()
        self.s.name = "S"
        self.evo = self.c + self.s
        self.evo.name = "SC"


    def evolve(self, t):
        circuit = self.evo.power(t)
        circuit.measure(range(self.reg_len), range(self.reg_len))
        return circuit


    def flip_flop(self):

        circuit = QuantumCircuit(self.reg_len, self.reg_len)
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
        circuit.x(self.vreg_len + 1)
        circuit.barrier()

        return circuit


    def coin(self, vertex_coins=None):

        circuit = QuantumCircuit(self.reg_len, self.reg_len)
        if vertex_coins is None:
            circuit.h(self.vreg_len)
            circuit.h(self.vreg_len + 1)
            circuit.barrier()

        else:
            
            for vertex in vertex_coins:

                func_dic = { 
                    "H": lambda x, y: y.h(range(x)),
                    "G": lambda x, y: y.append(
                        self.grover_diffuser(),
                        list(range(x))),
                    "T": lambda x, y: y.t(range(x)),
                    "S": lambda x,y: y.s(range(x)),
                    "SWAP": lambda x,y: y.swap(0 ,1),
                }

                op = vertex_coins[vertex]
                if op == "rand":
                    op = random.choice(list(func_dic.keys()))

                vcoin = QuantumCircuit(self.ereg_len, name='Coin'+op)


                # if op == "H":
                #     vcoin.h(range(self.ereg_len))

                # elif op == "G":
                #     vcoin.append(
                #         self.grover_diffuser(),
                #         list(range(self.ereg_len)))

                # elif op == "T":
                #     vcoin.t(range(self.ereng_len))

                # elif op == "SWAP":
                #     vcoin.swap(0, 1)
                func_dic[op](self.ereg_len, vcoin)

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
            mcx.mcx(np.arange(i + 1, mcx_len, dtype=int), target_qubit)
            mcx.to_gate().control(
                num_ctrl_qubits=num_control,
                ctrl_state=num_control * ctrl_state)
        mcx.x(end - 1)
        return mcx


    def alternative_flip_flop(self):

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


    def grover_diffuser(self):
        nqubits = self.ereg_len
        qc = QuantumCircuit(nqubits)
        qc.h(range(nqubits)) # Apply transformation |s> -> |00..0> (H-gates)
        qc.x(range(nqubits)) # Apply transformation |00..0> -> |11..1> (X-gates)

        # Do multi-controlled-Z gate
        qc.h(nqubits-1)
        qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
        qc.h(nqubits-1)

        qc.x(range(nqubits))
        qc.h(range(nqubits))

        grover = qc.to_gate()
        grover.name = "G"
        return grover

    
    def compile_and_run(self, t, vertex_coins, mode="ionq_simulator"):

        from qiskit_ionq_provider import IonQProvider 
        from qiskit.tools.visualization import circuit_drawer 
        from qiskit.providers.jobstatus import JobStatus

        provider = IonQProvider(token='UXA0mTBVroG62waNXpn6yCXDyx2iDNH0')
        backend = provider.get_backend(mode)

        self.build_evolution_operator(vertex_coins)
        circuit = self.evolve(t)

        transpiled = transpile(circuit, backend=backend)
        print(circuit_drawer(circuit))

        job = backend.run(transpiled)


        #save job_id
        job_id = job.job_id()

        if mode == "ionq_simulator":
            #Fetch the result:
            result = job.result()

        elif mode == "ionq_qpu":
            job=backend.retrieve_job(job_id)
            while job.status() is not JobStatus.DONE:
                time.sleep(5)


        from qiskit.visualization import plot_histogram
        fig = plot_histogram(result.get_counts())
        fig.savefig("hist.png")

    # def num_qubits(self):
    #     return [int(x) for x in np.ceil( 
    #         np.log2([self.graph.number_of_nodes(), 4]))]

