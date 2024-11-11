#!/bin/bash

echo "Adding assessments and questions for section 18 of Network Security Fundamentals..."
python manage.py shell <<EOF
from lms.models import Course, Section, Lesson, Assessment, Question

# Assuming course is already defined, if not define it by name or ID
course = Course.objects.get(title="Network Security Fundamentals")

# Get section 18 by title or any other unique identifier
section_18 = Section.objects.filter(course=course, title="Section 18 Title").first()  # Replace with actual title or identifier of section 18

if section_18:
    # Define lessons data
    lesson_data = [
        {
            'title': 'Assessment for Section 18',
            'content_type': 'assessment',
            'content': '',
            'duration': 0  # Or set duration if needed
        }
    ]

    # Create lessons and assessments for section 18
    for lesson in lesson_data:
        # Create lesson
        lesson_instance = Lesson.objects.create(
            section=section_18,
            title=lesson['title'],
            content_type=lesson['content_type'],
            content=lesson['content'],
            duration=lesson['duration']
        )
        print(f"Lesson '{lesson_instance.title}' added to section '{section_18.title}'.")

        # If the lesson is an assessment, create questions
        if lesson['content_type'] == 'assessment':
            # Create assessment
            assessment = Assessment.objects.create(
                section=section_18,
                title=lesson['title'],
                is_active=True
            )
            print(f"Assessment '{assessment.title}' added to section '{section_18.title}'.")

            # Define questions for this assessment
            questions_data = [
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

            # Add questions to the assessment
            for q in questions_data:
                Question.objects.create(
                    assessment=assessment,
                    question=q['question'],
                    options=q['options'],
                    answer=q['answer'],
                    marks=q['marks']
                )
                print(f"Question '{q['question']}' added to assessment '{assessment.title}'.")
else:
    print("Section 18 not found!")
EOF

echo "Assessment and questions for section 18 have been successfully added."
