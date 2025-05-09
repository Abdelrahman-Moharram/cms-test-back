from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings

import math

MODULES_NAMES = {
    'sessions':'sessions',
    'cases':'cases',
    'judgements':'judgements'
}


def paginate_query_set_list(query_set, params, serializer, module, context=None):
    page            = to_int(params.get('page'), 1)
    size            = to_int(params.get('size'), 10)
    
    
    count           = query_set.count()
    instances       = query_set[(page-1)*size : (page) * size]

    return {
        module          : serializer(instances, many=True, context=context).data,
        'total_pages'   : math.ceil(count/size) or 1,
        'page'          : page,
        'size'          : size
    }


def get_file_full_path(path):
    if settings.DEBUG:
        return str(settings.BASE_DIR) +"\\media\\"+path.replace('/', '\\')
    else:
        return str(settings.BASE_DIR) +"/media/"+path


def export_as_excel(data, file_name, excluded_cols=[]):

    df = pd.DataFrame(data)
    
    if excluded_cols and len(data):
        df = df.drop(excluded_cols, axis=1)


    buffer = BytesIO()
    
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.xlsx"'
    
    return response


def export_html_as_pdf(html, file_name):
    config = pdfkit.configuration(wkhtmltopdf=settings.PATH_WKHTMLTOPDF)
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'enable-local-file-access': None,  # Allows access to local files
        'quiet': '',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'disable-smart-shrinking': None,
    }


    pdf = pdfkit.from_string(html, False, options=options,  configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename=file_name
    return response

def export_case_as_pdf(data, file_name):
    template = get_template('pdf/case_details.html')
    # excluded = ['session_id', 'is_executable', 'is_objectionable', 'is_aganist_company', 'id']
    html = template.render({'data': data, 'excluded': ['session_id', 'is_executable', 'is_objectionable', 'is_aganist_company', 'id']})
    return export_html_as_pdf(html, file_name)
    


def export_table_as_pdf(data, file_name, excluded_cols=[]):
    df = pd.DataFrame(data)

    if excluded_cols and len(data):
        df = df.drop(excluded_cols, axis=1)

    columns = df.columns.tolist()
    template = get_template('pdf/datatable.html')
    html = template.render({'data': df.values, 'columns': columns})
    return export_html_as_pdf(html, file_name)



def compare_and_delete_files(query_dict, list_files):
    for f in query_dict:
        if(f.file not in list_files):
            # try:
            #     os.remove( get_file_full_path( str(f.file) ) )
            # except:
            #     pass
            Attachment.objects.filter(file=f.file).delete()


def to_int(val, default):
    if val:
        try:
            val = int(val)
            if val:
                return val
            return default
        except:
            pass
    return default


def date_converter_or_None(date, is_to_hijri=True, row_date=False):
    
    if not date or ('-' in date and '/' in date):
        return      ''
    elif '-' in date:
        date        = date.split('-')
    elif '/' in date:
        date        = date.split('/')
    else:
        return      ''


    if len(date) != 3:
        return      ''
    if is_to_hijri:
        try:
            return Gregorian(year=int(date[0]), month=int(date[1]), day=int(date[2])).to_hijri().dmyformat(separator='-')
        except:
            return  ''
    else:
        try:
            date = Hijri(int(date[2]), int(date[1]), int(date[0])).to_gregorian()
            if row_date:
                return date
            return date.isoformat()
        except:
            return  ''


