case_number_pattern         = '^[1-9][0-9]{2,20}$'
phone_number_pattern        = '^[0-9]{8}$'
identity_number_pattern     = '^[1-9][0-9]{9}$'
hijri_date_pattern          = '^([٠-٢]?[٠-٩])-([٠-١]?[٠-٩])-(١[٣-٤][٠-٩][٠-٩]|[١٢][٠-٩][٠-٩][٠-٩])$'
judgemen_number_pattern     = '[1-9][0-9]{2,}$'
amount_pattern              = '^[0-9.]+$'
username_pattern            = '^[a-zA-Z][a-zA-Z0-9_. -]{2,}$'
ar_name_pattern             = '^[ء-ي][ء-ي ]{5,}$'
common_en_name_pattern      = '^[a-zA-Z]{2,}$'
common_ar_name_pattern      = '^[ء-ي][ء-ي ]{2,}$'
email_pattern               = '^[a-zA-Z][A-Za-z0-9-_.]+@[a-z.]+.[a-z]{2,3}$'


case_number_regex           = {'pattern':case_number_pattern,      'message':'رقم القضية يجب أن يحتوي على أرقام فقط ولا يقل عن ثلاثة أرقام ولا يزيد عن 20 رقما'}
username_regex              = {'pattern':username_pattern,         'message':'اسم المستخدم يجب ان يبدأ بأحرف ويحتوي على 3 أحرف على الأقل ولا يحتوي على [+%$#/|\\!]'}
ar_name_regex               = {'pattern':ar_name_pattern,          'message':'اسم المستخدم باللغة العربية يجب ان يكون كاملا باللغة العربية و بدون أرقام ولا يقل عن 5 أحرف'}
common_ar_name_regex        = {'pattern':common_ar_name_pattern,   'message':'يجب ان يكون كاملا باللغة العربية و بدون أرقام ولا يقل عن 2 أحرف'}
common_en_name_regex        = {'pattern':common_en_name_pattern,   'message':'يجب ان يكون كاملا باللغة الإنجليزية و بدون أرقام ولا يقل عن 2 أحرف'}
phone_number_regex          = {'pattern':phone_number_pattern,     'message':'يجب أن يحتوي يبدأ رقم الجوال على 8 أرقام بعد (9665+)'}
judgement_number_regex      = {'pattern':judgemen_number_pattern,  'message':'رقم الحكم يجب أن يحتوي على أرقام فقط ويحتوي على 3 أرقام أو أكثر'}
amount_regex                = {'pattern':amount_pattern,           'message':'يجب أن يحتوي الملبغ على أرقام فقط'}
identity_number_regex       = {'pattern':identity_number_pattern,  'message':'رقم الهوية يجب أن يحوي على 10 أرقام ولا يبدأ ب "0"'}
email_regex                 = {'pattern':email_pattern,            'message':'البريد الإلكتروني غير صالح "example@domain.com" '}