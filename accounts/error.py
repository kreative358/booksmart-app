from booksmart.api.serializers import AuthorHyperlink
authorhyperlink = AuthorHyperlink

def serializer_errors(errs):
    message_errors = []
    for field_name, field_error in errs.items():
        # new_errors[field_name] = field_error[0]
        err = f"<p class='class_text_info' style='font-weight: bold;'> Field incorrect:<br>- {field_name}<br>type of error:<br>- {field_error[0].replace(',', '<br>- ')}</p>"
        message_errors.append(err)
    return message_errors