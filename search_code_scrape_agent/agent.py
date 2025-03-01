import os
from typing import List, Dict, Any, Callable, Optional
from abc import ABC, abstractmethod
import json
import requests
from dataclasses import dataclass
import openai
from datetime import datetime
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base class for all tools
class Tool(ABC):
    @abstractmethod
    def execute(self, input_data: str) -> str:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

# Google Search tool using Serper
class GoogleSearchTool(Tool):
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def execute(self, query: str) -> str:
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'q': query,
            'num': 10
        }
        response = requests.post(
            'https://google.serper.dev/search',
            headers=headers,
            json=payload
        )
        results = response.json()
        
        # Format results into a readable string
        formatted_results = []
        for item in results.get('organic', []):
            formatted_results.append(f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n")
        
        return "\n".join(formatted_results)
    
    def get_description(self) -> str:
        return "Searches Google and returns relevant web results. Input should be a search query."

# Web scraping tool
class WebScraperTool(Tool):
    def _extract_main_content(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "meta", "link"]):
            script.decompose()
            
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:500000]  # Limit content length

    def execute(self, url: str) -> str:
        try:
            response = requests.get(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            response.raise_for_status()
            return self._extract_main_content(response.text)
        except Exception as e:
            return f"Error scraping URL: {str(e)}"
    
    def get_description(self) -> str:
        return "Scrapes content from a given URL. Input should be a valid URL."

@dataclass
class TaskResult:
    task: str
    result: str
    confidence: float
    tools_used: List[str]
    completion_time: datetime
    error: Optional[str] = None

class Agent:
    def __init__(self, openai_api_key: str, tools: Dict[str, Tool]):
        self.openai_api_key = openai_api_key
        self.tools = tools
        openai.api_key = openai_api_key
        
    def _get_tool_descriptions(self) -> str:
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"{name}: {tool.get_description()}")
        return "\n".join(descriptions)

    def _create_system_prompt(self) -> str:
        return f"""You are a research assistant with access to the following tools:

{self._get_tool_descriptions()}

To use a tool, respond with a JSON object with the following structure:
{{
    "thought": "Your reasoning about what to do next",
    "tool": "tool_name",
    "input": "input for the tool"
}}

If you have gathered enough information to answer the question, respond with:
{{
    "thought": "Your final reasoning",
    "answer": "Your final answer",
    "confidence": 0.0-1.0
}}

Break down complex tasks into steps. Be thorough and accurate.
If you get large amounts of text, focus on the most relevant information."""

    def _truncate_text(self, text: str, max_length: int = 900000) -> str:
        """Truncate text to ensure it fits within OpenAI's context window"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "\n...[truncated]"

    def _execute_tool(self, tool_name: str, input_data: str) -> str:
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"
        try:
            result = self.tools[tool_name].execute(input_data)
            return self._truncate_text(result)
        except Exception as e:
            return f"Error executing tool {tool_name}: {str(e)}"

    def process_task(self, task: str, max_steps: int = 10) -> TaskResult:
        start_time = datetime.now()
        tools_used = []
        
        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            {"role": "user", "content": task}
        ]
        
        try:
            for _ in range(max_steps):
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.7
                )
                
                assistant_message = response.choices[0].message.content
                try:
                    action = json.loads(assistant_message)
                except json.JSONDecodeError:
                    continue
                    
                if "answer" in action:
                    return TaskResult(
                        task=task,
                        result=action["answer"],
                        confidence=action["confidence"],
                        tools_used=list(set(tools_used)),
                        completion_time=datetime.now()
                    )
                    
                if "tool" in action and "input" in action:
                    tool_name = action["tool"]
                    tools_used.append(tool_name)
                    tool_result = self._execute_tool(tool_name, action["input"])
                    
                    messages.append({"role": "assistant", "content": assistant_message})
                    messages.append({"role": "user", "content": f"Tool result: {tool_result}"})
            
            return TaskResult(
                task=task,
                result="Maximum steps reached without finding an answer",
                confidence=0.0,
                tools_used=list(set(tools_used)),
                completion_time=datetime.now()
            )
            
        except Exception as e:
            return TaskResult(
                task=task,
                result=f"Error processing task: {str(e)}",
                confidence=0.0,
                tools_used=list(set(tools_used)),
                completion_time=datetime.now(),
                error=str(e)
            )

def main(task_file_path: str, output_file_path: str):
    # Initialize tools
    tools = {
        "google_search": GoogleSearchTool(os.getenv("SERPER_API_KEY")),
        "web_scraper": WebScraperTool()
    }
    
    # Initialize agent
    agent = Agent(os.getenv("OPENAI_API_KEY"), tools)
    
    # Read tasks
    with open(task_file_path, 'r') as f:
        tasks = f.readlines()
    
    # Process tasks and collect results
    results = []
    for task in tasks:
        task = task.strip()
        if not task:
            continue
            
        result = agent.process_task(task)
        results.append({
            "task": result.task,
            "result": result.result,
            "confidence": result.confidence,
            "tools_used": result.tools_used,
            "completion_time": result.completion_time.isoformat(),
            "error": result.error
        })
    
    # Write results
    with open(output_file_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script.py <task_file_path> <output_file_path>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])