# REST API for text summarization

This minimalistic HTTP REST Service can be used to store texts and corresponding summaries. The texts are stored in a SQL like database, for the summarization a pre-trained NLP model from the Huggingface library is used.

## Installation
1. Create a virtual environment.
2. Install dependencies from `requirements.txt`.


## Usage
1. Set `export FLASK_APP=application.py` and `export FLASK_DEBUG=True`
2. Start the app with `flask run`

- GET request on `/texts` lists all available texts in JSON format. Summaries are shown for texts that have been summarized by a separate request.
- GET request on `/texts/<id>` displays a single text with the corresponding ID and it's summary (if it has been created) in JSON format.
- POST request on `/texts` adds a new text to the database.
- DELETE request on `/texts/<id>` removes a single text with the corresponding ID.
- GET request on `/summary/<id>` creates a summary of the text with the corresponding ID and stores the summary in the database. If the summary has been created previously, the request returns the summary without calling the summarizer again.

## Testing the code and other TODO's
- TODO: Unit tests for different chunks of the API (Adding text, receiving a text, deleting a text, creating a summary)
- TODO: Test different models from huggingface and compare them, consider possible tradeoff between `goodness` of a summary and inference time
- TODO: Workaround for escape characters in a text
