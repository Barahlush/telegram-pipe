# telegram-pipe
An MTProto telegram client, that allows you to collect messages from a set of source chats and channels, filter messages by some set of rules and then forward them into specified destination chats.

## Sample usecases
- Collect specific (e.g. "python middle developer") job vacancies from a set of telegram channels and forward them into one chat.
- Collecting messages with specific content into a database to build a recommender system.
- Creating a news feed from a set of channels and chats.

## Usage
### 1. Create `.env` file
It should contain `API_ID` and `API_HASH` for your telegram account. [Here](https://core.telegram.org/api/obtaining_api_id) is an official guide on how to get them. Here is also an `.env-example` file, that specifies the format.

**Optional:** you can also use a bot to forward the messages. It is better than using client, because with the client all the sent messages are marked as read. In order to use a bot, you **also** need to add a `BOT_TOKEN` variable to the `.env` file.

### 2. Add pipelines 
Open `pipelines.yaml` and add your pipelines in the `yaml` format. Here is an example:
```yaml
pipes:
  - name: "Job Extractor"
    sources:
      - "@young_relocate"
      - "@hrlunapark"
      - "@datasciencejobs"
      - "@gamedevjob"
      - "@remotedevjobs"
      - -123451245

    destinations:
      - -875236302
    filters:
      - job_filter

  - name: News feed
    sources:
      - "@meduza"
      - "@bbcnews"
      - -937814172
      - "@rtnews"

    destinations:
      - -789863182
      - "@my_hot_news"
    filters:
      - news_filter
      - anti_repeat_filter
    listener: "me"
    sender: "bot"
    use_listener_on_fail: True
```

Each pipe has 4 fields:
  - `name`: name of the pipe, may be anything, it's here just for convenience.
  - `sources`: list of telegram chats\channel IDs to listen for. Each ID should be either in the format of `"@channel_name"` or integer ID. You can obtain chat ID [by inviting @RawDataBot to your group](https://stackoverflow.com/a/46247058). To send messages to "Saved Messages" (yourself), just put "me" to the list.
  - `destinations`: list of telegram chats\channel IDs to forward messages to. Each ID should be either in the format of `"@channel_name"` or integer ID.
  - `filters`: list of filters to use. Filters should be defined in the `telegram_pipe/filters.py` file.
  - `listener`: name of the client, which will listen for new messages in the specified sources. One of `"bot"` or `"me"` for bot and client respectively. Optional, defaults to `"me"`. If using `"bot"`, `BOT_TOKEN` variable must be set in the `.env` file.
  - `sender`: name of the client, which will send new messages to the specified destinations. One of `"bot"` or `"me"` for bot and client respectively. Optional, defaults to `"me"`. If using `"bot"`, `BOT_TOKEN` variable must be set in the `.env` file.
  - `use_listener_on_fail`: if True, if sender fails to forward the message, then listener tries to forward it instead. Otherwise, skips the message.  
  
### 3. Define filters
You need to implement all the required filters in the `telegram_pipe/filters.py` file. 

To write a filter, just create a class, inherited from `filter_utils.CustomFilter`, and implement the following methods:
 - `__init__` (optional) - here you can provide all the neccessary data that can influence filter behaviour.
 - `func(self, text: str) -> bool` - the main functionality of the filter, if returns True, the message will be forwarded. 

Currently, only text filters are allowed.

Here is a sample `WordLookupFilter` that can filter messages by positive (select if contains a word) and negative (skip if contains a word) lookups:
```python
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
```

### 4. Install dependencies
The project uses poetry, and all the dependency management could be solved easily using it. First, install (if not yet) `poetry`:
```bash
pip install poetry
```

Then, install the project dependencies. Run this command from the project's root directory:
```bash
poetry install
```

### 5. Run the client
Now you are ready to run the client:
```bash
poetry run python3 telegram_pipe/main.py
```


## Other
The client is implemented using the Pyrogram MTProto client. Logging is handled by `loguru` and by default it goes to the stdout.

  
  


