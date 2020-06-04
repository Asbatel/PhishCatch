# Welcome to PhishCatch

A framework for analysis and detection of phishing URLs using Ensemble Learning. We used 4 different classes of features:

- Format-based [9 features]
- Object-based [3 features]
- HTML and JS-based [4 features]
- Domain-based [3 features]

# Evaluation

Our framework has been evaluated against 50,000 recent URLs from <a href="https://www.phishtank.com/">Phishtank</a>. Our Maxvote-based approach yields an accuracy of 93.2%, which is nearly comparable to state-of-the-art techniques.
   
# Installation and Usage

To test a URL:
- Download or clone the repo (git clone https://github.com/Asbatel/PhishCatch.git)
- Navigate to the main directory `cd phishCatch/`
- Run the following command: `python check_url.py <url>`




