from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2 import service_account
from flask import Flask, render_template, request, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load Google Sheets API credentials with proper scopes
credentials = service_account.Credentials.from_service_account_file(
    r'C:\Users\atinu\OneDrive\Documents\Billing Key\billing-automation-422823-55c587437e41.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)

# Authorize the client
client = gspread.authorize(credentials)

# Open the Google Sheets document
spreadsheet = client.open('Python Automation')

# Dictionary to map sheet names to their respective routes
sheet_routes = {
    "QRx Variance Bill": "qrx-variance",
    "PPMV Variance Bill": "ppmv-variance",
    "QRx Close-Out Bill": "qrx-close-out",
    "PPMV Close-Out Bill": "ppmv-close-out"
}

# Function to fetch data from multiple worksheets
def fetch_worksheet_data(worksheets):
    data = {}
    for sheet_name in worksheets:
        sheet = spreadsheet.worksheet(sheet_name)
        data[sheet_name] = sheet.get_all_records()
    return data

# Route for index page
@app.route('/')
def index():
    try:
        print("Loading index page...")
        return render_template('index.html')

    except Exception as e:
        # Handle any exceptions
        error_message = f"An error occurred: {str(e)}"
        print("Error:", error_message)
        return render_template('error.html', error_message=error_message)

# Route for processing form submission
@app.route('/process', methods=['POST'])
def process():
    try:
        # Get the selected billing type from the form
        selected_billing_type = request.form.get('billing-type')

        # Get the route associated with the selected billing type
        route = sheet_routes.get(selected_billing_type)

        if route:
            # Redirect to the selected route
            return redirect(url_for(route))
        else:
            return render_template('error.html', error_message="Invalid billing type selected")

    except Exception as e:
        # Handle any exceptions
        error_message = f"An error occurred: {str(e)}"
        print("Error:", error_message)
        return render_template('error.html', error_message=error_message)

# Route for QRx Variance Bill page
@app.route('/qrx-variance')
def qrx_variance():
    try:
        if request.method == 'POST':
            # Store the uploaded files in session
            session['supply_data'] = request.files['supply_data'].read().decode('utf-8')
            session['withdrawal_data'] = request.files['withdrawal_data'].read().decode('utf-8')
            session['dispensation_data'] = request.files['dispensation_data'].read().decode('utf-8')
            session['pricing_file'] = request.files['pricing_file'].read().decode('utf-8')
            if 'last_count_data' in request.files:
                session['last_count_data'] = request.files['last_count_data'].read().decode('utf-8')
            if 'buyout_data' in request.files:
                session['buyout_data'] = request.files['buyout_data'].read().decode('utf-8')
            # Redirect to another page or perform analysis
            
        # Fetch data from specified worksheets
        worksheet_data = fetch_worksheet_data(["QRx VDL", "Category Mapping", "QRx Facilities"])
        
        # Logic for QRx Variance Bill page
        qrx_vdl_data = worksheet_data.get("QRx VDL")
        category_mapping_data = worksheet_data.get("Category Mapping")
        qrx_facilities_data = worksheet_data.get("QRx Facilities")

        # Example usage of worksheet data
        return render_template('qrx_variance.html', 
                               qrx_vdl_data=qrx_vdl_data, 
                               category_mapping_data=category_mapping_data, 
                               qrx_facilities_data=qrx_facilities_data)

    except Exception as e:
        # Handle any exceptions
        error_message = f"An error occurred: {str(e)}"
        print("Error:", error_message)
        return render_template('error.html', error_message=error_message)

# Route for PPMV Variance Bill page
@app.route('/ppmv-variance')
def ppmv_variance():
    try:
        # Fetch data from specified worksheets
        worksheet_data = fetch_worksheet_data(["PPMV VDL", "Category Mapping", "PPMV Facilities"])
        
        # Logic for PPMV Variance Bill page
        ppmv_vdl_data = worksheet_data.get("PPMV VDL")
        category_mapping_data = worksheet_data.get("Category Mapping")
        ppmv_facilities_data = worksheet_data.get("PPMV Facilities")

        # Example usage of worksheet data
        return render_template('ppmv_variance.html', 
                               ppmv_vdl_data=ppmv_vdl_data, 
                               category_mapping_data=category_mapping_data, 
                               ppmv_facilities_data=ppmv_facilities_data)

    except Exception as e:
        # Handle any exceptions
        error_message = f"An error occurred: {str(e)}"
        print("Error:", error_message)
        return render_template('error.html', error_message=error_message)

# Route for QRx Close-Out Bill page
@app.route('/qrx-close-out', methods=['GET', 'POST'])
def qrx_close_out():
    try:
        if request.method == 'POST':
            # Store the uploaded files in session
            session['supply_data'] = request.files['supply_data'].read().decode('utf-8')
            session['withdrawal_data'] = request.files['withdrawal_data'].read().decode('utf-8')
            session['dispensation_data'] = request.files['dispensation_data'].read().decode('utf-8')
            session['pricing_file'] = request.files['pricing_file'].read().decode('utf-8')
            if 'last_count_data' in request.files:
                session['last_count_data'] = request.files['last_count_data'].read().decode('utf-8')
            if 'buyout_data' in request.files:
                session['buyout_data'] = request.files['buyout_data'].read().decode('utf-8')
            # Redirect to another page or perform analysis
            
        # Fetch data from specified worksheets
        worksheet_data = fetch_worksheet_data(["QRx VDL", "Category Mapping", "QRx Close-Out Facilities"])
        
        # Logic for QRx Close-Out Bill page
        qrx_vdl_data = worksheet_data.get("QRx VDL")
        category_mapping_data = worksheet_data.get("Category Mapping")
        qrx_close_out_facilities_data = worksheet_data.get("QRx Close-Out Facilities")

        # Example usage of worksheet data
        return render_template('qrx_close_out.html', 
                               qrx_vdl_data=qrx_vdl_data, 
                               category_mapping_data=category_mapping_data, 
                               qrx_close_out_facilities_data=qrx_close_out_facilities_data)

    except Exception as e:
        # Handle any exceptions
        error_message = f"An error occurred: {str(e)}"
        print("Error:", error_message)
        return render_template('error.html', error_message=error_message)

# Route for PPMV Close-Out Bill page
@app.route('/ppmv-close-out')
def ppmv_close_out():
    try:
        # Fetch data from specified worksheets
        worksheet_data = fetch_worksheet_data(["PPMV VDL", "Category Mapping", "PPMV Close-Out Facilities"])
        
        # Logic for PPMV Close-Out Bill page
        ppmv_vdl_data = worksheet_data.get("PPMV VDL")
        category_mapping_data = worksheet_data.get("Category Mapping")
        ppmv_close_out_facilities_data = worksheet_data.get("PPMV Close-Out Facilities")

        # Example usage of worksheet data
        return render_template('ppmv_close_out.html', 
                               ppmv_vdl_data=ppmv_vdl_data, 
                               category_mapping_data=category_mapping_data, 
                               ppmv_close_out_facilities_data=ppmv_close_out_facilities_data)

    except Exception as e:
        # Handle any exceptions
        error_message = f"An error occurred: {str(e)}"
        print("Error:", error_message)
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
