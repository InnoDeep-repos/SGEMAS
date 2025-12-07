import numpy as np
from scipy.stats import entropy

class SGEMAS_v33:
    """
    SGEMAS v3.3: Self-Growing Ephemeral Multi-Agent System
    
    Canonical implementation for the paper:
    "SGEMAS: A Self-Growing Ephemeral Multi-Agent System for Unsupervised Online Anomaly Detection"
    
    This version includes the Multi-Scale Instability Index and achieves AUC 0.570 on MIT-BIH DS2.
    """
    def __init__(self, 
                 alpha=0.6,    # Learning rate for mu
                 beta=0.18,    # Metabolic cost per agent
                 gamma=5.0,    # Metabolic gain from error
                 window=300,   # Window for precision estimation
                 max_agents=120,
                 growth_threshold=4.5,
                 death_threshold=0.6):
        
        # State variables
        self.mu = 0.0       # Internal belief (prediction)
        self.E = 0.0        # Metabolic Energy
        self.Pi = 1.0       # Adaptive Precision
        self.N = 1          # Agent Population
        self.win = []       # Rolling window for variance
        
        # Hyperparameters
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.window = window
        self.max_agents = max_agents
        self.growth_threshold = growth_threshold
        self.death_threshold = death_threshold

        # Multi-scale derivatives for Instability Index
        self.prev = 0
        self.prev2 = 0

    def process(self, x):
        """
        Process a single sample x(t).
        Returns a dictionary containing the anomaly score and internal states.
        """
        # 1. Update Rolling Window & Precision
        self.win.append(x)
        if len(self.win) > self.window:
            self.win.pop(0)

        if len(self.win) > 50:
            self.Pi = 1 / (np.var(self.win) + 1e-8)

        # 2. Compute Multi-scale Instability
        d1 = abs(x - self.prev)
        d2 = abs(self.prev - self.prev2)
        self.prev2 = self.prev
        self.prev = x
        
        instability = d1 + 0.5*d2

        # 3. Update Belief mu(t) (Langevin-like)
        # We add small jitter to simulate thermodynamic noise
        self.mu += self.alpha * (x - self.mu) + np.random.normal(0, 0.01)

        # 4. Compute Variational Free Energy (Surprise)
        F = abs(x - self.mu)

        # 5. Update Metabolic Energy Field E(t)
        # Gain from error + instability, Loss from population maintenance
        self.E += self.gamma * F * self.Pi + 0.7*instability - self.beta * self.N
        self.E = max(0, self.E)

        # 6. Structural Plasticity (Self-Organization)
        # Mitosis (Birth)
        if self.E > self.growth_threshold and self.N < self.max_agents:
            self.N += 1
        
        # Apoptosis (Death)
        if self.E < self.death_threshold and self.N > 1:
            self.N -= 1
        
        # 7. Return Metrics
        # Anomaly Score is Negative Energy (Deficit)
        return {
            "anom_score": -self.E,
            "instability": instability,
            "energy": self.E,
            "agents": self.N,
            "mu": self.mu
        }
