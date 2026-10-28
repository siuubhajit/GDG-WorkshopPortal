import functions_framework
from google.cloud import firestore

db = firestore.Client(project='cloudport-project')

@functions_framework.http
def cloudport_handler(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    if request.method != 'POST':
        return ({'error': 'Method Not Allowed'}, 405, headers)

    request_json = request.get_json(silent=True)
    if not request_json:
        return ({'error': 'Invalid JSON payload'}, 400, headers)

    name = request_json.get('name', '').strip()
    email = request_json.get('email', '').strip().lower()
    department = request_json.get('department', '').strip()
    interest = request_json.get('interest', '').strip()

    if not name or not email or not department or not interest:
        return ({'error': 'Missing required fields'}, 400, headers)

    try:
        # Check if email already exists in the registrations collection
        existing_docs = db.collection('registrations').where('email', '==', email).limit(1).get()
        if len(existing_docs) > 0:
            return ({'error': 'This email address is already registered.'}, 400, headers)

        # Save new unique registration
        doc_ref = db.collection('registrations').add({
            'name': name,
            'email': email,
            'department': department,
            'interest': interest,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        return ({'status': 'success', 'message': 'Registration successful!'}, 200, headers)
    except Exception as e:
        return ({'error': str(e)}, 500, headers)