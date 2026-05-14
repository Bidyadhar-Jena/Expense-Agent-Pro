CATEGORIES = {
    "food": ["swiggy", "zomato", "restaurant", "pizza", "burger"],
    "travel": ["uber", "ola", "metro", "bus"],
    "shopping": ["amazon", "flipkart", "myntra"],
    "gaming": ["steam", "playstation", "xbox"],
    "bills": ["wifi", "electricity", "recharge"]
}


def categorize_transaction(text):
    text = text.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "other"


def generate_insights(transactions):

    insights = []

    total = sum(t[1] for t in transactions)

    insights.append(f"💰 Total Spending: ₹{total}")

    category_total = {}

    for t in transactions:
        cat = t[2]
        category_total[cat] = category_total.get(cat, 0) + t[1]

    if category_total:
        top = max(category_total, key=category_total.get)
        insights.append(f"📊 Highest Spending Category: {top}")

    if category_total.get("food", 0) > total * 0.4:
        insights.append("⚠️ Warning: Food spending is very high!")

    if total > 5000:
        insights.append("🚨 You are crossing safe spending limits!")
