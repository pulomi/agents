from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task



@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['business_analyst'],
            verbose=True,
        )

    @agent
    def solutions_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['solutions_architect'],
            verbose=True,
        )
    
    @agent
    def penetration_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['penetration_tester'],
            verbose=True,
            allow_delegation=False,  # Security should focus on assessment
        )

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
            allow_delegation=True
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_delegation=False,  # Backend should focus on implementation
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
            allow_delegation=False,  # Frontend should focus on UI
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_delegation=False,  # QA should focus on testing
        )

    @task
    def requirements_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirements_analysis_task'],
        )

    @task
    def solutions_architect_task(self) -> Task:
        return Task(
            config=self.tasks_config['solutions_architect_task'],
        )

    @task
    def technical_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_design_task'],
        )

    @task
    def backend_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_task'],
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task
    def code_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_review_task'],
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
        ) 

    @task
    def penetration_test_task(self) -> Task:
        return Task(
            config=self.tasks_config['penetration_test_task'],
        ) 

    @crew
    def crew(self) -> Crew:
        """Creates the engineering team crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=True,
            verbose=True,
        )