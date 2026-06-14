import os
import requests
import yaml
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Default Mock Content if live fetch fails and no cached file exists
MOCK_SCHEMES_HTML = {
    "hdfc-mid-cap-fund-direct-growth": """
        <html>
        <body>
            <h1>HDFC Mid Cap Fund Direct Growth</h1>
            <div class="overview">
                <p>NAV: 185.40</p>
                <p>AUM: 65000 Cr</p>
                <p>Category: Equity - Mid Cap</p>
                <p>Riskometer: Very High</p>
            </div>
            <div class="expense-ratio-sec">
                <h3>Expense Ratio, Exit Load & Tax</h3>
                <table>
                    <tr><td>Expense Ratio</td><td>0.73%</td></tr>
                    <tr><td>Exit Load</td><td>1.00% if redeemed within 1 year</td></tr>
                    <tr><td>Tax Implications</td><td>15% tax on STCG (less than 1 year), 10% tax on LTCG over 1 Lakh (more than 1 year)</td></tr>
                </table>
            </div>
            <div class="minimum-investment">
                <h3>Minimum Investment</h3>
                <table>
                    <tr><td>Minimum SIP</td><td>₹100</td></tr>
                    <tr><td>Minimum Lumpsum</td><td>₹100</td></tr>
                </table>
            </div>
            <div class="benchmark">
                <h3>Benchmark</h3>
                <p>NIFTY Midcap 150 TRI</p>
            </div>
            <div class="fund-management">
                <h3>Fund Management</h3>
                <div class="manager">
                    <p class="manager-name">Chaitanya Choksi</p>
                    <p class="manager-tenure">Feb 2023 - Present</p>
                    <p class="manager-bio">Education: B.Com, CA. Experience: Over 20 years in equity research and portfolio management.</p>
                </div>
            </div>
        </body>
        </html>
    """,
    "hdfc-large-cap-fund-direct-growth": """
        <html>
        <body>
            <h1>HDFC Large Cap Fund Direct Growth</h1>
            <div class="overview">
                <p>NAV: 124.50</p>
                <p>AUM: 45000 Cr</p>
                <p>Category: Equity - Large Cap</p>
                <p>Riskometer: Very High</p>
            </div>
            <div class="expense-ratio-sec">
                <h3>Expense Ratio, Exit Load & Tax</h3>
                <table>
                    <tr><td>Expense Ratio</td><td>0.85%</td></tr>
                    <tr><td>Exit Load</td><td>1.00% if redeemed within 30 days</td></tr>
                    <tr><td>Tax Implications</td><td>15% tax on STCG (less than 1 year), 10% tax on LTCG over 1 Lakh (more than 1 year)</td></tr>
                </table>
            </div>
            <div class="minimum-investment">
                <h3>Minimum Investment</h3>
                <table>
                    <tr><td>Minimum SIP</td><td>₹100</td></tr>
                    <tr><td>Minimum Lumpsum</td><td>₹100</td></tr>
                </table>
            </div>
            <div class="benchmark">
                <h3>Benchmark</h3>
                <p>NIFTY 100 TRI</p>
            </div>
            <div class="fund-management">
                <h3>Fund Management</h3>
                <div class="manager">
                    <p class="manager-name">Gopal Agrawal</p>
                    <p class="manager-tenure">Dec 2020 - Present</p>
                    <p class="manager-bio">Education: B.E., M.B.A. Experience: Over 22 years of experience in fund management and equity research.</p>
                </div>
            </div>
        </body>
        </html>
    """,
    "hdfc-small-cap-fund-direct-growth": """
        <html>
        <body>
            <h1>HDFC Small Cap Fund Direct Growth</h1>
            <div class="overview">
                <p>NAV: 162.80</p>
                <p>AUM: 32000 Cr</p>
                <p>Category: Equity - Small Cap</p>
                <p>Riskometer: Very High</p>
            </div>
            <div class="expense-ratio-sec">
                <h3>Expense Ratio, Exit Load & Tax</h3>
                <table>
                    <tr><td>Expense Ratio</td><td>0.68%</td></tr>
                    <tr><td>Exit Load</td><td>1.00% if redeemed within 1 year</td></tr>
                    <tr><td>Tax Implications</td><td>15% tax on STCG (less than 1 year), 10% tax on LTCG over 1 Lakh (more than 1 year)</td></tr>
                </table>
            </div>
            <div class="minimum-investment">
                <h3>Minimum Investment</h3>
                <table>
                    <tr><td>Minimum SIP</td><td>₹100</td></tr>
                    <tr><td>Minimum Lumpsum</td><td>₹100</td></tr>
                </table>
            </div>
            <div class="benchmark">
                <h3>Benchmark</h3>
                <p>NIFTY Smallcap 250 TRI</p>
            </div>
            <div class="fund-management">
                <h3>Fund Management</h3>
                <div class="manager">
                    <p class="manager-name">Chirag Setalvad</p>
                    <p class="manager-tenure">Jun 2014 - Present</p>
                    <p class="manager-bio">Education: B.Sc. Experience: Over 25 years of experience in fund management and investment analysis.</p>
                </div>
            </div>
        </body>
        </html>
    """,
    "hdfc-gold-etf-fund-of-fund-direct-plan-growth": """
        <html>
        <body>
            <h1>HDFC Gold ETF Fund of Fund Direct Plan Growth</h1>
            <div class="overview">
                <p>NAV: 22.30</p>
                <p>AUM: 1500 Cr</p>
                <p>Category: Other - Gold</p>
                <p>Riskometer: High</p>
            </div>
            <div class="expense-ratio-sec">
                <h3>Expense Ratio, Exit Load & Tax</h3>
                <table>
                    <tr><td>Expense Ratio</td><td>0.15%</td></tr>
                    <tr><td>Exit Load</td><td>None</td></tr>
                    <tr><td>Tax Implications</td><td>Taxed according to investor's income tax slab rates (Debt taxation rules)</td></tr>
                </table>
            </div>
            <div class="minimum-investment">
                <h3>Minimum Investment</h3>
                <table>
                    <tr><td>Minimum SIP</td><td>₹100</td></tr>
                    <tr><td>Minimum Lumpsum</td><td>₹100</td></tr>
                </table>
            </div>
            <div class="benchmark">
                <h3>Benchmark</h3>
                <p>Domestic Price of Gold</p>
            </div>
            <div class="fund-management">
                <h3>Fund Management</h3>
                <div class="manager">
                    <p class="manager-name">Nirman Morakhia</p>
                    <p class="manager-tenure">Feb 2023 - Present</p>
                    <p class="manager-bio">Education: B.E., M.B.A. Experience: Over 15 years in equity dealer and portfolio analytics.</p>
                </div>
            </div>
        </body>
        </html>
    """,
    "hdfc-defence-fund-direct-growth": """
        <html>
        <body>
            <h1>HDFC Defence Fund Direct Growth</h1>
            <div class="overview">
                <p>NAV: 28.90</p>
                <p>AUM: 3200 Cr</p>
                <p>Category: Equity - Sectoral / Thematic (Defence)</p>
                <p>Riskometer: Very High</p>
            </div>
            <div class="expense-ratio-sec">
                <h3>Expense Ratio, Exit Load & Tax</h3>
                <table>
                    <tr><td>Expense Ratio</td><td>0.74%</td></tr>
                    <tr><td>Exit Load</td><td>1.00% if redeemed within 1 year</td></tr>
                    <tr><td>Tax Implications</td><td>15% tax on STCG (less than 1 year), 10% tax on LTCG over 1 Lakh (more than 1 year)</td></tr>
                </table>
            </div>
            <div class="minimum-investment">
                <h3>Minimum Investment</h3>
                <table>
                    <tr><td>Minimum SIP</td><td>₹100</td></tr>
                    <tr><td>Minimum Lumpsum</td><td>₹100</td></tr>
                </table>
            </div>
            <div class="benchmark">
                <h3>Benchmark</h3>
                <p>Nifty India Defence Index TRI</p>
            </div>
            <div class="fund-management">
                <h3>Fund Management</h3>
                <div class="manager">
                    <p class="manager-name">Priya Ranjan</p>
                    <p class="manager-tenure">Apr 2025 - Present</p>
                    <p class="manager-bio">Education: B.Tech, M.B.A. Experience: Prior to joining HDFC AMC, worked at various institutions covering industrial and capital goods sectors.</p>
                </div>
                <div class="manager">
                    <p class="manager-name">Dhruv Muchhal</p>
                    <p class="manager-tenure">Jun 2023 - Present</p>
                    <p class="manager-bio">Education: CA, CFA. Experience: Over 10 years in equity research and research analytics.</p>
                </div>
            </div>
        </body>
        </html>
    """
}

def load_corpus_config(config_path="config/corpus.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def fetch_html_for_schemes(config_path="config/corpus.yaml", output_dir="data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    config = load_corpus_config(config_path)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for scheme in config.get("schemes", []):
        slug = scheme.get("slug")
        url = scheme.get("url")
        file_path = os.path.join(output_dir, f"{slug}.html")

        logging.info(f"Processing scheme {slug}...")
        html_content = None

        try:
            logging.info(f"Fetching live data from {url}...")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                html_content = response.text
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                logging.info(f"Successfully saved live HTML for {slug}.")
            else:
                logging.warning(f"Live fetch returned status code {response.status_code} for {slug}.")
        except Exception as e:
            logging.error(f"Error fetching live data for {slug}: {e}")

        # Fallback handling
        if not html_content:
            if os.path.exists(file_path):
                logging.info(f"Using existing cached HTML file for {slug}.")
            else:
                logging.info(f"Writing mock fallback data for {slug}...")
                mock_data = MOCK_SCHEMES_HTML.get(slug, "<html><body>No details available</body></html>")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(mock_data)

if __name__ == "__main__":
    fetch_html_for_schemes()
