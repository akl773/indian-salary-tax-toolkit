from decimal import Decimal
from typing import Any, Callable
from calculator.income_tax_calculator import IncomeTaxCalculator


class SalaryMenu:
    """Menu handler for salary-related tax calculations."""

    def __init__(self, calculator: IncomeTaxCalculator):
        self.calculator = calculator

    def _format_currency(self, amount: Decimal | float) -> str:
        """Format currency in lakhs with proper separators."""
        amount_decimal = Decimal(str(amount))
        return f"₹{amount_decimal:,.2f}"

    def _get_validated_input(self, prompt: str, min_value: float = 0.1,
                             max_value: float = 1000.0) -> float:
        """Get and validate numeric input within range."""
        while True:
            try:
                amount = float(input(prompt))
                if amount < min_value:
                    print(f"❌ Amount must be at least {self._format_currency(min_value)} Lakhs")
                    continue
                if amount > max_value:
                    print(f"❌ Amount cannot exceed {self._format_currency(max_value)} Lakhs")
                    continue
                return amount
            except ValueError:
                print("❌ Please enter a valid number")

    def _print_section_header(self, title: str) -> None:
        """Print a formatted section header."""
        print("\n" + "=" * 60)
        print(f"{title}".center(60))
        print("=" * 60)

    def _format_result_row(self, key: str, value: Any) -> str:
        """Format a single result row."""
        key_display = key.replace('_', ' ').title()
        if isinstance(value, (float, Decimal)):
            return f"{key_display:<30}: {self._format_currency(value)} Lakhs"
        return f"{key_display:<30}: {value}"

    def _display_results(self, result: dict, show_insights: Callable[[dict], None]) -> None:
        """Display calculation results in a formatted manner."""
        print("\n📊 Detailed Breakdown:")
        print("-" * 60)

        for key, value in result.items():
            if key != 'deduction_details':
                print(self._format_result_row(key, value))

        print("-" * 60)
        show_insights(result)

    def _show_net_salary_insights(self, result: dict) -> None:
        """Display insights for net salary calculation."""
        gross = Decimal(str(result["gross_salary_lakhs"]))
        tax = Decimal(str(result["tax_lakhs"]))
        net = Decimal(str(result["net_salary_lakhs"]))

        effective_tax_rate = (tax / gross * 100).quantize(Decimal("0.01"))
        savings_rate = ((gross - tax) / gross * 100).quantize(Decimal("0.01"))

        print("\n📈 Key Insights:")
        print(f"• Effective Tax Rate: {effective_tax_rate}%")
        print(f"• Take Home Percentage: {savings_rate}%")
        print(f"• Monthly Take Home: {self._format_currency(result['monthly_take_home_lakhs'])} Lakhs")

    def _show_gross_salary_insights(self, result: dict) -> None:
        """Display insights for gross salary determination."""
        gross = Decimal(str(result["gross_salary_lakhs"]))
        monthly_gross = gross / Decimal('12')
        tax = Decimal(str(result["tax_lakhs"]))

        print("\n📈 Key Insights:")
        print(f"• Required Monthly Gross: {self._format_currency(monthly_gross)} Lakhs")
        print(f"• Annual Tax Liability: {self._format_currency(tax)} Lakhs")
        print(f"• Tax Percentage: {(tax / gross * 100).quantize(Decimal('0.01'))}%")

    def calculate_net_salary_menu(self) -> None:
        """Handle the net salary calculation menu flow."""
        try:
            self._print_section_header(
                f"Net Salary Calculation - {self.calculator.current_regime_name} Regime"
            )

            print("\n💡 This calculation will:")
            print("• Compute your net salary after taxes")
            print("• Show monthly take-home amount")
            print("• Calculate effective tax rate")

            gross_salary_lakhs = self._get_validated_input(
                "\n💰 Enter Gross Annual Salary (₹ in Lakhs): ",
                min_value=0.1,
                max_value=1000.0
            )

            result = self.calculator.calculate_net_salary(gross_salary_lakhs)
            self._display_results(result, self._show_net_salary_insights)

        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or contact support if the issue persists.")

    def find_gross_salary_menu(self) -> None:
        """Handle the gross salary determination menu flow."""
        try:
            self._print_section_header(
                f"Gross Salary Determination - {self.calculator.current_regime_name} Regime"
            )

            print("\n💡 This calculation will:")
            print("• Find the gross salary needed for your desired take-home")
            print("• Show monthly and annual breakdowns")
            print("• Calculate tax implications")

            target_monthly_lakhs = self._get_validated_input(
                "\n🎯 Enter Target Monthly Take-Home Salary (₹ in Lakhs): ",
                min_value=0.1,
                max_value=100.0
            )

            print("\n⏳ Calculating required gross salary...")
            result = self.calculator.find_gross_salary_for_target_take_home(target_monthly_lakhs)
            self._display_results(result, self._show_gross_salary_insights)

        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or contact support if the issue persists.")