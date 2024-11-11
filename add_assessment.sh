#!/bin/bash

echo "Adding assessments and questions for each section of Network Security Fundamentals..."

# Run Django shell and execute the following commands
python manage.py shell <<EOF
from lms.models import Section, Assessment, Question  # Replace 'your_app' with the name of your Django app

# Define assessments with questions data for each section
assessments_data = {
    18: {
        "title": "Assessment about model evaluation.",
        "questions": [
                {"question": "What is the first step in data preprocessing?", "options": "Data Cleaning, Data Transformation, Feature Selection", "answer": "Data Cleaning", "marks": 5},
                {"question": "Which method is used for missing data?", "options": "Imputation, Removal, Duplication", "answer": "Imputation", "marks": 5},
                {"question": "What is overfitting?", "options": "When the model performs well on training data but poorly on unseen data, When the model performs well on both training and testing data", "answer": "When the model performs well on training data but poorly on unseen data", "marks": 5},
                {"question": "Which metric is used for classification models?", "options": "Accuracy, R-squared, MSE", "answer": "Accuracy", "marks": 5},
                {"question": "Which algorithm is used for classification?", "options": "KNN, Linear Regression, PCA", "answer": "KNN", "marks": 5},
                {"question": "What is feature scaling?", "options": "Normalizing data, Reducing data size, Changing data types", "answer": "Normalizing data", "marks": 5},
                {"question": "What is the purpose of cross-validation?", "options": "To tune hyperparameters, To evaluate model performance, To train models", "answer": "To evaluate model performance", "marks": 5},
                {"question": "What is a confusion matrix?", "options": "A matrix to evaluate classification performance, A matrix to evaluate regression models", "answer": "A matrix to evaluate classification performance", "marks": 5},
                {"question": "Which model is used for regression?", "options": "Linear Regression, KNN, Decision Tree", "answer": "Linear Regression", "marks": 5},
                {"question": "What does PCA stand for?", "options": "Principal Component Analysis, Preprocessing Component Analysis", "answer": "Principal Component Analysis", "marks": 5}
            ]
        }
}

# Iterate over each section, create assessments, and add questions
for section_id, assessment_data in assessments_data.items():
    try:
        section = Section.objects.get(id=section_id)
        assessment = Assessment.objects.create(section=section, title=assessment_data["title"])

        for question_data in assessment_data["questions"]:
            Question.objects.create(
                assessment=assessment,
                question=question_data["question"],
                options=question_data["options"],
                answer=question_data["answer"],
                marks=question_data["marks"]
            )

        print(f"Assessment and questions added to section {section_id}.")
    except Section.DoesNotExist:
        print(f"Section with ID {section_id} does not exist.")

print("All assessments and questions added successfully!")
EOF

echo "Assessments and questions have been successfully added to the specified sections."
