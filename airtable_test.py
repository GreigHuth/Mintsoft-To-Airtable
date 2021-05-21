from config import USERNAME, PASS, AIRTABLE_KEY, BASE_KEY, TABLE
from tqdm import tqdm
import json
from airtable import Airtable


test_data = [
    {'SKU': 'SNAG-30-CARAMEL-C', 'SOLD YESTERDAY': 100, 'ONHAND': 10, 'BACKORDERS': 5},
    {'SKU': 'SNAG-30-CARAMEL-D', 'SOLD YESTERDAY': 36, 'ONHAND': 143, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-CARAMEL-E', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 56},
    {'SKU': 'SNAG-30-CARAMEL-F', 'SOLD YESTERDAY': 40, 'ONHAND': 490, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-CARAMEL-G', 'SOLD YESTERDAY': 1, 'ONHAND': 438, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-LIQUORICE-C', 'SOLD YESTERDAY': 7, 'ONHAND': 63, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-LIQUORICE-D', 'SOLD YESTERDAY': 3, 'ONHAND': 585, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-LIQUORICE-E', 'SOLD YESTERDAY': 5, 'ONHAND': 1382, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-LIQUORICE-F', 'SOLD YESTERDAY': 13, 'ONHAND': 774, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-LIQUORICE-G', 'SOLD YESTERDAY': 1, 'ONHAND': 607, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-PRALINE-C', 'SOLD YESTERDAY': 0, 'ONHAND': 376, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-PRALINE-D', 'SOLD YESTERDAY': 0, 'ONHAND': 1408, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-PRALINE-E', 'SOLD YESTERDAY': 0, 'ONHAND': 2276, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-PRALINE-F', 'SOLD YESTERDAY': 0, 'ONHAND': 495, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-PRALINE-G', 'SOLD YESTERDAY': 0, 'ONHAND': 833, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-VANILLA-C', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 85},
    {'SKU': 'SNAG-30-VANILLA-D', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 65},
    {'SKU': 'SNAG-30-VANILLA-E', 'SOLD YESTERDAY': 2, 'ONHAND': 16, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-VANILLA-F', 'SOLD YESTERDAY': 43, 'ONHAND': 66, 'BACKORDERS': 0},
    {'SKU': 'SNAG-30-VANILLA-G', 'SOLD YESTERDAY': 8, 'ONHAND': 295, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-BLACK-F', 'SOLD YESTERDAY': 47, 'ONHAND': 2462, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-BLACK-G', 'SOLD YESTERDAY': 7, 'ONHAND': 1402, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-BLUEBERRY-F', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-BLUEBERRY-G', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-BUILDERS-F', 'SOLD YESTERDAY': 5, 'ONHAND': 7848, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-BUILDERS-G', 'SOLD YESTERDAY': 3, 'ONHAND': 817, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-BURGUNDY-F', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-BURGUNDY-G', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-HOTCHOC-F', 'SOLD YESTERDAY': 0, 'ONHAND': 1545, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-HOTCHOC-G', 'SOLD YESTERDAY': 0, 'ONHAND': 535, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-NAVY-F', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-NAVY-G', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-SLATE-F', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-SLATE-G', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 0},
    {'SKU': 'SNAG-50-LEMONADE-F', 'SOLD YESTERDAY': 0, 'ONHAND': 0, 'BACKORDERS': 0}
]


airtable = Airtable(BASE_KEY, TABLE, AIRTABLE_KEY)

buffer = airtable.get_all()

for item in test_data:
    
    record = airtable.match('SKU', item['SKU'])
    if record == {}:
        airtable.insert(item)
    else:
        airtable.update(record['id'], item)


