import pandas as pd
from pypdf import PdfReader

def document_extract(uploaded_file):
    file=uploaded_file.name.lower()
    if file.endswith(".pdf") :
        reader=PdfReader(uploaded_file)

        text=""

        for page in reader.pages:
            extracted=page.extract_text()

            if extracted:
                text += extracted + "\n"

        return text
    
    elif file.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    elif file.endswith(".csv"):
       
       df =pd.read_csv(uploaded_file)
       return df.to_string(index=False)
    
    else:

        return ""
    
