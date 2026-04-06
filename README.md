# Retail Financial Analyzer - Tamil Nadu 📊

A comprehensive business analytics dashboard for analyzing retail sales performance across Tamil Nadu stores. Upload your sales transaction data and instantly visualize revenue patterns with interactive charts and actionable business insights.

## Features

### 1. **Data Processing**
- 📁 CSV file upload with drag-and-drop support
- 🧹 Automatic data cleaning (handle missing values, format dates)
- 🔄 Flexible date format support (YYYY-MM-DD, MM/DD/YYYY, etc.)
- ✓ Revenue calculation (quantity × price) and validation

### 2. **Data Aggregation**
- 📅 **Daily Aggregation**: Group sales by date with revenue totals and transaction counts
- 📦 **Product Aggregation**: Analyze sales by product type
- 🏪 **Store Aggregation**: Performance metrics by store location
- 📊 **Multi-dimensional Analysis**: Product performance across different stores

### 3. **Interactive Visualizations** (Plotly)
- 📊 **Bar Chart**: Daily revenue comparison with interactive tooltips
- 📈 **Trend Line**: Visualize revenue patterns over time
- 🌳 **Treemap**: Product sales distribution with proportional sizing
- 🥧 **Pie Chart**: Store revenue percentages
- 🔥 **Heatmap**: Product performance across stores
- 📊 **Store Comparison**: Side-by-side store performance analysis

### 4. **Automated Business Insights**
- 🏆 **Top Selling Product**: Automatically identifies your best-selling product
- 🏪 **Best Performing Store**: Find your highest-revenue store location
- 📅 **Best Sales Day**: Identify peak sales days
- 📋 **Product Performance**: Detailed metrics for each product
- 🏢 **Store Performance**: Location-wise sales analysis

### 5. **Business Summary Statistics**
- Total revenue amount (₹)
- Average transaction value
- Total units sold
- Number of unique products
- Number of store locations
- Date range coverage

## Project Structure

```
Financial_Dashboard/
├── app.py                      # Flask application
├── data_processor.py          # Data cleaning & aggregation
├── visualizations.py          # Plotly chart generation
├── insights.py                # Insight generation engine
├── requirements.txt           # Python dependencies
├── sample_data.csv           # Sample retail sales data (Tamil Nadu)
├── templates/
│   ├── index.html            # Upload page
│   └── dashboard.html        # Analytics dashboard
├── static/
│   ├── style.css             # Styling
│   └── script.js             # Frontend interactions
└── uploads/                  # Storage for uploaded CSV files
```

## Installation & Setup

### 1. Clone/Download the Project
```bash
cd Financial_Dashboard
```

### 2. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Flask Server
```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Access the Dashboard
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### Step 1: Prepare Your Data
Create a CSV file with three required columns:
- **date**: Transaction date (various formats supported)
- **amount**: Transaction amount (as numbers, e.g., 50.00)
- **category**: Expense category (e.g., Groceries, Dining, Rent)

Example CSV structure:
```csv
date,amount,category
2024-01-15,50.00,Groceries
2024-01-16,75.50,Dining
2024-01-17,1200.00,Rent
2024-01-18,45.99,Utilities
```

### Step 2: Upload Your File
1. Click "Choose CSV file" or drag & drop your CSV
2. Click "Upload & Analyze"
3. The dashboard will automatically process and display your data

### Step 3: Explore the Dashboard
The dashboard provides:
- **Summary Statistics**: Overview of your spending
- **Key Insights**: Top categories, spending records
- **Visualizations**: Interactive charts for deeper analysis
- **Detailed Tables**: Breakdown by category and month

### Step 4: Reset (Optional)
Click "Reset" to clear data and upload a new file.

## CSV Requirements

### Minimal Valid Column Names
Your CSV must contain (case-insensitive):
- `date` - Transaction date
- `amount` - Spending amount
- `category` - Expense category

Optional columns:
- `description` - Additional notes (if missing, filled with "Unknown")

### Supported Date Formats
- YYYY-MM-DD (2024-01-15)
- MM/DD/YYYY (01/15/2024)
- DD/MM/YYYY (15/01/2024)
- Many other common formats

### Example CSV Files

**Bank Statement Format:**
```csv
date,description,amount,category
2024-01-15,Whole Foods Market,45.50,Groceries
2024-01-16,Restaurant XYZ,75.50,Dining
2024-01-17,Landlord Payment,1200.00,Rent
```

**Simple Expense Tracker:**
```csv
date,amount,category
2024-01-15,45.50,Groceries
2024-01-16,75.50,Dining
2024-01-17,1200.00,Rent
```

## API Endpoints

The dashboard provides REST API endpoints for programmatic access:

### Get All Insights
```bash
GET /api/insights
```
Returns: Top category, highest/lowest days, category breakdown, monthly summary

### Get Summary Statistics
```bash
GET /api/summary
```
Returns: Total spending, averages, medians, date range, etc.

### Upload File
```bash
POST /upload
Content-Type: multipart/form-data
Body: file (CSV file)
```

### Reset Data
```bash
POST /reset
```

## Data Processing Pipeline

```
CSV Upload
    ↓
