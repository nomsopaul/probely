import requests
from django.core.management.base import BaseCommand
from myapp.models import Finding

class Command(BaseCommand):
    help = 'Retrieve and store Probely findings for a target in the database'

    def handle(self, *args, **options):
        target_id = 'Tt2f8EyPSTwq'
        api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyZWdpb24iOiJkZWZhdWx0IiwianRpIjoiUUQ3aFlBb3Y3U2JyIn0.Fzu2vUuFG_dYl9wnbR2Qd0CXaiIWZjJkNc7XKESZOMU'
        headers = {'Authorization': f'JWT {api_key}'}

        url = f'https://api.probely.com/targets/{target_id}/findings/'

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() 

            findings = response.json().get('results', [])
            

            for finding_data in findings:
                finding_id = finding_data['id']
                if not Finding.objects.filter(id=finding_id).exists():
                    finding = Finding(
                        id=finding_id,
                        target_id=target_id,
                        definition_id=finding_data['definition_id'],
                        scans=finding_data['scans'],
                        url=finding_data['url'],
                        path=finding_data['path'],
                        method=finding_data['method'],
                    )
                    finding.save()
                    self.stdout.write(f'Saved finding {finding_id} in the database.')
                else:
                    self.stdout.write(f'Finding {finding_id} already exists in the database.')

            attribute_names = set()

            for finding_data in findings:
                attribute_names.update(finding_data.keys())
       
            for name in attribute_names:
                print(name)

        except requests.exceptions.RequestException as e:
            self.stderr.write(f'Error retrieving findings from the API: {str(e)}')

        except (KeyError, ValueError) as e:
            self.stderr.write(f'Error parsing response JSON: {str(e)}')

        except Exception as e:
            self.stderr.write(f'An error occurred: {str(e)}')
