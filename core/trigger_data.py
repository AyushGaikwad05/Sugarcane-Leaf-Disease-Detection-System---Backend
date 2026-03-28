import json

SUGARCANE_TRIGGERS_JSON = """[
  {
    "category": "Disease",
    "name": "Rust",
    "trigger_conditions": "20C <= Temp <= 32C AND RH_I > 75% AND Rain > 0 mm",
    "priority": 1,
    "chemical_control": [
      {"chemical": "Mancozeb 0.30%", "dose_per_10L_water": "30 g"},
      {"chemical": "Tebuconazole 0.1%", "dose_per_10L_water": "10 ml"},
      {"chemical": "Azoxystrobin 18.2% + Difenoconazole 11.4% SC 0.1%", "dose_per_10L_water": "10 ml"}
    ],
    "notes": "Foliar spray on leaves"
  },
  {
    "category": "Disease",
    "name": "Smut",
    "trigger_conditions": "Max Temp > 35C AND RH_II < 40% AND Rain = 0 mm",
    "priority": 2,
    "chemical_control": [
      {"chemical": "Carbendazim 0.1%", "dose_per_10L_water": "10 g (seed treatment)"}
    ],
    "notes": "Seed treatment before sowing"
  },
  {
    "category": "Disease",
    "name": "Deficiencies",
    "trigger_conditions": "(Rain > 5 mm AND RH_I > 80%) OR (Rain = 0 AND Max Temp > 38C)",
    "priority": 2,
    "chemical_control": [
      {"chemical": "Carbendazim 0.1%", "dose_per_10L_water": "10 g (seed treatment)"},
      {"chemical": "Mancozeb 0.30% OR Carbendazim 0.1%", "dose_per_10L_water": "30 g OR 10 g"}
    ],
    "notes": "Treat based on observed deficiency symptoms; seed treatment and foliar spray recommended"
  },
  {
    "category": "Disease",
    "name": "Mawa (Mawa Disease / Grassy Shoot)",
    "trigger_conditions": "26C <= Temp <= 33C AND RH_I > 80% AND Sunshine < 7 hrs",
    "priority": 3,
    "biological_control": [
      {"agent": "Trichoderma + Pisolomyces", "dose": "50 g seed treatment AND soil application 20-25 kg/ha"}
    ],
    "notes": "Hot water seed treatment at 54C for 2.5 hours also effective"
  },
  {
    "category": "Disease",
    "name": "Pest infection (Mosaic + Early Rust)",
    "trigger_conditions": "25C <= Temp <= 32C AND 60% <= RH_I <= 80%",
    "priority": 4,
    "chemical_control": [
      {"chemical": "Mancozeb 0.30%", "dose_per_10L_water": "30 g"},
      {"chemical": "Tebuconazole 0.1%", "dose_per_10L_water": "10 ml"}
    ],
    "notes": "Combined mosaic (virus) and early rust infection"
  },
  {
    "category": "Pest",
    "name": "Borers (Stem/Shoot Borer)",
    "trigger_conditions": "Max Temp > 34C AND RH_II < 45% AND Rain = 0 mm",
    "priority": 1,
    "chemical_control": [
      {"chemical": "Chlorantraniliprole 0.4% granules", "dose": "18.75 kg mixed in sand and applied in soil"},
      {"chemical": "Fipronil 0.3% granules", "dose": "25 kg mixed in sand and applied in soil"}
    ],
    "notes": "Khodkid (stem borer) - apply granules in soil"
  },
  {
    "category": "Pest",
    "name": "Sugarcane Woolly Aphid (Lakshari Ali)",
    "trigger_conditions": "27C <= Temp <= 33C AND RH_I > 80%",
    "priority": 2,
    "chemical_control": [
      {"chemical": "Chlorantraniliprole 18.5% SC", "dose_per_10L_water": "4 ml spray"},
      {"chemical": "Emamectin Benzoate 5% SG", "dose_per_10L_water": "4 g spray"}
    ],
    "notes": "Foliar spray on affected plants"
  },
  {
    "category": "Pest",
    "name": "Pyrilla (Sugarcane Planthopper)",
    "trigger_conditions": "26C <= Temp <= 34C AND RH_I > 70% AND RH_II > 50%",
    "priority": 3,
    "chemical_control": [
      {"chemical": "Monocrotophos 36% SL", "dose_per_10L_water": "20 ml spray on crop"}
    ],
    "notes": "Monitor regularly during humid conditions"
  },
  {
    "category": "Pest",
    "name": "Termites",
    "trigger_conditions": "Max Temp > 35C AND RH_I < 60% AND Rain = 0 mm",
    "priority": 2,
    "chemical_control": [
      {"chemical": "Fipronil 0.3% granules", "dose": "25 kg mixed in soil"}
    ],
    "notes": "Soil application of granules at base of crop"
  },
  {
    "category": "Pest",
    "name": "White Grub",
    "trigger_conditions": "30C <= Temp <= 36C AND RH_I < 65% AND Rain < 2 mm",
    "priority": 3,
    "chemical_control": [
      {"chemical": "Fipronil 40% + Imidacloprid 40% WG", "dose": "4 g per 10L water, spray at base"}
    ],
    "notes": "Soil drench or granule application"
  },
  {
    "category": "Normal",
    "name": "No Disease / No Pest",
    "trigger_conditions": "Rain < 2 mm AND 40% <= RH_I <= 75% AND Temp < 34C",
    "priority": 5,
    "notes": "No disease/pest conditions met. Continue regular monitoring."
  }
]"""

def get_triggers():
    return json.loads(SUGARCANE_TRIGGERS_JSON)
