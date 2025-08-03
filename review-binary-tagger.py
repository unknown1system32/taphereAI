from transformers import pipeline
import csv

# Load zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)

INPUT_FILE = "reviews.csv"
OUTPUT_FILE = "reviews_tagged.csv"

CATEGORIES = {
    "HoReCa": ["fast service", "slow service", "friendly staff", "unfriendly staff",
               "good food quality", "bad food quality", "clean environment", "dirty environment",
               "good ambience", "noisy environment", "good value for money", "expensive",
               "would recommend", "would not recommend"],
    "Retail": ["fast service", "slow service", "friendly staff", "unfriendly staff",
               "good product quality", "poor product quality", "clean environment", "dirty environment",
               "good value for money", "expensive", "would recommend", "would not recommend"],
    "Services": ["fast service", "slow service", "friendly staff", "unfriendly staff",
                 "professionalism", "lack of professionalism", "good value for money", "expensive",
                 "would recommend", "would not recommend"]
}

def classify_text(text, labels):
    if not text or not labels:
        return {label: 0 for label in labels}
    results = classifier(text, labels)
    scores = {label: 0 for label in labels}
    for label, score in zip(results['labels'], results['scores']):
        scores[label] = 1 if score > 0.5 else 0
    return scores

def main():
    with open(INPUT_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        reviews = list(reader)

    if not reviews:
        print("No reviews found in the input file.")
        return

    output_fields = list(reviews[0].keys()) + ["category_label"] + list(set(sum(CATEGORIES.values(), [])))

    skipped = 0
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=output_fields)
        writer.writeheader()

        for idx, r in enumerate(reviews, start=1):
            text = r.get('text', '').strip()
            business_category = r.get('category', '').strip()
            labels = CATEGORIES.get(business_category, [])
            if not text or not labels:
                skipped += 1
                continue
            scores = classify_text(text, labels)
            r.update(scores)
            r['category_label'] = business_category
            writer.writerow(r)
            if idx % 100 == 0:
                print(f"Processed {idx}/{len(reviews)} reviews...")

    print(f"Tagged reviews saved to {OUTPUT_FILE}")
    print(f"Skipped {skipped} reviews (missing text or category).")

if __name__ == "__main__":
    main()