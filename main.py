import sys


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

    @staticmethod
    def calculate_old_regime_deductions(salary: float):
        """
        Calculate optimized deductions for the Old Tax Regime.

        Args:
            salary (float): Total annual salary

        Returns:
            dict: Deductions with optimized rent
        """
        # Precompute constant values
        basic_salary = salary * 0.5
        hra = salary * 0.4

        deductions = {
            'section_80c': min(150000.0, basic_salary),
            'section_80d_self': 25000,
            'section_80d_parents': 50000,
            'section_80d_health_checkup': 5000
        }

        def calculate_hra_exemption(rent_multiplier):
            """Calculate HRA exemption efficiently."""
            rent_paid = salary * rent_multiplier
            return min(
                hra,
                basic_salary * 0.5,
                rent_paid - (basic_salary * 0.1)
            )

        def find_optimal_rent_multiplier(low=0.1, high=0.5, step=0.1):
            """Find optimal rent multiplier using binary search strategy."""
            best_multiplier = low
            max_exemption = calculate_hra_exemption(low)

            current = low + step
            while current <= high:
                current_exemption = calculate_hra_exemption(current)

                # Prefer lower multiplier if exemptions are equal
                if current_exemption > max_exemption or \
                        (current_exemption == max_exemption and current < best_multiplier):
                    max_exemption = current_exemption
                    best_multiplier = current

                current += step

            return best_multiplier, max_exemption

        # Find optimal rent details
        optimal_rent_multiplier, hra_exemption = find_optimal_rent_multiplier()

        # Add HRA exemption to deductions
        deductions['hra_exemption'] = hra_exemption

        # Calculate total deductions and add additional details
        total_deductions = sum(deductions.values())

        return {
            **deductions,
            'optimal_rent': salary * optimal_rent_multiplier,
            'total_deductions': total_deductions
        }

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
        tax = tax * 1.04

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


