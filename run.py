import sys, ast, json
from data_extraction_agent import init_llm, run_extraction_prompt, run_web_request, run_summary_prompt
from DEA_v2 import data_extraction_agent, data_summary_agent
from agents import Runner

OUTPUT_FILE = "output.json"

if __name__ == "__main__":

    # Arguments
    url = sys.argv[1]
    user_request = sys.argv[2]

    # Check if URL is provided
    if not url:
        print("Please provide a URL as a command line argument.")
        sys.exit(1)

    # Initialize LLM
    client = init_llm()
    print("Initializing LLM...")

    # Fetch HTML content
    html_content = run_web_request(url)

    # Check if HTML content is fetched
    if not html_content:
        print("Failed to fetch HTML content.")
        sys.exit(1)

    print("HTML content fetched successfully.")

    # Data extraction prompt
    data_extraction_prompt = (
    "ROLE:\n"
    "Product data extraction specialist for e-commerce HTML parsing.\n\n"
    "TASK:\n"
    "Extract complete product information from HTML content.\n\n"
    "INPUT:\n"
    "- HTML content from e-commerce pages\n"
    "- Process all products in original order\n\n"
    "OUTPUT:\n"
    "JSON array of products with fields:\n"
    "- name: Exact product name (preserve formatting/special chars)\n"
    "- price: Full price with currency\n"
    "- description: Complete product description\n"
    "- link: Full product URL\n"
    "- specifications: Technical details as key-value pairs\n\n"
    "CONSTRAINTS:\n"
    "- Extract data exactly as shown, no modifications\n"
    "- Return only valid JSON array\n"
    "- No missing products or fields\n"
    "- No explanatory text or markdown\n\n"
    "HTML CONTENT:\n\n"
    f"{html_content}\n\n"
    )

    print("Running prompt...")
    #response = run_extraction_prompt(data_extraction_prompt, client)
    response = Runner.run_sync(data_extraction_agent, data_extraction_prompt)

    print("Prompt executed successfully.")

    # Write data to file
    parsed_data = ast.literal_eval(response.final_output)

    with open(OUTPUT_FILE, "w") as file:
        json.dump(parsed_data, file, indent=2)

    # Data summary prompt
    data_summary_prompt = (
        "ROLE:\n"
        "Product recommendation specialist focusing on specific requirements.\n\n"
        "TASK:\n"
        "Find the cheapest Raspberry Pi Pico board that has wireless capabilities.\n\n"
        "INPUT:\n"
        "- JSON array of products\n"
        "- User request with specific requirements\n\n"
        "OUTPUT FORMAT:\n"
        "Return a JSON object with this exact structure:\n"
        "{\n"
        '  "recommended_product": {product object},\n'
        '  "reason": "Brief explanation of why this product was chosen",\n'
        '  "price_numeric": extracted price as number without currency\n'
        "}\n\n"
        "INSTRUCTIONS:\n"
        " - Format response exactly as shown in OUTPUT FORMAT\n"
        " - Never return null unless absolutely no match found\n\n"
        "PRODUCTS:\n"
        f"{parsed_data}\n\n"
        "USER REQUEST:\n"
        f"{user_request}"
    )

    print("Running summary prompt...")
    #response = run_summary_prompt(data_summary_prompt, client)

    response = Runner.run_sync(data_summary_agent, data_summary_prompt)

    print("Summary prompt executed successfully.\n")

    # Write response
    print(response.final_output)