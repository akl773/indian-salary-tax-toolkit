from decimal import Decimal
from typing import Any
from calculator.income_tax_calculator import IncomeTaxCalculator


class FreelancerMenu:
    """Menu handler for freelancer tax calculations."""

    def __init__(self, calculator: IncomeTaxCalculator):
        self.calculator = calculator

    @staticmethod
    def _format_currency(amount: Decimal | float) -> str:
        """Format currency in lakhs with proper separators."""
        amount_decimal = Decimal(str(amount))
        return f"₹{amount_decimal:,.2f}"

    @staticmethod
    def _get_validated_input() -> float:
        """Get and validate gross receipts input."""
        while True:
            try:
                amount = float(input("\n💰 Enter Gross Annual Receipts (₹ in Lakhs): "))
                if amount <= 0:
                    print("❌ Amount must be greater than 0")
                    continue
                if amount > 1000:
                    print("❌ Amount seems too high. Please verify (max 1000 Lakhs)")
                    continue
                return amount
            except ValueError:
                print("❌ Please enter a valid number")

    @staticmethod
    def _print_section_header(title: str) -> None:
        """Print a formatted section header."""
        print("\n" + "=" * 60)
        print(f"{title}".center(60))
        print("=" * 60)

    @staticmethod
    def _display_44ada_info() -> None:
        """Display information about Section 44ADA."""
        print("\n📌 Section 44ADA Benefits:")
        print("• 50% of gross receipts considered as expenses")
        print("• No need to maintain books of accounts")
        print("• Applicable for gross receipts up to ₹75 lakhs")
        print("• Professional services like consultancy, freelancing etc.")

    def _format_result_row(self, key: str, value: Any) -> str:
        """Format a single result row."""
        key_display = key.replace('_', ' ').title()
        if isinstance(value, (float, Decimal)):
            return f"{key_display:<30}: {self._format_currency(value)} Lakhs"
        return f"{key_display:<30}: {value}"

    def _display_results(self, result: dict) -> None:
        """Display calculation results in a formatted manner."""
        self._print_section_header("Income & Tax Breakdown")

        # Display main results
        for key, value in result.items():
            if key != 'deductions':  # Skip deductions for now
                print(self._format_result_row(key, value))

        # Calculate and display additional insights
        gross = Decimal(str(result["gross_receipts_lakhs"]))
        tax = Decimal(str(result["tax_lakhs"]))
        effective_tax_rate = (tax / gross * 100).quantize(Decimal("0.01"))

        print("\n📊 Key Insights:")
        print(f"• Effective Tax Rate: {effective_tax_rate}%")
        print(f"• Monthly Take Home: {self._format_currency(result['monthly_take_home_lakhs'])} Lakhs")

    def calculate_freelancer_tax_menu(self) -> None:
        """Handle the freelancer tax calculation menu flow."""
        try:
            # Display header and info
            self._print_section_header(
                f"Freelancer Tax Calculation - {self.calculator.current_regime_name} Regime"
            )
            self._display_44ada_info()

            # Get input and calculate
            gross_receipts_lakhs = self._get_validated_input()
            result = self.calculator.calculate_freelancer_tax(gross_receipts_lakhs)

            # Display results
            self._display_results(result)

        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or contact support if the issue persists.")
