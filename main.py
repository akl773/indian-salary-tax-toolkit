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

    def calculate_tax(self, taxable_income, regime=None):
        """Calculate income tax based on the specified regime."""
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

        return tax

    def calculate_net_salary(self, gross_salary_lakhs, regime=None):
        """Calculate net take-home salary after tax."""
        # Convert lakhs to actual value
        gross_salary = gross_salary_lakhs * 100000

        if regime is None:
            regime = self.current_regime

        if regime == 'old':
            deductions = self.calculate_old_regime_deductions(gross_salary)
            taxable_income = max(0, gross_salary - deductions['total_deductions'])
        else:
            deductions = {"total_deductions": 0}
            taxable_income = gross_salary

        tax = self.calculate_tax(taxable_income, regime)
        net_salary = gross_salary - tax

        return {
            "gross_salary_lakhs": gross_salary_lakhs,
            "deductions_lakhs": round(deductions['total_deductions'] / 100000, 2),
            "taxable_income_lakhs": round(taxable_income / 100000, 2),
            "tax_lakhs": round(tax / 100000, 2),
            "net_salary_lakhs": round(net_salary / 100000, 2),
            "monthly_take_home_lakhs": round(net_salary / 1200000, 2),
            "deduction_details": deductions
        }

    def find_gross_salary_for_target_take_home(self, target_monthly_take_home_lakhs, regime=None):
        """Find gross salary required to achieve target monthly take-home salary."""
        if regime is None:
            regime = self.current_regime

        # Convert monthly take-home from lakhs to annual value
        target_annual_take_home = target_monthly_take_home_lakhs * 12 * 100000

        left, right = 1, 1000  # Search in lakhs

        while right - left > 0.01:
            mid = (left + right) / 2
            result = self.calculate_net_salary(mid, regime)

            annual_take_home = result['net_salary_lakhs'] * 100000

            if annual_take_home < target_annual_take_home:
                left = mid
            else:
                right = mid

        return self.calculate_net_salary(right, regime)
