NTAG213 = "213"
NTAG215 = "215"
NTAG216 = "216"

IC_CHOICES = (
    (NTAG213, "NTAG 213"),
    (NTAG215, "NTAG 215"),
    (NTAG216, "NTAG 216"),
)

EEPROM_SIZE = {
    NTAG213: 180,
    NTAG215: 540,
    NTAG216: 924,
}

# Roles
DESIGNERS = "NTAG Designers"
DESIGNER_PERMISSIONS = [
    "view_nfctagdesign",
    "add_nfctagdesign", "change_nfctagdesign", "delete_nfctagdesign",
    "lock_nfctagdesign", "unlock_nfctagdesign",
    "publish_nfctagdesign",
]

DEVELOPERS = "NTAG Developers"
DEVELOPER_PERMISSIONS = [
    "view_nfctageeprom",
    "add_nfctageeprom", "change_nfctageeprom", "delete_nfctageeprom",
    "lock_nfctageeprom", "unlock_nfctageeprom",
    "publish_nfctageeprom"
]

USERS = "NTAG Users"
USER_PERMISSIONS = [
    "view_nfctag", "change_nfctag",
    "view_nfctagdesign",
    "view_nfctagscan",
    "view_nfctageeprom",
]

GROUPS = {
    DESIGNERS: DESIGNER_PERMISSIONS,
    DEVELOPERS: DEVELOPER_PERMISSIONS,
    USERS: USER_PERMISSIONS
}