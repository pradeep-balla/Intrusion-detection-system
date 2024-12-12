# Intrusion Detection System (IDS) Project

## Overview
This project is an Intrusion Detection System (IDS) designed to detect and classify network intrusions and anomalies. The goal of the project was to develop a system capable of analyzing network traffic data and accurately identifying potentially malicious activities using machine learning techniques.

## Dataset
The project utilized the NSL-KDD dataset, a well-known benchmark in the field of network security. The dataset consists of 43 features representing various aspects of network traffic, providing a rich source for analysis and classification tasks.

## Approach
1. **Feature Selection**:
   - Given the high dimensionality of the dataset, several feature selection techniques were applied to identify the most relevant features:
     - Mutual Information
     - Kendall Correlation
     - Principal Component Analysis (PCA)
   - A Venn diagram was used to visualize the overlap among the features selected by these methods.
   - A common set of 20 features, identified as the most relevant across all methods, was selected for further processing.

2. **Model Training**:
   - Multiple machine learning models were trained on the reduced feature set, including:
     - Logistic Regression
     - Decision Trees
     - K-Nearest Neighbors (KNN)
   - Through experimentation and performance evaluation, the KNN model emerged as the top-performing model for this task.

3. **System Development**:
   - A GUI-based website interface was developed to make the system user-friendly.
   - The interface allows users to input network traffic data based on the top 15 features selected from the feature selection process.
   - The integrated KNN model performs binary classification, predicting whether the network traffic is normal or indicative of an intrusion.

## Key Features
- **Feature Selection**: Comprehensive analysis and reduction of dataset dimensionality for improved performance.
- **Machine Learning Models**: Evaluation and comparison of multiple models to identify the best-performing approach.
- **User-Friendly GUI**: Intuitive interface for real-time classification of network traffic data.

## Results
The KNN model demonstrated superior performance in classifying network traffic data, making it the ideal choice for deployment in this IDS. The GUI-based interface enhances usability, enabling effective and efficient intrusion detection.

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ids-project.git
   cd ids-project
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the GUI application:
   ```bash
   python app.py
   ```
4. Input network traffic data into the interface to receive classification results.

## Future Work
- Integration with real-time network monitoring systems.
- Exploration of advanced machine learning models and techniques for improved detection accuracy.
- Extension to multi-class classification for categorizing different types of intrusions.

