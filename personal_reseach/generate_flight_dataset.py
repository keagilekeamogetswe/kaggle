#Generating a dataset
import csv
import random
import uuid
from datetime import datetime, timedelta

random.seed(42)

# Restricted Country Configuration
COUNTRIES = ["RSA", "USA", "France", "Germany", "Australia", "Nigeria", "Singapore"]

AIRLINES = {
    "RSA": ["South African Airways", "FlySafair"],
    "USA": ["Delta Air Lines", "United Airlines"],
    "France": ["Air France"],
    "Germany": ["Lufthansa"],
    "Australia": ["Qantas"],
    "Nigeria": ["Air Peace"],
    "Singapore": ["Singapore Airlines"]
}

NAMES = {
    "RSA": {"first": ["Thabo", "Siyabonga", "Zinhle", "Johan", "Anika", "Kagiso", "Lethabo", "Pieter"], "last": ["Khoza", "Dlamini", "Van der Merwe", "Ndlovu", "Smit", "Mokoena"]},
    "USA": {"first": ["Ethan", "Emma", "Liam", "Olivia", "Noah", "Ava", "Jackson", "Sophia"], "last": ["Smith", "Johnson", "Williams", "Brown", "Miller", "Davis"]},
    "France": {"first": ["Lucas", "Camille", "Hugo", "Manon", "Louis", "Chloe", "Gabriel", "Inès"], "last": ["Martin", "Bernard", "Thomas", "Petit", "Richard", "Dubois"]},
    "Germany": {"first": ["Maximilian", "Sophie", "Alexander", "Hannah", "Leon", "Mia", "Felix", "Lina"], "last": ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer"]},
    "Australia": {"first": ["Oliver", "Charlotte", "Jack", "Amelia", "William", "Isla", "Thomas", "Grace"], "last": ["Taylor", "Wilson", "White", "Harris", "Martin", "Thompson"]},
    "Nigeria": {"first": ["Emeka", "Chidimma", "Oluwaseun", "Zainab", "Babajide", "Nneka", "Tunde", "Amina"], "last": ["Okafor", "Balogun", "Adeleyi", "Okeke", "Obi", "Danfulani"]},
    "Singapore": {"first": ["Wei Ting", "Jun Jie", "Xian", "Mei Ling", "Ryan", "Cheryl", "Derrick", "Hui Ling"], "last": ["Tan", "Lim", "Lee", "Ng", "Ong", "Wong"]}
}

CLASSES = ["Economy", "Premium Economy", "Business", "First"]
CLASS_WEIGHTS = [0.70, 0.15, 0.12, 0.03]
TODAY = datetime(2026, 10, 1)

def get_dob(p_type):
    if p_type == "Infant":
        days = random.randint(30, 650)
    elif p_type == "Child":
        days = random.randint(2 * 365, 12 * 365)
    elif p_type == "Senior":
        days = random.randint(65 * 365, 80 * 365)
    else:
        days = random.randint(18 * 365, 60 * 365)
    return (TODAY - timedelta(days=days)).strftime("%Y-%m-%d")

dataset = []
row_count = 0

while row_count < 500:
    tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
    nationality = random.choice(COUNTRIES)
    last_name = random.choice(NAMES[nationality]["last"])

    dep_country = nationality
    arr_country = random.choice(COUNTRIES)
    is_domestic = (dep_country == arr_country)

    airline = random.choice(AIRLINES[dep_country])
    cabin_class = random.choices(CLASSES, weights=CLASS_WEIGHTS)[0]
    expiry = (TODAY + timedelta(days=random.randint(1, 14), hours=random.randint(1, 23))).strftime("%Y-%m-%d %H:%M")

    group_type = random.choices(["solo", "couple", "family_small", "family_large"], weights=[0.45, 0.25, 0.20, 0.10])[0]

    members = []
    if group_type == "solo":
        members.append(("Adult" if random.random() > 0.15 else "Senior", "M" if random.random() > 0.5 else "F"))
    elif group_type == "couple":
        members.extend([("Adult", "M"), ("Adult", "F")])
    elif group_type == "family_small":
        members.extend([("Adult", "M"), ("Adult", "F"), ("Child" if random.random() > 0.3 else "Infant", random.choice(["M", "F"]))])
    elif group_type == "family_large":
        members.extend([("Adult", "M"), ("Adult", "F"), ("Child", "M"), ("Child", "F")])
        if random.random() > 0.4:
            members.append(("Infant", random.choice(["M", "F"])))

    base_price = random.randint(120, 250) if is_domestic else random.randint(650, 1400)
    class_mult = {"Economy": 1.0, "Premium Economy": 1.5, "Business": 3.2, "First": 5.5}[cabin_class]

    for p_type, gender in members:
        if row_count >= 500:
            break

        ticket_id = f"TKT-{random.randint(10000000, 99999999)}"
        first_name = random.choice(NAMES[nationality]["first"])
        full_name = f"{first_name} {last_name}"
        dob = get_dob(p_type)

        age_mult = {"Adult": 1.0, "Senior": 0.90, "Child": 0.75, "Infant": 0.10}[p_type]
        final_price = round(base_price * class_mult * age_mult + random.uniform(-15, 15), 2)

        dataset.append({
            "full names": full_name,
            "gender": gender,
            "nationality": nationality,
            "date of birth": dob,
            "passanger type": p_type,
            "class": cabin_class,
            "airline": airline,
            "from": dep_country,
            "to": arr_country,
            "expiry": expiry,
            "ticket id": ticket_id,
            "transaction id": tx_id,
            "price": final_price
        })
        row_count += 1

headers = list(dataset[0].keys())
with open("flight.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(dataset)