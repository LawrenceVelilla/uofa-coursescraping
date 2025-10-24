from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
import pandas as pd

load_dotenv()


class CourseDatabase:
    """
    Database interface for UAlberta course data with sentiment analysis.
    Handles connections, queries, and data operations for the course pipeline.

    Usage:
        with CourseDatabase() as db:
            courses = db.get_courses(limit=10)
            # Automatically closes when done
    """

    def __init__(self):
        """Initialize database connection using DIRECT_URL from .env"""
        direct_url = os.environ.get("DIRECT_URL")
        if not direct_url:
            raise ValueError("Missing DIRECT_URL in .env file")

        self.engine = create_engine(direct_url)

    def __enter__(self):
        """Context manager entry - returns self for use in 'with' statement"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically closes connection"""
        _ = exc_type, exc_val, exc_tb  # Unused but required by protocol
        self.close()
        return False

    def get_course(self, course_code):
        """
        Fetch a single course by course code.

        Args:
            course_code (str): Course code (e.g., 'CMPUT 174')

        Returns:
            dict: Course data or None if not found
        """
        with self.engine.connect() as conn:
            query = text('SELECT * FROM courses WHERE "courseCode" = :code')
            result = conn.execute(query, {"code": course_code})
            row = result.fetchone()

            if row:
                return dict(row._mapping)
            return None

    def get_courses(self, limit=None):
        """
        Fetch all courses from the database.

        Args:
            limit (int, optional): Maximum number of courses to return

        Returns:
            pandas.DataFrame: DataFrame with all courses
        """
        with self.engine.connect() as conn:
            if limit:
                query = text('SELECT department, "courseCode", title FROM courses LIMIT :limit')
                df = pd.read_sql(query, conn, params={"limit": limit})
            else:
                query = text('SELECT department, "courseCode", title FROM courses')
                df = pd.read_sql(query, conn)

            return df

    def get_courses_by_department(self, department):
        """
        Fetch all courses for a specific department.

        Args:
            department (str): Department code (e.g., 'cmput', 'math')

        Returns:
            pandas.DataFrame: DataFrame with courses from the department
        """
        with self.engine.connect() as conn:
            query = text('''
                SELECT department, "courseCode", title
                FROM courses
                WHERE LOWER(department) = LOWER(:dept)
            ''')
            df = pd.read_sql(query, conn, params={"dept": department})

            return df

    def close(self):
        """Close database connection."""
        self.engine.dispose()


# Test usage
if __name__ == "__main__":
    print("Testing database operations...\n")

    with CourseDatabase() as db:
        # Get all courses (limit 5 for testing)
        print("Fetching 5 courses...")
        courses = db.get_courses(limit=5)
        print(courses)
        print()

        # Get courses by department
        print("Fetching CMPUT courses...")
        cmput_courses = db.get_courses_by_department("cmput")
        print(f"Found {len(cmput_courses)} CMPUT courses")
        print(cmput_courses.head())
        print()

        # Get single course
        if not cmput_courses.empty:
            course_code = cmput_courses.iloc[0]['courseCode']
            print(f"Fetching details for {course_code}")
            course = db.get_course(course_code)
            print(course)

    
    print("\nDatabase connection closed automatically")
