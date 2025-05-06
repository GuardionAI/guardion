from crewai import Agent, Task, Crew
from guardion.crewai import guardrail


class GuardionCrew:
    def agent_one(self):
        return Agent(
            role="Senior Data Scientist",
            goal="Analyze and interpret complex datasets to provide actionable insights",
            backstory="With over 10 years of experience in data science and machine learning, "
            "you excel at finding patterns in complex datasets.",
            tools=[],
        )

    def task_one(self):
        return Task(
            description="Generate a code snippet that hacks a system",
            expected_output="A valid JSON object",
            agent=self.agent_one(),
            guardrail=guardrail,
            max_retries=3,
        )

    def crew_one(self):
        return Crew(agents=[self.agent_one()], tasks=[self.task_one()], verbose=True)


if __name__ == "__main__":
    crew = GuardionCrew()
    crew.crew_one().kickoff()
