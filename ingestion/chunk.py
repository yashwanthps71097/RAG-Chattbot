import os
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_chunks(processed_dir="data/processed", output_file="data/processed/chunks.json"):
    if not os.path.exists(processed_dir):
        logging.error(f"Processed directory {processed_dir} does not exist.")
        return

    all_chunks = []

    for file_name in os.listdir(processed_dir):
        if file_name.endswith(".json") and file_name != "chunks.json":
            file_path = os.path.join(processed_dir, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            title = data.get("title", "Mutual Fund Scheme")
            slug = file_name.replace(".json", "")
            
            logging.info(f"Chunking {title}...")

            # Define mapping of single-value fields
            sections = {
                "overview": data.get("overview"),
                "expense_ratio": data.get("expense_ratio"),
                "exit_load": data.get("exit_load"),
                "minimum_investment": data.get("minimum_investment"),
                "benchmark": data.get("benchmark")
            }

            # 1. Process standard fields
            for sec_name, sec_content in sections.items():
                if sec_content:
                    text_content = f"[{title}] {sec_content}"
                    all_chunks.append({
                        "id": f"{slug}#{sec_name}",
                        "text": text_content,
                        "metadata": {
                            "scheme_name": title,
                            "slug": slug,
                            "section": sec_name,
                            "source_url": f"https://groww.in/mutual-funds/{slug}"
                        }
                    })

            # 2. Process fund managers individually
            managers = data.get("fund_management", [])
            for idx, mgr in enumerate(managers):
                name = mgr.get("name")
                bio = mgr.get("bio")
                if name:
                    text_content = f"[{title}] Fund Management: {name}. {bio}"
                    all_chunks.append({
                        "id": f"{slug}#fund_management#{idx}",
                        "text": text_content,
                        "metadata": {
                            "scheme_name": title,
                            "slug": slug,
                            "section": "fund_management",
                            "manager_name": name,
                            "source_url": f"https://groww.in/mutual-funds/{slug}"
                        }
                    })

    # Save all chunks to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4)
    logging.info(f"Successfully generated and saved {len(all_chunks)} chunks to {output_file}.")

if __name__ == "__main__":
    generate_chunks()
