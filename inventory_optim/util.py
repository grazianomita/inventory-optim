import random
import numpy as np
import pandas as pd


class SyntheticInventoryData:
    @staticmethod
    def generate(num_rows=1000, random_seed=17):
        """
        Generate a synthetic inventory data with the following columns: id, category, region, store, unit_price,
        gross_margin. Here we assume that 10% of the items in the inventory have much higher demand than the rest.
        Such items have also a lower gross margin than the low demand items.

        :param num_rows: number of items in the inventory
        :param random_seed: random seed
        :return: pandas dataframe containing the list of items in the inventory
        """
        np.random.seed(random_seed)
        random.seed(random_seed)
        ids = np.arange(1, num_rows + 1)
        categories = np.random.choice(['A', 'B', 'C'], size=num_rows)
        regions = np.random.choice(['R1', 'R2', 'R3'], size=num_rows)
        stores = np.random.randint(1, 21, size=num_rows)  # Assuming there are 100 stores
        unit_price = np.random.normal(4, 3, size=num_rows)
        high_demand_quantity = np.random.normal(200, 150, size=num_rows // 10)  # 10% of items have high demand
        low_demand_quantity = np.random.normal(20, 15, size=num_rows - (num_rows // 10))
        quantity = np.concatenate([high_demand_quantity, low_demand_quantity])
        high_demand_margin = np.random.uniform(0.03, 0.02, size=num_rows // 10)  # Lower gross margin for high demand items
        low_demand_margin = np.random.uniform(0.2, 0.05, size=num_rows - (num_rows // 10))
        gross_margin = np.concatenate([high_demand_margin, low_demand_margin])
        df = pd.DataFrame({
            'category': categories,
            'region': regions,
            'store': stores,
            'quantity': quantity,
            'unit_price': unit_price,
            'gross_margin': gross_margin
        })
        cols = df.columns.tolist()
        df['quantity'] = np.ceil(df['quantity'])
        df['quantity'] = df['quantity'].apply(lambda x: 0 if x < 0 else x)
        df['unit_price'] = df['unit_price'].apply(lambda x: 0.5 if x < 0.5 else x)
        df['gross_margin'] = df['gross_margin'].apply(lambda x: 0 if x < 0 else x)
        df = df.sample(frac=1).reset_index(drop=True)
        df['id'] = df.reset_index().index + 1
        df = df[['id'] + cols]
        df['gross_profit'] = df['gross_margin'] * df['unit_price']
        return df