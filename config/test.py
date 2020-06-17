"""
Copyright ©2020. The Regents of the University of California (Regents). All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its documentation
for educational, research, and not-for-profit purposes, without fee and without a
signed licensing agreement, is hereby granted, provided that the above copyright
notice, this paragraph and the following two paragraphs appear in all copies,
modifications, and distributions.

Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue,
Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu,
http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED
"AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
ENHANCEMENTS, OR MODIFICATIONS.
"""
import os

# Base directory for the application (one level up from this config file).
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ALERT_INFREQUENT_ACTIVITY_ENABLED = False
ALERT_WITHDRAWAL_ENABLED = False

COURSE_CAPTURE_PILOT_JSON = f'{BASE_DIR}/fixtures/sis/course_capture_pilot.json'

CURRENT_TERM_ID = 2202
CURRENT_TERM_BEGIN = '2020-01-21'
CURRENT_TERM_END = '2020-05-08'

DIABLO_BASE_URL = 'https://manage-test.coursecapture.berkeley.edu'

EB_ENVIRONMENT = 'diablo-test'

FIXTURES_PATH = f'{BASE_DIR}/fixtures'

JOBS_AUTO_START = False
JOBS_SECONDS_BETWEEN_PENDING_CHECK = 0.5

INDEX_HTML = f'{BASE_DIR}/tests/static/test-index.html'

LOGGING_LOCATION = 'STDOUT'

SQLALCHEMY_DATABASE_URI = 'postgres://diablo:diablo@localhost:5432/pazuzu_test'

TESTING = True
