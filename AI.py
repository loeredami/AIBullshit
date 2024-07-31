import funcs
import json
import random
import zlib


class Node:
    def __init__(self, weight):
        self.value = 0
        self.weight = weight

    @property
    def output(self):
        return self.value * self.weight


class Input(Node):
    def __init__(self, init_val, weight):
        super().__init__(weight)
        self.value = init_val

    def copy(self):
        return Input(self.value, self.weight)


class Output(Node):
    def __init__(self, weight):
        self.inputs: list[Node] = []
        super().__init__(weight)

    def add_input(self, node: Node):
        self.inputs.append(node)

    @property
    def output(self):
        return sum([_input.output for _input in self.inputs]) * self.weight

    def copy(self):
        INPUTS = []
        for _input in self.inputs:
            INPUTS.append(_input.copy())
        output = Output(self.weight)
        output.inputs = INPUTS
        return output


class Functional(Output):
    def __init__(self, weight, layer):
        self.layer = layer
        super().__init__(weight)

    @property
    def output(self):
        all_inputs = [_input.output for _input in self.inputs]
        return sum(all_inputs) * self.weight
            
    def copy(self):
        INPUTS = []
        for _input in self.inputs:
            INPUTS.append(_input.copy())
        output = Functional(self.weight, self.layer)
        output.inputs = INPUTS
        return output


class Network:
    def __init__(self, inputSize, outPutSize, limit=10, start_spread=10, max_layers=10):
        self.inputs = [
            Input(0, funcs.randomDirection() * start_spread) for _ in range(inputSize)
        ]
        self.outputs = [
            Output(funcs.randomDirection() * start_spread) for _ in range(outPutSize)
        ]
        for output in self.outputs:
            output.add_input(random.choice(self.inputs))
        self.functional = []
        self.limit = limit
        self.maxLayers = max_layers

    @property
    def allNodes(self):
        return self.inputs + self.outputs + self.functional

    @property
    def canInput(self):
        return self.inputs + self.functional

    @property
    def canOutput(self):
        return self.outputs + self.functional

    def process(self, inputs):
        for i, inputVal in enumerate(inputs):
            self.inputs[i].value = inputVal
        return [round(output.output, 5) for output in self.outputs]

    def mutate(self, amount, changeCap=1):
        for _ in range(random.randint(0, amount)):
            # Create Node
            if funcs.percentChance(50):
                if len(self.functional) >= self.limit:
                    try:
                        self.mutate(amount - 1, changeCap)
                        return
                    except:
                        return
                self.functional.append(
                    Functional(
                        funcs.randomDirection() * changeCap,
                        random.randint(0, self.maxLayers),
                    )
                )
            # Connect Node
            elif funcs.percentChance(25):
                destNode = random.choice(self.canOutput)
                srcNode = random.choice(self.canInput)
                if (type(destNode) == type(Output(1))) and (
                    type(srcNode) == type(Input(1, 1))
                ):
                    destNode.add_input(srcNode)
                elif type(destNode) == type(Output(1)):
                    destNode.add_input(srcNode)
                else:
                    try:
                        while srcNode.layer <= destNode.layer:
                            srcNode = random.choice(self.canInput)
                            if type(srcNode) == type(Input(1, 1)):
                                break
                    except AttributeError:
                        pass
                    destNode.add_input(srcNode)
            elif funcs.percentChance(10):
                node = random.choice(self.canOutput)
                if len(node.inputs) >= 1:
                    node.inputs.pop(random.randint(0, len(node.inputs) - 1))
            elif funcs.percentChance(5):
                node = random.choice(self.canOutput)
                if len(node.inputs) >= 1:
                    if type(node.inputs[0]) == type(Functional(1, 1)):
                        if len(node.inputs[0].inputs) == 0:
                            del node.inputs[0]
            else:
                random.choice(self.allNodes).weight += (
                    funcs.randomDirection() * changeCap
                )

    def copy(self):
        n = Network(len(self.inputs), len(self.outputs), self.limit)
        INPUTS = []
        OUTPUTS = []
        FUNCITONAL = []
        for _input in self.inputs:
            INPUTS.append(_input.copy())
        for _output in self.outputs:
            OUTPUTS.append(_output.copy())
        for functional in self.functional:
            FUNCITONAL.append(functional.copy())
        n.inputs = INPUTS
        n.outputs = OUTPUTS
        n.functional = FUNCITONAL
        return n


class NetworkTemplate:
    def __init__(self, inputSize, outPutSize, brainCellLimit, startSpread, maxLayers):
        self.inputSize = inputSize
        self.outPutSize = outPutSize
        self.brainCellLimit = brainCellLimit
        self.startSpread = startSpread
        self.maxLayers = maxLayers

    @property
    def network(self):
        return Network(
            self.inputSize,
            self.outPutSize,
            self.brainCellLimit,
            self.startSpread,
            self.maxLayers,
        )


def save_network(network: Network, filename):
    enumerated = enumerate(network.allNodes)
    enumerated_as_list = []
    for i, node in enumerated:
        layer = 0
        if type(node) == Functional:
            layer = node.layer
        enumerated_as_list.append(
            [str(type(node).__name__), node.weight, layer, []]
        )

    def get_i(node):
        enumerated = enumerate(network.allNodes)

        for i, _node in enumerated:
            if _node is node:
                return i
        return 0

    enumerated = enumerate(network.allNodes)

    for i, node in enumerated:
        if type(node) != Input:
            for _input in node.inputs:
                enumerated_as_list[i][-1].append(get_i(_input))
    with open(filename, "w") as dest:
        json.dump(enumerated_as_list, dest)


# Usage:
# save_network(your_network_instance, 'network_data.json')
def load_network(filename, brainCellLimit=10):
    network = Network(0, 0, brainCellLimit)
    all_cells = []
    with open(filename, "r") as file:
        network_data = json.load(file)
    for cell in network_data:
        if cell[0] == "Input":
            all_cells.append(Input(0, cell[1]))
        elif cell[0] == "Output":
            all_cells.append(Output(cell[1]))
        elif cell[0] == "Functional":
            all_cells.append(Functional(cell[1],cell[2]))
    for i, cell in enumerate(network_data):
        if len(cell[3]) == 0:
            continue
        for _id in cell[3]:
            all_cells[i].add_input(all_cells[_id])

    for cell in all_cells:
        if type(cell) == Input:
            network.inputs.append(cell)
        elif type(cell) == Functional:
            network.functional.append(cell)
        elif type(cell) == Output:
            network.outputs.append(cell)
    return network


def package(source_file, export_file):
    with open(source_file, "r") as src:
        with open(export_file, "wb") as dest:
            dest.write(zlib.compress(src.read().encode()))


def unpackage(source_file, export_file):
    with open(source_file, "rb") as src:
        with open(export_file, "w") as dest:
            dest.write(zlib.decompress(src.read()).decode())

