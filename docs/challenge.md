Why did you select the model?

Based on the metrics, I selected **XGBoost model trained with the top 10 columns chosen by feature importance, with balance**. Here my reasons:

**Class Imbalance Handling:** The initial dataset is imbalanced, which generates a bias in favor of class 0.

```python
y_train.value_counts('%')*100

0    81.618452
1    18.381548

y_test.value_counts('%')*100

0    81.277768
1    18.722232
```

Even if we consider that the majority class is 0, the dataset is biased, and this is something that we must try to avoid. The balanced
XGBoost model addresses this issue by adjusting the weight of classes, which is crucial for achieving fair representation and performance across both classes.

**Improved recall for minority class:** The model significantly improves the recall for class 1 (69%) vs the other imbalanced models,
although this improvement comes at the cost of a lower precision for class 1 (52%), but considering the flight delays, it could be important to detect both cases.

```python
classification_report(y_test2, xgboost_y_preds_2)

              precision    recall  f1-score   support

           0       0.88      0.52      0.66     18294
           1       0.25      0.69      0.37      4214

    accuracy                           0.55     22508
   macro avg       0.56      0.61      0.51     22508
weighted avg       0.76      0.55      0.60     22508

```

**Feature Importance-Base Model Simplification:** Using the top 10 features based on feature importance
can lead to a simpler, more interpretable model. It also reduces the risk of overfitting by eliminating
less important features, and captures the necessary patterns from the more closely related information.

**Good metrics, in average:** Although the metrics look to lost precision in some cases, the model has a good performance in average,
and it is important to have a fair representation of both classes.
