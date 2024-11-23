class FreelancerMenu:
    def __init__(self, calculator):
        self.calculator = calculator

    def calculate_freelancer_tax_menu(self):
        print(f"\n💼 Freelancer Tax Calculation - Section 44ADA ({self.calculator.current_regime.title()} Regime)")
        gross_receipts_lakhs = float(input("Enter Gross Annual Receipts (₹ in Lakhs): "))
        result = self.calculator.calculate_freelancer_tax(gross_receipts_lakhs)
        print("\n📊 Income & Tax Breakdown:")
        for key, value in result.items():
            print(f"{key.replace('_', ' ').title()}: ₹{value} Lakhs")