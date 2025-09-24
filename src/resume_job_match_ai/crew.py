from typing import List

from crewai import Agent, Crew, Process, Task, TaskOutput
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from resume_job_match_ai.tools import (
    SerperDevTool,
    extract_job_description,
    extract_resume,
    save_resume_as_pdf,
)


@CrewBase
class ResumeJobMatchAi:
    """ResumeMatchAi crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    tasks_config: dict  # Add this line to define tasks_config
    agents_config: dict  # Add this line to define agents_config

    @agent
    def resume_analyst(self) -> Agent:
        """
        Creates and returns an Agent instance configured as a resume analyst.

        The agent uses the configuration specified in 'agents_config' under
        the 'resume_analyst' key. It operates in verbose mode,
        with a maximum of 10 requests per minute
        and a maximum execution time of 5 minutes.

        Returns:
            Agent: An initialized Agent object for analyzing resumes.
        """
        return Agent(
            config=self.agents_config["resume_analyst"],  # type: ignore[index]
            verbose=True,
            tools=[extract_resume],
            max_rpm=10,  # Requests per minute
            # max_execution_time=300,  # 5 minutes timeout
        )

    @agent
    def matchmaker(self) -> Agent:
        """
        Creates and returns an Agent instance configured as a matchmaker.

        The matchmaker agent is initialized with specific configuration parameters,
        including verbosity, request rate limiting, and execution timeout. It is
        intended to facilitate matching operations, such as pairing resumes with job
        descriptions.

        Returns:
            Agent: An instance of the Agent class configured for matchmaking tasks.
        """
        return Agent(
            config=self.agents_config["matchmaker"],  # type: ignore[index]
            verbose=True,
            tools=[extract_job_description],
            max_rpm=10,  # Requests per minute
            # max_execution_time=300,  # 5 minutes timeout
        )

    @agent
    def web_researcher(self) -> Agent:
        """
        Creates and returns an Agent instance configured as a web researcher.

        The agent is initialized with the 'web_researcher' configuration from the agents_config,
        runs in verbose mode, and is limited to 10 requests per minute with a maximum execution
        time of 5 minutes.

        Returns:
            Agent: An Agent instance configured for web research tasks.
        """
        return Agent(
            config=self.agents_config["web_researcher"],  # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
            max_rpm=10,  # Requests per minute
            # max_execution_time=300,  # 5 minutes timeout
        )

    @agent
    def resume_writer(self) -> Agent:
        """
        Creates and returns an Agent instance configured as a resume writer.

        The Agent is initialized with the 'resume_writer' configuration from the agents_config dictionary.
        It operates in verbose mode, allows up to 10 requests per minute, and has a maximum execution time of 5 minutes.

        Returns:
            Agent: An Agent instance configured for resume writing tasks.
        """
        return Agent(
            config=self.agents_config["resume_writer"],  # type: ignore[index]
            verbose=True,
            tools=[save_resume_as_pdf],
            max_retry_limit=3,
            max_rpm=10,  # Requests per minute
            # max_execution_time=300,  # 5 minutes timeout
        )

    @task
    def resume_analysis_task(self) -> Task:
        """
        Creates and returns a Task instance configured for analyzing resumes.

        Returns:
            Task: An instance of Task initialized with the resume analysis configuration and
            set to output the analyst report to 'output/analyst_report.md'.
        """
        return Task(
            config=self.tasks_config["resume_analysis_task"],  # type: ignore[index]
            # output_file="output/analyst_report.md",
            tools=[extract_resume],
        )

    @task
    def job_matching_task(self) -> Task:
        """
        Creates and returns a Task instance configured for job matching.

        Returns:
            Task: A Task object initialized with the job matching configuration and
            set to output the report to 'output/job_matching_report.md'.
        """
        return Task(
            config=self.tasks_config["job_matching_task"],  # type: ignore[index]
            # output_file="output/job_matching_report.md",
            tools=[extract_job_description],
        )

    @task
    def web_research_task(self) -> Task:
        """
        Creates and returns a Task instance configured for web research.

        Returns:
            Task: An instance of the Task class initialized with the web research task configuration
            and specifying the output file as 'output/web_research_summary.md'.
        """
        return Task(
            config=self.tasks_config["web_research_task"],  # type: ignore[index]
            # output_file="output/web_research_summary.md",
            tools=[SerperDevTool()],
        )

    def callback_function(self, output: TaskOutput):
        # Do something after the task is completed
        # Example: Send an email to the manager
        print(f"""
            Task completed!
            Task: {output.description}
            Agent: {output.agent}
        """)

    @task
    def resume_writer_task(self) -> Task:
        """
        Creates and returns a Task instance configured for the resume writer task.

        Returns:
            Task: An instance of the Task class initialized with the configuration
                specified in 'self.tasks_config["resume_writer_task"]' and the output
                file set to 'output/resume_advising_report.md'.
        """
        return Task(
            config=self.tasks_config["resume_writer_task"],  # type: ignore[index]
            # output_file="output/resume_advising_report.md",
            callback=self.callback_function,
            tools=[save_resume_as_pdf],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ResumeMatchAi crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
