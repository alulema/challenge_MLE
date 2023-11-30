## Model Selection and Implementation

### Model Selection: XGBoost with Top 10 Features and Class Balance

#### Reason for Selection

The chosen model is an XGBoost model trained with the top 10 features identified by feature importance, and with class
balance. The decision is based on the following considerations:

1. **Class Imbalance Handling**

    The dataset exhibited a significant class imbalance, favoring class 0. The imbalance ratios were as follows:

```python
y_train.value_counts('%')*100

0    81.618452
1    18.381548

y_test.value_counts('%')*100

0    81.277768
1    18.722232
```

To counteract this bias, the balanced XGBoost model adjusts the weight of classes, ensuring fair representation and more
accurate performance across both classes.

2. **Improved Recall for Minority Class**

   The balanced model demonstrated a substantial improvement in recall for class 1 (69%), essential for identifying delayed
flights. While this improvement impacted precision for class 1 (reducing it to 52%), the trade-off was deemed acceptable
considering the importance of accurately detecting delays.

```python
classification_report(y_test2, xgboost_y_preds_2)

              precision    recall  f1-score   support

           0       0.88      0.52      0.66     18294
           1       0.25      0.69      0.37      4214

    accuracy                           0.55     22508
   macro avg       0.56      0.61      0.51     22508
weighted avg       0.76      0.55      0.60     22508
```

3. **Feature Importance-Based Model Simplification**

   Utilizing only the top 10 features allows for a simpler, more interpretable model. This approach effectively captures
essential patterns with the most relevant information, reducing the risk of overfitting.

4. **Balanced Metrics**

   The model presents a balanced performance, offering a fair representation of both classes. This balance is crucial in
scenarios where both precision and recall are important.

## Model Deployment with FastAPI

The API's architecture has been structured to include middleware, services, and a comprehensive exception handling mechanism.
This organization enhances the modularity and readability of the code, making it more maintainable and scalable for future developments.

### Middleware and Exception Handling

**Exception Handling:** A robust exception handling mechanism has been implemented. Custom exception handlers have been
integrated to manage specific validation errors and custom exceptions related to business logic. This centralizes error
management, providing clearer error messages and improving the API's robustness.

**Service Layer:** The `ModelService` class encapsulates operations related to the `DelayModel`, including model initialization
and predictions. This service abstraction separates the model logic from the API routes, adhering to the Single Responsibility
Principle and enhancing the code's organization.

### Features and Functionalities

#### Model Initialization

**Automatic Model Initialization:** The ModelService class automatically initializes the `DelayModel` upon instantiation.
This involves loading data from a CSV file, preprocessing the data, and fitting the model.

**Data Loading:** Data for model initialization is loaded dynamically using the `Pathlib` and `glob` modules. This ensures
flexibility in file locations and enhances the API's adaptability to different deployment environments.

#### Prediction Endpoint

**Predictions:** The API includes a `/predict` endpoint that leverages the `ModelService` to make predictions. This endpoint
accepts a list of flights as input, processes the data, and returns predictions.

#### Request and Response Structure

**PredictionRequest DTO:** A Data Transfer Object (DTO), `PredictionRequest`, has been defined using Pydantic's `BaseModel`.
This DTO specifies the structure of the incoming prediction request, which includes a list of flights, each represented
as a dictionary.

### Custom Exception Handlers

- **ValidationError Handler:** Catches and handles validation errors arising from DTOs.
- **InvalidMonthValueException Handler:** Handles errors related to invalid 'MES' values in flight data.
- **InvalidTipoVueloValueException Handler:** Manages errors associated with incorrect 'TIPOVUELO' values.
- **General Exception Handler:** A catch-all handler for any other unanticipated exceptions, ensuring a graceful response
to unexpected issues.

### Code Organization and Best Practices

- **Separation of Concerns:** The application's structure adheres to the principle of separation of concerns, with distinct
layers for handling API routes, service logic, and exception handling.
- **Dependency Injection:** FastAPI's dependency injection system is used to manage instances of `ModelService`, enhancing
the flexibility and testability of the code.
- **Scalability and Maintainability:** The architectural choices and code organization strategies are geared towards
scalability and ease of maintenance, setting a solid foundation for future enhancements and expansions of the API.

## API Deployment and Optimization

### Deployment to AWS Elastic Beanstalk

#### Process Overview
The FastAPI application was containerized using Docker and deployed to AWS Elastic Beanstalk.

#### Key Steps

1. **Dockerization:** The application was packaged into a Docker container, which included all the necessary dependencies
and configurations.

2. **Elastic Beanstalk Configuration:**

   * An Elastic Beanstalk environment was set up to host the Docker container.
   * Configuration parameters, such as instance type, were adjusted to suit the application's needs.

3. **Deployment:**

   * The Docker container was deployed to the Elastic Beanstalk environment.
   * The application was made accessible via a URL provided by Elastic Beanstalk.

4. **Verification:** Post-deployment, the application was tested to ensure it was running correctly and accessible.

### ModelService Optimization

#### Saving and Loading Model

To enhance efficiency, the `ModelService` was optimized to save the trained model to a file using `joblib`. This approach
prevents the model from being retrained on every API call.

#### Implementation Details

* **Model Serialization:** The trained model is now serialized to a file upon the first training. If the saved model file
exists, it is loaded directly, bypassing the training process.
* **Joblib Integration:** The joblib library was used for model serialization due to its efficiency with large NumPy arrays,
which are common in machine learning models.

### Stress Testing
Post-deployment, stress tests were conducted to assess the application's performance under load. The application demonstrated:

* Stability: Consistent performance without significant degradation under simulated load.
* Responsiveness: Maintained acceptable response times throughout the testing period.
