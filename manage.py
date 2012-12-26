import os
import sys
from mock_github_api.core import app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = True if '-d' in sys.argv else False
    app.run(host='0.0.0.0', port=port, debug=debug)
