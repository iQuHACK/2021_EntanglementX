# A quantum walk based single player game
Matheus Guedes de Andrade, Mohammad Mobayenjarihani and Nitish K. Panigrahy
## Introduction
We consider discrete-time coined-quantum walks to design a single player quantum game. A discrete-time coined quantum walk on a graph *G* is an evolution process of a complex vector in a Hilbert space defined by the graph structure *G*. The vertex space has dimension $|V|$ and codifies the vertices of the graph by assigning to each vertex a basis vector. In turns, the coin space denotes the degrees of freedom of the walker movements, with dimension given by the maximum degree of the graph. In a similar way, the coin space codifies the degrees of movement by assigning each degree to a basis vector. We assume *G* to be a regular graph and the degrees of freedom of the walk are restricted, on each vertex, to its incident outward edges. 

One can define the walker wavefunction at discrete time instant *t*. Thus the quantum walk evolution is given by the action of two unitary operators: The shift operator (*S*) and the coin operator (*W*). Here, while both *S* and *W* may vary with time, this dependence is omitted for simplification. *W* acts on the degrees of freedom of the walker.

## The Game
### Graph Struture
We assume *G* to be a 2D torus graph as shown below.

![Grid](https://github.com/iQuHACK/2021_EntanglementX/blob/main/Torus_graph.png)

### The Rules
The player is provided with the initial quantum state (*I*, which is the superposition of a list edge basis vectors with specific amplitudes), a target quantum state (*T*) and the walk length (*L*) . The goal of the player is to choose the coin operators for the vertices in *G* and a start vertex such that the quantum state after L iterations should be as close to *T* as possible. Some of the coin operators that the player can choose are shown below. The player also has an option to choose a *Random Coin Operator* which selects uniformly at random a coin operator for each node from the list of operotors before the game begins.

![Gates](https://github.com/iQuHACK/2021_EntanglementX/blob/main/gates.png)

## Implementation
All the coin opertors and measurements are implemented using real ionQ hardware. We use efficient implememtation of quantum random walks for regular graphs from [[1]](https://arxiv.org/pdf/quant-ph/0504042.pdf). The quantum circuits are shown below. The assumption us that the player has chosen the hardamard coin operator.

![2D Circuit](https://github.com/iQuHACK/2021_EntanglementX/blob/main/2D_circuit.png)

![Inc Dec](https://github.com/iQuHACK/2021_EntanglementX/blob/main/inc_dec_circuit.png)


## Future Work
- How to set *T* as a game designer? *T* uniform superposition of all edges?
- Winning strategy for the player? 
- Is random selection of coin operators beneficial when *T* uniform superposition of all edges?
- What if the player is allowed to choose coin operators at each time step?

## References
[1] Ivens Carneiro et. al. "Entanglement in coined quantum walks on regular graphs", arxiv:0504042.
