# Step-1: Target mean strength
def calculate_target_mean_strength(fck, g):
    s_values = {'M20': 4, 'M25': 4, 'M30': 5, 'M35': 5, 'M40': 5, 'M45': 5}
    x_values = {'M20': 5.5, 'M25': 5.5, 'M30': 6.5, 'M35': 6.5, 'M40': 6.5, 'M45': 6.5}

    s = s_values[g]
    x = x_values[g]

    fck_1 = max(fck + 1.65 * s, fck + x)
    return fck_1

# Step-2: Water cement ratio
def calculate_water_cement_ratio(c_type, fck_1, s1, w):
    if c_type == 'OPC43':
        wcr_range = (0.25, 0.65)
        fck_range = (18, 65)
    elif c_type == 'OPC53':
        wcr_range = (0.25, 0.65)
        fck_range = (25, 74)
    else:
        raise ValueError("Invalid cement type")

    wc1 = (fck_1 - fck_range[0]) / (fck_range[1] - fck_range[0]) * (wcr_range[1] - wcr_range[0]) + wcr_range[0]

    w1_values = {'10mm': 208, '20mm': 186, '40mm': 165}
    w1 = w1_values[s1]

    w1_adjusted = w1 + 0.03 * ((w - 50) / 25) * w1

    return wc1, w1_adjusted

# Step-3: Cement content
def calculate_cement_content(w1, wc1, g):
    c2 = w1 / wc1

    if g > 'M20' and c2 > 320 and wc1 < 0.55:
        return c2
    else:
        raise ValueError("Invalid input parameters for cement content")

# Step-4: Volume of coarse and fine aggregate
def calculate_volume_of_aggregate(z1, s1, wc1):
    cav1_values = {'zone2': {'10mm': 0.5, '20mm': 0.62, '40mm': 0.71}}
    cav1 = cav1_values[z1][s1]

    if wc1 != 0.5:
        cav1 -= 0.01 * ((wc1 - 0.5) / 0.05)

    fa1 = 1 - cav1

    return cav1, fa1

# Step-5: Air content
def calculate_air_content(s1):
    air_content_values = {'10mm': 1.5, '20mm': 1, '40mm': 0.8}
    return air_content_values[s1]

# Step-6: Weight calculations
def calculate_weights(c2, sg1, a2, sg5, w1, s2, wc1, sg2, sg3):
    wa1 = 1 - (wc1 + w1 / 1000 + a2 * c2 / 100 / (sg5 * 1000) + s2 / 1000)
    wc1 = c2 / (sg1 * 1000)
    wad1 = (a2 * c2) / (sg5 * 1000 * 100)
    ww1 = w1 / 1000
    wag1 = 1 - (wa1 + wc1 + wad1 + ww1)
    wcag1 = wag1 * cav1 / 1000 * sg2 * 1000
    wfag1 = wag1 * fa1 / 1000 * sg3 * 1000

    return wa1, wc1, wad1, ww1, wcag1, wfag1

# Step-7: Total weight
def calculate_total_weight(c2, a2, w1, s2, sg2, sg3):
    weight_cement = c2
    weight_admixture = a2 * c2 / 100
    weight_water = w1
    weight_coarse_aggregate = wcag1 * wag1 * sg2 * 1000
    weight_fine_aggregate = wfag1 * wag1 * sg3 * 1000

    return weight_cement, weight_admixture, weight_water, weight_coarse_aggregate, weight_fine_aggregate

# Input values from the user
fck_input = input("Enter the grade of concrete required (e.g., M20, M25, etc.): ")
c_type_input = input("Enter the type of cement (OPC43 or OPC53): ")
s1_input = input("Enter the max nominal size of aggregates (10mm, 20mm, or 40mm): ")
e_input = input("Enter the exposure conditions (e.g., mild RCC): ")
w_input = input("Enter the workability (25mm, 50mm, 75mm, 100mm): ")
p1_input = input("Enter the method of concrete placing (e.g., chute): ")
a1_input = input("Enter the type of aggregate (e.g., crushed angular): ")
sg1_input = float(input("Enter the specific gravity of cement: "))
sg2_input = float(input("Enter the specific gravity of coarse aggregate: "))
sg3_input = float(input("Enter the specific gravity of fine aggregate: "))
sg4_input = float(input("Enter the specific gravity of water: "))
sg5_input = float(input("Enter the specific gravity of chemical admixture: "))
z1_input = input("Enter the zone of fine aggregate (e.g., zone 2): ")
a2_input = float(input("Enter the dosage of admixture (in percentage): "))

# Step-1: Target mean strength
fck_1 = calculate_target_mean_strength(int(fck_input[1:]), fck_input)

# Step-2: Water cement ratio
wc1, w1_adjusted = calculate_water_cement_ratio(c_type_input, fck_1, s1_input, int(w_input[:-2]))

# Step-3: Cement content
c2 = calculate_cement_content(w1_adjusted, wc1, fck_input)

# Step-4: Volume of coarse and fine aggregate
cav1, fa1 = calculate_volume_of_aggregate(z1_input, s1_input, wc1)

# Step-5: Air content
air_content = calculate_air_content(s1_input)

# Step-6: Weight calculations
wa1, wc1, wad1, ww1, wcag1, wfag1 = calculate_weights(c2, sg1_input, a2_input, sg5_input, w1_adjusted, int(s1_input[:-2]), wc1, sg2_input, sg3_input)

# Step-7: Total weight
weight_cement, weight_admixture, weight_water, weight_coarse_aggregate, weight_fine_aggregate = calculate_total_weight(c2, a2_input, w1_adjusted, int(s1_input[:-2]), sg2_input, sg3_input)

# Display results
print("\nConcrete Mix Design Results:")
print(f"Target Mean Strength (Fck'): {fck_1} N/mm^2")
print(f"Water-Cement Ratio (wc1): {wc1}")
print(f"Cement Content (c2): {c2} kg/m^3")
print(f"Volume of Coarse Aggregate (cav1): {cav1}")
print(f"Volume of Fine Aggregate (fa1): {fa1}")
print(f"Air Content: {air_content}%")
print("\nWeight Calculations:")
print(f"Weight of Cement: {weight_cement} kg")
print(f"Weight of Admixture: {weight_admixture} kg")
print(f"Weight of Water: {weight_water} kg")
print(f"Weight of Coarse Aggregate: {weight_coarse_aggregate} kg")
print(f"Weight of Fine Aggregate: {weight_fine_aggregate} kg")
