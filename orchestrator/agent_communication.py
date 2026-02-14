#!/usr/bin/env python3
"""
Agent Communication Module

Provides standardized interface for agents to:
- Report progress
- Submit results
- Handle errors
- Communicate with orchestrator
"""

import json
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class AgentStatus(Enum):
    STARTING = "starting"
    RUNNING = "running"
    PROGRESS = "progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentReport:
    agent_id: str
    task_id: str
    status: str
    timestamp: str
    message: Optional[str] = None
    progress: Optional[int] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentCommunicator:
    """Handles all communication between agents and orchestrator."""
    
    def __init__(self, task: Dict[str, Any], result_dir: Path):
        self.task = task
        self.task_id = task["id"]
        self.agent_id = f"agent_{task['type']}_{self.task_id}"
        self.result_dir = Path(result_dir)
        self.progress_file = self.result_dir / "progress.json"
        self.result_file = self.result_dir / "result.json"
        self._start_time = time.time()
    
    def _report(self, status: AgentStatus, **kwargs):
        """Send a status report to the orchestrator."""
        report = AgentReport(
            agent_id=self.agent_id,
            task_id=self.task_id,
            status=status.value,
            timestamp=datetime.now().isoformat(),
            **kwargs
        )
        
        # Write progress file (for live monitoring)
        try:
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(asdict(report), f, indent=2)
        except Exception as e:
            print(f"Error writing progress: {e}", file=sys.stderr)
        
        # Also log to stdout for debugging
        print(f"[{report.status}] {report.message or ''}")
    
    def report_start(self):
        """Report that agent has started."""
        self._report(AgentStatus.STARTING, message=f"Agent {self.agent_id} starting")
    
    def report_progress(self, progress: int, message: str = ""):
        """Report progress (0-100)."""
        self._report(
            AgentStatus.PROGRESS,
            progress=max(0, min(100, progress)),
            message=message
        )
    
    def report_result(self, result: Any):
        """Report successful completion with result."""
        elapsed = time.time() - self._start_time
        
        result_data = {
            "success": True,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "completed_at": datetime.now().isoformat(),
            "elapsed_seconds": elapsed,
            "result": result
        }
        
        try:
            with open(self.result_file, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=2)
        except Exception as e:
            print(f"Error writing result: {e}", file=sys.stderr)
        
        self._report(
            AgentStatus.COMPLETED,
            message=f"Task completed in {elapsed:.2f}s",
            result=result
        )
    
    def report_error(self, error: str):
        """Report failure with error message."""
        elapsed = time.time() - self._start_time
        
        result_data = {
            "success": False,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "failed_at": datetime.now().isoformat(),
            "elapsed_seconds": elapsed,
            "error": error
        }
        
        try:
            with open(self.result_file, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=2)
        except Exception as e:
            print(f"Error writing error result: {e}", file=sys.stderr)
        
        self._report(
            AgentStatus.FAILED,
            message=f"Task failed after {elapsed:.2f}s",
            error=error
        )


