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
        """Calculate deductions for the Old Tax Regime."""
        basic_salary = salary * 0.5
        hra = salary * 0.4
        rent_paid = salary * 0.5

        section_80c = min(150000.0, basic_salary * 0.1)
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
        print("4. Change Tax Regime")
        print("5. Exit")
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
                    choice = self.get_numeric_input("Enter your choice (1-5): ", int, 1, 5)

                    if choice == 1:
                        self.calculate_net_salary_menu()
                    elif choice == 2:
                        self.find_gross_salary_menu()
                    elif choice == 3:
                        self.detailed_deductions_menu()
                    elif choice == 4:
                        self.change_tax_regime()
                    elif choice == 5:
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
