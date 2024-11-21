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

    def calculate_old_regime_deductions(self, salary):
        """Calculate deductions for the Old Tax Regime."""
        basic_salary = salary * 0.5
        dearness_allowance = basic_salary * 0.1
        hra = salary * 0.4
        rent_paid = salary * 0.5

        section_80c = min(150000, basic_salary * 0.1)
        section_80d_self = 25000
        section_80d_parents = 50000
        section_80d_health_checkup = 5000

        hra_exemption = min(
            hra,
            basic_salary * 0.5,
            rent_paid - (basic_salary * 0.1)
        )

        total_deductions = (
                section_80c +
                section_80d_self +
                section_80d_parents +
                section_80d_health_checkup +
                hra_exemption
        )

        return {
            "section_80c": section_80c,
            "section_80d_self": section_80d_self,
            "section_80d_parents": section_80d_parents,
            "section_80d_health_checkup": section_80d_health_checkup,
            "hra_exemption": hra_exemption,
            "total_deductions": total_deductions
        }
