import os
import requests
import http.client
import json

def create_corpus(api_key , customer_id ,corpus_name,corpus_description):
    conn = http.client.HTTPSConnection("api.vectara.io")
    payload = json.dumps({
        "corpus": {
            "name": corpus_name,  # Replace with your actual corpus name
            "description": corpus_description,  # Optional
            "enabled": True,  # Optional
            "swapQenc": False,  # Optional
            "swapIenc": False,  # Optional
            "textless": False,  # Optional
            "encrypted": True,  # Optional
            "encoderId": 1,  # Optional, use integer
            "metadataMaxBytes": 0,  # Optional, use integer
            "customDimensions": [],  # Optional
            "filterAttributes": []  # Optional
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'customer-id': customer_id,  # Your customer ID
        'x-api-key': api_key  # Your API Key
    }
    conn.request("POST", "/v1/create-corpus", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    data_dict = json.loads(data.decode("utf-8"))
    corpus_number = data_dict["corpusId"]
    success_message = data_dict["status"]["statusDetail"]

    return corpus_number, success_message

def save_to_dir(uploaded_file):
  if uploaded_file is not None:
      temp_dir = "temp"
      os.makedirs(temp_dir, exist_ok=True)
      file_path = os.path.join(temp_dir, uploaded_file.name)

      with open(file_path, "wb") as f:
          f.write(uploaded_file.getbuffer())

      return file_path

  def upload_file(api_key, customer_id, corpus_number, file_path):
  url = f"https://api.vectara.io/v1/upload?c={customer_id}&o={corpus_number}"

  with open(file_path, "rb") as f:
      files = {
          "file": (os.path.basename(file_path), f),
      }

      headers = {"Accept": "application/json", "x-api-key": api_key}

      response = requests.post(url, headers=headers, files=files)

  return response.text


