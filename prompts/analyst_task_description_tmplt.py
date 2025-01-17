def analyst_task_description_tmplt(current_date: str, results) -> str:
    return f"""
        Generate a structured list of 5 of the most important updates from the research results provided.
        Include working links to the original source material of each article you identify.
        Verify that the source links are working.
        The current date is { current_date }.

        # Table of Contents

        - Requirements
        - Research Results

        # Requirements
        
        - All the reference links should be working links
        - Verify that the source links are working
        - Include working links to the original source material of each list item you provide
        - Focus on reliable news sources
        - Report all news in English
        - No duplicate coverage of same news
        - No opinion pieces or editorials
        - No paywalled content
        - 5 results in the final list

        # Research Results

        {
            "\n".join([f"- {result}" for result in results])
        }
    """