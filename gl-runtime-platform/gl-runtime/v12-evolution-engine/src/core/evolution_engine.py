"""V12 Evolution Engine - 演化引擎"""
from typing import Dict, List, Callable, Tuple
import random
from dataclasses import dataclass

@dataclass
class Genome:
    genes: Dict[str, float]
    fitness: float = 0.0

class EvolutionEngine:
    def __init__(self, population_size: int = 50):
        self.population: List[Genome] = []
        self.population_size = population_size
        self.generation = 0
        self.fitness_function: Callable = None
        self.mutation_rate = 0.1
    
    def initialize(self, gene_template: Dict[str, Tuple[float, float]]):
        self.population = []
        for _ in range(self.population_size):
            genes = {k: random.uniform(v[0], v[1]) for k, v in gene_template.items()}
            self.population.append(Genome(genes))
    
    def set_fitness_function(self, fn: Callable):
        self.fitness_function = fn
    
    def evaluate(self):
        for genome in self.population:
            if self.fitness_function:
                genome.fitness = self.fitness_function(genome.genes)
    
    def select(self) -> List[Genome]:
        sorted_pop = sorted(self.population, key=lambda g: g.fitness, reverse=True)
        return sorted_pop[:self.population_size // 2]
    
    def crossover(self, parent_a: Genome, parent_b: Genome) -> Genome:
        child_genes = {}
        for key in parent_a.genes:
            child_genes[key] = parent_a.genes[key] if random.random() > 0.5 else parent_b.genes[key]
        return Genome(child_genes)
    
    def mutate(self, genome: Genome) -> Genome:
        for key in genome.genes:
            if random.random() < self.mutation_rate:
                genome.genes[key] *= random.uniform(0.8, 1.2)
        return genome
    
    def evolve(self, generations: int = 10) -> Genome:
        for _ in range(generations):
            self.evaluate()
            survivors = self.select()
            new_population = survivors.copy()
            while len(new_population) < self.population_size:
                parents = random.sample(survivors, 2)
                child = self.crossover(parents[0], parents[1])
                child = self.mutate(child)
                new_population.append(child)
            self.population = new_population
            self.generation += 1
        return max(self.population, key=lambda g: g.fitness)
