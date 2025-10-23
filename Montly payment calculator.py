from decimal import Decimal, getcontext, ROUND_HALF_UP

# Set precision for financial calculations
getcontext().prec = 15

class LoanCalculator:
    """A precise loan calculator using Decimal for financial accuracy"""

    def __init__(self, principal, annual_rate, years):
        """
        Initialize loan calculator
        Args:
            principal: Loan amount as string or Decimal
            annual_rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
            years: Loan term in years
        """
        self.principal = Decimal(str(principal))
        self.annual_rate = Decimal(str(annual_rate))
        self.years = int(years)
        self.monthly_rate = self.annual_rate / Decimal('12')
        self.total_payments = self.years * 12

    def calculate_monthly_payment(self):
        """Calculate monthly payment using precise decimal arithmetic"""
        if self.annual_rate == 0:
            return (self.principal / Decimal(str(self.total_payments))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        r = self.monthly_rate
        n = Decimal(str(self.total_payments))
        factor = (Decimal('1') + r) ** n
        monthly_payment = self.principal * (r * factor) / (factor - Decimal('1'))
        return monthly_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def generate_amortization_schedule(self):
        """Generate first few payments of amortization schedule"""
        monthly_payment = self.calculate_monthly_payment()
        balance = self.principal
        schedule = []

        for payment_num in range(1, min(13, self.total_payments + 1)):
            interest_payment = (balance * self.monthly_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            schedule.append({
                'payment': payment_num,
                'monthly_payment': monthly_payment,
                'interest': interest_payment,
                'principal': principal_payment,
                'balance': balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            })
        return schedule

    def total_interest_paid(self):
        """Calculate total interest over the life of the loan"""
        monthly_payment = self.calculate_monthly_payment()
        total_paid = monthly_payment * Decimal(str(self.total_payments))
        return (total_paid - self.principal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# Example usage
print("=== Loan Calculator Application ===")

loans = [
    {"principal": "250000", "rate": "0.045", "years": 30, "description": "30-year mortgage"},
    {"principal": "25000", "rate": "0.0675", "years": 5, "description": "5-year car loan"},
    {"principal": "50000", "rate": "0", "years": 10, "description": "Interest-free loan"}
]

for loan_data in loans:
    print(f"\n{loan_data['description']}:")
    print("-" * 50)
    calc = LoanCalculator(loan_data["principal"], loan_data["rate"], loan_data["years"])
    monthly = calc.calculate_monthly_payment()
    total_interest = calc.total_interest_paid()
    print(f"Loan Amount: ${calc.principal:,}")
    print(f"Monthly Payment: ${monthly}")
    print(f"Total Interest: ${total_interest:,}")
    print(f"Total Cost: ${calc.principal + total_interest:,}")

    # Show first 3 payments
    schedule = calc.generate_amortization_schedule()
    print(f"\nFirst 3 Payments:")
    print(f"{'Pmt':<5} {'Payment':<12} {'Interest':<12} {'Principal':<12} {'Balance':<12}")
    print("-" * 50)
    for payment in schedule[:3]:
        print(f"{payment['payment']:<5} "
              f"${payment['monthly_payment']:<11} "
              f"${payment['interest']:<11} "
              f"${payment['principal']:<11} "
              f"${payment['balance']:<11}")
