from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	links    = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
	# pdf = pisa.pisaDocument(BytesIO(html.encode("utf8")), result, link_callback=links)
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")),dest=result, link_callback=links)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

