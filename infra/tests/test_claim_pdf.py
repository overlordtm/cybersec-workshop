"""PDF slip checks using dummy claim codes; Poppler verifies generated content."""
import csv
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("claim_pdf", Path(__file__).resolve().parents[1] / "print-claim-codes.py")
printer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(printer)


class ClaimPDFTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.csv = self.root / "codes.csv"
        self.pdf = self.root / "slips.pdf"
        self.rows = [{"user": f"udelezenec{100 + n}", "access": "kali",
                      "claim_code": f"TEST-{n:04d}", "active": "yes"} for n in range(1, 12)]
        self.rows += [{"user": "udelezenec201", "access": "wireguard", "claim_code": "TEST-0201", "active": "yes"},
                      {"user": "udelezenec199", "access": "kali", "claim_code": "TEST-0199", "active": "no"},
                      {"user": "admin", "access": "admin", "claim_code": "TEST-0000", "active": "yes"}]
        self.write_csv()

    def write_csv(self):
        with self.csv.open("w", newline="") as f:
            w = csv.DictWriter(f, ["user", "access", "claim_code", "active"])
            w.writeheader()
            w.writerows(self.rows)

    @unittest.skipUnless(shutil.which("pdfinfo") and shutil.which("pdftotext"), "Poppler tools needed for PDF content checks")
    def test_pagination_a4_and_exactly_one_slip_per_active_participant(self):
        self.assertEqual(printer.generate_pdf(self.csv, self.pdf), (12, 2))
        self.assertEqual(self.pdf.stat().st_mode & 0o777, 0o600)
        info = subprocess.check_output(["pdfinfo", str(self.pdf)], text=True)
        self.assertRegex(info, r"Pages:\s+2")
        self.assertIn("(A4)", info)
        text = subprocess.check_output(["pdftotext", "-layout", str(self.pdf), "-"], text=True)
        pages = text.split('\f')
        self.assertEqual(pages[0].count('TEST-'), 10)
        self.assertEqual(pages[1].count('TEST-'), 2)
        for row in self.rows:
            expected = int(row['active'] == 'yes' and row['access'] in ('kali', 'wireguard'))
            self.assertEqual(text.count(row['claim_code']), expected)
            if expected:
                self.assertEqual(text.count(row['user']), 1)
        self.assertIn('Kali v brskalniku', text)
        self.assertIn('Lastna Kali VM / WireGuard', text)
        self.assertEqual(printer.generate_pdf(self.csv, self.pdf, access="wireguard"), (1, 1))

    def test_filter_validation_and_failure_keeps_existing_output(self):
        self.assertEqual(len(printer.read_codes(self.csv, "kali")), 11)
        self.assertEqual(len(printer.read_codes(self.csv, "wireguard")), 1)
        self.pdf.write_bytes(b"previous output")
        for invalid_url in ('http://example.org/', 'https://example.org/?code=TEST-0001'):
            with self.assertRaises(ValueError):
                printer.generate_pdf(self.csv, self.pdf, url=invalid_url)
        self.rows[0]['claim_code'] = self.rows[1]['claim_code']
        self.write_csv()
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            printer.generate_pdf(self.csv, self.pdf)
        self.assertEqual(self.pdf.read_bytes(), b'previous output')
        self.rows = []
        self.write_csv()
        with self.assertRaisesRegex(ValueError, 'No active'):
            printer.generate_pdf(self.csv, self.pdf)


if __name__ == '__main__':
    unittest.main()
