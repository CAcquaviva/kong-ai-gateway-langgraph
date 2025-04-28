from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:80/agent-route",
    api_key="dummy"
)

# 🧠 Initial ReAct-style prompt
def build_prompt(task: str) -> str:
    return f"""
You are an intelligent AI agent solving problems using the ReAct pattern.

Follow this format:
Thought: What are you thinking?
Action: The action you are taking
Observation: (result from imaginary action)
Thought: ...
FINAL_ANSWER: <your final answer>

Task: {task}

Each time you respond, you should only give **one logical step** in your reasoning process.
Do not jump to the final answer immediately.
Each step should be presented using the format above.

Begin.

Thought:
"""

# 🔁 Reasoning loop with no tools
def run_simple_react_agent(task: str, max_steps: int = 10):
    prompt = build_prompt(task)

    for step in range(max_steps):
        print(f"\n🌀 Step {step + 1}")
        
        response = client.chat.completions.create(
            model="",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        output = response.choices[0].message.content.strip()
        print(output)

        prompt += output + "\n"

        if "FINAL_ANSWER:" in output:
            print("\n✅ Agent finished.")
            break

        # Continue loop by cueing next Thought
        prompt += "Thought:\n"
    else:
        print("\n⏳ Max steps reached without a final answer.")




# ✅ Run example
run_simple_react_agent("Taking the 'The Grapes of Wrath' novel by John Steinbeck, what are the main differences when comparing it to the movie?")
