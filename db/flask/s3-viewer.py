from flask import Flask

from flask_s3_viewer import FlaskS3Viewer
from flask_s3_viewer.aws.ref import Region


# Init Flask
app = Flask(__name__)

# Init Flask S3Viewer
s3viewer = FlaskS3Viewer(
    # Flask App
    app,
    # Namespace must be unique
    namespace='flask-s3-viewer',
    # Hostname, e.g. Cloudfront endpoint
    object_hostname='http://flask-s3-viewer.com',
    # Put your AWS's profile name and Bucket name
    config={
        'profile_name': 'PROFILE_NAME',
        'bucket_name': 'S3_BUCKET_NAME'
    }
)

# Register Flask S3Viewer's router
s3viewer.register()

if __name__ == '__main__':
    app.run(debug=True, port=3000)