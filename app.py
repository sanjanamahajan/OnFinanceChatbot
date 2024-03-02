from flask import Flask, request, jsonify
from google.cloud import storage, bigquery
from transformers import AutoTokenizer
from openai import OpenAI
from google.oauth2 import service_account

# Initialize Flask app
app = Flask(__name__)

# Google Cloud credentials
PROJECT_ID = 'imperial-data-415815'
PATH_TO_JSON_KEY = 'imperial-data-415815-fd65740a544c.json'

# OpenAI API key
openai_api_key = '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'

# Route to handle incoming POST requests
@app.route("/chatbot", methods=['POST'])
def hello():
    # Extract question from request
    question = request.json['question']
    # Authenticate and generate response
    return authenticate_implicit_with_adc(question, PROJECT_ID)

# Authenticate with Google Cloud and process user question
def authenticate_implicit_with_adc(question, project_id):
    storage_client = storage.Client.from_service_account_json(PATH_TO_JSON_KEY, project=PROJECT_ID)
    buckets = storage_client.list_buckets()
    for bucket in buckets:
        print(bucket.name)
    blobs = storage_client.list_blobs("onfinacedata")
    for blob in blobs:
        print(blob.name)
    return write_read(question)

# Process user question and generate response
def write_read(question):
    # Initialize BigQuery client
    credentials = service_account.Credentials.from_service_account_file(PATH_TO_JSON_KEY,
                                                                         scopes=["https://www.googleapis.com/auth/cloud-platform"])
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # Query external data source
    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = ["gs://onfinacedata/Question_foramtted1.csv"]
    external_config.schema = [bigquery.SchemaField("question", "STRING"), bigquery.SchemaField("evidence_text", "STRING")]
    external_config.options.skip_leading_rows = 1
    table_id = "EvidenceData"
    question_text = question
    job_config = bigquery.QueryJobConfig(table_definitions={table_id: external_config})
    sql = 'SELECT evidence_text FROM `{0}` WHERE question LIKE "{1}"'.format(table_id, question_text)
    query_job = client.query(sql, job_config=job_config)
    w_states = list(query_job)

    # Generate response using OpenAI's GPT-3.5 model
    prompt = "Question: {0} Answer using Data: {1}".format(question_text, w_states)
    client = OpenAI(api_key=openai_api_key)
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    answer = completion.choices[0].message.content

    # Serialize response
    data = {"answer": answer}
    return jsonify(data)

# Default route
@app.route("/")
def index():
    return "Homepage of GeeksForGeeks"

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
