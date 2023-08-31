from booksmart.api.serializers import AuthorHyperlink
authorhyperlink = AuthorHyperlink

def serializer_errors(errs):
    message_errors = []
    for field_name, field_error in errs.items():
        # new_errors[field_name] = field_error[0]
        err = f"field incorrect: {field_name}<br>type of error: {field_error[0]}"
        message_errors.append(err)
    return message_errors