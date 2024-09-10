import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  # Import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
def job(s):
    # Sample data for distinguishing true entry-level roles for fresh graduates
    data = {
        'job_description': [
            'You have programming experience. We work with Ruby / Rails, Typescript, React and Redux, and Python. However, languages can be learned: we care much more about your general engineering skill than knowledge of a particular language or framework',
            'Associate Web Developer position for recent graduates with 1-2 internships. Involves building and maintaining websites, requiring a Bachelor’s degree in Computer Science or related field and experience from coursework or personal projects.',
            'Junior Software Developer role requiring a recent Bachelor’s degree in Computer Science. Responsibilities include assisting with development tasks and learning from senior developers. Minimal prior professional experience needed.',
            'Entry-Level IT Analyst position with responsibilities for supporting IT systems and basic maintenance. Requires a recent degree in a related field and no prior professional experience.',
            'Associate Web Developer to help build and maintain websites. Requires a Bachelor’s degree in Computer Science or related field with experience through coursework or personal projects.',
            'Junior Data Analyst role focusing on data collection and analysis with support from senior analysts. Requires a recent degree in a quantitative field with some familiarity with data tools from coursework.',
            "Graduated in the last year with a Bachelor's or Master's degree in Computer Science or a related field, or are a bootcamp graduate with work experience or strong CS fundamentals.",
    "Experience with SQL, Java","A great attitude and desire for learning Excellent problem solving","learn and understand new technologies quickly",
    " a focus on learning and growth rather than extensive prior professional experience.'","0-1 years","2025","entry level",'Entry-level software developer position for recent Computer Science graduates. Involves working with Java, C++, Python, and SQL. Requires basic web development skills in React, HTML, and CSS. No prior professional experience required beyond internships or projects.',
            'Software Engineer intern position for recent graduates with experience in web technologies such as React and Flask. The role involves developing, testing, and optimizing applications. Requires good communication and problem-solving skills, with some experience through coursework or internships.',
            'Junior developer position with a focus on web development using React Native and AngularJS. Requires a Bachelor’s degree in Computer Science, but no prior work experience beyond personal projects or internships.',
            'Entry-level role for a data analyst with knowledge of SQL and data tools from coursework or projects. Open to fresh graduates with a Bachelor’s in Computer Science or a related field.',
            'Software development internship where you will work with technologies such as Docker, MongoDB, and Git. The position is designed for recent graduates or those with limited professional experience. Key skills include teamwork and problem-solving.',
        
    
            # Misleading Entry-Level for Fresh Graduates
            'Entry-Level Software Engineer position requiring 1 or more years of industry experience. Responsibilities include developing software and debugging, with a Bachelor’s degree in Computer Science required.',
            'Junior Systems Administrator role with responsibilities for maintaining IT systems and performing upgrades. Requires 1 year of relevant experience and a Bachelor’s degree in Computer Science or related field.',
            'Junior Data Scientist position requiring 1 or more years of professional experience in data science and an advanced degree preferred. Responsibilities include analyzing data and building models.',
            'Associate Software Developer role requiring 1 or more years of experience in software development. Responsibilities include maintaining code and designing solutions with strong technical skills beyond basic knowledge.',
            "Experience in infrastructure & systems level technologies: ",
            "5+ years experience",
            "4+ years of experience",
            "3+ years of experience",
            "2+ years of experience",
            "1+ years of experience",
        " 7-10 years of software development experience",
            'Junior Software Engineer role requiring 2+ years of professional experience in developing and maintaining complex software applications. Proficiency in full-stack development and extensive knowledge of JavaScript, Python, and SQL are mandatory.',
            'Entry-level software developer position requiring 1-3 years of experience working with C++ and SQL in a production environment. Responsibilities include design and deployment of large-scale systems.',
            'Junior Data Scientist role requiring a minimum of 1 year of industry experience in machine learning. Advanced knowledge of data science frameworks is preferred. A Master’s degree in a related field is a plus.',
            'Systems Engineer role requiring 1 year of experience with Docker, Kubernetes, and cloud technologies. Requires professional experience beyond academic projects or internships.',
            'Junior Full Stack Developer position requiring 1-2 years of professional experience in JavaScript, React, and Node.js. Applicants must have experience working on large, multi-tiered applications.',
            'Entry-level Software Engineer role that requires 2+ years of hands-on experience with Java and Spring Boot, working on large-scale enterprise systems.',
            'Junior Cloud Engineer role requiring a minimum of 1-2 years of experience managing cloud infrastructure (AWS, Azure). Strong DevOps knowledge required for CI/CD pipelines.',
            'Entry-level Data Engineer position demanding 1-3 years of professional experience with ETL processes and data warehousing. Proficiency in SQL and Python required.',
            'Junior Mobile Developer role requiring 1-2 years of experience in mobile development (iOS/Android) with knowledge of React Native and Swift.',
            'Entry-level Frontend Developer position requiring 1 year of professional experience working with JavaScript frameworks like AngularJS and React. Extensive knowledge of REST APIs is mandatory.',
            'Junior Security Analyst role requiring 2 years of hands-on experience in cybersecurity tools and penetration testing. Industry certifications such as CISSP or CEH are preferred.',
            'Software Engineer position requiring a Bachelor’s degree and at least 1 year of professional experience working with microservices architecture and containerization (Docker).',
            'Junior Product Manager role requiring 1 year of professional experience working with agile development teams. Must have experience in stakeholder communication and product lifecycle management.',
            'Junior AI Engineer role requiring 1-3 years of experience in developing machine learning models, with a strong understanding of TensorFlow and neural networks. A Master\'s degree is a plus.'
            
        ],
            'label': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]
    }
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Split data i

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['job_description'], df['label'], test_size=0.2, random_state=42)

    # Define a set of keywords that should penalize a job for not being truly entry-level
    experience_keywords = [
        'years of experience', '1+ years', '2+ years', 'industry experience', 'professional experience',
        'required experience', 'minimum of', 'prior experience', '3+ years', '4+ years'
    ]

    entry_level_indicators = [
        'internship', 'recent graduates', '0-1 years', 'entry-level', 'junior position', 'recent graduates', 
        'minimal experience', 'intern', 'co-op', 'no prior experience'
    ]

    # Custom tokenizer to include both experience and entry-level indicators
    def custom_tokenizer(text):
        # Split the text into words
        tokens = text.split()
        
        # Append any experience-related keywords found in the text
        tokens += [kw for kw in experience_keywords if kw.lower() in text.lower()]
        
        # Append any entry-level indicators found in the text
        tokens += [kw for kw in entry_level_indicators if kw.lower() in text.lower()]
        
        return tokens

    # Update the vectorizer with the custom tokenizer and stopword list for common, less useful words
    vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer, stop_words='english')

    # Create a pipeline with the vectorizer and a Naive Bayes model
    model = make_pipeline(vectorizer, ComplementNB())

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Print classification report
    print(classification_report(y_test, y_pred))

    # Applying stricter threshold for entry-level classification
    threshold = 0.8  # Adjust this threshold as needed
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    y_pred_thresholded = (y_pred_prob >= threshold).astype(int)

    # Print classification report based on the stricter threshold
    print("\nClassification report with stricter threshold:")
    print(classification_report(y_test, y_pred_thresholded))

    # Test with new input

    probs = model.predict_proba([s])[0]
    class_probabilities = dict(zip(model.classes_, probs))
    val=[]
    print("\nClass Probabilities for New Input:")
    for label, prob in class_probabilities.items():
        print(f"{label}: {prob:.2f}%")
        val.append(prob)

    # Print adjusted threshold result
    if val[1] >= val[0]:
        print("Classified as: Entry-level (1)")
        return  True
    else:
        print("Classified as: Not Entry-level (0)")
        return False