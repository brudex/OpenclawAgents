
**🧠 AI Extraction Prompt**

> You will be provided with a document containing exam practice questions. The formatting may vary across documents. Your task is to extract and structure all the questions into a consistent JSON format. Follow the rules and expected format strictly.

### 📘 Document Structure Variations You Might Encounter:

* Some documents are divided into **chapters**, where each chapter contains a **brief explanation**, **a set of questions**, and then **answers and explanations** listed at the end of the chapter.
* Some are organized into **topics**, where **each question is followed immediately by its answer and explanation**.
* Others contain **all questions first**, and then **answers only (no explanation)** at the end of the document.

---

### ✅ Output Format (strictly follow):

```json
[
  {
    "topic": "Topic or Chapter Title",
    "quizTitle": "Title of quiz", //If Quiz begins with a title set it if not use topic as title
    "questions": [
      {
        "questionType": "single-choice", // one of: 'single-choice', 'multi-choice', 'numeric', 'free-text'
        "difficulty": "medium",          // one of: 'easy', 'medium', 'hard'
        "points": 1,
        "translations": [
          {
            "languageCode": "en",
            "questionText": "Full question text",
            "options": {
              "option_1": "First option",
              "option_2": "Second option",
              "option_3": "Third option",
              "option_4": "Fourth option"
            },
            "correctAnswer": [
              "option_2" // always list as an array
            ],
            "explanation": "Short explanation if available, else leave empty string"
          }
        ]
      }
    ]
  }
]
```

---

### 🧾 Instructions:

* **Topic**: Use the chapter or topic title as the value of the `"topic"` field.
* **Question Type**: Default to `"single-choice"` unless it is obviously multiple-choice or numeric/free-text.
* **Difficulty**: If not stated, assume `"medium"` by default.
* **Points**: Always set to `1` unless the document states otherwise.
* **Correct Answer**: Extract this from the answer section, whether it is provided directly after the question or at the end.
* **Explanation**: If available (either immediately after question or at the end), include it. If not available, use `""`.
* **Option Matching**: Ensure the correct answer matches the relevant option key like `"option_1"`, `"option_2"`, etc.

---

### 🧠 Special Considerations:

* Remove any numbering or formatting symbols (e.g., "1.", "A)", "(b)") from questions and options.
* Ignore unrelated text like "Chapter objectives", "Summary", or "Further Reading".
* If options are missing or a question is incomplete, skip the question.

