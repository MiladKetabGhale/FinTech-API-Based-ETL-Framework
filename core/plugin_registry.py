"""
register plugin components (ingestion, validation, transformation) 
for each supported data source.

the PLUGINS dictionary maps a source name to its corresponding classes.
"""

from plugins.vantage.ingestion import VantageIngestion
from plugins.vantage.validation import VantageValidation
from plugins.vantage.transformation import VantageTransformation

from plugins.finnhub.ingestion import FinnhubIngestion
from plugins.finnhub.validation import FinnhubValidation
from plugins.finnhub.transformation import FinnhubTransformation

from plugins.fmp.ingestion import FMPIngestion
from plugins.fmp.validation import FMPValidation
from plugins.fmp.transformation import FMPTransformation

PLUGINS = {
    "vantage": {
        "ingestion": VantageIngestion,
        "validation": VantageValidation,
        "transformation": VantageTransformation
    },
    "finnhub": {
        "ingestion": FinnhubIngestion,
        "validation": FinnhubValidation,
        "transformation": FinnhubTransformation
    },
    "fmm": {
        "ingestion": FMPIngestion,
        "validation": FMPValidation,
        "transformation": FMPTransformation
    }
}

