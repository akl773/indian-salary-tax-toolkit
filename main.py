class IncomeTaxCalculator:
    def __init__(self):
        # Old Tax Regime Slabs
        self.old_regime_slabs = [
            {"max": 250000, "rate": 0},
            {"max": 500000, "rate": 0.05},
            {"max": 1000000, "rate": 0.20},
            {"max": float('inf'), "rate": 0.30}
        ]

        # New Tax Regime Slabs
        self.new_regime_slabs = [
            {"max": 300000, "rate": 0},
            {"max": 700000, "rate": 0.05},
            {"max": 1000000, "rate": 0.10},
            {"max": 1200000, "rate": 0.15},
            {"max": 1500000, "rate": 0.20},
            {"max": float('inf'), "rate": 0.30}
        ]

        # Current tax regime
        self.current_regime = 'old'