Load & Validate
    ↓
Data Cleaning
  - Remove missing values
  - Format dates
  - Validate amounts
    ↓
Aggregation
  - Monthly totals
  - Category totals
  - Combined breakdowns
    ↓
Visualization
  - Generate interactive charts
  - Create treemaps & heatmaps
    ↓
Insight Generation
  - Calculate spend statistics
  - Find records (top, highest, lowest)
    ↓
Display Dashboard
```

## Key Classes & Functions

### DataProcessor
- `load_csv()` - Load and validate CSV file
- `clean_data()` - Clean and normalize data
- `aggregate_by_month()` - Monthly spending totals
- `aggregate_by_category()` - Category spending totals
- `get_summary_stats()` - Calculate statistics

### DashboardVisualizer
- `create_monthly_bar_chart()` - Bar chart for months
- `create_category_treemap()` - Proportional treemap
- `create_category_pie_chart()` - Pie chart
- `create_category_month_heatmap()` - Heatmap
- `create_line_chart()` - Trend line

### InsightGenerator
- `get_top_spending_category()` - Find top category
- `get_highest_spending_day()` - Find peak spending day
- `get_lowest_spending_day()` - Find minimum spending day
- `get_category_breakdown()` - Detailed category stats
- `get_monthly_summary()` - Month-by-month breakdown
- `get_all_insights()` - All insights at once

## Sample Data

A `sample_data.csv` file is included for testing. Upload it to see the dashboard in action with realistic retail sales data from Tamil Nadu stores (Chennai, Coimbatore, Madurai, Trichy, Salem).

## Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Opera: ✅ Full support

## Performance Notes

- Recommended: CSV files up to 100,000 transactions
- Max file size: 16MB
- Large datasets (10,000+ rows) may take 1-2 seconds to process

## Troubleshooting

### "No file selected" error
- Ensure you've selected a CSV file before uploading

### "Missing required columns" error
- Check that your CSV has: date, amount, category columns
- Column names should be exactly as shown (case-insensitive)

### Date parsing errors
- Verify dates are in a standard format
- Try YYYY-MM-DD format if having issues

### No data appears in dashboard
- Check that CSV has valid data (not empty)
- Ensure amounts are valid numbers
- Avoid special characters in category names

### Charts not displaying
- Clear browser cache (Ctrl+Shift+Delete)
- Ensure JavaScript is enabled
- Try a different browser

## Technical Stack

- **Backend**: Flask 3.0.0
- **Data Processing**: Pandas 2.1.4
- **Visualization**: Plotly 5.18.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Server**: Built-in Flask development server

## Future Enhancements

Potential features to add:
- 📊 Budget tracking and alerts
- 💾 Data persistence (database integration)
- 📤 Export reports as PDF
- 🔐 User authentication
- 🌍 Multi-currency support
- 📱 Mobile-responsive improvements
- 📅 Recurring transaction detection
- 🎯 Spending goals and targets

## Security Notes

- Uploaded files are stored temporarily in the `uploads/` folder
- No data is sent to external servers
- Close the application to clear uploaded files
- Use the Reset button to manually clear data

## License

This project is free to use and modify.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify CSV format matches requirements
3. Ensure all dependencies are installed
4. Check browser console for JavaScript errors

---

**Enjoy analyzing your finances! 💰**
