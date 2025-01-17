def research_task_description_tmplt(link: str, date) -> str:
        return f"""
            Conduct research via this link: { link }
            You may crawl this link up to maximum one level deep.
            Make sure all the information is accurate.
            
            Requirements:
            - Include working links to the original source material of each article you identify and report
            - Make sure that the source links are present in the scraped text via the link
            - Do not hallucinate or fabricate information or sources
            - Focus on reliable news sources
            - All news must have clear business relevance
            - Report all news in English
            - No duplicate coverage of the same news
            - No opinion pieces or editorials
            - No paywalled content
        """