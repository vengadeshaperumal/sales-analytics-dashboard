import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from data_processor import DataProcessor
from visualizations import DashboardVisualizer
from insights import InsightGenerator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global data processor instance
processor = DataProcessor()

ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the home/upload page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload and data loading."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Only CSV files are allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load the file using the data processor
        result = processor.load_csv(filepath)
        if not result['success']:
            return jsonify(result), 400
        
        # Clean the data
        clean_result = processor.clean_data()
        if not clean_result['success']:
            return jsonify(clean_result), 400
        
        return jsonify({
            'success': True,
            'message': 'File uploaded and processed successfully',
            'data': clean_result
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@app.route('/dashboard')
def dashboard():
    """Render the dashboard with retail business analytics."""
    if processor.get_data() is None or processor.get_data().empty:
        return render_template('index.html', error='No data loaded. Please upload a sales data CSV file first.')
    
    try:
        # Get aggregated data
        daily_data = processor.aggregate_by_date()
        product_data = processor.aggregate_by_product()
        store_data = processor.aggregate_by_store()
        product_store_data = processor.get_product_by_store()
        summary_stats = processor.get_summary_stats()
        insights = InsightGenerator.get_all_insights(processor.get_data())
        
        # Create visualizations
        daily_chart = DashboardVisualizer.create_daily_revenue_chart(daily_data)
        product_treemap = DashboardVisualizer.create_product_treemap(product_data)
        store_pie = DashboardVisualizer.create_store_pie_chart(store_data)
        heatmap = DashboardVisualizer.create_product_store_heatmap(product_store_data)
        trend_chart = DashboardVisualizer.create_revenue_trend_chart(daily_data)
        store_chart = DashboardVisualizer.create_store_comparison_chart(store_data)
        
        return render_template(
            'dashboard.html',
            daily_chart=daily_chart,
            product_treemap=product_treemap,
            store_pie=store_pie,
            heatmap=heatmap,
            trend_chart=trend_chart,
            store_chart=store_chart,
            summary_stats=summary_stats,
            insights=insights
        )
    
    except Exception as e:
        return render_template('index.html', error=f'Error creating dashboard: {str(e)}')


@app.route('/api/insights')
def get_insights():
    """API endpoint to get insights JSON."""
    if processor.get_data() is None or processor.get_data().empty:
        return jsonify({'error': 'No data loaded'}), 400
    
    try:
        insights = InsightGenerator.get_all_insights(processor.get_data())
        return jsonify(insights), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/summary')
def get_summary():
    """API endpoint to get summary statistics."""
    if processor.get_data() is None or processor.get_data().empty:
        return jsonify({'error': 'No data loaded'}), 400
    
    try:
        stats = processor.get_summary_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reset', methods=['POST'])
def reset_data():
    """Reset the processor and clear uploaded files."""
    global processor
    processor = DataProcessor()
    
    # Clean up uploaded files
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
    except Exception as e:
        pass  # Continue even if cleanup fails
    
    return jsonify({'success': True, 'message': 'Data reset successfully'}), 200


if __name__ == '__main__':
    # Run the Flask app in debug mode for development
    app.run(debug=True, host='127.0.0.1', port=5000)
