from agents import Agent

data_extraction_agent = Agent(name="Assistant", instructions="You are a helpful data extraction assistent,\
            tasked with extracting data from HTML documents and converting into a given format.", 
            model="gpt-4.1-nano")

data_summary_agent = Agent(name="Assistant", instructions="You are a helpful data summarization assistent,\
            tasked with summarizing data from JSON documents and \
            offering the best result that matches a user's request.",
            model="gpt-4.1-nano")