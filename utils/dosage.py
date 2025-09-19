# path: utils/dosage.py
def suggest_dose(drug_name: str, age: int, weight_kg: float | None = None):
    dn = drug_name.lower()
    if "paracetamol" in dn:
        if age < 12 and weight_kg:
            return f"Bolalar: {min(round(15*weight_kg),500)} mg, 4–6 soatda (≤60 mg/kg/kun)."
        return "Kattalar: 500–1000 mg, 4–6 soatda (≤4 g/kun)."
    return "Shifokor bilan maslahatlashing."
