# db/supabase_client.py
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from redditscraper import fetch_posts

load_dotenv()

# Create engine once at module level - SQLAlchemy handles connection pooling
direct_url = os.environ.get("DIRECT_URL")
if not direct_url:
    raise ValueError("Missing DIRECT_URL in .env file")

engine = create_engine(direct_url)

# Usage
if __name__ == "__main__":
    try:

        # Test query using connection context manager
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT * FROM courses
                    WHERE department = :dept
                    ORDER BY "courseCode" ASC
                    LIMIT :limit
                """),
                {"dept": "CMPUT", "limit": 50}
            )

            courses = result.mappings().all()

            test = ["CMPUT 174","CMPUT 175", "CMPUT 201", "CMPUT 204", "CMPUT 301", "CMPUT 291"]

            course_to_test = []

            for course in courses:
                if course["courseCode"] in test:
                    course_to_test.append({
                        "courseCode": course["courseCode"],
                        "title": course["title"],
                        "description": course["description"]
                    })

            print(f"Successfully fetched {len(courses)} courses")

            

            for item in course_to_test:
                posts = fetch_posts(item["courseCode"], limit=3)

                
                print(posts)



    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
