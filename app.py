import requests 
import xml.etree.ElementTree as et
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe

"""
Basado en: https://stackoverflow.com/questions/62917910/python-export-pandas-dataframe-to-google-sheets-solved
"""

# ACCES GOOGLE SHEET
# gc = gspread.service_account(filename='api_credentials.json')
# sh = gc.open_by_key('1JcfrYwBVcYf7WSjZHknX7c2oLVSqf5nHixsmu89Mbq4')
# worksheet = sh.get_worksheet(0) #-> 0 - first sheet, 1 - second sheet etc.

# CLEAR SHEET CONTENT
# range_of_cells = worksheet.range('A1:J100000') #-> Select the range you want to clear
# for cell in range_of_cells:
#     cell.value = ''
# worksheet.update_cells(range_of_cells)

# APPEND DATA TO SHEET
# set_with_dataframe(worksheet, out_df) #-> THIS EXPORTS YOUR DATAFRAME TO THE GOOGLE SHEET

dataframe_total = pd.DataFrame()

"""
Basado en: https://medium.com/@robertopreste/from-xml-to-pandas-dataframes-9292980b1c1c
"""


countries = ["MDV", "AUS", "NOR", "USA", "CHL", "FRA"]

for country_id in range(len(countries)):
    print(f"Poblando: {countries[country_id]}")

    r = requests.get(f'http://tarea-4.2021-1.tallerdeintegracion.cl/gho_{countries[country_id]}.xml')


    root = et.fromstring(r.content)

    df_cols = ["GHO", "COUNTRY", "SEX", "YEAR", "GHECAUSES", "AGEGROUP", "Display", "Numeric", "Low", "High"]
    rows = []

    indicators = ["Number of deaths", "Number of infant deaths",
                  "Number of under-five deaths",
                  "Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)",
                  "Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)",
                  "Estimates of number of homicides",
                  "Crude suicide rates (per 100 000 population)",
                  "Mortality rate attributed to unintentional poisoning (per 100 000 population)",
                  "Number of deaths attributed to non-communicable diseases, by type of disease and sex",
                  "Estimated road traffic death rate (per 100 000 population)",
                  "Estimated number of road traffic deaths",
                  "Mean BMI (kg/m&#xb2;) (crude estimate)",
                  "Mean BMI (kg/m&#xb2;) (age-standardized estimate)",
                  "Prevalence of obesity among adults, BMI &GreaterEqual; 30 (age-standardized estimate) (%)",
                  "Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)",
                  "Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)",
                  "Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)",
                  "Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)",
                  "Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)",
                  "Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)",
                  "Estimate of daily cigarette smoking prevalence (%)",
                  "Estimate of daily tobacco smoking prevalence (%)",
                  "Estimate of current cigarette smoking prevalence (%)",
                  "Estimate of current tobacco smoking prevalence (%)",
                  "Mean systolic blood pressure (crude estimate)",
                  "Mean fasting blood glucose (mmol/l) (crude estimate)",
                  "Mean Total Cholesterol (crude estimate)"]


    for node in root:
        if node.find("GHO").text in indicators:
            s_gho = node.find("GHO").text if node.find("GHO") is not None else None
            s_country = node.find("COUNTRY").text if node.find("COUNTRY") is not None else None
            s_sex = node.find("SEX").text if node.find("SEX") is not None else None
            s_year = int(node.find("YEAR").text) if node.find("YEAR") is not None else None
            s_ghecauses = node.find("GHECAUSES").text if node.find("GHECAUSES") is not None else None
            s_agegroup = node.find("AGEGROUP").text if node.find("AGEGROUP") is not None else None
            s_display = node.find("Display").text if node.find("Display") is not None else None
            s_numeric = float(node.find("Numeric").text) if node.find("Numeric") is not None else None
            s_low = float(node.find("Low").text) if node.find("Low") is not None else None
            s_high = float(node.find("High").text) if node.find("High") is not None else None
            rows.append({"GHO": s_gho, "COUNTRY": s_country, "SEX": s_sex, "YEAR": s_year, "GHECAUSES": s_ghecauses, "AGEGROUP": s_agegroup, "Display": s_display, "Numeric": s_numeric, "Low": s_low, "High": s_high})

    out_df = pd.DataFrame(rows, columns = df_cols)
    dataframe_total = pd.concat([dataframe_total, out_df], axis=0)

"""
Basado en: https://stackoverflow.com/questions/62917910/python-export-pandas-dataframe-to-google-sheets-solved
"""
#
# # ACCES GOOGLE SHEET
gc = gspread.service_account(filename='api_credentials.json')
sh = gc.open_by_key('1JcfrYwBVcYf7WSjZHknX7c2oLVSqf5nHixsmu89Mbq4')
worksheet = sh.get_worksheet(0) #-> 0 - first sheet, 1 - second sheet etc.
#
# # CLEAR SHEET CONTENT
range_of_cells = worksheet.range('A1:J100000') #-> Select the range you want to clear
for cell in range_of_cells:
    cell.value = ''
worksheet.update_cells(range_of_cells)

# APPEND DATA TO SHEET
set_with_dataframe(worksheet, dataframe_total) #-> THIS EXPORTS YOUR DATAFRAME TO THE GOOGLE SHEET

# worksheet = sh.get_worksheet(6)  # -> 0 - first sheet, 1 - second sheet etc.
# set_with_dataframe(worksheet, out_df)
