# Sentiment Analysis Web App

The application returns a visualization displaying the probabilities of the text having a POSITIVE, NEGATIVE, NEUTRAL OR MIXED sentiment. <br>
The API request is handled by a AWS Lambda function, which processes the input text for AWS Comprehend, stores the input/output in an S3 bucket, calls the Comprehend method, and returns the sentiment score through the Gateway API.
