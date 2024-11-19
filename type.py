from typing import TypedDict

import pandas as pd

Info = TypedDict('Info', 
                 {'name': str, 
                  'nvars': str,
                  'nobs': int,
                  'src': str,
                  'vars': pd.DataFrame,
                  })
