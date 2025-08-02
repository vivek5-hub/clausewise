from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - Allow all origins for development
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            "status": "healthy",
            "message": "Legal Document Analyzer Backend is running",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Analysis endpoint
@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_document():
    """Analyze document endpoint"""
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No data provided"
            }), 400
        
        # Extract parameters
        text = data.get('text', '')
        model = data.get('model', 'microsoft/DialoGPT-medium')
        analysis_type = data.get('analysis_type', 'text-generation')
        parameters = data.get('parameters', {})
        
        logger.info(f"Analyzing document with model: {model}, type: {analysis_type}")
        
        # For now, return mock data - you can integrate with Hugging Face here
        # This is where you would call your Hugging Face API
        mock_result = generate_mock_analysis(text, model, analysis_type, parameters)
        
        return jsonify(mock_result), 200
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return jsonify({
            "error": "Analysis failed",
            "message": str(e)
        }), 500

def generate_mock_analysis(text, model, analysis_type, parameters):
    """Generate mock analysis results"""
    
    # Detect document type
    doc_type = detect_document_type(text)
    
    base_result = {
        "document_type": doc_type,
        "confidence": 85.5 + (len(text) % 10),  # Mock confidence
        "model_used": model,
        "analysis_type": analysis_type,
        "processing_time": 2.3,
        "timestamp": datetime.now().isoformat()
    }
    
    # Generate analysis based on type
    if analysis_type == 'text-generation':
        base_result["analysis_result"] = f"""
Based on the analysis of this {doc_type.lower()}, here are the key findings:

1. **Document Structure**: The document follows standard legal formatting and includes necessary sections for a {doc_type.lower()}.

2. **Key Elements Identified**:
   - Clear definitions and terminology
   - Well-defined obligations and responsibilities  
   - Appropriate termination and dispute resolution clauses
   - Standard legal protections and limitations

3. **Risk Assessment**:
   - **Low Risk**: Standard legal language and structure
   - **Medium Risk**: Some terms may benefit from clarification
   - **Areas for Review**: Payment terms and liability limitations

4. **Compliance Notes**:
   - Document appears to follow industry standards
   - Recommend legal review for jurisdiction-specific requirements
   - Consider adding force majeure provisions if not present

5. **Recommendations**:
   - Review indemnification clauses for balance
   - Ensure data protection compliance
   - Verify proper execution procedures
        """
    
    elif analysis_type == 'text-classification':
        base_result["classifications"] = [
            {"label": "CONTRACT", "score": 0.89},
            {"label": "LEGAL_DOCUMENT", "score": 0.76},
            {"label": "AGREEMENT", "score": 0.65}
        ]
    
    elif analysis_type == 'token-classification':
        base_result["entities"] = [
            {"entity": "ORG", "word": "Company", "start": 10, "end": 17, "score": 0.99},
            {"entity": "PERSON", "word": "John Smith", "start": 25, "end": 35, "score": 0.95},
            {"entity": "DATE", "word": "January 1, 2024", "start": 45, "end": 60, "score": 0.98},
            {"entity": "MONEY", "word": "$10,000", "start": 70, "end": 77, "score": 0.92}
        ]
    
    elif analysis_type == 'question-answering':
        base_result["analysis_result"] = [
            {"question": "What type of document is this?", "answer": doc_type, "confidence": 0.95},
            {"question": "What are the main parties?", "answer": "The contracting parties as defined in the agreement", "confidence": 0.87},
            {"question": "What are key obligations?", "answer": "Payment obligations, confidentiality, and performance requirements", "confidence": 0.82}
        ]
    
    elif analysis_type == 'summarization':
        base_result["summary"] = f"This {doc_type.lower()} establishes the terms and conditions governing the relationship between the parties. Key provisions include payment terms, confidentiality obligations, termination conditions, and dispute resolution procedures. The agreement includes standard legal protections and defines the scope of work or services to be provided."
    
    return base_result

def detect_document_type(text):
    """Simple document type detection"""
    text_lower = text.lower()
    
    if 'contract' in text_lower or 'agreement' in text_lower:
        return 'Contract'
    elif 'nda' in text_lower or 'non-disclosure' in text_lower:
        return 'NDA'
    elif 'terms of service' in text_lower or 'terms and conditions' in text_lower:
        return 'Terms of Service'
    elif 'privacy policy' in text_lower:
        return 'Privacy Policy'
    elif 'lease' in text_lower or 'rental' in text_lower:
        return 'Lease Agreement'
    else:
        return 'Legal Document'

# Serve frontend
@app.route('/')
def serve_frontend():
    """Serve the frontend HTML"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return jsonify({
            "message": "Frontend HTML not found",
            "instructions": "Place your HTML file as 'index.html' in this directory",
            "available_endpoints": {
                "health": "/health",
                "analyze": "/analyze (POST)"
            }
        }), 404

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Legal Document Analyzer Backend on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Backend will be available at:")
    print(f"  - http://localhost:{port}")
    print(f"  - http://127.0.0.1:{port}")
    print(f"Health check: http://localhost:{port}/health")
    
    try:
        app.run(
            host='127.0.0.1',  # Changed from 0.0.0.0 to 127.0.0.1
            port=port,
            debug=debug,
            threaded=True
        )
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {port} is already in use. Trying port {port + 1}")
            app.run(
                host='127.0.0.1',
                port=port + 1,
                debug=debug,
                threaded=True
            )
        else:
            print(f"Error starting server: {e}")
            raise