class TaxCalculatorApp:
    def __init__(self):
        self.calculator = IncomeTaxCalculator()

    @staticmethod
    def display_regime_selection_menu():
        """Display the tax regime selection menu."""
        print("\n===== 🇮🇳 Indian Income Tax Calculator 📊 =====")
        print("Select Tax Regime:")
        print("1. Old Tax Regime")
        print("2. New Tax Regime")
        print("3. Exit")
        print("=" * 50)

    def display_main_menu(self):
        """Display the main menu options."""
        current_regime = self.calculator.current_regime.title()
        print(f"\n===== 🏦 {current_regime} Tax Regime Options 💼 =====")
        print("1. Calculate Net Salary")
        print("2. Find Gross Salary for Target Take-Home")
        print("3. Detailed Deduction Breakdown")
        print("4. Calculate Freelancer Tax (Section 44ADA)")
        print("5. Change Tax Regime")
        print("6. Exit")
        print("=" * 50)

    def get_numeric_input(self, prompt, input_type=float, min_val=None, max_val=None):
        """Get validated numeric input from user."""
        while True:
            try:
                value = input_type(input(prompt))
                if min_val is not None and value < min_val:
                    print(f"❌ Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"❌ Value must not exceed {max_val}")
                    continue
                return value
            except ValueError:
                print("❌ Invalid input. Please enter a numeric value.")

    def calculate_net_salary_menu(self):
        """Interactive menu for calculating net salary."""
        print(f"\n🔍 Net Salary Calculation ({self.calculator.current_regime.title()} Regime)")
        gross_salary_lakhs = self.get_numeric_input("Enter Gross Annual Salary (₹ in Lakhs): ", min_val=0)

        result = self.calculator.calculate_net_salary(gross_salary_lakhs)

        print("\n📊 Salary Breakdown:")
        labels = {
            "gross_salary_lakhs": "Gross Salary",
            "deductions_lakhs": "Total Deductions",
            "taxable_income_lakhs": "Taxable Income",
            "tax_lakhs": "Total Tax",
            "net_salary_lakhs": "Net Annual Salary",
            "monthly_take_home_lakhs": "Monthly Take-Home"
        }

        for key, value in result.items():
            if key != 'deduction_details' and key in labels:
                print(f"{labels[key]}: ₹{value} Lakhs")

    def find_gross_salary_menu(self):
        """Interactive menu for finding gross salary."""
        print(f"\n💰 Gross Salary Determination ({self.calculator.current_regime.title()} Regime)")
        target_monthly_lakhs = self.get_numeric_input("Enter Target Monthly Take-Home Salary (₹ in Lakhs): ", min_val=0)

        result = self.calculator.find_gross_salary_for_target_take_home(target_monthly_lakhs)

        print("\n📊 Gross Salary Requirement:")
        labels = {
            "gross_salary_lakhs": "Gross Annual Salary",
            "deductions_lakhs": "Total Deductions",
            "taxable_income_lakhs": "Taxable Income",
            "tax_lakhs": "Total Tax",
            "net_salary_lakhs": "Net Annual Salary",
            "monthly_take_home_lakhs": "Monthly Take-Home"
        }

        for key, value in result.items():
            if key != 'deduction_details' and key in labels:
                print(f"{labels[key]}: ₹{value} Lakhs")

    def detailed_deductions_menu(self):
        """Detailed deduction breakdown for Old Regime."""
        if self.calculator.current_regime != 'old':
            print("\n❌ Detailed deductions are only available for the Old Tax Regime.")
            return

        print("\n📋 Detailed Deductions Breakdown (Old Regime)")
        gross_salary_lakhs = self.get_numeric_input("Enter Gross Annual Salary (₹ in Lakhs): ", min_val=0)

        # Convert lakhs to actual value for calculations
        gross_salary = gross_salary_lakhs * 100000
        deductions = self.calculator.calculate_old_regime_deductions(gross_salary)

        print("\n🧾 Deduction Details:")
        total_deductions = 0
        for key, value in deductions.items():
            if key != 'total_deductions':
                deduction_lakhs = round(value / 100000, 2)
                print(f"{key.replace('_', ' ').title()}: ₹{deduction_lakhs} Lakhs")
                total_deductions += value

        print(f"\nTotal Deductions: ₹{round(total_deductions / 100000, 2)} Lakhs")

    def calculate_freelancer_tax_menu(self):
        """Interactive menu for calculating freelancer tax under Section 44ADA."""
        print(f"\n💼 Freelancer Tax Calculation - Section 44ADA ({self.calculator.current_regime.title()} Regime)")
        print("Note: This calculation assumes 50% of gross receipts as professional expenses.")

        gross_receipts_lakhs = self.get_numeric_input("Enter Gross Annual Receipts (₹ in Lakhs): ", min_val=0)

        result = self.calculator.calculate_freelancer_tax(gross_receipts_lakhs)

        print("\n📊 Income & Tax Breakdown:")
        labels = {
            "gross_receipts_lakhs": "Gross Receipts",
            "expense_deduction_lakhs": "Professional Expenses (50%)",
            "presumptive_income_lakhs": "Presumptive Income",
            "tax_lakhs": "Total Tax",
            "net_income_lakhs": "Net Annual Income",
            "monthly_take_home_lakhs": "Monthly Take-Home"
        }

        for key, value in result.items():
            if key in labels:
                print(f"{labels[key]}: ₹{value} Lakhs")

    def change_tax_regime(self):
        """Change the current tax regime."""
        print("\n🔄 Change Tax Regime")
        print("Current Regime:", self.calculator.current_regime.title())

        new_regime = 'new' if self.calculator.current_regime == 'old' else 'old'
        self.calculator.current_regime = new_regime

        print(f"Regime changed to {new_regime.title()} Tax Regime.")

    def run(self):
        """Main application loop."""
        while True:
            try:
                # Regime Selection
                self.display_regime_selection_menu()
                regime_choice = self.get_numeric_input("Enter your choice (1-3): ", int, 1, 3)

                if regime_choice == 3:
                    print("🚪 Exiting Tax Calculator. Goodbye! 👋")
                    sys.exit(0)

                # Set the current regime
                self.calculator.current_regime = 'old' if regime_choice == 1 else 'new'

                # Main Menu Loop
                while True:
                    self.display_main_menu()
                    choice = self.get_numeric_input("Enter your choice (1-6): ", int, 1, 6)

                    if choice == 1:
                        self.calculate_net_salary_menu()
                    elif choice == 2:
                        self.find_gross_salary_menu()
                    elif choice == 3:
                        self.detailed_deductions_menu()
                    elif choice == 4:
                        self.calculate_freelancer_tax_menu()
                    elif choice == 5:
                        self.change_tax_regime()
                    elif choice == 6:
                        break

                    input("\n📌 Press Enter to continue...")

            except KeyboardInterrupt:
                print("\n🚪 Exiting Tax Calculator. Goodbye! 👋")
                sys.exit(0)


def main():
    app = TaxCalculatorApp()
    app.run()


if __name__ == "__main__":
    main()
