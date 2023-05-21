# various manual mocks

import json
from services.util.async_iterable_list import AsyncIterableList
from services.util.attribute_dict import AttributeDict

# includes "==" base64 padding
MOCK_ENCODED_STR = "eyIxMTExMTEiOiB7ImNpc3NwIjogeyJjb3JyZWN0IjogNSwgImluY29ycmVjdCI6IDF9LCAiY2VoIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAiY2NuYSI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImFwbHVzIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDF9LCAibmV0cGx1cyI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImxpbnV4cGx1cyI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgInNlY3BsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJxdWl6IjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9fSwgIjIyMjIyMiI6IHsiY2lzc3AiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJjZWgiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJjY25hIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAiYXBsdXMiOiB7ImNvcnJlY3QiOiAxLCAiaW5jb3JyZWN0IjogMH0sICJuZXRwbHVzIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAibGludXhwbHVzIjogeyJjb3JyZWN0IjogMiwgImluY29ycmVjdCI6IDB9LCAic2VjcGx1cyI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgInF1aXoiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMX19LCAiMzMzMzMzIjogeyJjaXNzcCI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImNlaCI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImNjbmEiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJhcGx1cyI6IHsiY29ycmVjdCI6IDEsICJpbmNvcnJlY3QiOiAwfSwgIm5ldHBsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJsaW51eHBsdXMiOiB7ImNvcnJlY3QiOiAyLCAiaW5jb3JyZWN0IjogMH0sICJzZWNwbHVzIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAicXVpeiI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAxfX0sICI0NDQ0NDQiOiB7ImNpc3NwIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAiY2VoIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAiY2NuYSI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImFwbHVzIjogeyJjb3JyZWN0IjogMSwgImluY29ycmVjdCI6IDB9LCAibmV0cGx1cyI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImxpbnV4cGx1cyI6IHsiY29ycmVjdCI6IDIsICJpbmNvcnJlY3QiOiAwfSwgInNlY3BsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJxdWl6IjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDF9fX0="

half_mock_encoded_str_length = len(MOCK_ENCODED_STR) // 2

MOCK_ENCODED_STR_CHUNKS = [
    MOCK_ENCODED_STR[:half_mock_encoded_str_length],
    MOCK_ENCODED_STR[half_mock_encoded_str_length:],
]

MOCK_DISCORD_LEADERBOARD_MESSAGE = AttributeDict(
    {
        "author": "MOCK_BOT_ID",
        "embeds": [
            AttributeDict(
                {
                    "fields": [
                        AttributeDict(
                            {
                                "name": "chunk:0",
                                "value": "```" + MOCK_ENCODED_STR_CHUNKS[0] + "```",
                            }
                        ),
                        AttributeDict(
                            {
                                "name": "chunk:1",
                                "value": "```" + MOCK_ENCODED_STR_CHUNKS[1] + "```",
                            }
                        ),
                    ]
                }
            ),
        ],
    }
)


def MOCK_DISCORD_CHANNEL_HISTORY():
    return AsyncIterableList([MOCK_DISCORD_LEADERBOARD_MESSAGE])


MOCK_DISCORD_CHANNEL = AttributeDict({"history": MOCK_DISCORD_CHANNEL_HISTORY})
MOCK_DISCORD_CLIENT = AttributeDict({"user": "MOCK_BOT_ID"})

MOCK_USER_SCORES = json.loads(
    """
{
  "111111": {
    "cissp": {
      "correct": 5,
      "incorrect": 1
    },
    "ceh": {
      "correct": 0,
      "incorrect": 0
    },
    "ccna": {
      "correct": 0,
      "incorrect": 0
    },
    "aplus": {
      "correct": 0,
      "incorrect": 1
    },
    "netplus": {
      "correct": 0,
      "incorrect": 0
    },
    "linuxplus": {
      "correct": 0,
      "incorrect": 0
    },
    "secplus": {
      "correct": 0,
      "incorrect": 0
    },
    "quiz": {
      "correct": 0,
      "incorrect": 0
    }
  },
  "222222": {
    "cissp": {
      "correct": 0,
      "incorrect": 0
    },
    "ceh": {
      "correct": 0,
      "incorrect": 0
    },
    "ccna": {
      "correct": 0,
      "incorrect": 0
    },
    "aplus": {
      "correct": 1,
      "incorrect": 0
    },
    "netplus": {
      "correct": 0,
      "incorrect": 0
    },
    "linuxplus": {
      "correct": 2,
      "incorrect": 0
    },
    "secplus": {
      "correct": 0,
      "incorrect": 0
    },
    "quiz": {
      "correct": 0,
      "incorrect": 1
    }
  },
  "333333": {
    "cissp": {
      "correct": 0,
      "incorrect": 0
    },
    "ceh": {
      "correct": 0,
      "incorrect": 0
    },
    "ccna": {
      "correct": 0,
      "incorrect": 0
    },
    "aplus": {
      "correct": 1,
      "incorrect": 0
    },
    "netplus": {
      "correct": 0,
      "incorrect": 0
    },
    "linuxplus": {
      "correct": 2,
      "incorrect": 0
    },
    "secplus": {
      "correct": 0,
      "incorrect": 0
    },
    "quiz": {
      "correct": 0,
      "incorrect": 1
    }
  },
  "444444": {
    "cissp": {
      "correct": 0,
      "incorrect": 0
    },
    "ceh": {
      "correct": 0,
      "incorrect": 0
    },
    "ccna": {
      "correct": 0,
      "incorrect": 0
    },
    "aplus": {
      "correct": 1,
      "incorrect": 0
    },
    "netplus": {
      "correct": 0,
      "incorrect": 0
    },
    "linuxplus": {
      "correct": 2,
      "incorrect": 0
    },
    "secplus": {
      "correct": 0,
      "incorrect": 0
    },
    "quiz": {
      "correct": 0,
      "incorrect": 1
    }
  }
}
"""
)
