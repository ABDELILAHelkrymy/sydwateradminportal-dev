import os
from dotenv import load_dotenv
load_dotenv()

def export_environment_variables(request):
    data = {
        'INVOICE_URL': os.getenv("INVOICE_URL"),
        'API_URL': os.getenv("API_URL")
    }

    return data