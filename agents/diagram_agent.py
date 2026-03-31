from agents.llm_agent import client


def clean_mermaid_output(diagram):
    if not diagram:
        return None

    # Remove unwanted markdown
    diagram = diagram.replace("```mermaid", "")
    diagram = diagram.replace("```", "")
    diagram = diagram.strip()

    # Force correct starting keyword
    if not diagram.lower().startswith("flowchart"):
        diagram = "flowchart TD\n" + diagram

    return diagram


def generate_mermaid_diagram(text):

    prompt = f"""
Generate ONLY valid Mermaid flowchart code.

STRICT RULES:
- Start with: flowchart TD
- No explanation
- No markdown
- No ```
- Do NOT use parentheses ()
- Use simple node text
- Keep it clean and professional
- Maximum 8-12 nodes

Create diagram based on:

{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You generate clean Mermaid flowchart diagrams only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=700
        )

        raw_output = response.choices[0].message.content.strip()

        return clean_mermaid_output(raw_output)

    except Exception as e:
        print("Mermaid Generation Error:", str(e))

        # Safe fallback diagram
        return """flowchart TD
    A[Start] --> B[Process]
    B --> C[End]
"""