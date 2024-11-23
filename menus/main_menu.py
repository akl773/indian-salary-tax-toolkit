import sys
from menus.salary_menu import SalaryMenu
from menus.freelancer_menu import FreelancerMenu
from calculator.income_tax_calculator import IncomeTaxCalculator

class MainMenu:
    def __init__(self):
        self.calculator = IncomeTaxCalculator()

    @staticmethod
    def display_regime_selection_menu():
        print("\n===== 🇮🇳 Indian Income Tax Calculator 📊 =====")
        print("Select Tax Regime:")
        print("1. Old Tax Regime")
        print("2. New Tax Regime")
        print("3. Exit")
        print("=" * 50)

    def display_main_menu(self):
        current_regime = self.calculator.current_regime.title()
        print(f"\n===== 🏦 {current_regime} Tax Regime Options 💼 =====")
        print("1. Calculate Net Salary")
        print("2. Find Gross Salary for Target Take-Home")
        print("3. Calculate Freelancer Tax (Section 44ADA)")
        print("4. Change Tax Regime")
        print("5. Exit")
        print("=" * 50)

    def change_tax_regime(self):
        print("\n🔄 Change Tax Regime")
        print("Current Regime:", self.calculator.current_regime.title())
        new_regime = 'new' if self.calculator.current_regime == 'old' else 'old'
        self.calculator.current_regime = new_regime
        print(f"Regime changed to {new_regime.title()} Tax Regime.")

    def run(self):
        while True:
            try:
                self.display_regime_selection_menu()
                regime_choice = int(input("Enter your choice (1-3): "))
                if regime_choice == 3:
                    print("🚪 Exiting Tax Calculator. Goodbye! 👋")
                    sys.exit(0)

                self.calculator.current_regime = 'old' if regime_choice == 1 else 'new'

                while True:
                    self.display_main_menu()
                    choice = int(input("Enter your choice (1-5): "))

                    if choice == 1:
                        SalaryMenu(self.calculator).calculate_net_salary_menu()
                    elif choice == 2:
                        SalaryMenu(self.calculator).find_gross_salary_menu()
                    elif choice == 3:
                        FreelancerMenu(self.calculator).calculate_freelancer_tax_menu()
                    elif choice == 4:
                        self.change_tax_regime()
                    elif choice == 5:
                        break

                    input("\n📌 Press Enter to continue...")

            except KeyboardInterrupt:
                print("\n🚪 Exiting Tax Calculator. Goodbye! 👋")
                sys.exit(0)
            except ValueError:
                print("❌ Invalid input. Please try again.")