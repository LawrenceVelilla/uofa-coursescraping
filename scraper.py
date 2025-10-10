import requests
from bs4 import BeautifulSoup
import re
import json


BASE_URL = "https://apps.ualberta.ca/catalogue/course/"

def fetch_course_data(dept):
    """
    Fetch course data for a specific department.
    Args:
        dept (str): Department code (e.g., 'CMPUT' for Computer Science).
    Returns:
        list: A list of dictionaries containing course information.
    """
    url = f"{BASE_URL}/{dept}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    course_info = []
    title_div = soup.find_all('div', class_='course')
    
    for titles in title_div:
        info = {}
        course_title = titles.h2.text.strip() if titles.h2 else 'N/A'

        # Split code and name, handling multi-word departments like "INT D" or "SOC D"
        if course_title != 'N/A':
            parts = course_title.split(' - ', 1)
            code = parts[0] if len(parts) > 0 else 'N/A'
            name = parts[1] if len(parts) > 1 else 'N/A'

            # Extract department using regex to handle multi-word departments
            dept_match = re.match(r'^([A-Z]+(?:\s[A-Z]+)?)', code)
            department = dept_match.group(1).lower() if dept_match else 'N/A'
        else:
            code = 'N/A'
            name = 'N/A'
            department = 'N/A'

        info['department'] = department
        info['courseCode'] = code
        info['title'] = name

        description = titles.p.text.strip() if titles.p else 'N/A'
        units_and_term = titles.b.text.strip() if titles.b else 'N/A'

        # Parse units, fee index, and term
        match = re.match(r'^(\d+(?:\.\d+)?)\s+units?\s+\(fi\s+(\d+)\)\(([^,]+),\s*[\d-]+\)$', units_and_term, re.IGNORECASE)
        units = {}
        if match:
            units['term'] = match.group(3).strip()
            units['credits'] = float(match.group(1))
            units['fee_index'] = int(match.group(2))
            
        else:
            units['credits'] = 'N/A'
            units['fee_index'] = 'N/A'
            units['term'] = 'N/A'

        info['description'] = description
        info['units'] = units

        courseUrl = titles.h2.a['href'] if titles.h2 and titles.h2.a else 'N/A'
        info['url'] = courseUrl

        course_info.append(info)
        
    return course_info
def main():
    dept = input("Enter the department code (e.g., cmput or int_d): ").strip().lower()

    # Convert space to underscore for URL (e.g., "int d" -> "int_d")
    dept = dept.replace(" ", "_")

    try:
        course_data = fetch_course_data(dept)
        print(json.dumps(course_data[0:20], indent=2))
    except ValueError as e:
        print(e)
    else:
        print(json.dumps(course_data[0:20], indent=2))
   

main()