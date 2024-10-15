from my_imports import *

app = Flask(__name__)



@app.route("/")
def index():
    # Render the index page
    THIS_FOLDER = Path(__file__).parent.resolve()
    myfile = "index.html"
    return render_template(myfile)

def read_file_lines(filename):
    """Read and return all lines from a file."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def read_csv_file(filename):
    """Read a CSV file and return the headers and rows."""
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader, [])
        rows = [row for row in reader]
    return headers, rows

def format_text_with_paragraphs(text_lines):
    """Format text with HTML paragraph tags."""
    text_with_paragraphs = "".join(text_lines).replace("\n","</p><p>")
    return f'<p>{text_with_paragraphs}</p>'

@app.route("/about")
def about():
    """Render the about page with data from bio.txt, summary.txt, and summary.csv."""
    THIS_FOLDER = Path(__file__).parent.resolve()
    myfile = "bio.txt"
    bio_lines = read_file_lines(myfile)
    image_url = bio_lines[0]
    heading = bio_lines[1]
    text = format_text_with_paragraphs(bio_lines[2:])

    myfile = THIS_FOLDER / "summary.txt"

    title = read_file_lines(myfile)[0]
    myfile = "summary.csv"
    headers, rows = read_csv_file(myfile)

    return render_template('about.html', image_url=image_url, heading=heading, text=text, title=title, headers=headers, rows=rows)


def load_portfolio_entries(filepath):
    """Load and return portfolio entries from a text file."""
    entries = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            content = file.read().strip().split("\n\n")
            for entry in content:
                entry_lines = entry.strip().split("\n")
                if len(entry_lines) >= 4:  # Ensure necessary fields exist
                    title, image_url = entry_lines[:2]

                    summary_lines = []
                    for line in entry_lines[2:]:
                        if line.strip() == '**':
                            break
                        summary_lines.append(line)

                    # Process summary lines to replace anchor tags with HTML links
                    processed_summary_lines = []
                    for line in summary_lines:
                        # Check if the line contains an anchor tag pattern
                        if '<a href="' in line:
                            # Directly add lines with anchor tags
                            processed_summary_lines.append(line)
                        else:
                            # For other lines, convert them to plain text
                            processed_summary_lines.append(line)

                    # Join summary lines with <br> to preserve line breaks in HTML
                    summary = "<br>".join(processed_summary_lines).strip()

                    hyperlink = entry_lines[-1]
                    if hyperlink == "<>":
                        hyperlink = ""

                    # Remove the hyperlink from the summary if it appears
                    if hyperlink in summary:
                        summary = summary.replace(hyperlink, "").strip()

                    if title and summary:
                        entries.append({
                            'title': title,
                            'image_url': image_url,
                            'summary': summary,
                            'hyperlink': hyperlink
                        })
    return entries


@app.route('/portfolio')
def portfolio():
    """Render the portfolio page with entries from a file."""
    THIS_FOLDER = Path(__file__).parent.resolve()
    myfile = "portfolio_entries.txt"
    entries = load_portfolio_entries(myfile)
    return render_template('portfolio.html', entries=entries)


def send_contact_email(name, email, message):
    """Send an email with contact form details."""
    msg = MIMEText(message)
    msg["Subject"] = "Contact Form Submission"
    msg["From"] = email
    msg["To"] = "danhathway@gmail.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("danhathway@gmail.com", os.environ["gmail_key"])
        server.send_message(msg)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Handle contact form submission."""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        try:
            send_contact_email(name, email, message)
        except Exception as e:
            print("Error sending email:", e)
            return redirect(url_for('contact', _anchor='error'))

        return redirect(url_for('contact', _anchor='success'))

    return render_template("contact.html")

def send_email_via_smtp(name, email, message):
    """Send an email using SMTP with the provided details."""
    gmail_key = os.getenv('gmail_key')
    if not gmail_key:
        return "Gmail key not set in environment variables", 500

    sender_email = 'danhathway@gmail.com'
    receiver_email = 'danhathway@gmail.com'
    subject = 'Contact Form Submission'
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, gmail_key)
        server.send_message(msg)

@app.route("/send", methods=["POST"])
def send_email():
    """Handle the sending of email when form is submitted."""
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    try:
        return send_email_via_smtp(name, email, message)
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
