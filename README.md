
# Project Title: Loan_Approval_Analysis

# Introduction

In this project, I worked on a loan approval dataset to understand how banks decide whether a person’s loan should be approved or rejected. The dataset contains information like applicant income, loan amount, credit history, education, marital status, property area, etc.
The main purpose of this project was to study the dataset properly, find useful patterns, and understand which factors affect loan approval the most.

# What I did in this project (Step-by-Step)
# 1. Checking and Handling Missing Values

First, I loaded the dataset and checked if there were any missing values. I used isnull().sum() to see which columns had null values.
I found missing values in columns like:

Gender
Married
Dependents
Self_Employed
LoanAmount
Loan_Amount_Term
Credit_History
To solve this, I filled missing values instead of deleting rows because deleting data could reduce dataset size.

✅ For categorical columns I filled with the most common value
Example:
Gender → Male
Married → Yes
Self_Employed → No

✅ For numerical columns I filled with common/mean values
Example:
LoanAmount → 128
Loan_Amount_Term → 360
Credit_History → 1
After this, the dataset became clean and ready for analysis.

# 2. Demographic Analysis

After cleaning the data, I explored demographic columns like:

Gender
Married
Dependents
Education
Self employed
From my analysis, I noticed that:

Married applicants had more approvals compared to unmarried.
Graduate applicants had a better approval rate than non-graduates.
People with fewer dependents had slightly better approval chances.
Self-employed applicants had a little lower approval rate compared to non self-employed.
So overall, demographic features affect loan approval, but they are not the strongest deciding factors.

# 3. Income and Loan Amount Analysis

Then I analyzed financial features like:

ApplicantIncome
CoapplicantIncome
LoanAmount
From this part I understood that
Applicants with higher income generally got more approvals.
Co-applicant income also helps in approval.
If loan amount is too high and income is not enough, chances of rejection increase.
So income plays an important role, but loan approval does not depend only on income. Other factors like credit history matter more.

# 4. Credit History and Loan Term Analysis

This was the most important part of my project.

I analyzed:
Credit_History
Loan_Amount_Term
From my results:

✅ Credit History had the biggest impact on loan approval.
Applicants with Credit_History = 1 were approved in most cases.
Applicants with Credit_History = 0 were mostly rejected.

For loan term, most people had a loan term of 360 months, and approvals were also high for this common term.
So I can say that credit history is the strongest factor in this dataset.

# 5. Property Area Analysis

Finally, I checked how property area affects loan approval. The dataset had:
Urban
Semiurban
Rural

From analysis:

Semiurban area had the highest loan approval rate.
Urban was in the middle.
Rural area had comparatively lower approvals.
This shows that location also affects loan approval chances.

# Final Conclusion (What I Learned)

After completing this project, I understood that loan approval depends on many features, but the most important factors are:

✅ Credit History (most important)
✅ Applicant Income and Co-applicant Income
✅ Loan Amount
✅ Property Area

Demographic features like gender, dependents, and self-employed status have some impact but not as strong as credit history.

Overall, this project helped me understand how to clean data, handle missing values, and perform EDA to find important insights from the dataset.
