from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from races.models import Season, Race
from races.forms import UploadRaceForm


class UploadRaceFormTest(TestCase):
    def test_upload_race_form_excel_file_label(self):
        form = UploadRaceForm()
        self.assertTrue(
            form.fields['excel_file'].label is None
            or form.fields['excel_file'].label == 'Excel file')

    def test_upload_race_form_xlsx_is_valid(self):
        xlsx_file = SimpleUploadedFile(
            "kings.xlsx",
            b"file_content",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        form = UploadRaceForm(files={'excel_file': xlsx_file})
        self.assertTrue(form.is_valid())

    def test_upload_race_form_pdf_is_not_valid(self):
        pdf_file = SimpleUploadedFile(
            "kings.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        form = UploadRaceForm(files={'excel_file': pdf_file})
        self.assertFalse(form.is_valid())
