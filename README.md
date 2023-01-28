# telegram-pipe
An MTProto telegram client, that allows you to collect messages from a set of source chats and channels, filter messages by some set of rules and then forward them into specified destination chats.

## Sample usecases
- Collect specified (e.g. "python middle developer") job vacancies from a set of telegram channels and forward them into one chat.
- Collect selected messages into a database and build a recommender system.
- Creating a news feed.

## Usage
### 1. Create `.env` file
It should contain `API_ID` and `API_HASH` for your telegram account. [Here](https://core.telegram.org/api/obtaining_api_id) is an official guide on how to get them. Here is also an `.env-example` file, that specifies the format.

### 2. Add pipelines 
Open `pipelines.yaml` and add your pipelines in the `yaml` format. Here is an example:
```yaml
pipes:
  - name: Job Extractor
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
```

Each pipe has 4 fields:
  - `name`: name of the pipe, may be anything, it's here just for convenience.
  - `sources`: list of telegram chats\channel IDs to listen for. Each ID should be either in the format of `"@channel_name"` or integer ID. You can obtain chat ID [by inviting @RawDataBot to your group](https://stackoverflow.com/a/46247058). To send messages to "Saved Messages" (yourself), just put "me" to the list.
  - `destinations`: list of telegram chats\channel IDs to forward messages to. Each ID should be either in the format of `"@channel_name"` or integer ID.
  - `filters`: names of the filters to use. Filters should be defined in the `telegram_pipe/filters.py` file.
  
### 3. Define filters
You need to implement all the required filters in the `telegram_pipe/filters.py` file. Here is a sample `word_lookup_filter` that can filter messages by positive (select if contains a word) and negative (skip if contains a word) lookups. 

### 4. Install dependencies
The project uses poetry, and all the dependency management could be solved easily using it. First, install (if not yet) `poetry`:
```bash
pip install poetry
```

Then, install the project dependencies. Run this command from the project's root directory:
```bash
poetry install
```

Now you are ready to run the client:
```bash
poetry run python3 telegram_pipe/client.py
```


## Other
The client is implemented using the Pyrogram MTProto client. Logging is handled by `loguru` and by default it goes to the stdout.

  
  


