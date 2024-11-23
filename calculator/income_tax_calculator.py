class IncomeTaxCalculator:
    def __init__(self):
        self.old_regime_slabs = [
            {"max": 250000, "rate": 0},
            {"max": 500000, "rate": 0.05},
            {"max": 1000000, "rate": 0.20},
            {"max": float('inf'), "rate": 0.30}
        ]
        self.new_regime_slabs = [
            {"max": 300000, "rate": 0},
            {"max": 700000, "rate": 0.05},
            {"max": 1000000, "rate": 0.10},
            {"max": 1200000, "rate": 0.15},
            {"max": 1500000, "rate": 0.20},
            {"max": float('inf'), "rate": 0.30}
        ]
        self.cess_percentage = 0.04
        self.current_regime = 'old'

    def calculate_tax(self, taxable_income, regime=None):
        if regime is None:
            regime = self.current_regime
        slabs = self.old_regime_slabs if regime == 'old' else self.new_regime_slabs
        tax = 0
        prev_max = 0
        for slab in slabs:
            if taxable_income > slab['max']:
                taxable_in_slab = slab['max'] - prev_max
            else:
                taxable_in_slab = max(0, taxable_income - prev_max)
            tax += taxable_in_slab * slab['rate']
            if taxable_income <= slab['max']:
                break
            prev_max = slab['max']
        cess = tax * self.cess_percentage
        total_tax = tax + cess
        return total_tax

    def calculate_net_salary(self, gross_salary_lakhs, regime=None):
        gross_salary = gross_salary_lakhs * 100000
        if regime is None:
            regime = self.current_regime
        taxable_income = gross_salary
        tax = self.calculate_tax(taxable_income, regime)
        net_salary = gross_salary - tax
        return {
            "gross_salary_lakhs": gross_salary_lakhs,
            "taxable_income_lakhs": round(taxable_income / 100000, 2),
            "tax_lakhs": round(tax / 100000, 2),
            "net_salary_lakhs": round(net_salary / 100000, 2),
            "monthly_take_home_lakhs": round(net_salary / 1200000, 2)
        }

    def find_gross_salary_for_target_take_home(self, target_monthly_take_home_lakhs, regime=None):
        if regime is None:
            regime = self.current_regime
        target_annual_take_home = target_monthly_take_home_lakhs * 12 * 100000
        left, right = 1, 1000
        while right - left > 0.01:
            mid = (left + right) / 2
            result = self.calculate_net_salary(mid, regime)
            annual_take_home = result['net_salary_lakhs'] * 100000
            if annual_take_home < target_annual_take_home:
                left = mid
            else:
                right = mid
        return self.calculate_net_salary(right, regime)
