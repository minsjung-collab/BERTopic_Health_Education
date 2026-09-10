# -*- coding: utf-8 -*-

# PubMed Data Collection for BERTopic Analysis
# Health Education & Health Promotion Journals, 2016-2025
# Reproducibility copy of the May 24, 2026 retrieval script.
# The original Entrez.email value has been replaced with a placeholder.

from Bio import Entrez, Medline
import pandas as pd
import numpy as np
import random
import time
import re
import os

random.seed(42)
np.random.seed(42)

# Replace with your own email as required by NCBI Entrez.
Entrez.email = "YOUR_EMAIL@example.com"

START_YEAR = 2016
END_YEAR = 2025
BATCH_SIZE = 100

OUTPUT_DIR = r"C:\Users\gigs1\Desktop\Health Education BERTopic"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_EXCEL = os.path.join(OUTPUT_DIR, "Health_Promotion_BERTopic_2016_2025.xlsx")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "Health_Promotion_BERTopic_2016_2025.csv")

JOURNALS = {
    "HEB": {"name": "Health Education & Behavior", "issn": "1090-1981"},
    "HER": {"name": "Health Education Research", "issn": "0268-1153"},
    "HPI": {"name": "Health Promotion International", "issn": "0957-4824"},
    "AJHP": {"name": "American Journal of Health Promotion", "issn": "0890-1171"},
}

def build_query(journal_issn):
    query = f'''\n    "{journal_issn}"[ISSN]\n    AND ("{START_YEAR}"[PDAT] : "{END_YEAR}"[PDAT])\n    AND hasabstract[text]\n    AND english[lang]\n    NOT (\n        editorial[pt]\n        OR comment[pt]\n        OR letter[pt]\n        OR news[pt]\n        OR biography[pt]\n        OR published erratum[pt]\n    )\n    '''
    return " ".join(query.split())

def search_pmids(query):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=50000, usehistory="y")
    record = Entrez.read(handle)
    handle.close()
    total = int(record["Count"])
    return record["WebEnv"], record["QueryKey"], total

def fetch_records(webenv, query_key, total):
    all_records = []
    for start in range(0, total, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total)
        print(f"Fetching records {start+1} - {end} / {total}")
        success = False
        while not success:
            try:
                handle = Entrez.efetch(
                    db="pubmed", rettype="medline", retmode="text",
                    webenv=webenv, query_key=query_key,
                    retstart=start, retmax=BATCH_SIZE
                )
                records = list(Medline.parse(handle))
                handle.close()
                all_records.extend(records)
                success = True
                time.sleep(1)
            except Exception as e:
                print(f"\nError: {e}")
                print("Retrying in 5 seconds...\n")
                time.sleep(5)
    return all_records

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'[^\w\s\-\.;,:()]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

SECTION_HEADERS = [
    "OBJECTIVE", "OBJECTIVES", "PURPOSE", "PURPOSES", "AIM", "AIMS",
    "CONCLUSION", "CONCLUSIONS", "IMPLICATION", "IMPLICATIONS",
    "PRACTICE IMPLICATIONS", "PUBLIC HEALTH IMPLICATIONS"
]
STOP_HEADERS = [
    "METHOD", "METHODS", "RESULT", "RESULTS", "DESIGN", "SETTING",
    "PARTICIPANTS", "INTERVENTION", "MEASURES", "ANALYSIS"
]

def extract_key_sections(text):
    if not text:
        return ""
    original_text = text
    text = re.sub(r'\s+', ' ', text)
    extracted_sections = []
    for section in SECTION_HEADERS:
        pattern = rf'{section}\s*:\s*(.*?)\s*(?=({"|".join(STOP_HEADERS + SECTION_HEADERS)})\s*:|$)'
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            content = match[0] if isinstance(match, tuple) else match
            content = content.strip()
            if len(content.split()) >= 5:
                extracted_sections.append(content)
    if extracted_sections:
        return clean_text(" ".join(extracted_sections))
    return clean_text(original_text)

def extract_doi(rec):
    doi = next((a.replace(" [doi]", "") for a in rec.get("AID", []) if "[doi]" in a), "")
    return doi.strip()

def parse_record(rec, journal_label):
    abstract_raw = rec.get("AB", "")
    if not abstract_raw:
        return None
    abstract_processed = extract_key_sections(abstract_raw)
    if len(abstract_processed.split()) < 30:
        return None
    title = clean_text(rec.get("TI", ""))
    authors = "; ".join(rec.get("AU", []))
    keywords = "; ".join(rec.get("OT", []))
    mesh_terms = "; ".join(rec.get("MH", []))
    dp = rec.get("DP", "")
    year_match = re.match(r'(\d{4})', dp)
    year = year_match.group(1) if year_match else ""
    month = dp[5:].strip() if len(dp) > 4 else ""
    doi = extract_doi(rec)
    title_only = title
    abstract_only = abstract_processed
    keywords_only = clean_text(keywords)
    combined_text = " ".join([part for part in [title_only, abstract_only, keywords_only] if part])
    combined_text = clean_text(combined_text)
    document_length = len(combined_text.split())
    return {
        "Journal": journal_label,
        "PMID": rec.get("PMID", ""),
        "DOI": doi,
        "Year": year,
        "Month": month,
        "Volume": rec.get("VI", ""),
        "Issue": rec.get("IP", ""),
        "Title": title,
        "Authors": authors,
        "AbstractRaw": abstract_raw,
        "AbstractProcessed": abstract_processed,
        "TitleOnly": title_only,
        "AbstractOnly": abstract_only,
        "KeywordsOnly": keywords_only,
        "AuthorKeywords": keywords,
        "MeSH": mesh_terms,
        "CombinedText": combined_text,
        "DocumentLength": document_length,
    }

print("\n========================================")
print("Health Promotion BERTopic Data Collection")
print("2016-2025")
print("========================================")

all_data = []
for label, journal_info in JOURNALS.items():
    journal_name = journal_info["name"]
    journal_issn = journal_info["issn"]
    print("\n========================================")
    print(f"{label} : {journal_name}")
    print("========================================")
    query = build_query(journal_issn)
    print("\nPubMed Query:")
    print(query)
    webenv, query_key, total = search_pmids(query)
    print(f"\nTotal records found: {total}")
    records = fetch_records(webenv, query_key, total)
    print(f"Downloaded records: {len(records)}")
    for rec in records:
        parsed = parse_record(rec, label)
        if parsed:
            all_data.append(parsed)

df = pd.DataFrame(all_data)
df = df.drop_duplicates(subset=["PMID"])
df = df.drop_duplicates(subset=["DOI"], keep="first")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df = df.sort_values(by=["Journal", "Year", "Volume", "Issue"])
df.to_excel(OUTPUT_EXCEL, index=False)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print("\n========================================")
print("Completed Successfully")
print("========================================")
print("\nRecords by Journal:")
print(df.groupby("Journal").size())
print("\nAverage Document Length:")
print(df.groupby("Journal")["DocumentLength"].mean())
print("\nTotal Final Records:")
print(len(df))
print(f"\nExcel saved: {OUTPUT_EXCEL}")
print(f"CSV saved: {OUTPUT_CSV}")
