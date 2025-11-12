from flask import Flask, request, send_file
import tempfile
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ LaTeX PDF API is running!"
@app.route('/health', methods=['GET'])
def health():
    return "OK", 200

@app.route("/compile", methods=["POST"])
def compile_pdf():
    # Get the LaTeX code from Make.com (as plain text or JSON)
    latex_code = request.get_data(as_text=True)
    if not latex_code:
        return "Error: No LaTeX content received.", 400

    # Create a temporary directory for compilation
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "document.tex")
        pdf_path = os.path.join(tmpdir, "document.pdf")

        # Write the LaTeX code to a .tex file
        with open(tex_path, "w") as f:
            f.write(latex_code)

        # Run pdflatex (requires TeX Live)
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_path],
                cwd=tmpdir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            return f"LaTeX compilation failed:\n{e.stderr.decode()}", 500

        # Return the generated PDF
        return send_file(pdf_path, as_attachment=True, download_name="output.pdf")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
