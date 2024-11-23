class SalaryMenu:
    def __init__(self, calculator):
        self.calculator = calculator

    def calculate_net_salary_menu(self):
        print(f"\n🔍 Net Salary Calculation ({self.calculator.current_regime.title()} Regime)")
        gross_salary_lakhs = float(input("Enter Gross Annual Salary (₹ in Lakhs): "))
        result = self.calculator.calculate_net_salary(gross_salary_lakhs)
        print("\n📊 Salary Breakdown:")
        for key, value in result.items():
            if key != 'deduction_details':
                print(f"{key.replace('_', ' ').title()}: ₹{value} Lakhs")

    def find_gross_salary_menu(self):
        print(f"\n💰 Gross Salary Determination ({self.calculator.current_regime.title()} Regime)")
        target_monthly_lakhs = float(input("Enter Target Monthly Take-Home Salary (₹ in Lakhs): "))
        result = self.calculator.find_gross_salary_for_target_take_home(target_monthly_lakhs)
        print("\n📊 Gross Salary Requirement:")
        for key, value in result.items():
            if key != 'deduction_details':
                print(f"{key.replace('_', ' ').title()}: ₹{round(value, 2)} Lakhs")
