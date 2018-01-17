import os
import json

from decimal import Decimal

BASE_DIR = os.path.dirname(__file__)
TRANCHES_DIR = os.path.join(BASE_DIR, 'tranches')
tranches = list(filter(lambda x: x.endswith('.json'), os.listdir(TRANCHES_DIR)))

def ask_tranche(tranches):
    """
    Get the user to pick a tranche.
    """
    print("We support the following tranches, please select one.")
    print("To exit press CTRL+C")

    msg = ''
    for i, t in enumerate(tranches):
        msg += "[{}] {}\n".format(i, t)

    print(msg)

    res = -1
    while res >= len(tranches) or res < 0:
        res = input("Please select a number from above, default [0]: ")
        res = int(res) if res != '' else 0

    return tranches[res]

def ask_power_consumption():
    """
    Get power consumption from the user in kWh and for how many hours.
    """
    power = Decimal(input("Please specify the power consumed in kWh: "))
    hours = Decimal(input("Please specify how many hours to calculate consumption: "))
    return float(power * hours)

def calculate_tranche(tranche, consumption):
    """
    Calculate electricity bill portion of that electric consumption.
    """
    tranche = os.path.join(TRANCHES_DIR, tranche)
    with open(tranche, 'r') as fd:
        tranche = json.load(fd)

    name = tranche['name']
    bill = {'name': name}
    for tariff in reversed(tranche['tariff']): # highest to lowest tariff tranche
        trange, amount = tariff
        trange[1] = float("inf") if trange[1] < 0 else trange[1]

        if consumption >= trange[0]:
            tranche_kwh = consumption - trange[0] + 1
            bill[str(trange)] = [tranche_kwh, tranche_kwh * amount / 100]
            consumption -= tranche_kwh

    total = 0
    for tranche, amount in bill.items():
        if tranche == 'name':
            continue
        total += amount[1]
    bill['total'] = total

    return bill

def main():
    # Pick a tranche
    tranche = ask_tranche(tranches)

    # Get power consumption in kWh
    power = ask_power_consumption()

    bill = calculate_tranche(tranche, power)

    print()
    print("For the tranche {} your bill total is: {} EGP".format(
        bill['name'], bill['total']))
    print("Following is a break down of your bill:")

    for tranche, amount in bill.items():
        if tranche in ('name', 'total'):
            continue
        print("{}: {} kWh {} EGP".format(tranche, amount[0], amount[1]))

if __name__ == '__main__':
    main()
