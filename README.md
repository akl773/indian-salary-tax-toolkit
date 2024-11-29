
# Indian Income Tax Calculator

## Overview
This Python application is a comprehensive tool for calculating Indian income tax based on both the **Old Tax Regime** and the **New Tax Regime**. It also includes features for determining the gross salary required to achieve a target take-home salary and provides detailed deductions for the Old Tax Regime.

## Features
1. **Tax Calculation**:
   - Calculate tax for both Old and New Tax Regimes.
2. **Net Salary Calculation**:
   - Determine net take-home salary after tax.
3. **Gross Salary Determination**:
   - Find gross salary required to achieve a target monthly take-home salary.
4. **Deductions Breakdown**:
   - Get detailed deductions for the Old Tax Regime.
5. **Interactive Menu**:
   - User-friendly CLI for selecting tax regime, calculating tax, and more.


## Usage
1. Select a tax regime (Old or New).
2. Choose an option from the main menu:
   - Calculate net salary
   - Find gross salary for a target take-home
   - View detailed deductions (Old Regime only)
   - Switch between tax regimes
3. Follow the on-screen prompts to enter salary details.

## File Details
- `IncomeTaxCalculator`: Main class handling tax slab definitions, deductions, and tax calculations.
- `TaxCalculatorApp`: CLI application for interacting with the user and performing calculations.

## Example
**Calculate Net Salary**
- Enter gross annual salary (in lakhs): 10
- View detailed results:
  - Gross Salary: ₹10 Lakhs
  - Total Deductions: ₹1.25 Lakhs
  - Taxable Income: ₹8.75 Lakhs
  - Total Tax: ₹0.95 Lakhs
  - Net Salary: ₹9.05 Lakhs
  - Monthly Take-Home: ₹0.75 Lakhs

**Switch Tax Regime**
- Select Old/New regime and calculate tax based on the selected slabs.

## Dependencies
- Python 3.x (Recommended: Python 3.8+)

## Keyboard Shortcuts
- Press `Ctrl+C` to exit the application at any time.

## License
This project is open-source and available under the MIT License.
