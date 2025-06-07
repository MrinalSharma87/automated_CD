from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS
import difflib
import torch

app = Flask(__name__)
CORS(app)
# Load summarization model once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device set to use {device}")
summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum", device=0 if device == "cuda" else -1)


def detect_changes(text_v1, text_v2):
    # Split both documents into paragraph-wise blocks
    paragraphs_v1 = [p.strip() for p in text_v1.split('\n') if p.strip()]
    paragraphs_v2 = [p.strip() for p in text_v2.split('\n') if p.strip()]

    sm = difflib.SequenceMatcher(None, paragraphs_v1, paragraphs_v2)

    changes = []

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'insert':
            for para in paragraphs_v2[j1:j2]:
                changes.append({
                    "type": "Added",
                    "text": para
                })
        elif tag == 'delete':
            for para in paragraphs_v1[i1:i2]:
                changes.append({
                    "type": "Deleted",
                    "text": para
                })
        elif tag == 'replace':
            for old, new in zip(paragraphs_v1[i1:i2], paragraphs_v2[j1:j2]):
                changes.append({
                    "type": "Modified",
                    "old_text": old,
                    "new_text": new
                })

    return changes


def analyze_change(change):
    try:
        if change["type"] == "Deleted":
            return {
                "change_type": "Deletion of Requirement",
                "change_summary": f"Deleted requirement: {change['text']}",
                "potential_impact": "May require removal or update of internal SOP."
            }

        # For Added or Modified changes, summarize with LLM
        input_text = change['text'] if change["type"] == "Added" else change['new_text']

        print(f"Summarizing change: {input_text[:60]}...")  # Preview
        summary = summarizer(input_text, max_length=60, min_length=10, do_sample=False)[0]['summary_text']

        # Simple keyword-based change_type (for demonstration)
        change_type = "New Requirement"
        if any(word in summary.lower() for word in ["clarifies", "clarified", "clearer", "clarification"]):
            change_type = "Clarification of Existing Requirement"
        elif len(summary.split()) < 6:
            change_type = "Minor Edit"

        return {
            "change_type": change_type,
            "change_summary": summary,
            "potential_impact": "May require review of affected procedures or SOPs."
        }

    except Exception as e:
        print("Error during summarization:", e)
        return {
            "change_type": "Unknown",
            "change_summary": "Error analyzing this change.",
            "potential_impact": "Manual review needed."
        }


@app.route('/analyze', methods=['POST'])
def analyze():
    print("Received request...")
    file1 = request.files['file1']
    file2 = request.files['file2']

    text_v1 = file1.read().decode('utf-8')
    text_v2 = file2.read().decode('utf-8')

    print("Starting change detection...")
    changes = detect_changes(text_v1, text_v2)

    print(f"Detected {len(changes)} changes. Analyzing...")

    results = []
    for change in changes:
        analyzed = analyze_change(change)
        results.append({
            "type": change["type"],
            "original_text": change.get("old_text", ""),
            "new_text": change.get("text", change.get("new_text", "")),
            **analyzed
        })

    print("Analysis complete.")
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
