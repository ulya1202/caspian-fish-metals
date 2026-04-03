"""
Shared constants, regulatory limits, and exposure parameters.
"""
import os

# paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# EU Regulation 2023/915 — maximum levels in fish muscle (µg/g ww)
EU_LIMITS = {"Pb": 0.30, "Cd": 0.05, "Hg": 0.50}

# US EPA IRIS oral reference doses (mg/kg-day)
RFD = {
    "Pb": 0.004, "Cd": 0.001, "Hg": 0.0001, "As": 0.0003,
    "Ni": 0.02,  "Cu": 0.04,  "Zn": 0.30,
}

# health risk parameters
EXPOSURE_FREQ = 365       # days/yr
EXPOSURE_DUR  = 30        # years
BODY_WEIGHT   = 70        # kg
AVG_TIME      = EXPOSURE_FREQ * EXPOSURE_DUR  # days

# consumption scenarios (g/day)
SCENARIOS = {
    "Azerbaijan (~1 kg/yr)":       2.74,   # ~1 kg/yr
    "Global average (20.7 kg/yr)": 56.7,   # FAO 2022
}

# metals with enough data for statistical testing (n >= 6)
TARGET_METALS = ["As", "Cd", "Cu", "Hg", "Ni", "Pb", "Zn"]

SEED = 42
