from telegram_pipe.filter_utils import CustomFilter


class WordLookupFilter(CustomFilter):
    def __init__(self, positive: list[str], negative: list[str]):
        """Filters messages that contain a word from a list of positive words
        and don't contain a word from a list of negative words.

        Args:
            positive (str | list[str]): List of words that must be in the
                message.
            negative (str | list[str]): List of words that must not be in the
                message.
        """
        self.positive = positive
        self.negative = negative

    def func(self, text: str) -> bool:
        text = text.lower()
        return all(word in text for word in self.positive) and not any(
            word in text for word in self.negative
        )


# Dict of filters that can be used in the pipelines.yaml file
available_filters = {
    'job_filter': WordLookupFilter(positive=['python'], negative=['senior']),
}
