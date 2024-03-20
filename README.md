# Inventory Optimization

This Python project aims to optimize the inventory management of a retailer taking into account various constraints. 

- The optimization solver used in this project is Highs. 
- In real scenarios, variable bounds and constraints are set up based on demand forecasts and business objectives. 
- Additionally, to ensure solutions are aligned with business objectives, the optimization process usually runs on data coming from a 
  reference period that closely resembles the expected item distribution.
- Specific preprocessing may also be applied before running the optimization.

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/grazianomita/<repo_name>.git
   cd <repo_name>
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Optimization

The optimizer runs via `main.py`. 

#### Input parameters

You can check the required parameters by running the following command:

```bash
python main.py --help
```

#### Running example

Run the optimizer:

```bash
python main.py --data data/sample_data.csv --constraints=data/sample_constraints.json --optim-col=gross_profit --var-col=quantity --export-solution=data/example/res.csv --export-statistics=data/example/statistics.json
```

#### Reference data

The optimizer requires input raw data representing the optimization instance. 

- Such data should contain the dimensions of interest. In the data sample we have:
  - id, category, region, store 
  - quantity
  - unit_price, gross_margin, gross_profit

#### Constraints data

Constraints are defined into a json file.
The json file must follow a specific format, where each constraint has:

- a list of feature names and their corresponding values defining the constraint scope
  - when multiple feature-value pairs are specified for the same constraint, they are combined via the **AND** operator
- a lower bound and an upper bound expressing the volume in TEUs for the constraint scope

```json
{
  "constraints": [{
      "lb": 1200,
      "ub": 1250,
      "features": [
        {"name": "store", "values": [1]}
      ]
    }, {
      "lb": 100,
      "ub": 150,
      "features": [
        {"name": "category", "values": ["B"]},
        {"name": "region", "values": ["R1"]}
      ]
    }, {
      "lb": 39000,
      "ub": 39000,
      "features": []
    }
  ]
}
```

- The json example above translates into the following constraints:
  - Quantity set for `store 1` must be between `1200` and `1250`
  - Quantity set for `category B` and `region R1` must be between `100` and `150`
  - Quantity for the whole `inventory` must be exactly `39000`

#### Output

The result of the optimization is stored into a csv file.
Statistics about the optimization instance are provided into a separate json file.

#### Demo

[Jupyter Notebook](./notebooks/demo.ipynb)