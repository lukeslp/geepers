#!/usr/bin/env python3
"""
Clinical Reference Data Quality Audit
Analyzes all condition index.md files for data quality issues
"""

import re
from pathlib import Path
from collections import defaultdict
import json

class ClinicalDataAuditor:
    def __init__(self, conditions_dir):
        self.conditions_dir = Path(conditions_dir)
        self.conditions = []
        self.issues = defaultdict(list)

    def audit_all_conditions(self):
        """Run comprehensive audit on all conditions"""
        condition_dirs = sorted([d for d in self.conditions_dir.iterdir() if d.is_dir()])

        for condition_dir in condition_dirs:
            index_md = condition_dir / 'index.md'
            if index_md.exists():
                self.audit_condition(condition_dir.name, index_md)

        return self.generate_report()

    def audit_condition(self, slug, filepath):
        """Audit a single condition file"""
        try:
            content = filepath.read_text(encoding='utf-8')

            condition_data = {
                'slug': slug,
                'filepath': str(filepath),
                'word_count': len(content.split()),
                'line_count': len(content.splitlines()),
                'has_html': (filepath.parent / 'index.html').exists()
            }

            # Extract metadata
            condition_data.update(self.extract_metadata(content))

            # Check for issues
            self.check_duplicate_potential(slug, condition_data)
            self.check_medical_accuracy(condition_data, content)
            self.check_data_consistency(condition_data, content)
            self.check_content_quality(condition_data, content)
            self.check_terminology(condition_data, content, slug)

            self.conditions.append(condition_data)

        except Exception as e:
            self.issues['read_errors'].append(f"{slug}: {str(e)}")

    def extract_metadata(self, content):
        """Extract key metadata from markdown content"""
        data = {}

        # Quick Reference data
        qr_match = re.search(r'\|\s*\*\*Incidence\*\*\s*\|\s*(.+?)\s*\|', content)
        data['incidence'] = qr_match.group(1) if qr_match else None

        qr_match = re.search(r'\|\s*\*\*Prevalence\*\*\s*\|\s*(.+?)\s*\|', content)
        data['prevalence'] = qr_match.group(1) if qr_match else None

        qr_match = re.search(r'\|\s*\*\*Gender Distribution\*\*\s*\|\s*(.+?)\s*\|', content)
        data['gender'] = qr_match.group(1) if qr_match else None

        qr_match = re.search(r'\|\s*\*\*Primary Age of Onset\*\*\s*\|\s*(.+?)\s*\|', content)
        data['age_of_onset'] = qr_match.group(1) if qr_match else None

        qr_match = re.search(r'\|\s*\*\*AT/AAC Requirements\*\*\s*\|\s*(.+?)\s*\|', content)
        data['aac_requirements'] = qr_match.group(1) if qr_match else None

        # ICD codes
        icd11_match = re.search(r'\*\*ICD-11:\*\*\s*(.+?)(?:\n|$)', content, re.MULTILINE)
        data['icd11'] = icd11_match.group(1).strip() if icd11_match else None

        icd10_match = re.search(r'\*\*ICD-10-CM:\*\*\s*(.+?)(?:\n|$)', content, re.MULTILINE)
        data['icd10'] = icd10_match.group(1).strip() if icd10_match else None

        # Core characteristics
        etiology_match = re.search(r'\*\*Etiology:\*\*\s*(.+?)(?:\n|$)', content, re.MULTILINE)
        data['etiology'] = etiology_match.group(1).strip() if etiology_match else None

        pathology_match = re.search(r'\*\*Pathology:\*\*\s*(.+?)(?:\n|$)', content, re.MULTILINE)
        data['pathology'] = pathology_match.group(1).strip() if pathology_match else None

        onset_match = re.search(r'\*\*Typical Onset:\*\*\s*(.+?)(?:\n|$)', content, re.MULTILINE)
        data['typical_onset'] = onset_match.group(1).strip() if onset_match else None

        gender_impact_match = re.search(r'\*\*Gender Impact:\*\*\s*(.+?)(?:\n|$)', content, re.MULTILINE)
        data['gender_impact'] = gender_impact_match.group(1).strip() if gender_impact_match else None

        seizure_match = re.search(r'\*\*Seizure Prevalence:\*\*\s*(.+?)(?:\n|$)', content, re.MULTILINE)
        data['seizure_prevalence'] = seizure_match.group(1).strip() if seizure_match else None

        # Count sections
        data['section_count'] = len(re.findall(r'^##\s+', content, re.MULTILINE))

        # Count references
        data['reference_count'] = len(re.findall(r'^\d+\..*?(?:http|doi|DOI)', content, re.MULTILINE))

        # Count images
        data['image_count'] = len(re.findall(r'!\[.*?\]\(.*?\)', content))

        return data

    def check_duplicate_potential(self, slug, data):
        """Check for potential duplicate conditions"""
        # Look for overlapping syndrome names
        syndrome_keywords = ['syndrome', 'disease', 'disorder', 'palsy', 'atrophy', 'dystrophy']

        # Check for similar naming patterns
        for existing in self.conditions:
            if self.names_similar(slug, existing['slug']):
                self.issues['potential_duplicates'].append({
                    'condition1': slug,
                    'condition2': existing['slug'],
                    'reason': 'Similar naming pattern'
                })

    def names_similar(self, name1, name2):
        """Check if two condition names are similar"""
        # Remove common suffixes
        suffixes = ['-syndrome', '-disease', '-disorder']
        clean1 = name1
        clean2 = name2
        for suffix in suffixes:
            clean1 = clean1.replace(suffix, '')
            clean2 = clean2.replace(suffix, '')

        # Check for shared base words (3+ chars)
        words1 = set(w for w in clean1.split('-') if len(w) >= 3)
        words2 = set(w for w in clean2.split('-') if len(w) >= 3)

        shared = words1 & words2
        return len(shared) >= 2

    def check_medical_accuracy(self, data, content):
        """Check medical information for accuracy issues"""
        slug = data['slug']

        # Check incidence/prevalence plausibility
        if data['incidence']:
            if self.extract_numeric_from_incidence(data['incidence']) > 0.5:
                self.issues['accuracy_warnings'].append({
                    'condition': slug,
                    'field': 'incidence',
                    'value': data['incidence'],
                    'issue': 'Incidence seems implausibly high (>1 in 2)'
                })

        # Check ICD code format
        if data['icd11'] and not re.match(r'^[0-9A-Z]{2,6}(?:\.[0-9A-Z]+)?$', data['icd11']):
            self.issues['accuracy_warnings'].append({
                'condition': slug,
                'field': 'icd11',
                'value': data['icd11'],
                'issue': 'ICD-11 code format appears invalid'
            })

        if data['icd10'] and not re.match(r'^[A-Z][0-9]{2}(?:\.[0-9A-Z]+)?$', data['icd10']):
            self.issues['accuracy_warnings'].append({
                'condition': slug,
                'field': 'icd10',
                'value': data['icd10'],
                'issue': 'ICD-10 code format appears invalid'
            })

    def extract_numeric_from_incidence(self, incidence_str):
        """Extract numeric probability from incidence string"""
        try:
            # Match patterns like "1 in 10,000" or "1:10000"
            match = re.search(r'1\s+(?:in|:)\s+([\d,]+)', incidence_str)
            if match:
                denominator = int(match.group(1).replace(',', ''))
                return 1.0 / denominator
            return 0
        except:
            return 0

    def check_data_consistency(self, data, content):
        """Check for data consistency issues"""
        slug = data['slug']

        # Check Quick Reference completeness
        qr_fields = ['incidence', 'prevalence', 'gender', 'age_of_onset', 'aac_requirements']
        missing_qr = [f for f in qr_fields if not data.get(f)]
        if missing_qr:
            self.issues['consistency_issues'].append({
                'condition': slug,
                'issue': 'Incomplete Quick Reference',
                'missing_fields': missing_qr
            })

        # Check Core Characteristics completeness
        core_fields = ['etiology', 'pathology', 'typical_onset', 'gender_impact', 'seizure_prevalence']
        missing_core = [f for f in core_fields if not data.get(f)]
        if missing_core:
            self.issues['consistency_issues'].append({
                'condition': slug,
                'issue': 'Incomplete Core Characteristics',
                'missing_fields': missing_core
            })

        # Check ICD codes present
        if not data['icd11'] and not data['icd10']:
            self.issues['consistency_issues'].append({
                'condition': slug,
                'issue': 'Missing ICD codes',
                'details': 'No ICD-11 or ICD-10 codes found'
            })

        # Check AAC percentage format (should be descriptive, not numeric percentage)
        if data['aac_requirements']:
            aac = data['aac_requirements']
            # Check if it looks like a bare percentage without context
            if re.match(r'^\d+%?\s*$', aac.strip()):
                self.issues['consistency_issues'].append({
                    'condition': slug,
                    'issue': 'AAC requirement format',
                    'value': aac,
                    'details': 'Should be descriptive (e.g., "High - 80-90% benefit") not bare percentage'
                })

    def check_content_quality(self, data, content):
        """Check content quality and completeness"""
        slug = data['slug']

        # Check for very short content
        if data['word_count'] < 500:
            self.issues['quality_issues'].append({
                'condition': slug,
                'issue': 'Very short content',
                'word_count': data['word_count'],
                'details': 'Less than 500 words'
            })

        # Check for placeholder text
        placeholders = ['TODO', 'TBD', 'PLACEHOLDER', 'COMING SOON', '[INSERT', 'FIXME']
        for placeholder in placeholders:
            if placeholder in content.upper():
                self.issues['quality_issues'].append({
                    'condition': slug,
                    'issue': 'Contains placeholder text',
                    'placeholder': placeholder
                })
                break

        # Check for key sections
        required_sections = [
            'Overview',
            'Pathophysiology',
            'Diagnosis',
            'AAC',
            'Management'
        ]

        missing_sections = []
        for section in required_sections:
            if not re.search(rf'#+\s*{section}', content, re.IGNORECASE):
                missing_sections.append(section)

        if missing_sections:
            self.issues['quality_issues'].append({
                'condition': slug,
                'issue': 'Missing key sections',
                'missing': missing_sections
            })

        # Check reference count
        if data['reference_count'] == 0:
            self.issues['quality_issues'].append({
                'condition': slug,
                'issue': 'No references',
                'details': 'No citations found'
            })
        elif data['reference_count'] < 3:
            self.issues['quality_issues'].append({
                'condition': slug,
                'issue': 'Few references',
                'count': data['reference_count'],
                'details': 'Less than 3 citations'
            })

        # Check image count
        if data['image_count'] == 0:
            self.issues['quality_issues'].append({
                'condition': slug,
                'issue': 'No images',
                'details': 'No clinical illustrations'
            })

    def check_terminology(self, data, content, slug):
        """Check terminology consistency"""

        # Extract condition name from slug
        condition_name = slug.replace('-', ' ').title()

        # Check for inconsistent capitalization of condition name
        name_variants = re.findall(rf'\b{re.escape(condition_name)}\b', content, re.IGNORECASE)
        if len(set(name_variants)) > 2:  # Allow for 2 variants (title case and sentence case)
            self.issues['terminology_issues'].append({
                'condition': slug,
                'issue': 'Inconsistent condition name capitalization',
                'variants': list(set(name_variants))[:5]  # Show first 5
            })

        # Check for common medical terminology inconsistencies
        inconsistencies = []

        # Check AAC vs. AAC device inconsistency
        aac_count = len(re.findall(r'\bAAC\b', content))
        aac_device_count = len(re.findall(r'\bAAC device', content, re.IGNORECASE))
        if aac_count > 0 and aac_device_count > 0:
            ratio = aac_device_count / aac_count
            if ratio > 0.5:  # More than half of AAC mentions have "device"
                inconsistencies.append('Mix of "AAC" and "AAC device" - consider standardizing')

        # Check for mixed terminology for same concept
        if 'speech-language pathologist' in content.lower() and 'speech pathologist' in content.lower():
            inconsistencies.append('Mixed use of "speech-language pathologist" and "speech pathologist"')

        if inconsistencies:
            self.issues['terminology_issues'].append({
                'condition': slug,
                'issue': 'Terminology inconsistencies',
                'details': inconsistencies
            })

    def generate_report(self):
        """Generate comprehensive audit report"""
        report = {
            'summary': {
                'total_conditions': len(self.conditions),
                'conditions_with_html': sum(1 for c in self.conditions if c['has_html']),
                'avg_word_count': sum(c['word_count'] for c in self.conditions) / len(self.conditions) if self.conditions else 0,
                'conditions_with_images': sum(1 for c in self.conditions if c['image_count'] > 0),
                'conditions_with_references': sum(1 for c in self.conditions if c['reference_count'] > 0),
                'issue_categories': {k: len(v) for k, v in self.issues.items()}
            },
            'conditions': self.conditions,
            'issues': dict(self.issues)
        }

        return report

def main():
    conditions_dir = Path('/home/coolhand/servers/clinical/conditions')

    print("Starting Clinical Reference Data Quality Audit...")
    print(f"Analyzing conditions in: {conditions_dir}\n")

    auditor = ClinicalDataAuditor(conditions_dir)
    report = auditor.audit_all_conditions()

    # Save full report as JSON
    output_dir = Path('/home/coolhand/geepers/reports/by-date/2026-01-05')
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / 'clinical-data-audit.json'
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"Full audit data saved to: {json_path}")
    print(f"\nTotal conditions analyzed: {report['summary']['total_conditions']}")
    print(f"Average word count: {report['summary']['avg_word_count']:.0f}")
    print(f"\nIssue Summary:")
    for category, count in report['summary']['issue_categories'].items():
        print(f"  {category}: {count}")

    return report

if __name__ == '__main__':
    main()
