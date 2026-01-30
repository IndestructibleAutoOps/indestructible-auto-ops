"""V15 Neural Fabric - 神經織網"""
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass
import math
import random

@dataclass
class Neuron:
    id: str
    weights: List[float]
    bias: float = 0.0
    activation: float = 0.0

class NeuralFabric:
    def __init__(self):
        self.neurons: Dict[str, Neuron] = {}
        self.connections: Dict[str, List[str]] = {}
        self.layers: List[List[str]] = []
    
    def add_layer(self, size: int, input_size: int = None) -> List[str]:
        layer_ids = []
        input_s = input_size or (len(self.layers[-1]) if self.layers else 1)
        for i in range(size):
            nid = f"n_{len(self.layers)}_{i}"
            weights = [random.uniform(-1, 1) for _ in range(input_s)]
            self.neurons[nid] = Neuron(nid, weights, random.uniform(-0.5, 0.5))
            layer_ids.append(nid)
        self.layers.append(layer_ids)
        return layer_ids
    
    def connect_layers(self):
        for i in range(len(self.layers) - 1):
            for nid in self.layers[i]:
                self.connections[nid] = self.layers[i + 1]
    
    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-max(-500, min(500, x))))
    
    def forward(self, inputs: List[float]) -> List[float]:
        current = inputs
        for layer in self.layers:
            next_values = []
            for nid in layer:
                neuron = self.neurons[nid]
                total = sum(w * v for w, v in zip(neuron.weights, current)) + neuron.bias
                neuron.activation = self._sigmoid(total)
                next_values.append(neuron.activation)
            current = next_values
        return current
    
    def train(self, inputs: List[float], targets: List[float], lr: float = 0.1):
        outputs = self.forward(inputs)
        # Backpropagation (simplified)
        errors = [t - o for t, o in zip(targets, outputs)]
        for i, nid in enumerate(self.layers[-1]):
            neuron = self.neurons[nid]
            delta = errors[i] * neuron.activation * (1 - neuron.activation)
            for j in range(len(neuron.weights)):
                prev_activation = inputs[j] if len(self.layers) == 1 else self.neurons[self.layers[-2][j]].activation
                neuron.weights[j] += lr * delta * prev_activation
            neuron.bias += lr * delta
        return sum(e**2 for e in errors) / len(errors)
