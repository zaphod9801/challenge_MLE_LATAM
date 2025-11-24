# Challenge Documentation

## Part I: Model Implementation

### Model Choice
I chose **Logistic Regression** over XGBoost for the following reasons:
1.  **Simplicity and Interpretability**: Logistic Regression is a linear model, making it easier to interpret feature importance and model behavior.
2.  **Requirements**: The `requirements.txt` file did not include `xgboost`, and while I could have added it, Logistic Regression provides a solid baseline with the available dependencies (`scikit-learn`).
3.  **Performance**: With class balancing (`class_weight='balanced'`), Logistic Regression performs adequately for this classification task, as observed in the notebook analysis.

### Implementation Details
-   **Feature Engineering**: Implemented `preprocess` method to generate features like `period_day`, `high_season`, and `min_diff`.
-   **One-Hot Encoding**: Used `pd.get_dummies` for categorical variables (`OPERA`, `TIPOVUELO`, `MES`).
-   **Feature Selection**: Restricted the model to the top 10 features identified in the notebook to reduce dimensionality and improve inference speed.
-   **Model Persistence**: The model is trained and saved to `challenge/model.joblib` to ensure the API can serve predictions without retraining on startup.

## Part II: API Development

### Framework
Used **FastAPI** for its speed, automatic validation, and documentation generation.

### Endpoints
-   `GET /health`: Returns the health status of the API.
-   `POST /predict`: Accepts a JSON payload with flight details and returns the predicted delay probability (0 or 1).

### Validation
Implemented strict validation using **Pydantic**:
-   `MES`: Must be between 1 and 12.
-   `TIPOVUELO`: Must be 'I' or 'N'.
-   `OPERA`: Must be one of the known airlines from the training data.
-   Invalid requests return a `400 Bad Request` status code.

## Part III: Cloud Deployment

### Strategy
The application is containerized using **Docker**. The `Dockerfile` is optimized for a Python environment.
For the challenge, the API was run locally using `uvicorn` and tested with `locust`.
In a real-world scenario, this Docker image would be deployed to a serverless platform like **Google Cloud Run** or **AWS Lambda** (with an adapter).

### Stress Testing
The API passed the stress test using `locust`, handling concurrent requests with acceptable latency.

## Part IV: CI/CD

### Workflows
Implemented GitHub Actions workflows in `.github/workflows`:
1.  **Continuous Integration (`ci.yml`)**:
    -   Triggers on push/pull_request to `main` and `develop`.
    -   Sets up Python environment.
    -   Installs dependencies.
    -   Runs `make model-test` and `make api-test`.
2.  **Continuous Delivery (`cd.yml`)**:
    -   Triggers on push to `main`.
    -   Builds the Docker image.
    -   (Simulated) Pushes the image to a container registry and deploys to the cloud provider.
