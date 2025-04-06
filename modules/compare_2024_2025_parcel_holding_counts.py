import os
import pandas as pd
import matplotlib.pyplot as plt

# give me a python script that goes through a folder with csv files, and compares pairs of CSV files with "<gsa_code>_mar2025_ulm_extracted_sample" and "<gsa_code>_mar2025_simple_extracted_sample" substrings in their names. <gsa_code> is a country code - there are 2 files per country. so, we're comparing for example "mt_mar2025_ulm_extracted_sample" with "mt_mar2025_simple_extracted_sample" files and so on.

# for each pair, the function should compare the number of unique values in the gsa_par_id column. also it should compare the number of unique values in the gsa_hol_id column. the results can be stored in a dataframe and then saved as excel (one excel file for all countries)

# process the csv with pandas.


all_files = os.listdir('output/mar2025_analysis')

file_pairs = {}

for f in all_files:
    if 'mar2025' in f and f.endswith('.csv'):
        country_code = f.split("_")[0]
        if "ancient_extracted_sample" in f:
            if country_code not in file_pairs:
                file_pairs[country_code] = {"2024": f}
            else:
                file_pairs[country_code]["2024"] = f
        elif "simple_extracted_sample" in f:
            if country_code not in file_pairs:
                file_pairs[country_code] = {"2025": f}
            else:
                file_pairs[country_code]["2025"] = f


results = []

for country, files in file_pairs.items():
    print(country,files)
    ulm = pd.read_csv(f'output/mar2025_analysis/{files["2024"]}')
    simple = pd.read_csv(f'output/mar2025_analysis/{files["2025"]}')
    results.append(
        {
            "country": country,
            "2024_gsa_par_ids": ulm["gsa_par_id"].nunique(),
            "2025_gsa_par_ids": simple["gsa_par_id"].nunique(),
            "2024_gsa_hol_ids": ulm["gsa_hol_id"].nunique(),
            "2025_gsa_hol_ids": simple["gsa_hol_id"].nunique(),
        }
    )

# simple bar chart for comparisons - parcels

plt.figure(figsize=(15, 8))
x = [r["country"] for r in results]
y1 = [r["2024_gsa_par_ids"] for r in results]
y2 = [r["2025_gsa_par_ids"] for r in results]

bar_width = 0.3
index = range(len(x))
plt.bar(index, y1, bar_width, label="2024 parcel count", color='#f0ad29')
plt.bar([i + bar_width for i in index], y2, bar_width, label="2025 parcel count", color='#5bb033')
plt.xlabel("Country")
plt.ylabel("Unique values")
plt.title("Parcel count - 2024 ULM vs 2025 ULM")
plt.xticks([i + 1.5 * bar_width for i in index], x)

# add counts above columns

for i in index:
    plt.text(i, y1[i] + 0.1, y1[i], ha="center", color='#f0ad29')
    plt.text(i + bar_width, y2[i] + 0.1, y2[i], ha="center", color='#5bb033')

parcels_2024_count = sum(y1)
parcels_2025_count = sum(y2)

parcels_2024_average = parcels_2024_count / len(y1)
parcels_2025_average = parcels_2025_count / len(y2)

plt.axhline(y=parcels_2024_average, color='#f0ad29', linestyle='--', label=f"2024 average: {parcels_2024_average:.2f}")
plt.axhline(y=parcels_2025_average, color='#5bb033', linestyle='--', label=f"2025 average: {parcels_2025_average:.2f}")

plt.legend()


# simple bar chart for comparisons - holdings

plt.figure(figsize=(15, 8))
x = [r["country"] for r in results]
y1 = [r["2024_gsa_hol_ids"] for r in results]
y2 = [r["2025_gsa_hol_ids"] for r in results]

bar_width = 0.3
index = range(len(x))
plt.bar(index, y1, bar_width, label="2024 holding count", color='#f0ad29')
plt.bar([i + bar_width for i in index], y2, bar_width, label="2025 holding count", color='#5bb033')
plt.xlabel("Country")
plt.ylabel("Unique values")
plt.title("Holding count - 2024 ULM vs 2025 ULM")
plt.xticks([i + 1.5 * bar_width for i in index], x)

# add counts above columns

for i in index:
    plt.text(i, y1[i] + 0.1, y1[i], ha="center", color='#f0ad29')
    plt.text(i + bar_width, y2[i] + 0.1, y2[i], ha="center", color='#5bb033')

holdings_2024_count = sum(y1)
holdings_2025_count = sum(y2)

holdings_2024_average = holdings_2024_count / len(y1)
holdings_2025_average = holdings_2025_count / len(y2)

plt.axhline(y=holdings_2024_average, color='#f0ad29', linestyle='--', label=f"2024 average: {holdings_2024_average:.2f}")
plt.axhline(y=holdings_2025_average, color='#5bb033', linestyle='--', label=f"2025 average: {holdings_2025_average:.2f}")

plt.legend()


plt.show()



#results_df = pd.DataFrame(results)

#results_df.to_excel('output/mar2025_analysis/mar2025_analysis_results.xlsx', index=False)