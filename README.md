# Udacity_ND_DataScientist_Project_4_Data_Scientist_Capstone_Pred_Mat_Reqs

## Motivation

This project is part of the **Udacity Data Scientist Nanodegree Capstone**.  
Goal: Optimize the Supply-to-Line process by analyzing material request patterns and predicting time between requests.

---

## Python Version
**Python 3.13.5**  
Ensure you use this version or higher for compatibility.

---

## Repository Structure

- `data/Peticiones_Demora_20251025.xlsx`: 1 Excel File of Transactional Data as example for 1 day.
*In the analysis, 27 files corresponding to 27 days were used.*

- `master_data/Parasum_iTLS.xlsx`: 1 Excel File of Master Data.

- `notebooks/Data_Scientist_Capstone_1_Prepare_and_Clean_Data.ipynb`: Jupyter Notebook for Data preparation and cleaning. 
*Result stored in SQL DB in `sql_db/`. Python version also included.* 

- `notebooks/Data_Scientist_Capstone_2_Analysis_and_Plots.ipynb`: Juypter Notebook for Exploratory analysis and visualizations.
*Python version also included.*

- `notebooks/Data_Scientist_Capstone_3_Pipeline_Python.ipynb`: Jupyter Notebook for Machine learning pipelines and predictions.
*Python version also included.*

- `report/Capstone_Project_Report.md`: Full project report.

- `sql_db/SPA_Data_Analytics.db`: SQLite database storing cleaned and prepared data.

---

## Libraries Used

- pandas, numpy, matplotlib

- scikit-learn

- sqlite3


## Installation
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>


python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

python --version
pip list


## How to Run

1. Place data files in `data/` and `master_data/` folders.

2. Run notebooks in order:

    Data_Scientist_Capstone_1_Prepare_and_Clean_Data.ipynb
    Data_Scientist_Capstone_2_Analysis_and_Plots.ipynb
    Data_Scientist_Capstone_3_Pipeline_Python.ipynb

    Or run Python scripts in the same order:
    python Data_Scientist_Capstone_1_Prepare_and_Clean_Data_Python_version.py
    python Data_Scientist_Capstone_2_Analysis_and_Plots_Python_version.py
    python Data_Scientist_Capstone_3_Pipeline_Python_version.py

## Results Summary

- Best model: RandomForest with GridSearchCV
    RMSE: 10.87 hours
    R²: 0.44

# Modeling Approach and Documentation

## 1. Dataset and Features
The dataset consists of material request records from the production process. Key features selected for prediction:
- **Consumo**: Median consumption parts per day.
- **Cap. Sumin**: Number of parts per container in each request.
- **Supply_time_hours**: Time taken to deliver material after request.

Target variable:
- **time_between_MatReqs**: Hours between consecutive material requests.

These features were chosen based on domain knowledge: they influence how frequently materials are requested.

---

## 2. Algorithms and Techniques
We implemented three regression models:

### **RandomForestRegressor**
- **Principle**: Ensemble of decision trees using bagging to reduce variance.
- **Why chosen**: Handles non-linear relationships and mixed feature types well.
- **Assumptions**: No strict linearity assumption; robust to outliers.

### **RandomForest with GridSearchCV**
- **Purpose**: Hyperparameter tuning to improve performance.
- **Parameters tuned**:
  - `n_estimators`: Number of trees (100, 200).
  - `max_depth`: Tree depth (None, 10, 20).
  - `min_samples_split`: Minimum samples to split (2, 5).
- **Reasoning**: These parameters control complexity and prevent overfitting.

### **GradientBoostingRegressor**
- **Principle**: Sequentially builds trees to reduce bias.
- **Why chosen**: Often performs better on small datasets by focusing on residual errors.

---

## 3. Metrics and Evaluation
We used:
- **RMSE (Root Mean Squared Error)**: Measures average prediction error in hours.
- **R² (Coefficient of Determination)**: Proportion of variance explained by the model.

| Model                     | RMSE (hours) | R²   |
|---------------------------|-------------|------|
| RandomForest              | 11.94       | 0.38 |
| RandomForest + GridSearch | 10.87       | 0.44 |
| GradientBoosting          | 11.20       | 0.41 |

**Interpretation**:
- Predictions are off by ~11 hours on average.
- Models explain less than half of variability (R² < 0.5), likely due to small dataset and high variability across PLPs (Production Line Points).

---

## 4. Challenges and Next Steps
- **Challenges**:
  - Small dataset (4 weeks) → limited generalization.
  - Outliers (e.g., weekend gaps).
  - High variability between PLPs.

- **Next Steps**:
  - Collect more data (>4 weeks).
  - Remove weekend outliers.
  - Group PLPs by similar characteristics.
  - Explore advanced models (XGBoost, Neural Networks).


## Acknowledgements

Thanks to all resources and references used during the project.
Special thanks to SEAT Supply-to-Line Inhouse team for their support

---

✅ This version is **Udacity-ready**:  
- Includes **Python version (3.13.5)**  
- Adds **installation instructions**  
- Mentions **Udacity context**  
- Keeps your detailed modeling documentation