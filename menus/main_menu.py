from enum import Enum, auto
import sys
from typing import NoReturn
from menus.salary_menu import SalaryMenu
from menus.freelancer_menu import FreelancerMenu
from calculator.income_tax_calculator import IncomeTaxCalculator, TaxRegime


class MenuChoice(Enum):
    """Enumeration for main menu choices."""
    NET_SALARY = auto()
    FIND_GROSS = auto()
    FREELANCER = auto()
    CHANGE_REGIME = auto()
    EXIT = auto()


class RegimeChoice(Enum):
    """Enumeration for regime selection choices."""
    OLD = auto()
    NEW = auto()
    EXIT = auto()


class MainMenu:
    """Main menu handler for the Indian Income Tax Calculator."""

    def __init__(self) -> None:
        self.calculator = IncomeTaxCalculator()
        self._menu_handlers = {
            MenuChoice.NET_SALARY: self._handle_net_salary,
            MenuChoice.FIND_GROSS: self._handle_find_gross,
            MenuChoice.FREELANCER: self._handle_freelancer,
            MenuChoice.CHANGE_REGIME: self._handle_regime_change,
            MenuChoice.EXIT: self._handle_exit
        }

    @staticmethod
    def _print_decorated(text: str, char: str = "=", width: int = 50) -> None:
        """Print text with decorative borders."""
        print(f"\n{char * width}")
        print(text.center(width))
        print(char * width)

    def display_regime_selection_menu(self) -> None:
        """Display the tax regime selection menu."""
        self._print_decorated("🇮🇳 Indian Income Tax Calculator 📊")
        print("\nSelect Tax Regime:")
        print("1. Old Tax Regime")
        print("2. New Tax Regime")
        print("3. Exit")

    def display_main_menu(self) -> None:
        """Display the main options menu."""
        current_regime = self.calculator.current_regime.value.title()
        self._print_decorated(f"🏦 {current_regime} Tax Regime Options 💼")
        print("\n1. Calculate Net Salary")
        print("2. Find Gross Salary for Target Take-Home")
        print("3. Calculate Freelancer Tax (Section 44ADA)")
        print("4. Change Tax Regime")
        print("5. Exit")

    def _handle_net_salary(self) -> None:
        """Handle net salary calculation menu."""
        SalaryMenu(self.calculator).calculate_net_salary_menu()

    def _handle_find_gross(self) -> None:
        """Handle gross salary calculation menu."""
        SalaryMenu(self.calculator).find_gross_salary_menu()

    def _handle_freelancer(self) -> None:
        """Handle freelancer tax calculation menu."""
        FreelancerMenu(self.calculator).calculate_freelancer_tax_menu()

    def _handle_regime_change(self) -> None:
        """Handle tax regime change."""
        print("\n🔄 Change Tax Regime")
        print(f"Current Regime: {self.calculator.current_regime.value.title()}")
        new_regime = (TaxRegime.NEW if self.calculator.current_regime == TaxRegime.OLD
                      else TaxRegime.OLD)
        self.calculator.current_regime = new_regime
        print(f"Regime changed to {new_regime.value.title()} Tax Regime.")

    def _handle_exit(self) -> NoReturn:
        """Handle exit from the program."""
        print("\n🚪 Exiting Tax Calculator. Goodbye! 👋")
        sys.exit(0)

    def _get_user_choice(self, max_choice: int) -> int:
        """
        Get and validate user input.
        
        Args:
            max_choice: Maximum allowed choice number
            
        Returns:
            Validated user choice
        
        Raises:
            ValueError: If input is invalid
        """
        choice = input(f"\nEnter your choice (1-{max_choice}): ")
        if not choice.isdigit() or not 1 <= int(choice) <= max_choice:
            raise ValueError(f"Please enter a number between 1 and {max_choice}")
        return int(choice)

    def _process_regime_choice(self, choice: int) -> TaxRegime:
        """
        Process regime selection choice.
        
        Args:
            choice: User's regime selection
            
        Returns:
            Selected tax regime
            
        Raises:
            SystemExit: If exit is chosen
        """
        regime_choice = RegimeChoice(choice)
        if regime_choice == RegimeChoice.EXIT:
            self._handle_exit()
        return TaxRegime.OLD if regime_choice == RegimeChoice.OLD else TaxRegime.NEW

    def _process_menu_choice(self, choice: int) -> bool:
        """
        Process main menu choice.
        
        Args:
            choice: User's menu selection
            
        Returns:
            True if should continue, False if should exit to regime selection
        """
        menu_choice = MenuChoice(choice)
        if menu_choice == MenuChoice.EXIT:
            return False

        self._menu_handlers[menu_choice]()
        input("\n📌 Press Enter to continue...")
        return True

    def run(self) -> None:
        """Run the main menu loop."""
        while True:
            try:
                # Regime selection loop
                self.display_regime_selection_menu()
                regime_choice = self._get_user_choice(3)
                self.calculator.current_regime = self._process_regime_choice(regime_choice)

                # Main menu loop
                while True:
                    self.display_main_menu()
                    menu_choice = self._get_user_choice(5)
                    if not self._process_menu_choice(menu_choice):
                        break

            except KeyboardInterrupt:
                self._handle_exit()
            except ValueError as e:
                print(f"\n❌ {str(e)}")
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {str(e)}")
                print("Please try again.")
