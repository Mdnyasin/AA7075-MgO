# Reproducing the AA7075/MgO yield-strength analysis

Keep the CSV and the Python script in the same directory. From that directory run:

```sh
python3 Reproduce-model.py
```

Python 3 is sufficient. The script uses only the standard library.

## Input data

Each row of Yield-data.csv represents one composition. MgO_wt_percent is the nominal MgO mass percentage and yield_strength_MPa is the reported composition-level yield strength in MPa. The first row (Control) fixes the recast matrix baseline at 98.0 MPa. The remaining rows (S1, S2, S3) are ordered by increasing MgO content. The script uses this row order.

## Fitting and output

Each fold fits the residual coefficient on two reinforced rows and predicts the third. The control is excluded from the pooled validation errors. The nominal calculation is printed first, followed by nine one-at-a-time sensitivity scenarios. Each line starts with the changed settings (an empty dictionary for the nominal calculation), followed by the full-fit coefficient in MPa, three fold coefficients in MPa, three held-out predictions in MPa, pooled MAE in MPa, pooled RMSE in MPa, and pooled R². The fold order is S1, S2, S3.

The nominal predictions are 126.85, 123.66 and 108.32 MPa. The pooled MAE is 4.70 MPa, RMSE is 4.92 MPa and R² is 0.730. The fitted response is yield strength. No individual tensile replicate data are represented in the CSV.
