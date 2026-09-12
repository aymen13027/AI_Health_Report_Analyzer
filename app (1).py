
import gradio as gr
import pytesseract
from PIL import Image
import re


# ==============================
# REPORT TEST DATABASE
# ==============================

REPORT_TESTS = {

    "Complete Blood Count (CBC)": [
        "hemoglobin",
        "total leukocyte count",
        "neutrophils",
        "lymphocyte",
        "eosinophils",
        "monocytes",
        "basophils",
        "platelet count",
        "total rbc count",
        "hematocrit",
        "hct",
        "mcv",
        "mch",
        "mchc"
    ],

    "Blood Sugar Fasting": [
        "glucose",
        "fasting blood sugar",
        "fbs"
    ],

    "HbA1c": [
        "hba1c",
        "glycated hemoglobin"
    ],

    "Lipid Profile": [
        "total cholesterol",
        "triglycerides",
        "hdl",
        "ldl",
        "vldl"
    ],

    "Liver Function Test": [
        "bilirubin",
        "sgpt",
        "alt",
        "sgot",
        "ast",
        "albumin",
        "alkaline phosphatase"
    ],

    "Kidney Function Test": [
        "creatinine",
        "urea",
        "uric acid",
        "egfr"
    ],

    "Thyroid Profile": [
        "tsh",
        "t3",
        "t4"
    ],

    "Vitamin D": [
        "vitamin d",
        "25-oh vitamin d"
    ],

    "Vitamin B12": [
        "vitamin b12",
        "b12"
    ],

    "Calcium": [
        "calcium"
    ],

    "Iron Studies": [
        "iron",
        "ferritin",
        "tibc",
        "transferrin"
    ]
}


# ==============================
# CHECK VALUE
# ==============================

def check_value(value, minimum, maximum):

    if minimum <= value <= maximum:
        return "✅ Within Reported Range"

    return "⚠️ Outside Reported Range"


# ==============================
# READ REPORT
# ==============================

def read_report(image_path):

    if image_path is None:
        return "❌ Please upload or take a report picture."

    try:

        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        if not text.strip():
            return "❌ No readable text found."

        return text

    except Exception as e:

        return f"❌ Error reading report: {e}"


# ==============================
# ANALYZE REPORT
# ==============================

def analyze_report(report_type, report_text):

    if not report_text or not report_text.strip():
        return "❌ Please read the report first."

    if report_type not in REPORT_TESTS:
        return "❌ Please select a report type."

    selected_tests = REPORT_TESTS[report_type]

    findings = []

    for line in report_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        lower_line = line.lower()

        for test in selected_tests:

            if test in lower_line:

                numbers = re.findall(
                    r"\d[\d,]*(?:\.\d+)?",
                    line
                )

                numbers = [
                    float(n.replace(",", ""))
                    for n in numbers
                ]

                if len(numbers) >= 3:

                    value = numbers[0]
                    minimum = numbers[-2]
                    maximum = numbers[-1]

                    status = check_value(
                        value,
                        minimum,
                        maximum
                    )

                    findings.append(
                        f"### 🧪 {test.title()}\n\n"
                        f"**Result:** {value}\n\n"
                        f"**Reported Range:** "
                        f"{minimum} - {maximum}\n\n"
                        f"**Status:** {status}"
                    )

                else:

                    findings.append(
                        f"### 🧪 {test.title()}\n\n"
                        f"**Report line:** `{line}`\n\n"
                        f"⚠️ Reference range could not be "
                        f"determined automatically."
                    )

                break

    if not findings:

        return """
# ❌ No matching tests detected

Please make sure:

1. The report picture is clear.
2. The correct report type is selected.
3. The report text was successfully extracted.
"""

    return f"""
# 📋 {report_type} Analysis

{"---".join(findings)}

---

## 🇵🇰 آسان اردو

یہ analysis آپ کی report میں موجود information
اور printed reference ranges کی بنیاد پر ہے۔

اگر کوئی value واضح طور پر سمجھ نہ آئے تو app
خود سے reference range نہیں بناتا۔

---

## ⚠️ Important

This tool provides educational information only.
It does not provide a medical diagnosis or medication advice.

For concerning or unclear findings, discuss the report
with a qualified healthcare professional.
"""


# ==============================
# ASK QUESTION
# ==============================

