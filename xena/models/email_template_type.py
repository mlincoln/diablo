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

from enum import Enum


class EmailTemplateType(Enum):

    ADMIN_DATE_CHANGE = 'Admin alert: Date change'
    ADMIN_INSTR_CHANGE = 'Admin alert: Instructor change'
    ADMIN_ROOM_CHANGE = 'Admin alert: Room change'
    ADMIN_WEIRD_DATES = 'Admin alert: Weird start/end dates'
    INSTR_AWAITING_APPROVAL = 'Waiting for approval'
    INSTR_INVITATION = 'Invitation'
    INSTR_RECORDINGS_SCHEDULED = 'Recordings scheduled'
    INSTR_ROOM_CHANGE_INELIGIBLE = 'Room change: No longer eligible'
    INSTR_SETTINGS_CHANGE = 'Notify instructor of changes'
