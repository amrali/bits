def purchase_power(inflation, usdegp):
    """\
    Calculate the purchasing power given USD-EGP rate and inflation rate.

    Headline inflation shouldn't be used, we want to use the core inflation to
    arrive at a non-volatile purchasing power.
    """
    power = usdegp / (usdegp * (1 + inflation))
    return power

# Purchasing power before EGP floating and at USD-EGP conv rate back then
power_a = purchase_power(
        0.13, # Core inflation rate around Nov-2016
        8.8913) # USD-EGP conv rate around Nov-2016
print("Purchasing power before EGP floating at 8.8913 USD-EGP conv rate:", power_a)

# Purchasing power after EGP floating and at current USD-EGP conv rate
power_b = purchase_power(
        0.3, # Core inflation rate today Jul-2017
        17.83) # USD-EGP conv rate today Jul-2017
print("Purchasing power after EGP floating at 17.83 USD-EGP conv rate:", power_b)

print("Difference in purchasing power between the two periods:", power_b - power_a)
