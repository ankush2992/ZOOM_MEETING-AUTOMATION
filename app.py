from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor#+
from zoom import is_link, extract_link, open_link_with_selenium

app = Flask(__name__)


# Create a ThreadPoolExecutor#+
executor = ThreadPoolExecutor(max_workers=5)  # Adjust the number of workers as needed#+
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zoom_link = request.form['zoom_link']
        meeting_duration = request.form['meeting_duration']
        user_name = request.form['user_name']#+

        if not is_link(zoom_link):
            return jsonify({"error": "Invalid Zoom link"}), 400

        extracted_link = extract_link(zoom_link)
        if not extracted_link:
            return jsonify({"error": "Failed to extract Zoom link"}), 400

        try:
            duration = int(meeting_duration)
            if duration <= 0:
                return jsonify({"error": "Duration must be a positive number"}), 400
        except ValueError:
            return jsonify({"error": "Invalid duration"}), 400

        
        # Submit the task to the thread pool#+
        try:#+
            future = executor.submit(open_link_with_selenium, extracted_link, duration, user_name)#+
            return jsonify({"message": f"Joining Zoom meeting for {duration} minutes as {user_name}: {extracted_link}"}), 200#+
        except RuntimeError:#+
            return jsonify({"error": "Server is at capacity. Please try again later."}), 503#+

    # This return statement is for GET requests#+
    return render_template('index.html')#+

if __name__ == '__main__':
    app.run(debug=True)
