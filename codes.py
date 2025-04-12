# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 18:28:12 2025
Author: HP
"""




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



file_path = "C:\\Users\\HP\\OneDrive\\Desktop\\fnsdjsd\\Accidental_Drug_Related_Deaths_2012-2023.xlsx"
df = pd.read_excel(file_path)

# cleaning starts from here

# Clean column names: lowercase, no spaces or dashes
df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('-', '_').str.lower()

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Convert 'date' to datetime format
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Drop columns with more than 30% missing data
df = df.loc[:, df.isnull().mean() < 0.3]

# Fill missing values
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna(df[col].mode()[0])  # Fill with most frequent value
    else:
        df[col] = df[col].fillna(df[col].median())   # Fill with median

# Standardize 'sex' and 'race' entries
df['sex'] = df['sex'].str.upper().replace({'M': 'MALE', 'F': 'FEMALE'})
df['race'] = df['race'].str.upper().str.strip()

# Remove rows with invalid age values
df = df[(df['age'] > 0) & (df['age'] <= 120)]
df.reset_index(drop=True, inplace=True)

#charts 

# 1. Monthly Drug-Related Deaths (Line Plot)
if 'date' in df.columns:
    monthly_trend = df['date'].dt.to_period('M').value_counts().sort_index()
    monthly_trend.plot(kind='line', marker='o', figsize=(12, 6), color='darkblue')
    plt.title('Monthly Drug-Related Deaths')
    plt.xlabel('Month')
    plt.ylabel('Number of Deaths')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 2. Gender-wise Death Count (Bar Chart)
df['sex'].value_counts().plot(kind='bar', color=['#1f77b4', '#ff7f0e'], edgecolor='black')
plt.title('Deaths by Gender')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 3. Top 5 Races Involved (Horizontal Bar Chart)
df['race'].value_counts().head(5).plot(kind='barh', color='darkorange', edgecolor='black')
plt.title('Top 5 Races Involved in Deaths')
plt.xlabel('Number of Deaths')
plt.tight_layout()
plt.show()

# 4. Manner of Death (Pie Chart)
if 'manner_of_death' in df.columns:
    df['manner_of_death'].value_counts().plot(
        kind='pie',
        autopct='%1.1f%%',
        startangle=140,
        colors=sns.color_palette('pastel'),
        wedgeprops={'edgecolor': 'black'}
    )
    plt.title('Manner of Death')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

# 5. Age Distribution (Histogram)
plt.hist(df['age'].dropna(), bins=30, color='mediumslateblue', edgecolor='black')
plt.title("Age Distribution of Deceased Individuals")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 6. Age Distribution by Gender (Boxplot)
sns.boxplot(data=df, x='sex', y='age', palette='Set2')
plt.title("Age Distribution by Gender")
plt.xlabel("Gender")
plt.ylabel("Age")
plt.tight_layout()
plt.show()

# 7. Year-wise Drug Death Trends (Line Plot)
if 'date' in df.columns:
    yearly_trend = df['date'].dt.year.value_counts().sort_index()
    yearly_trend.plot(kind='line', marker='o', figsize=(10, 5), color='green')
    plt.title('Yearly Trend of Drug-Related Deaths')
    plt.xlabel("Year")
    plt.ylabel("Number of Deaths")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 8. Top Location Types (Bar Plot)
if 'location' in df.columns:
    loc_counts = df['location'].value_counts().head(8)
    sns.barplot(x=loc_counts.values, y=loc_counts.index, palette='mako')
    plt.title("Top Locations Where Deaths Occurred")
    plt.xlabel("Number of Deaths")
    plt.ylabel("Location")
    plt.tight_layout()
    plt.show()
