#!/bin/bash

echo "Adding assessment for section 36 with 10 questions..."

# Run Django shell and execute the following commands
python manage.py shell <<EOF
from lms.models import Section, Assessment, Question  # Replace 'lms' with the name of your Django app

# Define assessment and questions for section 36
try:
    section = Section.objects.get(id=36)
    
    # Create assessment for section 36
    assessment = Assessment.objects.create(
        section=section,
        title="Assessment: Model Evaluation Techniques",
    )

    # Define questions for the assessment
    questions_data = [
        {"question": "Cross-validation helps to avoid overfitting.", "options": "True, False", "answer": "True", "marks": 5},
        {"question": "Confusion matrix is used only for regression models.", "options": "True, False", "answer": "False", "marks": 5},
        {"question": "Which metric is commonly used for classification models?", "options": "Accuracy, R-squared, MSE", "answer": "Accuracy", "marks": 5},
        {"question": "What is the purpose of cross-validation?", "options": "To tune hyperparameters, To evaluate model performance, To train models", "answer": "To evaluate model performance", "marks": 5},
        {"question": "Which model evaluation metric is suitable for regression?", "options": "Precision, Recall, R-squared", "answer": "R-squared", "marks": 5},
        {"question": "Precision and recall are metrics used for classification models.", "options": "True, False", "answer": "True", "marks": 5},
        {"question": "ROC curve is useful to evaluate which type of model?", "options": "Regression, Classification", "answer": "Classification", "marks": 5},
        {"question": "Which metric is not typically used in model evaluation?", "options": "Accuracy, F1 Score, Mean Squared Error, Standard Deviation", "answer": "Standard Deviation", "marks": 5},
        {"question": "A high accuracy always means a good model.", "options": "True, False", "answer": "False", "marks": 5},
        {"question": "Which method can help in handling imbalanced data?", "options": "Cross-validation, Resampling techniques, Normalization", "answer": "Resampling techniques", "marks": 5}
    ]

    # Add questions to the assessment
    for question_data in questions_data:
        Question.objects.create(
            assessment=assessment,
            question=question_data["question"],
            options=question_data["options"],
            answer=question_data["answer"],
            marks=question_data["marks"]
        )

    print("Assessment with questions added to section 36.")
except Section.DoesNotExist:
    print("Section with ID 36 does not exist.")

print("Assessment and questions have been successfully added.")
EOF

echo "Assessment has been successfully added to section 36."
