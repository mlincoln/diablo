"""
Copyright ©2022. The Regents of the University of California (Regents). All Rights Reserved.

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

from flask import current_app as app
import pytest
from xena.models.email import Email
from xena.models.publish_type import PublishType
from xena.models.recording_approval_status import RecordingApprovalStatus
from xena.models.recording_schedule import RecordingSchedule
from xena.models.recording_scheduling_status import RecordingSchedulingStatus
from xena.models.section import Section
from xena.test_utils import util


@pytest.mark.usefixtures('page_objects')
class TestCourseInstructorChanges:

    real_test_data = util.get_test_script_course('test_course_changes_real')
    fake_test_data = util.get_test_script_course('test_course_changes_fake')
    real_section = util.get_test_section(real_test_data)
    real_meeting = real_section.meetings[0]
    fake_section = Section(fake_test_data)
    fake_meeting = fake_section.meetings[0]
    recording_sched = RecordingSchedule(real_section)

    def test_disable_jobs(self):
        self.login_page.load_page()
        self.login_page.dev_auth()
        self.ouija_page.click_jobs_link()
        self.jobs_page.disable_all_jobs()

    def test_delete_old_diablo_and_kaltura(self):
        self.kaltura_page.log_in_via_calnet()
        self.kaltura_page.reset_test_data(self.term, self.recording_sched)
        util.reset_sign_up_test_data(self.real_section)
        self.recording_sched.approval_status = RecordingApprovalStatus.NOT_INVITED
        self.recording_sched.scheduling_status = RecordingSchedulingStatus.NOT_SCHEDULED

    def test_emails_pre_run(self):
        self.jobs_page.load_page()
        self.jobs_page.run_emails_job()

    @pytest.mark.skipif(app.config['SKIP_EMAILS'], reason='Check email')
    def test_delete_old_email(self):
        self.email_page.log_in()
        self.email_page.delete_all_messages()

    # SCHEDULED COURSE CHANGES INSTRUCTOR

    def test_set_fake_instr(self):
        util.change_course_instructor(self.real_section, self.real_section.instructors[0], self.fake_section.instructors[0])

    def test_sign_up_with_fake_instr(self):
        self.ouija_page.load_page()
        self.ouija_page.log_out()
        self.login_page.dev_auth(self.fake_section.instructors[0].uid)
        self.ouija_page.click_sign_up_page_link(self.real_section)
        self.sign_up_page.select_publish_type(PublishType.BCOURSES.value)
        self.sign_up_page.click_agree_checkbox()
        self.sign_up_page.click_approve_button()

    def test_schedule_recordings_with_fake_instr(self):
        self.sign_up_page.log_out()
        self.login_page.dev_auth()
        self.ouija_page.click_jobs_link()
        self.jobs_page.run_kaltura_job()
        util.get_kaltura_id(self.recording_sched, self.term)

    def test_revert_to_real_instr(self):
        util.change_course_instructor(self.real_section, self.fake_section.instructors[0], self.real_section.instructors[0])

    def test_run_email_job_with_instr_change(self):
        self.jobs_page.run_emails_job()
        self.recording_sched.approval_status = RecordingApprovalStatus.INVITED

    def test_run_kaltura_no_change(self):
        self.jobs_page.run_kaltura_job()
        self.sign_up_page.load_page(self.real_section)
        self.sign_up_page.click_kaltura_series_link(self.recording_sched)
        self.kaltura_page.wait_for_delete_button()
        course = f'{self.real_section.code}, {self.real_section.number} ({self.term.name})'
        assert self.kaltura_page.visible_series_title() == course
        instr = f'{self.fake_section.instructors[0].first_name} {self.fake_section.instructors[0].last_name}'
        expected_desc = f'{course} is taught by {instr}.'
        assert expected_desc in self.kaltura_page.visible_series_desc()
        assert len(self.kaltura_page.collaborator_rows()) == 1
        assert self.kaltura_page.collaborator_perm(self.fake_section.instructors[0]) == 'Co-Editor, Co-Publisher'
        self.kaltura_page.close_window_and_switch()

    def test_changes_page_summary(self):
        self.sign_up_page.click_course_changes_link()
        self.changes_page.wait_for_course_row(self.real_section)
        expected = 'Instructors are obsolete.'
        actual = self.changes_page.scheduled_card_summary(self.real_section)
        app.logger.info(f'Expecting: {expected}')
        app.logger.info(f'Actual: {actual}')
        assert expected in actual

    def test_changes_page_old_instructor(self):
        fake_instr_name = f'{self.fake_section.instructors[0].first_name} {self.fake_section.instructors[0].last_name}'
        expected = f'{fake_instr_name} ({self.fake_section.instructors[0].uid})'
        actual = self.changes_page.scheduled_card_old_instructors(self.real_section)
        app.logger.info(f'Expecting: {expected}')
        app.logger.info(f'Actual: {actual}')
        assert expected in actual

    def test_changes_page_new_instructor(self):
        real_instr_name = f'{self.real_section.instructors[0].first_name} {self.real_section.instructors[0].last_name}'
        expected = f'{real_instr_name} ({self.real_section.instructors[0].uid})'
        actual = self.changes_page.current_card_instructors(self.real_section, node=None)
        app.logger.info(f'Expecting: {expected}')
        app.logger.info(f'Actual: {actual}')
        assert expected in actual

    # CHECK FILTERS AND ADMIN EMAIL

    def test_filter_all(self):
        self.ouija_page.load_page()
        self.ouija_page.search_for_course_code(self.real_section)
        self.ouija_page.filter_for_all()
        assert self.ouija_page.is_course_in_results(self.real_section) is True

    def test_approval_status(self):
        visible_status = self.ouija_page.course_row_approval_status_el(self.real_section).text.strip()
        assert visible_status == self.recording_sched.approval_status.value

    def test_sched_status(self):
        visible_status = self.ouija_page.course_row_sched_status_el(self.real_section).text.strip()
        assert visible_status == self.recording_sched.scheduling_status.value

    def test_filter_no_email(self):
        self.ouija_page.filter_for_do_not_email()
        assert self.ouija_page.is_course_in_results(self.real_section) is False

    def test_filter_not_invited(self):
        self.ouija_page.filter_for_not_invited()
        assert self.ouija_page.is_course_in_results(self.real_section) is False

    def test_filter_invited(self):
        self.ouija_page.filter_for_invited()
        assert self.ouija_page.is_course_in_results(self.real_section) is False

    def test_filter_partial_approve(self):
        self.ouija_page.filter_for_partially_approved()
        assert self.ouija_page.is_course_in_results(self.real_section) is False

    def test_filter_queued(self):
        self.ouija_page.filter_for_queued_for_scheduling()
        assert self.ouija_page.is_course_in_results(self.real_section) is False

    def test_filter_scheduled(self):
        self.ouija_page.filter_for_scheduled()
        assert self.ouija_page.is_course_in_results(self.real_section) is True

    def test_filter_weird(self):
        self.ouija_page.filter_for_scheduled_weird()
        assert self.ouija_page.is_course_in_results(self.real_section) is False

    @pytest.mark.skipif(app.config['SKIP_EMAILS'], reason='Check email')
    def test_admin_emails_with_instr_change(self):
        subj = f'Course Capture Admin: {self.real_section.code} Instructor changes'
        email = Email(msg_type=None, subject=subj, sender=None)
        assert self.email_page.is_message_delivered(email)

    # UNSCHEDULE AND RESCHEDULE

    def test_unschedule_confirm(self):
        self.sign_up_page.load_page(self.real_section)
        self.sign_up_page.confirm_unscheduling(self.recording_sched)

    def test_changes_page_course_gone(self):
        self.changes_page.load_page()
        self.changes_page.wait_for_results()
        assert not self.changes_page.is_course_row_present(self.real_section)

    def test_real_instr_approves(self):
        self.ouija_page.load_page()
        self.ouija_page.log_out()
        self.login_page.dev_auth(self.real_section.instructors[0].uid)
        self.ouija_page.click_sign_up_page_link(self.real_section)
        self.sign_up_page.select_publish_type(PublishType.BCOURSES.value)
        self.sign_up_page.click_agree_checkbox()
        self.sign_up_page.click_approve_button()

    def test_update_recordings_with_new_instr(self):
        self.sign_up_page.log_out()
        self.login_page.dev_auth()
        self.changes_page.click_jobs_link()
        self.jobs_page.run_kaltura_job()

    def test_new_series_in_kaltura(self):
        util.get_kaltura_id(self.recording_sched, self.term)
        self.sign_up_page.load_page(self.real_section)
        self.sign_up_page.click_kaltura_series_link(self.recording_sched)
        self.kaltura_page.wait_for_delete_button()

    def test_series_collab_count(self):
        assert len(self.kaltura_page.collaborator_rows()) == len(self.real_section.instructors)

    def test_series_collab_rights(self):
        for instr in self.real_section.instructors:
            assert self.kaltura_page.collaborator_perm(instr) == 'Co-Editor, Co-Publisher'