class AgentRunner:
    """Base class for agent implementations."""
    
    def __init__(self, task: Dict[str, Any], result_dir: str):
        self.task = task
        self.task_id = task["id"]
        self.task_type = task["type"]
        self.description = task["description"]
        self.result_dir = Path(result_dir)
        self.communicator = AgentCommunicator(task, self.result_dir)
        self._handlers: Dict[str, Callable] = {}
    
    def register_handler(self, task_type: str, handler: Callable):
        """Register a handler for a specific task type."""
        self._handlers[task_type] = handler
    
    def execute(self):
        """Execute the task with proper error handling."""
        self.communicator.report_start()
        
        try:
            # Find appropriate handler
            handler = self._handlers.get(self.task_type)
            
            if not handler:
                # Try to find in agent config
                handler = self._load_handler_from_config()
            
            if not handler:
                raise ValueError(f"No handler registered for task type: {self.task_type}")
            
            # Execute handler
            result = handler(self.task, self.communicator)
            
            # Report success
            self.communicator.report_result(result)
            
        except Exception as e:
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            print(error_msg, file=sys.stderr)
            self.communicator.report_error(error_msg)
            sys.exit(1)
    
    def _load_handler_from_config(self) -> Optional[Callable]:
        """Load handler based on agent configuration."""
        config_path = Path(__file__).parent / "agents" / f"{self.task_type}_agent.json"
        
        if not config_path.exists():
            return None
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            handler_type = config.get("handler_type", "default")
            
            if handler_type == "scrape":
                return self._create_scrape_handler(config)
            elif handler_type == "code":
                return self._create_code_handler(config)
            elif handler_type == "research":
                return self._create_research_handler(config)
            else:
                return self._create_default_handler(config)
                
        except Exception as e:
            print(f"Error loading handler config: {e}", file=sys.stderr)
            return None
    
    def _create_default_handler(self, config: Dict) -> Callable:
        """Create a default handler that just echoes the task."""
        def handler(task: Dict, comm: AgentCommunicator):
            comm.report_progress(50, "Processing task...")
            time.sleep(1)  # Simulate work
            return {
                "task_type": task["type"],
                "description": task["description"],
                "config_used": config.get("name", "unknown"),
                "message": "Task processed by default handler"
            }
        return handler
    
    def _create_scrape_handler(self, config: Dict) -> Callable:
        """Create a handler for web scraping tasks."""
        def handler(task: Dict, comm: AgentCommunicator):
            comm.report_progress(10, "Initializing scraper...")
            
            # Simulate scraping workflow
            steps = config.get("steps", ["fetch", "parse", "extract", "save"])
            progress_per_step = 90 // len(steps)
            
            results = []
            for i, step in enumerate(steps):
                comm.report_progress(10 + (i * progress_per_step), f"Executing: {step}")
                time.sleep(0.5)  # Simulate step execution
                results.append({"step": step, "status": "completed"})
            
            comm.report_progress(100, "Scraping complete")
            
            return {
                "scraped_items": len(results),
                "steps_completed": results,
                "source": task["description"][:100]
            }
        return handler
    
    def _create_code_handler(self, config: Dict) -> Callable:
        """Create a handler for code generation tasks."""
        def handler(task: Dict, comm: AgentCommunicator):
            comm.report_progress(10, "Analyzing requirements...")
            time.sleep(0.5)
            
            comm.report_progress(30, "Generating code...")
            time.sleep(1)
            
            comm.report_progress(70, "Reviewing generated code...")
            time.sleep(0.5)
            
            comm.report_progress(100, "Code generation complete")
            
            # Simulate code output
            code = f"# Auto-generated code for: {task['description'][:50]}...\n"
            code += "def main():\n"
            code += "    pass  # TODO: Implement\n"
            
            return {
                "files_generated": 1,
                "lines_of_code": code.count('\n'),
                "code_preview": code[:200],
                "language": config.get("language", "python")
            }
        return handler
    
    def _create_research_handler(self, config: Dict) -> Callable:
        """Create a handler for research tasks."""
        def handler(task: Dict, comm: AgentCommunicator):
            comm.report_progress(10, "Planning research...")
            time.sleep(0.5)
            
            comm.report_progress(30, "Gathering sources...")
            time.sleep(1)
            
            comm.report_progress(60, "Analyzing findings...")
            time.sleep(1)
            
            comm.report_progress(90, "Compiling report...")
            time.sleep(0.5)
            
            comm.report_progress(100, "Research complete")
            
            return {
                "sources_checked": 5,
                "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
                "research_topic": task["description"][:100],
                "report_length": "medium"
            }
        return handler


def create_result_submission(task_id: str, result: Any, result_dir: Path) -> bool:
    """Standalone function for agents to submit results directly."""
    try:
        result_file = Path(result_dir) / "result.json"
        result_data = {
            "success": True,
            "task_id": task_id,
            "completed_at": datetime.now().isoformat(),
            "result": result
        }
        
        result_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error submitting result: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # Test mode
    print("Agent Communication Module - Test Mode")
    
    test_task = {
        "id": "test123",
        "type": "test",
        "description": "Test task for communication module"
    }
    
    test_dir = Path("./test_results")
    test_dir.mkdir(exist_ok=True)
    
    runner = AgentRunner(test_task, str(test_dir))
    
    def test_handler(task, comm):
        for i in range(5):
            comm.report_progress(i * 20, f"Step {i+1}/5")
            time.sleep(0.5)
        return {"message": "Test completed successfully"}
    
    runner.register_handler("test", test_handler)
    runner.execute()
    
    print("Test completed. Check test_results/ for output.")