def ask_question(report_text, question):

    if not report_text or not report_text.strip():
        return "❌ Please read a report first."

    if not question or not question.strip():
        return "❌ Please enter a question."

    q = question.lower()

    if "hemoglobin" in q or "haemoglobin" in q:

        return """
### 🩸 Hemoglobin

Hemoglobin is a protein in red blood cells that helps
carry oxygen around the body.

### 🇵🇰 آسان اردو

Hemoglobin خون کے سرخ خلیوں میں موجود ایک پروٹین ہے
جو جسم میں آکسیجن پہنچانے میں مدد کرتا ہے۔

⚠️ Educational information only.
"""

    elif "platelet" in q:

        return """
### 🩸 Platelets

Platelets are involved in normal blood clotting.

### 🇵🇰 آسان اردو

Platelets خون جمنے کے عام عمل میں مدد کرتے ہیں۔

⚠️ Educational information only.
"""

    elif "wbc" in q or "white blood" in q:

        return """
### 🦠 WBC

White blood cells are part of the body's immune system.

### 🇵🇰 آسان اردو

White Blood Cells جسم کے immune system کا حصہ ہوتے ہیں۔

⚠️ Educational information only.
"""

    elif "glucose" in q or "sugar" in q:

        return """
### 🍬 Glucose

Glucose is a type of sugar in the blood that provides
energy to the body.

### 🇵🇰 آسان اردو

Glucose خون میں موجود ایک قسم کی شکر ہے جو جسم کو
توانائی فراہم کرتی ہے۔

⚠️ Educational information only.
"""

    elif "tsh" in q or "thyroid" in q:

        return """
### 🦋 TSH / Thyroid

TSH is a hormone-related test commonly used when
evaluating thyroid function.

### 🇵🇰 آسان اردو

TSH ایک hormone-related test ہے جو thyroid function
کو evaluate کرنے میں استعمال ہوتا ہے۔

⚠️ Educational information only.
"""

    elif "vitamin d" in q:

        return """
### ☀️ Vitamin D

Vitamin D is important for bones and several body functions.

### 🇵🇰 آسان اردو

Vitamin D ہڈیوں اور جسم کے کئی functions کے لیے اہم ہے۔

⚠️ Educational information only.
"""

    else:

        return f"""
### 🔎 Your Question

**{question}**

The current free version can provide basic educational
information about common report tests.

Try asking about:

- Hemoglobin
- WBC
- Platelets
- Glucose
- TSH
- Vitamin D

⚠️ For concerning or unclear findings, discuss the report
with a qualified healthcare professional.
"""


# ==============================
# GRADIO APP
# ==============================

with gr.Blocks(
    title="AI Health Report Analyzer"
) as app:

    gr.Markdown("""
    # 🩺 AI Health Report Analyzer

    ### Understand your health report in simple English + Urdu

    📷 Upload a report picture or take a picture using your camera.

    ⚠️ This is an educational tool and does not provide a diagnosis.
    """)

    with gr.Row():

        with gr.Column():

            report_image = gr.Image(
                sources=["upload", "webcam"],
                type="filepath",
                label="📷 Upload / Camera"
            )

            report_type = gr.Dropdown(
                choices=list(REPORT_TESTS.keys()),
                label="📋 Select Report Type",
                value="Complete Blood Count (CBC)"
            )

            read_button = gr.Button(
                "📖 Read Report",
                variant="primary"
            )

            report_text = gr.Textbox(
                label="📄 Extracted Report Text",
                lines=12
            )

            analyze_button = gr.Button(
                "🔍 Analyze Report",
                variant="primary"
            )

        with gr.Column():

            analysis_output = gr.Markdown()

            gr.Markdown("---")

            gr.Markdown(
                "## 🔎 Ask a Question About Your Report"
            )

            question = gr.Textbox(
                label="Your Question",
                placeholder="Example: What does hemoglobin mean?"
            )

            ask_button = gr.Button(
                "💬 Ask Question"
            )

            answer_output = gr.Markdown()


    read_button.click(
        fn=read_report,
        inputs=report_image,
        outputs=report_text
    )

    analyze_button.click(
        fn=analyze_report,
        inputs=[report_type, report_text],
        outputs=analysis_output
    )

    ask_button.click(
        fn=ask_question,
        inputs=[report_text, question],
        outputs=answer_output
    )


app.launch()
