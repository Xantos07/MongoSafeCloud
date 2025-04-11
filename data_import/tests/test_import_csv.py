import unittest
import sys
import pandas as pd
sys.path.append("..")
from import_csv import addition, import_data_to_mongo, connect_to_mongo
from unittest.mock import patch, MagicMock

print("✅ Start PYTHON TEST !")

class TestImportCSV(unittest.TestCase):

    # Test d'une fonction pour pour voir si cela fonctionne 
    def test_addition(self):
        self.assertEqual(addition(2, 3), 5)
        self.assertEqual(addition(-1, 1), 0)

    @patch('import_csv.connect_to_mongo')  
    @patch('pandas.read_csv')  
    def test_import_data_to_mongo(self, mock_read_csv, mock_connect):
        mock_read_csv.return_value = pd.DataFrame([{"col1": "value1", "col2": "value2"}])

        mock_client = MagicMock()
        mock_connect.return_value = mock_client
        
        mock_db = MagicMock()
        mock_collection = MagicMock()
        
        mock_client.__getitem__.return_value = mock_db  
        mock_db.__getitem__.return_value = mock_collection  
        
 
        import_data_to_mongo()

        mock_read_csv.assert_called_once_with("/app/data/dataset.csv")

        mock_collection.insert_many.assert_called_once_with([{"col1": "value1", "col2": "value2"}])




print("✅ END PYTHON TEST !")
if __name__ == '__main__':
     unittest.main()    
