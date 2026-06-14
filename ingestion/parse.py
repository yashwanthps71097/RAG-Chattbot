import os
import json
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clean_text(text):
    if not text:
        return ""
    return " ".join(text.strip().split())

def parse_scheme_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Check if there's an embedded __NEXT_DATA__ JSON script tag (Groww's standard Next.js data store)
    next_data_script = soup.find("script", id="__NEXT_DATA__")
    
    if next_data_script:
        try:
            json_content = json.loads(next_data_script.string)
            # Drill down to find the mutual fund server side data
            # Path: props -> pageProps -> mfServerSideData
            mf_data = json_content.get("props", {}).get("pageProps", {}).get("mfServerSideData", {})
            if mf_data:
                logging.info(f"Found __NEXT_DATA__ payload for {file_path}, extracting structured fields.")
                
                # Extract fund managers details
                managers = []
                for mgr in mf_data.get("fund_manager_details", []):
                    name = mgr.get("person_name", "")
                    education = mgr.get("education", "")
                    experience = mgr.get("experience", "")
                    
                    managers.append({
                        "name": clean_text(name),
                        "bio": clean_text(f"Education: {education}. Experience: {experience}")
                    })
                
                # If no managers lists but a single manager string is present
                if not managers and mf_data.get("fund_manager"):
                    managers.append({
                        "name": clean_text(mf_data.get("fund_manager")),
                        "bio": "Fund Manager profile details not fully specified."
                    })

                parsed_data = {
                    "title": clean_text(mf_data.get("scheme_name", "")),
                    "overview": clean_text(f"Category: {mf_data.get('category', '')} - {mf_data.get('sub_category', '')}. Risk Description: {mf_data.get('nfo_risk', mf_data.get('risk', ''))} risk. NAV: {mf_data.get('nav', '')} (as of {mf_data.get('nav_date', '')}). AUM: ₹{mf_data.get('aum', '')} Cr. Launch Date: {mf_data.get('launch_date', '')}."),
                    "expense_ratio": clean_text(f"Expense Ratio: {mf_data.get('expense_ratio', '')}%"),
                    "exit_load": clean_text(f"Exit Load: {mf_data.get('exit_load', '')}"),
                    "minimum_investment": clean_text(f"Minimum SIP Investment: ₹{mf_data.get('min_sip_investment', '')}. Minimum Additional Investment: ₹{mf_data.get('mini_additional_investment', '')}."),
                    "benchmark": clean_text(f"Benchmark: {mf_data.get('benchmark_name', mf_data.get('benchmark', ''))}"),
                    "fund_management": managers
                }
                return parsed_data
        except Exception as e:
            logging.error(f"Failed to parse __NEXT_DATA__ JSON in {file_path}, falling back to HTML selectors. Error: {e}")

    # 2. If Next.js data is not found or parsing failed, fallback to standard HTML parser
    logging.info(f"Using default HTML parser fallback for {file_path}")
    title_tag = soup.find("h1")
    title = clean_text(title_tag.text) if title_tag else os.path.basename(file_path).replace(".html", "")

    data = {
        "title": title,
        "overview": "",
        "expense_ratio": "",
        "exit_load": "",
        "minimum_investment": "",
        "benchmark": "",
        "fund_management": []
    }

    # Overview
    overview_div = soup.find("div", class_="overview")
    if overview_div:
        data["overview"] = clean_text(overview_div.text)

    # Expense Ratio & Exit Load
    exp_ratio_sec = soup.find("div", class_="expense-ratio-sec")
    if exp_ratio_sec:
        rows = exp_ratio_sec.find_all("tr")
        for row in rows:
            cols = [clean_text(td.text) for td in row.find_all("td")]
            if len(cols) == 2:
                label, val = cols[0].lower(), cols[1]
                if "expense" in label:
                    data["expense_ratio"] = f"Expense Ratio: {val}"
                elif "exit" in label:
                    data["exit_load"] = f"Exit Load: {val}"

    # Minimum Investment
    min_invest_div = soup.find("div", class_="minimum-investment")
    if min_invest_div:
        data["minimum_investment"] = clean_text(min_invest_div.text)

    # Benchmark
    bench_div = soup.find("div", class_="benchmark")
    if bench_div:
        data["benchmark"] = clean_text(bench_div.text)

    # Fund Management list
    fund_mgmt_div = soup.find("div", class_="fund-management")
    if fund_mgmt_div:
        managers = fund_mgmt_div.find_all("div", class_="manager")
        for mgr in managers:
            name_tag = mgr.find(class_="manager-name")
            bio_tag = mgr.find(class_="manager-bio")
            name = clean_text(name_tag.text) if name_tag else ""
            bio = clean_text(bio_tag.text) if bio_tag else ""
            if name:
                data["fund_management"].append({
                    "name": name,
                    "bio": bio
                })

    return data

def parse_all_raw_files(input_dir="data/raw", output_dir="data/processed"):
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(input_dir):
        logging.error(f"Input directory {input_dir} does not exist.")
        return

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".html"):
            slug = file_name.replace(".html", "")
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, f"{slug}.json")
            
            logging.info(f"Parsing {file_name}...")
            parsed_data = parse_scheme_html(input_path)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(parsed_data, f, indent=4)
            logging.info(f"Saved parsed structured JSON to {output_path}.")

if __name__ == "__main__":
    parse_all_raw_files()
