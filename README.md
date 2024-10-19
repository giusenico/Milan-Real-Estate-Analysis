# Milan Real Estate Market Analysis

## Project Overview
This project is an end-to-end data analysis of the real estate market in Milan, focusing on two key indices:
- **House Price Index (HPI)**
- **Housing Affordability Index (HAI)**

The goal of this analysis is to help real estate investors make informed decisions based on a detailed evaluation of Milan’s real estate market. We utilize data collection, analysis, and visualization through an interactive dashboard to explore trends across Milan’s macrozones.

## Project Structure
The repository contains the following components:
- **Data Collection**: Scripts and methods used to scrape and gather data from real estate websites.
- **Data Cleaning**: Jupyter notebooks for cleaning and preprocessing the data.
- **Analysis**: Scripts for calculating the HPI and HAI and performing exploratory data analysis (EDA).
- **Visualization**: Interactive Tableau dashboards that display the distribution of housing prices, affordability, and key real estate metrics.
- **Presentation**: PowerPoint slides summarizing the key insights and analysis.

## Key Features
1. **House Price Index (HPI) Calculation**:
   - The HPI measures price changes per square meter of residential properties in Milan’s different zones.
   - Formula:
     `HPI = (Current Price per sqm / Base Price per sqm) * 100`

2. **Housing Affordability Index (HAI) Calculation**:
   - The HAI measures the affordability of houses by comparing household income to the price of a median-priced home.
   - Formula:
     `HAI = (Median Household Income / Income Required to Buy Median-Priced House) * 100`

3. **Interactive Dashboard**:
   - A Tableau dashboard where users can filter properties by price range, typology, macrozone, and more, to explore real estate trends.

## Usage Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Milan-Real-Estate-Market-Analysis.git
2. Install dependencies:
   pip install -r requirements.txt
3. Explore the data and perform analysis through the provided Jupyter notebooks.
4. The Tableau dashboard can be accessed here: [View Dashboard on Tableau Public](https://public.tableau.com/app/profile/giuseppe.nicol./viz/RealEstate_17293237825170/InvestmentInsightsTheMilanRealEstateMarket).


## Project Deliverables
- Data & Analysis: All the scripts used for data collection, cleaning, and analysis.
- Slides: PowerPoint slides summarizing the analysis.
- Interactive Dashboard: Available on Tableau Public.

## Dependencies
- Python 3.x
- Pandas
- Tableau Public

## Author
Giuseppe Nicolò
