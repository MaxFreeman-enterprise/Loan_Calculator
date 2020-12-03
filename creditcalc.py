import math
import argparse
import sys


def calculate_annuity_payment(nominal_interest_rate, number_of_payments, loan_principal):
    return (loan_principal * nominal_interest_rate * (1 + nominal_interest_rate) ** number_of_payments) / (
            (1 + nominal_interest_rate) ** number_of_payments - 1)


def calculate_nominal_interest_rate(annual_interest_rate):
    return annual_interest_rate / (100 * 12)


def calculate_number_of_payments(annuity_payment, nominal_interest_rate, loan_principal):
    return math.ceil(math.log(annuity_payment / (annuity_payment - nominal_interest_rate * loan_principal),
                              1 + nominal_interest_rate))


def calculate_loan_principal(annuity_payment, nominal_interest_rate, number_of_payments):
    return annuity_payment / ((nominal_interest_rate * (1 + nominal_interest_rate) ** number_of_payments) / (
            (1 + nominal_interest_rate) ** number_of_payments - 1))


def is_positive_or_none(value):
    return value is None or (isinstance(value, int) or isinstance(value, float)) and value >= 0


def calculate_differentiated_monthly_payment(loan_principal, nominal_interest_rate, number_of_payments,
                                             current_repayment_month):
    return loan_principal / number_of_payments + nominal_interest_rate * (
                loan_principal - loan_principal * (current_repayment_month - 1) / number_of_payments)


def display_loan_principal(annuity_payment, number_of_payments, annual_interest_rate):
    loan_principal = calculate_loan_principal(annuity_payment, calculate_nominal_interest_rate(annual_interest_rate),
                                              number_of_payments)

    print(f"Your loan principal = {int(loan_principal)}!")
    print(f"Overpayment = {math.ceil(annuity_payment * number_of_payments - loan_principal)}")


def display_payment(loan_principal, number_of_payments, annual_interest_rate):
    annuity_payment = math.ceil(
        calculate_annuity_payment(calculate_nominal_interest_rate(annual_interest_rate), number_of_payments,
                                  loan_principal))

    print(f"Your monthly payment = {annuity_payment}!")
    print(f"Overpayment = {math.ceil(annuity_payment * number_of_payments - loan_principal)}")


def display_number_of_payments(loan_principal, annuity_payment, annual_interest_rate):
    nominal_interest_rate = calculate_nominal_interest_rate(annual_interest_rate)

    number_of_payments = calculate_number_of_payments(annuity_payment, nominal_interest_rate, loan_principal)

    years = number_of_payments // 12
    months = number_of_payments % 12

    plural = "s" if months > 1 or months == 0 else ""

    if years > 0 and months > 0:
        print(f"It will take {years} years and {months} month{plural} to repay this loan!")

    elif years == 0:
        print(f"It will take {months} month{plural} to repay this loan!")

    elif months == 0:
        print(f"It will take {years} years to repay this loan!")

    else:
        pass
    print(f"Overpayment = {math.ceil(annuity_payment * number_of_payments - loan_principal)}")


def check_valid_arguments(args):

    if args.type is None or args.interest is None:
        print("Incorrect parameters")
        exit()

    elif args.type == "diff" and args.payment is not None:
        print("Incorrect parameters")
        exit()

    elif len(sys.argv) < 4:
        print("Incorrect parameters")
        exit()

    elif not is_positive_or_none(args.payment) or not is_positive_or_none(args.principal) \
            or not is_positive_or_none(args.periods) or not is_positive_or_none(args.interest):
        print("Incorrect parameters")
        exit()

    else:
        pass


def display_differentiated_payments(loan_principal, number_of_payments, annual_interest_rate):
    nominal_interest_rate = calculate_nominal_interest_rate(annual_interest_rate)
    total_paid = 0
    for i in range(1, number_of_payments + 1):
        current_payment = math.ceil(
            calculate_differentiated_monthly_payment(loan_principal, nominal_interest_rate, number_of_payments, i))
        print(f"Month {i}: payment is {current_payment}")
        total_paid += current_payment
    print()
    print(f"Overpayment = {math.ceil(total_paid - loan_principal)}")


#################################:main:###########################################


parse = argparse.ArgumentParser(usage="This program is a loan calculator")

parse.add_argument("--type", choices=["annuity", "diff"])
parse.add_argument("--payment")
parse.add_argument("--principal")
parse.add_argument("--periods")
parse.add_argument("--interest")

args = parse.parse_args()

if args.payment:
    args.payment = float(args.payment)

if args.principal:
    args.principal = float(args.principal)

if args.periods:
    args.periods = int(args.periods)

if args.interest:
    args.interest = float(args.interest)

check_valid_arguments(args)

if args.type == "annuity":

    if args.periods is None:
        display_number_of_payments(args.principal, args.payment, args.interest)

    elif args.payment is None:
        display_payment(args.principal, args.periods, args.interest)

    elif args.principal is None:
        display_loan_principal(args.payment, args.periods, args.interest)

    else:
        print("Incorrect parameters")

elif args.type == "diff":
    display_differentiated_payments(args.principal, args.periods, args.interest)

else:
    print("Incorrect parameters")
