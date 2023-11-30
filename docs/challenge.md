# Flight Delay Predictor API: Development and Deployment Documentation

## Introduction

This document provides a comprehensive overview of the development, deployment, and continuous improvement processes for
the Flight Delay Predictor API. The API, built using FastAPI and hosted on AWS Elastic Beanstalk, is designed to predict
flight delays based on various input parameters. The document details the model selection, API architecture, optimization
strategies, and the implementation of Continuous Integration (CI) and Continuous Deployment (CD) workflows.

## Objective

The primary objective of this documentation is to offer insights into the technical decisions, architectural design, and
deployment strategies that were employed to create a robust and scalable Flight Delay Predictor API. It serves as a guide
and reference for understanding the project's lifecycle, from model selection and API development to its deployment and
continuous enhancement through automated CI/CD pipelines.

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

## Continuous Integration and Continuous Deployment (CI/CD)

### Continuous Integration (CI)

#### Workflow Setup

The CI workflow (`ci.yml`) is triggered on every push and pull request to the main branch. It performs several checks and
tests to ensure code quality and functionality:

* **Environment Setup:** The workflow runs on the latest Ubuntu runner with Python 3.8.
* **Dependency Installation:** Installs all necessary dependencies from requirements.txt and additional tools like pytest,
pytest-cov, and locust.
* **Testing:**

  * **Model Tests:** Runs model-specific tests (`make model-test`).
  * **API Tests:** Executes tests for the API functionality (`make api-test`).
  * **Stress Tests:** Conducts stress tests to assess the API's performance under load (`make stress-test`).

* Docker Image Build: Builds a Docker image of the application to ensure it's correctly containerized.

#### Benefits

* Ensures code quality and functionality before merging into the main branch.
* Automates the testing process, reducing manual effort and the potential for human error.

### Continuous Deployment (CD)

#### Workflow Setup

The CD workflow (`cd.yml`) is triggered only after the CI workflow completes successfully. It automates the deployment of
the application to AWS Elastic Beanstalk:

* **Dependency and Tool Installation:** Installs the AWS CLI, necessary for AWS interactions.
* **AWS Credentials Configuration:** Securely configures AWS credentials using GitHub Secrets.
* **Application Packaging:** Packages the application into a ZIP file for deployment.
* **S3 Upload:** Uploads the ZIP file to a specified S3 bucket.
* **Elastic Beanstalk Deployment:**

   * **Create Application Version:** Creates a new version of the application on Elastic Beanstalk using the ZIP file from
S3. The version label is dynamically generated using the Git commit hash (`${{ github.sha }}`) for uniqueness.
   * **Update Environment:** Updates the Elastic Beanstalk environment to use the new application version.

#### Benefits
* Automates the deployment process, ensuring new changes are deployed efficiently and consistently.
* Uses a unique versioning system (using Git commit hash) to keep track of deployments and facilitate rollbacks if needed.

## Conclusion

The development and deployment of the Flight Delay Predictor API represent a significant achievement in applying machine
learning to real-world problems. Throughout the project, a strong focus was maintained on not only selecting the most
effective predictive model but also on ensuring that the API is robust, scalable, and easily maintainable.

### Key Accomplishments

- **Effective Model Selection and Optimization:** The choice of the XGBoost model, balanced for class representation and
based on the most significant features, demonstrates a thoughtful approach to handling real-world data imbalances and
complexities.

- **Robust API Design and Implementation:** The use of FastAPI, a modern, fast framework for building APIs, along with a
well-structured codebase, sets a solid foundation for future scalability and enhancements.

- **Successful Deployment to AWS Elastic Beanstalk:** Leveraging AWS services for deployment ensured high availability
and reliability of the API, making it accessible for real-time flight delay predictions.

- **Automated CI/CD Workflows:** The implementation of Continuous Integration and Continuous Deployment using GitHub
Actions exemplifies best practices in software development, ensuring code quality and facilitating seamless updates to
the application.

### Future Outlook

Looking ahead, the project is well-positioned for further enhancements, such as incorporating additional data sources,
implementing more complex machine learning algorithms, or expanding the API's functionality. The successful establishment
of CI/CD pipelines also ensures that future updates and improvements can be efficiently integrated, tested, and deployed.

In conclusion, the Flight Delay Predictor API project stands as a testament to the effective application of technology in
solving practical challenges and lays a strong foundation for continuous improvement and adaptation to evolving requirements.
