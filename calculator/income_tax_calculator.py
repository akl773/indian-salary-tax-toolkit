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

    def calculate_freelancer_tax(self, gross_receipts_lakhs, regime=None):
        """
        Calculate tax for freelancers under Section 44ADA.

        Args:
            gross_receipts_lakhs (float): Gross receipts in lakhs
            regime (str, optional): Tax regime to use. Defaults to current regime if None

        Returns:
            dict: Dictionary containing tax calculation details in lakhs
        """
        if regime is None:
            regime = self.current_regime

        # Convert lakhs to actual value
        gross_receipts = gross_receipts_lakhs * 100000.0

        # Under 44ADA, 50% is considered as expense deduction
        presumptive_income = gross_receipts * 0.5

        # Calculate deductions based on actual limits
        deductions = {
            'section_80c': 150000.0,
            'section_80d_self': min(25000.0, presumptive_income),
            'section_80d_parents': 50000.0,
            'section_80d_health_checkup': 5000.0,
            'hra': 60000.0
        }

        # Calculate total deductions
        total_deductions = sum(deductions.values())

        # Apply deductions to presumptive income
        taxable_income = max(0.0, presumptive_income - total_deductions)

        # Calculate tax on taxable income
        tax = self.calculate_tax(taxable_income, regime)

        # Add health and education cess (4%)
        tax = tax * (1 + self.cess_percentage)

        # Calculate final values in lakhs
        results = {
            "gross_receipts_lakhs": round(gross_receipts_lakhs, 2),
            "presumptive_income_lakhs": round(presumptive_income / 100000, 2),
            "total_deductions_lakhs": round(total_deductions / 100000, 2),
            "taxable_income_lakhs": round(taxable_income / 100000, 2),
            "tax_lakhs": round(tax / 100000, 2),
            "net_income_lakhs": round((gross_receipts - tax) / 100000, 2),
            "monthly_take_home_lakhs": round((gross_receipts - tax) / 1200000, 2),
            "expense_deduction_lakhs": round(gross_receipts * 0.5 / 100000, 2)
        }

        return results
