"""transform_maps - provides dictionaries which define the mapping of various fields to more human-readable values"""

model_map = {
    "ACURITE-606TX": "ACURITE-606TX",
    "Acurite-606TX": "ACURITE-606TX",
    "INFACTORY-TH": "SMARTRO-SC91",
}

id_map = {
    169: {
        "idx": "SC91-A",
        "name": "OFC-A",
    },
    167: {
        "idx": "SC91-B",
        "name": "PATIO-B",
    },
    211: {
        "idx": "SC91-C",
        "name": "PATIO-C",
    },
    49: {
        "idx": "ACRT-01",
        "name": "OFC-ACRT",
    },
}

"""
id_map = {
    "169": "SC91-A",
    169: "SC91-A",
    "167": "SC91-B",
    167: "SC91-B",
    "211": "SC91-C",
    211: "SC91-C",
    "49": "ACRT-01",
    49: "ACRT-01",
}
"""

"""
name_map = {
    "169": "OFC-A",
    169: "OFC-A",
    "167": "PATIO-B",
    167: "PATIO-B",
    "211": "PATIO-C",
    211: "PATIO-C",
    "49": "OFC-ACRT",
    49: "OFC-ACRT",
}
"""
