# Illustrative demo limits only. Do not use these values to make real-world crossing decisions.
LIMITS = {
    "pedestrian": 15,
    "two_wheeler": 20,
    "hatchback": 25,
    "suv": 35,
    "ambulance": 20,
}

def verdict(lo, hi, confidence, mode, flow="still"):
    if confidence < 0.45:
        return "UNKNOWN"
    limit = LIMITS.get(mode, 20)
    # Fast flow is treated more conservatively.
    if flow == "fast":
        limit *= 0.5
    elif flow == "slow":
        limit *= 0.8
    if lo >= limit:
        return "DO_NOT_CROSS"
    if hi >= limit or hi >= limit * 0.8:
        return "CAUTION"
    return "GO"
