from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from myapp.models import Finding

class FindingListView(View):
    def get(self, request):
        definition_id = request.GET.get('definition_id', None)
        scan = request.GET.get('scan', None)

        findings = Finding.objects.all()

        if definition_id:
            findings = findings.filter(definition_id = definition_id)

        if scan:
            findings = findings.filter(scans=scan)

        data = [
            {
                'id': finding.id,
                'target_id': finding.target_id,
                'definition_id': finding.definition_id,
                'scans': finding.scans,
                'url': finding.url,
                'path': finding.path,
                'method': finding.method,
            }
            for finding in findings
        ]

        print(findings)
        return JsonResponse(data, safe=False)


