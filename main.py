from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


# HARDCODED ANSWERS FOR DEMO
DEMO_ANSWERS = {
    "newton": {
        "book": """📖 **Source:** Physics Class 9 - Chapter 3: Dynamics
📚 **Subject:** Physics

**Newton's Laws of Motion:**

**First Law (Law of Inertia):**
A body at rest remains at rest, and a body in motion continues in motion with constant velocity unless acted upon by an external force. This law explains why passengers jerk forward when a bus suddenly stops.

**Formula:** ΣF = 0 (when object is at rest or moving with constant velocity)

**Second Law (Law of Acceleration):**
The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. This law helps us calculate the force needed to move objects.

**Formula:** F = ma
Where: F = Force (Newtons), m = mass (kg), a = acceleration (m/s²)

**Third Law (Action-Reaction Law):**
For every action, there is an equal and opposite reaction. When you push a wall, the wall pushes you back with equal force.

**Formula:** F₁₂ = -F₂₁""",
        "ai": "According to your Physics textbook: Newton gave three fundamental laws that explain motion. The first law states objects resist changes in motion (inertia). The second law (F=ma) shows how force, mass, and acceleration relate. The third law explains that forces always come in pairs - action and reaction are equal and opposite."
    },
    
    "osmosis": {
        "book": """📖 **Source:** Biology Class 9 - Chapter 2: Biological Molecules
📚 **Subject:** Biology

**Osmosis - Movement of Water Through Membranes:**

Osmosis is the movement of water molecules from a region of higher water concentration (dilute solution) to a region of lower water concentration (concentrated solution) through a semi-permeable membrane. This is a passive process that does not require energy.

**Real-Life Example:**
When you place a raisin in water, it swells up because water moves into the raisin through osmosis. Similarly, plant cells absorb water from soil through osmosis in their root hairs.

**Importance in Living Organisms:**
- Helps plants absorb water from soil
- Maintains water balance in animal cells
- Controls turgor pressure in plant cells
- Essential for kidney function in removing waste

**Types of Solutions:**
- Hypotonic: Less solute concentration (water enters cell)
- Hypertonic: More solute concentration (water leaves cell)
- Isotonic: Equal concentration (no net movement)""",
        "ai": "According to your Biology textbook: Osmosis is how water naturally moves through cell membranes from areas with more water to areas with less water. This process is crucial for plants absorbing water from soil and for maintaining proper water balance in all living cells. It happens without using energy."
    },
    
    "electrolysis": {
        "book": """📖 **Source:** Chemistry Class 9 - Chapter 5: Chemical Reactions
📚 **Subject:** Chemistry

**Electrolysis - Decomposition by Electric Current:**

Electrolysis is a chemical process in which electrical energy is used to bring about a non-spontaneous chemical reaction. It involves passing electric current through an ionic compound (either molten or dissolved in water) to decompose it into its elements.

**Process of Electrolysis:**
The substance being electrolyzed is called the electrolyte. It contains mobile ions that carry electric charge. When electricity passes through, positive ions (cations) move toward the negative electrode (cathode), while negative ions (anions) move toward the positive electrode (anode).

**Example - Electrolysis of Water:**
2H₂O(l) → 2H₂(g) + O₂(g)

When electric current passes through acidified water:
- Hydrogen gas is produced at the cathode (negative electrode)
- Oxygen gas is produced at the anode (positive electrode)
- Volume ratio: 2 volumes of H₂ : 1 volume of O₂

**Applications:**
- Extraction of metals like aluminum and sodium
- Purification of metals like copper
- Electroplating (coating objects with metal)
- Production of chemicals like chlorine and sodium hydroxide""",
        "ai": "According to your Chemistry textbook: Electrolysis uses electricity to break down compounds into simpler substances. For example, when you pass current through water, it splits into hydrogen and oxygen gases. This process is widely used in industry for metal extraction and purification."
    },
    
    "photosynthesis": {
        "book": """📖 **Source:** Biology Class 9 - Chapter 4: Bioenergetics
📚 **Subject:** Biology

**Photosynthesis - Food Production in Plants:**

Photosynthesis is the process by which green plants manufacture their own food (glucose) using carbon dioxide and water in the presence of sunlight and chlorophyll. This process occurs mainly in the leaves of plants.

**The Chemical Equation:**
6CO₂ + 6H₂O + Light Energy → C₆H₁₂O₆ + 6O₂
(Carbon dioxide + Water → Glucose + Oxygen)

**Requirements for Photosynthesis:**
1. **Chlorophyll** - Green pigment in chloroplasts that absorbs light
2. **Sunlight** - Provides energy for the reaction
3. **Carbon Dioxide** - Obtained from air through stomata
4. **Water** - Absorbed by roots from soil

**Two Stages of Photosynthesis:**

**Light Reaction (in thylakoid):**
Light energy is captured and converted to chemical energy (ATP). Water is split, releasing oxygen as a by-product.

**Dark Reaction (in stroma):**
Carbon dioxide is converted into glucose using the energy from light reactions. This can occur without direct light.

**Importance:**
- Produces food for all living organisms
- Releases oxygen necessary for respiration
- Removes carbon dioxide from atmosphere
- Source of all energy in food chains""",
        "ai": "According to your Biology textbook: Photosynthesis is how plants make food using sunlight, water, and carbon dioxide. The process happens in two stages in chloroplasts and produces glucose (food) and oxygen. The equation is: 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂. This is essential for all life on Earth."
    }
}


@app.get("/")
def root():
    return {
        "project": "AI Study Companion",
        "class": "9th Sindh Board",
        "status": "Running ✅"
    }


@app.post("/ask")
def ask(q: Question):
    question_lower = q.question.lower()
    
    # Check which question was asked
    if "newton" in question_lower or "law" in question_lower and "motion" in question_lower:
        response = DEMO_ANSWERS["newton"]
        found = True
    elif "osmosis" in question_lower:
        response = DEMO_ANSWERS["osmosis"]
        found = True
    elif "electrolysis" in question_lower:
        response = DEMO_ANSWERS["electrolysis"]
        found = True
    elif "photosynthesis" in question_lower:
        response = DEMO_ANSWERS["photosynthesis"]
        found = True
    else:
        # Default response for unknown questions
        response = {
            "book": "⚠️ This topic was not found in the 9th class Sindh Board syllabus. Please try asking about: Newton's Laws, Osmosis, Electrolysis, or Photosynthesis.",
            "ai": "Try asking questions from your Physics, Chemistry, or Biology textbooks for class 9."
        }
        found = False
    
    return {
        "book_answer": response["book"],
        "general_ai_answer": response["ai"],
        "context_found": found,
        "source": "Sindh Textbook Board"
    }