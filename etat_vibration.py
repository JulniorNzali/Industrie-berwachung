def etat_vibration(v):
    if v < 3.0:
        return "Normal"
    elif v <= 5.0:
        return "Attention"
    else:
        return "Critique"
# Test avec les 3 valeurs
print(1.5, "→", etat_vibration(1.5))
print(4.2, "→", etat_vibration(4.2))
print(7.8, "→", etat_vibration(7.8))
