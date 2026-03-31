from flask import Flask, render_template, request
from main import get_answer
from agents.retriever_agent import create_retriever
import os
import webbrowser
import threading

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

retriever = None


# 🔹 CLEAN MERMAID FUNCTION (ONLY FOR FLOWCHART)
def clean_mermaid(diagram):
    if not diagram:
        return None

    diagram = diagram.replace("```mermaid", "")
    diagram = diagram.replace("```", "")
    diagram = diagram.strip()

    # Ensure it starts with flowchart
    if not diagram.lower().startswith("flowchart"):
        diagram = "flowchart TD\n" + diagram

    return diagram


@app.route("/", methods=["GET", "POST"])
def index():
    global retriever

    answer_text = ""
    flowchart_code = None
    message = ""

    if request.method == "POST":

        # 📄 Upload PDF
        if "upload_btn" in request.form:
            file = request.files.get("pdf_file")

            if file and file.filename.lower().endswith(".pdf"):
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)

                try:
                    retriever = create_retriever(custom_file=filepath)
                    message = "✅ PDF uploaded successfully."
                except Exception as e:
                    retriever = None
                    message = "❌ Error processing PDF."
                    print("Retriever Error:", e)
            else:
                message = "⚠ Please upload a valid PDF file."

        # ❓ Ask Question
        elif "ask_btn" in request.form:

            if retriever is None:
                message = "⚠ Please upload and process a PDF first."
            else:
                question = request.form.get("question", "").strip()

                if not question:
                    message = "⚠ Please enter a question."
                else:
                    try:
                        result = get_answer(question, retriever)

                        # EXPECT: { "text": "...", "flowchart": "mermaid code" }
                        if isinstance(result, dict):
                            answer_text = result.get("text", "")
                            flowchart_code = clean_mermaid(result.get("flowchart"))
                        else:
                            answer_text = str(result)

                    except Exception as e:
                        print("Answer generation error:", e)
                        message = "❌ Something went wrong while generating answer."

    return render_template(
        "index.html",
        answer=answer_text,
        flowchart=flowchart_code,
        message=message
    )


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True, use_reloader=False)