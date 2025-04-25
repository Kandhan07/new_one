from flask import Flask, render_template, request, send_file
from weasyprint import HTML
from datetime import datetime
import json
import io

app = Flask(__name__)

def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_document():
    try:
        doc_type = request.form.get('doc_type')
        name = request.form.get('name')
        
        # Load data from JSON file
        template_data = load_data()
        
        # Common data for all documents
        data = {
            "name": name,
            "date": datetime.now().strftime("%B %d, %Y")
        }
        
        # Add specific data based on document type
        if doc_type == 'profile':
            data.update(template_data['profile'])
            template = 'profile_card.html'
            filename = f"profile_{name.lower().replace(' ', '_')}.pdf"
        elif doc_type == 'invoice':
            invoice_data = template_data['invoice']
            data.update({
                "company_name": invoice_data['company_name'],
                "address": invoice_data['address'],
                "city_state": invoice_data['city_state'],
                "invoice_no": f"{invoice_data['invoice_prefix']}{datetime.now().strftime('%Y%m%d')}",
                "items": invoice_data['items'],
                "amount": "$999.99"
            })
            template = 'invoice.html'
            filename = f"invoice_{name.lower().replace(' ', '_')}.pdf"
        elif doc_type == 'blog':
            blog_data = template_data['blog']
            data.update({
                "title": blog_data['title'],
                "subtitle": blog_data['subtitle'],
                "content": blog_data['content'],
                "author": blog_data['author'],
                "metadata": blog_data['metadata'],
                "featured_image": blog_data['featured_image'],
                "sections": blog_data['sections'],
                "comments_enabled": blog_data['comments_enabled'],
                "likes_count": blog_data['likes_count'],
                "views_count": blog_data['views_count'],
                "author_prefix": blog_data['author_prefix'],
                "related_posts": blog_data['related_posts']
            })
            template = 'blog_post.html'
            filename = f"blog_{name.lower().replace(' ', '_')}.pdf"
        else:  # certificate
            cert_data = template_data['certificate']
            data.update({
                "title": cert_data['title'],
                "course": cert_data['course'],
                "certificate_id": f"{cert_data['cert_prefix']}{datetime.now().strftime('%Y%m%d')}001",
                "signature_text": cert_data['signature_text']
            })
            template = 'certificate.html'
            filename = f"certificate_{name.lower().replace(' ', '_')}.pdf"
        
        # Generate PDF
        # Add this before rendering the template
        print("Template data:", data)
        html = render_template(template, **data)
        pdf = HTML(string=html).write_pdf()
        
        # Create BytesIO object
        pdf_buffer = io.BytesIO(pdf)
        pdf_buffer.seek(0)
        
        # Return PDF file for download
        return send_file(
            pdf_buffer,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"Error generating document: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)