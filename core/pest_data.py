import json

PEST_MANAGEMENT = [
  {
    "pest": "Stem Borer / Early Shoot Borer",
    "management": [
      "Use of Trichocards (Trichogramma chilonis) @ 5-6 cards/ha at an interval of 15 days",
      "Install ESB lure pheromone traps @ 5 traps/ha",
      "Soil application of Chlorantraniliprole 0.40% GR @ 18.75 kg or Fipronil 0.3% GR @ 25 kg per hectare",
      "Spraying of Chlorpyriphos 20% EC @ 25 ml or Chlorantraniliprole 18.5% SC @ 4 ml per 10 litre water"
    ]
  },
  {
    "pest": "Top Borer / Top Shoot Borer",
    "management": [
      "Use of Trichocards (Trichogramma chilonis) @ 5-6 cards/ha at an interval of 15 days during July to October",
      "Install TSB lure pheromone traps @ 5 traps/ha",
      "Soil application of Chlorantraniliprole 0.40% GR @ 18.75 kg in the furrows"
    ]
  },
  {
    "pest": "Internode Borer",
    "management": [
      "Use of Trichocards (Trichogramma chilonis) @ 5-6 cards/ha at an interval of 15 days during July to October",
      "Install INB lure pheromone traps @ 5 traps/ha"
    ]
  },
  {
    "pest": "Root Borer",
    "management": [
      "Use of Trichocards (Trichogramma chilonis) @ 5-6 cards/ha at an interval of 15 days",
      "Soil application Fipronil 0.3% GR @ 25 kg per ha or spray Fipronil 5% SC @ 1500-2000 ml per 500 litre water per hectare"
    ]
  },
  {
    "pest": "White Grub",
    "management": [
      "Install light traps @ 5 traps/ha",
      "Drenching of Heterorhabditis indica or Heterorhabditis bacteriophora @ 12.5 kg per 500 litre water at the time of early earthing up and 2 months after early earthing up",
      "Drenching of Fipronil 40% + Imidacloprid 40% WG @ 4 g per 10 litre water",
      "Soil application of Thiamethoxam 0.90% + Fipronil 0.20% GR @ 15 kg/ha"
    ]
  },
  {
    "pest": "Mealy Bug and Scale Insect",
    "management": [
      "Release of Cryptolaemus montrouzieri @ 1500 adults/ha for control of mealy bugs",
      "Spray Monocrotophos 36% SL @ 20 ml per 10 litre water"
    ]
  },
  {
    "pest": "Termites",
    "management": [
      "Soil drenching of Clothianidin 50% WDG @ 2.5 g per 10 litre water"
    ]
  },
  {
    "pest": "Pyrilla",
    "management": [
      "Release lepidopterous nymphal parasitoid, Epiricania melanoleuca @ 5,00,000 eggs or 5,000 pupae per hectare",
      "Spray Chlorpyrifos 20% EC @ 1500 ml per 500-1000 litre water or Acephate 50% + Imidacloprid 01.80% SP @ 2500 g per 500 litre water per hectare"
    ]
  },
  {
    "pest": "Woolly Aphid",
    "management": [
      "Release Dipha aphidivora 1,000 larvae or pupa or release Chrysoperla or Micromus @ 2,500 larvae per hectare at an interval of 15 days during August to October"
    ]
  }
]

PEST_MANAGEMENT_JSON = json.dumps(PEST_MANAGEMENT, indent=2)
