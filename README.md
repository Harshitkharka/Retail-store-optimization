# Retail Store Optimization: Optimizing Retail Promotions

## Project Overview
This repository contains the analysis and report for a retail optimization project aimed at enhancing promotional strategies for a multi-city retail chain. The project evaluates the effectiveness of promotions, identifies profitable products and categories across seasons, assesses customer responses, and analyzes revenue drivers by store type and payment method.

## Business Problem
The retail chain operates various store formats (Warehouse Club, Specialty Store, Department Store, Pharmacy) and runs promotions and discounts. However, uncertainties exist regarding:
- Which promotions drive sales effectively.
- The most profitable products/categories in each season.
- Customer category responses (e.g., Young Adults, Homemakers, Professionals) to promotions.
- Store types and payment methods that generate higher revenue.

## Objectives
Management seeks to:
- Boost seasonal sales while minimizing expenditure on ineffective promotions.
- Customize product offerings by city and season.
- Enhance store type performance by aligning with customer demand.

## Key Findings
- **Promotion Effectiveness**: Discounts on Selected Items yield the highest uplift (up to 5.15%) for Professionals in Warehouse Clubs and Pharmacies. BOGO promotions perform well (approximately 4%) for Teenagers in Convenience Stores.
- **Product and Seasonal Trends**: Toothpaste is the top performer across seasons with consistent profit margins (~1.30M). Groceries dominate sales (~27M per season), with seasonal highlights like Ice Cream in Summer and Oranges in Winter.
- **Customer Responses**: Professionals show high responsiveness to discounts; Teenagers prefer BOGO. Moderate uplifts observed for Homemakers and Senior Citizens.
- **Store and Payment Analysis**: Revenue is balanced across store types and payment methods (e.g., Cash, Credit Card), each contributing uniformly (~80 units on a normalized scale).

## Recommendations
- Prioritize targeted promotions: Discounts for Professionals and BOGO for Teenagers to avoid low-impact campaigns.
- Tailor inventories seasonally and by city, emphasizing Groceries and high-margin items.
- Align store formats with customer segments (e.g., bulk items in Warehouse Clubs for Professionals) and promote mobile payments for convenience.
- Projected impact: 3-5% increase in seasonal sales through optimized resource allocation.

## Data and Methodology
- Data sourced from a PostgreSQL retail transaction dataset.
- Analysis includes uplift calculations relative to non-promotion baselines; profit margins exclude external costs.

For further details, refer to the full report (`Retail optimization report.pdf`) in this repository or contact the analytics team.
