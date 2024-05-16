def validate_word_limit(value):
    word_limit = 100  # Set the desired word limit here

    words = value.split()
    if len(words) > word_limit:
        raise ValidationError(
            _('The text must not exceed %(limit)d words.'),
            code='word_limit',
            params={'limit': word_limit},
        )
