# 📑 HomeMatch Model Report

## 🔹 Regression Results
- **Best Model:** XGB

### Metrics
| Model | RMSE | MAE | R² |
|-------|------|-----|----|
| Linear | 33294.8541 | 27378.7872 | 0.0619 |
| RF | 25059.3431 | 20034.1408 | 0.4686 |
| XGB | 25049.6220 | 20055.0808 | 0.4690 |
| Ensemble | 25987.2455 | 20576.5749 | 0.4285 |

### Plots
- [Residuals vs Predicted](../images/regression/residuals_vs_predicted.png)
- [Error Distribution](../images/regression/error_distribution.png)

## 🔹 Classification Results
- **Best Model:** RFC

### Metrics
| Model | F1 Score |
|-------|----------|
| Logistic | 0.8417 |
| RFC | 0.8425 |
| XGB | 0.8417 |
| Voting | 0.8417 |

### Plots
- [Confusion Matrix](../images/classification/confusion_matrix.png)
- [ROC Curve](../images/classification/roc_curve.png)
