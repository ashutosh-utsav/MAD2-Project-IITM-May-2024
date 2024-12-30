from flask import Blueprint, Response
from io import StringIO
import csv
from models import Books

export_bp = Blueprint('export', __name__)

@export_bp.route('/download-books-csv', methods=['GET'])
def download_books_csv():
    # Create a CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    
    # Add the CSV header
    writer.writerow(['Book Name', 'Author', 'Content', 'Date Issued'])

    # Fetch the data from the database
    books = Books.query.all()

    # Write the data to CSV
    for book in books:
        writer.writerow([book.name, book.author, book.content, book.date_added])

    # Set the CSV file content
    output = si.getvalue()
    si.close()

    # Prepare the response with the CSV file
    response = Response(output, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=books_export.csv'
    return response
