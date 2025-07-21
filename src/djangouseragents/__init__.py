VERSION_MAJOR = 0
VERSION_MINOR = 0
PATCH_VERSION_MAJOR = 1

__version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{PATCH_VERSION_MAJOR}"

USERAGENTS_ADMIN_ORDERING = [
    (
        'djangouseragents',
        [
            'UserAgentDevice',
            'UserAgentRequest',
        ],
    ),
]
