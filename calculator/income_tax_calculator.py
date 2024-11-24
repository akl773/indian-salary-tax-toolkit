from enum import Enum
from decimal import Decimal


class TaxRegime(Enum):
    """Enumeration for different tax regimes."""
    OLD = "old"
    NEW = "new"


class TaxSlab:
    """Represents a tax slab with maximum income limit and tax rate."""

    def __init__(self, max_amount: Decimal, rate: Decimal) -> None:
        self.max_amount = max_amount
        self.rate = rate


class TaxSlabCollection:
    """Collection of tax slabs for a specific regime."""

    def __init__(self, slabs: list[TaxSlab]) -> None:
        self.slabs = slabs


class IncomeTaxCalculator:
    """Professional income tax calculator with support for different regimes."""

    def __init__(self) -> None:
        self.cess_percentage: Decimal = Decimal('0.04')
        self.current_regime: TaxRegime = TaxRegime.OLD

        # Initialize tax slabs
        self._tax_slabs: dict[TaxRegime, TaxSlabCollection] = {
            TaxRegime.OLD: TaxSlabCollection([
                TaxSlab(Decimal('250000'), Decimal('0')),
                TaxSlab(Decimal('500000'), Decimal('0.05')),
                TaxSlab(Decimal('1000000'), Decimal('0.20')),
                TaxSlab(Decimal('Infinity'), Decimal('0.30'))
            ]),
            TaxRegime.NEW: TaxSlabCollection([
                TaxSlab(Decimal('300000'), Decimal('0')),
                TaxSlab(Decimal('600000'), Decimal('0.05')),
                TaxSlab(Decimal('900000'), Decimal('0.10')),
                TaxSlab(Decimal('1200000'), Decimal('0.15')),
                TaxSlab(Decimal('1500000'), Decimal('0.20')),
                TaxSlab(Decimal('Infinity'), Decimal('0.30'))
            ])
        }

    @property
    def current_regime_name(self):
        """ :return regime name """
        return self.current_regime.name.title()

    def calculate_tax(self, taxable_income: Decimal, regime: TaxRegime | None = None) -> Decimal:
        """
        Calculate tax based on taxable income and regime.

        Args:
            taxable_income: Income amount to calculate tax on
            regime: Tax regime to use (defaults to current regime if None)

        Returns:
            Total tax including cess
        """
        regime = regime or self.current_regime
        slabs = self._tax_slabs[regime].slabs

        tax: Decimal = Decimal('0')
        prev_max: Decimal = Decimal('0')

        for slab in slabs:
            if taxable_income > slab.max_amount:
                taxable_in_slab = slab.max_amount - prev_max
            else:
                taxable_in_slab = max(Decimal('0'), taxable_income - prev_max)

            tax += taxable_in_slab * slab.rate

            if taxable_income <= slab.max_amount:
                break

            prev_max = slab.max_amount

        cess = tax * self.cess_percentage
        return tax + cess

    def calculate_net_salary(
            self,
            gross_salary_lakhs: Decimal | float,
            regime: TaxRegime | None = None
    ) -> dict:
        """
        Calculate net salary after tax deductions.

        Args:
            gross_salary_lakhs: Gross salary in lakhs
            regime: Tax regime to use (defaults to current regime if None)

        Returns:
            Dictionary containing calculation details
        """
        gross_salary_lakhs = Decimal(str(gross_salary_lakhs))
        gross_salary = gross_salary_lakhs * Decimal('100000')
        regime = regime or self.current_regime

        # Calculate basic salary (50% of gross salary)
        basic_salary = gross_salary * Decimal('0.5')

        # Calculate HRA component (Assuming HRA is 50% of basic salary)
        hra = basic_salary * Decimal('0.4')

        # Calculate employee's PF contribution (12% of basic salary)
        employee_pf = basic_salary * Decimal('0.12')

        # Calculate employer's PF contribution (12% of basic salary)
        employer_pf = basic_salary * Decimal('0.12')

        # total pf
        total_pf =  employee_pf +employer_pf
        # Deductions
        standard_deduction = Decimal('50000')  # Standard deduction allowed in both regimes

        if regime == TaxRegime.OLD:
            # PF contribution under section 80C (up to ₹1.5 lakh)
            section_80c_deduction = min(employee_pf, Decimal('150000'))

            # HRA exemption calculation
            # Assuming maximum HRA exemption (rent paid is high enough)
            hra_exemption = hra  # Since we're assuming the maximum possible exemption

            # Total deductions
            deductions = standard_deduction + section_80c_deduction + hra_exemption
        else:
            # In the new regime, only standard deduction is allowed
            deductions = standard_deduction

        # Calculate taxable income
        taxable_income = gross_salary - deductions

        # Calculate tax
        tax = self.calculate_tax(taxable_income, regime)

        # Calculate net salary (only employee's PF is deducted from net salary)
        net_salary = gross_salary - total_pf - tax

        return {
            "gross_salary_lakhs": gross_salary_lakhs,
            "basic_salary_lakhs": round(basic_salary / Decimal('100000'), 2),
            "hra_lakhs": round(hra / Decimal('100000'), 2),
            "pf_lakhs": round(total_pf / Decimal('100000'), 2),
            "deductions_lakhs": round(deductions / Decimal('100000'), 2),
            "taxable_income_lakhs": round(taxable_income / Decimal('100000'), 2),
            "tax_lakhs": round(tax / Decimal('100000'), 2),
            "net_salary_lakhs": round(net_salary / Decimal('100000'), 2),
            "monthly_take_home_lakhs": round(net_salary / Decimal('1200000'), 2)
        }

    def find_gross_salary_for_target_take_home(
            self,
            target_monthly_take_home_lakhs: Decimal | float,
            regime: TaxRegime | None = None
    ) -> dict:
        """
        Find required gross salary for desired monthly take-home salary.

        Args:
            target_monthly_take_home_lakhs: Desired monthly take-home salary in lakhs
            regime: Tax regime to use (defaults to current regime if None)

        Returns:
            Dictionary with required gross salary details
        """
        target_monthly_take_home_lakhs = Decimal(str(target_monthly_take_home_lakhs))
        target_annual_take_home = target_monthly_take_home_lakhs * Decimal('12') * Decimal('100000')
        regime = regime or self.current_regime

        left, right = Decimal('1'), Decimal('1000')
        while right - left > Decimal('0.01'):
            mid = (left + right) / Decimal('2')
            result = self.calculate_net_salary(mid, regime)
            annual_take_home = result["net_salary_lakhs"] * Decimal('100000')

            if annual_take_home < target_annual_take_home:
                left = mid
            else:
                right = mid

        return self.calculate_net_salary(right, regime)

    def calculate_freelancer_tax(
            self,
            gross_receipts_lakhs: Decimal | float,
            regime: TaxRegime | None = None
    ) -> dict:
        """
        Calculate tax for freelancers under Section 44ADA.

        Args:
            gross_receipts_lakhs: Gross receipts in lakhs
            regime: Tax regime to use (defaults to current regime if None)

        Returns:
            Dictionary containing calculation details
        """
        gross_receipts_lakhs = Decimal(str(gross_receipts_lakhs))
        gross_receipts = gross_receipts_lakhs * Decimal('100000')
        regime = regime or self.current_regime

        # Under 44ADA, 50% is considered as an expense deduction
        presumptive_income = gross_receipts * Decimal('0.5')

        # Calculate deductions based on actual limits
        deductions: dict[str, Decimal] = {
            'section_80c': Decimal('150000'),
            'section_80d_self': min(Decimal('25000'), presumptive_income),
            'section_80d_parents': Decimal('50000'),
            'section_80d_health_checkup': Decimal('5000'),
            'hra': Decimal('60000'),
            'standard_deduction': Decimal('50000')
        }

        total_deductions = sum(deductions.values())
        taxable_income = max(Decimal('0'), presumptive_income - total_deductions)
        tax = self.calculate_tax(taxable_income, regime)

        return {
            "gross_receipts_lakhs": round(gross_receipts_lakhs, 2),
            "presumptive_income_lakhs": round(presumptive_income / Decimal('100000'), 2),
            "total_deductions_lakhs": round(total_deductions / Decimal('100000'), 2),
            "taxable_income_lakhs": round(taxable_income / Decimal('100000'), 2),
            "tax_lakhs": round(tax / Decimal('100000'), 2),
            "net_income_lakhs": round((gross_receipts - tax) / Decimal('100000'), 2),
            "monthly_take_home_lakhs": round((gross_receipts - tax) / Decimal('1200000'), 2),
            "expense_deduction_lakhs": round(gross_receipts * Decimal('0.5') / Decimal('100000'), 2)
        }
